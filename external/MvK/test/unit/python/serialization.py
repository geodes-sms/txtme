'''
Created on 6-mrt.-2014

@author: Simon
'''
from inspect import Attribute
from json.encoder import JSONEncoder
import unittest

from mvk.impl.python.datatype import *
from mvk.impl.python.datavalue import IntegerValue, FloatValue, BooleanValue, \
    StringValue, LocationValue, InfiniteValue, SequenceValue, TupleValue, SetValue, \
    MappingValue
from mvk.impl.python.object import Package, Model, ModelReference, Clabject, \
    ClabjectReference, Association, AssociationReference, AssociationEnd, Attribute
from mvk.impl.python.python_representer import PythonRepresenter
from mvk.impl.client.jsondeserializer import MvKDecoder
from mvk.impl.python.util.jsonserializer import MvKEncoder
from mvk.util import logger
from mvk.util.utility_functions import lists_eq_items
from mvk.impl.python.action import *

class TestSerialization(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.encoder = MvKEncoder()
        self.refencoder = JSONEncoder()
        self.decoder = MvKDecoder()

    def test_serialize_primitives(self):
        vals = [(IntegerValue(5), {'type': 'IntegerValue',
                                   'value': 5}),
                (FloatValue(5.0), {'type': 'FloatValue',
                                   'value': 5.0}),
                (BooleanValue(True), {'type': 'BooleanValue',
                                      'value': True}),
                (StringValue('test'), {'type': 'StringValue',
                                       'value': 'test'}),
                (LocationValue('formalisms.Petrinets'), {'type': 'LocationValue',
                                                         'value': 'formalisms.Petrinets'}),
                (InfiniteValue('+'), {'type': 'InfiniteValue',
                                      'value': float('+inf')})]
        for val in vals:
            encoded = self.encoder.encode(val[0])
            refencoded = self.refencoder.encode(val[1])
            self.assertEquals(encoded, refencoded)
            self.assertEquals(self.decoder.decode(encoded), val[0])

    def test_serialize_composite(self):
        vals = [SequenceValue([IntegerValue(1), IntegerValue(2), IntegerValue(3)]),
                TupleValue((FloatValue(1.0), FloatValue(2.0), FloatValue(3.0))),
                SetValue(set([StringValue('1'), StringValue('2'), StringValue('3')])),
                MappingValue({StringValue('1'): IntegerValue(1),
                               StringValue('2'): IntegerValue(2),
                               StringValue('3'): IntegerValue(3)}),
                MappingValue({TupleValue((IntegerValue(1),
                                          IntegerValue(2),
                                          IntegerValue(3))): StringValue('123'),
                              StringValue('1'): StringValue('231'),
                              IntegerValue(1): StringValue('1')}),
                SequenceValue([MappingValue({TupleValue((IntegerValue(1),
                                                         IntegerValue(2),
                                                         IntegerValue(3))): StringValue('123'),
                               StringValue('1'): StringValue('231'),
                               IntegerValue(1): StringValue('1')}),
                               SetValue(set([StringValue('1'), StringValue('2'), StringValue('3')])),
                               SequenceValue([IntegerValue(1), IntegerValue(2), IntegerValue(3)])])]
        for val in vals:
            encoded = self.encoder.encode(val)
            ''' we can't test the reference encoder here, because of
            differences when encoding composite values where the order of
            items does not matter '''
            self.assertEquals(self.decoder.decode(encoded), val)

    def test_serialize_changelogs(self):
        from mvk.impl.python.changelog import MvKDeleteLog, MvKCreateLog, MvKReadLog, MvKCompositeLog, MvKCreateCompositeLog, MvKOperationLog
        from mvk.impl.python.constants import DeleteConstants, CreateConstants, ReadConstants, LogConstants

        delete_log = MvKDeleteLog()
        delete_log.set_location(LocationValue("a.b.c"))
        # Just set something here...
        delete_log.set_item(StringValue("abc"))
        delete_log.set_type(LocationValue("d.e.f"))
        delete_log.set_status_code(DeleteConstants.SUCCESS_CODE)
        delete_log.set_status_message(StringValue("Success"))

        create_log = MvKCreateLog()
        create_log.set_location(LocationValue("a.b.c"))
        create_log.set_type(LocationValue("d.e.f"))
        create_log.set_name(StringValue("g"))
        create_log.add_attr_change(StringValue('attr1'), StringValue("h"))
        create_log.set_status_code(CreateConstants.SUCCESS_CODE)
        create_log.set_status_message(StringValue("Success"))

        read_log = MvKReadLog()
        read_log.set_location(LocationValue("a.b.c"))
        read_log.set_type(LocationValue("d.e.f"))
        read_log.set_item(StringValue("abc"))
        read_log.set_status_code(ReadConstants.SUCCESS_CODE)
        read_log.set_status_message(StringValue("Success"))

        composite_log = MvKCompositeLog()
        composite_log.set_status_code(ReadConstants.SUCCESS_CODE)
        composite_log.set_status_message(StringValue("OK"))
        composite_log.add_log(read_log)
        composite_log.add_log(delete_log)

        create_composite_log = MvKCreateCompositeLog()
        create_composite_log.set_status_code(ReadConstants.SUCCESS_CODE)
        create_composite_log.set_status_message(StringValue("OK"))
        create_composite_log.add_log(create_log)
        create_composite_log.add_log(create_log)

        operation_log = MvKOperationLog(operation_name=StringValue('clear'))
        operation_log.set_result(IntegerValue(1))
        operation_log.set_status_code(LogConstants.SUCCESS_CODE)
        operation_log.set_status_message(StringValue("Success"))

        vals = [delete_log,
                create_log,
                read_log,
                composite_log,
                create_composite_log,
                operation_log
                ]

        for i, log in enumerate(vals):
            self.assertEquals(type(self.encoder.encode(log)), str)
            for j, other_log in enumerate(vals):
                if i == j:
                    # Equal logs should stay equal after serialization
                    self.assertEquals(self.decoder.decode(self.encoder.encode(log)), other_log)
                else:   
                    # Different logs should be different after serialization
                    self.assertFalse(self.decoder.decode(self.encoder.encode(log)) == other_log)

    def test_serialize_objects(self):
        root = Package(name=StringValue("root"))

        # Test a Package first
        p = Package(name=StringValue("test_package"))
        p.parent = root
        p1 = Package(name=StringValue("child1"))
        p1.parent = p
        p2 = Package(name=StringValue("child2"))
        p2.parent = p
        p3 = Package(name=StringValue("child3"))
        p3.parent = p1
        p1.name_lookup[StringValue('child3')] = p3
        p.name_lookup[StringValue('child1')] = p1
        p.name_lookup[StringValue('child2')] = p2
        enc_p = self.encoder.encode(p)
        self.assertTrue(isinstance(p, mvk.impl.python.object.Package))
        self.assertTrue(isinstance(enc_p, str))
        enc_p = self.decoder.decode(enc_p)
        self.assertTrue(isinstance(enc_p, mvk.impl.client.object.Package))

        self.assertEquals(enc_p.location, StringValue("root.test_package"))
        self.assertEquals(enc_p.linguistic_type, StringValue("mvk.object.Package"))
        self.assertEquals(enc_p.name, StringValue("test_package"))
        self.assertEquals(enc_p.children, [(StringValue("child1"), StringValue("root.test_package.child1")), (StringValue("child2"), StringValue("root.test_package.child2"))])

        # Now a Model
        m = Model(name=StringValue("test_model"), l_type=ModelReference(LocationValue('mvk.object')), potency=IntegerValue(1))
        m.parent = root
        enc_m = self.encoder.encode(m)
        self.assertTrue(isinstance(m, mvk.impl.python.object.Model))
        self.assertTrue(isinstance(enc_m, str))
        enc_m = self.decoder.decode(enc_m)
        self.assertTrue(isinstance(enc_m, mvk.impl.client.object.Model))

        self.assertEquals(enc_m.location, StringValue("root.test_model"))
        self.assertEquals(enc_m.linguistic_type, LocationValue("mvk.object"))
        self.assertEquals(enc_m.name, StringValue("test_model"))
        self.assertEquals(enc_m.potency, IntegerValue(1))
        self.assertEquals(enc_m.in_associations, SequenceValue([]))
        self.assertEquals(enc_m.out_associations, SequenceValue([]))
        self.assertEquals(enc_m.functions, SequenceValue([]))
        self.assertEquals(enc_m.elements, [])
        self.assertEquals(enc_m.attributes, [])

        # An abstract clabject with potency > 0
        c = Clabject(name=StringValue("test_clabject"), l_type=ClabjectReference(LocationValue('mvk.object.Clabject')), potency=IntegerValue(1), abstract=BooleanValue(True))
        c.parent = m
        enc_c = self.encoder.encode(c)
        self.assertTrue(isinstance(c, mvk.impl.python.object.Clabject))
        self.assertTrue(isinstance(enc_c, str))
        enc_c = self.decoder.decode(enc_c)
        self.assertTrue(isinstance(enc_c, mvk.impl.client.object.Clabject))

        self.assertEquals(enc_c.location, StringValue("root.test_model.test_clabject"))
        self.assertEquals(enc_c.name, StringValue("test_clabject"))
        self.assertEquals(enc_c.linguistic_type, StringValue("mvk.object.Clabject"))
        self.assertEquals(enc_c.attributes, [])
        self.assertEquals(enc_c.in_associations, SequenceValue([]))
        self.assertEquals(enc_c.out_associations, SequenceValue([]))
        self.assertEquals(enc_c.potency, IntegerValue(1))
        self.assertEquals(enc_c.abstract, BooleanValue(True))
        self.assertEquals(enc_c.lower, IntegerValue(0))
        self.assertEquals(enc_c.upper, InfiniteValue("+"))
        self.assertEquals(enc_c.ordered, BooleanValue(False))
        self.assertEquals(enc_c.superclasses, SequenceValue([]))

        # Then a non-abstract clabject with potency 0
        c = Clabject(name=StringValue("test_clabject_inst"), l_type=ClabjectReference(LocationValue('root.test_model.test_clabject')), potency=IntegerValue(0), abstract=BooleanValue(False))
        c.parent = m
        enc_c = self.encoder.encode(c)
        self.assertTrue(isinstance(c, mvk.impl.python.object.Clabject))
        self.assertTrue(isinstance(enc_c, str))
        enc_c = self.decoder.decode(enc_c)
        self.assertTrue(isinstance(enc_c, mvk.impl.client.object.Clabject))

        self.assertEquals(enc_c.location, StringValue("root.test_model.test_clabject_inst"))
        self.assertEquals(enc_c.name, StringValue("test_clabject_inst"))
        self.assertEquals(enc_c.linguistic_type, StringValue("root.test_model.test_clabject"))
        self.assertEquals(enc_c.potency, IntegerValue(0))
        self.assertEquals(enc_c.in_associations, SequenceValue([]))
        self.assertEquals(enc_c.out_associations, SequenceValue([]))
        self.assertEquals(enc_c.attributes, [])

        # Associations require access to the MvK, which we don't want to do here

        # Finally we create an attribute
        # Let's start with potency > 0
        a = Attribute(name=StringValue("test_attribute"), the_type=IntegerType(), default=IntegerValue(1), potency=IntegerValue(1), l_type=ClabjectReference(LocationValue("root.l_type")))
        a.parent = c
        enc_a = self.encoder.encode(a)
        self.assertTrue(isinstance(a, mvk.impl.python.object.Attribute))
        self.assertTrue(isinstance(enc_a, str))
        enc_a = self.decoder.decode(enc_a)
        self.assertTrue(isinstance(enc_a, mvk.impl.client.object.Attribute))

        self.assertEquals(enc_a.location, StringValue("root.test_model.test_clabject_inst.test_attribute"))
        self.assertEquals(enc_a.short_location, StringValue("test_clabject_inst.test_attribute"))
        self.assertEquals(enc_a.name, StringValue("test_attribute"))
        self.assertEquals(enc_a.linguistic_type, StringValue("root.l_type"))
        self.assertEquals(enc_a.the_type, IntegerType())
        self.assertEquals(enc_a.potency, IntegerValue(1))
        self.assertEquals(enc_a.attributes, [])
        self.assertEquals(enc_a.default, IntegerValue(1))
        self.assertEquals(enc_a.lower, IntegerValue(1))
        self.assertEquals(enc_a.in_associations, SequenceValue([]))
        self.assertEquals(enc_a.out_associations, SequenceValue([]))
        self.assertEquals(enc_a.upper, IntegerValue(1))

        # And for potency == 0
        a = Attribute(name=StringValue("test_attribute2"), the_type=IntegerType(), value=IntegerValue(2), potency=IntegerValue(0), l_type=a)
        a.parent = c
        enc_a = self.encoder.encode(a)
        self.assertTrue(isinstance(a, mvk.impl.python.object.Attribute))
        self.assertTrue(isinstance(enc_a, str))
        enc_a = self.decoder.decode(enc_a)
        self.assertTrue(isinstance(enc_a, mvk.impl.client.object.Attribute))

        self.assertEquals(enc_a.location, StringValue("root.test_model.test_clabject_inst.test_attribute2"))
        self.assertEquals(enc_a.name, StringValue("test_attribute2"))
        self.assertEquals(enc_a.linguistic_type, StringValue("root.test_model.test_clabject_inst.test_attribute"))
        self.assertEquals(enc_a.potency, IntegerValue(0))
        self.assertEquals(enc_a.attributes, [])
        self.assertEquals(enc_a.in_associations, SequenceValue([]))
        self.assertEquals(enc_a.out_associations, SequenceValue([]))
        self.assertEquals(enc_a.value, IntegerValue(2))

    def test_serialize_action(self):
        from mvk.impl.python.object import Package, Model, ClabjectReference

        # The same one as found in the action test
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

        enc = self.encoder.encode(test)
        self.assertTrue(isinstance(test, mvk.impl.python.object.Package))
        self.assertTrue(isinstance(enc, str))
        enc = self.decoder.decode(enc)
        self.assertTrue(isinstance(enc, mvk.impl.client.object.Package))

        self.assertEquals(enc.location, StringValue("test"))
        self.assertEquals(enc.linguistic_type, StringValue("mvk.object.Package"))
        self.assertEquals(enc.name, StringValue("test"))
        self.assertEquals(enc.children, [(StringValue("test_model"), StringValue("test.test_model"))])

        enc = self.encoder.encode(test_model)
        self.assertTrue(isinstance(test_model, mvk.impl.python.object.Model))
        self.assertTrue(isinstance(enc, str))
        enc = self.decoder.decode(enc)
        self.assertTrue(isinstance(enc, mvk.impl.client.object.Model))

        self.assertEquals(enc.location, StringValue("test.test_model"))
        self.assertEquals(enc.linguistic_type, LocationValue("mvk.object"))
        self.assertEquals(enc.name, StringValue("test_model"))
        self.assertEquals(enc.potency, IntegerValue(1))
        self.assertEquals(enc.in_associations, SequenceValue([]))
        self.assertEquals(enc.out_associations, SequenceValue([]))
        self.assertEquals(enc.functions, SequenceValue([LocationValue("test.test_model.f")]))
        self.assertEquals(enc.elements, [])
        self.assertEquals(enc.attributes, [])

        enc = self.encoder.encode(f)
        self.assertTrue(isinstance(f, mvk.impl.python.action.Function))
        self.assertTrue(isinstance(enc, str))
        enc = self.decoder.decode(enc)
        self.assertTrue(isinstance(enc, mvk.impl.client.action.Function))

        self.assertEquals(enc.name, StringValue("f"))
        self.assertEquals(enc.location, StringValue("test.test_model.f"))
        self.assertEquals(enc.the_type, StringType())
        self.assertEquals(enc.parameters.len(), IntegerValue(2))

        # Check parameter a
        a = enc.parameters[IntegerValue(0)]
        self.assertTrue(isinstance(a, mvk.impl.client.action.Parameter))
        self.assertEquals(a.name, StringValue("a"))
        self.assertEquals(a.location, LocationValue("test.test_model.f.a"))
        self.assertEquals(a.param_type, StringValue("in"))
        self.assertEquals(a.the_type, IntegerType())

        # Identical checks for parameter b
        b = enc.parameters[IntegerValue(1)]
        self.assertTrue(isinstance(b, mvk.impl.client.action.Parameter))
        self.assertEquals(b.name, StringValue("b"))
        self.assertEquals(b.location, LocationValue("test.test_model.f.b"))
        self.assertEquals(b.param_type, StringValue("in"))
        self.assertEquals(b.the_type, FloatType())

        # Finally check the body
        body = enc.body
        self.assertTrue(isinstance(body, mvk.impl.client.action.Body))
        self.assertEquals(body.name, StringValue("body"))
        self.assertEquals(body.location, LocationValue("test.test_model.f.body"))
        self.assertEquals(body.value.len(), IntegerValue(3))

        # First part of the body
        stmt1 = body.value[IntegerValue(0)]
        self.assertTrue(isinstance(stmt1, mvk.impl.client.action.DeclarationStatement))
        self.assertEquals(stmt1.name, StringValue("decl_i"))
        self.assertEquals(stmt1.location, LocationValue("test.test_model.f.body.decl_i"))

        ident = stmt1.identifier
        self.assertTrue(isinstance(ident, mvk.impl.client.action.Identifier))
        self.assertEquals(ident.name, StringValue("i"))
        self.assertEquals(ident.location, LocationValue("test.test_model.f.body.decl_i.i"))
        self.assertEquals(ident.the_type, IntegerType())

        init = stmt1.initialization_expression
        self.assertTrue(isinstance(init, mvk.impl.client.action.Expression))
        self.assertTrue(isinstance(init, mvk.impl.client.action.Constant))
        self.assertEquals(init.name, StringValue("five"))
        self.assertEquals(init.location, LocationValue("test.test_model.f.body.decl_i.five"))
        self.assertEquals(init.value, IntegerValue(5))
        self.assertEquals(init.the_type, IntegerType())

        stmt2 = body.value[IntegerValue(1)]
        self.assertTrue(isinstance(stmt2, mvk.impl.client.action.WhileLoop))
        self.assertEquals(stmt2.name, StringValue("while_1"))
        self.assertEquals(stmt2.location, LocationValue("test.test_model.f.body.while_1"))

        test = stmt2.test
        self.assertTrue(isinstance(test, mvk.impl.client.action.Expression))
        self.assertTrue(isinstance(test, mvk.impl.client.action.GreaterThan))
        self.assertEquals(test.name, StringValue("while_1_expr"))
        self.assertEquals(test.location, LocationValue("test.test_model.f.body.while_1.while_1_expr"))
        self.assertTrue(isinstance(test.children, SequenceValue))

        child = test.children[IntegerValue(0)]
        self.assertTrue(isinstance(child, mvk.impl.client.action.Navigation))
        self.assertEquals(child.name, StringValue("i"))
        self.assertEquals(child.location, LocationValue("test.test_model.f.body.while_1.while_1_expr.i"))
        self.assertEquals(child.path, LocationValue("i"))

        child = test.children[IntegerValue(1)]
        self.assertTrue(isinstance(child, mvk.impl.client.action.Constant))
        self.assertEquals(child.name, StringValue("zero"))
        self.assertEquals(child.location, LocationValue("test.test_model.f.body.while_1.while_1_expr.zero"))
        self.assertEquals(child.value, IntegerValue(0))
        self.assertEquals(child.the_type, IntegerType())

        while_body = stmt2.body
        self.assertTrue(isinstance(while_body, mvk.impl.client.action.Body))
        self.assertEquals(while_body.name, StringValue("body"))
        self.assertEquals(while_body.location, LocationValue("test.test_model.f.body.while_1.body"))

        body_value = while_body.value
        self.assertTrue(isinstance(body_value, SequenceValue))
        self.assertTrue(body_value.len(), IntegerValue(2))

        elem = body_value[IntegerValue(0)]
        self.assertTrue(isinstance(elem, mvk.impl.client.action.ExpressionStatement))
        self.assertEquals(elem.name, StringValue("e_s_1"))
        self.assertEquals(elem.location, LocationValue("test.test_model.f.body.while_1.body.e_s_1"))
        self.assertTrue(isinstance(elem.expression, mvk.impl.client.action.Assignment))

        assignment = elem.expression
        self.assertEquals(assignment.name, StringValue("a_e_1"))
        self.assertEquals(assignment.location, LocationValue("test.test_model.f.body.while_1.body.e_s_1.a_e_1"))
        self.assertTrue(isinstance(assignment.children, SequenceValue))

        child = assignment.children[IntegerValue(0)]
        self.assertTrue(isinstance(child, mvk.impl.client.action.Identifier))
        self.assertEquals(child.name, StringValue("b"))
        self.assertEquals(child.location, LocationValue("test.test_model.f.body.while_1.body.e_s_1.a_e_1.b"))
        self.assertEquals(child.the_type, FloatType())

        child = assignment.children[IntegerValue(1)]
        self.assertTrue(isinstance(child, mvk.impl.client.action.Plus))
        self.assertEquals(child.name, StringValue("b_plus_g"))
        self.assertEquals(child.location, LocationValue("test.test_model.f.body.while_1.body.e_s_1.a_e_1.b_plus_g"))
        self.assertTrue(isinstance(child.children, SequenceValue))

        nchild = child.children[IntegerValue(0)]
        self.assertTrue(isinstance(nchild, mvk.impl.client.action.Navigation))
        self.assertEquals(nchild.name, StringValue("b"))
        self.assertEquals(nchild.location, LocationValue("test.test_model.f.body.while_1.body.e_s_1.a_e_1.b_plus_g.b"))
        self.assertEquals(nchild.path, LocationValue("b"))

        nchild = child.children[IntegerValue(1)]
        self.assertTrue(isinstance(nchild, mvk.impl.client.action.FunctionCall))
        self.assertEquals(nchild.name, StringValue("g"))
        self.assertEquals(nchild.location, LocationValue("test.test_model.f.body.while_1.body.e_s_1.a_e_1.b_plus_g.g"))
        self.assertEquals(nchild.function, StringValue("g"))
        self.assertTrue(isinstance(nchild.arguments, SequenceValue))
        
        arg = nchild.arguments[IntegerValue(0)]
        self.assertTrue(isinstance(arg, mvk.impl.client.action.Argument))
        self.assertEquals(arg.name, StringValue("c"))
        self.assertEquals(arg.location, LocationValue("test.test_model.f.body.while_1.body.e_s_1.a_e_1.b_plus_g.g.c"))
        self.assertEquals(arg.key, StringValue("c"))

        expr = arg.expression
        self.assertTrue(isinstance(expr, mvk.impl.client.action.Constant))
        self.assertEquals(expr.name, StringValue("five"))
        self.assertEquals(expr.location, LocationValue("test.test_model.f.body.while_1.body.e_s_1.a_e_1.b_plus_g.g.c.five"))
        self.assertEquals(expr.value, IntegerValue(5))
        self.assertEquals(expr.the_type, IntegerType())

        self.assertTrue(isinstance(nchild.called_expression, mvk.impl.client.action.Expression))

        elem = body_value[IntegerValue(1)]
        self.assertTrue(isinstance(elem, mvk.impl.client.action.ExpressionStatement))

        stmt3 = body.value[IntegerValue(2)]
        self.assertTrue(isinstance(stmt3, mvk.impl.client.action.IfStatement))

#if __name__ == "__main__":
def runTests():
    unittest.main()
