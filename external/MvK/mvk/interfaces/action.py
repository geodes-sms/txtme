'''
Created on 24-apr.-2014

@author: Simon
'''
import mvk.interfaces.object


class Function(mvk.interfaces.element.TypedElement, mvk.interfaces.object.Node):
    """
    A function is the encapsulating unit for a sequence of statements.
    It has a name, which means it can be created in the modelverse, and
    can be executed. It has a name, a type (its return type), and a number
    of L{Parameter<mvk.interfaces.action.Parameter>}.
    """

    def get_body(self):
        """
        Returns the body of this function.
        @rtype: L{Body<mvk.interfaces.action.Body>}
        @return: The statements of this function.
        """
        pass

    def get_parameters(self):
        """
        Returns the parameters of this function.
        @rtype: L{SequenceValue<mvk.interfaces.datavalue.SequenceValue>}
        @return: The parameters of this function.
        """
        pass


class Body(mvk.interfaces.datavalue.SequenceValue, mvk.interfaces.object.Node):
    def get_statement(self, name):
        """
        Returns a statement with given name from the body.
        @rtype: L{SequenceValue<mvk.interfaces.datavalue.SequenceValue>}
        @return: The statements of this function.
        @raise L{MvKKeyError<mvk.interfaces.exception.MvKKeyError>}: if the given name was not found.
        """
        pass


class Parameter(mvk.interfaces.element.TypedElement, mvk.interfaces.object.Node):
    '''
    A L{Function<mvk.interfaces.action.Function>} has parameters.
    A parameter can either be input, output, or both. This is denoted
    by the parameter type, which is a string. A parameter also has a name,
    and a declared type.
    '''

    def get_parameter_type(self):
        """
        Returns the type of parameter. Possible values are 'in', 'out', and 'inout'.
        @rtype: L{StringValue<mvk.interfaces.datavalue.StringValue>}
        @return: The type of parameter: 'in', 'out', or 'inout'.
        """
        pass


class Statement(mvk.interfaces.object.Node):
    '''
    Abstract superclass for any statement in the modelverse.
    '''

    pass


class ExpressionStatement(Statement):
    '''
    An expression statement is used when an expression (such as an assignment)
    has to be executed.
    '''

    def get_expression(self):
        '''
        Returns the expression of this statement.
        @rtype: L{Expression<mvk.interfaces.action.Expression>}
        @return: The expression of this statement.
        '''
        pass


class ReturnStatement(ExpressionStatement):
    pass


class DeclarationStatement(Statement):
    '''
    Declaration statements introduce a new name (identifier) in a scope.
    '''

    def get_type(self):
        '''
        Returns the type of the declaration.
        @rtype: L{Type<mvk.interfaces.datatype.Type>}
        @return: The type of this declaration.
        '''
        pass

    def get_identifier(self):
        '''
        Returns the declared identifier.
        @rtype: L{Identifier<mvk.interfaces.action.Identifier>}
        @return: The type of this declaration.
        '''
        pass

    def get_initialization_expression(self):
        '''
        Returns the initialization expression of this declaration.
        @rtype: L{Expression<mvk.interfaces.action.Expression>}
        @return: The initialization expression of this declaration.
        '''
        pass


class WhileLoop(Statement):
    '''
    A while loop executes a sequence of statements until its test no longer is True.
    '''

    def get_test(self):
        '''
        Returns the test of the while loop.
        @rtype: L{Expression<mvk.interfaces.action.Expression>}
        @return: The test of the while loop.
        '''
        pass

    def get_body(self):
        '''
        Returns the body of the while loop, which is a sequence of statements.
        @rtype: L{Body<mvk.interfaces.action.Body>}
        @return: The body of the while loop.
        '''
        pass


class IfStatement(Statement):
    '''
    An if statement has a test, a sequence of statements that are exectued if
    the test if True, and a sequence of statements that are executed if the
    test is False.
    '''

    def get_test(self):
        '''
        Returns the test of the if statement.
        @rtype: L{Expression<mvk.interfaces.action.Expression>}
        @return: The test of the if statement.
        '''
        pass

    def get_if_body(self):
        '''
        Returns the body executed if the test is True, which is a sequence of statements.
        @rtype: L{Body<mvk.interfaces.datavalue.SequenceValue>}
        @return: The body executed if the test is True.
        '''
        pass

    def get_else_body(self):
        '''
        Returns the body executed if the test is False, which is a sequence of statements.
        @rtype: L{Body<mvk.interfaces.action.Body>}
        @return: The body executed if the test is False.
        '''
        pass


class BreakStatement(Statement):
    '''
    A break statement breaks out of the currently executing loop.
    '''

    pass


class ContinueStatement(Statement):
    '''
    A continue statement executes the next loop iteration.
    '''

    pass


class Expression(mvk.interfaces.object.Node):
    '''
    Abstract superclass for all expressions.
    The type of the expression is calculated by subclasses.
    '''
    pass


class Constant(Expression, mvk.interfaces.element.TypedElement):
    def get_value(self):
        '''
        Returns the value of this constant.
        @rtype: L{DataValue<mvk.interfaces.datavalue.DataValue>}
        @return: The value of this constant.
        '''
        pass


class Identifier(Expression, mvk.interfaces.element.TypedElement):
    '''
    An identifier used in a scope. It has a type and a name.
    '''
    pass


class Navigation(Expression):
    '''
    A navigation expression is used to reference anything: it could be
    a variable in local scope, or anything in the modelverse. It is up
    to the execution engine to resolve the navigation expression to the
    correct instance referenced.
    '''

    def get_path(self):
        """
        Returns the path of this navigation expression.
        @rtype: L{LocationValue<mvk.interfaces.datavalue.LocationValue>}
        @return: The path of this navigation expression.
        """
        pass


class Assignment(Expression):
    '''
    Assigns a value to an identifier.
    '''

    def get_children(self):
        """
        Returns the arguments on which the assignment is applied.
        @rtype: L{SequenceValue<mvk.interfaces.datavalue.SequenceValue>}
        @return: The arguments on which the assignment is applied.
        """
        pass


class FunctionCall(Expression):
    '''
    Represents a function call: a function (idenfitied by its name)
    is called on an expression (usually a navigation expression, or
    an identifier), and a number of actual parameters are passed.
    '''
    def get_called_expression(self):
        """
        Returns the expression of which a function was called.
        @rtype: L{Expression<mvk.interfaces.action.Expression>}
        @return: The expression of which a function was called.
        """
        pass

    def get_function(self):
        """
        Returns the name of the called function.
        @rtype: L{StringValue<mvk.interfaces.datavalue.StringValue>}
        @return: The name of the called function.
        """
        pass

    def get_arguments(self):
        """
        Returns the arguments passed to this function. It is a sequence
        of mappings of the form <param-name>: <param-value>
        @rtype: L{SequenceValue<mvk.interfaces.datavalue.SequenceValue>}
        @return: The arguments passed to this function.
        """
        pass


class Argument(mvk.interfaces.object.Node):
    '''
    An argument is passed to a function call. It has a key (the name of the parameter)
    and a value (an L{Expression<mvk.interfaces.action.Expression})
    '''

    def get_key(self):
        """
        Returns the key of this argument, which is the name of the L{Parameter<mvk.interfaces.action.Parameter>}
        it links to.
        @rtype: L{StringValue<mvk.interfaces.datavalue.StringValue>}
        @return: The key of this argument.
        """
        pass

    def get_expression(self):
        """
        Returns the expression, which is the value of this argument.
        @rtype: L{Expression<mvk.interfaces.action.Expression>}
        @return: The expression, which is the value of this argument.
        """
        pass


class Operator(Expression):
    '''
    Abstract superclass for all operators.
    '''

    def get_children(self):
        """
        Returns the arguments on which the operator is applied: depending on
        which kind of operator (unary, binary, or ternary), this function
        returns a sequence of different length.
        @rtype: L{SequenceValue<mvk.interfaces.datavalue.SequenceValue>}
        @return: The arguments on which the operator is applied.
        """
        pass


class UnaryOperator(Operator):
    pass


class Not(UnaryOperator):
    pass


class BinaryOperator(Operator):
    pass


class Or(BinaryOperator):
    pass


class And(BinaryOperator):
    pass


class ComparisonOperator(BinaryOperator):
    pass


class Equal(ComparisonOperator):
    pass


class LessThan(ComparisonOperator):
    pass


class GreaterThan(ComparisonOperator):
    pass


class In(ComparisonOperator):
    pass


class ArithmeticOperator(BinaryOperator):
    pass


class Plus(ArithmeticOperator):
    pass


class Minus(ArithmeticOperator):
    pass


class Multiplication(ArithmeticOperator):
    pass


class Division(ArithmeticOperator):
    pass


class Modulo(ArithmeticOperator):
    pass

''' TODO: Add primitive operations for CRUD calls. (?) -> They can also be function calls... '''
