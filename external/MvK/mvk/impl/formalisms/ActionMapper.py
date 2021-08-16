'''
Created on 6-mei-2014

@author: Simon
'''
from mvk.impl.python.changelog import MvKCreateLog
from mvk.impl.python.constants import CreateConstants, UpdateConstants
from mvk.impl.python.datatype import StringType
from mvk.impl.python.datavalue import MappingValue, LocationValue, TupleValue, StringValue, IntegerValue
from mvk.impl.python.python_representer import PythonRepresenter
import mvk.interfaces.action
from mvk.interfaces.physical_mapper import PhysicalMapper


class ActionMapper(PhysicalMapper):
    def __init__(self, **kwds):
        super(ActionMapper, self).__init__(**kwds)
        self.phys_attribute_mapping = MappingValue({LocationValue('ActionLanguage.name'): TupleValue((StringValue('name'),)),
                                                    LocationValue('Function.name'): TupleValue((StringValue('name'),)),
                                                    LocationValue('Function.type'): TupleValue((StringValue('type'),)),
                                                    LocationValue('Body.name'): TupleValue((StringValue('name'),)),
                                                    LocationValue('Parameter.name'): TupleValue((StringValue('name'),)),
                                                    LocationValue('Parameter.type'): TupleValue((StringValue('type'),)),
                                                    LocationValue('Parameter.parameter_type'): TupleValue((StringValue('parameter_type'),)),
                                                    LocationValue('Statement.name'): TupleValue((StringValue('name'),)),
                                                    LocationValue('Expression.name'): TupleValue((StringValue('name'),)),
                                                    LocationValue('Constant.type'): TupleValue((StringValue('type'),)),
                                                    LocationValue('Constant.value'): TupleValue((StringValue('value'),)),
                                                    LocationValue('Identifier.type'): TupleValue((StringValue('type'),)),
                                                    LocationValue('Identifier.value'): TupleValue((StringValue('value'),)),
                                                    LocationValue('Navigation.path'): TupleValue((StringValue('path'),)),
                                                    LocationValue('FunctionCall.function_name'): TupleValue((StringValue('function'),)),
                                                    LocationValue('Argument.name'): TupleValue((StringValue('name'),)),
                                                    LocationValue('Argument.key'): TupleValue((StringValue('key'),)),
                                                    LocationValue('NamedElement.name'): TupleValue((StringValue('name'),))
                                                    })
        self.phys_actions_update = MappingValue({LocationValue('ActionLanguage.name'): StringValue('set_name'),
                                                 LocationValue('Function.name'): StringValue('set_name'),
                                                 LocationValue('Function.type'): StringValue('set_type'),
                                                 LocationValue('Body.name'): StringValue('set_name'),
                                                 LocationValue('Parameter.name'): StringValue('set_name'),
                                                 LocationValue('Parameter.type'): StringValue('set_type'),
                                                 LocationValue('Parameter.parameter_type'): StringValue('set_parameter_type'),
                                                 LocationValue('Statement.name'): StringValue('set_name'),
                                                 LocationValue('Expression.name'): StringValue('set_name'),
                                                 LocationValue('Constant.type'): StringValue('set_type'),
                                                 LocationValue('Constant.value'): StringValue('set_value'),
                                                 LocationValue('Identifier.type'): StringValue('set_type'),
                                                 LocationValue('Identifier.value'): StringValue('set_value'),
                                                 LocationValue('Navigation.path'): StringValue('set_type'),
                                                 LocationValue('FunctionCall.function_name'): StringValue('set_function'),
                                                 LocationValue('Argument.name'): StringValue('set_name'),
                                                 LocationValue('Argument.key'): StringValue('set_key'),
                                                 LocationValue('NamedElement.name'): StringValue('set_name')
                                                 })

    def __create_actionlanguage(self, params):
        attributes = params[CreateConstants.ATTRS_KEY]
        attributes[StringValue('type_model')] = params[CreateConstants.TYPE_KEY]
        attributes[StringValue('potency')] = IntegerValue(0)
        from mvk.mvk import MvK
        return MvK().create(MappingValue({CreateConstants.LOCATION_KEY: params[CreateConstants.LOCATION_KEY],
                                          CreateConstants.TYPE_KEY: LocationValue('mvk.object.Model'),
                                          CreateConstants.ATTRS_KEY: attributes
                                          })
                            )

    def __create_function(self, params):
        attributes = params[CreateConstants.ATTRS_KEY]
        attributes[StringValue('class')] = params[CreateConstants.TYPE_KEY]
        attributes[StringValue('potency')] = IntegerValue(0)
        from mvk.mvk import MvK
        cl = MvK().create(MappingValue({CreateConstants.LOCATION_KEY: params[CreateConstants.LOCATION_KEY],
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.action.Function'),
                                        CreateConstants.ATTRS_KEY: attributes
                                        })
                          )
        if not cl.is_success():
            return cl
        a_cl = self.create(MappingValue({CreateConstants.LOCATION_KEY: params[CreateConstants.LOCATION_KEY] + StringValue('.') + attributes[StringValue('Function.name')],
                                         CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Body'),
                                         CreateConstants.ATTRS_KEY: MappingValue({StringValue('Body.name'): StringValue('body')})
                                         })
                           )
        if not a_cl.is_success():
            cl.set_status_code(a_cl.get_status_code())
            cl.set_status_message(a_cl.get_status_message())
        return cl

    def __create_body(self, params):
        attributes = params[CreateConstants.ATTRS_KEY]
        attributes[StringValue('class')] = params[CreateConstants.TYPE_KEY]
        attributes[StringValue('potency')] = IntegerValue(0)
        from mvk.mvk import MvK
        cl = MvK().create(MappingValue({CreateConstants.LOCATION_KEY: params[CreateConstants.LOCATION_KEY],
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.action.Body'),
                                        CreateConstants.ATTRS_KEY: attributes
                                        })
                          )
        if not cl.is_success():
            return cl
        idx = params[CreateConstants.LOCATION_KEY].rfind(StringValue('.'))
        from_el = MvK().read(params[CreateConstants.LOCATION_KEY]).get_item()
        to_body = params[CreateConstants.LOCATION_KEY] + StringValue('.') + attributes[StringValue('Body.name')]
        comp = None
        portname = None
        if isinstance(from_el, mvk.interfaces.action.Function):
            comp = 'function_body'
            portname = 'from_function'
        if isinstance(from_el, mvk.interfaces.action.WhileLoop):
            comp = 'whileloop_body'
            portname = 'from_whileloop'
        if isinstance(from_el, mvk.interfaces.action.IfStatement):
            comp = 'ifstatement_body'
            portname = 'from_ifstatement'
        assert comp
        parent = MvK().read(params[CreateConstants.LOCATION_KEY].substring(stop=idx)).get_item()
        while not isinstance(parent, mvk.interfaces.object.Model):
            parent = parent.get_parent()
        a_cl = MvK().create(MappingValue({CreateConstants.LOCATION_KEY: parent.get_location(),
                                          CreateConstants.TYPE_KEY: LocationValue('mvk.object.Composition'),
                                          CreateConstants.ATTRS_KEY: MappingValue({StringValue('NamedElement.name'): from_el.get_name() + StringValue('_b_') + attributes[StringValue('Body.name')],
                                                                                   StringValue('potency'): IntegerValue(0),
                                                                                   StringValue('class'): LocationValue('protected.formalisms.ActionLanguage.' + comp),
                                                                                   StringValue(portname): from_el.get_location(),
                                                                                   StringValue('to_body'): to_body
                                                                                   })
                                          })
                            )
        if not a_cl.is_success():
            cl.set_status_code(a_cl.get_status_code())
            cl.set_status_message(a_cl.get_status_message())
        return cl

    def __create_parameter(self, params):
        attributes = params[CreateConstants.ATTRS_KEY]
        attributes[StringValue('class')] = params[CreateConstants.TYPE_KEY]
        attributes[StringValue('potency')] = IntegerValue(0)
        from mvk.mvk import MvK
        cl = MvK().create(MappingValue({CreateConstants.LOCATION_KEY: params[CreateConstants.LOCATION_KEY],
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.action.Parameter'),
                                        CreateConstants.ATTRS_KEY: attributes
                                        })
                          )
        if not cl.is_success():
            return cl
        idx = params[CreateConstants.LOCATION_KEY].rfind(StringValue('.'))
        from_el = MvK().read(params[CreateConstants.LOCATION_KEY]).get_item()
        to_param = params[CreateConstants.LOCATION_KEY] + StringValue('.') + attributes[StringValue('Parameter.name')]
        from mvk.impl.python.object import ClabjectReference
        comp = None
        portname = None
        if isinstance(from_el, mvk.interfaces.action.Function):
            comp = 'function_parameters'
            portname = 'from_function'
        assert comp
        parent = MvK().read(params[CreateConstants.LOCATION_KEY].substring(stop=idx)).get_item()
        while not isinstance(parent, mvk.interfaces.object.Model):
            parent = parent.get_parent()
        a_cl = MvK().create(MappingValue({CreateConstants.LOCATION_KEY: parent.get_location(),
                                          CreateConstants.TYPE_KEY: LocationValue('mvk.object.Composition'),
                                          CreateConstants.ATTRS_KEY: MappingValue({StringValue('NamedElement.name'): from_el.get_name() + StringValue('_p_') + attributes[StringValue('Parameter.name')],
                                                                                   StringValue('potency'): IntegerValue(0),
                                                                                   StringValue('class'): LocationValue('protected.formalisms.ActionLanguage.' + comp),
                                                                                   StringValue(portname): from_el.get_location(),
                                                                                   StringValue('to_parameter'): to_param
                                                                                   })
                                          })
                            )
        if not a_cl.is_success():
            cl.set_status_code(a_cl.get_status_code())
            cl.set_status_message(a_cl.get_status_message())
        return cl

    def __create_statement(self, params, statement_type):
        def add_statement_to_parent(params):
            attributes = params[CreateConstants.ATTRS_KEY]
            idx = params[CreateConstants.LOCATION_KEY].rfind(StringValue('.'))
            from mvk.mvk import MvK
            from_el = MvK().read(params[CreateConstants.LOCATION_KEY]).get_item()
            to_param = params[CreateConstants.LOCATION_KEY] + StringValue('.') + attributes[StringValue('Statement.name')]
            comp = None
            portname = None
            if isinstance(from_el, mvk.interfaces.action.Body):
                comp = 'body_statement'
                portname = 'from_body'
            parent = MvK().read(params[CreateConstants.LOCATION_KEY].substring(stop=idx)).get_item()
            while not isinstance(parent, mvk.interfaces.object.Model):
                parent = parent.get_parent()
            return MvK().create(MappingValue({CreateConstants.LOCATION_KEY: parent.get_location(),
                                              CreateConstants.TYPE_KEY: LocationValue('mvk.object.Composition'),
                                              CreateConstants.ATTRS_KEY: MappingValue({StringValue('NamedElement.name'): from_el.get_name() + StringValue('_s_') + attributes[StringValue('Statement.name')],
                                                                                       StringValue('potency'): IntegerValue(0),
                                                                                       StringValue('class'): LocationValue('protected.formalisms.ActionLanguage.' + comp),
                                                                                       StringValue(portname): from_el.get_location(),
                                                                                       StringValue('to_statement'): to_param
                                                                                       })
                                              })
                                )
        attributes = params[CreateConstants.ATTRS_KEY]
        attributes[StringValue('class')] = params[CreateConstants.TYPE_KEY]
        attributes[StringValue('potency')] = IntegerValue(0)
        from mvk.mvk import MvK
        cl = MvK().create(MappingValue({CreateConstants.LOCATION_KEY: params[CreateConstants.LOCATION_KEY],
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.action.' + statement_type),
                                        CreateConstants.ATTRS_KEY: attributes
                                        })
                          )
        if not cl.is_success():
            return cl
        a_cl = add_statement_to_parent(params)
        if not a_cl.is_success():
            cl.set_status_code(a_cl.get_status_code())
            cl.set_status_message(a_cl.get_status_message())
        return cl

    def __create_expression_statement(self, params):
        return self.__create_statement(params, 'ExpressionStatement')

    def __create_return_statement(self, params):
        return self.__create_statement(params, 'ReturnStatement')

    def __create_declaration_statement(self, params):
        return self.__create_statement(params, 'DeclarationStatement')

    def __create_while_loop(self, params):
        cl = self.__create_statement(params, 'WhileLoop')
        if not cl.is_success():
            return cl
        a_cl = self.create(MappingValue({CreateConstants.LOCATION_KEY: params[CreateConstants.LOCATION_KEY] + StringValue('.') + params[CreateConstants.ATTRS_KEY][StringValue('Statement.name')],
                                         CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Body'),
                                         CreateConstants.ATTRS_KEY: MappingValue({StringValue('Body.name'): StringValue('body')})
                                         })
                           )
        if not a_cl.is_success():
            cl.set_status_code(a_cl.get_status_code())
            cl.set_status_message(a_cl.get_status_message())
        return cl

    def __create_if_statement(self, params):
        cl = self.__create_statement(params, 'IfStatement')
        if not cl.is_success():
            return cl
        a_cl = self.create(MappingValue({CreateConstants.LOCATION_KEY: params[CreateConstants.LOCATION_KEY] + StringValue('.') + params[CreateConstants.ATTRS_KEY][StringValue('Statement.name')],
                                         CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Body'),
                                         CreateConstants.ATTRS_KEY: MappingValue({StringValue('Body.name'): StringValue('ifbody')})
                                         })
                           )
        if not a_cl.is_success():
            cl.set_status_code(a_cl.get_status_code())
            cl.set_status_message(a_cl.get_status_message())
        a_cl = self.create(MappingValue({CreateConstants.LOCATION_KEY: params[CreateConstants.LOCATION_KEY] + StringValue('.') + params[CreateConstants.ATTRS_KEY][StringValue('Statement.name')],
                                         CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Body'),
                                         CreateConstants.ATTRS_KEY: MappingValue({StringValue('Body.name'): StringValue('elsebody')})
                                         })
                           )
        if not a_cl.is_success():
            cl.set_status_code(a_cl.get_status_code())
            cl.set_status_message(a_cl.get_status_message())
        return cl

    def __create_break_statement(self, params):
        return self.__create_statement(params, 'BreakStatement')

    def __create_continue_statement(self, params):
        return self.__create_statement(params, 'ContinueStatement')

    def __create_expression(self, params, expression_type):
        def add_expression_to_parent(self):
            attributes = params[CreateConstants.ATTRS_KEY]
            idx = params[CreateConstants.LOCATION_KEY].rfind(StringValue('.'))
            from mvk.mvk import MvK
            from_el = MvK().read(params[CreateConstants.LOCATION_KEY]).get_item()
            to_expr = params[CreateConstants.LOCATION_KEY] + StringValue('.') + attributes[StringValue('Expression.name')]
            comp = None
            to_portname = 'to_expression'
            from_portname = None
            if isinstance(from_el, mvk.interfaces.action.ExpressionStatement):
                comp = 'expressionstatement_expression'
                from_portname = 'from_expressionstatement'
            if isinstance(from_el, mvk.interfaces.action.DeclarationStatement) and expression_type == 'Identifier':
                comp = 'declarationstatement_identifier'
                from_portname = 'from_declarationstatement'
                to_portname = 'to_identifier'
            elif isinstance(from_el, mvk.interfaces.action.DeclarationStatement):
                comp = 'declarationstatement_expression'
                from_portname = 'from_declarationstatement'
                to_portname = 'to_expression'
            elif isinstance(from_el, mvk.interfaces.action.WhileLoop):
                comp = 'whileloop_expression'
                from_portname = 'from_whileloop'
            elif isinstance(from_el, mvk.interfaces.action.IfStatement):
                comp = 'ifstatement_expression'
                from_portname = 'from_ifstatement'
            elif isinstance(from_el, mvk.interfaces.action.Assignment):
                comp = 'assignment_expression'
                from_portname = 'from_assignment'
            elif isinstance(from_el, mvk.interfaces.action.FunctionCall):
                comp = 'functioncall_expression'
                from_portname = 'from_functioncall'
            elif isinstance(from_el, mvk.interfaces.action.Argument):
                comp = 'argument_expression'
                from_portname = 'from_argument'
            elif isinstance(from_el, mvk.interfaces.action.Operator):
                comp = 'operator_expression'
                from_portname = 'from_operator'
            assert comp
            parent = MvK().read(params[CreateConstants.LOCATION_KEY].substring(stop=idx)).get_item()
            while not isinstance(parent, mvk.interfaces.object.Model):
                parent = parent.get_parent()
            return MvK().create(MappingValue({CreateConstants.LOCATION_KEY: parent.get_location(),
                                              CreateConstants.TYPE_KEY: LocationValue('mvk.object.Composition'),
                                              CreateConstants.ATTRS_KEY: MappingValue({StringValue('NamedElement.name'): from_el.get_name() + StringValue('_e_') + attributes[StringValue('Expression.name')],
                                                                                       StringValue('potency'): IntegerValue(0),
                                                                                       StringValue('class'): LocationValue('protected.formalisms.ActionLanguage.' + comp),
                                                                                       StringValue(from_portname): from_el.get_location(),
                                                                                       StringValue(to_portname): to_expr
                                                                                       })
                                              })
                                )
        attributes = params[CreateConstants.ATTRS_KEY]
        attributes[StringValue('class')] = params[CreateConstants.TYPE_KEY]
        attributes[StringValue('potency')] = IntegerValue(0)
        from mvk.mvk import MvK
        cl = MvK().create(MappingValue({CreateConstants.LOCATION_KEY: params[CreateConstants.LOCATION_KEY],
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.action.' + expression_type),
                                        CreateConstants.ATTRS_KEY: attributes
                                        })
                          )
        if not cl.is_success():
            return cl
        a_cl = add_expression_to_parent(params)
        if not a_cl.is_success():
            cl.set_status_code(a_cl.get_status_code())
            cl.set_status_message(a_cl.get_status_message())
        return cl

    def __create_constant(self, params):
        return self.__create_expression(params, 'Constant')

    def __create_identifier(self, params):
        return self.__create_expression(params, 'Identifier')

    def __create_navigation(self, params):
        return self.__create_expression(params, 'Navigation')

    def __create_assignment(self, params):
        return self.__create_expression(params, 'Assignment')

    def __create_function_call(self, params):
        return self.__create_expression(params, 'FunctionCall')

    def __create_argument(self, params):
        attributes = params[CreateConstants.ATTRS_KEY]
        attributes[StringValue('class')] = params[CreateConstants.TYPE_KEY]
        attributes[StringValue('potency')] = IntegerValue(0)
        from mvk.mvk import MvK
        cl = MvK().create(MappingValue({CreateConstants.LOCATION_KEY: params[CreateConstants.LOCATION_KEY],
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.action.Argument'),
                                        CreateConstants.ATTRS_KEY: attributes
                                        })
                          )
        if not cl.is_success():
            return cl
        idx = params[CreateConstants.LOCATION_KEY].rfind(StringValue('.'))
        from_el = MvK().read(params[CreateConstants.LOCATION_KEY]).get_item()
        to_arg = params[CreateConstants.LOCATION_KEY] + StringValue('.') + attributes[StringValue('Argument.name')]
        parent = MvK().read(params[CreateConstants.LOCATION_KEY].substring(stop=idx)).get_item()
        while not isinstance(parent, mvk.interfaces.object.Model):
            parent = parent.get_parent()
        a_cl = MvK().create(MappingValue({CreateConstants.LOCATION_KEY: parent.get_location(),
                                          CreateConstants.TYPE_KEY: LocationValue('mvk.object.Composition'),
                                          CreateConstants.ATTRS_KEY: MappingValue({StringValue('NamedElement.name'): from_el.get_name() + StringValue('_b_') + attributes[StringValue('Argument.name')],
                                                                                   StringValue('potency'): IntegerValue(0),
                                                                                   StringValue('class'): LocationValue('protected.formalisms.ActionLanguage.functioncall_argument'),
                                                                                   StringValue('from_functioncall'): from_el.get_location(),
                                                                                   StringValue('to_argument'): to_arg
                                                                                   })
                                          })
                            )
        if not a_cl.is_success():
            cl.set_status_code(a_cl.get_status_code())
            cl.set_status_message(a_cl.get_status_message())
        return cl

    def __create_not(self, params):
        return self.__create_expression(params, 'Not')

    def __create_or(self, params):
        return self.__create_expression(params, 'Or')

    def __create_and(self, params):
        return self.__create_expression(params, 'And')

    def __create_equal(self, params):
        return self.__create_expression(params, 'Equal')

    def __create_less_than(self, params):
        return self.__create_expression(params, 'LessThan')

    def __create_greater_than(self, params):
        return self.__create_expression(params, 'GreaterThan')

    def __create_in(self, params):
        return self.__create_expression(params, 'In')

    def __create_plus(self, params):
        return self.__create_expression(params, 'Plus')

    def __create_minus(self, params):
        return self.__create_expression(params, 'Minus')

    def __create_multiplication(self, params):
        self.__create_expression(params, 'Multiplication')

    def __create_division(self, params):
        return self.__create_expression(params, 'Division')

    def __create_modulo(self, params):
        return self.__create_expression(params, 'Modulo')

    def __create_unknown(self, params):
        cl = MvKCreateLog()
        cl.set_status_code(CreateConstants.BAD_REQUEST_CODE)
        cl.set_status_message(StringValue('Unknown type!'))
        return cl

    def create(self, params):
        types = {LocationValue('protected.formalisms.ActionLanguage'): self.__create_actionlanguage,
                 LocationValue('protected.formalisms.ActionLanguage.Function'): self.__create_function,
                 LocationValue('protected.formalisms.ActionLanguage.Body'): self.__create_body,
                 LocationValue('protected.formalisms.ActionLanguage.Parameter'): self.__create_parameter,
                 LocationValue('protected.formalisms.ActionLanguage.ExpressionStatement'): self.__create_expression_statement,
                 LocationValue('protected.formalisms.ActionLanguage.ReturnStatement'): self.__create_return_statement,
                 LocationValue('protected.formalisms.ActionLanguage.DeclarationStatement'): self.__create_declaration_statement,
                 LocationValue('protected.formalisms.ActionLanguage.WhileLoop'): self.__create_while_loop,
                 LocationValue('protected.formalisms.ActionLanguage.IfStatement'): self.__create_if_statement,
                 LocationValue('protected.formalisms.ActionLanguage.BreakStatement'): self.__create_break_statement,
                 LocationValue('protected.formalisms.ActionLanguage.ContinueStatement'): self.__create_continue_statement,
                 LocationValue('protected.formalisms.ActionLanguage.Constant'): self.__create_constant,
                 LocationValue('protected.formalisms.ActionLanguage.Identifier'): self.__create_identifier,
                 LocationValue('protected.formalisms.ActionLanguage.Navigation'): self.__create_navigation,
                 LocationValue('protected.formalisms.ActionLanguage.Assignment'): self.__create_assignment,
                 LocationValue('protected.formalisms.ActionLanguage.FunctionCall'): self.__create_function_call,
                 LocationValue('protected.formalisms.ActionLanguage.Argument'): self.__create_argument,
                 LocationValue('protected.formalisms.ActionLanguage.Not'): self.__create_not,
                 LocationValue('protected.formalisms.ActionLanguage.Or'): self.__create_or,
                 LocationValue('protected.formalisms.ActionLanguage.And'): self.__create_and,
                 LocationValue('protected.formalisms.ActionLanguage.Equal'): self.__create_equal,
                 LocationValue('protected.formalisms.ActionLanguage.LessThan'): self.__create_less_than,
                 LocationValue('protected.formalisms.ActionLanguage.GreaterThan'): self.__create_greater_than,
                 LocationValue('protected.formalisms.ActionLanguage.In'): self.__create_in,
                 LocationValue('protected.formalisms.ActionLanguage.Plus'): self.__create_plus,
                 LocationValue('protected.formalisms.ActionLanguage.Minus'): self.__create_minus,
                 LocationValue('protected.formalisms.ActionLanguage.Multiplication'): self.__create_multiplication,
                 LocationValue('protected.formalisms.ActionLanguage.Division'): self.__create_division,
                 LocationValue('protected.formalisms.ActionLanguage.Modulo'): self.__create_modulo}
        return types.get(params[CreateConstants.TYPE_KEY], self.__create_unknown)(params)

    def read(self, location):
        raise NotImplementedError()

    def update(self, params):
        types = {LocationValue('protected.formalisms.ActionLanguage'): PythonRepresenter.MODEL,
                 LocationValue('protected.formalisms.ActionLanguage.Function'): PythonRepresenter.FUNCTION,
                 LocationValue('protected.formalisms.ActionLanguage.Body'): PythonRepresenter.BODY,
                 LocationValue('protected.formalisms.ActionLanguage.Parameter'): PythonRepresenter.PARAMETER,
                 LocationValue('protected.formalisms.ActionLanguage.ExpressionStatement'): PythonRepresenter.EXPRESSIONSTATEMENT,
                 LocationValue('protected.formalisms.ActionLanguage.ReturnStatement'): PythonRepresenter.RETURNSTATEMENT,
                 LocationValue('protected.formalisms.ActionLanguage.DeclarationStatement'): PythonRepresenter.DECLARATIONSTATEMENT,
                 LocationValue('protected.formalisms.ActionLanguage.WhileLoop'): PythonRepresenter.WHILELOOP,
                 LocationValue('protected.formalisms.ActionLanguage.IfStatement'): PythonRepresenter.IFSTATEMENT,
                 LocationValue('protected.formalisms.ActionLanguage.BreakStatement'): PythonRepresenter.BREAKSTATEMENT,
                 LocationValue('protected.formalisms.ActionLanguage.ContinueStatement'): PythonRepresenter.CONTINUESTATEMENT,
                 LocationValue('protected.formalisms.ActionLanguage.Constant'): PythonRepresenter.CONSTANT,
                 LocationValue('protected.formalisms.ActionLanguage.Identifier'): PythonRepresenter.IDENTIFIER,
                 LocationValue('protected.formalisms.ActionLanguage.Navigation'): PythonRepresenter.NAVIGATION,
                 LocationValue('protected.formalisms.ActionLanguage.Assignment'): PythonRepresenter.ASSIGNMENT,
                 LocationValue('protected.formalisms.ActionLanguage.FunctionCall'): PythonRepresenter.FUNCTIONCALL,
                 LocationValue('protected.formalisms.ActionLanguage.Argument'): PythonRepresenter.ARGUMENT,
                 LocationValue('protected.formalisms.ActionLanguage.Not'): PythonRepresenter.NOT,
                 LocationValue('protected.formalisms.ActionLanguage.Or'): PythonRepresenter.OR,
                 LocationValue('protected.formalisms.ActionLanguage.And'): PythonRepresenter.AND,
                 LocationValue('protected.formalisms.ActionLanguage.Equal'): PythonRepresenter.EQUAL,
                 LocationValue('protected.formalisms.ActionLanguage.LessThan'): PythonRepresenter.LESSTHAN,
                 LocationValue('protected.formalisms.ActionLanguage.GreaterThan'): PythonRepresenter.GREATERTHAN,
                 LocationValue('protected.formalisms.ActionLanguage.In'): PythonRepresenter.IN,
                 LocationValue('protected.formalisms.ActionLanguage.Plus'): PythonRepresenter.PLUS,
                 LocationValue('protected.formalisms.ActionLanguage.Minus'): PythonRepresenter.MINUS,
                 LocationValue('protected.formalisms.ActionLanguage.Multiplication'): PythonRepresenter.MODEL,
                 LocationValue('protected.formalisms.ActionLanguage.Division'): PythonRepresenter.MODEL,
                 LocationValue('protected.formalisms.ActionLanguage.Modulo'): PythonRepresenter.MODEL}
        from mvk.mvk import MvK
        params[UpdateConstants.TYPE_KEY] = types[params[UpdateConstants.TYPE_KEY]]
        item = MvK().read(params[UpdateConstants.LOCATION_KEY]).get_item()
        cl = item.update(params)
        return cl

    def delete(self, location):
        raise NotImplementedError()

    def get_physical_attribute_mapping(self):
        return self.phys_attribute_mapping

    def get_physical_update_actions(self):
        return self.phys_actions_update
