'''
Created on 11-mrt.-2014

@author: Simon
'''
import unittest

from mvk.impl.python.constants import CreateConstants
from mvk.impl.python.datatype import TypeFactory, StringType, BooleanType, \
    TypeType, AnyType, IntegerType
from mvk.impl.python.datavalue import MappingValue, LocationValue, StringValue, \
    IntegerValue, BooleanValue, SequenceValue, InfiniteValue, AnyValue
from mvk.impl.python.python_representer import PythonRepresenter
from mvk.mvk import MvK
from mvk.plugins.transformation.algorithm import get_matches


class MatchTestCase(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName=methodName)
        self.mvk = MvK()

    def assert_lists_eq_items(self, l1, l2):
        self.assertEqual(len(l1), len(l2))
        for i in l1:
            self.assertTrue(i in l2)

    def setUp(self):
        unittest.TestCase.setUp(self)
        cl = self.mvk.clear()
        assert cl.is_success(), cl

    def tearDown(self):
        cl = self.mvk.clear()
        assert cl.is_success()
        unittest.TestCase.tearDown(self)

    def test_smoke(self):
        ''' create test type model '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('TestTM')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestTM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('A'),
                                                                                    StringValue('Class.is_abstract'): BooleanValue(False),
                                                                                    StringValue('Class.id_field'): StringValue('A.name')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestTM.A'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                                    StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                                    StringValue('Attribute.default'): StringValue('')})
                                           })
                             )
        self.assertTrue(cl.is_success())

        ''' RAMify '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('MTpre_TestTM')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.MTpre_TestTM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('MTpre_A'),
                                                                                    StringValue('Class.is_abstract'): BooleanValue(False)
                                                                                    })
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.MTpre_TestTM.MTpre_A'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MTpre_name'),
                                                                                    StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                                    StringValue('Attribute.default'): StringValue('True')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.MTpre_TestTM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('a_i_el'),
                                                                                    StringValue('from_class'): LocationValue('formalisms.MTpre_TestTM.MTpre_A'),
                                                                                    StringValue('to_class'): LocationValue('protected.formalisms.Rule.MTpre_Element')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)

        ''' create test model '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.TestTM'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('TestTM.name'): StringValue('TestM')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.TestTM.A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.TestM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('A.name'): StringValue('a1')})
                                           })
                             )
        self.assertTrue(cl.is_success())

        ''' create test rule '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Rule.name'): StringValue('TestRule')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule.LHS'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MTpre_Pattern.pattern_name'): StringValue('lhs')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.MTpre_TestTM.MTpre_A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MT_Element.MT_label'): StringValue('a_inst'),
                                                                                    StringValue('MT_Element.id'): StringValue('a_inst')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule.MTpre_Contents'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MTpre_Contents.id'): StringValue('lhs_to_a_inst'),
                                                                                    StringValue('from_pattern'): LocationValue('rules.TestRule.lhs'),
                                                                                    StringValue('to_el'): LocationValue('rules.TestRule.a_inst')})
                                           })
                             )
        self.assertTrue(cl.is_success())

        ''' create test transformation '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Transformation'),
                                           CreateConstants.LOCATION_KEY: LocationValue('transformations'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Transformation.name'): StringValue('TestTransformation')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Transformation.Rule'),
                                           CreateConstants.LOCATION_KEY: LocationValue('transformations.TestTransformation'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Rule.rule_loc'): LocationValue('rules.TestRule'),
                                                                                    StringValue('Rule.id'): StringValue('rule_1')})
                                           })
                             )

        ''' get all matches '''
        self.assertEqual(get_matches(model_location=LocationValue('models.TestM'),
                                     transformation_location=LocationValue('transformations.TestTransformation')),
                         {StringValue('TestRule'): [{StringValue('a_inst'): MvK().read(LocationValue('models.TestM.a1')).get_item()}]})

    def test_multiple_matches(self):
        ''' create test type model '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('TestTM')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestTM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('A'),
                                                                                    StringValue('Class.is_abstract'): BooleanValue(False),
                                                                                    StringValue('Class.id_field'): StringValue('A.name')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestTM.A'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                                    StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                                    StringValue('Attribute.default'): StringValue('')})
                                           })
                             )
        self.assertTrue(cl.is_success())

        ''' RAMify '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('MTpre_TestTM')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.MTpre_TestTM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('MTpre_A'),
                                                                                    StringValue('Class.is_abstract'): BooleanValue(False)
                                                                                    })
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.MTpre_TestTM.MTpre_A'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MTpre_name'),
                                                                                    StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                                    StringValue('Attribute.default'): StringValue('True')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.MTpre_TestTM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('a_i_el'),
                                                                                    StringValue('from_class'): LocationValue('formalisms.MTpre_TestTM.MTpre_A'),
                                                                                    StringValue('to_class'): LocationValue('protected.formalisms.Rule.MTpre_Element')})
                                           })
                             )
        self.assertTrue(cl.is_success())

        ''' create test model '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.TestTM'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('TestTM.name'): StringValue('TestM')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.TestTM.A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.TestM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('A.name'): StringValue('a1')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.TestTM.A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.TestM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('A.name'): StringValue('a2')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.TestTM.A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.TestM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('A.name'): StringValue('a3')})
                                           })
                             )
        self.assertTrue(cl.is_success())

        ''' create test rule '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Rule.name'): StringValue('TestRule')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule.LHS'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MTpre_Pattern.pattern_name'): StringValue('lhs')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.MTpre_TestTM.MTpre_A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MT_Element.MT_label'): StringValue('a_inst'),
                                                                                    StringValue('MT_Element.id'): StringValue('a_inst')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule.MTpre_Contents'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MTpre_Contents.id'): StringValue('lhs_to_a_inst'),
                                                                                    StringValue('from_pattern'): LocationValue('rules.TestRule.lhs'),
                                                                                    StringValue('to_el'): LocationValue('rules.TestRule.a_inst')})
                                           })
                             )
        self.assertTrue(cl.is_success())

        ''' create test transformation '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Transformation'),
                                           CreateConstants.LOCATION_KEY: LocationValue('transformations'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Transformation.name'): StringValue('TestTransformation')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Transformation.Rule'),
                                           CreateConstants.LOCATION_KEY: LocationValue('transformations.TestTransformation'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Rule.rule_loc'): LocationValue('rules.TestRule'),
                                                                                    StringValue('Rule.id'): StringValue('rule_1')})
                                           })
                             )

        ''' get all matches '''
        self.assert_lists_eq_items(get_matches(model_location=LocationValue('models.TestM'),
                                               transformation_location=LocationValue('transformations.TestTransformation')),
                                   {StringValue('TestRule'): [{StringValue('a_inst'): MvK().read(LocationValue('models.TestM.a1')).get_item()},
                                                              {StringValue('a_inst'): MvK().read(LocationValue('models.TestM.a2')).get_item()},
                                                              {StringValue('a_inst'): MvK().read(LocationValue('models.TestM.a3')).get_item()}]})

    def test_association(self):
        ''' create test type model '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('TestTM')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestTM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('A'),
                                                                                    StringValue('Class.is_abstract'): BooleanValue(False),
                                                                                    StringValue('Class.id_field'): StringValue('A.name')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestTM.A'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                                    StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                                    StringValue('Attribute.default'): StringValue('')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Association'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestTM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('from_class'): LocationValue('formalisms.TestTM.A'),
                                                                                    StringValue('to_class'): LocationValue('formalisms.TestTM.A'),
                                                                                    StringValue('Class.name'): StringValue('A_to_A'),
                                                                                    StringValue('Class.is_abstract'): BooleanValue(False),
                                                                                    StringValue('Class.id_field'): StringValue('A_to_A.name'),
                                                                                    StringValue('Association.from_min'): IntegerValue(0),
                                                                                    StringValue('Association.from_max'): InfiniteValue('+'),
                                                                                    StringValue('Association.from_port'): StringValue('from_a'),
                                                                                    StringValue('Association.to_min'): IntegerValue(0),
                                                                                    StringValue('Association.to_max'): InfiniteValue('+'),
                                                                                    StringValue('Association.to_port'): StringValue('to_a')
                                                                                    })
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestTM.A_to_A'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                                    StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                                    StringValue('Attribute.default'): StringValue('')})
                                           })
                             )
        self.assertTrue(cl.is_success())

        ''' RAMify '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('MTpre_TestTM')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.MTpre_TestTM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('MTpre_A'),
                                                                                    StringValue('Class.is_abstract'): BooleanValue(False)
                                                                                    })
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.MTpre_TestTM.MTpre_A'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MTpre_name'),
                                                                                    StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                                    StringValue('Attribute.default'): StringValue('True')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.MTpre_TestTM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('a_i_el'),
                                                                                    StringValue('from_class'): LocationValue('formalisms.MTpre_TestTM.MTpre_A'),
                                                                                    StringValue('to_class'): LocationValue('protected.formalisms.Rule.MTpre_Element')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Association'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.MTpre_TestTM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('from_class'): LocationValue('formalisms.MTpre_TestTM.MTpre_A'),
                                                                                    StringValue('to_class'): LocationValue('formalisms.MTpre_TestTM.MTpre_A'),
                                                                                    StringValue('Class.name'): StringValue('MTpre_A_to_A'),
                                                                                    StringValue('Class.is_abstract'): BooleanValue(False),
                                                                                    StringValue('Association.from_min'): IntegerValue(0),
                                                                                    StringValue('Association.from_max'): InfiniteValue('+'),
                                                                                    StringValue('Association.from_port'): StringValue('from_a'),
                                                                                    StringValue('Association.to_min'): IntegerValue(0),
                                                                                    StringValue('Association.to_max'): InfiniteValue('+'),
                                                                                    StringValue('Association.to_port'): StringValue('to_a')
                                                                                    })
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.MTpre_TestTM.MTpre_A_to_A'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MTpre_name'),
                                                                                    StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                                    StringValue('Attribute.default'): StringValue('True')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.MTpre_TestTM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('a_to_a_i_assoc'),
                                                                                    StringValue('from_class'): LocationValue('formalisms.MTpre_TestTM.MTpre_A_to_A'),
                                                                                    StringValue('to_class'): LocationValue('protected.formalisms.Rule.MTpre_Association')})
                                           })
                             )
        self.assertTrue(cl.is_success())

        ''' create test model '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.TestTM'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('TestTM.name'): StringValue('TestM')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.TestTM.A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.TestM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('A.name'): StringValue('a1')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.TestTM.A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.TestM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('A.name'): StringValue('a2')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.TestTM.A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.TestM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('A.name'): StringValue('a3')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.TestTM.A_to_A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.TestM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('A_to_A.name'): StringValue('a1_to_a2'),
                                                                                    StringValue('from_a'): LocationValue('models.TestM.a1'),
                                                                                    StringValue('to_a'): LocationValue('models.TestM.a2')
                                                                                    })
                                          })
                             )
        self.assertTrue(cl.is_success())

        ''' create test rule '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Rule.name'): StringValue('TestRule')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule.LHS'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MTpre_Pattern.pattern_name'): StringValue('lhs')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.MTpre_TestTM.MTpre_A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MT_Element.MT_label'): StringValue('a_inst_1'),
                                                                                    StringValue('MT_Element.id'): StringValue('a_inst_1')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule.MTpre_Contents'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MTpre_Contents.id'): StringValue('lhs_to_a_inst_1'),
                                                                                    StringValue('from_pattern'): LocationValue('rules.TestRule.lhs'),
                                                                                    StringValue('to_el'): LocationValue('rules.TestRule.a_inst_1')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.MTpre_TestTM.MTpre_A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MT_Element.MT_label'): StringValue('a_inst_2'),
                                                                                    StringValue('MT_Element.id'): StringValue('a_inst_2')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule.MTpre_Contents'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MTpre_Contents.id'): StringValue('lhs_to_a_inst_2'),
                                                                                    StringValue('from_pattern'): LocationValue('rules.TestRule.lhs'),
                                                                                    StringValue('to_el'): LocationValue('rules.TestRule.a_inst_2')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.MTpre_TestTM.MTpre_A_to_A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MT_Element.MT_label'): StringValue('a_to_a_inst'),
                                                                                    StringValue('MT_Element.id'): StringValue('a_to_a_inst'),
                                                                                    StringValue('from_a'): LocationValue('rules.TestRule.a_inst_1'),
                                                                                    StringValue('to_a'): LocationValue('rules.TestRule.a_inst_2')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule.MTpre_Contents'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MTpre_Contents.id'): StringValue('lhs_to_a_to_a_inst'),
                                                                                    StringValue('from_pattern'): LocationValue('rules.TestRule.lhs'),
                                                                                    StringValue('to_el'): LocationValue('rules.TestRule.a_to_a_inst')})
                                           })
                             )
        self.assertTrue(cl.is_success())

        ''' create test transformation '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Transformation'),
                                           CreateConstants.LOCATION_KEY: LocationValue('transformations'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Transformation.name'): StringValue('TestTransformation')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Transformation.Rule'),
                                           CreateConstants.LOCATION_KEY: LocationValue('transformations.TestTransformation'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Rule.rule_loc'): LocationValue('rules.TestRule'),
                                                                                    StringValue('Rule.id'): StringValue('rule_1')})
                                           })
                             )

        ''' get all matches '''
        self.assertEqual(get_matches(model_location=LocationValue('models.TestM'),
                                     transformation_location=LocationValue('transformations.TestTransformation')),
                         {StringValue('TestRule'): [{StringValue('a_inst_1'): MvK().read(LocationValue('models.TestM.a1')).get_item(),
                                                     StringValue('a_inst_2'): MvK().read(LocationValue('models.TestM.a2')).get_item(),
                                                     StringValue('a_to_a_inst'): MvK().read(LocationValue('models.TestM.a1_to_a2')).get_item()}]})

    def test_triangle(self):
        ''' create test type model '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('TestTM')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestTM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('A'),
                                                                                    StringValue('Class.is_abstract'): BooleanValue(False),
                                                                                    StringValue('Class.id_field'): StringValue('A.name')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestTM.A'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                                    StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                                    StringValue('Attribute.default'): StringValue('')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Association'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestTM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('from_class'): LocationValue('formalisms.TestTM.A'),
                                                                                    StringValue('to_class'): LocationValue('formalisms.TestTM.A'),
                                                                                    StringValue('Class.name'): StringValue('A_to_A'),
                                                                                    StringValue('Class.is_abstract'): BooleanValue(False),
                                                                                    StringValue('Class.id_field'): StringValue('A_to_A.name'),
                                                                                    StringValue('Association.from_min'): IntegerValue(0),
                                                                                    StringValue('Association.from_max'): InfiniteValue('+'),
                                                                                    StringValue('Association.from_port'): StringValue('from_a'),
                                                                                    StringValue('Association.to_min'): IntegerValue(0),
                                                                                    StringValue('Association.to_max'): InfiniteValue('+'),
                                                                                    StringValue('Association.to_port'): StringValue('to_a')
                                                                                    })
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestTM.A_to_A'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                                    StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                                    StringValue('Attribute.default'): StringValue('')})
                                           })
                             )
        self.assertTrue(cl.is_success())

        ''' RAMify '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('MTpre_TestTM')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.MTpre_TestTM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('MTpre_A'),
                                                                                    StringValue('Class.is_abstract'): BooleanValue(False)
                                                                                    })
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.MTpre_TestTM.MTpre_A'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MTpre_name'),
                                                                                    StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                                    StringValue('Attribute.default'): StringValue('True')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.MTpre_TestTM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('a_i_el'),
                                                                                    StringValue('from_class'): LocationValue('formalisms.MTpre_TestTM.MTpre_A'),
                                                                                    StringValue('to_class'): LocationValue('protected.formalisms.Rule.MTpre_Element')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Association'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.MTpre_TestTM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('from_class'): LocationValue('formalisms.MTpre_TestTM.MTpre_A'),
                                                                                    StringValue('to_class'): LocationValue('formalisms.MTpre_TestTM.MTpre_A'),
                                                                                    StringValue('Class.name'): StringValue('MTpre_A_to_A'),
                                                                                    StringValue('Class.is_abstract'): BooleanValue(False),
                                                                                    StringValue('Association.from_min'): IntegerValue(0),
                                                                                    StringValue('Association.from_max'): InfiniteValue('+'),
                                                                                    StringValue('Association.from_port'): StringValue('from_a'),
                                                                                    StringValue('Association.to_min'): IntegerValue(0),
                                                                                    StringValue('Association.to_max'): InfiniteValue('+'),
                                                                                    StringValue('Association.to_port'): StringValue('to_a')
                                                                                    })
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.MTpre_TestTM.MTpre_A_to_A'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MTpre_name'),
                                                                                    StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                                    StringValue('Attribute.default'): StringValue('True')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.MTpre_TestTM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('a_to_a_i_assoc'),
                                                                                    StringValue('from_class'): LocationValue('formalisms.MTpre_TestTM.MTpre_A_to_A'),
                                                                                    StringValue('to_class'): LocationValue('protected.formalisms.Rule.MTpre_Association')})
                                           })
                             )
        self.assertTrue(cl.is_success())

        ''' create test model '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.TestTM'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('TestTM.name'): StringValue('TestM')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.TestTM.A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.TestM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('A.name'): StringValue('a1')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.TestTM.A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.TestM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('A.name'): StringValue('a2')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.TestTM.A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.TestM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('A.name'): StringValue('a3')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.TestTM.A_to_A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.TestM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('A_to_A.name'): StringValue('a1_to_a2'),
                                                                                    StringValue('from_a'): LocationValue('models.TestM.a1'),
                                                                                    StringValue('to_a'): LocationValue('models.TestM.a2')
                                                                                    })
                                          })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.TestTM.A_to_A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.TestM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('A_to_A.name'): StringValue('a2_to_a3'),
                                                                                    StringValue('from_a'): LocationValue('models.TestM.a2'),
                                                                                    StringValue('to_a'): LocationValue('models.TestM.a3')
                                                                                    })
                                          })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.TestTM.A_to_A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.TestM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('A_to_A.name'): StringValue('a3_to_a1'),
                                                                                    StringValue('from_a'): LocationValue('models.TestM.a3'),
                                                                                    StringValue('to_a'): LocationValue('models.TestM.a1')
                                                                                    })
                                          })
                             )
        self.assertTrue(cl.is_success())

        ''' create test rule '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Rule.name'): StringValue('TestRule')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule.LHS'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MTpre_Pattern.pattern_name'): StringValue('lhs')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.MTpre_TestTM.MTpre_A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MT_Element.MT_label'): StringValue('a_inst_1'),
                                                                                    StringValue('MT_Element.id'): StringValue('a_inst_1')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule.MTpre_Contents'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MTpre_Contents.id'): StringValue('lhs_to_a_inst_1'),
                                                                                    StringValue('from_pattern'): LocationValue('rules.TestRule.lhs'),
                                                                                    StringValue('to_el'): LocationValue('rules.TestRule.a_inst_1')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.MTpre_TestTM.MTpre_A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MT_Element.MT_label'): StringValue('a_inst_2'),
                                                                                    StringValue('MT_Element.id'): StringValue('a_inst_2')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule.MTpre_Contents'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MTpre_Contents.id'): StringValue('lhs_to_a_inst_2'),
                                                                                    StringValue('from_pattern'): LocationValue('rules.TestRule.lhs'),
                                                                                    StringValue('to_el'): LocationValue('rules.TestRule.a_inst_2')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.MTpre_TestTM.MTpre_A_to_A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MT_Element.MT_label'): StringValue('a_to_a_inst'),
                                                                                    StringValue('MT_Element.id'): StringValue('a_to_a_inst'),
                                                                                    StringValue('from_a'): LocationValue('rules.TestRule.a_inst_1'),
                                                                                    StringValue('to_a'): LocationValue('rules.TestRule.a_inst_2')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule.MTpre_Contents'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MTpre_Contents.id'): StringValue('lhs_to_a_to_a_inst'),
                                                                                    StringValue('from_pattern'): LocationValue('rules.TestRule.lhs'),
                                                                                    StringValue('to_el'): LocationValue('rules.TestRule.a_to_a_inst')})
                                           })
                             )
        self.assertTrue(cl.is_success())

        ''' create test transformation '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Transformation'),
                                           CreateConstants.LOCATION_KEY: LocationValue('transformations'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Transformation.name'): StringValue('TestTransformation')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Transformation.Rule'),
                                           CreateConstants.LOCATION_KEY: LocationValue('transformations.TestTransformation'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Rule.rule_loc'): LocationValue('rules.TestRule'),
                                                                                    StringValue('Rule.id'): StringValue('rule_1')})
                                           })
                             )

        ''' get all matches '''
        self.assert_lists_eq_items(get_matches(model_location=LocationValue('models.TestM'),
                                               transformation_location=LocationValue('transformations.TestTransformation')),
                                   {StringValue('TestRule'): [{StringValue('a_inst_1'): MvK().read(LocationValue('models.TestM.a1')).get_item(),
                                                               StringValue('a_inst_2'): MvK().read(LocationValue('models.TestM.a2')).get_item(),
                                                               StringValue('a_to_a_inst'): MvK().read(LocationValue('models.TestM.a1_to_a2')).get_item()},
                                                              {StringValue('a_inst_1'): MvK().read(LocationValue('models.TestM.a2')).get_item(),
                                                               StringValue('a_inst_2'): MvK().read(LocationValue('models.TestM.a3')).get_item(),
                                                               StringValue('a_to_a_inst'): MvK().read(LocationValue('models.TestM.a2_to_a3')).get_item()},
                                                              {StringValue('a_inst_1'): MvK().read(LocationValue('models.TestM.a3')).get_item(),
                                                               StringValue('a_inst_2'): MvK().read(LocationValue('models.TestM.a1')).get_item(),
                                                               StringValue('a_to_a_inst'): MvK().read(LocationValue('models.TestM.a3_to_a1')).get_item()}]})

    def test_triangle_multiple(self):
        ''' create test type model '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('TestTM')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestTM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('A'),
                                                                                    StringValue('Class.is_abstract'): BooleanValue(False),
                                                                                    StringValue('Class.id_field'): StringValue('A.name')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestTM.A'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                                    StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                                    StringValue('Attribute.default'): StringValue('')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Association'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestTM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('from_class'): LocationValue('formalisms.TestTM.A'),
                                                                                    StringValue('to_class'): LocationValue('formalisms.TestTM.A'),
                                                                                    StringValue('Class.name'): StringValue('A_to_A'),
                                                                                    StringValue('Class.is_abstract'): BooleanValue(False),
                                                                                    StringValue('Class.id_field'): StringValue('A_to_A.name'),
                                                                                    StringValue('Association.from_min'): IntegerValue(0),
                                                                                    StringValue('Association.from_max'): InfiniteValue('+'),
                                                                                    StringValue('Association.from_port'): StringValue('from_a'),
                                                                                    StringValue('Association.to_min'): IntegerValue(0),
                                                                                    StringValue('Association.to_max'): InfiniteValue('+'),
                                                                                    StringValue('Association.to_port'): StringValue('to_a')
                                                                                    })
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestTM.A_to_A'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                                    StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                                    StringValue('Attribute.default'): StringValue('')})
                                           })
                             )
        self.assertTrue(cl.is_success())

        ''' RAMify '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('MTpre_TestTM')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.MTpre_TestTM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('MTpre_A'),
                                                                                    StringValue('Class.is_abstract'): BooleanValue(False)
                                                                                    })
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.MTpre_TestTM.MTpre_A'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MTpre_name'),
                                                                                    StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                                    StringValue('Attribute.default'): StringValue('True')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.MTpre_TestTM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('a_i_el'),
                                                                                    StringValue('from_class'): LocationValue('formalisms.MTpre_TestTM.MTpre_A'),
                                                                                    StringValue('to_class'): LocationValue('protected.formalisms.Rule.MTpre_Element')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Association'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.MTpre_TestTM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('from_class'): LocationValue('formalisms.MTpre_TestTM.MTpre_A'),
                                                                                    StringValue('to_class'): LocationValue('formalisms.MTpre_TestTM.MTpre_A'),
                                                                                    StringValue('Class.name'): StringValue('MTpre_A_to_A'),
                                                                                    StringValue('Class.is_abstract'): BooleanValue(False),
                                                                                    StringValue('Association.from_min'): IntegerValue(0),
                                                                                    StringValue('Association.from_max'): InfiniteValue('+'),
                                                                                    StringValue('Association.from_port'): StringValue('from_a'),
                                                                                    StringValue('Association.to_min'): IntegerValue(0),
                                                                                    StringValue('Association.to_max'): InfiniteValue('+'),
                                                                                    StringValue('Association.to_port'): StringValue('to_a')
                                                                                    })
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.MTpre_TestTM.MTpre_A_to_A'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MTpre_name'),
                                                                                    StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                                    StringValue('Attribute.default'): StringValue('True')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.MTpre_TestTM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('a_to_a_i_assoc'),
                                                                                    StringValue('from_class'): LocationValue('formalisms.MTpre_TestTM.MTpre_A_to_A'),
                                                                                    StringValue('to_class'): LocationValue('protected.formalisms.Rule.MTpre_Association')})
                                           })
                             )
        self.assertTrue(cl.is_success())

        ''' create test model '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.TestTM'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('TestTM.name'): StringValue('TestM')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.TestTM.A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.TestM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('A.name'): StringValue('a1')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.TestTM.A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.TestM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('A.name'): StringValue('a2')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.TestTM.A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.TestM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('A.name'): StringValue('a3')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.TestTM.A_to_A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.TestM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('A_to_A.name'): StringValue('a1_to_a2'),
                                                                                    StringValue('from_a'): LocationValue('models.TestM.a1'),
                                                                                    StringValue('to_a'): LocationValue('models.TestM.a2')
                                                                                    })
                                          })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.TestTM.A_to_A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.TestM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('A_to_A.name'): StringValue('a2_to_a1'),
                                                                                    StringValue('from_a'): LocationValue('models.TestM.a2'),
                                                                                    StringValue('to_a'): LocationValue('models.TestM.a1')
                                                                                    })
                                          })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.TestTM.A_to_A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.TestM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('A_to_A.name'): StringValue('a2_to_a3'),
                                                                                    StringValue('from_a'): LocationValue('models.TestM.a2'),
                                                                                    StringValue('to_a'): LocationValue('models.TestM.a3')
                                                                                    })
                                          })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.TestTM.A_to_A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.TestM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('A_to_A.name'): StringValue('a2_to_a2'),
                                                                                    StringValue('from_a'): LocationValue('models.TestM.a2'),
                                                                                    StringValue('to_a'): LocationValue('models.TestM.a2')
                                                                                    })
                                          })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.TestTM.A_to_A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.TestM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('A_to_A.name'): StringValue('a3_to_a1'),
                                                                                    StringValue('from_a'): LocationValue('models.TestM.a3'),
                                                                                    StringValue('to_a'): LocationValue('models.TestM.a1')
                                                                                    })
                                          })
                             )
        self.assertTrue(cl.is_success())

        ''' create test rule '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Rule.name'): StringValue('TestRule')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule.LHS'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MTpre_Pattern.pattern_name'): StringValue('lhs')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.MTpre_TestTM.MTpre_A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MT_Element.MT_label'): StringValue('a_inst_1'),
                                                                                    StringValue('MT_Element.id'): StringValue('a_inst_1')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule.MTpre_Contents'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MTpre_Contents.id'): StringValue('lhs_to_a_inst_1'),
                                                                                    StringValue('from_pattern'): LocationValue('rules.TestRule.lhs'),
                                                                                    StringValue('to_el'): LocationValue('rules.TestRule.a_inst_1')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.MTpre_TestTM.MTpre_A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MT_Element.MT_label'): StringValue('a_inst_2'),
                                                                                    StringValue('MT_Element.id'): StringValue('a_inst_2')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule.MTpre_Contents'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MTpre_Contents.id'): StringValue('lhs_to_a_inst_2'),
                                                                                    StringValue('from_pattern'): LocationValue('rules.TestRule.lhs'),
                                                                                    StringValue('to_el'): LocationValue('rules.TestRule.a_inst_2')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.MTpre_TestTM.MTpre_A_to_A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MT_Element.MT_label'): StringValue('a_to_a_inst'),
                                                                                    StringValue('MT_Element.id'): StringValue('a_to_a_inst'),
                                                                                    StringValue('from_a'): LocationValue('rules.TestRule.a_inst_1'),
                                                                                    StringValue('to_a'): LocationValue('rules.TestRule.a_inst_2')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule.MTpre_Contents'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MTpre_Contents.id'): StringValue('lhs_to_a_to_a_inst'),
                                                                                    StringValue('from_pattern'): LocationValue('rules.TestRule.lhs'),
                                                                                    StringValue('to_el'): LocationValue('rules.TestRule.a_to_a_inst')})
                                           })
                             )
        self.assertTrue(cl.is_success())

        ''' create test transformation '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Transformation'),
                                           CreateConstants.LOCATION_KEY: LocationValue('transformations'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Transformation.name'): StringValue('TestTransformation')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Transformation.Rule'),
                                           CreateConstants.LOCATION_KEY: LocationValue('transformations.TestTransformation'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Rule.rule_loc'): LocationValue('rules.TestRule'),
                                                                                    StringValue('Rule.id'): StringValue('rule_1')})
                                           })
                             )

        ''' get all matches '''
        self.assert_lists_eq_items(get_matches(model_location=LocationValue('models.TestM'),
                                               transformation_location=LocationValue('transformations.TestTransformation')),
                                   {StringValue('TestRule'): [{StringValue('a_inst_1'): MvK().read(LocationValue('models.TestM.a1')).get_item(),
                                                               StringValue('a_inst_2'): MvK().read(LocationValue('models.TestM.a2')).get_item(),
                                                               StringValue('a_to_a_inst'): MvK().read(LocationValue('models.TestM.a1_to_a2')).get_item()},
                                                              {StringValue('a_inst_1'): MvK().read(LocationValue('models.TestM.a2')).get_item(),
                                                               StringValue('a_inst_2'): MvK().read(LocationValue('models.TestM.a3')).get_item(),
                                                               StringValue('a_to_a_inst'): MvK().read(LocationValue('models.TestM.a2_to_a3')).get_item()},
                                                              {StringValue('a_inst_1'): MvK().read(LocationValue('models.TestM.a3')).get_item(),
                                                               StringValue('a_inst_2'): MvK().read(LocationValue('models.TestM.a1')).get_item(),
                                                               StringValue('a_to_a_inst'): MvK().read(LocationValue('models.TestM.a3_to_a1')).get_item()},
                                                              {StringValue('a_inst_1'): MvK().read(LocationValue('models.TestM.a2')).get_item(),
                                                               StringValue('a_inst_2'): MvK().read(LocationValue('models.TestM.a1')).get_item(),
                                                               StringValue('a_to_a_inst'): MvK().read(LocationValue('models.TestM.a2_to_a1')).get_item()},
                                                              {StringValue('a_inst_1'): MvK().read(LocationValue('models.TestM.a2')).get_item(),
                                                               StringValue('a_inst_2'): MvK().read(LocationValue('models.TestM.a2')).get_item(),
                                                               StringValue('a_to_a_inst'): MvK().read(LocationValue('models.TestM.a2_to_a2')).get_item()}]})

    def test_nac(self):
        ''' create test type model '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('TestTM')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestTM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('A'),
                                                                                    StringValue('Class.is_abstract'): BooleanValue(False),
                                                                                    StringValue('Class.id_field'): StringValue('A.name')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestTM.A'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                                    StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                                    StringValue('Attribute.default'): StringValue('')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Association'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestTM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('from_class'): LocationValue('formalisms.TestTM.A'),
                                                                                    StringValue('to_class'): LocationValue('formalisms.TestTM.A'),
                                                                                    StringValue('Class.name'): StringValue('A_to_A'),
                                                                                    StringValue('Class.is_abstract'): BooleanValue(False),
                                                                                    StringValue('Class.id_field'): StringValue('A_to_A.name'),
                                                                                    StringValue('Association.from_min'): IntegerValue(0),
                                                                                    StringValue('Association.from_max'): InfiniteValue('+'),
                                                                                    StringValue('Association.from_port'): StringValue('from_a'),
                                                                                    StringValue('Association.to_min'): IntegerValue(0),
                                                                                    StringValue('Association.to_max'): InfiniteValue('+'),
                                                                                    StringValue('Association.to_port'): StringValue('to_a')
                                                                                    })
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestTM.A_to_A'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                                    StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                                    StringValue('Attribute.default'): StringValue('')})
                                           })
                             )
        self.assertTrue(cl.is_success())

        ''' RAMify '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('MTpre_TestTM')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.MTpre_TestTM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('MTpre_A'),
                                                                                    StringValue('Class.is_abstract'): BooleanValue(False)
                                                                                    })
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.MTpre_TestTM.MTpre_A'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MTpre_name'),
                                                                                    StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                                    StringValue('Attribute.default'): StringValue('True')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.MTpre_TestTM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('a_i_el'),
                                                                                    StringValue('from_class'): LocationValue('formalisms.MTpre_TestTM.MTpre_A'),
                                                                                    StringValue('to_class'): LocationValue('protected.formalisms.Rule.MTpre_Element')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Association'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.MTpre_TestTM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('from_class'): LocationValue('formalisms.MTpre_TestTM.MTpre_A'),
                                                                                    StringValue('to_class'): LocationValue('formalisms.MTpre_TestTM.MTpre_A'),
                                                                                    StringValue('Class.name'): StringValue('MTpre_A_to_A'),
                                                                                    StringValue('Class.is_abstract'): BooleanValue(False),
                                                                                    StringValue('Association.from_min'): IntegerValue(0),
                                                                                    StringValue('Association.from_max'): InfiniteValue('+'),
                                                                                    StringValue('Association.from_port'): StringValue('from_a'),
                                                                                    StringValue('Association.to_min'): IntegerValue(0),
                                                                                    StringValue('Association.to_max'): InfiniteValue('+'),
                                                                                    StringValue('Association.to_port'): StringValue('to_a')
                                                                                    })
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.MTpre_TestTM.MTpre_A_to_A'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MTpre_name'),
                                                                                    StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                                    StringValue('Attribute.default'): StringValue('True')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.MTpre_TestTM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('a_to_a_i_assoc'),
                                                                                    StringValue('from_class'): LocationValue('formalisms.MTpre_TestTM.MTpre_A_to_A'),
                                                                                    StringValue('to_class'): LocationValue('protected.formalisms.Rule.MTpre_Association')})
                                           })
                             )
        self.assertTrue(cl.is_success())

        ''' create test model '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.TestTM'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('TestTM.name'): StringValue('TestM')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.TestTM.A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.TestM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('A.name'): StringValue('a1')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.TestTM.A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.TestM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('A.name'): StringValue('a2')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.TestTM.A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.TestM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('A.name'): StringValue('a3')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.TestTM.A_to_A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.TestM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('A_to_A.name'): StringValue('a1_to_a2'),
                                                                                    StringValue('from_a'): LocationValue('models.TestM.a1'),
                                                                                    StringValue('to_a'): LocationValue('models.TestM.a2')
                                                                                    })
                                          })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.TestTM.A_to_A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.TestM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('A_to_A.name'): StringValue('a2_to_a1'),
                                                                                    StringValue('from_a'): LocationValue('models.TestM.a2'),
                                                                                    StringValue('to_a'): LocationValue('models.TestM.a1')
                                                                                    })
                                          })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.TestTM.A_to_A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.TestM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('A_to_A.name'): StringValue('a2_to_a3'),
                                                                                    StringValue('from_a'): LocationValue('models.TestM.a2'),
                                                                                    StringValue('to_a'): LocationValue('models.TestM.a3')
                                                                                    })
                                          })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.TestTM.A_to_A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.TestM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('A_to_A.name'): StringValue('a2_to_a2'),
                                                                                    StringValue('from_a'): LocationValue('models.TestM.a2'),
                                                                                    StringValue('to_a'): LocationValue('models.TestM.a2')
                                                                                    })
                                          })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.TestTM.A_to_A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.TestM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('A_to_A.name'): StringValue('a3_to_a1'),
                                                                                    StringValue('from_a'): LocationValue('models.TestM.a3'),
                                                                                    StringValue('to_a'): LocationValue('models.TestM.a1')
                                                                                    })
                                          })
                             )
        self.assertTrue(cl.is_success())

        ''' create test rule '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Rule.name'): StringValue('TestRule')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule.LHS'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MTpre_Pattern.pattern_name'): StringValue('lhs')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.MTpre_TestTM.MTpre_A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MT_Element.MT_label'): StringValue('a_inst_1'),
                                                                                    StringValue('MT_Element.id'): StringValue('lhs_a_inst_1')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule.MTpre_Contents'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MTpre_Contents.id'): StringValue('lhs_to_lhs_a_inst_1'),
                                                                                    StringValue('from_pattern'): LocationValue('rules.TestRule.lhs'),
                                                                                    StringValue('to_el'): LocationValue('rules.TestRule.lhs_a_inst_1')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.MTpre_TestTM.MTpre_A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MT_Element.MT_label'): StringValue('a_inst_2'),
                                                                                    StringValue('MT_Element.id'): StringValue('lhs_a_inst_2')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule.MTpre_Contents'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MTpre_Contents.id'): StringValue('lhs_to_lhs_a_inst_2'),
                                                                                    StringValue('from_pattern'): LocationValue('rules.TestRule.lhs'),
                                                                                    StringValue('to_el'): LocationValue('rules.TestRule.lhs_a_inst_2')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.MTpre_TestTM.MTpre_A_to_A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MT_Element.MT_label'): StringValue('a_to_a_inst'),
                                                                                    StringValue('MT_Element.id'): StringValue('lhs_a_to_a_inst'),
                                                                                    StringValue('from_a'): LocationValue('rules.TestRule.lhs_a_inst_1'),
                                                                                    StringValue('to_a'): LocationValue('rules.TestRule.lhs_a_inst_2')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule.MTpre_Contents'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MTpre_Contents.id'): StringValue('lhs_to_a_to_a_inst'),
                                                                                    StringValue('from_pattern'): LocationValue('rules.TestRule.lhs'),
                                                                                    StringValue('to_el'): LocationValue('rules.TestRule.lhs_a_to_a_inst')})
                                           })
                             )
        self.assertTrue(cl.is_success())

        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule.NAC'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MTpre_Pattern.pattern_name'): StringValue('nac_1')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.MTpre_TestTM.MTpre_A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MT_Element.MT_label'): StringValue('a_inst_1'),
                                                                                    StringValue('MT_Element.id'): StringValue('nac_a_inst_1')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule.MTpre_Contents'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MTpre_Contents.id'): StringValue('nac_1_to_nac_a_inst_1'),
                                                                                    StringValue('from_pattern'): LocationValue('rules.TestRule.nac_1'),
                                                                                    StringValue('to_el'): LocationValue('rules.TestRule.nac_a_inst_1')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.MTpre_TestTM.MTpre_A_to_A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MT_Element.MT_label'): StringValue('a_to_a_nac'),
                                                                                    StringValue('MT_Element.id'): StringValue('a_to_a_nac'),
                                                                                    StringValue('from_a'): LocationValue('rules.TestRule.nac_a_inst_1'),
                                                                                    StringValue('to_a'): LocationValue('rules.TestRule.nac_a_inst_1')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule.MTpre_Contents'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MTpre_Contents.id'): StringValue('nac_1_to_a_to_a_nac'),
                                                                                    StringValue('from_pattern'): LocationValue('rules.TestRule.nac_1'),
                                                                                    StringValue('to_el'): LocationValue('rules.TestRule.a_to_a_nac')})
                                           })
                             )
        self.assertTrue(cl.is_success())

        ''' create test transformation '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Transformation'),
                                           CreateConstants.LOCATION_KEY: LocationValue('transformations'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Transformation.name'): StringValue('TestTransformation')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Transformation.Rule'),
                                           CreateConstants.LOCATION_KEY: LocationValue('transformations.TestTransformation'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Rule.rule_loc'): LocationValue('rules.TestRule'),
                                                                                    StringValue('Rule.id'): StringValue('rule_1')})
                                           })
                             )

        ''' get all matches '''
        self.assert_lists_eq_items(get_matches(model_location=LocationValue('models.TestM'),
                                               transformation_location=LocationValue('transformations.TestTransformation')),
                                   {StringValue('TestRule'): [{StringValue('a_inst_1'): MvK().read(LocationValue('models.TestM.a1')).get_item(),
                                                               StringValue('a_inst_2'): MvK().read(LocationValue('models.TestM.a2')).get_item(),
                                                               StringValue('a_to_a_inst'): MvK().read(LocationValue('models.TestM.a1_to_a2')).get_item()},
                                                              {StringValue('a_inst_1'): MvK().read(LocationValue('models.TestM.a3')).get_item(),
                                                               StringValue('a_inst_2'): MvK().read(LocationValue('models.TestM.a1')).get_item(),
                                                               StringValue('a_to_a_inst'): MvK().read(LocationValue('models.TestM.a3_to_a1')).get_item()}]})

if __name__ == "__main__":
    unittest.main()
