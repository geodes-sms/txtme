'''
Created on 19-mrt.-2014

@author: Simon
'''
import logging
import unittest

from mvk.impl.python.constants import CreateConstants
from mvk.impl.python.datatype import StringType, BooleanType, IntegerType, \
    TypeFactory, TypeType, AnyType
from mvk.impl.python.datavalue import MappingValue, LocationValue, StringValue, \
    IntegerValue, BooleanValue, InfiniteValue, AnyValue


class TestEverything(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName=methodName)
        from mvk.mvk import MvK
        self.mvk = MvK()

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.mvk.clear()

    def tearDown(self):
        self.mvk.clear()
        unittest.TestCase.tearDown(self)

    def test_petrinets(self):
        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('formalisms'),
                                           CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('Petrinets')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        rl = self.mvk.read(LocationValue('formalisms.Petrinets'))
        self.assertTrue(rl.is_success(), rl)

        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets'),
                                           CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Place'),
                                                                                    StringValue('Class.is_abstract'): BooleanValue(False),
                                                                                    StringValue('Class.id_field'): StringValue('Place.name')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        rl = self.mvk.read(LocationValue('formalisms.Petrinets.Place'))
        self.assertTrue(rl.is_success(), rl)

        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets.Place'),
                                           CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                                    StringValue('Attribute.type'): StringType(),
                                                                                    StringValue('Attribute.default'): StringValue('')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        rl = self.mvk.read(LocationValue('formalisms.Petrinets.Place.name'))
        self.assertTrue(rl.is_success(), rl)

        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets.Place'),
                                           CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('tokens'),
                                                                                    StringValue('Attribute.type'): IntegerType(),
                                                                                    StringValue('Attribute.default'): IntegerValue(0)})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        rl = self.mvk.read(LocationValue('formalisms.Petrinets.Place.tokens'))
        self.assertTrue(rl.is_success(), rl)

        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets'),
                                           CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Transition'),
                                                                                    StringValue('Class.is_abstract'): BooleanValue(False),
                                                                                    StringValue('Class.id_field'): StringValue('Transition.name')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        rl = self.mvk.read(LocationValue('formalisms.Petrinets.Transition'))
        self.assertTrue(rl.is_success(), rl)

        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets.Transition'),
                                           CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                                    StringValue('Attribute.type'): StringType(),
                                                                                    StringValue('Attribute.default'): StringValue('')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        rl = self.mvk.read(LocationValue('formalisms.Petrinets.Transition.name'))
        self.assertTrue(rl.is_success(), rl)

        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets'),
                                           CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Association'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('P2T'),
                                                                                    StringValue('Class.is_abstract'): BooleanValue(False),
                                                                                    StringValue('Class.id_field'): StringValue('P2T.name'),
                                                                                    StringValue('from_class'): LocationValue('formalisms.Petrinets.Place'),
                                                                                    StringValue('to_class'): LocationValue('formalisms.Petrinets.Transition'),
                                                                                    StringValue('Association.from_min'): IntegerValue(0),
                                                                                    StringValue('Association.from_max'): InfiniteValue('+'),
                                                                                    StringValue('Association.from_port'): StringValue('from_place'),
                                                                                    StringValue('Association.to_min'): IntegerValue(0),
                                                                                    StringValue('Association.to_max'): InfiniteValue('+'),
                                                                                    StringValue('Association.to_port'): StringValue('to_transition')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        rl = self.mvk.read(LocationValue('formalisms.Petrinets.P2T'))
        self.assertTrue(rl.is_success(), rl)

        cl = self.mvk.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets'),
                                           CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Association'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('T2P'),
                                                                                    StringValue('Class.is_abstract'): BooleanValue(False),
                                                                                    StringValue('Class.id_field'): StringValue('T2P.name'),
                                                                                    StringValue('from_class'): LocationValue('formalisms.Petrinets.Transition'),
                                                                                    StringValue('to_class'): LocationValue('formalisms.Petrinets.Place'),
                                                                                    StringValue('Association.from_min'): IntegerValue(0),
                                                                                    StringValue('Association.from_max'): InfiniteValue('+'),
                                                                                    StringValue('Association.from_port'): StringValue('from_transition'),
                                                                                    StringValue('Association.to_min'): IntegerValue(0),
                                                                                    StringValue('Association.to_max'): InfiniteValue('+'),
                                                                                    StringValue('Association.to_port'): StringValue('to_place')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        rl = self.mvk.read(LocationValue('formalisms.Petrinets.T2P'))
        self.assertTrue(rl.is_success(), rl)

if __name__ == "__main__":
    unittest.main()
