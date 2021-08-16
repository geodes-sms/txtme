'''
Created on 11-jun.-2014

@author: Simon
'''
import unittest

from mvk.impl.python.constants import CreateConstants
from mvk.impl.python.datatype import TypeFactory
from mvk.impl.python.datavalue import MappingValue, LocationValue, StringValue, BooleanValue, IntegerValue, FloatValue, InfiniteValue
from mvk.mvk import MvK


class ConformanceTestCase(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName=methodName)
        self.mvk = MvK()

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.mvk.clear()

    def tearDown(self):
        self.mvk.clear()
        unittest.TestCase.tearDown(self)

    def test_type_not_found(self):
        ''' type model MM_A '''
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('MM_A')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.MM_A'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.MM_A'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('A'),
                                                                               StringValue('Class.is_abstract'): BooleanValue(False),
                                                                               StringValue('Class.id_field'): StringValue('A.name')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.MM_A.A'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        ''' type model MM_B '''
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('MM_B')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.MM_B'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.MM_B'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('A'),
                                                                               StringValue('Class.is_abstract'): BooleanValue(False),
                                                                               StringValue('Class.id_field'): StringValue('A.name')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.MM_B.A'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        ''' instance model '''
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.MM_A'),
                                      CreateConstants.LOCATION_KEY: LocationValue('models'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('MM_A.name'): StringValue('myModel')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.MM_A.A'),
                                      CreateConstants.LOCATION_KEY: LocationValue('models.myModel'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('A.name'): StringValue('a')})
                                      })
                        )
        self.assertTrue(self.mvk.conforms_to(LocationValue('models.myModel'), LocationValue('formalisms.MM_A')).get_result())
        self.assertFalse(self.mvk.conforms_to(LocationValue('models.myModel'), LocationValue('formalisms.MM_B')).get_result())

    def test_wrong_attribute_type(self):
        ''' type model MM_A '''
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('MM_A')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.MM_A'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.MM_A'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('A'),
                                                                               StringValue('Class.is_abstract'): BooleanValue(False),
                                                                               StringValue('Class.id_field'): StringValue('A.name')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.MM_A.A'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.MM_A.A'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('c'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('IntegerType'),
                                                                               StringValue('Attribute.default'): IntegerValue(0)})
                                      })
                        )
        ''' instance model '''
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.MM_A'),
                                      CreateConstants.LOCATION_KEY: LocationValue('models'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('MM_A.name'): StringValue('myModel')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.MM_A.A'),
                                      CreateConstants.LOCATION_KEY: LocationValue('models.myModel'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('A.name'): StringValue('a'),
                                                                               StringValue('A.c'): StringValue('1')})
                                      })
                        )
        self.assertFalse(self.mvk.conforms_to(LocationValue('models.myModel'), LocationValue('formalisms.MM_A')).get_result())

    def test_out_card_min(self):
        ''' type model MM_A '''
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('MM_A')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.MM_A'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.MM_A'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('A'),
                                                                               StringValue('Class.is_abstract'): BooleanValue(False),
                                                                               StringValue('Class.id_field'): StringValue('A.name')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.MM_A.A'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.MM_A'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('B'),
                                                                               StringValue('Class.is_abstract'): BooleanValue(False),
                                                                               StringValue('Class.id_field'): StringValue('A.name')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.MM_A.B'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.SimpleClassDiagrams.Association"),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.MM_A'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('from_class'): LocationValue('formalisms.MM_A.A'),
                                                                               StringValue('to_class'): LocationValue('formalisms.MM_A.B'),
                                                                               StringValue('Class.name'): StringValue('A_to_B'),
                                                                               StringValue('Class.is_abstract'): BooleanValue(False),
                                                                               StringValue('Class.id_field'): StringValue('A_to_B.name'),
                                                                               StringValue('Association.from_min'): IntegerValue(0),
                                                                               StringValue('Association.from_max'): InfiniteValue('+'),
                                                                               StringValue('Association.from_port'): StringValue('from_A'),
                                                                               StringValue('Association.to_min'): IntegerValue(1),
                                                                               StringValue('Association.to_max'): InfiniteValue('+'),
                                                                               StringValue('Association.to_port'): StringValue('to_B')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.MM_A.A_to_B'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        ''' instance model '''
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.MM_A'),
                                      CreateConstants.LOCATION_KEY: LocationValue('models'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('MM_A.name'): StringValue('myModel')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.MM_A.A'),
                                      CreateConstants.LOCATION_KEY: LocationValue('models.myModel'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('A.name'): StringValue('a')})
                                      })
                        )
        self.assertFalse(self.mvk.conforms_to(LocationValue('models.myModel'), LocationValue('formalisms.MM_A')).get_result())

    def test_out_card_max(self):
        ''' type model MM_A '''
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('MM_A')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.MM_A'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.MM_A'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('A'),
                                                                               StringValue('Class.is_abstract'): BooleanValue(False),
                                                                               StringValue('Class.id_field'): StringValue('A.name')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.MM_A.A'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.MM_A'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('B'),
                                                                               StringValue('Class.is_abstract'): BooleanValue(False),
                                                                               StringValue('Class.id_field'): StringValue('B.name')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.MM_A.B'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.SimpleClassDiagrams.Association"),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.MM_A'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('from_class'): LocationValue('formalisms.MM_A.A'),
                                                                               StringValue('to_class'): LocationValue('formalisms.MM_A.B'),
                                                                               StringValue('Class.name'): StringValue('A_to_B'),
                                                                               StringValue('Class.is_abstract'): BooleanValue(False),
                                                                               StringValue('Class.id_field'): StringValue('A_to_B.name'),
                                                                               StringValue('Association.from_min'): IntegerValue(0),
                                                                               StringValue('Association.from_max'): InfiniteValue('+'),
                                                                               StringValue('Association.from_port'): StringValue('from_A'),
                                                                               StringValue('Association.to_min'): IntegerValue(1),
                                                                               StringValue('Association.to_max'): IntegerValue(1),
                                                                               StringValue('Association.to_port'): StringValue('to_B')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.MM_A.A_to_B'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        ''' instance model '''
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.MM_A'),
                                      CreateConstants.LOCATION_KEY: LocationValue('models'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('MM_A.name'): StringValue('myModel')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.MM_A.A'),
                                      CreateConstants.LOCATION_KEY: LocationValue('models.myModel'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('A.name'): StringValue('a')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.MM_A.B'),
                                      CreateConstants.LOCATION_KEY: LocationValue('models.myModel'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('B.name'): StringValue('b1')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.MM_A.B'),
                                      CreateConstants.LOCATION_KEY: LocationValue('models.myModel'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('B.name'): StringValue('b2')})
                                      })
                        )
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.MM_A.A_to_B'),
                                      CreateConstants.LOCATION_KEY: LocationValue('models.myModel'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('A_to_B.name'): StringValue('a_to_b1'),
                                                                               StringValue('from_A'): LocationValue('models.myModel.a'),
                                                                               StringValue('to_B'): LocationValue('models.myModel.b1')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.MM_A.A_to_B'),
                                      CreateConstants.LOCATION_KEY: LocationValue('models.myModel'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('A_to_B.name'): StringValue('a_to_b2'),
                                                                               StringValue('from_A'): LocationValue('models.myModel.a'),
                                                                               StringValue('to_B'): LocationValue('models.myModel.b2')})
                                      })
                        )
        self.assertFalse(self.mvk.conforms_to(LocationValue('models.myModel'), LocationValue('formalisms.MM_A')).get_result())

    def test_in_card_min(self):
        ''' type model MM_A '''
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('MM_A')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.MM_A'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.MM_A'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('A'),
                                                                               StringValue('Class.is_abstract'): BooleanValue(False),
                                                                               StringValue('Class.id_field'): StringValue('A.name')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.MM_A.A'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.MM_A'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('B'),
                                                                               StringValue('Class.is_abstract'): BooleanValue(False),
                                                                               StringValue('Class.id_field'): StringValue('B.name')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.MM_A.B'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.SimpleClassDiagrams.Association"),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.MM_A'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('from_class'): LocationValue('formalisms.MM_A.A'),
                                                                               StringValue('to_class'): LocationValue('formalisms.MM_A.B'),
                                                                               StringValue('Class.name'): StringValue('A_to_B'),
                                                                               StringValue('Class.is_abstract'): BooleanValue(False),
                                                                               StringValue('Class.id_field'): StringValue('A_to_B.name'),
                                                                               StringValue('Association.from_min'): IntegerValue(1),
                                                                               StringValue('Association.from_max'): InfiniteValue('+'),
                                                                               StringValue('Association.from_port'): StringValue('from_A'),
                                                                               StringValue('Association.to_min'): IntegerValue(0),
                                                                               StringValue('Association.to_max'): InfiniteValue('+'),
                                                                               StringValue('Association.to_port'): StringValue('to_B')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.MM_A.A_to_B'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        ''' instance model '''
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.MM_A'),
                                      CreateConstants.LOCATION_KEY: LocationValue('models'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('MM_A.name'): StringValue('myModel')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.MM_A.B'),
                                      CreateConstants.LOCATION_KEY: LocationValue('models.myModel'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('B.name'): StringValue('b')})
                                      })
                        )
        self.assertFalse(self.mvk.conforms_to(LocationValue('models.myModel'), LocationValue('formalisms.MM_A')).get_result())

    def test_in_card_max(self):
        ''' type model MM_A '''
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('MM_A')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.MM_A'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.MM_A'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('A'),
                                                                               StringValue('Class.is_abstract'): BooleanValue(False),
                                                                               StringValue('Class.id_field'): StringValue('A.name')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.MM_A.A'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.MM_A'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('B'),
                                                                               StringValue('Class.is_abstract'): BooleanValue(False),
                                                                               StringValue('Class.id_field'): StringValue('B.name')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.MM_A.B'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.SimpleClassDiagrams.Association"),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.MM_A'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('from_class'): LocationValue('formalisms.MM_A.A'),
                                                                               StringValue('to_class'): LocationValue('formalisms.MM_A.B'),
                                                                               StringValue('Class.name'): StringValue('A_to_B'),
                                                                               StringValue('Class.is_abstract'): BooleanValue(False),
                                                                               StringValue('Class.id_field'): StringValue('A_to_B.name'),
                                                                               StringValue('Association.from_min'): IntegerValue(1),
                                                                               StringValue('Association.from_max'): IntegerValue(1),
                                                                               StringValue('Association.from_port'): StringValue('from_A'),
                                                                               StringValue('Association.to_min'): IntegerValue(1),
                                                                               StringValue('Association.to_max'): InfiniteValue('+'),
                                                                               StringValue('Association.to_port'): StringValue('to_B')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.MM_A.A_to_B'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        ''' instance model '''
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.MM_A'),
                                      CreateConstants.LOCATION_KEY: LocationValue('models'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('MM_A.name'): StringValue('myModel')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.MM_A.A'),
                                      CreateConstants.LOCATION_KEY: LocationValue('models.myModel'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('A.name'): StringValue('a1')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.MM_A.A'),
                                      CreateConstants.LOCATION_KEY: LocationValue('models.myModel'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('A.name'): StringValue('a2')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.MM_A.B'),
                                      CreateConstants.LOCATION_KEY: LocationValue('models.myModel'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('B.name'): StringValue('b')})
                                      })
                        )
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.MM_A.A_to_B'),
                                      CreateConstants.LOCATION_KEY: LocationValue('models.myModel'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('A_to_B.name'): StringValue('a1_to_b'),
                                                                               StringValue('from_A'): LocationValue('models.myModel.a1'),
                                                                               StringValue('to_B'): LocationValue('models.myModel.b')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.MM_A.A_to_B'),
                                      CreateConstants.LOCATION_KEY: LocationValue('models.myModel'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('A_to_B.name'): StringValue('a2_to_b'),
                                                                               StringValue('from_A'): LocationValue('models.myModel.a2'),
                                                                               StringValue('to_B'): LocationValue('models.myModel.b')})
                                      })
                        )
        self.assertFalse(self.mvk.conforms_to(LocationValue('models.myModel'), LocationValue('formalisms.MM_A')).get_result())


if __name__ == "__main__":
    unittest.main()
