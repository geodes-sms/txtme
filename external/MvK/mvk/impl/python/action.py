'''
Created on 24-apr.-2014

@author: Simon
'''
from mvk.impl.python.changelog import MvKReadLog, MvKUpdateLog
from mvk.impl.python.constants import ReadConstants, CreateConstants, UpdateConstants
from mvk.impl.python.datatype import LocationType
from mvk.impl.python.datavalue import ImmutableSequenceValue, SequenceValue, StringValue, AnyValue, LocationValue, IntegerValue, MappingValue, BooleanValue
from mvk.impl.python.element import NamedElement, TypedElement, Element
from mvk.impl.python.exception import MvKKeyError, MvKException, MvKValueError, MvKPotencyError
from mvk.impl.python.object import Node, ClabjectReference
import mvk.interfaces.action
from mvk.util.logger import get_logger


logger = get_logger('object')


class Function(Node, TypedElement, mvk.interfaces.action.Function):
    ''' == CONSTRUCTOR == '''
    def __init__(self, **kwargs):
        self.body = None
        self.parameters = SequenceValue()
        self.param_lookup = {}

        super(Function, self).__init__(**kwargs)

    ''' == PUBLIC INTERFACE == '''
    def get_body(self):
        return self.body

    def get_parameters(self):
        return ImmutableSequenceValue(self.parameters)

    def __eq__(self, other):
        return (super(Function, self).__eq__(other) and
                self.get_statements() == other.get_statements() and
                self.get_parameters() == other.get_parameters())

    ''' == PYTHON SPECIFIC == '''
    def add_parameter(self, param, idx=None):
        if idx is None:
            idx = self.parameters.len()
        assert isinstance(param, mvk.interfaces.action.Parameter)
        assert (isinstance(idx, mvk.interfaces.datavalue.IntegerValue) and
                isinstance(idx.typed_by(), mvk.interfaces.datatype.IntegerType))
        assert param.get_name() not in self.param_lookup
        self.parameters.insert(idx, param)
        self.param_lookup[param.get_name()] = param
        param.set_parent(self)

    def remove_parameter(self, param):
        assert isinstance(param, mvk.interfaces.action.Parameter)
        assert param.get_name() in self.param_lookup
        del self.param_lookup[param.get_name()]
        self.parameters.remove(param)
        param.set_parent(None)

    def set_body(self, body):
        assert body is None or isinstance(body, mvk.interfaces.action.Body)
        self.body = body
        if self.body:
            self.body.set_parent(self)

    ''' == CRUD == '''
    @classmethod
    def _check_params_create(cls, params):
        res = Node._check_params_create(params)
        if res is not None:
            return res
        from mvk.impl.python.constants import CreateConstants
        attributes = params[CreateConstants.ATTRS_KEY]
        cls._check_param(attributes,
                         StringValue('type'),
                         mvk.interfaces.datatype.Type)

    @classmethod
    def _create_inst(cls, params, cl):
        from mvk.impl.python.constants import CreateConstants
        attributes = params[CreateConstants.ATTRS_KEY]
        name = attributes[StringValue('name')]
        potency = attributes[StringValue('potency')] if StringValue('potency') in attributes else None
        clz = attributes[StringValue('class')]
        the_type = attributes[StringValue('type')]
        assert logger.debug('Creating %s with name %s, potency %s, type %s, the_type %s' %
                            (cls.__name__, name, potency, clz, the_type))
        n = cls(name=name, potency=potency, the_type=the_type,
                l_type=ClabjectReference(path=clz))
        cl.add_attr_change(StringValue('name'), n.get_name())
        cl.add_attr_change(StringValue('potency'), n.get_potency())
        cl.add_attr_change(StringValue('class'), n.typed_by().get_location())
        cl.add_attr_change(StringValue('type'), StringValue(str(n.get_type())))
        return n

    @classmethod
    def _add_to_parent(cls, inst, parent):
        assert isinstance(parent, mvk.interfaces.object.Node)
        parent.add_function(inst)

    def _remove_from_parent(self):
        self.get_parent().remove_function(self.get_name())

    @classmethod
    def _check_params_update(cls, params):
        cl = Node._check_params_update(params)
        if cl is not None:
            return cl
        cl = MvKUpdateLog()
        if not (isinstance(params, mvk.interfaces.datavalue.MappingValue) and
                isinstance(params.typed_by(), mvk.interfaces.datatype.MappingType)):
            cl.set_status_code(UpdateConstants.MALFORMED_REQUEST_CODE)
            cl.set_status_message(StringValue('Expected a MappingValue'))
            return cl
        try:
            cls._check_param(params,
                             CreateConstants.ATTRS_KEY,
                             mvk.interfaces.datavalue.MappingValue,
                             mvk.interfaces.datatype.MappingType)
            attributes = params[CreateConstants.ATTRS_KEY]
            cls._check_param(attributes,
                             StringValue('type'),
                             mvk.interfaces.datatype.Type,
                             req=False)
        except MvKException, e:
            cl.set_status_code(CreateConstants.BAD_REQUEST_CODE)
            cl.set_status_message(e.get_message())
            return cl
        return None

    def _update(self, params):
        cl = Node._update(self, params)
        if not cl.is_success():
            return cl
        attributes = params[UpdateConstants.ATTRS_KEY]
        it = attributes.__iter__()
        try:
            while it.has_next():
                name = it.next()
                if self.typed_by().get_location().startswith(StringValue('mvk')):
                    if name == StringValue('type'):
                        new_val = attributes[name]
                        cl.add_attr_change(name, self.get_type(), new_val)
                        self.set_type(new_val)
        except MvKKeyError, e:
            ''' TODO: revert! '''
            cl.set_status_code(UpdateConstants.NOT_FOUND_CODE)
            cl.set_status_message(e.get_message())
        except MvKValueError, e:
            ''' TODO: revert! '''
            cl.set_status_code(UpdateConstants.NOT_FOUND_CODE)
            cl.set_status_message(e.get_message())
        except MvKPotencyError, e:
            ''' TODO: revert! '''
            cl.set_status_code(UpdateConstants.BAD_REQUEST_CODE)
            cl.set_status_message(e.get_message())
        cl.set_status_code(UpdateConstants.SUCCESS_CODE)
        cl.set_status_message(StringValue('Successfully updated function.'))
        return cl

    def read(self, location):
        from mvk.impl.python.python_representer import PythonRepresenter
        assert (isinstance(location, LocationValue) and
                isinstance(location.typed_by(), LocationType))

        rl = MvKReadLog()
        if location == LocationValue(''):
            ''' Base case. '''
            rl.set_item(self)
            rl.set_location(self.get_location())
            rl.set_status_code(ReadConstants.SUCCESS_CODE)
            rl.set_type(self.typed_by().get_location())
            rl.set_status_message(StringValue('Success!'))
            return rl
        else:
            idx = location.find(StringValue('.'))
            el_name = location if idx == IntegerValue(-1) else location.substring(stop=idx)
            if el_name in self.param_lookup:
                return self.param_lookup[el_name].read(LocationValue('') if idx == IntegerValue(-1) else location.substring(start=idx + IntegerValue(1)))
            elif self.get_body() is not None and el_name == StringValue('body'):
                return self.get_body().read(LocationValue('') if idx == IntegerValue(-1) else location.substring(start=idx + IntegerValue(1)))
            else:
                return Node.read(self, location)


class Body(SequenceValue, Node, mvk.interfaces.action.Body):
    ''' == CONSTRUCTOR == '''
    def __init__(self, **kwds):
        self.stmt_lookup = {}
        super(Body, self).__init__(**kwds)

    ''' == PUBLIC INTERFACE == '''
    def get_statement(self, name):
        return self.stmt_lookup[name]

    def typed_by(self):
        return Node.typed_by(self)

    def __eq__(self, other):
        if not Node.__eq__(self, other):
            return BooleanValue(False)
        it_self = self.__iter__()
        it_other = other.__iter__()
        while (it_self.has_next()):
            if not it_self.next() == it_other.next():
                return BooleanValue(False)
        return BooleanValue(True)

    ''' == PYTHON SPECIFIC == '''
    def add_statement(self, stmt, idx=None):
        if idx is None:
            idx = self.len()
        assert isinstance(stmt, mvk.interfaces.action.Statement)
        assert (isinstance(idx, mvk.interfaces.datavalue.IntegerValue) and
                isinstance(idx.typed_by(), mvk.interfaces.datatype.IntegerType))
        assert stmt.get_name() not in self.stmt_lookup
        self.insert(idx, stmt)
        self.stmt_lookup[stmt.get_name()] = stmt
        stmt.set_parent(self)

    def remove_statement(self, stmt):
        assert isinstance(stmt, mvk.interfaces.action.Statement)
        assert stmt.get_name() in self.stmt_lookup
        self.remove(stmt)
        del self.stmt_lookup[stmt.get_name()]
        stmt.set_parent(None)

    def read(self, location):
        from mvk.impl.python.python_representer import PythonRepresenter
        assert (isinstance(location, LocationValue) and
                isinstance(location.typed_by(), LocationType))

        rl = MvKReadLog()
        if location == LocationValue(''):
            ''' Base case. '''
            rl.set_item(self)
            rl.set_location(self.get_location())
            rl.set_status_code(ReadConstants.SUCCESS_CODE)
            rl.set_type(self.typed_by().get_location())
            rl.set_status_message(StringValue('Success!'))
            return rl
        else:
            idx = location.find(StringValue('.'))
            el_name = location if idx == IntegerValue(-1) else location.substring(stop=idx)
            if el_name in self.stmt_lookup:
                return self.stmt_lookup[el_name].read(LocationValue('') if idx == IntegerValue(-1) else location.substring(start=idx + IntegerValue(1)))
            else:
                return Node.read(self, location)

    ''' == CRUD == '''
    @classmethod
    def _add_to_parent(cls, inst, parent):
        assert (isinstance(parent, mvk.interfaces.action.Function) or
                isinstance(parent, mvk.interfaces.action.WhileLoop) or
                isinstance(parent, mvk.interfaces.action.IfStatement))
        if isinstance(parent, mvk.interfaces.action.Function) or isinstance(parent, mvk.interfaces.action.WhileLoop):
            parent.set_body(inst)
        elif inst.get_name() == StringValue('ifbody'):
            parent.set_if_body(inst)
        elif inst.get_name() == StringValue('elsebody'):
            parent.set_else_body(inst)

    def _remove_from_parent(self):
        parent = self.get_parent()
        if isinstance(parent, mvk.interfaces.action.Function) or isinstance(parent, mvk.interfaces.action.WhileLoop):
            parent.set_body(None)
        elif self.get_name() == StringValue('ifbody'):
            parent.set_if_body(None)
        elif self.get_name() == StringValue('elsebody'):
            parent.set_else_body(None)


class Parameter(Node, TypedElement, mvk.interfaces.action.Parameter):
    ''' == CONSTRUCTOR == '''
    def __init__(self, param_type, **kwargs):
        self.set_parameter_type(param_type)
        super(Parameter, self).__init__(**kwargs)

    ''' == PUBLIC INTERFACE == '''
    def get_parameter_type(self):
        return self.param_type

    def __eq__(self, other):
        return (super(Parameter, self).__eq__(other) and
                self.get_parameter_type() == other.get_parameter_type())

    ''' == PYTHON SPECIFIC == '''
    def set_parameter_type(self, param_type):
        assert (isinstance(param_type, mvk.interfaces.datavalue.StringValue) and
                isinstance(param_type.typed_by(), mvk.interfaces.datatype.StringType) and
                param_type == StringValue('in') or param_type == StringValue('out') or param_type == StringValue('inout'))
        self.param_type = param_type

    ''' == CRUD == '''
    @classmethod
    def _check_params_create(cls, params):
        res = Node._check_params_create(params)
        if res is not None:
            return res
        from mvk.impl.python.constants import CreateConstants
        attributes = params[CreateConstants.ATTRS_KEY]
        cls._check_param(attributes,
                         StringValue('type'),
                         mvk.interfaces.datatype.Type)
        cls._check_param(attributes,
                         StringValue('parameter_type'),
                         mvk.interfaces.datavalue.StringValue,
                         mvk.interfaces.datatype.StringType)

    @classmethod
    def _create_inst(cls, params, cl):
        from mvk.impl.python.constants import CreateConstants
        attributes = params[CreateConstants.ATTRS_KEY]
        name = attributes[StringValue('name')]
        potency = attributes[StringValue('potency')] if StringValue('potency') in attributes else None
        clz = attributes[StringValue('class')]
        the_type = attributes[StringValue('type')]
        parameter_type = attributes[StringValue('parameter_type')]
        assert logger.debug('Creating %s with name %s, potency %s, type %s, the_type %s, parameter_type %s' %
                            (cls.__name__, name, potency, clz, the_type, parameter_type))
        n = cls(name=name, potency=potency, param_type=parameter_type,
                the_type=the_type, l_type=ClabjectReference(path=clz))
        cl.add_attr_change(StringValue('name'), n.get_name())
        cl.add_attr_change(StringValue('potency'), n.get_potency())
        cl.add_attr_change(StringValue('class'), n.typed_by().get_location())
        cl.add_attr_change(StringValue('type'), StringValue(str(n.get_type())))
        cl.add_attr_change(StringValue('parameter_type'), n.get_parameter_type())
        return n

    @classmethod
    def _add_to_parent(cls, inst, parent):
        assert isinstance(parent, mvk.interfaces.action.Function)
        parent.add_parameter(inst)

    def _remove_from_parent(self):
        self.get_parent().remove_parameter(self)

    @classmethod
    def _check_params_update(cls, params):
        cl = Node._check_params_update(params)
        if cl is not None:
            return cl
        cl = MvKUpdateLog()
        if not (isinstance(params, mvk.interfaces.datavalue.MappingValue) and
                isinstance(params.typed_by(), mvk.interfaces.datatype.MappingType)):
            cl.set_status_code(UpdateConstants.MALFORMED_REQUEST_CODE)
            cl.set_status_message(StringValue('Expected a MappingValue'))
            return cl
        try:
            cls._check_param(params,
                             CreateConstants.ATTRS_KEY,
                             mvk.interfaces.datavalue.MappingValue,
                             mvk.interfaces.datatype.MappingType)
            attributes = params[CreateConstants.ATTRS_KEY]
            cls._check_param(attributes,
                             StringValue('parameter_type'),
                             mvk.interfaces.datavalue.StringValue,
                             mvk.interfaces.datatype.StringType,
                             req=False)
        except MvKException, e:
            cl.set_status_code(CreateConstants.BAD_REQUEST_CODE)
            cl.set_status_message(e.get_message())
            return cl
        return None

    def _update(self, params):
        cl = Node._update(self, params)
        if not cl.is_success():
            return cl
        attributes = params[UpdateConstants.ATTRS_KEY]
        it = attributes.__iter__()
        try:
            while it.has_next():
                name = it.next()
                if self.typed_by().get_location().startswith(StringValue('mvk')):
                    if name == StringValue('parameter_type'):
                        new_val = attributes[name]
                        cl.add_attr_change(name, self.get_parameter_type(), new_val)
                        self.set_parameter_type(new_val)
        except MvKKeyError, e:
            ''' TODO: revert! '''
            cl.set_status_code(UpdateConstants.NOT_FOUND_CODE)
            cl.set_status_message(e.get_message())
        except MvKValueError, e:
            ''' TODO: revert! '''
            cl.set_status_code(UpdateConstants.NOT_FOUND_CODE)
            cl.set_status_message(e.get_message())
        except MvKPotencyError, e:
            ''' TODO: revert! '''
            cl.set_status_code(UpdateConstants.BAD_REQUEST_CODE)
            cl.set_status_message(e.get_message())
        cl.set_status_code(UpdateConstants.SUCCESS_CODE)
        cl.set_status_message(StringValue('Successfully updated parameter.'))
        return cl

    def read(self, location):
        from mvk.impl.python.python_representer import PythonRepresenter
        assert (isinstance(location, LocationValue) and
                isinstance(location.typed_by(), LocationType))

        rl = MvKReadLog()
        if location == LocationValue(''):
            ''' Base case. '''
            rl.set_item(self)
            rl.set_location(self.get_location())
            rl.set_status_code(ReadConstants.SUCCESS_CODE)
            rl.set_type(self.typed_by().get_location())
            rl.set_status_message(StringValue('Success!'))
            return rl
        else:
            return Node.read(self, location)


class Statement(Node, mvk.interfaces.action.Statement):
    ''' == CRUD == '''
    @classmethod
    def _add_to_parent(cls, inst, parent):
        assert isinstance(parent, mvk.interfaces.action.Body)
        parent.add_statement(inst)

    def _remove_from_parent(self):
        self.get_parent().remove_statement(self)


class ExpressionStatement(Statement, mvk.interfaces.action.ExpressionStatement):
    ''' == CONSTRUCTOR == '''
    def __init__(self, **kwargs):
        self.expression = None
        super(ExpressionStatement, self).__init__(**kwargs)

    ''' == PUBLIC INTERFACE == '''
    def get_expression(self):
        return self.expression

    def __eq__(self, other):
        return (super(ExpressionStatement, self).__eq__(other) and
                self.get_expression() == other.get_expression())

    ''' == PYTHON SPECIFIC == '''
    def set_expression(self, expr):
        assert expr is None or isinstance(expr, mvk.interfaces.action.Expression)
        self.expression = expr
        if self.expression is not None:
            self.expression.set_parent(self)

    ''' == CRUD == '''
    def read(self, location):
        from mvk.impl.python.python_representer import PythonRepresenter
        assert (isinstance(location, LocationValue) and
                isinstance(location.typed_by(), LocationType))

        rl = MvKReadLog()
        if location == LocationValue(''):
            ''' Base case. '''
            rl.set_item(self)
            rl.set_location(self.get_location())
            rl.set_status_code(ReadConstants.SUCCESS_CODE)
            rl.set_type(self.typed_by().get_location())
            rl.set_status_message(StringValue('Success!'))
            return rl
        else:
            idx = location.find(StringValue('.'))
            el_name = location if idx == IntegerValue(-1) else location.substring(stop=idx)
            if self.get_expression() is not None and el_name == self.get_expression().get_name():
                return self.get_expression().read(LocationValue('') if idx == IntegerValue(-1) else location.substring(start=idx + IntegerValue(1)))
            else:
                return Node.read(self, location)


class ReturnStatement(ExpressionStatement):
    pass


class DeclarationStatement(Statement, mvk.interfaces.action.DeclarationStatement):
    ''' == CONSTRUCTOR == '''
    def __init__(self, **kwargs):
        self.identifier = None
        self.initialization_expression = None
        super(DeclarationStatement, self).__init__(**kwargs)

    ''' == PUBLIC INTERFACE == '''
    def get_type(self):
        return self.identifier.get_type()

    def get_identifier(self):
        return self.identifier

    def get_initialization_expression(self):
        return self.initialization_expression

    def __eq__(self, other):
        return (super(DeclarationStatement, self).__eq__(other) and
                self.get_identifier() == other.get_identifier())

    ''' == PYTHON SPECIFIC '''
    def set_identifier(self, identifier):
        assert identifier is None or isinstance(identifier, mvk.interfaces.action.Identifier)
        self.identifier = identifier
        if self.identifier is not None:
            self.identifier.set_parent(self)

    def set_initialization_expression(self, expr):
        assert expr is None or isinstance(expr, mvk.interfaces.action.Expression)
        self.initialization_expression = expr
        if self.initialization_expression is not None:
            self.initialization_expression.set_parent(self)

    ''' == CRUD == '''
    def read(self, location):
        from mvk.impl.python.python_representer import PythonRepresenter
        assert (isinstance(location, LocationValue) and
                isinstance(location.typed_by(), LocationType))

        rl = MvKReadLog()
        if location == LocationValue(''):
            ''' Base case. '''
            rl.set_item(self)
            rl.set_location(self.get_location())
            rl.set_status_code(ReadConstants.SUCCESS_CODE)
            rl.set_type(self.typed_by().get_location())
            rl.set_status_message(StringValue('Success!'))
            return rl
        else:
            idx = location.find(StringValue('.'))
            el_name = location if idx == IntegerValue(-1) else location.substring(stop=idx)
            if self.get_identifier() is not None and el_name == self.get_identifier().get_name():
                return self.get_identifier().read(LocationValue('') if idx == IntegerValue(-1) else location.substring(start=idx + IntegerValue(1)))
            elif self.get_initialization_expression() is not None and el_name == self.get_initialization_expression().get_name():
                return self.get_initialization_expression().read(LocationValue('') if idx == IntegerValue(-1) else location.substring(start=idx + IntegerValue(1)))
            else:
                return Node.read(self, location)


class WhileLoop(Statement, mvk.interfaces.action.WhileLoop):
    ''' == CONSTRUCTOR == '''
    def __init__(self, **kwargs):
        self.test = None
        self.body = None
        super(WhileLoop, self).__init__(**kwargs)

    ''' == PUBLIC INTERFACE == '''
    def get_test(self):
        return self.test

    def get_body(self):
        return self.body

    def __eq__(self, other):
        return (super(WhileLoop, self).__eq__(other) and
                self.get_test() == other.get_test() and
                self.get_body() == other.get_body())

    ''' == PYTHON SPECIFIC == '''
    def set_test(self, test):
        assert test is None or isinstance(test, mvk.interfaces.action.Expression)
        self.test = test
        if self.test is not None:
            self.test.set_parent(self)

    def set_body(self, body):
        assert body is None or isinstance(body, mvk.interfaces.action.Body)
        self.body = body
        if self.body:
            self.body.set_parent(self)

    ''' == CRUD == '''
    def read(self, location):
        from mvk.impl.python.python_representer import PythonRepresenter
        assert (isinstance(location, LocationValue) and
                isinstance(location.typed_by(), LocationType))

        rl = MvKReadLog()
        if location == LocationValue(''):
            ''' Base case. '''
            rl.set_item(self)
            rl.set_location(self.get_location())
            rl.set_status_code(ReadConstants.SUCCESS_CODE)
            rl.set_type(self.typed_by().get_location())
            rl.set_status_message(StringValue('Success!'))
            return rl
        else:
            idx = location.find(StringValue('.'))
            el_name = location if idx == IntegerValue(-1) else location.substring(stop=idx)
            if self.get_test() is not None and el_name == self.get_test().get_name():
                return self.get_test().read(LocationValue('') if idx == IntegerValue(-1) else location.substring(start=idx + IntegerValue(1)))
            elif self.get_body() is not None and el_name == LocationValue('body'):
                return self.body.read(LocationValue('') if idx == IntegerValue(-1) else location.substring(start=idx + IntegerValue(1)))
            else:
                return Node.read(self, location)


class IfStatement(Statement, mvk.interfaces.action.IfStatement):
    ''' == CONSTRUCTOR == '''
    def __init__(self, **kwargs):
        self.test = None
        self.if_body = None
        self.else_body = None
        super(IfStatement, self).__init__(**kwargs)

    ''' == PUBLIC INTERFACE == '''
    def get_test(self):
        return self.test

    def get_if_body(self):
        return self.if_body

    def get_else_body(self):
        return self.else_body

    def __eq__(self, other):
        return (super(IfStatement, self).__eq__(other) and
                self.get_test() == other.get_test() and
                self.get_if_body() == other.get_if_body() and
                self.get_else_body() == other.get_else_body())

    ''' == PYTHON SPECIFIC == '''
    def set_test(self, test):
        assert test is None or isinstance(test, mvk.interfaces.action.Expression)
        self.test = test
        if self.test is not None:
            self.test.set_parent(self)

    def set_if_body(self, body):
        assert body is None or isinstance(body, mvk.interfaces.action.Body)
        self.if_body = body
        if self.if_body:
            self.if_body.set_parent(self)

    def set_else_body(self, body):
        assert body is None or isinstance(body, mvk.interfaces.action.Body)
        self.else_body = body
        if self.else_body:
            self.else_body.set_parent(self)

    ''' == CRUD == '''
    def read(self, location):
        from mvk.impl.python.python_representer import PythonRepresenter
        assert (isinstance(location, LocationValue) and
                isinstance(location.typed_by(), LocationType))

        rl = MvKReadLog()
        if location == LocationValue(''):
            ''' Base case. '''
            rl.set_item(self)
            rl.set_location(self.get_location())
            rl.set_status_code(ReadConstants.SUCCESS_CODE)
            rl.set_type(self.typed_by().get_location())
            rl.set_status_message(StringValue('Success!'))
            return rl
        else:
            idx = location.find(StringValue('.'))
            el_name = location if idx == IntegerValue(-1) else location.substring(stop=idx)
            if self.get_test() is not None and el_name == self.get_test().get_name():
                return self.get_test().read(LocationValue('') if idx == IntegerValue(-1) else location.substring(start=idx + IntegerValue(1)))
            elif self.get_if_body() is not None and el_name == LocationValue('ifbody'):
                return self.get_if_body().read(LocationValue('') if idx == IntegerValue(-1) else location.substring(start=idx + IntegerValue(1)))
            elif self.get_else_body() is not None and el_name == LocationValue('elsebody'):
                return self.get_else_body().read(LocationValue('') if idx == IntegerValue(-1) else location.substring(start=idx + IntegerValue(1)))
            else:
                return Node.read(self, location)


class BreakStatement(Statement, mvk.interfaces.action.BreakStatement):
    pass


class ContinueStatement(Statement, mvk.interfaces.action.ContinueStatement):
    pass


class Expression(Node, mvk.interfaces.action.Expression):
    ''' == CRUD == '''
    @classmethod
    def _add_to_parent(cls, inst, parent):
        assert (isinstance(parent, mvk.interfaces.action.ExpressionStatement) or
                isinstance(parent, mvk.interfaces.action.DeclarationStatement) or
                isinstance(parent, mvk.interfaces.action.WhileLoop) or
                isinstance(parent, mvk.interfaces.action.Assignment) or
                isinstance(parent, mvk.interfaces.action.IfStatement) or
                isinstance(parent, mvk.interfaces.action.Operator) or
                isinstance(parent, mvk.interfaces.action.Argument) or
                isinstance(parent, mvk.interfaces.action.FunctionCall))
        if isinstance(parent, mvk.interfaces.action.ExpressionStatement) or isinstance(parent, mvk.interfaces.action.Argument):
            parent.set_expression(inst)
        elif isinstance(parent, mvk.interfaces.action.FunctionCall):
            parent.set_called_expression(inst)
        elif isinstance(parent, mvk.interfaces.action.DeclarationStatement):
            parent.set_initialization_expression(inst)
        elif isinstance(parent, mvk.interfaces.action.WhileLoop) or isinstance(parent, mvk.interfaces.action.IfStatement):
            parent.set_test(inst)
        elif isinstance(parent, mvk.interfaces.action.Operator) or isinstance(parent, mvk.interfaces.action.Assignment):
            parent.add_child(inst)
        else:
            assert False

    def _remove_from_parent(self):
        parent = self.get_parent()
        if isinstance(parent, mvk.interfaces.action.ExpressionStatement) or isinstance(parent, mvk.interfaces.action.Argument):
            parent.set_expression(None)
        elif isinstance(parent, mvk.interfaces.action.FunctionCall):
            parent.set_called_expression(None)
        elif isinstance(parent, mvk.interfaces.action.DeclarationStatement):
            parent.set_initialization_expression(None)
        elif isinstance(parent, mvk.interfaces.action.WhileLoop) or isinstance(parent, mvk.interfaces.action.IfStatement):
            parent.set_test(None)
        elif isinstance(parent, mvk.interfaces.action.Operator) or isinstance(parent, mvk.interfaces.action.Assignment):
            parent.remove_child(self)
        else:
            assert False

    def read(self, location):
        from mvk.impl.python.python_representer import PythonRepresenter
        assert (isinstance(location, LocationValue) and
                isinstance(location.typed_by(), LocationType))

        rl = MvKReadLog()
        if location == LocationValue(''):
            ''' Base case. '''
            rl.set_item(self)
            rl.set_location(self.get_location())
            rl.set_status_code(ReadConstants.SUCCESS_CODE)
            rl.set_type(self.typed_by().get_location())
            rl.set_status_message(StringValue('Success!'))
            return rl
        else:
            return Node.read(self, location)


class Constant(Expression, TypedElement, mvk.interfaces.action.Constant):
    ''' == CONSTRUCTOR == '''
    def __init__(self, value, **kwargs):
        assert isinstance(value, mvk.interfaces.datavalue.DataValue)
        self.value = value
        super(Constant, self).__init__(the_type=value.typed_by(), **kwargs)

    ''' == PUBLIC INTERFACE == '''
    def get_value(self):
        return self.value

    ''' == CRUD == '''
    @classmethod
    def _check_params_create(cls, params):
        res = Expression._check_params_create(params)
        if res is not None:
            return res
        from mvk.impl.python.constants import CreateConstants
        attributes = params[CreateConstants.ATTRS_KEY]
        cls._check_param(attributes,
                         StringValue('value'),
                         mvk.interfaces.datavalue.DataValue,
                         mvk.interfaces.datatype.DataType)

    @classmethod
    def _create_inst(cls, params, cl):
        from mvk.impl.python.constants import CreateConstants
        attributes = params[CreateConstants.ATTRS_KEY]
        name = attributes[StringValue('name')]
        potency = attributes[StringValue('potency')] if StringValue('potency') in attributes else None
        clz = attributes[StringValue('class')]
        value = attributes[StringValue('value')]
        assert logger.debug('Creating %s with name %s, potency %s, type %s, value %s' %
                            (cls.__name__, name, potency, clz, value))
        n = cls(name=name, potency=potency,
                value=value, l_type=ClabjectReference(path=clz))
        cl.add_attr_change(StringValue('name'), n.get_name())
        cl.add_attr_change(StringValue('potency'), n.get_potency())
        cl.add_attr_change(StringValue('class'), n.typed_by().get_location())
        cl.add_attr_change(StringValue('type'), StringValue(str(n.get_type())))
        cl.add_attr_change(StringValue('value'), n.get_value())
        return n


class Identifier(Expression, TypedElement, NamedElement,
                 mvk.interfaces.action.Identifier):
    ''' == CRUD == '''
    @classmethod
    def _add_to_parent(cls, inst, parent):
        if isinstance(parent, mvk.interfaces.action.DeclarationStatement):
            parent.set_identifier(inst)
        else:
            Expression._add_to_parent(inst, parent)

    def _remove_from_parent(self):
        parent = self.get_parent()
        if isinstance(parent, mvk.interfaces.action.DeclarationStatement):
            parent.set_identifier(None)
        else:
            Expression._remove_from_parent(self)

    @classmethod
    def _check_params_create(cls, params):
        res = Expression._check_params_create(params)
        if res is not None:
            return res
        attributes = params[CreateConstants.ATTRS_KEY]
        cls._check_param(attributes,
                         StringValue('type'),
                         mvk.interfaces.datatype.Type)

    @classmethod
    def _create_inst(cls, params, cl):
        attributes = params[CreateConstants.ATTRS_KEY]
        name = attributes[StringValue('name')]
        potency = attributes[StringValue('potency')] if StringValue('potency') in attributes else None
        clz = attributes[StringValue('class')]
        the_type = attributes[StringValue('type')]
        assert logger.debug('Creating %s with name %s, potency %s, type %s, the_type %s' %
                            (cls.__name__, name, potency, clz, the_type))
        n = cls(name=name, potency=potency, the_type=the_type,
                l_type=ClabjectReference(path=clz))
        cl.add_attr_change(StringValue('name'), n.get_name())
        cl.add_attr_change(StringValue('potency'), n.get_potency())
        cl.add_attr_change(StringValue('class'), n.typed_by().get_location())
        cl.add_attr_change(StringValue('type'), StringValue(str(n.get_type())))
        return n

    @classmethod
    def _check_params_update(cls, params):
        cl = Node._check_params_update(params)
        if cl is not None:
            return cl
        cl = MvKUpdateLog()
        if not (isinstance(params, mvk.interfaces.datavalue.MappingValue) and
                isinstance(params.typed_by(), mvk.interfaces.datatype.MappingType)):
            cl.set_status_code(UpdateConstants.MALFORMED_REQUEST_CODE)
            cl.set_status_message(StringValue('Expected a MappingValue'))
            return cl
        try:
            cls._check_param(params,
                             CreateConstants.ATTRS_KEY,
                             mvk.interfaces.datavalue.MappingValue,
                             mvk.interfaces.datatype.MappingType)
            attributes = params[CreateConstants.ATTRS_KEY]
            cls._check_param(attributes,
                             StringValue('type'),
                             mvk.interfaces.datatype.Type,
                             req=False)
        except MvKException, e:
            cl.set_status_code(CreateConstants.BAD_REQUEST_CODE)
            cl.set_status_message(e.get_message())
            return cl
        return None

    def _update(self, params):
        cl = Node._update(self, params)
        if not cl.is_success():
            return cl
        attributes = params[UpdateConstants.ATTRS_KEY]
        it = attributes.__iter__()
        try:
            while it.has_next():
                name = it.next()
                if self.typed_by().get_location().startswith(StringValue('mvk')):
                    if name == StringValue('type'):
                        new_val = attributes[name]
                        cl.add_attr_change(name, self.get_value(), new_val)
                        self.set_value(new_val)
        except MvKKeyError, e:
            ''' TODO: revert! '''
            cl.set_status_code(UpdateConstants.NOT_FOUND_CODE)
            cl.set_status_message(e.get_message())
        except MvKValueError, e:
            ''' TODO: revert! '''
            cl.set_status_code(UpdateConstants.NOT_FOUND_CODE)
            cl.set_status_message(e.get_message())
        except MvKPotencyError, e:
            ''' TODO: revert! '''
            cl.set_status_code(UpdateConstants.BAD_REQUEST_CODE)
            cl.set_status_message(e.get_message())
        cl.set_status_code(UpdateConstants.SUCCESS_CODE)
        cl.set_status_message(StringValue('Successfully updated identifier.'))
        return cl


class Navigation(Expression, mvk.interfaces.action.Navigation):
    ''' == CONSTRUCTOR == '''
    def __init__(self, path, **kwargs):
        self.set_path(path)
        super(Navigation, self).__init__(**kwargs)

    ''' == PUBLIC INTERFACE == '''
    def get_path(self):
        return self.path

    def __eq__(self, other):
        return (super(Navigation, self).__eq__(other) and
                self.get_path() == other.get_path())

    ''' == PYTHON SPECIFIC == '''
    def set_path(self, path):
        assert isinstance(path, mvk.interfaces.datavalue.LocationValue)
        self.path = path

    ''' == CRUD == '''
    @classmethod
    def _check_params_create(cls, params):
        res = Node._check_params_create(params)
        if res is not None:
            return res
        from mvk.impl.python.constants import CreateConstants
        attributes = params[CreateConstants.ATTRS_KEY]
        cls._check_param(attributes,
                         StringValue('path'),
                         mvk.interfaces.datavalue.LocationValue,
                         mvk.interfaces.datatype.LocationType)

    @classmethod
    def _create_inst(cls, params, cl):
        from mvk.impl.python.constants import CreateConstants
        attributes = params[CreateConstants.ATTRS_KEY]
        name = attributes[StringValue('name')]
        potency = attributes[StringValue('potency')] if StringValue('potency') in attributes else None
        clz = attributes[StringValue('class')]
        path = attributes[StringValue('path')]
        assert logger.debug('Creating %s with name %s, potency %s, type %s, path %s' %
                            (cls.__name__, name, potency, clz, path))
        n = cls(name=name, potency=potency, path=path,
                l_type=ClabjectReference(path=clz))
        cl.add_attr_change(StringValue('name'), n.get_name())
        cl.add_attr_change(StringValue('potency'), n.get_potency())
        cl.add_attr_change(StringValue('class'), n.typed_by().get_location())
        cl.add_attr_change(StringValue('path'), n.get_path())
        return n

    @classmethod
    def _check_params_update(cls, params):
        cl = Node._check_params_update(params)
        if cl is not None:
            return cl
        cl = MvKUpdateLog()
        if not (isinstance(params, mvk.interfaces.datavalue.MappingValue) and
                isinstance(params.typed_by(), mvk.interfaces.datatype.MappingType)):
            cl.set_status_code(UpdateConstants.MALFORMED_REQUEST_CODE)
            cl.set_status_message(StringValue('Expected a MappingValue'))
            return cl
        try:
            cls._check_param(params,
                             CreateConstants.ATTRS_KEY,
                             mvk.interfaces.datavalue.MappingValue,
                             mvk.interfaces.datatype.MappingType)
            attributes = params[CreateConstants.ATTRS_KEY]
            cls._check_param(attributes,
                             StringValue('path'),
                             mvk.interfaces.datavalue.LocationValue,
                             mvk.interfaces.datatype.LocationType,
                             req=False)
        except MvKException, e:
            cl.set_status_code(CreateConstants.BAD_REQUEST_CODE)
            cl.set_status_message(e.get_message())
            return cl
        return None

    def _update(self, params):
        cl = Node._update(self, params)
        if not cl.is_success():
            return cl
        attributes = params[UpdateConstants.ATTRS_KEY]
        it = attributes.__iter__()
        try:
            while it.has_next():
                name = it.next()
                if self.typed_by().get_location().startswith(StringValue('mvk')):
                    if name == StringValue('path'):
                        new_val = attributes[name]
                        cl.add_attr_change(name, self.get_path(), new_val)
                        self.set_path(new_val)
        except MvKKeyError, e:
            ''' TODO: revert! '''
            cl.set_status_code(UpdateConstants.NOT_FOUND_CODE)
            cl.set_status_message(e.get_message())
        except MvKValueError, e:
            ''' TODO: revert! '''
            cl.set_status_code(UpdateConstants.NOT_FOUND_CODE)
            cl.set_status_message(e.get_message())
        except MvKPotencyError, e:
            ''' TODO: revert! '''
            cl.set_status_code(UpdateConstants.BAD_REQUEST_CODE)
            cl.set_status_message(e.get_message())
        cl.set_status_code(UpdateConstants.SUCCESS_CODE)
        cl.set_status_message(StringValue('Successfully updated navigation.'))
        return cl


class Assignment(Expression, mvk.interfaces.action.Assignment):
    ''' == CONSTRUCTOR == '''
    def __init__(self, **kwargs):
        self.children = SequenceValue()
        self.child_lookup = {}
        super(Assignment, self).__init__(**kwargs)

    ''' == PUBLIC INTERFACE == '''
    def get_children(self):
        return ImmutableSequenceValue(self.children)

    def __eq__(self, other):
        return (super(Assignment, self).__eq__(other) and
                self.get_children() == other.get_children())

    ''' == PYTHON SPECIFIC == '''
    def add_child(self, child):
        assert isinstance(child, mvk.interfaces.action.Expression)
        assert child.get_name() not in self.child_lookup
        self.children.append(child)
        self.child_lookup[child.get_name()] = child
        child.set_parent(self)

    def remove_child(self, child):
        assert isinstance(child, mvk.interfaces.action.Expression)
        assert child.get_name() in self.child_lookup
        self.children.remove(child)
        del self.child_lookup[child.get_name()]
        child.set_parent(None)

    ''' == CRUD == '''
    def read(self, location):
        from mvk.impl.python.python_representer import PythonRepresenter
        assert (isinstance(location, LocationValue) and
                isinstance(location.typed_by(), LocationType))

        rl = MvKReadLog()
        if location == LocationValue(''):
            ''' Base case. '''
            rl.set_item(self)
            rl.set_location(self.get_location())
            rl.set_status_code(ReadConstants.SUCCESS_CODE)
            rl.set_type(self.typed_by().get_location())
            rl.set_status_message(StringValue('Success!'))
            return rl
        else:
            idx = location.find(StringValue('.'))
            el_name = location if idx == IntegerValue(-1) else location.substring(stop=idx)
            if el_name in self.child_lookup:
                return self.child_lookup[el_name].read(LocationValue('') if idx == IntegerValue(-1) else location.substring(start=idx + IntegerValue(1)))
            else:
                return Node.read(self, location)


class FunctionCall(Expression, mvk.interfaces.action.FunctionCall):
    ''' == CONSTRUCTOR == '''
    def __init__(self, function, **kwargs):
        self.set_function(function)
        self.arguments = SequenceValue()
        self.argument_lookup = {}
        self.called_expression = None
        super(FunctionCall, self).__init__(**kwargs)

    ''' == PUBLIC INTERFACE == '''
    def get_called_expression(self):
        return self.called_expression

    def get_function(self):
        return self.function

    def get_arguments(self):
        return ImmutableSequenceValue(self.arguments)

    def __eq__(self, other):
        return (super(FunctionCall, self).__eq__(other) and
                self.get_called_expression() == other.get_called_expression() and
                self.get_function() == other.get_function() and
                self.get_arguments() == other.get_arguments())

    ''' == PUBLIC INTERFACE == '''
    def set_called_expression(self, called_expr):
        assert called_expr is None or isinstance(called_expr, mvk.interfaces.action.Expression)
        self.called_expression = called_expr
        if called_expr is not None:
            called_expr.set_parent(self)

    def set_function(self, function):
        assert (isinstance(function, mvk.interfaces.datavalue.StringValue) and
                isinstance(function.typed_by(), mvk.interfaces.datatype.StringType))
        self.function = function

    def add_argument(self, argument, idx=None):
        if idx is None:
            idx = self.arguments.len()
        assert isinstance(argument, mvk.interfaces.action.Argument)
        assert (isinstance(idx, mvk.interfaces.datavalue.IntegerValue) and
                isinstance(idx.typed_by(), mvk.interfaces.datatype.IntegerType))
        assert not (argument.get_name() in self.argument_lookup or (self.called_expression is not None and argument.get_name() == self.called_expression.get_name()))
        self.arguments.insert(idx, argument)
        self.argument_lookup[argument.get_name()] = argument
        argument.set_parent(self)

    def remove_argument(self, argument):
        assert isinstance(argument, mvk.interfaces.action.Argument)
        assert argument.get_name() in self.argument_lookup
        argument.set_parent(None)
        self.arguments.remove(argument)
        del self.argument_lookup[argument.get_name()]

    ''' == CRUD == '''
    @classmethod
    def _check_params_create(cls, params):
        res = Node._check_params_create(params)
        if res is not None:
            return res
        from mvk.impl.python.constants import CreateConstants
        attributes = params[CreateConstants.ATTRS_KEY]
        cls._check_param(attributes,
                         StringValue('function'),
                         mvk.interfaces.datavalue.StringValue,
                         mvk.interfaces.datatype.StringType)

    @classmethod
    def _create_inst(cls, params, cl):
        from mvk.impl.python.constants import CreateConstants
        attributes = params[CreateConstants.ATTRS_KEY]
        name = attributes[StringValue('name')]
        potency = attributes[StringValue('potency')] if StringValue('potency') in attributes else None
        clz = attributes[StringValue('class')]
        function = attributes[StringValue('function')]
        assert logger.debug('Creating %s with name %s, potency %s, type %s, function %s' %
                            (cls.__name__, name, potency, clz, function))
        n = cls(name=name, potency=potency, function=function,
                l_type=ClabjectReference(path=clz))
        cl.add_attr_change(StringValue('name'), n.get_name())
        cl.add_attr_change(StringValue('potency'), n.get_potency())
        cl.add_attr_change(StringValue('class'), n.typed_by().get_location())
        cl.add_attr_change(StringValue('function'), n.get_function())
        return n

    @classmethod
    def _check_params_update(cls, params):
        cl = Node._check_params_update(params)
        if cl is not None:
            return cl
        cl = MvKUpdateLog()
        if not (isinstance(params, mvk.interfaces.datavalue.MappingValue) and
                isinstance(params.typed_by(), mvk.interfaces.datatype.MappingType)):
            cl.set_status_code(UpdateConstants.MALFORMED_REQUEST_CODE)
            cl.set_status_message(StringValue('Expected a MappingValue'))
            return cl
        try:
            cls._check_param(params,
                             CreateConstants.ATTRS_KEY,
                             mvk.interfaces.datavalue.MappingValue,
                             mvk.interfaces.datatype.MappingType)
            attributes = params[CreateConstants.ATTRS_KEY]
            cls._check_param(attributes,
                             StringValue('function'),
                             mvk.interfaces.datavalue.StringValue,
                             mvk.interfaces.datatype.StringType,
                             req=False)
        except MvKException, e:
            cl.set_status_code(CreateConstants.BAD_REQUEST_CODE)
            cl.set_status_message(e.get_message())
            return cl
        return None

    def _update(self, params):
        cl = Node._update(self, params)
        if not cl.is_success():
            return cl
        attributes = params[UpdateConstants.ATTRS_KEY]
        it = attributes.__iter__()
        try:
            while it.has_next():
                name = it.next()
                if self.typed_by().get_location().startswith(StringValue('mvk')):
                    if name == StringValue('function'):
                        new_val = attributes[name]
                        cl.add_attr_change(name, self.get_function(), new_val)
                        self.set_function(new_val)
        except MvKKeyError, e:
            ''' TODO: revert! '''
            cl.set_status_code(UpdateConstants.NOT_FOUND_CODE)
            cl.set_status_message(e.get_message())
        except MvKValueError, e:
            ''' TODO: revert! '''
            cl.set_status_code(UpdateConstants.NOT_FOUND_CODE)
            cl.set_status_message(e.get_message())
        except MvKPotencyError, e:
            ''' TODO: revert! '''
            cl.set_status_code(UpdateConstants.BAD_REQUEST_CODE)
            cl.set_status_message(e.get_message())
        cl.set_status_code(UpdateConstants.SUCCESS_CODE)
        cl.set_status_message(StringValue('Successfully updated function call.'))
        return cl

    def read(self, location):
        from mvk.impl.python.python_representer import PythonRepresenter
        assert (isinstance(location, LocationValue) and
                isinstance(location.typed_by(), LocationType))

        rl = MvKReadLog()
        if location == LocationValue(''):
            ''' Base case. '''
            rl.set_item(self)
            rl.set_location(self.get_location())
            rl.set_status_code(ReadConstants.SUCCESS_CODE)
            rl.set_type(self.typed_by().get_location())
            rl.set_status_message(StringValue('Success!'))
            return rl
        else:
            idx = location.find(StringValue('.'))
            el_name = location if idx == IntegerValue(-1) else location.substring(stop=idx)
            if self.get_called_expression() is not None and el_name == self.get_called_expression().get_name():
                return self.get_called_expression().read(LocationValue('') if idx == IntegerValue(-1) else location.substring(start=idx + IntegerValue(1)))
            elif el_name in self.argument_lookup:
                return self.argument_lookup[el_name].read(LocationValue('') if idx == IntegerValue(-1) else location.substring(start=idx + IntegerValue(1)))
            else:
                return Node.read(self, location)


class Argument(Node, mvk.interfaces.action.Argument):
    ''' == CONSTRUCTOR == '''
    def __init__(self, key=None, **kwds):
        if key is None:
            key = StringValue('')
        self.set_key(key)
        self.expression = None
        super(Argument, self).__init__(**kwds)

    ''' == PUBLIC INTERFACE == '''
    def get_key(self):
        return self.key

    def get_expression(self):
        return self.expression

    ''' == PYTHON SPECIFIC == '''
    def set_key(self, key):
        assert (isinstance(key, mvk.interfaces.datavalue.StringValue) and
                isinstance(key.typed_by(), mvk.interfaces.datatype.StringType))
        self.key = key

    def set_expression(self, expression):
        assert expression is None or isinstance(expression, mvk.interfaces.action.Expression)
        self.expression = expression
        if expression is not None:
            expression.set_parent(self)

    ''' == CRUD == '''
    @classmethod
    def _add_to_parent(cls, inst, parent):
        assert isinstance(parent, FunctionCall)
        parent.add_argument(inst)

    def _remove_from_parent(self):
        parent = self.get_parent()
        parent.remove_argument(self)

    @classmethod
    def _check_params_create(cls, params):
        res = Node._check_params_create(params)
        if res is not None:
            return res
        from mvk.impl.python.constants import CreateConstants
        attributes = params[CreateConstants.ATTRS_KEY]
        cls._check_param(attributes,
                         StringValue('key'),
                         mvk.interfaces.datavalue.StringValue,
                         mvk.interfaces.datatype.StringType,
                         req=False)

    @classmethod
    def _create_inst(cls, params, cl):
        from mvk.impl.python.constants import CreateConstants
        attributes = params[CreateConstants.ATTRS_KEY]
        name = attributes[StringValue('name')]
        potency = attributes[StringValue('potency')] if StringValue('potency') in attributes else None
        clz = attributes[StringValue('class')]
        key = attributes[StringValue('key')] if StringValue('potency') in attributes else None
        assert logger.debug('Creating %s with name %s, potency %s, type %s, key %s' %
                            (cls.__name__, name, potency, clz, key))
        n = cls(name=name, potency=potency, key=key,
                l_type=ClabjectReference(path=clz))
        cl.add_attr_change(StringValue('name'), n.get_name())
        cl.add_attr_change(StringValue('potency'), n.get_potency())
        cl.add_attr_change(StringValue('class'), n.typed_by().get_location())
        cl.add_attr_change(StringValue('key'), n.get_key())
        return n

    @classmethod
    def _check_params_update(cls, params):
        cl = Node._check_params_update(params)
        if cl is not None:
            return cl
        cl = MvKUpdateLog()
        if not (isinstance(params, mvk.interfaces.datavalue.MappingValue) and
                isinstance(params.typed_by(), mvk.interfaces.datatype.MappingType)):
            cl.set_status_code(UpdateConstants.MALFORMED_REQUEST_CODE)
            cl.set_status_message(StringValue('Expected a MappingValue'))
            return cl
        try:
            cls._check_param(params,
                             CreateConstants.ATTRS_KEY,
                             mvk.interfaces.datavalue.MappingValue,
                             mvk.interfaces.datatype.MappingType)
            attributes = params[CreateConstants.ATTRS_KEY]
            cls._check_param(attributes,
                             StringValue('key'),
                             mvk.interfaces.datavalue.StringValue,
                             mvk.interfaces.datatype.StringType,
                             req=False)
        except MvKException, e:
            cl.set_status_code(CreateConstants.BAD_REQUEST_CODE)
            cl.set_status_message(e.get_message())
            return cl
        return None

    def _update(self, params):
        cl = Node._update(self, params)
        if not cl.is_success():
            return cl
        attributes = params[UpdateConstants.ATTRS_KEY]
        it = attributes.__iter__()
        try:
            while it.has_next():
                name = it.next()
                if self.typed_by().get_location().startswith(StringValue('mvk')):
                    if name == StringValue('key'):
                        new_val = attributes[name]
                        cl.add_attr_change(name, self.get_key(), new_val)
                        self.set_key(new_val)
        except MvKKeyError, e:
            ''' TODO: revert! '''
            cl.set_status_code(UpdateConstants.NOT_FOUND_CODE)
            cl.set_status_message(e.get_message())
        except MvKValueError, e:
            ''' TODO: revert! '''
            cl.set_status_code(UpdateConstants.NOT_FOUND_CODE)
            cl.set_status_message(e.get_message())
        except MvKPotencyError, e:
            ''' TODO: revert! '''
            cl.set_status_code(UpdateConstants.BAD_REQUEST_CODE)
            cl.set_status_message(e.get_message())
        cl.set_status_code(UpdateConstants.SUCCESS_CODE)
        cl.set_status_message(StringValue('Successfully updated function call.'))
        return cl

    def read(self, location):
        from mvk.impl.python.python_representer import PythonRepresenter
        assert (isinstance(location, LocationValue) and
                isinstance(location.typed_by(), LocationType))

        rl = MvKReadLog()
        if location == LocationValue(''):
            ''' Base case. '''
            rl.set_item(self)
            rl.set_location(self.get_location())
            rl.set_status_code(ReadConstants.SUCCESS_CODE)
            rl.set_type(self.typed_by().get_location())
            rl.set_status_message(StringValue('Success!'))
            return rl
        else:
            idx = location.find(StringValue('.'))
            el_name = location if idx == IntegerValue(-1) else location.substring(stop=idx)
            if self.get_expression() is not None and el_name == self.get_expression().get_name():
                return self.get_expression().read(LocationValue('') if idx == IntegerValue(-1) else location.substring(start=idx + IntegerValue(1)))
            else:
                return Node.read(self, location)


class Operator(Expression, mvk.interfaces.action.Operator):
    ''' == CONSTRUCTOR == '''
    def __init__(self, **kwargs):
        self.children = SequenceValue()
        self.child_lookup = {}
        super(Operator, self).__init__(**kwargs)

    ''' == PUBLIC INTERFACE == '''
    def get_children(self):
        return self.children

    def __eq__(self, other):
        return (super(Operator, self).__eq__(other) and
                self.get_children() == other.get_children())

    ''' == PYTHON SPECIFIC == '''
    def add_child(self, child, idx=None):
        if idx is None:
            idx = self.children.len()
        assert isinstance(child, mvk.interfaces.action.Expression)
        assert (isinstance(idx, mvk.interfaces.datavalue.IntegerValue) and
                isinstance(idx.typed_by(), mvk.interfaces.datatype.IntegerType))
        assert not child.get_name() in self.child_lookup
        self.children.insert(idx, child)
        self.child_lookup[child.get_name()] = child
        child.set_parent(self)

    def remove_child(self, child):
        self.children.remove(child)
        del self.child_lookup[child.get_name()]

    ''' == CRUD == '''
    def read(self, location):
        from mvk.impl.python.python_representer import PythonRepresenter
        assert (isinstance(location, LocationValue) and
                isinstance(location.typed_by(), LocationType))

        rl = MvKReadLog()
        if location == LocationValue(''):
            ''' Base case. '''
            rl.set_item(self)
            rl.set_location(self.get_location())
            rl.set_status_code(ReadConstants.SUCCESS_CODE)
            rl.set_type(self.typed_by().get_location())
            rl.set_status_message(StringValue('Success!'))
            return rl
        else:
            idx = location.find(StringValue('.'))
            el_name = location if idx == IntegerValue(-1) else location.substring(stop=idx)
            if el_name in self.child_lookup:
                return self.child_lookup[el_name].read(LocationValue('') if idx == IntegerValue(-1) else location.substring(start=idx + IntegerValue(1)))
            else:
                return Node.read(self, location)


class UnaryOperator(Operator, mvk.interfaces.action.UnaryOperator):
    ''' == CONSTRUCTOR == '''
    def __init__(self, **kwargs):
        super(UnaryOperator, self).__init__(**kwargs)


class Not(UnaryOperator, mvk.interfaces.action.Not):
    pass


class BinaryOperator(Operator, mvk.interfaces.action.BinaryOperator):
    ''' == CONSTRUCTOR == '''
    def __init__(self, **kwargs):
        super(BinaryOperator, self).__init__(**kwargs)


class Or(BinaryOperator, mvk.interfaces.action.Or):
    pass


class And(BinaryOperator, mvk.interfaces.action.And):
    pass


class ComparisonOperator(BinaryOperator, mvk.interfaces.action.ComparisonOperator):
    pass


class Equal(ComparisonOperator, mvk.interfaces.action.Equal):
    pass


class LessThan(ComparisonOperator, mvk.interfaces.action.LessThan):
    pass


class GreaterThan(ComparisonOperator, mvk.interfaces.action.GreaterThan):
    pass


class In(ComparisonOperator, mvk.interfaces.action.In):
    pass


class ArithmeticOperator(BinaryOperator, mvk.interfaces.action.ArithmeticOperator):
    pass


class Plus(ArithmeticOperator, mvk.interfaces.action.Plus):
    pass


class Minus(ArithmeticOperator, mvk.interfaces.action.Minus):
    pass


class Multiplication(ArithmeticOperator, mvk.interfaces.action.Multiplication):
    pass


class Division(ArithmeticOperator, mvk.interfaces.action.Division):
    pass


class Modulo(ArithmeticOperator, mvk.interfaces.action.Modulo):
    pass
