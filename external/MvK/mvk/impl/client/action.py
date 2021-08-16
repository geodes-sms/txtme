class BaseAction(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        
class Function(BaseAction):
    pass

class Statement(BaseAction):
    pass

class ExpressionStatement(Statement):
    pass

class Body(BaseAction):
    pass

class Parameter(BaseAction):
    pass

class ReturnStatement(ExpressionStatement):
    pass

class DeclarationStatement(Statement):
    pass

class WhileLoop(Statement):
    pass

class IfStatement(Statement):
    pass

class BreakStatement(Statement):
    pass

class ContinueStatement(Statement):
    pass

class Expression(BaseAction):
    pass

class Constant(Expression):
    pass

class Identifier(Expression):
    pass

class Navigation(Expression):
    pass

class Assignment(Expression):
    pass

class FunctionCall(Expression):
    pass

class Argument(BaseAction):
    pass

class Operator(Expression):
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
