from json.encoder import JSONEncoder

from mvk.impl.python.datavalue import IntegerValue, SequenceValue, StringValue, MappingValue
from mvk.impl.python.object import Attribute
from mvk.impl.python.python_representer import PythonRepresenter
import mvk.interfaces.datavalue

class MvKEncoder(JSONEncoder):
    def __init__(self):
        '''
        Constructor. When deep=True, serializes all children of packages
        and models. Otherwise, only serializes its names.
        '''
        JSONEncoder.__init__(self, skipkeys=False, ensure_ascii=True,
                             check_circular=True, allow_nan=True,
                             sort_keys=False, indent=None,
                             separators=None, encoding='utf-8',
                             default=None)

    def default(self, o):
        cls_to_method = {'RootPackage': self._encode_package,
                         'Package': self._encode_package,
                         'Model': self._encode_model,
                         'Clabject': self._encode_clabject,
                         'Association': self._encode_association,
                         'Composition': self._encode_association,
                         'Aggregation': self._encode_association,
                         'Inherits': self._encode_association,
                         'Attribute': self._encode_attribute,
                         'Function': self._encode_function,
                         'Body': self._encode_body,
                         'Parameter': self._encode_parameter,
                         'ExpressionStatement': self._encode_expressionstatement,
                         'ReturnStatement': self._encode_return_statement,
                         'DeclarationStatement': self._encode_declaration_statement,
                         'WhileLoop': self._encode_while_loop,
                         'IfStatement': self._encode_if_statement,
                         'BreakStatement': self._encode_break_statement,
                         'ContinueStatement': self._encode_continue_statement,
                         'Constant': self._encode_constant,
                         'Identifier': self._encode_identifier,
                         'Navigation': self._encode_navigation,
                         'Assignment': self._encode_assignment,
                         'FunctionCall': self._encode_function_call,
                         'Argument': self._encode_argument
                         }

        if isinstance(o, mvk.interfaces.action.Operator):
            return self._encode_operator(o)
        elif o.__class__.__name__ in cls_to_method:
            ''' object classes '''
            retval = cls_to_method[o.__class__.__name__](o)
            if "physical_type" not in retval:
                retval["physical_type"] = PythonRepresenter.CLS_TO_PHYS_TYPE[o.__class__]
            if "name" not in retval:
                retval["name"] = o.name
            return retval
        elif isinstance(o, mvk.interfaces.changelog.MvKCompositeLog):
            # Encode all sub-logs too
            inner = o.get_value()
            value = {}
            for key in inner:
                value[str(key)] = inner[key]
            value["logs"] = o.logs
            return {'type': o.__class__.__name__, 'value': value}
        elif isinstance(o, mvk.interfaces.datavalue.DataValue):
            type_str = o.__class__.__name__
            value = None
            if (isinstance(o, mvk.interfaces.datavalue.MappingValue) and
                isinstance(o.typed_by(), mvk.interfaces.datatype.MappingType)):
                mapping_keys = []
                mapping_values = []
                value = {'keys': mapping_keys,
                         'values': mapping_values}
                for key in o:
                    mapping_keys.append(key)
                    mapping_values.append(o[key])
            elif ((isinstance(o, mvk.interfaces.datavalue.SequenceValue) and
                   isinstance(o.typed_by(), mvk.interfaces.datatype.SequenceType)) or
                  (isinstance(o, mvk.interfaces.datavalue.TupleValue) and
                   isinstance(o.typed_by(), mvk.interfaces.datatype.TupleType)) or
                  (isinstance(o, mvk.interfaces.datavalue.SetValue) and
                   isinstance(o.typed_by(), mvk.interfaces.datatype.SetType))):
                value = []
                for v in o:
                    value.append(v)
            elif isinstance(o, mvk.interfaces.datavalue.DataValue):
                ''' primitive values '''
                value = o.get_value()
            return {'type': type_str, 'value': value}
        elif isinstance(o, mvk.interfaces.datatype.CompositeType):
            return {'type': o.__class__.__name__, 'value': o.types}
        elif isinstance(o, mvk.interfaces.datatype.Type):
            return {'type': o.__class__.__name__}
        else:
            raise TypeError('I only know how to serialize DataValues and all object Classes! %s' % o.__class__.__name__)

    def _encode_package(self, o):
        elements = []
        for itnext in o.get_elements():
            child = o.get_element(itnext)
            elements.append({"name": child.get_name(), "location": child.get_location()})
        return {'location': o.get_location(),
                'physical_attributes': {'name': o.get_name()},
                'physical_type': PythonRepresenter.CLS_TO_PHYS_TYPE[o.__class__],
                'elements': elements}

    def _encode_model(self, o):
        ret_val = self._encode_package(o)
        ret_val['linguistic_type'] = o.typed_by().get_location()
        ret_val['physical_attributes']['potency'] = o.get_potency()
        ret_val['physical_attributes']['in_associations'] = self._encode_association_list(o.get_in_associations())
        ret_val['physical_attributes']['out_associations'] = self._encode_association_list(o.get_out_associations())
        ret_val['physical_attributes']['functions'] = self._encode_function_list(o.get_functions())
        ret_val['linguistic_attributes'] = []
        for attr in o.get_attributes():
            #TODO strip of if not a (primitive) DataValue
            if not isinstance(attr, mvk.interfaces.object.AssociationEnd):
                ret_val['linguistic_attributes'].append(attr)
        return ret_val

    def _encode_association_list(self, o):
        # o will be an ImmutableSequenceValue
        o = o.get_value()
        ret_val = [assoc.get_location() for assoc in o]
        return mvk.impl.python.datavalue.SequenceValue(ret_val)

    def _encode_function_list(self, o):
        # o will be an ImmutableSequenceValue
        o = o.get_value()
        ret_val = [function.get_location() for function in o]
        return mvk.impl.python.datavalue.SequenceValue(ret_val)

    def _encode_clabject(self, o):
        ret_val = {'location': o.get_location(),
                   'linguistic_type': o.typed_by().get_location(),
                   'physical_type': PythonRepresenter.CLS_TO_PHYS_TYPE[o.__class__],
                   'physical_attributes': {'name': o.get_name(),
                                           'potency': o.get_potency(),
                                           'functions': self._encode_function_list(o.get_functions()),
                                           'in_associations': self._encode_association_list(o.get_in_associations()),
                                           'out_associations': self._encode_association_list(o.get_out_associations())}
                   }
        attributes = []
        ret_val['linguistic_attributes'] = []
        for attr in o.get_all_attributes():
            #TODO strip of if not a (primitive) DataValue
            if not isinstance(attr, mvk.interfaces.object.AssociationEnd):
                ret_val['linguistic_attributes'].append(attr)
        if o.get_potency() > IntegerValue(0):
            ret_val['physical_attributes']['lower'] = o.get_lower()
            ret_val['physical_attributes']['upper'] = o.get_upper()
            ret_val['physical_attributes']['ordered'] = o.is_ordered()
            ret_val['physical_attributes']['abstract'] = o.is_abstract()
            superclasses = []
            for val in o.get_super_classes():
                superclasses.append(val.get_location())
            ret_val['physical_attributes']['superclasses'] = SequenceValue(superclasses)
        return ret_val

    def _encode_association(self, o):
        def encode_association_end(ae):
            return {'node': ae.get_node().get_location(),
                    'port_name': ae.get_port_name(),
                    'lower': ae.get_lower(),
                    'upper': ae.get_upper(),
                    'ordered': ae.is_ordered()}
        ret_val = self._encode_clabject(o)
        ret_val['physical_attributes']['from_multiplicity'] = encode_association_end(o.get_from_multiplicity())
        ret_val['physical_attributes']['to_multiplicity'] = encode_association_end(o.get_to_multiplicity())
        return ret_val

    def _encode_attribute(self, o):
        ltype = o.typed_by()
        ret_val = {'location': o.get_location(),
                   'short_location': o.get_short_location(),
                   'linguistic_type': {'type': 'Attribute' if isinstance(ltype, Attribute) else 'Clabject',
                                       'value': o.typed_by().get_location()},
                   'physical_type': PythonRepresenter.CLS_TO_PHYS_TYPE[o.__class__],
                   'physical_attributes': {'name': o.get_name(),
                                           'potency': o.get_potency(),
                                           'type': StringValue(str(o.get_type())),
                                           'functions': self._encode_function_list(o.get_functions()),
                                           'in_associations': self._encode_association_list(o.get_in_associations()),
                                           'out_associations': self._encode_association_list(o.get_out_associations())}
                    }
        if o.get_potency() > IntegerValue(0):
            attributes = []
            for value in o.get_attributes():
                #TODO strip of if not a (primitive) DataValue
                attributes.append(value)
            ret_val['linguistic_attributes'] = attributes
            ret_val['physical_attributes']['lower'] = o.get_lower()
            ret_val['physical_attributes']['upper'] = o.get_upper()
            ret_val['physical_attributes']['ordered'] = o.is_ordered()
            ret_val['physical_attributes']['default'] = o.get_default()
        else:
            ret_val['linguistic_attributes'] = []
            ret_val['physical_attributes']['value'] = o.get_value()
        return ret_val

    def _encode_base_action(self, o):
        retval = {}
        retval['physical_type'] = PythonRepresenter.CLS_TO_PHYS_TYPE[o.__class__]
        retval["name"] = o.get_name()
        retval["location"] = o.get_location()
        retval['potency'] = o.get_potency()
        retval['in_associations'] = self._encode_association_list(o.get_in_associations())
        retval['out_associations'] = self._encode_association_list(o.get_out_associations())
        retval['functions'] = self._encode_function_list(o.get_functions())
        retval['linguistic_attributes'] = []
        retval['linguistic_type'] = o.typed_by().get_location()
        for attr in o.get_attributes():
            #TODO strip of if not a (primitive) DataValue
            if not isinstance(attr, mvk.interfaces.object.AssociationEnd):
                retval['linguistic_attributes'].append(attr)
        return retval
        
    def _encode_function(self, o):
        retval = self._encode_base_action(o)
        retval["parameters"] = o.parameters
        retval["the_type"] = o.type
        retval["body"] = o.body
        return retval

    def _encode_body(self, o):
        retval = self._encode_base_action(o)
        retval["value"] = SequenceValue(o.value)
        return retval

    def _encode_parameter(self, o):
        retval = self._encode_base_action(o)
        retval["param_type"] = o.param_type
        retval["the_type"] = o.type
        return retval

    def _encode_return_statement(self, o):
        retval = self._encode_base_action(o)
        retval["expression"] = o.expression
        return retval

    def _encode_declaration_statement(self, o):
        retval = self._encode_base_action(o)
        retval["identifier"] = o.identifier
        retval["initialization_expression"] = o.initialization_expression
        return retval

    def _encode_while_loop(self, o):
        retval = self._encode_base_action(o)
        retval["test"] = o.test
        retval["body"] = o.body
        return retval

    def _encode_if_statement(self, o):
        retval = self._encode_base_action(o)
        retval["test"] = o.test
        retval["if_body"] = o.if_body
        retval["else_body"] = o.else_body
        return retval

    def _encode_break_statement(self, o):
        retval = self._encode_base_action(o)
        return retval

    def _encode_continue_statement(self, o):
        retval = self._encode_base_action(o)
        return retval

    def _encode_constant(self, o):
        retval = self._encode_base_action(o)
        retval["value"] = o.value
        retval["the_type"] = o.type
        return retval

    def _encode_identifier(self, o):
        retval = self._encode_base_action(o)
        retval["the_type"] = o.type
        return retval

    def _encode_navigation(self, o):
        retval = self._encode_base_action(o)
        retval["path"] = o.path
        return retval

    def _encode_assignment(self, o):
        retval = self._encode_base_action(o)
        retval["children"] = o.children
        return retval

    def _encode_function_call(self, o):
        retval = self._encode_base_action(o)
        retval["function"] = o.function
        retval["arguments"] = o.arguments
        retval["called_expression"] = o.called_expression
        return retval

    def _encode_argument(self, o):
        retval = self._encode_base_action(o)
        retval["key"] = o.key
        retval["expression"] = o.expression
        return retval

    def _encode_expressionstatement(self, o):
        retval = self._encode_base_action(o)
        retval["expression"] = o.expression
        return retval

    def _encode_operator(self, o):
        retval = self._encode_base_action(o)
        retval["children"] = o.children
        return retval
