'''
Created on 17-mrt.-2014

@author: Simon
'''
import logging
import unittest

from mvk.impl.python.constants import CreateConstants
from mvk.impl.python.datatype import TypeFactory, IntegerType, StringType, \
    BooleanType, TypeType, AnyType
from mvk.impl.python.datavalue import MappingValue, LocationValue, StringValue, \
    IntegerValue, BooleanValue, SequenceValue, InfiniteValue, DataValueFactory, \
    AnyValue
from mvk.impl.python.object import ClabjectReference
from mvk.impl.python.python_representer import PythonRepresenter
from mvk.mvk import MvK
from mvk.plugins.transformation.mt import ramify_scd


class ModelTransformationTestCase(unittest.TestCase):
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

    def create_simple_association_test(self):
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
                                                                                    StringValue('Association.to_max'): IntegerValue(5),
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

    def create_inheritance_type_model(self):
        tm_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('TestSubTyping')})
                                               })
                                 )
        self.assertTrue(tm_log.is_success())
        el_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Element'),
                                                                                        StringValue('Class.is_abstract'): BooleanValue(True)})
                                               })
                                 )
        self.assertTrue(el_log.is_success())
        an_int_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                                   CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping.Element'),
                                                   CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('an_int'),
                                                                                            StringValue('Attribute.type'): TypeFactory.get_type('IntegerType'),
                                                                                            StringValue('Attribute.default'): IntegerValue(0)})
                                                   })
                                     )
        self.assertTrue(an_int_log.is_success())
        a_str_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                                  CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping.Element'),
                                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('a_str'),
                                                                                           StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                                           StringValue('Attribute.default'): StringValue('test')})
                                                  })
                                    )
        self.assertTrue(a_str_log.is_success())
        location_el_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                                        CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping'),
                                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('LocationElement'),
                                                                                                 StringValue('Class.is_abstract'): BooleanValue(True)})
                                                        })
                                          )
        self.assertTrue(location_el_log.is_success())
        location_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                                     CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping.LocationElement'),
                                                     CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('location'),
                                                                                              StringValue('Attribute.type'): TypeFactory.get_type('TupleType(IntegerType, IntegerType)'),
                                                                                              StringValue('Attribute.default'): DataValueFactory.create_instance((0, 0))})
                                                     })
                                       )
        self.assertTrue(location_log.is_success())
        sc_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('LocationElement_i_formalisms_TestSubTyping_Element'),
                                                                                        StringValue('from_class'): LocationValue('formalisms.TestSubTyping.LocationElement'),
                                                                                        StringValue('to_class'): LocationValue('formalisms.TestSubTyping.Element')})
                                               })
                                 )
        self.assertTrue(sc_log.is_success(), sc_log)
        named_el_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                                     CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping'),
                                                     CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('NamedElement'),
                                                                                              StringValue('Class.is_abstract'): BooleanValue(True),
                                                                                              StringValue('Class.id_field'): StringValue('NamedElement.name')})
                                                     })
                                       )
        self.assertTrue(named_el_log.is_success())
        location_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                                     CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping.NamedElement'),
                                                     CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                                              StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                                              StringValue('Attribute.default'): StringValue('')})
                                                     })
                                       )
        sc_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('NamedElement_i_formalisms_TestSubTyping_Element'),
                                                                                        StringValue('from_class'): LocationValue('formalisms.TestSubTyping.NamedElement'),
                                                                                        StringValue('to_class'): LocationValue('formalisms.TestSubTyping.Element')})
                                               })
                                 )
        self.assertTrue(sc_log.is_success())
        character_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping'),
                                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Character'),
                                                                                               StringValue('Class.is_abstract'): BooleanValue(False)})
                                                      })
                                        )
        self.assertTrue(character_log.is_success())
        location_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                                     CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping.Character'),
                                                     CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('fighting_strength'),
                                                                                              StringValue('Attribute.type'): TypeFactory.get_type('IntegerType'),
                                                                                              StringValue('Attribute.default'): IntegerValue(100)})
                                                     })
                                       )
        self.assertTrue(location_log.is_success())
        sc_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('Character_i_formalisms_TestSubTyping_NamedElement'),
                                                                                        StringValue('from_class'): LocationValue('formalisms.TestSubTyping.Character'),
                                                                                        StringValue('to_class'): LocationValue('formalisms.TestSubTyping.NamedElement')})
                                               })
                                 )
        self.assertTrue(sc_log.is_success())
        sc_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('Character_i_formalisms_TestSubTyping_LocationElement'),
                                                                                        StringValue('from_class'): LocationValue('formalisms.TestSubTyping.Character'),
                                                                                        StringValue('to_class'): LocationValue('formalisms.TestSubTyping.LocationElement')})
                                               })
                                 )
        self.assertTrue(sc_log.is_success())
        hero_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                                 CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping'),
                                                 CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Hero'),
                                                                                          StringValue('Class.is_abstract'): BooleanValue(False)})
                                                 })
                                   )
        self.assertTrue(hero_log.is_success())
        points_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                                   CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping.Hero'),
                                                   CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('points'),
                                                                                            StringValue('Attribute.type'): TypeFactory.get_type('IntegerType'),
                                                                                            StringValue('Attribute.default'): IntegerValue(0)})
                                                   })
                                     )
        self.assertTrue(points_log.is_success())
        sc_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('Hero_i_formalisms_TestSubTyping_Character'),
                                                                                        StringValue('from_class'): LocationValue('formalisms.TestSubTyping.Hero'),
                                                                                        StringValue('to_class'): LocationValue('formalisms.TestSubTyping.Character')})
                                               })
                                 )
        self.assertTrue(sc_log.is_success())
        door_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                                 CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping'),
                                                 CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Door'),
                                                                                          StringValue('Class.is_abstract'): BooleanValue(False)})
                                                 })
                                   )
        self.assertTrue(door_log.is_success())
        is_locked_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping.Door'),
                                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('is_locked'),
                                                                                               StringValue('Attribute.type'): TypeFactory.get_type('BooleanType'),
                                                                                               StringValue('Attribute.default'): BooleanValue(False)})
                                                      })
                                     )
        self.assertTrue(is_locked_log.is_success())
        sc_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('Door_i_formalisms_TestSubTyping_NamedElement'),
                                                                                        StringValue('from_class'): LocationValue('formalisms.TestSubTyping.Door'),
                                                                                        StringValue('to_class'): LocationValue('formalisms.TestSubTyping.NamedElement')})
                                               })
                                 )
        self.assertTrue(sc_log.is_success(), sc_log)

    def create_simple_inheritance_type_model(self):
        tm_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('TestSubTyping')})
                                               })
                                 )
        self.assertTrue(tm_log.is_success())
        el_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Element'),
                                                                                        StringValue('Class.is_abstract'): BooleanValue(True)})
                                               })
                                 )
        self.assertTrue(el_log.is_success())
        an_int_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                                   CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping.Element'),
                                                   CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('an_int'),
                                                                                            StringValue('Attribute.type'): TypeFactory.get_type('IntegerType'),
                                                                                            StringValue('Attribute.default'): IntegerValue(0)})
                                                   })
                                     )
        self.assertTrue(an_int_log.is_success())
        a_str_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                                  CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping.Element'),
                                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('a_str'),
                                                                                           StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                                           StringValue('Attribute.default'): StringValue('test')})
                                                  })
                                    )
        self.assertTrue(a_str_log.is_success())
        location_el_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                                        CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping'),
                                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('LocationElement'),
                                                                                                 StringValue('Class.is_abstract'): BooleanValue(True)})
                                                        })
                                          )
        self.assertTrue(location_el_log.is_success())
        location_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                                     CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping.LocationElement'),
                                                     CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('location'),
                                                                                              StringValue('Attribute.type'): TypeFactory.get_type('TupleType(IntegerType, IntegerType)'),
                                                                                              StringValue('Attribute.default'): DataValueFactory.create_instance((0, 0))})
                                                     })
                                       )
        self.assertTrue(location_log.is_success())
        sc_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('LocationElement_i_formalisms_TestSubTyping_Element'),
                                                                                        StringValue('from_class'): LocationValue('formalisms.TestSubTyping.LocationElement'),
                                                                                        StringValue('to_class'): LocationValue('formalisms.TestSubTyping.Element')})
                                               })
                                 )
        self.assertTrue(sc_log.is_success(), sc_log)

    def test_ramification_simple(self):
        self.create_simple_test()

        ''' RAMify - pre '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('MTpre_TestTM')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpre_TestTM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('MTpre_A'),
                                                                                    StringValue('Class.is_abstract'): BooleanValue(False)})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpre_TestTM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('MTpre_A_i_protected_formalisms_Rule_MTpre_Element'),
                                                                                    StringValue('from_class'): LocationValue('formalisms_ref.MTpre_TestTM.MTpre_A'),
                                                                                    StringValue('to_class'): LocationValue('protected.formalisms.Rule.MTpre_Element')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpre_TestTM.MTpre_A'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MTpre_id'),
                                                                                    StringValue('Attribute.type'): StringType(),
                                                                                    StringValue('Attribute.default'): StringValue('True')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpre_TestTM.MTpre_A'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MTpre_test_attr'),
                                                                                    StringValue('Attribute.type'): StringType(),
                                                                                    StringValue('Attribute.default'): StringValue('True')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)

        ''' RAMify - post '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('MTpost_TestTM')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpost_TestTM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('MTpost_A'),
                                                                                    StringValue('Class.is_abstract'): BooleanValue(False)})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpost_TestTM'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('MTpost_A_i_protected_formalisms_Rule_MTpost_Element'),
                                                                                    StringValue('from_class'): LocationValue('formalisms_ref.MTpost_TestTM.MTpost_A'),
                                                                                    StringValue('to_class'): LocationValue('protected.formalisms.Rule.MTpost_Element')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpost_TestTM.MTpost_A'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MTpost_id'),
                                                                                    StringValue('Attribute.type'): StringType(),
                                                                                    StringValue('Attribute.default'): StringValue('get_attribute()')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpost_TestTM.MTpost_A'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MTpost_test_attr'),
                                                                                    StringValue('Attribute.type'): StringType(),
                                                                                    StringValue('Attribute.default'): StringValue('get_attribute()')})
                                           })
                             )
        self.assertTrue(cl.is_success())

        cl = ramify_scd(model_location=LocationValue('formalisms.TestTM'))
        self.assertTrue(cl.is_success(), cl)
        read_log_pre = self.mvk.read(LocationValue('formalisms.MTpre_TestTM'))
        self.assertTrue(read_log_pre.is_success())
        read_log_post = self.mvk.read(LocationValue('formalisms.MTpost_TestTM'))
        self.assertTrue(read_log_post.is_success())
        self.assertTrue(cl.is_success())
        read_log_pre_ref = self.mvk.read(LocationValue('formalisms_ref.MTpre_TestTM'))
        self.assertTrue(read_log_pre_ref.is_success())
        read_log_post_ref = self.mvk.read(LocationValue('formalisms_ref.MTpost_TestTM'))
        self.assertTrue(read_log_post_ref.is_success())
        self.assertEqual(read_log_pre.get_item(), read_log_pre_ref.get_item())
        self.assertEqual(read_log_post.get_item(), read_log_post_ref.get_item())

    def test_ramify_association(self):
        self.create_simple_association_test()
        cl = ramify_scd(model_location=LocationValue('formalisms.TestTM'))
        self.assertTrue(cl.is_success(), cl)
        read_log_pre = self.mvk.read(LocationValue('formalisms.MTpre_TestTM'))
        self.assertTrue(read_log_pre.is_success())
        read_log_post = self.mvk.read(LocationValue('formalisms.MTpre_TestTM'))
        self.assertTrue(read_log_post.is_success())
        self.assertTrue(cl.is_success())
        read_log_pre_assoc = self.mvk.read(LocationValue('formalisms.MTpre_TestTM.MTpre_A_to_A'))
        self.assertTrue(read_log_pre_assoc.is_success())
        read_log_post_assoc = self.mvk.read(LocationValue('formalisms.MTpost_TestTM.MTpost_A_to_A'))
        self.assertTrue(read_log_post_assoc.is_success())
        pre_assoc = read_log_pre_assoc.get_item()
        self.assertEqual(pre_assoc.get_super_classes(), SequenceValue([ClabjectReference(LocationValue('protected.formalisms.Rule.MTpre_Association'))]))
        post_assoc = read_log_post_assoc.get_item()
        self.assertEqual(post_assoc.get_super_classes(), SequenceValue([ClabjectReference(LocationValue('protected.formalisms.Rule.MTpost_Association'))]))
        f_multiplicity_pre = pre_assoc.get_from_multiplicity()
        self.assertEqual(f_multiplicity_pre.get_node(), self.mvk.read(LocationValue('formalisms.MTpre_TestTM.MTpre_A')).get_item())
        self.assertEqual(f_multiplicity_pre.get_lower(), IntegerValue(0))
        self.assertEqual(f_multiplicity_pre.get_upper(), InfiniteValue('+'))
        t_multiplicity_pre = pre_assoc.get_to_multiplicity()
        self.assertEqual(t_multiplicity_pre.get_node(), self.mvk.read(LocationValue('formalisms.MTpre_TestTM.MTpre_A')).get_item())
        self.assertEqual(t_multiplicity_pre.get_lower(), IntegerValue(0))
        self.assertEqual(t_multiplicity_pre.get_upper(), IntegerValue(5))
        f_multiplicity_post = post_assoc.get_from_multiplicity()
        self.assertEqual(f_multiplicity_post.get_node(), self.mvk.read(LocationValue('formalisms.MTpost_TestTM.MTpost_A')).get_item())
        self.assertEqual(f_multiplicity_post.get_lower(), IntegerValue(0))
        self.assertEqual(f_multiplicity_post.get_upper(), InfiniteValue('+'))
        t_multiplicity_post = post_assoc.get_to_multiplicity()
        self.assertEqual(t_multiplicity_post.get_node(), self.mvk.read(LocationValue('formalisms.MTpost_TestTM.MTpost_A')).get_item())
        self.assertEqual(t_multiplicity_post.get_lower(), IntegerValue(0))
        self.assertEqual(t_multiplicity_post.get_upper(), IntegerValue(5))

    def test_ramify_subclassing(self):
        self.create_inheritance_type_model()

        ''' RAMify - pre '''
        tm_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('MTpre_TestSubTyping')})
                                               })
                                 )
        self.assertTrue(tm_log.is_success())
        el_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpre_TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('MTpre_Element'),
                                                                                        StringValue('Class.is_abstract'): BooleanValue(False)})
                                               })
                                 )
        self.assertTrue(el_log.is_success())
        sc_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpre_TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('MTpre_Element_i_protected_formalisms_Rule_MTpre_Element'),
                                                                                        StringValue('from_class'): LocationValue('formalisms_ref.MTpre_TestSubTyping.MTpre_Element'),
                                                                                        StringValue('to_class'): LocationValue('protected.formalisms.Rule.MTpre_Element')})
                                               })
                                 )
        self.assertTrue(sc_log.is_success(), sc_log)
        an_int_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                                   CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpre_TestSubTyping.MTpre_Element'),
                                                   CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MTpre_an_int'),
                                                                                            StringValue('Attribute.type'): StringType(),
                                                                                            StringValue('Attribute.default'): StringValue('True')})
                                                   })
                                     )
        self.assertTrue(an_int_log.is_success())
        a_str_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                                  CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpre_TestSubTyping.MTpre_Element'),
                                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MTpre_a_str'),
                                                                                           StringValue('Attribute.type'): StringType(),
                                                                                           StringValue('Attribute.default'): StringValue('True')})
                                                  })
                                    )
        self.assertTrue(a_str_log.is_success())
        location_el_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                                        CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpre_TestSubTyping'),
                                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('MTpre_LocationElement'),
                                                                                                 StringValue('Class.is_abstract'): BooleanValue(False)})
                                                        })
                                          )
        self.assertTrue(location_el_log.is_success())
        sc_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpre_TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('MTpre_LocationElement_i_protected_formalisms_Rule_MTpre_Element'),
                                                                                        StringValue('from_class'): LocationValue('formalisms_ref.MTpre_TestSubTyping.MTpre_LocationElement'),
                                                                                        StringValue('to_class'): LocationValue('protected.formalisms.Rule.MTpre_Element')})
                                               })
                                 )
        self.assertTrue(sc_log.is_success(), sc_log)
        location_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                                     CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpre_TestSubTyping.MTpre_LocationElement'),
                                                     CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MTpre_location'),
                                                                                              StringValue('Attribute.type'): StringType(),
                                                                                              StringValue('Attribute.default'): StringValue('True')})
                                                     })
                                       )
        self.assertTrue(location_log.is_success())
        sc_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpre_TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('MTpre_LocationElement_i_formalisms_MTpre_TestSubTyping_MTpre_Element'),
                                                                                        StringValue('from_class'): LocationValue('formalisms_ref.MTpre_TestSubTyping.MTpre_LocationElement'),
                                                                                        StringValue('to_class'): LocationValue('formalisms_ref.MTpre_TestSubTyping.MTpre_Element')})
                                               })
                                 )
        self.assertTrue(sc_log.is_success(), sc_log)
        named_el_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                                     CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpre_TestSubTyping'),
                                                     CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('MTpre_NamedElement'),
                                                                                              StringValue('Class.is_abstract'): BooleanValue(False)})
                                                     })
                                       )
        self.assertTrue(named_el_log.is_success())
        sc_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpre_TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('MTpre_NamedElement_i_protected_formalisms_Rule_MTpre_Element'),
                                                                                        StringValue('from_class'): LocationValue('formalisms_ref.MTpre_TestSubTyping.MTpre_NamedElement'),
                                                                                        StringValue('to_class'): LocationValue('protected.formalisms.Rule.MTpre_Element')})
                                               })
                                 )
        self.assertTrue(sc_log.is_success(), sc_log)
        location_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                                     CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpre_TestSubTyping.MTpre_NamedElement'),
                                                     CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MTpre_name'),
                                                                                              StringValue('Attribute.type'): StringType(),
                                                                                              StringValue('Attribute.default'): StringValue('True')})
                                                     })
                                       )
        sc_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpre_TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('MTpre_NamedElement_i_formalisms_MTpre_TestSubTyping_MTpre_Element'),
                                                                                        StringValue('from_class'): LocationValue('formalisms_ref.MTpre_TestSubTyping.MTpre_NamedElement'),
                                                                                        StringValue('to_class'): LocationValue('formalisms_ref.MTpre_TestSubTyping.MTpre_Element')})
                                               })
                                 )
        self.assertTrue(sc_log.is_success())
        character_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpre_TestSubTyping'),
                                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('MTpre_Character'),
                                                                                               StringValue('Class.is_abstract'): BooleanValue(False)})
                                                      })
                                        )
        self.assertTrue(character_log.is_success())
        sc_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpre_TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('MTpre_Character_i_protected_formalisms_Rule_MTpre_Element'),
                                                                                        StringValue('from_class'): LocationValue('formalisms_ref.MTpre_TestSubTyping.MTpre_Character'),
                                                                                        StringValue('to_class'): LocationValue('protected.formalisms.Rule.MTpre_Element')})
                                               })
                                 )
        self.assertTrue(sc_log.is_success(), sc_log)
        location_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                                     CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpre_TestSubTyping.MTpre_Character'),
                                                     CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MTpre_fighting_strength'),
                                                                                              StringValue('Attribute.type'): StringType(),
                                                                                              StringValue('Attribute.default'): StringValue('True')})
                                                     })
                                       )
        self.assertTrue(location_log.is_success())
        sc_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpre_TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('MTpre_Character_i_formalisms_MTpre_TestSubTyping_MTpre_NamedElement'),
                                                                                        StringValue('from_class'): LocationValue('formalisms_ref.MTpre_TestSubTyping.MTpre_Character'),
                                                                                        StringValue('to_class'): LocationValue('formalisms_ref.MTpre_TestSubTyping.MTpre_NamedElement')})
                                               })
                                 )
        self.assertTrue(sc_log.is_success())
        sc_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpre_TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('MTpre_Character_i_formalisms_MTpre_TestSubTyping_MTpre_LocationElement'),
                                                                                        StringValue('from_class'): LocationValue('formalisms_ref.MTpre_TestSubTyping.MTpre_Character'),
                                                                                        StringValue('to_class'): LocationValue('formalisms_ref.MTpre_TestSubTyping.MTpre_LocationElement')})
                                               })
                                 )
        self.assertTrue(sc_log.is_success())
        hero_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                                 CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpre_TestSubTyping'),
                                                 CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('MTpre_Hero'),
                                                                                          StringValue('Class.is_abstract'): BooleanValue(False)})
                                                 })
                                   )
        self.assertTrue(hero_log.is_success())
        sc_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpre_TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('MTpre_Hero_i_protected_formalisms_Rule_MTpre_Element'),
                                                                                        StringValue('from_class'): LocationValue('formalisms_ref.MTpre_TestSubTyping.MTpre_Hero'),
                                                                                        StringValue('to_class'): LocationValue('protected.formalisms.Rule.MTpre_Element')})
                                               })
                                 )
        self.assertTrue(sc_log.is_success(), sc_log)
        points_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                                   CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpre_TestSubTyping.MTpre_Hero'),
                                                   CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MTpre_points'),
                                                                                            StringValue('Attribute.type'): StringType(),
                                                                                            StringValue('Attribute.default'): StringValue('True')})
                                                   })
                                     )
        self.assertTrue(points_log.is_success())
        sc_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpre_TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('MTpre_Hero_i_formalisms_MTpre_TestSubTyping_MTpre_Character'),
                                                                                        StringValue('from_class'): LocationValue('formalisms_ref.MTpre_TestSubTyping.MTpre_Hero'),
                                                                                        StringValue('to_class'): LocationValue('formalisms_ref.MTpre_TestSubTyping.MTpre_Character')})
                                               })
                                 )
        self.assertTrue(sc_log.is_success())
        door_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                                 CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpre_TestSubTyping'),
                                                 CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('MTpre_Door'),
                                                                                          StringValue('Class.is_abstract'): BooleanValue(False)})
                                                 })
                                   )
        self.assertTrue(door_log.is_success())
        sc_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpre_TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('MTpre_Door_i_protected_formalisms_Rule_MTpre_Element'),
                                                                                        StringValue('from_class'): LocationValue('formalisms_ref.MTpre_TestSubTyping.MTpre_Door'),
                                                                                        StringValue('to_class'): LocationValue('protected.formalisms.Rule.MTpre_Element')})
                                               })
                                 )
        self.assertTrue(sc_log.is_success(), sc_log)
        is_locked_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpre_TestSubTyping.MTpre_Door'),
                                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MTpre_is_locked'),
                                                                                               StringValue('Attribute.type'): StringType(),
                                                                                               StringValue('Attribute.default'): StringValue('True')})
                                                      })
                                     )
        self.assertTrue(is_locked_log.is_success())
        sc_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpre_TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('MTpre_Door_i_formalisms_MTpre_TestSubTyping_MTpre_NamedElement'),
                                                                                        StringValue('from_class'): LocationValue('formalisms_ref.MTpre_TestSubTyping.MTpre_Door'),
                                                                                        StringValue('to_class'): LocationValue('formalisms_ref.MTpre_TestSubTyping.MTpre_NamedElement')})
                                               })
                                 )
        self.assertTrue(sc_log.is_success(), sc_log)

        ''' RAMify - post '''
        tm_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('MTpost_TestSubTyping')})
                                               })
                                 )
        self.assertTrue(tm_log.is_success())
        el_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpost_TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('MTpost_Element'),
                                                                                        StringValue('Class.is_abstract'): BooleanValue(False)})
                                               })
                                 )
        self.assertTrue(el_log.is_success())
        sc_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpost_TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('MTpost_Element_i_protected_formalisms_Rule_MTpost_Element'),
                                                                                        StringValue('from_class'): LocationValue('formalisms_ref.MTpost_TestSubTyping.MTpost_Element'),
                                                                                        StringValue('to_class'): LocationValue('protected.formalisms.Rule.MTpost_Element')})
                                               })
                                 )
        self.assertTrue(sc_log.is_success(), sc_log)
        an_int_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                                   CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpost_TestSubTyping.MTpost_Element'),
                                                   CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MTpost_an_int'),
                                                                                            StringValue('Attribute.type'): StringType(),
                                                                                            StringValue('Attribute.default'): StringValue('get_attribute()')})
                                                   })
                                     )
        self.assertTrue(an_int_log.is_success())
        a_str_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                                  CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpost_TestSubTyping.MTpost_Element'),
                                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MTpost_a_str'),
                                                                                           StringValue('Attribute.type'): StringType(),
                                                                                           StringValue('Attribute.default'): StringValue('get_attribute()')})
                                                  })
                                    )
        self.assertTrue(a_str_log.is_success())
        location_el_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                                        CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpost_TestSubTyping'),
                                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('MTpost_LocationElement'),
                                                                                                 StringValue('Class.is_abstract'): BooleanValue(False)})
                                                        })
                                          )
        self.assertTrue(location_el_log.is_success())
        sc_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpost_TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('MTpost_LocationElement_i_protected_formalisms_Rule_MTpost_Element'),
                                                                                        StringValue('from_class'): LocationValue('formalisms_ref.MTpost_TestSubTyping.MTpost_LocationElement'),
                                                                                        StringValue('to_class'): LocationValue('protected.formalisms.Rule.MTpost_Element')})
                                               })
                                 )
        self.assertTrue(sc_log.is_success(), sc_log)
        location_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                                     CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpost_TestSubTyping.MTpost_LocationElement'),
                                                     CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MTpost_location'),
                                                                                              StringValue('Attribute.type'): StringType(),
                                                                                              StringValue('Attribute.default'): StringValue('get_attribute()')})
                                                     })
                                       )
        self.assertTrue(location_log.is_success())
        sc_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpost_TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('MTpost_LocationElement_i_formalisms_MTpost_TestSubTyping_MTpost_Element'),
                                                                                        StringValue('from_class'): LocationValue('formalisms_ref.MTpost_TestSubTyping.MTpost_LocationElement'),
                                                                                        StringValue('to_class'): LocationValue('formalisms_ref.MTpost_TestSubTyping.MTpost_Element')})
                                               })
                                 )
        self.assertTrue(sc_log.is_success(), sc_log)
        named_el_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                                     CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpost_TestSubTyping'),
                                                     CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('MTpost_NamedElement'),
                                                                                              StringValue('Class.is_abstract'): BooleanValue(False)})
                                                     })
                                       )
        self.assertTrue(named_el_log.is_success())
        sc_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpost_TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('MTpost_NamedElement_i_protected_formalisms_Rule_MTpost_Element'),
                                                                                        StringValue('from_class'): LocationValue('formalisms_ref.MTpost_TestSubTyping.MTpost_NamedElement'),
                                                                                        StringValue('to_class'): LocationValue('protected.formalisms.Rule.MTpost_Element')})
                                               })
                                 )
        self.assertTrue(sc_log.is_success(), sc_log)
        location_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                                     CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpost_TestSubTyping.MTpost_NamedElement'),
                                                     CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MTpost_name'),
                                                                                              StringValue('Attribute.type'): StringType(),
                                                                                              StringValue('Attribute.default'): StringValue('get_attribute()')})
                                                     })
                                       )
        sc_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpost_TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('MTpost_NamedElement_i_formalisms_MTpost_TestSubTyping_MTpost_Element'),
                                                                                        StringValue('from_class'): LocationValue('formalisms_ref.MTpost_TestSubTyping.MTpost_NamedElement'),
                                                                                        StringValue('to_class'): LocationValue('formalisms_ref.MTpost_TestSubTyping.MTpost_Element')})
                                               })
                                 )
        self.assertTrue(sc_log.is_success())
        character_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpost_TestSubTyping'),
                                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('MTpost_Character'),
                                                                                               StringValue('Class.is_abstract'): BooleanValue(False)})
                                                      })
                                        )
        self.assertTrue(character_log.is_success())
        sc_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpost_TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('MTpost_Character_i_protected_formalisms_Rule_MTpost_Element'),
                                                                                        StringValue('from_class'): LocationValue('formalisms_ref.MTpost_TestSubTyping.MTpost_Character'),
                                                                                        StringValue('to_class'): LocationValue('protected.formalisms.Rule.MTpost_Element')})
                                               })
                                 )
        self.assertTrue(sc_log.is_success(), sc_log)
        location_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                                     CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpost_TestSubTyping.MTpost_Character'),
                                                     CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MTpost_fighting_strength'),
                                                                                              StringValue('Attribute.type'): StringType(),
                                                                                              StringValue('Attribute.default'): StringValue('get_attribute()')})
                                                     })
                                       )
        self.assertTrue(location_log.is_success())
        sc_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpost_TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('MTpost_Character_i_formalisms_MTpost_TestSubTyping_MTpost_NamedElement'),
                                                                                        StringValue('from_class'): LocationValue('formalisms_ref.MTpost_TestSubTyping.MTpost_Character'),
                                                                                        StringValue('to_class'): LocationValue('formalisms_ref.MTpost_TestSubTyping.MTpost_NamedElement')})
                                               })
                                 )
        self.assertTrue(sc_log.is_success())
        sc_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpost_TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('MTpost_Character_i_formalisms_MTpost_TestSubTyping_MTpost_LocationElement'),
                                                                                        StringValue('from_class'): LocationValue('formalisms_ref.MTpost_TestSubTyping.MTpost_Character'),
                                                                                        StringValue('to_class'): LocationValue('formalisms_ref.MTpost_TestSubTyping.MTpost_LocationElement')})
                                               })
                                 )
        self.assertTrue(sc_log.is_success())
        hero_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                                 CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpost_TestSubTyping'),
                                                 CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('MTpost_Hero'),
                                                                                          StringValue('Class.is_abstract'): BooleanValue(False)})
                                                 })
                                   )
        self.assertTrue(hero_log.is_success())
        sc_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpost_TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('MTpost_Hero_i_protected_formalisms_Rule_MTpost_Element'),
                                                                                        StringValue('from_class'): LocationValue('formalisms_ref.MTpost_TestSubTyping.MTpost_Hero'),
                                                                                        StringValue('to_class'): LocationValue('protected.formalisms.Rule.MTpost_Element')})
                                               })
                                 )
        self.assertTrue(sc_log.is_success(), sc_log)
        points_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                                   CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpost_TestSubTyping.MTpost_Hero'),
                                                   CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MTpost_points'),
                                                                                            StringValue('Attribute.type'): StringType(),
                                                                                            StringValue('Attribute.default'): StringValue('get_attribute()')})
                                                   })
                                     )
        self.assertTrue(points_log.is_success())
        sc_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpost_TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('MTpost_Hero_i_formalisms_MTpost_TestSubTyping_MTpost_Character'),
                                                                                        StringValue('from_class'): LocationValue('formalisms_ref.MTpost_TestSubTyping.MTpost_Hero'),
                                                                                        StringValue('to_class'): LocationValue('formalisms_ref.MTpost_TestSubTyping.MTpost_Character')})
                                               })
                                 )
        self.assertTrue(sc_log.is_success())
        door_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                                 CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpost_TestSubTyping'),
                                                 CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('MTpost_Door'),
                                                                                          StringValue('Class.is_abstract'): BooleanValue(False)})
                                                 })
                                   )
        self.assertTrue(door_log.is_success())
        sc_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpost_TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('MTpost_Door_i_protected_formalisms_Rule_MTpost_Element'),
                                                                                        StringValue('from_class'): LocationValue('formalisms_ref.MTpost_TestSubTyping.MTpost_Door'),
                                                                                        StringValue('to_class'): LocationValue('protected.formalisms.Rule.MTpost_Element')})
                                               })
                                 )
        self.assertTrue(sc_log.is_success(), sc_log)
        is_locked_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpost_TestSubTyping.MTpost_Door'),
                                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MTpost_is_locked'),
                                                                                               StringValue('Attribute.type'): StringType(),
                                                                                               StringValue('Attribute.default'): StringValue('get_attribute()')})
                                                      })
                                     )
        self.assertTrue(is_locked_log.is_success())
        sc_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpost_TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('MTpost_Door_i_formalisms_MTpost_TestSubTyping_MTpost_NamedElement'),
                                                                                        StringValue('from_class'): LocationValue('formalisms_ref.MTpost_TestSubTyping.MTpost_Door'),
                                                                                        StringValue('to_class'): LocationValue('formalisms_ref.MTpost_TestSubTyping.MTpost_NamedElement')})
                                               })
                                 )
        self.assertTrue(sc_log.is_success(), sc_log)

        cl = ramify_scd(model_location=LocationValue('formalisms.TestSubTyping'))
        self.assertTrue(cl.is_success(), cl)
        read_log_pre = self.mvk.read(LocationValue('formalisms.MTpre_TestSubTyping'))
        self.assertTrue(read_log_pre.is_success(), read_log_pre)
        read_log_post = self.mvk.read(LocationValue('formalisms.MTpost_TestSubTyping'))
        self.assertTrue(read_log_post.is_success())
        self.assertTrue(cl.is_success())
        read_log_pre_ref = self.mvk.read(LocationValue('formalisms_ref.MTpre_TestSubTyping'))
        self.assertTrue(read_log_pre_ref.is_success())
        self.assertEqual(read_log_pre.get_item(), read_log_pre_ref.get_item())
        read_log_post_ref = self.mvk.read(LocationValue('formalisms_ref.MTpost_TestSubTyping'))
        self.assertTrue(read_log_post_ref.is_success())
        self.assertEqual(read_log_post.get_item(), read_log_post_ref.get_item())

    def test_ramify_simple_subclassing(self):
        self.create_simple_inheritance_type_model()

        ''' RAMify - pre '''
        tm_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('MTpre_TestSubTyping')})
                                               })
                                 )
        self.assertTrue(tm_log.is_success())
        el_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpre_TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('MTpre_Element'),
                                                                                        StringValue('Class.is_abstract'): BooleanValue(False)})
                                               })
                                 )
        self.assertTrue(el_log.is_success())
        sc_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpre_TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('MTpre_Element_i_protected_formalisms_Rule_MTpre_Element'),
                                                                                        StringValue('from_class'): LocationValue('formalisms_ref.MTpre_TestSubTyping.MTpre_Element'),
                                                                                        StringValue('to_class'): LocationValue('protected.formalisms.Rule.MTpre_Element')})
                                               })
                                 )
        self.assertTrue(sc_log.is_success(), sc_log)
        an_int_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                                   CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpre_TestSubTyping.MTpre_Element'),
                                                   CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MTpre_an_int'),
                                                                                            StringValue('Attribute.type'): StringType(),
                                                                                            StringValue('Attribute.default'): StringValue('True')})
                                                   })
                                     )
        self.assertTrue(an_int_log.is_success())
        a_str_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                                  CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpre_TestSubTyping.MTpre_Element'),
                                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MTpre_a_str'),
                                                                                           StringValue('Attribute.type'): StringType(),
                                                                                           StringValue('Attribute.default'): StringValue('True')})
                                                  })
                                    )
        self.assertTrue(a_str_log.is_success())
        location_el_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                                        CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpre_TestSubTyping'),
                                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('MTpre_LocationElement'),
                                                                                                 StringValue('Class.is_abstract'): BooleanValue(False)})
                                                        })
                                          )
        self.assertTrue(location_el_log.is_success())
        sc_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpre_TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('MTpre_LocationElement_i_protected_formalisms_Rule_MTpre_Element'),
                                                                                        StringValue('from_class'): LocationValue('formalisms_ref.MTpre_TestSubTyping.MTpre_LocationElement'),
                                                                                        StringValue('to_class'): LocationValue('protected.formalisms.Rule.MTpre_Element')})
                                               })
                                 )
        self.assertTrue(sc_log.is_success(), sc_log)
        location_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                                     CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpre_TestSubTyping.MTpre_LocationElement'),
                                                     CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MTpre_location'),
                                                                                              StringValue('Attribute.type'): StringType(),
                                                                                              StringValue('Attribute.default'): StringValue('True')})
                                                     })
                                       )
        self.assertTrue(location_log.is_success())
        sc_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpre_TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('MTpre_LocationElement_i_formalisms_MTpre_TestSubTyping_MTpre_Element'),
                                                                                        StringValue('from_class'): LocationValue('formalisms_ref.MTpre_TestSubTyping.MTpre_LocationElement'),
                                                                                        StringValue('to_class'): LocationValue('formalisms_ref.MTpre_TestSubTyping.MTpre_Element')})
                                               })
                                 )
        self.assertTrue(sc_log.is_success(), sc_log)

        ''' RAMify - post '''
        tm_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('MTpost_TestSubTyping')})
                                               })
                                 )
        self.assertTrue(tm_log.is_success())
        el_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpost_TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('MTpost_Element'),
                                                                                        StringValue('Class.is_abstract'): BooleanValue(False)})
                                               })
                                 )
        self.assertTrue(el_log.is_success())
        sc_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpost_TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('MTpost_Element_i_protected_formalisms_Rule_MTpost_Element'),
                                                                                        StringValue('from_class'): LocationValue('formalisms_ref.MTpost_TestSubTyping.MTpost_Element'),
                                                                                        StringValue('to_class'): LocationValue('protected.formalisms.Rule.MTpost_Element')})
                                               })
                                 )
        self.assertTrue(sc_log.is_success(), sc_log)
        an_int_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                                   CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpost_TestSubTyping.MTpost_Element'),
                                                   CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MTpost_an_int'),
                                                                                            StringValue('Attribute.type'): StringType(),
                                                                                            StringValue('Attribute.default'): StringValue('get_attribute()')})
                                                   })
                                     )
        self.assertTrue(an_int_log.is_success())
        a_str_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                                  CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpost_TestSubTyping.MTpost_Element'),
                                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MTpost_a_str'),
                                                                                           StringValue('Attribute.type'): StringType(),
                                                                                           StringValue('Attribute.default'): StringValue('get_attribute()')})
                                                  })
                                    )
        self.assertTrue(a_str_log.is_success())
        location_el_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                                        CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpost_TestSubTyping'),
                                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('MTpost_LocationElement'),
                                                                                                 StringValue('Class.is_abstract'): BooleanValue(False)})
                                                        })
                                          )
        self.assertTrue(location_el_log.is_success())
        sc_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpost_TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('MTpost_LocationElement_i_protected_formalisms_Rule_MTpost_Element'),
                                                                                        StringValue('from_class'): LocationValue('formalisms_ref.MTpost_TestSubTyping.MTpost_LocationElement'),
                                                                                        StringValue('to_class'): LocationValue('protected.formalisms.Rule.MTpost_Element')})
                                               })
                                 )
        self.assertTrue(sc_log.is_success(), sc_log)
        location_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                                     CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpost_TestSubTyping.MTpost_LocationElement'),
                                                     CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('MTpost_location'),
                                                                                              StringValue('Attribute.type'): StringType(),
                                                                                              StringValue('Attribute.default'): StringValue('get_attribute()')})
                                                     })
                                       )
        self.assertTrue(location_log.is_success())
        sc_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms_ref.MTpost_TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('MTpost_LocationElement_i_formalisms_MTpost_TestSubTyping_MTpost_Element'),
                                                                                        StringValue('from_class'): LocationValue('formalisms_ref.MTpost_TestSubTyping.MTpost_LocationElement'),
                                                                                        StringValue('to_class'): LocationValue('formalisms_ref.MTpost_TestSubTyping.MTpost_Element')})
                                               })
                                 )
        self.assertTrue(sc_log.is_success(), sc_log)

        cl = ramify_scd(model_location=LocationValue('formalisms.TestSubTyping'))
        self.assertTrue(cl.is_success(), cl)
        read_log_pre = self.mvk.read(LocationValue('formalisms.MTpre_TestSubTyping'))
        self.assertTrue(read_log_pre.is_success(), read_log_pre)
        read_log_post = self.mvk.read(LocationValue('formalisms.MTpost_TestSubTyping'))
        self.assertTrue(read_log_post.is_success())
        self.assertTrue(cl.is_success())
        read_log_pre_ref = self.mvk.read(LocationValue('formalisms_ref.MTpre_TestSubTyping'))
        self.assertTrue(read_log_pre_ref.is_success())
        self.assertEqual(read_log_pre.get_item(), read_log_pre_ref.get_item())
        read_log_post_ref = self.mvk.read(LocationValue('formalisms_ref.MTpost_TestSubTyping'))
        self.assertTrue(read_log_post_ref.is_success())
        self.assertEqual(read_log_post.get_item(), read_log_post_ref.get_item())


if __name__ == "__main__":
    unittest.main()
