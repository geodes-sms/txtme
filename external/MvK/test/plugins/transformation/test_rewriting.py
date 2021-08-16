'''
Created on 12-mrt.-2014

@author: Simon
'''
import unittest

from mvk.impl.python.constants import CreateConstants
from mvk.impl.python.datatype import TypeFactory, IntegerType, StringType, \
    BooleanType, TypeType, AnyType
from mvk.impl.python.datavalue import MappingValue, LocationValue, StringValue, \
    IntegerValue, BooleanValue, SequenceValue, InfiniteValue, AnyValue
from mvk.impl.python.python_representer import PythonRepresenter
from mvk.mvk import MvK
from mvk.plugins.transformation.algorithm import get_matches, match_and_rewrite


class RewriteTestCase(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName=methodName)
        self.mvk = MvK()

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.mvk.clear()

    def tearDown(self):
        self.mvk.clear()
        unittest.TestCase.tearDown(self)

    def create_simple_test(self):
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
                                                                                    StringValue('Class.id_field'): StringValue('A.id')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestTM.A'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('id'),
                                                                                    StringValue('Attribute.type'): StringType(),
                                                                                    StringValue('Attribute.default'): StringValue('')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestTM.A'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('test_attr'),
                                                                                    StringValue('Attribute.type'): IntegerType(),
                                                                                    StringValue('Attribute.default'): IntegerValue(0)})
                                           })
                             )
        self.assertTrue(cl.is_success())

        ''' RAMify - pre '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('MTpre_TestTM')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.MTpre_TestTM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('MTpre_A'),
                                                                                    StringValue('Class.is_abstract'): BooleanValue(False)})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.MTpre_TestTM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('a_i_pre_el'),
                                                                                    StringValue('from_class'): LocationValue('formalisms.MTpre_TestTM.MTpre_A'),
                                                                                    StringValue('to_class'): LocationValue('protected.formalisms.Rule.MTpre_Element')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.MTpre_TestTM.MTpre_A'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MTpre_id'),
                                                                                    StringValue('Attribute.type'): StringType(),
                                                                                    StringValue('Attribute.default'): StringValue('True')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.MTpre_TestTM.MTpre_A'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MTpre_test_attr'),
                                                                                    StringValue('Attribute.type'): StringType(),
                                                                                    StringValue('Attribute.default'): StringValue('True')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)

        ''' RAMify - post '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('MTpost_TestTM')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.MTpost_TestTM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('MTpost_A'),
                                                                                    StringValue('Class.is_abstract'): BooleanValue(False)})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.MTpost_TestTM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('a_i_post_el'),
                                                                                    StringValue('from_class'): LocationValue('formalisms.MTpost_TestTM.MTpost_A'),
                                                                                    StringValue('to_class'): LocationValue('protected.formalisms.Rule.MTpost_Element')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.MTpost_TestTM.MTpost_A'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MTpost_id'),
                                                                                    StringValue('Attribute.type'): StringType(),
                                                                                    StringValue('Attribute.default'): StringValue('get_attribute()')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.MTpost_TestTM.MTpost_A'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MTpost_test_attr'),
                                                                                    StringValue('Attribute.type'): StringType(),
                                                                                    StringValue('Attribute.default'): StringValue('get_attribute()')})
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
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: PythonRepresenter.CLABJECT,
                                           CreateConstants.TYPE_KEY: LocationValue('formalisms.TestTM.A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.TestM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('A.id'): StringValue('a')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        self.assertTrue(self.mvk.read(LocationValue('models.TestM.a.A.test_attr')).is_success())

    def test_add(self):
        self.create_simple_test()
        ''' create test rule '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Rule.name'): StringValue('TestRule')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: PythonRepresenter.CLABJECT,
                                           CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule.LHS'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MTpre_Pattern.pattern_name'): StringValue('lhs')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: PythonRepresenter.CLABJECT,
                                           CreateConstants.TYPE_KEY: LocationValue('formalisms.MTpre_TestTM.MTpre_A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MT_Element.MT_label'): StringValue('a_inst'),
                                                                                    StringValue('MT_Element.id'): StringValue('lhs_a_inst')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: PythonRepresenter.ASSOCIATION,
                                           CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule.MTpre_Contents'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MTpre_Contents.id'): StringValue('lhs_to_lhs_a_inst'),
                                                                                    StringValue('from_pattern'): LocationValue('rules.TestRule.lhs'),
                                                                                    StringValue('to_el'): LocationValue('rules.TestRule.lhs_a_inst')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: PythonRepresenter.CLABJECT,
                                           CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule.RHS'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MTpost_Pattern.pattern_name'): StringValue('rhs')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: PythonRepresenter.CLABJECT,
                                           CreateConstants.TYPE_KEY: LocationValue('formalisms.MTpost_TestTM.MTpost_A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MT_Element.MT_label'): StringValue('a_inst'),
                                                                                    StringValue('MT_Element.id'): StringValue('rhs_a_inst_1')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: PythonRepresenter.ASSOCIATION,
                                           CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule.MTpost_Contents'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MTpost_Contents.id'): StringValue('rhs_to_rhs_a_inst_1'),
                                                                                    StringValue('from_pattern'): LocationValue('rules.TestRule.rhs'),
                                                                                    StringValue('to_el'): LocationValue('rules.TestRule.rhs_a_inst_1')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: PythonRepresenter.CLABJECT,
                                           CreateConstants.TYPE_KEY: LocationValue('formalisms.MTpost_TestTM.MTpost_A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MT_Element.MT_label'): StringValue('a_inst_new'),
                                                                                    StringValue('MT_Element.id'): StringValue('rhs_a_inst_2'),
                                                                                    StringValue('MTpost_A.MTpost_id'): StringValue('DataValueFactory.create_instance(\'a2\')')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: PythonRepresenter.ASSOCIATION,
                                           CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule.MTpost_Contents'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MTpost_Contents.id'): StringValue('rhs_to_rhs_a_inst_2'),
                                                                                    StringValue('from_pattern'): LocationValue('rules.TestRule.rhs'),
                                                                                    StringValue('to_el'): LocationValue('rules.TestRule.rhs_a_inst_2')})
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
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: PythonRepresenter.CLABJECT,
                                           CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Transformation.Rule'),
                                           CreateConstants.LOCATION_KEY: LocationValue('transformations.TestTransformation'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Rule.id'): StringValue('rule'),
                                                                                    StringValue('Rule.rule_loc'): LocationValue('rules.TestRule')})
                                           })
                             )

        ''' rewrite '''
        self.assertEquals(self.mvk.read(LocationValue('models.TestM')).get_item().get_elements().len(), IntegerValue(1))
        cl = match_and_rewrite(model_location=LocationValue('models.TestM'),
                               transformation_location=LocationValue('transformations.TestTransformation'))
        self.assertTrue(cl.is_success(), cl)
        self.assertEquals(self.mvk.read(LocationValue('models.TestM')).get_item().get_elements().len(), IntegerValue(2))

    def test_delete(self):
        self.create_simple_test()
        ''' create test rule '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Rule.name'): StringValue('TestRule')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: PythonRepresenter.CLABJECT,
                                           CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule.LHS'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MTpre_Pattern.pattern_name'): StringValue('lhs')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: PythonRepresenter.CLABJECT,
                                           CreateConstants.TYPE_KEY: LocationValue('formalisms.MTpre_TestTM.MTpre_A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MT_Element.MT_label'): StringValue('a_inst'),
                                                                                    StringValue('MT_Element.id'): StringValue('lhs_a_inst')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: PythonRepresenter.ASSOCIATION,
                                           CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule.MTpre_Contents'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MTpre_Contents.id'): StringValue('lhs_to_lhs_a_inst'),
                                                                                    StringValue('from_pattern'): LocationValue('rules.TestRule.lhs'),
                                                                                    StringValue('to_el'): LocationValue('rules.TestRule.lhs_a_inst')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: PythonRepresenter.CLABJECT,
                                           CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule.RHS'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MTpost_Pattern.pattern_name'): StringValue('rhs')})
                                           })
                             )

        ''' create test transformation '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Transformation'),
                                           CreateConstants.LOCATION_KEY: LocationValue('transformations'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Transformation.name'): StringValue('TestTransformation')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: PythonRepresenter.CLABJECT,
                                           CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Transformation.Rule'),
                                           CreateConstants.LOCATION_KEY: LocationValue('transformations.TestTransformation'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Rule.id'): StringValue('rule'),
                                                                                    StringValue('Rule.rule_loc'): LocationValue('rules.TestRule')})
                                           })
                             )

        ''' rewrite '''
        self.assertEquals(self.mvk.read(LocationValue('models.TestM')).get_item().get_elements().len(), IntegerValue(1))
        cl = match_and_rewrite(model_location=LocationValue('models.TestM'),
                               transformation_location=LocationValue('transformations.TestTransformation'))
        self.assertTrue(cl.is_success())
        self.assertEquals(self.mvk.read(LocationValue('models.TestM')).get_item().get_elements().len(), IntegerValue(0))

    def test_update(self):
        self.create_simple_test()
        ''' create test rule '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Rule.name'): StringValue('TestRule')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: PythonRepresenter.CLABJECT,
                                           CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule.LHS'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MTpre_Pattern.pattern_name'): StringValue('lhs')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: PythonRepresenter.CLABJECT,
                                           CreateConstants.TYPE_KEY: LocationValue('formalisms.MTpre_TestTM.MTpre_A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MT_Element.MT_label'): StringValue('a_inst'),
                                                                                    StringValue('MT_Element.id'): StringValue('lhs_a_inst')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: PythonRepresenter.ASSOCIATION,
                                           CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule.MTpre_Contents'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MTpre_Contents.id'): StringValue('lhs_to_lhs_a_inst'),
                                                                                    StringValue('from_pattern'): LocationValue('rules.TestRule.lhs'),
                                                                                    StringValue('to_el'): LocationValue('rules.TestRule.lhs_a_inst')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: PythonRepresenter.CLABJECT,
                                           CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule.RHS'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MTpost_Pattern.pattern_name'): StringValue('rhs')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: PythonRepresenter.CLABJECT,
                                           CreateConstants.TYPE_KEY: LocationValue('formalisms.MTpost_TestTM.MTpost_A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MT_Element.MT_label'): StringValue('a_inst'),
                                                                                    StringValue('MT_Element.id'): StringValue('rhs_a_inst_1'),
                                                                                    StringValue('MTpost_A.MTpost_test_attr'): StringValue('get_attribute() + IntegerValue(1)')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: PythonRepresenter.ASSOCIATION,
                                           CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Rule.MTpost_Contents'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MTpost_Contents.id'): StringValue('rhs_to_rhs_a_inst_1'),
                                                                                    StringValue('from_pattern'): LocationValue('rules.TestRule.rhs'),
                                                                                    StringValue('to_el'): LocationValue('rules.TestRule.rhs_a_inst_1')})
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
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: PythonRepresenter.CLABJECT,
                                           CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.Transformation.Rule'),
                                           CreateConstants.LOCATION_KEY: LocationValue('transformations.TestTransformation'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Rule.id'): StringValue('rule'),
                                                                                    StringValue('Rule.rule_loc'): LocationValue('rules.TestRule')})
                                           })
                             )

        ''' rewrite '''
        self.assertEquals(self.mvk.read(LocationValue('models.TestM')).get_item().get_elements().len(), IntegerValue(1))
        self.assertEquals(self.mvk.read(LocationValue('models.TestM.a.A.test_attr')).get_item().get_value(), IntegerValue(0))
        cl = match_and_rewrite(model_location=LocationValue('models.TestM'),
                               transformation_location=LocationValue('transformations.TestTransformation'))
        self.assertTrue(cl.is_success())
        self.assertEquals(self.mvk.read(LocationValue('models.TestM')).get_item().get_elements().len(), IntegerValue(1))
        self.assertEquals(self.mvk.read(LocationValue('models.TestM.a.A.test_attr')).get_item().get_value(), IntegerValue(1))

if __name__ == "__main__":
    unittest.main()
