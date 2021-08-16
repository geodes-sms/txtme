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
from mvk.plugins.transformation.algorithm import get_matches, match_and_rewrite, execute_transformation
#from mvk.util import draw

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
                                                                                    StringValue('MTpost_A.MTpost_id'): StringValue('DataValueFactory.create_instance(\'a3\')')})
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
  
         
        '''Create transformation schedule, no transformation steps here just rule steps'''
        ''''''''''''''''''''''''''''''''''''''''''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.MT'),
                                           CreateConstants.LOCATION_KEY: LocationValue('transformations'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MT.name'): StringValue('CreateTrans')})
                                           })
                             )
        '''Create ARule step'''
        cl = self.mvk.create(MappingValue({
                                           CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.MT.ARule'),
                                           CreateConstants.LOCATION_KEY: LocationValue('transformations.CreateTrans'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Rule.location'): LocationValue('rules.TestRule'),
                                                                                    StringValue('Step.name'): StringValue('arule1'),
                                                                                    StringValue('Step.id'): StringValue('arule1'),
                                                                                    StringValue('Step.isStart'): BooleanValue(True),
                                                                                    StringValue('Rule.first_match'): BooleanValue(True)})
                                           })
                             )
        '''OnSuccess flow that can be navigated 0 times'''
        cl = self.mvk.create(MappingValue({
                                           CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.MT.OnSuccess'),
                                           CreateConstants.LOCATION_KEY: LocationValue('transformations.CreateTrans'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Flow.id'): StringValue('ar1_to_ar1'),
                                                                                    StringValue('from_step'): LocationValue('transformations.CreateTrans.arule1'),
                                                                                    StringValue('to_step'): LocationValue('transformations.CreateTrans.arule1'),
                                                                                    StringValue('Flow.exec_num'): IntegerValue(0)})
                                           })
                             )
         
        ''' Execute transformation'''
        self.assertEquals(self.mvk.read(LocationValue('models.TestM')).get_item().get_elements().len(), IntegerValue(1))
        cl = execute_transformation(model_location=LocationValue('models.TestM'),transformation_location=LocationValue("transformations.CreateTrans"))
        self.assertTrue(cl.is_success(), cl)
        self.assertEquals(self.mvk.read(LocationValue('models.TestM')).get_item().get_elements().len(), IntegerValue(2))



    def test_update_successful(self):
        self.create_simple_test()
        '''Transformation here will increment attribute 4 times.'''
        
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
        
        
        '''Create 2 transformation (schedules) models/packages '''
        ''''''''''''''''''''''''''''''''''''''''''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.MT'),
                                           CreateConstants.LOCATION_KEY: LocationValue('transformations'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MT.name'): StringValue('Trans1')})
                                           })
                             )
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.MT'),
                                           CreateConstants.LOCATION_KEY: LocationValue('transformations'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MT.name'): StringValue('Trans2')})
                                           })
                             )

        '''Create transformation step'''
        cl = self.mvk.create(MappingValue({
                                           CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.MT.Transformation'),
                                           CreateConstants.LOCATION_KEY: LocationValue('transformations.Trans1'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Transformation.location'): LocationValue('transformations.Trans2'),
                                                                                    StringValue('Step.name'): StringValue('Trans1'),
                                                                                    StringValue('Step.id'): StringValue('Trans1'),
                                                                                    StringValue('Step.isStart'): BooleanValue(True)})
                                           })
                             )
        '''Create another transformation step'''
        cl = self.mvk.create(MappingValue({
                                           CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.MT.Transformation'),
                                           CreateConstants.LOCATION_KEY: LocationValue('transformations.Trans2'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Transformation.location'): LocationValue('transformations.UpdateTrans'),
                                                                                    StringValue('Step.name'): StringValue('Trans2'),
                                                                                    StringValue('Step.id'): StringValue('Trans2'),
                                                                                    StringValue('Step.isStart'): BooleanValue(True)})
                                           })
                             )
        
        
        '''Create another transformation schedule, no transformation blobs here just rules'''
        ''''''''''''''''''''''''''''''''''''''''''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.MT'),
                                           CreateConstants.LOCATION_KEY: LocationValue('transformations'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MT.name'): StringValue('UpdateTrans')})
                                           })
                             )
        '''Create ARule step'''
        cl = self.mvk.create(MappingValue({
                                           CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.MT.ARule'),
                                           CreateConstants.LOCATION_KEY: LocationValue('transformations.UpdateTrans'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Rule.location'): LocationValue('rules.TestRule'),
                                                                                    StringValue('Step.name'): StringValue('arule1'),
                                                                                    StringValue('Step.id'): StringValue('arule1'),
                                                                                    StringValue('Step.isStart'): BooleanValue(True),
                                                                                    StringValue('Rule.first_match'): BooleanValue(True)})
                                           })
                             )
        
        
        '''Create another ARule step'''
        cl = self.mvk.create(MappingValue({
                                           CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.MT.ARule'),
                                           CreateConstants.LOCATION_KEY: LocationValue('transformations.UpdateTrans'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Rule.location'): LocationValue('rules.TestRule'),
                                                                                    StringValue('Step.name'): StringValue('arule2'),
                                                                                    StringValue('Step.id'): StringValue('arule2'),
                                                                                    StringValue('Step.isStart'): BooleanValue(False),
                                                                                    StringValue('Rule.first_match'): BooleanValue(True)})
                                           })
                             )
        
        '''OnSuccess flow that can be navigated only twice'''
        cl = self.mvk.create(MappingValue({
                                           CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.MT.OnSuccess'),
                                           CreateConstants.LOCATION_KEY: LocationValue('transformations.UpdateTrans'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Flow.id'): StringValue('ar1_to_ar2'),
                                                                                    StringValue('from_step'): LocationValue('transformations.UpdateTrans.arule1'),
                                                                                    StringValue('to_step'): LocationValue('transformations.UpdateTrans.arule2'),
                                                                                    StringValue('Flow.exec_num'): IntegerValue(2)})
                                           })
                             )
        '''OnSuccess flow that can be navigated only once'''
        cl = self.mvk.create(MappingValue({
                                           CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.MT.OnSuccess'),
                                           CreateConstants.LOCATION_KEY: LocationValue('transformations.UpdateTrans'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Flow.id'): StringValue('ar2_to_ar1'),
                                                                                    StringValue('from_step'): LocationValue('transformations.UpdateTrans.arule2'),
                                                                                    StringValue('to_step'): LocationValue('transformations.UpdateTrans.arule1'),
                                                                                    StringValue('Flow.exec_num'): IntegerValue(1)})
                                           })
                             )
        
        
    
        self.assertEquals(self.mvk.read(LocationValue('models.TestM')).get_item().get_elements().len(), IntegerValue(1))
        self.assertEquals(self.mvk.read(LocationValue('models.TestM.a.A.test_attr')).get_item().get_value(), IntegerValue(0))
        
        '''Execute transformation where we have just rule steps'''
        #cl = execute_transformation(model_location=LocationValue('models.TestM'),transformation_location=LocationValue("transformations.UpdateTrans"))
        '''Execute transformation where we have some transformation steps'''
        cl = execute_transformation(model_location=LocationValue('models.TestM'),transformation_location=LocationValue("transformations.Trans1"))
        
        ''''''''''''''''''''''''''''''''''''''''''
    
        self.assertTrue(cl.is_success())
        self.assertEquals(self.mvk.read(LocationValue('models.TestM')).get_item().get_elements().len(), IntegerValue(1))
        self.assertEquals(self.mvk.read(LocationValue('models.TestM.a.A.test_attr')).get_item().get_value(), IntegerValue(4))
        
    def test_update_notapplicable(self):
        self.create_simple_test()
        '''Transformation here will increment attribute 4 times.'''
         
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
        
        '''This will not match'''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: PythonRepresenter.CLABJECT,
                                           CreateConstants.TYPE_KEY: LocationValue('formalisms.MTpre_TestTM.MTpre_A'),
                                           CreateConstants.LOCATION_KEY: LocationValue('rules.TestRule'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MT_Element.MT_label'): StringValue('a_inst'),
                                                                                    StringValue('MT_Element.id'): StringValue('lhs_a_inst'),
                                                                                    StringValue('MTpre_A.MTpre_test_attr'): StringValue('False')})
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
         
         
        '''Create 2 transformation (schedules) models/packages '''
        ''''''''''''''''''''''''''''''''''''''''''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.MT'),
                                           CreateConstants.LOCATION_KEY: LocationValue('transformations'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MT.name'): StringValue('Trans1')})
                                           })
                             )
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.MT'),
                                           CreateConstants.LOCATION_KEY: LocationValue('transformations'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MT.name'): StringValue('Trans2')})
                                           })
                             )
 
        '''Create transformation step'''
        cl = self.mvk.create(MappingValue({
                                           CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.MT.Transformation'),
                                           CreateConstants.LOCATION_KEY: LocationValue('transformations.Trans1'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Transformation.location'): LocationValue('transformations.Trans2'),
                                                                                    StringValue('Step.name'): StringValue('Trans1'),
                                                                                    StringValue('Step.id'): StringValue('Trans1'),
                                                                                    StringValue('Step.isStart'): BooleanValue(True)})
                                           })
                             )
        '''Create another transformation step'''
        cl = self.mvk.create(MappingValue({
                                           CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.MT.Transformation'),
                                           CreateConstants.LOCATION_KEY: LocationValue('transformations.Trans2'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Transformation.location'): LocationValue('transformations.UpdateTrans'),
                                                                                    StringValue('Step.name'): StringValue('Trans2'),
                                                                                    StringValue('Step.id'): StringValue('Trans2'),
                                                                                    StringValue('Step.isStart'): BooleanValue(True)})
                                           })
                             )
         
         
        '''Create another transformation schedule, no transformation blobs here just rules'''
        ''''''''''''''''''''''''''''''''''''''''''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.MT'),
                                           CreateConstants.LOCATION_KEY: LocationValue('transformations'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('MT.name'): StringValue('UpdateTrans')})
                                           })
                             )
        '''Create ARule step'''
        cl = self.mvk.create(MappingValue({
                                           CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.MT.ARule'),
                                           CreateConstants.LOCATION_KEY: LocationValue('transformations.UpdateTrans'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Rule.location'): LocationValue('rules.TestRule'),
                                                                                    StringValue('Step.name'): StringValue('arule1'),
                                                                                    StringValue('Step.id'): StringValue('arule1'),
                                                                                    StringValue('Step.isStart'): BooleanValue(True),
                                                                                    StringValue('Rule.first_match'): BooleanValue(True)})
                                           })
                             )
         
         
        '''Create another ARule step'''
        cl = self.mvk.create(MappingValue({
                                           CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.MT.ARule'),
                                           CreateConstants.LOCATION_KEY: LocationValue('transformations.UpdateTrans'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Rule.location'): LocationValue('rules.TestRule'),
                                                                                    StringValue('Step.name'): StringValue('arule2'),
                                                                                    StringValue('Step.id'): StringValue('arule2'),
                                                                                    StringValue('Step.isStart'): BooleanValue(False),
                                                                                    StringValue('Rule.first_match'): BooleanValue(True)})
                                           })
                             )
         
        '''OnSuccess flow that can be navigated only twice'''
        cl = self.mvk.create(MappingValue({
                                           CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.MT.OnSuccess'),
                                           CreateConstants.LOCATION_KEY: LocationValue('transformations.UpdateTrans'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Flow.id'): StringValue('ar1_to_ar2'),
                                                                                    StringValue('from_step'): LocationValue('transformations.UpdateTrans.arule1'),
                                                                                    StringValue('to_step'): LocationValue('transformations.UpdateTrans.arule2'),
                                                                                    StringValue('Flow.exec_num'): IntegerValue(2)})
                                           })
                             )
        '''OnSuccess flow that can be navigated only once'''
        cl = self.mvk.create(MappingValue({
                                           CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.MT.OnSuccess'),
                                           CreateConstants.LOCATION_KEY: LocationValue('transformations.UpdateTrans'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Flow.id'): StringValue('ar2_to_ar1'),
                                                                                    StringValue('from_step'): LocationValue('transformations.UpdateTrans.arule2'),
                                                                                    StringValue('to_step'): LocationValue('transformations.UpdateTrans.arule1'),
                                                                                    StringValue('Flow.exec_num'): IntegerValue(1)})
                                           })
                             )
         
         
     
        self.assertEquals(self.mvk.read(LocationValue('models.TestM')).get_item().get_elements().len(), IntegerValue(1))
        self.assertEquals(self.mvk.read(LocationValue('models.TestM.a.A.test_attr')).get_item().get_value(), IntegerValue(0))
         
        '''Execute transformation where we have just rule steps'''
        #cl = execute_transformation(model_location=LocationValue('models.TestM'),transformation_location=LocationValue("transformations.UpdateTrans"))
        '''Execute transformation where we have some transformation steps'''
        cl = execute_transformation(model_location=LocationValue('models.TestM'),transformation_location=LocationValue("transformations.Trans1"))
         
        ''''''''''''''''''''''''''''''''''''''''''
     
        self.assertTrue(cl.is_success())
        self.assertEquals(self.mvk.read(LocationValue('models.TestM')).get_item().get_elements().len(), IntegerValue(1))
        self.assertEquals(self.mvk.read(LocationValue('models.TestM.a.A.test_attr')).get_item().get_value(), IntegerValue(0))

if __name__ == "__main__":
    unittest.main()
