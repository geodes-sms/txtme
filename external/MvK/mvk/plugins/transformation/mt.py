'''
Created on 10-mrt.-2014

@author: Simon
'''
from mvk.impl.python.changelog import MvKCompositeLog
from mvk.impl.python.constants import CreateConstants, CRUDConstants
from mvk.impl.python.datatype import StringType
from mvk.impl.python.datavalue import StringValue, IntegerValue, LocationValue, \
    MappingValue, SequenceValue, BooleanValue
from mvk.impl.python.python_representer import PythonRepresenter
import mvk.interfaces.datavalue
from mvk.mvk import MvK


def ramify_scd(model_location):
    assert (isinstance(model_location, mvk.interfaces.datavalue.LocationValue) and
            isinstance(model_location.typed_by(), mvk.interfaces.datatype.LocationType))
    return_log = MvKCompositeLog()
    mvkinst = MvK()
    read_log = mvkinst.read(model_location)
    if not read_log.is_success():
        return_log.set_status_code(read_log.get_status_code())
        return_log.set_status_message(read_log.get_status_message())
        return return_log
    m = read_log.get_item()
    idx = model_location.rfind(StringValue('.')) + IntegerValue(1)
    loc = model_location.substring(stop=idx)
    pre_name = LocationValue('MTpre_') + model_location.substring(start=idx)
    post_name = LocationValue('MTpost_') + model_location.substring(start=idx)
    pre_loc = loc + pre_name
    post_loc = loc + post_name
    read_log_pre = mvkinst.read(pre_loc)
    if read_log_pre.is_success():
        mvkinst.delete(pre_loc)
    read_log_post = mvkinst.read(post_loc)
    if read_log_post.is_success():
        mvkinst.delete(post_loc)
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: m.typed_by().get_location(),
                                      CreateConstants.LOCATION_KEY: loc if loc.len() == 0 else loc.substring(start=IntegerValue(0), stop=idx - IntegerValue(1)),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): pre_name})
                                      })
                        )
    if not cl.is_success():
        return_log.set_status_code(cl.get_status_code())
        return_log.set_status_message(cl.get_status_message())
        return return_log
    cl = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: m.typed_by().get_location(),
                                      CreateConstants.LOCATION_KEY: loc if loc.len() == 0 else loc.substring(start=IntegerValue(0), stop=idx - IntegerValue(1)),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): post_name})
                                      })
                        )
    if not cl.is_success():
        return_log.set_status_code(cl.get_status_code())
        return_log.set_status_message(cl.get_status_message())
        return return_log

    def top_sort_superclasses(classes):
        ret_val_c = SequenceValue([])
        ret_val_a = SequenceValue([])
        no_inc = SequenceValue([])
        it = classes.__iter__()
        while it.has_next():
            el = it.next()
            if ((not isinstance(el, mvk.interfaces.object.Clabject)) or
                el.get_potency() == IntegerValue(0)):
                continue
            if el.get_super_classes().len() == IntegerValue(0):
                no_inc.append(el)
        while no_inc.len() > IntegerValue(0):
            el = no_inc.pop()
            if isinstance(el, mvk.interfaces.object.Association):
                ret_val_a.append(el)
            else:
                ret_val_c.append(el)
            spec_classes_it = el.get_specialise_classes().__iter__()
            while spec_classes_it.has_next():
                spec_cls = spec_classes_it.next()
                super_cls_it = spec_cls.get_super_classes().__iter__()
                no_parents = True
                while super_cls_it.has_next() and no_parents:
                    n_sc = super_cls_it.next()
                    if not ((n_sc in ret_val_c) or
                            (n_sc in ret_val_a)):
                        no_parents = False
                if no_parents:
                    no_inc.append(spec_cls)
        return ret_val_c + ret_val_a

    it = top_sort_superclasses(m.get_elements().values()).__iter__()
    while it.has_next():
        el = it.next()
        superclasses_pre = []
        superclasses_post = []
        attrs_pre = MappingValue({StringValue('Class.name'): StringValue('MTpre_') + el.get_name(),
                                  StringValue('Class.is_abstract'): BooleanValue(False)})
        attrs_post = MappingValue({StringValue('Class.name'): StringValue('MTpost_') + el.get_name(),
                                  StringValue('Class.is_abstract'): BooleanValue(False)})
        linguistic_attrs_pre = []
        linguistic_attrs_post = []
        params_pre = MappingValue({CreateConstants.TYPE_KEY: el.typed_by().get_location(),
                                   CreateConstants.LOCATION_KEY: pre_loc,
                                   CreateConstants.ATTRS_KEY: attrs_pre})
        params_post = MappingValue({CreateConstants.TYPE_KEY: el.typed_by().get_location(),
                                    CreateConstants.LOCATION_KEY: post_loc,
                                    CreateConstants.ATTRS_KEY: attrs_post})
        if isinstance(el, mvk.interfaces.object.Association) and el.get_potency() > IntegerValue(0):
            f_m_orig = el.get_from_multiplicity()
            f_m_orig_cl = f_m_orig.get_node().get_location()
            idx = f_m_orig_cl.rfind(StringValue('.')) + IntegerValue(1)
            idx_s = f_m_orig_cl.rfind(StringValue('.'), end=(idx - IntegerValue(1))) + IntegerValue(1)
            attrs_pre[StringValue('from_class')] = (f_m_orig_cl.substring(stop=idx_s) +
                                                    StringValue('MTpre_') +
                                                    f_m_orig_cl.substring(start=idx_s, stop=idx) +
                                                    StringValue('MTpre_') +
                                                    f_m_orig_cl.substring(start=idx))
            attrs_pre[StringValue('Association.from_min')] = IntegerValue(0)
            attrs_pre[StringValue('Association.from_max')] = f_m_orig.get_upper()
            attrs_pre[StringValue('Association.from_port')] = f_m_orig.get_port_name()
            attrs_post[StringValue('from_class')] = (f_m_orig_cl.substring(stop=idx_s) +
                                                     StringValue('MTpost_') +
                                                     f_m_orig_cl.substring(start=idx_s, stop=idx) +
                                                     StringValue('MTpost_') +
                                                     f_m_orig_cl.substring(start=idx))
            attrs_post[StringValue('Association.from_min')] = IntegerValue(0)
            attrs_post[StringValue('Association.from_max')] = f_m_orig.get_upper()
            attrs_post[StringValue('Association.from_port')] = f_m_orig.get_port_name()
            t_m_orig = el.get_to_multiplicity()
            t_m_orig_cl = t_m_orig.get_node().get_location()
            idx = t_m_orig_cl.rfind(StringValue('.')) + IntegerValue(1)
            idx_s = t_m_orig_cl.rfind(StringValue('.'), end=(idx - IntegerValue(1))) + IntegerValue(1)
            attrs_pre[StringValue('to_class')] = (t_m_orig_cl.substring(stop=idx_s) +
                                                  StringValue('MTpre_') +
                                                  t_m_orig_cl.substring(start=idx_s, stop=idx) +
                                                  StringValue('MTpre_') +
                                                  t_m_orig_cl.substring(start=idx))
            attrs_pre[StringValue('Association.to_min')] = IntegerValue(0)
            attrs_pre[StringValue('Association.to_max')] = t_m_orig.get_upper()
            attrs_pre[StringValue('Association.to_port')] = t_m_orig.get_port_name()
            attrs_post[StringValue('to_class')] = (t_m_orig_cl.substring(stop=idx_s) +
                                                   StringValue('MTpost_') +
                                                   t_m_orig_cl.substring(start=idx_s, stop=idx) +
                                                   StringValue('MTpost_') +
                                                   t_m_orig_cl.substring(start=idx))
            attrs_post[StringValue('Association.to_min')] = IntegerValue(0)
            attrs_post[StringValue('Association.to_max')] = t_m_orig.get_upper()
            attrs_post[StringValue('Association.to_port')] = t_m_orig.get_port_name()
            superclasses_pre.append(LocationValue('protected.formalisms.Rule.MTpre_Association'))
            superclasses_post.append(LocationValue('protected.formalisms.Rule.MTpost_Association'))
        elif  el.get_potency() > IntegerValue(0):
            superclasses_pre.append(LocationValue('protected.formalisms.Rule.MTpre_Element'))
            superclasses_post.append(LocationValue('protected.formalisms.Rule.MTpost_Element'))
        sc_it = el.get_super_classes().__iter__()
        while sc_it.has_next():
            sc = sc_it.next()
            sc_loc = sc.get_location()
            idx = sc_loc.rfind(StringValue('.')) + IntegerValue(1)
            idx_s = sc_loc.rfind(StringValue('.'), end=(idx - IntegerValue(1))) + IntegerValue(1)
            superclasses_pre.append(sc_loc.substring(stop=idx_s) +
                                    StringValue('MTpre_') +
                                    sc_loc.substring(start=idx_s, stop=idx) +
                                    StringValue('MTpre_') +
                                    sc_loc.substring(start=idx))
            superclasses_post.append(sc_loc.substring(stop=idx_s) +
                                     StringValue('MTpost_') +
                                     sc_loc.substring(start=idx_s, stop=idx) +
                                     StringValue('MTpost_') +
                                     sc_loc.substring(start=idx))
        attr_it = el.get_attributes().__iter__()
        while attr_it.has_next():
            attr = attr_it.next()
            if attr.get_potency() > IntegerValue(0):
                linguistic_attrs_pre.append(MappingValue({CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MTpre_') + attr.get_name(),
                                                                                                   StringValue('Attribute.type'): StringType(),
                                                                                                   StringValue('Attribute.default'): StringValue('True')}),
                                                          CreateConstants.TYPE_KEY: attr.typed_by().get_location(),
                                                          CreateConstants.LOCATION_KEY: LocationValue('%s.%s' % (pre_loc, StringValue('MTpre_') + el.get_name()))
                                                          })
                                            )
                linguistic_attrs_post.append(MappingValue({CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MTpost_') + attr.get_name(),
                                                                                                    StringValue('Attribute.type'): StringType(),
                                                                                                    StringValue('Attribute.default'): StringValue('get_attribute()')}),
                                                          CreateConstants.TYPE_KEY: attr.typed_by().get_location(),
                                                          CreateConstants.LOCATION_KEY: LocationValue('%s.%s' % (post_loc, StringValue('MTpost_') + el.get_name()))
                                                          })
                                             )
        cl = mvkinst.create(params_pre)
        if not cl.is_success():
            return_log.set_status_code(cl.get_status_code())
            return_log.set_status_message(cl.get_status_message())
            return return_log
        return_log.add_log(cl)
        for sc in superclasses_pre:
            name = StringValue('%s_i_%s' % (StringValue('MTpre_') + el.get_name(), sc.replace(StringValue('.'), StringValue('_'))))
            sc_log = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                                  CreateConstants.LOCATION_KEY: pre_loc,
                                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): name,
                                                                                           StringValue('from_class'): LocationValue('%s.%s' % (pre_loc, StringValue('MTpre_') + el.get_name())),
                                                                                           StringValue('to_class'): sc})
                                                   })
                                     )
            if not sc_log.is_success():
                return_log.set_status_code(sc_log.get_status_code())
                return_log.set_status_message(sc_log.get_status_message())
                return return_log
            return_log.add_log(sc_log)
        for params in linguistic_attrs_pre:
            attr_log = mvkinst.create(params)
            if not attr_log.is_success():
                return_log.set_status_code(sc_log.get_status_code())
                return_log.set_status_message(sc_log.get_status_message())
                return return_log
            return_log.add_log(attr_log)

        cl = mvkinst.create(params_post)
        if not cl.is_success():
            return_log.set_status_code(cl.get_status_code())
            return_log.set_status_message(cl.get_status_message())
            return return_log
        return_log.add_log(cl)
        for sc in superclasses_post:
            name = StringValue('%s_i_%s' % (StringValue('MTpost_') + el.get_name(), sc.replace(StringValue('.'), StringValue('_'))))
            sc_log = mvkinst.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                                  CreateConstants.LOCATION_KEY: post_loc,
                                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): name,
                                                                                           StringValue('from_class'): LocationValue('%s.%s' % (post_loc, StringValue('MTpost_') + el.get_name())),
                                                                                           StringValue('to_class'): sc})
                                                   })
                                     )
            if not sc_log.is_success():
                return_log.set_status_code(sc_log.get_status_code())
                return_log.set_status_message(sc_log.get_status_message())
                return return_log
            return_log.add_log(sc_log)
        for params in linguistic_attrs_post:
            attr_log = mvkinst.create(params)
            if not attr_log.is_success():
                return_log.set_status_code(sc_log.get_status_code())
                return_log.set_status_message(sc_log.get_status_message())
                return return_log
            return_log.add_log(attr_log)
    return_log.set_status_code(CRUDConstants.SUCCESS_CODE)
    return_log.set_status_message(StringValue('Success!'))
    return return_log
