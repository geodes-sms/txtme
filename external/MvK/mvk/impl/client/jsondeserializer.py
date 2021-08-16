from json.decoder import JSONDecoder

from mvk.impl.client.object import Package, Model, Multiplicity, Clabject, Attribute, Association, Composition, Aggregation, Inherits, AssociationEnd
from mvk.impl.client.action import *
from mvk.impl.python.python_representer import PythonRepresenter
from mvk.impl.python.datavalue import *
from mvk.impl.python.datatype import *
from mvk.impl.python.changelog import *

class MvKDecoder(JSONDecoder):
    def __init__(self):
        JSONDecoder.__init__(self, encoding=None, object_hook=None,
                             parse_float=None, parse_int=None,
                             parse_constant=None, strict=True,
                             object_pairs_hook=None)
        self.cls_to_method = {PythonRepresenter.PACKAGE: self._decode_package,
                         PythonRepresenter.MODEL: self._decode_model,
                         PythonRepresenter.CLABJECT: self._decode_clabject,
                         PythonRepresenter.ASSOCIATION: self._decode_association,
                         PythonRepresenter.COMPOSITION: self._decode_composition,
                         PythonRepresenter.AGGREGATION: self._decode_aggregation,
                         PythonRepresenter.INHERITS: self._decode_inherits,
                         PythonRepresenter.ATTRIBUTE: self._decode_attribute,
                         PythonRepresenter.FUNCTION: self._decode_function,
                         PythonRepresenter.BODY: self._decode_body,
                         PythonRepresenter.PARAMETER: self._decode_parameter,
                         PythonRepresenter.RETURNSTATEMENT: self._decode_returnstatement,
                         PythonRepresenter.DECLARATIONSTATEMENT: self._decode_declarationstatement,
                         PythonRepresenter.WHILELOOP: self._decode_whileloop,
                         PythonRepresenter.IFSTATEMENT: self._decode_ifstatement,
                         PythonRepresenter.BREAKSTATEMENT: self._decode_breakstatement,
                         PythonRepresenter.CONTINUESTATEMENT: self._decode_continuestatement,
                         PythonRepresenter.EXPRESSIONSTATEMENT: self._decode_expressionstatement,
                         PythonRepresenter.CONSTANT: self._decode_constant,
                         PythonRepresenter.IDENTIFIER: self._decode_identifier,
                         PythonRepresenter.NAVIGATION: self._decode_navigation,
                         PythonRepresenter.ASSIGNMENT: self._decode_assignment,
                         PythonRepresenter.FUNCTIONCALL: self._decode_functioncall,
                         PythonRepresenter.ARGUMENT: self._decode_argument,
                         PythonRepresenter.NOT: self._decode_not,
                         PythonRepresenter.OR: self._decode_or,
                         PythonRepresenter.AND: self._decode_and,
                         PythonRepresenter.EQUAL: self._decode_equal,
                         PythonRepresenter.LESSTHAN: self._decode_lessthan,
                         PythonRepresenter.GREATERTHAN: self._decode_greaterthan,
                         PythonRepresenter.IN: self._decode_in,
                         PythonRepresenter.PLUS: self._decode_plus,
                         PythonRepresenter.MINUS: self._decode_minus,
                         PythonRepresenter.MULTIPLICATION: self._decode_multiplication,
                         PythonRepresenter.DIVISION: self._decode_division,
                         PythonRepresenter.MODULO: self._decode_modulo
                         }

    def decode(self, s):
        return self._decode_to_mvk(JSONDecoder.decode(self, s))

    def _decode_to_mvk(self, o):
        if o is None:
            return None
        elif 'physical_type' in o:
            physical_type = self._decode_to_mvk(o['physical_type'])
            return self.cls_to_method[physical_type](o)
        elif isinstance(o, list):
            # Part of a function's parameters
            return [[self._decode_to_mvk(i) for i in o[0]], {k: self._decode_to_mvk(v) for k, v in o[1].items()}]
        elif isinstance(o, (str, unicode)):
            return o
        t = o['type']
        if t == 'StringValue':
            return StringValue(o['value'])
        elif t == 'LocationValue':
            return LocationValue(o['value'])
        elif t == 'SequenceValue':
            return SequenceValue([self._decode_to_mvk(item) for item in o['value']])
        elif t == 'ImmutableSequenceValue':
            return ImmutableSequenceValue(SequenceValue([self._decode_to_mvk(item) for item in o['value']]))
        elif t == 'SetValue':
            return SetValue(set([self._decode_to_mvk(item) for item in o['value']]))
        elif t == 'ImmutableSetValue':
            return ImmutableSetValue(SetValue(set([self._decode_to_mvk(item) for item in o['value']])))
        elif t == 'TupleValue':
            return TupleValue(tuple([self._decode_to_mvk(item) for item in o['value']]))
        elif t == 'MappingValue':
            return MappingValue({self._decode_to_mvk(key): self._decode_to_mvk(value) for key, value in zip(o['value']['keys'], o['value']['values'])})
        elif t == 'ImmutableMappingValue':
            return ImmutableMappingValue(MappingValue({self._decode_to_mvk(key): self._decode_to_mvk(value) for key, value in zip(o['value']['keys'], o['value']['values'])}))
        elif t == 'MvKCreateCompositeLog' or o['type'] == 'MvKCompositeLog' or o['type'] == 'MvKDeleteCompositeLog' or o['type'] == "MvKReadCompositeLog":
            v = DataValueFactory.create_instance(data=dict([(StringValue(key), self._decode_to_mvk(value)) for key,value in o['value'].items()]),
                                                   datacls=o['type'])
            v.logs = v[StringValue('logs')]
            del v[StringValue('logs')]
            return v
        elif t == 'MvKOperationLog':
            m = dict(zip([self._decode_to_mvk(item) for item in o['value']['keys']], [self._decode_to_mvk(item) for item in o['value']['values']]))
            return MvKOperationLog(operation_name=m[StringValue('operation_name')], value=m)
        elif t == 'MvKReadLog' or t == 'MvKCreateLog' or t == "MvKUpdateLog" or t == "MvKDeleteLog":
            return DataValueFactory.create_instance(data=dict(zip([self._decode_to_mvk(item) for item in o['value']['keys']],
                                                                  [self._decode_to_mvk(item) for item in o['value']['values']])),
                                                    datacls=o['type'])
        elif "Type" in t and "value" not in o:
            return eval(o["type"] + "()")
        elif "Type" in t and "value" in o:
            a = self._decode_to_mvk(o["value"])
            return eval(t + "(a)")
        else:
            ''' primitive values '''
            return DataValueFactory.create_instance(data=o['value'], datacls=t)

    def _decode_package(self, o):
        children = [(self._decode_to_mvk(x["name"]), self._decode_to_mvk(x["location"])) for x in o["elements"]]
        return Package(location=self._decode_to_mvk(o['location']),
                       linguistic_type=StringValue("mvk.object.Package"),
                       name=self._decode_to_mvk(o['name']),
                       children=children)

    def _decode_model(self, o):
        physical_attributes = o['physical_attributes']
        linguistic_type = o['linguistic_type']
        children = [(self._decode_to_mvk(x["name"]), self._decode_to_mvk(x["location"])) for x in o["elements"]]
        return Model(location=self._decode_to_mvk(o['location']),
                     linguistic_type=self._decode_to_mvk(linguistic_type),
                     name=self._decode_to_mvk(physical_attributes['name']),
                     potency=self._decode_to_mvk(physical_attributes['potency']),
                     in_associations=self._decode_to_mvk(physical_attributes['in_associations']),
                     out_associations=self._decode_to_mvk(physical_attributes['out_associations']),
                     functions=self._decode_to_mvk(physical_attributes['functions']),
                     elements=children,
                     attributes=[self._decode_to_mvk(attr) for attr in o["linguistic_attributes"]])

    def _decode_clabject(self, o):
        physical_attributes = o['physical_attributes']
        potency = self._decode_to_mvk(physical_attributes['potency'])
        if potency > IntegerValue(0):
            ret_val = Clabject(location=self._decode_to_mvk(o['location']),
                               name=self._decode_to_mvk(physical_attributes['name']),
                               linguistic_type=self._decode_to_mvk(o['linguistic_type']),
                               potency=potency,
                               abstract=self._decode_to_mvk(physical_attributes['abstract']),
                               lower=self._decode_to_mvk(physical_attributes['lower']),
                               upper=self._decode_to_mvk(physical_attributes['upper']),
                               ordered=self._decode_to_mvk(physical_attributes['ordered']),
                               in_associations=self._decode_to_mvk(physical_attributes['in_associations']),
                               out_associations=self._decode_to_mvk(physical_attributes['out_associations']),
                               functions=self._decode_to_mvk(physical_attributes['functions']),
                               attributes=[self._decode_to_mvk(attr) for attr in o['linguistic_attributes']],
                               superclasses=self._decode_to_mvk(physical_attributes['superclasses']))
        else:
            ret_val = Clabject(location=self._decode_to_mvk(o['location']),
                               name=self._decode_to_mvk(physical_attributes['name']),
                               linguistic_type=self._decode_to_mvk(o['linguistic_type']),
                               attributes=[self._decode_to_mvk(attr) for attr in o['linguistic_attributes']],
                               in_associations=self._decode_to_mvk(physical_attributes['in_associations']),
                               out_associations=self._decode_to_mvk(physical_attributes['out_associations']),
                               functions=self._decode_to_mvk(physical_attributes['functions']),
                               potency=potency)
        return ret_val

    def _decode_association(self, o, cls=Association):
        def decode_association_end(ae):
            return AssociationEnd(node=self._decode_to_mvk(ae['node']),
                                  port_name=self._decode_to_mvk(ae['port_name']),
                                  lower=self._decode_to_mvk(ae['lower']),
                                  upper=self._decode_to_mvk(ae['upper']),
                                  ordered=self._decode_to_mvk(ae['ordered']))

        physical_attributes = o['physical_attributes']
        potency = self._decode_to_mvk(physical_attributes['potency'])
        if potency > IntegerValue(0):
            ret_val = cls(location=self._decode_to_mvk(o['location']),
                          name=self._decode_to_mvk(physical_attributes['name']),
                          linguistic_type=self._decode_to_mvk(o['linguistic_type']),
                          attributes=[self._decode_to_mvk(attr) for attr in o['linguistic_attributes']],
                          abstract=self._decode_to_mvk(physical_attributes['abstract']),
                          potency=potency,
                          lower=self._decode_to_mvk(physical_attributes['lower']),
                          upper=self._decode_to_mvk(physical_attributes['upper']),
                          ordered=self._decode_to_mvk(physical_attributes['ordered']),
                          from_multiplicity=decode_association_end(physical_attributes['from_multiplicity']),
                          to_multiplicity=decode_association_end(physical_attributes['to_multiplicity']),
                          in_associations=self._decode_to_mvk(physical_attributes['in_associations']),
                          out_associations=self._decode_to_mvk(physical_attributes['out_associations']),
                          functions=self._decode_to_mvk(physical_attributes['functions']),
                          superclasses=[LocationValue(self._decode_to_mvk(sc)) for sc in physical_attributes["superclasses"]])
        else:
            ret_val = cls(location=self._decode_to_mvk(o['location']),
                          name=self._decode_to_mvk(physical_attributes['name']),
                          linguistic_type=self._decode_to_mvk(o['linguistic_type']),
                          potency=potency,
                          attributes=[self._decode_to_mvk(attr) for attr in o['linguistic_attributes']],
                          in_associations=self._decode_to_mvk(physical_attributes['in_associations']),
                          out_associations=self._decode_to_mvk(physical_attributes['out_associations']),
                          functions=self._decode_to_mvk(physical_attributes['functions']),
                          from_multiplicity=decode_association_end(physical_attributes['from_multiplicity']),
                          to_multiplicity=decode_association_end(physical_attributes['to_multiplicity']))
        return ret_val

    def _decode_composition(self, o):
        return self._decode_association(o, Composition)

    def _decode_aggregation(self, o):
        return self._decode_association(o, Aggregation)

    def _decode_inherits(self, o):
        return self._decode_association(o, Inherits)

    def _decode_attribute(self, o):
        physical_attributes = o['physical_attributes']
        potency = self._decode_to_mvk(physical_attributes['potency'])
        if potency.get_value() > 0:
            ret_val = Attribute(location=self._decode_to_mvk(o['location']),
                                short_location=self._decode_to_mvk(o['short_location']),
                                name=self._decode_to_mvk(physical_attributes['name']),
                                linguistic_type=self._decode_to_mvk(o["linguistic_type"]['value']),
                                the_type=TypeFactory.get_type(str(self._decode_to_mvk(physical_attributes['type']))),
                                potency=potency,
                                attributes=[self._decode_to_mvk(attr) for attr in o['linguistic_attributes']],
                                default=self._decode_to_mvk(physical_attributes['default']),
                                lower=self._decode_to_mvk(physical_attributes['lower']),
                                in_associations=self._decode_to_mvk(physical_attributes['in_associations']),
                                out_associations=self._decode_to_mvk(physical_attributes['out_associations']),
                                functions=self._decode_to_mvk(physical_attributes['functions']),
                                upper=self._decode_to_mvk(physical_attributes['upper']))
            ret_val.attributes = [self._decode_to_mvk(attr) for attr in o["linguistic_attributes"]]
        else:
            ret_val = Attribute(location=self._decode_to_mvk(o['location']),
                                name=self._decode_to_mvk(physical_attributes['name']),
                                linguistic_type=self._decode_to_mvk(o["linguistic_type"]['value']),
                                attributes=[self._decode_to_mvk(attr) for attr in o['linguistic_attributes']],
                                in_associations=self._decode_to_mvk(physical_attributes['in_associations']),
                                out_associations=self._decode_to_mvk(physical_attributes['out_associations']),
                                functions=self._decode_to_mvk(physical_attributes['functions']),
                                the_type=TypeFactory.get_type(str(self._decode_to_mvk(physical_attributes['type']))),
                                potency=potency,
                                value=self._decode_to_mvk(physical_attributes['value']))
        return ret_val

    def _decode_function(self, o):
        return Function(location=self._decode_to_mvk(o["location"]),
                        name=self._decode_to_mvk(o["name"]),
                        body=self._decode_to_mvk(o["body"]),
                        potency=self._decode_to_mvk(o["potency"]),
                        in_associations=self._decode_to_mvk(o["in_associations"]),
                        out_associations=self._decode_to_mvk(o["out_associations"]),
                        functions=self._decode_to_mvk(o["functions"]),
                        attributes=[self._decode_to_mvk(attr) for attr in o['linguistic_attributes']],
                        linguistic_type=self._decode_to_mvk(o["linguistic_type"]),
                        the_type=self._decode_to_mvk(o["the_type"]),
                        parameters=self._decode_to_mvk(o["parameters"])
               )

    def _decode_body(self, o):
        return Body(location=self._decode_to_mvk(o["location"]),
                        name=self._decode_to_mvk(o["name"]),
                        potency=self._decode_to_mvk(o["potency"]),
                        in_associations=self._decode_to_mvk(o["in_associations"]),
                        out_associations=self._decode_to_mvk(o["out_associations"]),
                        attributes=[self._decode_to_mvk(attr) for attr in o['linguistic_attributes']],
                        linguistic_type=self._decode_to_mvk(o["linguistic_type"]),
                        functions=self._decode_to_mvk(o["functions"]),
                        value=self._decode_to_mvk(o["value"])
               )

    def _decode_parameter(self, o):
        return Parameter(location=self._decode_to_mvk(o["location"]),
                        name=self._decode_to_mvk(o["name"]),
                        potency=self._decode_to_mvk(o["potency"]),
                        in_associations=self._decode_to_mvk(o["in_associations"]),
                        out_associations=self._decode_to_mvk(o["out_associations"]),
                        functions=self._decode_to_mvk(o["functions"]),
                        attributes=[self._decode_to_mvk(attr) for attr in o['linguistic_attributes']],
                        linguistic_type=self._decode_to_mvk(o["linguistic_type"]),
                        param_type=self._decode_to_mvk(o["param_type"]),
                        the_type=self._decode_to_mvk(o["the_type"])
               )

    def _decode_returnstatement(self, o):
        return ReturnStatement(location=self._decode_to_mvk(o["location"]),
                        name=self._decode_to_mvk(o["name"]),
                        potency=self._decode_to_mvk(o["potency"]),
                        in_associations=self._decode_to_mvk(o["in_associations"]),
                        out_associations=self._decode_to_mvk(o["out_associations"]),
                        attributes=[self._decode_to_mvk(attr) for attr in o['linguistic_attributes']],
                        linguistic_type=self._decode_to_mvk(o["linguistic_type"]),
                        functions=self._decode_to_mvk(o["functions"]),
                        expression=self._decode_to_mvk(o["expression"])
               )

    def _decode_declarationstatement(self, o):
        return DeclarationStatement(location=self._decode_to_mvk(o["location"]),
                        name=self._decode_to_mvk(o["name"]),
                        potency=self._decode_to_mvk(o["potency"]),
                        in_associations=self._decode_to_mvk(o["in_associations"]),
                        out_associations=self._decode_to_mvk(o["out_associations"]),
                        functions=self._decode_to_mvk(o["functions"]),
                        identifier=self._decode_to_mvk(o["identifier"]),
                        attributes=[self._decode_to_mvk(attr) for attr in o['linguistic_attributes']],
                        linguistic_type=self._decode_to_mvk(o["linguistic_type"]),
                        initialization_expression=self._decode_to_mvk(o["initialization_expression"])
               )

    def _decode_whileloop(self, o):
        return WhileLoop(location=self._decode_to_mvk(o["location"]),
                        name=self._decode_to_mvk(o["name"]),
                        potency=self._decode_to_mvk(o["potency"]),
                        in_associations=self._decode_to_mvk(o["in_associations"]),
                        out_associations=self._decode_to_mvk(o["out_associations"]),
                        functions=self._decode_to_mvk(o["functions"]),
                        test=self._decode_to_mvk(o["test"]),
                        attributes=[self._decode_to_mvk(attr) for attr in o['linguistic_attributes']],
                        linguistic_type=self._decode_to_mvk(o["linguistic_type"]),
                        body=self._decode_to_mvk(o["body"])
               )

    def _decode_ifstatement(self, o):
        return IfStatement(location=self._decode_to_mvk(o["location"]),
                        name=self._decode_to_mvk(o["name"]),
                        potency=self._decode_to_mvk(o["potency"]),
                        in_associations=self._decode_to_mvk(o["in_associations"]),
                        out_associations=self._decode_to_mvk(o["out_associations"]),
                        attributes=[self._decode_to_mvk(attr) for attr in o['linguistic_attributes']],
                        linguistic_type=self._decode_to_mvk(o["linguistic_type"]),
                        functions=self._decode_to_mvk(o["functions"]),
                        test=self._decode_to_mvk(o["test"]),
                        if_body=self._decode_to_mvk(o["if_body"]),
                        else_body=self._decode_to_mvk(o["else_body"])
               )

    def _decode_breakstatement(self, o):
        return BreakStatement(location=self._decode_to_mvk(o["location"]),
                        potency=self._decode_to_mvk(o["potency"]),
                        in_associations=self._decode_to_mvk(o["in_associations"]),
                        out_associations=self._decode_to_mvk(o["out_associations"]),
                        attributes=[self._decode_to_mvk(attr) for attr in o['linguistic_attributes']],
                        linguistic_type=self._decode_to_mvk(o["linguistic_type"]),
                        functions=self._decode_to_mvk(o["functions"]),
                        name=self._decode_to_mvk(o["name"])
               )

    def _decode_expressionstatement(self, o):
        return ExpressionStatement(location=self._decode_to_mvk(o["location"]),
                        potency=self._decode_to_mvk(o["potency"]),
                        in_associations=self._decode_to_mvk(o["in_associations"]),
                        out_associations=self._decode_to_mvk(o["out_associations"]),
                        attributes=[self._decode_to_mvk(attr) for attr in o['linguistic_attributes']],
                        linguistic_type=self._decode_to_mvk(o["linguistic_type"]),
                        functions=self._decode_to_mvk(o["functions"]),
                        name=self._decode_to_mvk(o["name"]),
                        expression=self._decode_to_mvk(o["expression"])
               )

    def _decode_continuestatement(self, o):
        return ContinueStatement(location=self._decode_to_mvk(o["location"]),
                        potency=self._decode_to_mvk(o["potency"]),
                        in_associations=self._decode_to_mvk(o["in_associations"]),
                        out_associations=self._decode_to_mvk(o["out_associations"]),
                        attributes=[self._decode_to_mvk(attr) for attr in o['linguistic_attributes']],
                        linguistic_type=self._decode_to_mvk(o["linguistic_type"]),
                        functions=self._decode_to_mvk(o["functions"]),
                        name=self._decode_to_mvk(o["name"])
               )

    def _decode_constant(self, o):
        return Constant(location=self._decode_to_mvk(o["location"]),
                        potency=self._decode_to_mvk(o["potency"]),
                        in_associations=self._decode_to_mvk(o["in_associations"]),
                        out_associations=self._decode_to_mvk(o["out_associations"]),
                        attributes=[self._decode_to_mvk(attr) for attr in o['linguistic_attributes']],
                        linguistic_type=self._decode_to_mvk(o["linguistic_type"]),
                        functions=self._decode_to_mvk(o["functions"]),
                        name=self._decode_to_mvk(o["name"]),
                        value=self._decode_to_mvk(o["value"]),
                        the_type=self._decode_to_mvk(o["the_type"])
               )

    def _decode_identifier(self, o):
        return Identifier(location=self._decode_to_mvk(o["location"]),
                        potency=self._decode_to_mvk(o["potency"]),
                        in_associations=self._decode_to_mvk(o["in_associations"]),
                        out_associations=self._decode_to_mvk(o["out_associations"]),
                        attributes=[self._decode_to_mvk(attr) for attr in o['linguistic_attributes']],
                        linguistic_type=self._decode_to_mvk(o["linguistic_type"]),
                        functions=self._decode_to_mvk(o["functions"]),
                        name=self._decode_to_mvk(o["name"]),
                        the_type=self._decode_to_mvk(o["the_type"])
               )

    def _decode_navigation(self, o):
        return Navigation(location=self._decode_to_mvk(o["location"]),
                        potency=self._decode_to_mvk(o["potency"]),
                        in_associations=self._decode_to_mvk(o["in_associations"]),
                        out_associations=self._decode_to_mvk(o["out_associations"]),
                        attributes=[self._decode_to_mvk(attr) for attr in o['linguistic_attributes']],
                        linguistic_type=self._decode_to_mvk(o["linguistic_type"]),
                        functions=self._decode_to_mvk(o["functions"]),
                        name=self._decode_to_mvk(o["name"]),
                        path=self._decode_to_mvk(o["path"])
               )

    def _decode_assignment(self, o):
        return Assignment(location=self._decode_to_mvk(o["location"]),
                        potency=self._decode_to_mvk(o["potency"]),
                        in_associations=self._decode_to_mvk(o["in_associations"]),
                        out_associations=self._decode_to_mvk(o["out_associations"]),
                        attributes=[self._decode_to_mvk(attr) for attr in o['linguistic_attributes']],
                        linguistic_type=self._decode_to_mvk(o["linguistic_type"]),
                        functions=self._decode_to_mvk(o["functions"]),
                        name=self._decode_to_mvk(o["name"]),
                        children=self._decode_to_mvk(o["children"])
               )

    def _decode_functioncall(self, o):
        return FunctionCall(location=self._decode_to_mvk(o["location"]),
                        potency=self._decode_to_mvk(o["potency"]),
                        in_associations=self._decode_to_mvk(o["in_associations"]),
                        out_associations=self._decode_to_mvk(o["out_associations"]),
                        attributes=[self._decode_to_mvk(attr) for attr in o['linguistic_attributes']],
                        linguistic_type=self._decode_to_mvk(o["linguistic_type"]),
                        functions=self._decode_to_mvk(o["functions"]),
                        name=self._decode_to_mvk(o["name"]),
                        function=self._decode_to_mvk(o["function"]),
                        arguments=self._decode_to_mvk(o["arguments"]),
                        called_expression=self._decode_to_mvk(o["called_expression"])
               )

    def _decode_argument(self, o):
        return Argument(location=self._decode_to_mvk(o["location"]),
                        potency=self._decode_to_mvk(o["potency"]),
                        in_associations=self._decode_to_mvk(o["in_associations"]),
                        out_associations=self._decode_to_mvk(o["out_associations"]),
                        attributes=[self._decode_to_mvk(attr) for attr in o['linguistic_attributes']],
                        linguistic_type=self._decode_to_mvk(o["linguistic_type"]),
                        functions=self._decode_to_mvk(o["functions"]),
                        name=self._decode_to_mvk(o["name"]),
                        key=self._decode_to_mvk(o["key"]),
                        expression=self._decode_to_mvk(o["expression"])
               )

    def _decode_operator(self, o):
        return {"location": self._decode_to_mvk(o["location"]),
                "potency": self._decode_to_mvk(o["potency"]),
                "in_associations": self._decode_to_mvk(o["in_associations"]),
                "out_associations": self._decode_to_mvk(o["out_associations"]),
                "attributes": [self._decode_to_mvk(attr) for attr in o['linguistic_attributes']],
                "linguistic_type": self._decode_to_mvk(o["linguistic_type"]),
                "functions": self._decode_to_mvk(o["functions"]),
                "name": self._decode_to_mvk(o["name"]),
                "children": self._decode_to_mvk(o["children"])
                }

    def _decode_not(self, o):
        return Not(**self._decode_operator(o))

    def _decode_or(self, o):
        return Or(**self._decode_operator(o))

    def _decode_and(self, o):
        return And(**self._decode_operator(o))

    def _decode_equal(self, o):
        return Equal(**self._decode_operator(o))

    def _decode_lessthan(self, o):
        return LessThan(**self._decode_operator(o))

    def _decode_greaterthan(self, o):
        return GreaterThan(**self._decode_operator(o))

    def _decode_in(self, o):
        return In(**self._decode_operator(o))

    def _decode_plus(self, o):
        return Plus(**self._decode_operator(o))

    def _decode_minus(self, o):
        return Minus(**self._decode_operator(o))

    def _decode_multiplication(self, o):
        return Multiplication(**self._decode_operator(o))

    def _decode_division(self, o):
        return Division(**self._decode_operator(o))

    def _decode_modulo(self, o):
        return Modulo(**self._decode_operator(o))
