'''
Created on 10-mrt.-2014

@author: Simon
'''
from mvk.impl.python.changelog import MvKCompositeLog, MvKLog, MvKUpdateLog, \
    MvKDeleteLog
from mvk.impl.python.constants import CreateConstants, UpdateConstants, \
    CRUDConstants, TransformationConstants,RuleExecutionConstants
from mvk.impl.python.datavalue import StringValue, LocationValue, IntegerValue, \
    MappingValue, BooleanValue, SequenceValue, DataValueFactory, InfiniteValue
from mvk.impl.python.object import ClabjectReference
from mvk.impl.python.python_representer import PythonRepresenter
import mvk.interfaces.datavalue
from mvk.mvk import MvK
from mvk.util.logger import get_logger
from mvk.impl.python.object import Model, ModelReference, Clabject, ClabjectReference, Attribute, Association, AssociationEnd, AssociationReference, Inherits, \
    Composition
from mvk.impl.python.datatype import IntegerType, SequenceType, StringType, TypeFactory, BooleanType, FloatType, TypeType, AnyType, InfiniteType,MappingType, LocationType
#from mvk.util import draw
from mvk.util.seeded_random import Random
from mvk.plugins.transformation.mt import ramify_scd

logger = get_logger('match_rewrite')


class Scheduler(object):
    def __init__(self, t_loc):
        assert isinstance(t_loc, mvk.interfaces.datavalue.LocationValue)
        self.t = MvK().read(t_loc).get_item()
        rule_type = MvK().read(LocationValue('protected.formalisms.Transformation.Rule')).get_item()
        self.r = None
        it = self.t.get_elements().__iter__()
        while it.has_next():
            el = self.t.get_element(it.next())
            if rule_type.is_type_of(el):
                self.r = MvK().read(el.get_attribute(StringValue('Rule.rule_loc')).get_value()).get_item()
                break  # TODO: Support multiple rules.
        assert self.r
        self.rule_applied = None

    def done(self):
        return self.rule_applied is not None

    def next_rule(self):
        self.rule_applied = None
        return self.r

    def set_rule_applied(self, applied):
        assert isinstance(applied, bool)
        self.rule_applied = applied

    def has_rule_applied(self):
        return self.rule_applied



class State(object):
    def __init__(self, m_loc, rule):
        self.r = rule
        self.m = MvK().read(m_loc).get_item()
        self.lhs = None
        self.rhs = None
        self.nacs = []
        lhs_type = MvK().read(LocationValue('protected.formalisms.Rule.LHS')).get_item()
        nac_type = MvK().read(LocationValue('protected.formalisms.Rule.NAC')).get_item()
        rhs_type = MvK().read(LocationValue('protected.formalisms.Rule.RHS')).get_item()
        it = self.r.get_elements().__iter__()
        while it.has_next():
            el = self.r.get_element(it.next())
            if lhs_type.is_type_of(el):
                self.lhs = el
            elif nac_type.is_type_of(el):
                self.nacs.append(el)
            elif rhs_type.is_type_of(el):
                self.rhs = el
        assert self.lhs
        self.curr_nac_idx = 0

    def create_matcher_lhs(self):
        return Matcher(self.m, self.lhs)

    def set_lhs_matches(self, matches):
        self.lhs_matches = matches

    def lhs_matches_left(self):
        return len(self.lhs_matches)

    def select_lhs_match(self):
        self.curr_lhs_match = self.lhs_matches.pop()
        self.curr_nac_idx = 0

    def get_current_lhs_match(self):
        return self.curr_lhs_match

    def nacs_left(self):
        return self.curr_nac_idx < len(self.nacs)

    def next_nac(self):
        self.curr_nac = self.nacs[self.curr_nac_idx]
        self.curr_nac_idx += 1

    def create_matcher_nac(self):
        return Matcher(self.m, self.curr_nac, self.curr_lhs_match)

    def create_rewriter(self):
        assert not self.nacs_left()
        return Rewriter(self.m, self.curr_lhs_match, self.rhs)


class Match(dict):
    def __init__(self, matcher, initial_match={}):
        assert isinstance(initial_match, dict)
        assert isinstance(matcher, Matcher)
        self.matcher = matcher
        self.suggested_mappings = {}
        for k, v in initial_match.iteritems():
            self[k] = v

    def can_extend(self):
        assert logger.debug('PARTIAL MATCH %s (len needed = %s + %s)' %
                            (self, len(self.matcher.p_nodes), len(self.matcher.p_edges)))
        if len(self) == len(self.matcher.p_nodes) + len(self.matcher.p_edges):
            return False
        keys_used = self.keys()
        self.next_key = sorted(list((set(self.matcher.p_nodes.keys()) | set(self.matcher.p_edges.keys())) - set(keys_used)))[0]
        assert logger.debug('NEXT KEY: %s' % self.next_key)
        if not self.next_key in self.suggested_mappings:
            key_suggestions = []
            p_el = self.matcher.p_edges[self.next_key] if self.next_key in self.matcher.p_edges else self.matcher.p_nodes[self.next_key]
            for s_el in self.matcher.s_edges + self.matcher.s_nodes:
                if self.matcher.is_feasible(self, p_el, s_el):
                    assert logger.debug('%s is a feasible match for %s' %
                                        (s_el.get_name(), self.next_key))
                    key_suggestions.append(s_el)
                else:
                    assert logger.debug('%s is not a feasible match for %s' %
                                        (s_el.get_name(), self.next_key))
            self.suggested_mappings[self.next_key] = key_suggestions
        assert logger.debug('SUGGESTED MAPPINGS: %s' %
                            self.suggested_mappings[self.next_key])
        return len(self.suggested_mappings[self.next_key])

    def extend_one_element(self):
        new_match = Match(self.matcher, self)
        new_match[self.next_key] = self.suggested_mappings[self.next_key].pop()
        return new_match


class Matcher(object):
    def __init__(self, host_model, pattern, initial_match={},maxmatches=1):
        self.s = host_model
        self.p = pattern
        self.maxmatches=maxmatches
        self.matches = []

        pattern_class = MvK().read(LocationValue('protected.formalisms.Rule.MTpre_Element')).get_item()
        pattern_association_class = MvK().read(LocationValue('protected.formalisms.Rule.MTpre_Association')).get_item()
        pattern_content_class = MvK().read(LocationValue('protected.formalisms.Rule.MTpre_Contents')).get_item()

        self.pattern_contents = []
        it = self.p.get_out_associations().__iter__()
        while it.has_next():
            a = it.next()
            if pattern_content_class.is_type_of(a):
                self.pattern_contents.append(a.get_to_multiplicity().get_node())

        self.p_nodes = {}
        self.p_edges = {}
        for p_c in self.pattern_contents:
            if isinstance(p_c, mvk.interfaces.object.Association):
                if pattern_association_class.is_type_of(p_c):
                    self.p_edges[p_c.get_attribute(StringValue('MT_Element.MT_label')).get_value()] = p_c
            elif isinstance(p_c, mvk.interfaces.object.Clabject):
                if pattern_class.is_type_of(p_c):
                    self.p_nodes[p_c.get_attribute(StringValue('MT_Element.MT_label')).get_value()] = p_c

        self.initial_match = Match(self, initial_match)
        to_delete = []
        for k in self.initial_match:
            if not (k in self.p_nodes or k in self.p_edges):
                to_delete.append(k)
        for k in to_delete:
            del self.initial_match[k]

        self.s_nodes = []
        self.s_edges = []
        it = self.s.get_elements().__iter__()
        while it.has_next():
            el = self.s.get_element(it.next())
            if isinstance(el, mvk.interfaces.object.Association):
                self.s_edges.append(el)
            elif isinstance(el, mvk.interfaces.object.Clabject):
                self.s_nodes.append(el)

    def get_initial_match(self):
        return self.initial_match

    def exhausted(self):
        try:
            self.curr_suggested_mapping = self.suggested_mappings.next()
            return False
        except StopIteration:
            return True

    #process nacs as we get matches vs get all matches first then invalidate (old)
    def match_pattern2(self,state):
        stack = []
        stack.append(self.get_initial_match())
        while not len(stack) == 0:
            if not self.maxmatches == -1 and IntegerValue(len(self.matches)) == self.maxmatches:
                break #enough matches
            assert logger.debug('STACK BEFORE: %s' % stack)
            partial_match = stack[-1]
            if partial_match.can_extend():
                next_partial = partial_match.extend_one_element()
                stack.append(next_partial)
            else:
                match = stack.pop()
                valid = True
                if len(match) == len(self.get_pattern_contents()):
                    res =  self.__store_match(match)
                    if res:
                        state.curr_lhs_match = match
                        while state.nacs_left():
                            state.next_nac()
                            nac_matcher = state.create_matcher_nac()
                            nac_matcher.match_pattern()
                            if len(nac_matcher.get_matches()) != 0:
                                #valid = False
                                self.matches.pop()
                                break
                    #if valid:
                        #self.__store_match(match)
                
            assert logger.debug('STACK AFTER: %s' % stack)
    def match_pattern(self):
        stack = []
        stack.append(self.get_initial_match())
        while not len(stack) == 0:
            if len(self.matches) == self.maxmatches:
                break #enough matches
            assert logger.debug('STACK BEFORE: %s' % stack)
            partial_match = stack[-1]
            if partial_match.can_extend():
                next_partial = partial_match.extend_one_element()
                stack.append(next_partial)
            else:
                match = stack.pop()
                if len(match) == len(self.get_pattern_contents()):
                    self.__store_match(match)
                
            assert logger.debug('STACK AFTER: %s' % stack)

    def __store_match(self, match):
        for k in match:
            it = (self.p_nodes[k] if k in self.p_nodes else self.p_edges[k]).get_attributes().__iter__()
            while it.has_next():
                attr = it.next()
                if attr.get_name() != StringValue('MT_Element.MT_label') and attr.get_name() != StringValue('MT_Element.id'):
                    assert isinstance(attr.get_value(), mvk.interfaces.datavalue.StringValue)
                    if not eval(str(attr.get_value())):
                        return False

        lhs_constraint = self.p.get_attribute(StringValue('MTpre_Pattern.MT_constraint')).get_value()
        if self.matches.count(match) == 0 and eval(str(lhs_constraint)):
            self.matches.append(match)
            return True

    def is_feasible(self, partial_match, p_el, s_el):
        if isinstance(p_el, mvk.interfaces.object.Association):
            if not isinstance(s_el, mvk.interfaces.object.Association):
                assert logger.debug('%s is an Association, but %s is not!' %
                                    (p_el.get_name(), s_el.get_name()))
                return False
        elif isinstance(s_el, mvk.interfaces.object.Association):
            if not isinstance(p_el, mvk.interfaces.object.Association):
                assert logger.debug('%s is an Association, but %s is not!' %
                                    (p_el.get_name(), s_el.get_name()))
                return False

        def is_type_compatible(p_el, s_el):
            types = [s_el.typed_by()]
            super_classes = s_el.typed_by().get_all_super_classes()
            it = super_classes.__iter__()
            while it.has_next():
                types.append(it.next())
            p_type_name = p_el.typed_by().get_name().substring(start=IntegerValue(6))

            assert logger.debug('looking for type %s in %s' %
                                (p_type_name, types))

            for t in types:
                if t.get_name() == p_type_name:
                    return True

            return False

        if not is_type_compatible(p_el, s_el):
            assert logger.debug('%s is not type compatible with %s' %
                                (s_el.get_name(), p_el.get_name()))
            return False

        ''' Mp and Ms after lhs_el and host_el are added. '''
        f_m_p = [self.p_nodes[l] if l in self.p_nodes else self.p_edges[l] for l in partial_match] + [p_el]  # Mp
        f_m_s = partial_match.values() + [s_el]  # Ms

        f_m_p = set(f_m_p)
        f_m_s = set(f_m_s)

        out_lhs = set()  # out(p)
        in_lhs = set()   # in(p)

        if isinstance(p_el, mvk.interfaces.object.Association):
            out_lhs.add(p_el.get_to_multiplicity().get_node())
            in_lhs.add(p_el.get_from_multiplicity().get_node())
        elif isinstance(p_el, mvk.interfaces.object.Clabject):
            it = p_el.get_out_associations().__iter__()
            while it.has_next():
                out_lhs.add(it.next())
            it = p_el.get_in_associations().__iter__()
            while it.has_next():
                a = it.next()
                if a.get_from_multiplicity().get_node() in self.p_nodes.values():  # extra check to avoid adding associations coming from the precondition pattern
                    in_lhs.add(a)

        out_host = set()  # out(s)
        in_host = set()   # in(s)

        if isinstance(s_el, mvk.interfaces.object.Association):
            out_host.add(s_el.get_to_multiplicity().get_node())
            in_host.add(s_el.get_from_multiplicity().get_node())
        elif isinstance(s_el, mvk.interfaces.object.Clabject):
            it = s_el.get_out_associations().__iter__()
            while it.has_next():
                out_host.add(it.next())
            it = s_el.get_in_associations().__iter__()
            while it.has_next():
                in_host.add(it.next())

        if len(out_lhs) > len(out_host):
            assert logger.debug('out_lhs (%s) > out_host (%s)' %
                                (out_lhs, out_host))
            return False
        elif len(in_lhs) > len(in_host):
            assert logger.debug('in_lhs (%s) > in_host (%s)' %
                                (in_lhs, in_host))
            return False
        elif len(out_lhs & f_m_p) != len(out_host & f_m_s):
            assert logger.debug('out_lhs & f_m_p (%s) > out_host & f_m_s (%s)' %
                                (out_lhs & f_m_p, out_host & f_m_s))
            return False
        elif len(in_lhs & f_m_p) != len(in_host & f_m_s):
            assert logger.debug('in_lhs & f_m_p (%s) > in_host & f_m_s (%s)' %
                                (in_lhs & f_m_p, in_host & f_m_s))
            return False

        in_lhs_mapped = set([partial_match[s.get_attribute(StringValue('MT_Element.MT_label')).get_value()] for s in in_lhs if s.get_attribute(StringValue('MT_Element.MT_label')).get_value() in partial_match])
        out_lhs_mapped = set([partial_match[s.get_attribute(StringValue('MT_Element.MT_label')).get_value()] for s in out_lhs if s.get_attribute(StringValue('MT_Element.MT_label')).get_value() in partial_match])
        inout_lhs_mapped = in_lhs_mapped | out_lhs_mapped
        inout_host = in_host | out_host

        if len(in_lhs_mapped - in_host) != 0:
            assert logger.debug('len(in_lhs_mapped - in_host) != 0 (%s)' %
                                (in_lhs_mapped - in_host))
            return False
        elif len(out_lhs_mapped - out_host) != 0:
            assert logger.debug('len(out_lhs_mapped - out_host) != 0 (%s)' %
                                (in_lhs_mapped - in_host))
            return False
        elif len(inout_lhs_mapped - inout_host) != 0:
            assert logger.debug('len(inout_lhs_mapped - inout_host) != 0 (%s)' %
                                (inout_lhs_mapped - inout_host))
            return False

        return True

    def has_matches(self):
        return len(self.matches)

    def get_matches(self):
        return self.matches

    def get_pattern_contents(self):
        return self.pattern_contents


class Rewriter(object):
    def __init__(self, host_model, match, rhs):
        self.host_model = host_model
        self.match = match
        self.rhs = rhs

        self.in_rhs = set()
        self.new_elements = {}

        pattern_class = MvK().read(LocationValue('protected.formalisms.Rule.MTpost_Element')).get_item()
        pattern_association_class = MvK().read(LocationValue('protected.formalisms.Rule.MTpost_Association')).get_item()
        pattern_content_class = MvK().read(LocationValue('protected.formalisms.Rule.MTpost_Contents')).get_item()

        self.rhs_contents = []
        it = rhs.get_out_associations().__iter__()
        while it.has_next():
            a = it.next()
            if pattern_content_class.is_type_of(a):
                self.rhs_contents.append(a.get_to_multiplicity().get_node())

        self.rhs_nodes = {}
        self.rhs_edges = {}
        for r_c in self.rhs_contents:
            if isinstance(r_c, mvk.interfaces.object.Association):
                if pattern_association_class.is_type_of(r_c):
                    self.rhs_edges[r_c.get_attribute(StringValue('MT_Element.MT_label')).get_value()] = r_c
            elif isinstance(r_c, mvk.interfaces.object.Clabject):
                if pattern_class.is_type_of(r_c):
                    self.rhs_nodes[r_c.get_attribute(StringValue('MT_Element.MT_label')).get_value()] = r_c

        self.nodes_to_create = {}
        self.nodes_to_update = {}
        for mt_label in self.rhs_nodes:
            self.in_rhs.add(mt_label)
            if not mt_label in self.match:
                self.nodes_to_create[mt_label] = self.rhs_nodes[mt_label]
            else:
                self.nodes_to_update[mt_label] = self.rhs_nodes[mt_label]

        self.edges_to_create = {}
        self.edges_to_update = {}
        for mt_label in self.rhs_edges:
            self.in_rhs.add(mt_label)
            if not mt_label in self.match:
                self.edges_to_create[mt_label] = self.rhs_edges[mt_label]
            else:
                self.edges_to_update[mt_label] = self.rhs_edges[mt_label]

        in_lhs_not_rhs = list(set(match.keys()) - self.in_rhs)
        self.elements_to_delete = [match[label] for label in in_lhs_not_rhs]
    
    def run(self,*args):
        for string in args:
            #print string
            exec str(string) in globals(), locals()
    
    def done(self):
        return (len(self.nodes_to_create) + len(self.nodes_to_update) +
                len(self.edges_to_create) + len(self.edges_to_update) +
                len(self.elements_to_delete)) == 0

    def rewrite_next_element(self):
        def update_attributes(n, el):
            it = n.get_attributes().__iter__()
            ret_log = MvKCompositeLog()
            while it.has_next():
                rhs_attr = it.next()
                if rhs_attr.get_name().startswith(StringValue('MTpost_')):
                    attr_name = rhs_attr.get_name()
                    idx = attr_name.find(StringValue('.'))
                    if idx == IntegerValue(-1):
                        attr_name = attr_name.substring(start=IntegerValue(7))
                    else:
                        attr_name = (attr_name.substring(start=IntegerValue(7), stop=idx+IntegerValue(1)) +
                                     attr_name.substring(start=idx+IntegerValue(8)))
                    host_attr = el.get_attribute(attr_name)

                    def get_attribute(attr_name=None):
                        if attr_name is None:
                            return host_attr.get_value()
                        else:
                            return el.get_attribute(attr_name).get_value()

                    new_val = eval(str(rhs_attr.get_value()))
                    cl = MvK().update(MappingValue({UpdateConstants.TYPE_KEY: el.typed_by().get_location(),
                                                    UpdateConstants.LOCATION_KEY: el.get_location(),
                                                    UpdateConstants.ATTRS_KEY: MappingValue({host_attr.get_name(): new_val})}))
                    ret_log.add_log(cl)
            ret_log.set_status_code(UpdateConstants.SUCCESS_CODE)
            ret_log.set_status_message(StringValue('Success!'))
            return ret_log

        def compute_attributes(n, t):
            it = n.get_attributes().__iter__()
            ret_val = MappingValue({})
            while it.has_next():
                rhs_attr = it.next()
                if rhs_attr.get_name().startswith(StringValue('MTpost_')):
                    attr_name = rhs_attr.get_name()
                    idx = attr_name.find(StringValue('.'))
                    if idx == IntegerValue(-1):
                        attr_name = attr_name.substring(start=IntegerValue(7))
                    else:
                        attr_name = (attr_name.substring(start=IntegerValue(7), stop=idx+IntegerValue(1)) +
                                     attr_name.substring(start=idx+IntegerValue(8)))

                    def get_attribute():
                        if attr_name.startswith(t.get_name() + StringValue('.')):
                            attr_name_t = attr_name.substring(start=t.get_name().len() + IntegerValue(1))
                        else:
                            attr_name_t = attr_name
                        return t.get_attribute(attr_name_t).get_default()

                    new_val = eval(str(rhs_attr.get_value()))
                    ret_val[attr_name] = new_val
            return ret_val

        if len(self.nodes_to_create) != 0:
            l, n = self.nodes_to_create.popitem()
            ''' RAMified metamodel = MTpost_<mmname> '''
            n_type = n.typed_by()
            mm_ramified_loc = n_type.get_parent().get_location()
            idx = mm_ramified_loc.rfind(StringValue('.'))
            mm_loc = mm_ramified_loc.substring(stop=idx + IntegerValue(1)) + mm_ramified_loc.substring(start=idx + IntegerValue(8))
            l_type = mm_loc + StringValue('.') + n_type.get_name().substring(IntegerValue(7))
            attrs = compute_attributes(n, ClabjectReference(path=l_type))

            cl = MvK().create(MappingValue({CreateConstants.TYPE_KEY: l_type,
                                            CreateConstants.LOCATION_KEY: self.host_model.get_location(),
                                            CreateConstants.ATTRS_KEY: attrs
                                            })
                              )
            if cl.is_success():
                new_el = MvK().read(cl.get_location() + LocationValue('.') + cl.get_name()).get_item()
                self.new_elements[l] = new_el
                self.match[l] = new_el
            return cl
        elif len(self.edges_to_create) != 0:
            l, n = self.edges_to_create.popitem()

        if len(self.nodes_to_create) != 0:
            l, e = self.edges_to_create.popitem()
            ''' RAMified metamodel = MTpost_<mmname> '''
            e_type = e.typed_by()
            mm_ramified_loc = e_type.get_parent().get_location()
            idx = mm_ramified_loc.rfind(StringValue('.'))
            mm_loc = mm_ramified_loc.substring(stop=idx + IntegerValue(1)) + mm_ramified_loc.substring(start=idx + IntegerValue(8))
            l_type = mm_loc + StringValue('.') + e_type.get_name().substring(IntegerValue(7))
            attrs = compute_attributes(n, ClabjectReference(path=l_type))
            from_label = e.get_from_multiplicity().get_node().get_attribute(StringValue('MT_Element.MT_label')).get_value()
            to_label = e.get_to_multiplicity().get_node().get_attribute(StringValue('MT_Element.MT_label')).get_value()
            from_node = self.match[from_label]
            to_node = self.match[to_label]
            attrs[e.get_from_multiplicity().get_port_name()] = from_node.get_location()
            attrs[e.get_to_multiplicity().get_port_name()] = to_node.get_location()

            cl = MvK().create(MappingValue({CreateConstants.TYPE_KEY: l_type,
                                            CreateConstants.LOCATION_KEY: self.host_model.get_location(),
                                            CreateConstants.ATTRS_KEY: attrs
                                            })
                              )
            if cl.is_success():
                new_el = MvK().read(cl.get_location() + LocationValue('.') + cl.get_name()).get_item()
                self.new_elements[l] = new_el
                self.match[l] = new_el
            return cl
        elif len(self.nodes_to_update) != 0:
            l, n = self.nodes_to_update.popitem()
            return update_attributes(n, self.match[l])
        elif len(self.edges_to_update) != 0:
            l, n = self.edges_to_update.popitem()
            return update_attributes(n, self.match[l])
        elif len(self.elements_to_delete) != 0:
            el = self.elements_to_delete.pop()
            return MvK().delete(el.get_location())

    def execute_action(self):
        ret_log = MvKCompositeLog()

        def set_attribute(label, attr_name, new_val):
            el = self.match[label]
            cl = MvK().update(MappingValue({UpdateConstants.TYPE_KEY: el.typed_by(),
                                            UpdateConstants.LOCATION_KEY: el.get_location(),
                                            UpdateConstants.ATTRS_KEY: MappingValue({attr_name: new_val})}))
            ret_log.add_log(cl)
            if not cl.is_succes():
                ret_log.set_status_code(cl.get_status_code())
                ret_log.set_status_message(cl.get_status_message())
                return ret_log

        def get_attribute(label, attr_name):
            el = self.match[label]
            return el.get_attribute(attr_name).get_value()

        exec str(self.rhs.get_attribute(StringValue('MTpost_Pattern.MT_action')).get_value()) in globals(), locals()

        ret_log.set_status_code(CRUDConstants.SUCCESS_CODE)
        ret_log.set_status_message(StringValue('Success!'))
        return ret_log


def get_matches(model_location, transformation_location):
    scheduler = Scheduler(transformation_location)
    rule_matches = {}
    while not scheduler.done():
        rule = scheduler.next_rule()
        state = State(model_location, rule)
        matcher = state.create_matcher_lhs()
        matcher.match_pattern()
        state.set_lhs_matches(matcher.get_matches())
        rule_matches[rule.get_name()] = []
        while state.lhs_matches_left():
            state.select_lhs_match()
            valid_match = True
            while state.nacs_left():
                state.next_nac()
                nac_matcher = state.create_matcher_nac()
                nac_matcher.match_pattern()
                if len(nac_matcher.get_matches()) != 0:
                    valid_match = False
            if valid_match:
                rule_matches[rule.get_name()].append(state.get_current_lhs_match())
        scheduler.set_rule_applied(True)
    return rule_matches


def match_and_rewrite(model_location, transformation_location):
    scheduler = Scheduler(transformation_location)
    cl = MvKCompositeLog()
    while not scheduler.done():
        rule = scheduler.next_rule()
        state = State(model_location, rule)
        matcher = state.create_matcher_lhs()
        matcher.match_pattern()
        state.set_lhs_matches(matcher.get_matches())
        scheduler.set_rule_applied(False)
        while state.lhs_matches_left() and not scheduler.has_rule_applied():
            state.select_lhs_match()
            valid_match = True
            while state.nacs_left():
                state.next_nac()
                nac_matcher = state.create_matcher_nac()
                nac_matcher.match_pattern()
                if len(nac_matcher.get_matches()) != 0:
                    valid_match = False
            if valid_match:
                rewriter = state.create_rewriter()
                while not rewriter.done():
                    next_cl = rewriter.rewrite_next_element()
                    cl.add_log(next_cl)
                    if not next_cl.is_success():
                        cl.set_status_code(next_cl.get_status_code())
                        cl.set_status_message(next_cl.get_status_message())
                        return cl
                ''' TODO: How to receive a log from the action? '''
                a_cl = rewriter.execute_action()
                if not a_cl.is_success():
                    cl.set_status_code(a_cl.get_status_code())
                    cl.set_status_message(a_cl.get_status_message())
                    return cl
                cl.add_log(a_cl)
                cl.set_status_code(CRUDConstants.SUCCESS_CODE)
                cl.set_status_message(StringValue('Success!'))
                scheduler.set_rule_applied(True)
    return cl


def del_attr(el, attr_name):
    if attr_name in el.attributes:
        del el.attributes[attr_name]
        
'''Maris Jukss'''
def set_attribute(el, attr_name, new_val):
    
    cl = MvK().update(MappingValue({UpdateConstants.TYPE_KEY: el.typed_by().get_location(),
                                    UpdateConstants.LOCATION_KEY: el.get_location(),
                                    UpdateConstants.ATTRS_KEY: MappingValue({attr_name: new_val})}))


def execute_transformation(model_location,transformation_location):
    scheduler = Scheduler2(transformation_location)
    rule = scheduler.next_rule(RuleExecutionConstants.SUCCESS_CODE)
    cl = MvKCompositeLog()
    while rule:
        #Need to cache rules!
        state = State2(model_location, rule,scheduler.current_rule_type)
        try:
            matcher = state.create_matcher_lhs(first_match=True) #take value from Rule 
            #try catch here for failure case
            matcher.match_pattern()
            state.set_lhs_matches(matcher.get_matches())
            #draw.Draw.plot( model_location,"_before_")
            if len(state.lhs_matches) == 0:
                rule = scheduler.next_rule(RuleExecutionConstants.NOT_APPLICABLE_CODE)
                continue
            else:
                while state.lhs_matches_left():
                    state.select_lhs_match()
                    valid_match = True
                    while state.nacs_left():
                        state.next_nac()
                        nac_matcher = state.create_matcher_nac(first_match=True)
                        nac_matcher.match_pattern()
                        if len(nac_matcher.get_matches()) != 0:
                            valid_match = False
                    if valid_match:
                        rewriter = state.create_rewriter()
                        while not rewriter.done():
                            next_cl = rewriter.rewrite_next_element()
                            cl.add_log(next_cl)
                            if not next_cl.is_success():
                                cl.set_status_code(next_cl.get_status_code())
                                cl.set_status_message(next_cl.get_status_message())
                                return cl
                        ''' TODO: How to receive a log from the action? '''
                        a_cl = rewriter.execute_action() #treat success here
        except Exception:
            rule = scheduler.next_rule(RuleExecutionConstants.FAILURE_CODE)
            continue
        #draw.Draw.plot( model_location,"_after_")
        rule = scheduler.next_rule(RuleExecutionConstants.SUCCESS_CODE) #in case of success 
    return cl

class Scheduler2(object):
    def __init__(self, t_loc):
        self.stack = []
        self.t = MvK().read(t_loc).get_item()
        self.onsuccess_type = MvK().read(LocationValue('protected.formalisms.MT.OnSuccess')).get_item()
        self.onfailure_type = MvK().read(LocationValue('protected.formalisms.MT.OnFailure')).get_item()
        self.onnotapplicable_type = MvK().read(LocationValue('protected.formalisms.MT.OnNotApplicable')).get_item()
        self.step_type = MvK().read(LocationValue('protected.formalisms.MT.Step')).get_item()
        self.arule = MvK().read(LocationValue('protected.formalisms.MT.ARule')).get_item()
        self.rule = MvK().read(LocationValue('protected.formalisms.MT.ARule')).get_item()
        self.tranf = MvK().read(LocationValue('protected.formalisms.MT.Transformation')).get_item()
        self.current_rule = None
        self.current_step = None
        self.current_rule_type = None
        assert isinstance(t_loc, mvk.interfaces.datavalue.LocationValue)

    def done(self):
        return self.rule_applied is not None
    
    def first_step(self):
        isStart = False
        start_step = None
        it = self.t.get_elements().__iter__()
        while it.has_next():
            el = self.t.get_element(it.next())
            if self.step_type.is_type_of(el):
                if el.get_attribute(StringValue('Step.isStart')).get_value() == BooleanValue(True):
                    if isStart == True:
                        raise Exception("Cannot have several starting points in transformation.")
                    else:
                        isStart = True
                        start_step = el
        return start_step
    
    def next_rule(self,result):
        #We go here is we recurse into transformation blob and find the start point
        if not self.current_step:
            self.current_step = self.first_step()
            if not self.current_step:
                if len(self.stack) > 0:
                    self.current_step = self.stack.pop()
                    #print "No Start Step Pop Stack!"
                    return self.next_rule(result)
                else:
                    #print "No Start Step!"
                    return None
            #pop stack on no first step and return next_step()
            if self.rule.is_type_of(self.current_step):
                self.current_rule = MvK().read(self.current_step.get_attribute(StringValue('Rule.location')).get_value()).get_item()
                self.current_rule_type = self.current_step.typed_by()
                #print "Running Start Step Rule: %s"%self.current_step
                return self.current_rule
            elif self.tranf.is_type_of(self.current_step):
                    self.stack.append(self.current_step)
                    #print "Recurse from %s into Start Step Transf.: %s"%(self.current_step,self.current_step.get_attribute(StringValue('Transformation.location')).get_value())
                    self.t = MvK().read(self.current_step.get_attribute(StringValue('Transformation.location')).get_value()).get_item()
                    self.current_step = None
                    return self.next_rule(result)
        #From here we attempt to open next setp according to the result
        else:
            #print "Begin Current Step: %s"%self.current_step
            if result == RuleExecutionConstants.SUCCESS_CODE:
                next_t = self.onsuccess_type
            elif result == RuleExecutionConstants.NOT_APPLICABLE_CODE:
                next_t = self.onnotapplicable_type
            elif result == RuleExecutionConstants.FAILURE_CODE:
                next_t = self.onfailure_type
            it = self.current_step.get_out_associations().__iter__()
            if not it.has_next():
                if len(self.stack) == 0:
                    #print "No Next Step, No Stack!"
                    return None
                else:
                    #print "No Next Step, Pop Stack!"
                    self.current_step = self.stack.pop()
                    return self.next_rule(result)
            #pop stack on no next step
            while it.has_next():
                el = it.next()
                if next_t.is_type_of(el):
                    exec_num = el.get_attribute(StringValue('Flow.exec_num')).get_value()
                    assert not exec_num < IntegerValue(-1) 
                    if exec_num == IntegerValue(0) :
                        if len(self.stack) == 0:
                            #print "Cannot follow next branch, No Stack!"
                            return None
                        else:
                            #print "Cannot follow next branch, Pop Stack!"
                            self.current_step = self.stack.pop()
                            return self.next_rule(result) 
                    elif exec_num ==IntegerValue(-1) or exec_num > IntegerValue(0) : #go to branch
                        set_attribute(el,StringValue('Flow.exec_num'), exec_num-IntegerValue(1) )
                        self.current_step = el.get_to_multiplicity().get_node()
                        if self.rule.is_type_of(self.current_step):
                            #print "Running Next Step Rule: %s"%self.current_step
                            self.current_rule = MvK().read(self.current_step.get_attribute(StringValue('Rule.location')).get_value()).get_item()
                            self.current_rule_type = self.current_step.typed_by()
                            return self.current_rule
                        elif self.tranf.is_type_of(self.current_step):
                            self.stack.append(self.current_step)
                            self.t = MvK().read(self.current_step.get_attribute(StringValue('Transformation.location')).get_value()).get_item()
                            #print "Recurse from %s into Next Step Transf.: %s"%(self.current_step,self.current_step.get_attribute(StringValue('Transformation.location')).get_value())
                            self.current_step = None
                            return self.next_rule(result)
        
#     '''Next rule based on result: OnSuccess, OnNotApplicable, OnFailure'''
#     '''Error checks: two OnSuccess branches? what to do? Check on construction? Parallel?'''
#     def next_rule(self,result):
#         #return first rule as we do not need to follow branch
#         if not self.rule_applied:
#             self.rule_applied = True
#             return (self.current_rule,self.current_rule_type)
#         '''lets assume for now, return values are succ,na,fail'''
#         if result == 'succ':
#             next_t = self.onsuccess_type
#         elif result == 'na':
#             next_t = self.onnotapplicable_type
#         else:
#             next_t = self.onfailure_type
#         it = self.current_step.get_out_associations().__iter__()
#         while it.has_next():
#             el = it.next()
#             if next_t.is_type_of(el): #this is the branch we want
#                 #check if we can got to next step based on num_exec number
#                 exec_num = el.get_attribute(StringValue('Flow.exec_num')).get_value()
#                 assert not exec_num < IntegerValue(-1) 
#                 if exec_num ==IntegerValue(-1) :
#                     break #infininte
#                 elif exec_num == IntegerValue(0) :
#                     return None #thus branch is done
#                 else: #go to branch
#                     set_attribute(el,StringValue('Flow.exec_num'), exec_num-IntegerValue(1) )
# #                     loc = el.get_location()
# #                     type = el.typed_by()
# #                     cl = MvK().update(MappingValue({UpdateConstants.TYPE_KEY: type,
# #                                     UpdateConstants.LOCATION_KEY: loc,
# #                                     UpdateConstants.ATTRS_KEY: MappingValue({StringValue('Flow.exec_num'): exec_num-IntegerValue(1)})}))
#                     
#                     #next can be rule or transformation
#                     #recurse into transformation
#                     self.current_step = el.get_to_multiplicity().get_node()
#                     if self.rule.is_type_of(self.current_step):
#                         self.current_rule = MvK().read(self.current_step.get_attribute(StringValue('Rule.location')).get_value()).get_item()
#                         self.current_rule_type = self.current_step.typed_by()
#                         return (self.current_rule,self.current_rule_type)
#                     elif self.tranf.is_type_of(el):
#                         pass #TODO
#         #self.rule_applied = None
#         return self.r

    def set_rule_applied(self, applied):
        assert isinstance(applied, bool)
        self.rule_applied = applied

    def has_rule_applied(self):
        return self.rule_applied        
        
class State2(object):
    def __init__(self, m_loc, rule,type=None):
        self.rules = {}
        self.r = MvK().read(rule).get_item()
        self.m = MvK().read(m_loc).get_item()
        self.lhs = None
        self.rhs = None
        self.nacs = []
        lhs_type = MvK().read(LocationValue('protected.formalisms.Rule.LHS')).get_item()
        nac_type = MvK().read(LocationValue('protected.formalisms.Rule.NAC')).get_item()
        rhs_type = MvK().read(LocationValue('protected.formalisms.Rule.RHS')).get_item()
        it = self.r.get_elements().__iter__()
        self.matchset2rewrite = None
        self.curr_lhs_match = None
        while it.has_next():
            el = self.r.get_element(it.next())
            if lhs_type.is_type_of(el):
                self.lhs = el
            elif nac_type.is_type_of(el):
                self.nacs.append(el)
            elif rhs_type.is_type_of(el):
                self.rhs = el
        assert self.lhs
        self.curr_nac_idx = 0

    def create_matcher_lhs(self,maxmatches=1):
        return Matcher(self.m, self.lhs,maxmatches=maxmatches)

    def set_lhs_matches(self, matches):
        self.lhs_matches = matches

    def lhs_matches_left(self):
        return len(self.lhs_matches)

    def select_lhs_match(self):
        self.curr_lhs_match = self.lhs_matches.pop()
        self.curr_nac_idx = 0

    def get_current_lhs_match(self):
        return self.curr_lhs_match
    
    def set_current_lhs_match(self,packet,rule):
        packet_matchsets = packet.get_attribute(StringValue('Packet.matchsets')).get_value()
        if rule not in packet_matchsets:
            return False
        else:
            self.matchset2rewrite = packet_matchsets[rule]
            match = self.matchset2rewrite.get_attribute(StringValue('MatchSet.match2rewrite')).get_value()
            mapping = match.get_attribute(StringValue('Match.mapping')).get_value()
            self.curr_lhs_match = dict(mapping)
            return True
        
    def nacs_left(self):
        return self.curr_nac_idx < len(self.nacs)

    def next_nac(self):
        self.curr_nac = self.nacs[self.curr_nac_idx]
        self.curr_nac_idx += 1

    def create_matcher_nac(self,maxmatches=1):
        return Matcher(self.m, self.curr_nac, self.curr_lhs_match,maxmatches=maxmatches)

    def create_rewriter(self):
        #assert not self.nacs_left()
        return Rewriter(self.m, self.curr_lhs_match, self.rhs)        
        
        

        
def next_in(primitive,packet):
    pass        

def packet_in(primitive,packet):
    
    matcher_type = MvK().read(LocationValue('protected.formalisms.MT.TCore.Matcher')).get_item()
    rewriter_type = MvK().read(LocationValue('protected.formalisms.MT.TCore.Rewriter')).get_item()
    packet_type = MvK().read(LocationValue('protected.formalisms.MT.TCore.Packet')).get_item()
    iter_type = MvK().read(LocationValue('protected.formalisms.MT.TCore.Iter')).get_item()
    #match2rewrite_type = MvK().read(LocationValue('protected.formalisms.MT.TCore.Match2Rewrite')).get_item()
    
    if not packet_type.is_type_of(packet):
        set_failure(packet)
        set_message(packet,"This is not a packet.")
        return packet
   
    if matcher_type.is_type_of(primitive):
        try:
            model = LocationValue(packet.get_attribute(StringValue('Packet.model')).get_value())
            rule = LocationValue(primitive.get_attribute(StringValue('Matcher.rule')).get_value())
            maxmatches = primitive.get_attribute(StringValue('Matcher.max')).get_value()
            state = State2(model, rule)
            matcher = state.create_matcher_lhs(maxmatches=maxmatches) #take value from Rule 
            matcher.match_pattern2(state)
            state.set_lhs_matches(matcher.get_matches())
            i = 1
            packet_matchsets = packet.get_attribute(StringValue('Packet.matchsets')).get_value()
            matches = None
            del_attr(packet, StringValue("Packet.current"))
            packet.add_attribute(Attribute(name=StringValue("Packet.current"),
                                         the_type=LocationType(),
                                         l_type=MvK().read(LocationValue("protected.formalisms.MT.TCore.Packet.current")).get_item(),
                                         potency=IntegerValue(0),
                                         value=rule))
        except Exception, e:
            set_failure(packet)
            set_message(packet,"Exception while matching: %s"%str(e))
            return packet
        if packet_matchsets.value and rule in packet_matchsets:
            matchset = packet_matchsets[rule]
            matches = matchset.get_attribute(StringValue('MatchSet.matches')).get_value().get_value()
            matches = matches['matches']
        else:
            matchset = Clabject(name=StringValue("m%d"%i),
                      l_type=ClabjectReference(path=LocationValue("protected.formalisms.MT.TCore.MatchSet")),
                      potency=IntegerValue(0))
            matches = []
            matchset.add_attribute(Attribute(name=StringValue("MatchSet.matches"),
                                   the_type=MappingType(),
                                   l_type=MvK().read(LocationValue("protected.formalisms.MT.TCore.MatchSet.matches")).get_item(),
                                   potency=IntegerValue(0),
                                   value=MappingValue({'matches':matches})))
            del_attr(packet, StringValue("Packet.matchsets"))
            packet.add_attribute(Attribute(name=StringValue("Packet.matchsets"),
                                   the_type=MappingType(),
                                   l_type=MvK().read(LocationValue("protected.formalisms.MT.TCore.Packet.matchsets")).get_item(),
                                   potency=IntegerValue(0),
                                   value=MappingValue({rule:matchset})))
            
        for match in state.lhs_matches:
            match_clab = Clabject(name=StringValue("m%d"%i),
                  l_type=ClabjectReference(path=LocationValue("protected.formalisms.MT.TCore.Match")),
                  potency=IntegerValue(0))
            
            match_clab.add_attribute(Attribute(name=StringValue("Match.mapping"),
                                   the_type=MappingType(),
                                   l_type=MvK().read(LocationValue("protected.formalisms.MT.TCore.Match.mapping")).get_item(),
                                   potency=IntegerValue(0),
                                   value=MappingValue(match)))
            match_clab.add_attribute(Attribute(name=StringValue("Match.name"),
                                   the_type=StringType(),
                                   l_type=MvK().read(LocationValue("protected.formalisms.MT.TCore.Match.name")).get_item(),
                                   potency=IntegerValue(0),
                                   value=StringValue("m%d"%i)))
            matches.append(match_clab)
            i+=1
        set_success(packet)
        return packet
        
    elif rewriter_type.is_type_of(primitive):
        model = LocationValue(packet.get_attribute(StringValue('Packet.model')).get_value())
        #draw.Draw.plot(model, 'before')
        rule = LocationValue(primitive.get_attribute(StringValue('Rewriter.rule')).get_value())
        state = State2(model, rule)
        res = state.set_current_lhs_match(packet,rule)
        if not res:
            #rewriter wants to rewrite for matchset that has no match selected for the rewrite.
            #FAILURE for packet and return
            set_failure(packet)
            set_message(packet,"No matches to rewrite.")
            #print "PACKET FAIL"
            return packet
            pass
        rewriter = state.create_rewriter()
        cl = MvKCompositeLog()
        while not rewriter.done():
            next_cl = rewriter.rewrite_next_element()
            cl.add_log(next_cl)
            if not next_cl.is_success():
                cl.set_status_code(next_cl.get_status_code())
                cl.set_status_message(next_cl.get_status_message())
                set_failure(packet)
                set_message(packet,next_cl.get_status_message())
                return packet
        a_cl = rewriter.execute_action()
        state.matchset2rewrite.remove_attribute(StringValue('MatchSet.match2rewrite'))
        set_success(packet)
        return packet
    elif iter_type.is_type_of(primitive):
        iter_rule = None
        random = primitive.get_attribute(StringValue('Iter.Random')).get_value()
        try:
            iter_rule = LocationValue(iter.get_attribute(StringValue('Iter.rule')).get_value())
        except:
            pass
        packet_current = packet.get_attribute(StringValue('Packet.current')).get_value()
        packet_matchsets = packet.get_attribute(StringValue('Packet.matchsets')).get_value()
        if not iter_rule:
            iter_rule = packet_current
        elif iter_rule not in packet_matchsets:
            set_failure(packet)
            return packet
        elif iter_rule != packet_current:
            packet_current = iter_rule
            packet.remove_attribute('Packet.current')
            packet.add_attribute(Attribute(name=StringValue("Packet.current"),
                                             the_type=LocationType(),
                                             l_type=MvK().read(LocationValue("protected.formalisms.MT.TCore.Packet.current")).get_item(),
                                             potency=IntegerValue(0),
                                             value=packet_current))
        matchset = packet_matchsets[packet_current]
        matches = matchset.get_attribute(StringValue('MatchSet.matches')).get_value().get_value()
        matches = matches['matches']
        if len(matches) == 0:
            del packet_matchsets[packet_current]
            set_failure(packet)
            set_message(packet,"No matches to iterate.")
            return packet
        if not random:
            match = matches.pop(0)
        else:
            match = matches.pop((MvK()._randomGen if MvK()._randomGen != None else Random).randint(0, len(matches) - 1))
        if StringValue('MatchSet.match2rewrite') in matchset.attributes:
            matchset.remove_attribute('MatchSet.match2rewrite')
        
        matchset.add_attribute(Attribute(name=StringValue("MatchSet.match2rewrite"),
                                             the_type=AnyType(),
                                             l_type=MvK().read(LocationValue("protected.formalisms.MT.TCore.MatchSet.match2rewrite")).get_item(),
                                             potency=IntegerValue(0),
                                             value=match))
        set_success(packet)
        return packet
    else:
        set_failure(packet)
        set_message(packet,"Unsupported.")
        return packet
    return packet
        

def set_message(packet,msg):
    if StringValue("Packet.msg") in packet.attributes:
        packet.remove_attribute(StringValue("Packet.msg"))
    packet.add_attribute(Attribute(name=StringValue("Packet.msg"),
                                         the_type=StringType(),
                                         l_type=MvK().read(LocationValue("protected.formalisms.MT.TCore.Packet.msg")).get_item(),
                                         potency=IntegerValue(0),
                                         value=StringValue(msg)))

def set_success(packet):
    if StringValue("Packet.isSuccess") in packet.attributes:
        packet.remove_attribute(StringValue("Packet.isSuccess"))
    packet.add_attribute(Attribute(name=StringValue("Packet.isSuccess"),
                                         the_type=BooleanType(),
                                         l_type=MvK().read(LocationValue("protected.formalisms.MT.TCore.Packet.isSuccess")).get_item(),
                                         potency=IntegerValue(0),
                                         value=BooleanValue(True)))
def set_failure(packet):
    if StringValue("Packet.isSuccess") in packet.attributes:
        packet.remove_attribute(StringValue("Packet.isSuccess"))
    packet.add_attribute(Attribute(name=StringValue("Packet.isSuccess"),
                                         the_type=BooleanType(),
                                         l_type=MvK().read(LocationValue("protected.formalisms.MT.TCore.Packet.isSuccess")).get_item(),
                                         potency=IntegerValue(0),
                                         value=BooleanValue(False)))

def select_match_start(hasmatch,toselect,match2rewrite,packet):        
    it = toselect.get_out_associations().__iter__()
    next_match = None
    #first set match to rewrite
    if not match2rewrite:
        p_to_m2r = Association(name=StringValue("p_to_m2r"),
                               l_type=AssociationReference(path=LocationValue("protected.formalisms.MT.TCore.Match2Rewrite")),
                               potency=IntegerValue(0),
                               from_multiplicity=AssociationEnd(node=packet,
                                                                port_name=StringValue('from_packet')),
                               to_multiplicity=AssociationEnd(node=toselect,
                                                                port_name=StringValue('to_match')))

    elif match2rewrite:
        match2rewrite.set_to_multiplicity(AssociationEnd(node=toselect,port_name=StringValue('to_match')))
    it = toselect.get_out_associations().__iter__()
    next_ass = None
    while it.has_next():    
        next_ass = it.next()
        next_match = next_ass.get_to_multiplicity().get_node()
    #we do have next match
    if next_match:
        #packet now points to next match after first
        hasmatch.set_to_multiplicity(AssociationEnd(node=next_match,port_name=StringValue('to_match')))
        toselect.remove_out_association(next_ass.get_location())
        next_match.remove_in_association(next_ass.get_location())
    else:
        packet.remove_out_association(hasmatch.get_location())
        toselect.remove_in_association(hasmatch.get_location())
        
def ramify(location):
    ramify_scd(model_location=LocationValue(location))
        
        