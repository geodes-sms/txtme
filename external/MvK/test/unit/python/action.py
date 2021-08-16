'''
Created on 28-apr.-2014

@author: Simon
'''
import unittest

from mvk.impl.python.action import Function, DeclarationStatement, Parameter, Identifier, WhileLoop, GreaterThan, Navigation, Assignment, ExpressionStatement, \
    Plus, Constant, Minus, IfStatement, ReturnStatement, FunctionCall, Argument, Body
from mvk.impl.python.constants import CreateConstants
from mvk.impl.python.datatype import StringType, IntegerType, FloatType
from mvk.impl.python.datavalue import MappingValue, LocationValue, StringValue, IntegerValue
from mvk.impl.python.object import Package, Model, ModelReference, ClabjectReference
from mvk.mvk import MvK


class ActionTestCase(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName=methodName)
        self.mvk = MvK()

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.mvk.clear()

    def test_CRUD(self):
        '''
        package test
            model test_model:
                string f(a: int, b: float) {
                    int i = 5
                    while i > 0:
                        b = b + mvk.g(c=5)
                        i = i - 1
                    if b > 100:
                        return b
                    else:
                        return -b
                }
        '''

        '''
        Oracle.
        '''
        test = Package(name=StringValue("test"))
        test_model = Model(name=StringValue("test_model"), l_type=ModelReference(LocationValue('mvk.object')), potency=IntegerValue(1))
        test.add_element(test_model)
        f = Function(name=StringValue('f'), l_type=ClabjectReference(LocationValue('mvk.action.Function')), the_type=StringType())
        test_model.add_function(f)
        f.set_body(Body(name=StringValue('body'), l_type=ClabjectReference(LocationValue('mvk.action.Body'), potency=None)))
        f_a = Parameter(name=StringValue('a'), l_type=ClabjectReference(LocationValue('mvk.action.Parameter')), the_type=IntegerType(), param_type=StringValue('in'))
        f.add_parameter(f_a)
        f_b = Parameter(name=StringValue('b'), l_type=ClabjectReference(LocationValue('mvk.action.Parameter')), the_type=FloatType(), param_type=StringValue('in'))
        f.add_parameter(f_b)
        f_decl_i = DeclarationStatement(name=StringValue('decl_i'), l_type=ClabjectReference(LocationValue('mvk.action.DeclarationStatement')))
        f_decl_i.set_identifier(Identifier(name=StringValue('i'), l_type=ClabjectReference(LocationValue('mvk.action.Identifier')), the_type=IntegerType()))
        f_decl_i.set_initialization_expression(Constant(name=StringValue('five'), l_type=ClabjectReference(LocationValue('mvk.action.Constant')), value=IntegerValue(5)))
        f_while = WhileLoop(name=StringValue('while_1'), l_type=ClabjectReference(LocationValue('mvk.action.WhileLoop')))
        f_while.set_body(Body(name=StringValue('body'), l_type=ClabjectReference(LocationValue('mvk.action.Body'), potency=None)))
        f_while_test = GreaterThan(name=StringValue('while_1_expr'), l_type=ClabjectReference(LocationValue('mvk.action.GreaterThan')))
        f_while_test.add_child(Navigation(name=StringValue('i'), l_type=ClabjectReference(LocationValue('mvk.action.Navigation')), path=LocationValue('i')))
        f_while_test.add_child(Constant(name=StringValue('zero'), l_type=ClabjectReference(LocationValue('mvk.action.Constant')), value=IntegerValue(0)))
        f_while.set_test(f_while_test)
        f_while_e_s_1 = ExpressionStatement(name=StringValue('e_s_1'), l_type=ClabjectReference(LocationValue('mvk.action.ExpressionStatement')))
        f_while.get_body().add_statement(f_while_e_s_1)
        f_while_a_e_1 = Assignment(name=StringValue('a_e_1'), l_type=ClabjectReference(LocationValue('mvk.action.Assignment')))
        f_while_e_s_1.set_expression(f_while_a_e_1)
        f_while_a_e_1.add_child(Identifier(name=StringValue('b'), l_type=ClabjectReference(LocationValue('mvk.action.Identifier')), the_type=FloatType()))
        f_while_a_e_1_plus = Plus(name=StringValue('b_plus_g'), l_type=ClabjectReference(LocationValue('mvk.action.Plus')))
        f_while_a_e_1_plus.add_child(Navigation(name=StringValue('b'), l_type=ClabjectReference(LocationValue('mvk.action.Navigation')), path=LocationValue('b')))
        f_while_a_e_1_plus_g = FunctionCall(name=StringValue('g'), l_type=ClabjectReference(LocationValue('mvk.action.FunctionCall')), function=StringValue('g'))
        f_while_a_e_1_plus.add_child(f_while_a_e_1_plus_g)
        f_while_a_e_1_plus_g.set_called_expression(Navigation(name=StringValue('mvk'), l_type=ClabjectReference(LocationValue('mvk.action.Navigation')), path=LocationValue('mvk')))
        f_while_a_e_1_plus_g_a = Argument(name=StringValue('c'), l_type=ClabjectReference(LocationValue('mvk.action.Argument')), key=StringValue('c'))
        f_while_a_e_1_plus_g.add_argument(f_while_a_e_1_plus_g_a)
        f_while_a_e_1_plus_g_a.set_expression(Constant(name=StringValue('five'), l_type=ClabjectReference(LocationValue('mvk.action.Constant')), value=IntegerValue(5)))
        f_while_a_e_1.add_child(f_while_a_e_1_plus)
        f_while_e_s_2 = ExpressionStatement(name=StringValue('e_s_2'), l_type=ClabjectReference(LocationValue('mvk.action.ExpressionStatement')))
        f_while.get_body().add_statement(f_while_e_s_2)
        f_while_a_e_2 = Assignment(name=StringValue('a_e_2'), l_type=ClabjectReference(LocationValue('mvk.action.Assignment')))
        f_while_e_s_2.set_expression(f_while_a_e_2)
        f_while_a_e_2.add_child(Identifier(name=StringValue('i'), l_type=ClabjectReference(LocationValue('mvk.action.Identifier')), the_type=IntegerType()))
        f_while_a_e_2_min = Minus(name=StringValue('i_min_1'), l_type=ClabjectReference(LocationValue('mvk.action.Minus')))
        f_while_a_e_2_min.add_child(Navigation(name=StringValue('i'), l_type=ClabjectReference(LocationValue('mvk.action.Navigation')), path=LocationValue('i')))
        f_while_a_e_2_min.add_child(Constant(name=StringValue('one'), l_type=ClabjectReference(LocationValue('mvk.action.Constant')), value=IntegerValue(1)))
        f_while_a_e_2.add_child(f_while_a_e_2_min)

        f_if = IfStatement(name=StringValue('ifstmt_1'), l_type=ClabjectReference(LocationValue('mvk.action.IfStatement')))
        f_if.set_if_body(Body(name=StringValue('ifbody'), l_type=ClabjectReference(LocationValue('mvk.action.Body'), potency=None)))
        f_if.set_else_body(Body(name=StringValue('elsebody'), l_type=ClabjectReference(LocationValue('mvk.action.Body'), potency=None)))
        f_if_test = GreaterThan(name=StringValue('ifstmt_1_expr'), l_type=ClabjectReference(LocationValue('mvk.action.GreaterThan')))
        f_if.set_test(f_if_test)
        f_if_test.add_child(Navigation(name=StringValue('b'), l_type=ClabjectReference(LocationValue('mvk.action.Navigation')), path=LocationValue('b')))
        f_if_test.add_child(Constant(name=StringValue('onehundred'), l_type=ClabjectReference(LocationValue('mvk.action.Constant')), value=IntegerValue(100)))
        f_if_r_s_if = ReturnStatement(name=StringValue('r_s_1'), l_type=ClabjectReference(LocationValue('mvk.action.ReturnStatement')))
        f_if_r_s_if.set_expression(Navigation(name=StringValue('b'), l_type=ClabjectReference(LocationValue('mvk.action.Navigation')), path=LocationValue('b')))
        f_if.get_if_body().add_statement(f_if_r_s_if)
        f_if_r_s_else = ReturnStatement(name=StringValue('r_s_2'), l_type=ClabjectReference(LocationValue('mvk.action.ReturnStatement')))
        f_if_r_s_else_expr = Minus(name=StringValue('zero_minus_b'), l_type=ClabjectReference(LocationValue('mvk.action.Minus')))
        f_if_r_s_else.set_expression(f_if_r_s_else_expr)
        f_if_r_s_else_expr.add_child(Constant(name=StringValue('zero'), l_type=ClabjectReference(LocationValue('mvk.action.Constant')), value=IntegerValue(0)))
        f_if_r_s_else_expr.add_child(Navigation(name=StringValue('b'), l_type=ClabjectReference(LocationValue('mvk.action.Navigation')), path=LocationValue('b')))
        f_if.get_else_body().add_statement(f_if_r_s_else)

        f.get_body().add_statement(f_decl_i)
        f.get_body().add_statement(f_while)
        f.get_body().add_statement(f_if)

        '''
        package test
            model test_model:
        '''
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('test'),
                                           CreateConstants.TYPE_KEY: LocationValue('mvk.object.Model'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('test_model'),
                                                                                    StringValue('potency'): IntegerValue(1),
                                                                                    StringValue('type_model'): LocationValue('mvk.object')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        self.assertTrue(self.mvk.read(LocationValue('test.test_model')).is_success())
        '''
        package test
            model test_model:
                string f(a: int, b:float) {
        '''
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('test.test_model'),
                                           CreateConstants.TYPE_KEY: LocationValue('mvk.action.Function'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('f'),
                                                                                    StringValue('type'): StringType(),
                                                                                    StringValue('class'): LocationValue('mvk.action.Function')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        self.assertTrue(self.mvk.read(LocationValue('test.test_model.f')).is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f'),
                                           CreateConstants.TYPE_KEY: LocationValue('mvk.action.Body'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('body'),
                                                                                    StringValue('class'): LocationValue('mvk.action.Body')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        self.assertTrue(self.mvk.read(LocationValue('test.test_model.f.body')).is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f'),
                                           CreateConstants.TYPE_KEY: LocationValue('mvk.action.Parameter'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('a'),
                                                                                    StringValue('type'): IntegerType(),
                                                                                    StringValue('parameter_type'): StringValue('in'),
                                                                                    StringValue('class'): LocationValue('mvk.action.Parameter')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        self.assertTrue(self.mvk.read(LocationValue('test.test_model.f.a')).is_success())
        self.assertEqual(self.mvk.read(LocationValue('test.test_model.f.a')).get_item(), f_a)
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f'),
                                           CreateConstants.TYPE_KEY: LocationValue('mvk.action.Parameter'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('b'),
                                                                                    StringValue('type'): FloatType(),
                                                                                    StringValue('parameter_type'): StringValue('in'),
                                                                                    StringValue('class'): LocationValue('mvk.action.Parameter')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        self.assertTrue(self.mvk.read(LocationValue('test.test_model.f.b')).is_success())
        self.assertEqual(self.mvk.read(LocationValue('test.test_model.f.b')).get_item(), f_b)
        '''
        package test
            model test_model:
                string f(a: int, b:float) {
                    int i = 5
        '''
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body'),
                                           CreateConstants.TYPE_KEY: LocationValue('mvk.action.DeclarationStatement'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('decl_i'),
                                                                                    StringValue('class'): LocationValue('mvk.action.DeclarationStatement')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        self.assertTrue(self.mvk.read(LocationValue('test.test_model.f.body.decl_i')).is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.decl_i'),
                                           CreateConstants.TYPE_KEY: LocationValue('mvk.action.Identifier'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('i'),
                                                                                    StringValue('type'): IntegerType(),
                                                                                    StringValue('class'): LocationValue('mvk.action.Identifier')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        self.assertTrue(self.mvk.read(LocationValue('test.test_model.f.body.decl_i.i')).is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.decl_i'),
                                           CreateConstants.TYPE_KEY: LocationValue('mvk.action.Constant'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('five'),
                                                                                    StringValue('value'): IntegerValue(5),
                                                                                    StringValue('class'): LocationValue('mvk.action.Constant')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        self.assertTrue(self.mvk.read(LocationValue('test.test_model.f.body.decl_i.five')).is_success())
        self.assertEqual(self.mvk.read(LocationValue('test.test_model.f.body.decl_i')).get_item(), f_decl_i)
        '''
        package test
            model test_model:
                string f(a: int, b:float) {
                    int i = 5
                    while i > 0:
        '''
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body'),
                                           CreateConstants.TYPE_KEY: LocationValue('mvk.action.WhileLoop'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('while_1'),
                                                                                    StringValue('class'): LocationValue('mvk.action.WhileLoop')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        self.assertTrue(self.mvk.read(LocationValue('test.test_model.f.body.while_1')).is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1'),
                                           CreateConstants.TYPE_KEY: LocationValue('mvk.action.Body'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('body'),
                                                                                    StringValue('class'): LocationValue('mvk.action.Body')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        self.assertTrue(self.mvk.read(LocationValue('test.test_model.f.body.while_1.body')).is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1'),
                                           CreateConstants.TYPE_KEY: LocationValue('mvk.action.GreaterThan'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('while_1_expr'),
                                                                                    StringValue('class'): LocationValue('mvk.action.GreaterThan')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        self.assertTrue(self.mvk.read(LocationValue('test.test_model.f.body.while_1.while_1_expr')).is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1.while_1_expr'),
                                           CreateConstants.TYPE_KEY: LocationValue('mvk.action.Navigation'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('i'),
                                                                                    StringValue('class'): LocationValue('mvk.action.Navigation'),
                                                                                    StringValue('path'): LocationValue('i')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        self.assertTrue(self.mvk.read(LocationValue('test.test_model.f.body.while_1.while_1_expr.i')).is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1.while_1_expr'),
                                           CreateConstants.TYPE_KEY: LocationValue('mvk.action.Constant'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('zero'),
                                                                                    StringValue('class'): LocationValue('mvk.action.Constant'),
                                                                                    StringValue('value'): IntegerValue(0)})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        self.assertTrue(self.mvk.read(LocationValue('test.test_model.f.body.while_1.while_1_expr.zero')).is_success())
        self.assertEqual(self.mvk.read(LocationValue('test.test_model.f.body.while_1.while_1_expr')).get_item(), f_while_test)
        '''
        package test
            model test_model:
                string f(a: int, b:float) {
                    int i = 5
                    while i > 0:
                        b = b + mvk.g(c=5)
        '''
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1.body'),
                                           CreateConstants.TYPE_KEY: LocationValue('mvk.action.ExpressionStatement'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('e_s_1'),
                                                                                    StringValue('class'): LocationValue('mvk.action.ExpressionStatement')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        self.assertTrue(self.mvk.read(LocationValue('test.test_model.f.body.while_1.body.e_s_1')).is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1.body.e_s_1'),
                                           CreateConstants.TYPE_KEY: LocationValue('mvk.action.Assignment'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('a_e_1'),
                                                                                    StringValue('class'): LocationValue('mvk.action.Assignment')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        self.assertTrue(self.mvk.read(LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1')).is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1'),
                                           CreateConstants.TYPE_KEY: LocationValue('mvk.action.Identifier'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('b'),
                                                                                    StringValue('type'): FloatType(),
                                                                                    StringValue('class'): LocationValue('mvk.action.Identifier')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        self.assertTrue(self.mvk.read(LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1.b')).is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1'),
                                           CreateConstants.TYPE_KEY: LocationValue('mvk.action.Plus'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('b_plus_g'),
                                                                                    StringValue('class'): LocationValue('mvk.action.Plus')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        self.assertTrue(self.mvk.read(LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1.b_plus_g')).is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1.b_plus_g'),
                                           CreateConstants.TYPE_KEY: LocationValue('mvk.action.Navigation'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('b'),
                                                                                    StringValue('class'): LocationValue('mvk.action.Navigation'),
                                                                                    StringValue('path'): LocationValue('b')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        self.assertTrue(self.mvk.read(LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1.b_plus_g.b')).is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1.b_plus_g'),
                                           CreateConstants.TYPE_KEY: LocationValue('mvk.action.FunctionCall'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('g'),
                                                                                    StringValue('class'): LocationValue('mvk.action.FunctionCall'),
                                                                                    StringValue('function'): LocationValue('g')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        self.assertTrue(self.mvk.read(LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1.b_plus_g.g')).is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1.b_plus_g.g'),
                                           CreateConstants.TYPE_KEY: LocationValue('mvk.action.Navigation'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('mvk'),
                                                                                    StringValue('class'): LocationValue('mvk.action.Navigation'),
                                                                                    StringValue('path'): LocationValue('mvk')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        self.assertTrue(self.mvk.read(LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1.b_plus_g.g.mvk')).is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1.b_plus_g.g'),
                                           CreateConstants.TYPE_KEY: LocationValue('mvk.action.Argument'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('c'),
                                                                                    StringValue('class'): LocationValue('mvk.action.Argument'),
                                                                                    StringValue('key'): LocationValue('c')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        self.assertTrue(self.mvk.read(LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1.b_plus_g.g.c')).is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1.b_plus_g.g.c'),
                                           CreateConstants.TYPE_KEY: LocationValue('mvk.action.Constant'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('five'),
                                                                                    StringValue('class'): LocationValue('mvk.action.Constant'),
                                                                                    StringValue('value'): IntegerValue(5)})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        self.assertTrue(self.mvk.read(LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1.b_plus_g.g.c.five')).is_success())
        self.assertEqual(self.mvk.read(LocationValue('test.test_model.f.body.while_1.body.e_s_1')).get_item(), f_while_e_s_1)
        '''
        package test
            model test_model:
                string f(a: int, b:float) {
                    int i = 5
                    while i > 0:
                        b = b + mvk.g(c=5)
                        i = i - 1
        '''
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1.body'),
                                           CreateConstants.TYPE_KEY: LocationValue('mvk.action.ExpressionStatement'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('e_s_2'),
                                                                                    StringValue('class'): LocationValue('mvk.action.ExpressionStatement')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        self.assertTrue(self.mvk.read(LocationValue('test.test_model.f.body.while_1.body.e_s_2')).is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1.body.e_s_2'),
                                           CreateConstants.TYPE_KEY: LocationValue('mvk.action.Assignment'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('a_e_2'),
                                                                                    StringValue('class'): LocationValue('mvk.action.Assignment')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        self.assertTrue(self.mvk.read(LocationValue('test.test_model.f.body.while_1.body.e_s_2.a_e_2')).is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1.body.e_s_2.a_e_2'),
                                           CreateConstants.TYPE_KEY: LocationValue('mvk.action.Identifier'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('i'),
                                                                                    StringValue('type'): IntegerType(),
                                                                                    StringValue('class'): LocationValue('mvk.action.Identifier')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        self.assertTrue(self.mvk.read(LocationValue('test.test_model.f.body.while_1.body.e_s_2.a_e_2.i')).is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1.body.e_s_2.a_e_2'),
                                           CreateConstants.TYPE_KEY: LocationValue('mvk.action.Minus'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('i_min_1'),
                                                                                    StringValue('class'): LocationValue('mvk.action.Minus')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        self.assertTrue(self.mvk.read(LocationValue('test.test_model.f.body.while_1.body.e_s_2.a_e_2.i_min_1')).is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1.body.e_s_2.a_e_2.i_min_1'),
                                           CreateConstants.TYPE_KEY: LocationValue('mvk.action.Navigation'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('i'),
                                                                                    StringValue('class'): LocationValue('mvk.action.Navigation'),
                                                                                    StringValue('path'): LocationValue('i')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        self.assertTrue(self.mvk.read(LocationValue('test.test_model.f.body.while_1.body.e_s_2.a_e_2.i_min_1.i')).is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1.body.e_s_2.a_e_2.i_min_1'),
                                           CreateConstants.TYPE_KEY: LocationValue('mvk.action.Constant'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('one'),
                                                                                    StringValue('class'): LocationValue('mvk.action.Constant'),
                                                                                    StringValue('value'): IntegerValue(1)})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        self.assertTrue(self.mvk.read(LocationValue('test.test_model.f.body.while_1.body.e_s_2.a_e_2.i_min_1.one')).is_success())
        self.assertEqual(self.mvk.read(LocationValue('test.test_model.f.body.while_1.body.e_s_2')).get_item(), f_while_e_s_2)
        self.assertEqual(self.mvk.read(LocationValue('test.test_model.f.body.while_1')).get_item(), f_while)
        '''
        package test
            model test_model:
                string f(a: int, b:float) {
                    int i = 5
                    while i > 0:
                        b = b + mvk.g(c=5)
                        i = i - 1
                    if b > 100:
        '''
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body'),
                                           CreateConstants.TYPE_KEY: LocationValue('mvk.action.IfStatement'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('ifstmt_1'),
                                                                                    StringValue('class'): LocationValue('mvk.action.IfStatement')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        self.assertTrue(self.mvk.read(LocationValue('test.test_model.f.body.ifstmt_1')).is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.ifstmt_1'),
                                           CreateConstants.TYPE_KEY: LocationValue('mvk.action.Body'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('ifbody'),
                                                                                    StringValue('class'): LocationValue('mvk.action.Body')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        self.assertTrue(self.mvk.read(LocationValue('test.test_model.f.body.ifstmt_1.ifbody')).is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.ifstmt_1'),
                                           CreateConstants.TYPE_KEY: LocationValue('mvk.action.Body'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('elsebody'),
                                                                                    StringValue('class'): LocationValue('mvk.action.Body')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        self.assertTrue(self.mvk.read(LocationValue('test.test_model.f.body.ifstmt_1.elsebody')).is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.ifstmt_1'),
                                           CreateConstants.TYPE_KEY: LocationValue('mvk.action.GreaterThan'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('ifstmt_1_expr'),
                                                                                    StringValue('class'): LocationValue('mvk.action.GreaterThan')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        self.assertTrue(self.mvk.read(LocationValue('test.test_model.f.body.ifstmt_1.ifstmt_1_expr')).is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.ifstmt_1.ifstmt_1_expr'),
                                           CreateConstants.TYPE_KEY: LocationValue('mvk.action.Navigation'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('b'),
                                                                                    StringValue('class'): LocationValue('mvk.action.Navigation'),
                                                                                    StringValue('path'): LocationValue('b')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        self.assertTrue(self.mvk.read(LocationValue('test.test_model.f.body.ifstmt_1.ifstmt_1_expr.b')).is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.ifstmt_1.ifstmt_1_expr'),
                                           CreateConstants.TYPE_KEY: LocationValue('mvk.action.Constant'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('onehundred'),
                                                                                    StringValue('class'): LocationValue('mvk.action.Constant'),
                                                                                    StringValue('value'): IntegerValue(100)})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        self.assertTrue(self.mvk.read(LocationValue('test.test_model.f.body.ifstmt_1.ifstmt_1_expr.onehundred')).is_success())
        self.assertEqual(self.mvk.read(LocationValue('test.test_model.f.body.ifstmt_1.ifstmt_1_expr')).get_item(), f_if_test)
        '''
        package test
            model test_model:
                string f(a: int, b:float) {
                    int i = 5
                    while i > 0:
                        b = b + mvk.g(c=5)
                        i = i - 1
                    if b > 100:
                        return b
        '''
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.ifstmt_1.ifbody'),
                                           CreateConstants.TYPE_KEY: LocationValue('mvk.action.ReturnStatement'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('r_s_1'),
                                                                                    StringValue('class'): LocationValue('mvk.action.ReturnStatement')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        self.assertTrue(self.mvk.read(LocationValue('test.test_model.f.body.ifstmt_1.ifbody.r_s_1')).is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.ifstmt_1.ifbody.r_s_1'),
                                           CreateConstants.TYPE_KEY: LocationValue('mvk.action.Navigation'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('b'),
                                                                                    StringValue('class'): LocationValue('mvk.action.Navigation'),
                                                                                    StringValue('path'): LocationValue('b')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        self.assertTrue(self.mvk.read(LocationValue('test.test_model.f.body.ifstmt_1.ifbody.r_s_1.b')).is_success())
        self.assertEqual(self.mvk.read(LocationValue('test.test_model.f.body.ifstmt_1.ifbody.r_s_1')).get_item(), f_if_r_s_if)
        '''
        package test
            model test_model:
                string f(a: int, b:float) {
                    int i = 5
                    while i > 0:
                        b = b + mvk.g(c=5)
                        i = i - 1
                    if b > 100:
                        return b
                    else:
                        return -b
        '''
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.ifstmt_1.elsebody'),
                                           CreateConstants.TYPE_KEY: LocationValue('mvk.action.ReturnStatement'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('r_s_2'),
                                                                                    StringValue('class'): LocationValue('mvk.action.ReturnStatement')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        self.assertTrue(self.mvk.read(LocationValue('test.test_model.f.body.ifstmt_1.elsebody.r_s_2')).is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.ifstmt_1.elsebody.r_s_2'),
                                           CreateConstants.TYPE_KEY: LocationValue('mvk.action.Minus'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('zero_minus_b'),
                                                                                    StringValue('class'): LocationValue('mvk.action.Minus')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        self.assertTrue(self.mvk.read(LocationValue('test.test_model.f.body.ifstmt_1.elsebody.r_s_2.zero_minus_b')).is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.ifstmt_1.elsebody.r_s_2.zero_minus_b'),
                                           CreateConstants.TYPE_KEY: LocationValue('mvk.action.Constant'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('zero'),
                                                                                    StringValue('class'): LocationValue('mvk.action.Constant'),
                                                                                    StringValue('value'): IntegerValue(0)})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        self.assertTrue(self.mvk.read(LocationValue('test.test_model.f.body.ifstmt_1.elsebody.r_s_2.zero_minus_b.zero')).is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.ifstmt_1.elsebody.r_s_2.zero_minus_b'),
                                           CreateConstants.TYPE_KEY: LocationValue('mvk.action.Navigation'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('b'),
                                                                                    StringValue('class'): LocationValue('mvk.action.Navigation'),
                                                                                    StringValue('path'): LocationValue('b')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        self.assertTrue(self.mvk.read(LocationValue('test.test_model.f.body.ifstmt_1.elsebody.r_s_2.zero_minus_b.b')).is_success())
        self.assertEqual(self.mvk.read(LocationValue('test.test_model.f.body.ifstmt_1.elsebody.r_s_2')).get_item(), f_if_r_s_else)
        self.assertEqual(self.mvk.read(LocationValue('test.test_model.f.body.ifstmt_1')).get_item(), f_if)

        self.assertTrue(self.mvk.delete(LocationValue('test.test_model.f.body.ifstmt_1.elsebody.r_s_2.zero_minus_b.zero')).is_success())
        self.assertFalse(self.mvk.read(LocationValue('test.test_model.f.body.ifstmt_1.elsebody.r_s_2.zero_minus_b.zero')).is_success())
        self.assertTrue(self.mvk.delete(LocationValue('test.test_model.f.body.ifstmt_1.elsebody.r_s_2.zero_minus_b.b')).is_success())
        self.assertFalse(self.mvk.read(LocationValue('test.test_model.f.body.ifstmt_1.elsebody.r_s_2.zero_minus_b.b')).is_success())
        self.assertTrue(self.mvk.delete(LocationValue('test.test_model.f.body.ifstmt_1.elsebody.r_s_2.zero_minus_b')).is_success())
        self.assertFalse(self.mvk.read(LocationValue('test.test_model.f.body.ifstmt_1.elsebody.r_s_2.zero_minus_b')).is_success())
        self.assertTrue(self.mvk.delete(LocationValue('test.test_model.f.body.ifstmt_1.elsebody.r_s_2')).is_success())
        self.assertFalse(self.mvk.read(LocationValue('test.test_model.f.body.ifstmt_1.elsebody.r_s_2')).is_success())

        self.assertTrue(self.mvk.delete(LocationValue('test.test_model.f.body.ifstmt_1.ifbody.r_s_1.b')).is_success())
        self.assertFalse(self.mvk.read(LocationValue('test.test_model.f.body.ifstmt_1.ifbody.r_s_1.b')).is_success())
        self.assertTrue(self.mvk.delete(LocationValue('test.test_model.f.body.ifstmt_1.ifbody.r_s_1')).is_success())
        self.assertFalse(self.mvk.read(LocationValue('test.test_model.f.body.ifstmt_1.ifbody.r_s_1')).is_success())

        self.assertTrue(self.mvk.delete(LocationValue('test.test_model.f.body.ifstmt_1')).is_success())
        self.assertFalse(self.mvk.read(LocationValue('test.test_model.f.body.ifstmt_1')).is_success())

        self.assertTrue(self.mvk.delete(LocationValue('test.test_model.f.body.while_1.body.e_s_2.a_e_2.i_min_1.i')).is_success())
        self.assertFalse(self.mvk.read(LocationValue('test.test_model.f.body.while_1.body.e_s_2.a_e_2.i_min_1.i')).is_success())
        self.assertTrue(self.mvk.delete(LocationValue('test.test_model.f.body.while_1.body.e_s_2.a_e_2.i_min_1.one')).is_success())
        self.assertFalse(self.mvk.read(LocationValue('test.test_model.f.body.while_1.body.e_s_2.a_e_2.i_min_1.one')).is_success())
        self.assertTrue(self.mvk.delete(LocationValue('test.test_model.f.body.while_1.body.e_s_2.a_e_2.i_min_1')).is_success())
        self.assertFalse(self.mvk.read(LocationValue('test.test_model.f.body.while_1.body.e_s_2.a_e_2.i_min_1')).is_success())
        self.assertTrue(self.mvk.delete(LocationValue('test.test_model.f.body.while_1.body.e_s_2.a_e_2')).is_success())
        self.assertFalse(self.mvk.read(LocationValue('test.test_model.f.body.while_1.body.e_s_2.a_e_2')).is_success())
        self.assertTrue(self.mvk.delete(LocationValue('test.test_model.f.body.while_1.body.e_s_2')).is_success())
        self.assertFalse(self.mvk.read(LocationValue('test.test_model.f.body.while_1.body.e_s_2')).is_success())

        self.assertTrue(self.mvk.delete(LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1.b_plus_g.g.c.five')).is_success())
        self.assertFalse(self.mvk.read(LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1.b_plus_g.g.c.five')).is_success())
        self.assertTrue(self.mvk.delete(LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1.b_plus_g.g.c')).is_success())
        self.assertFalse(self.mvk.read(LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1.b_plus_g.g.c')).is_success())
        self.assertTrue(self.mvk.delete(LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1.b_plus_g.g.mvk')).is_success())
        self.assertFalse(self.mvk.read(LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1.b_plus_g.g.mvk')).is_success())
        self.assertTrue(self.mvk.delete(LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1.b_plus_g.g')).is_success())
        self.assertFalse(self.mvk.read(LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1.b_plus_g.g')).is_success())
        self.assertTrue(self.mvk.delete(LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1.b_plus_g.b')).is_success())
        self.assertFalse(self.mvk.read(LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1.b_plus_g.b')).is_success())
        self.assertTrue(self.mvk.delete(LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1.b_plus_g')).is_success())
        self.assertFalse(self.mvk.read(LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1.b_plus_g')).is_success())
        self.assertTrue(self.mvk.delete(LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1')).is_success())
        self.assertFalse(self.mvk.read(LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1')).is_success())
        self.assertTrue(self.mvk.delete(LocationValue('test.test_model.f.body.while_1.body.e_s_1')).is_success())
        self.assertFalse(self.mvk.read(LocationValue('test.test_model.f.body.while_1.body.e_s_1')).is_success())

        self.assertTrue(self.mvk.delete(LocationValue('test.test_model.f.body.while_1')).is_success())
        self.assertFalse(self.mvk.read(LocationValue('test.test_model.f.body.while_1')).is_success())

        self.assertTrue(self.mvk.delete(LocationValue('test.test_model.f.body.decl_i.i')).is_success())
        self.assertFalse(self.mvk.read(LocationValue('test.test_model.f.body.decl_i.i')).is_success())
        self.assertTrue(self.mvk.delete(LocationValue('test.test_model.f.body.decl_i')).is_success())
        self.assertFalse(self.mvk.read(LocationValue('test.test_model.f.body.decl_i')).is_success())

        self.assertTrue(self.mvk.delete(LocationValue('test.test_model.f.a')).is_success())
        self.assertFalse(self.mvk.read(LocationValue('test.test_model.f.a')).is_success())
        self.assertTrue(self.mvk.delete(LocationValue('test.test_model.f.b')).is_success())
        self.assertFalse(self.mvk.read(LocationValue('test.test_model.f.b')).is_success())
        self.assertTrue(self.mvk.delete(LocationValue('test.test_model.f')).is_success())
        self.assertFalse(self.mvk.read(LocationValue('test.test_model.f')).is_success())

#if __name__ == "__main__":
def runTests():
    unittest.main()
