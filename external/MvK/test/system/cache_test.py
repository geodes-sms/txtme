import unittest

from mvk.impl.python.constants import CreateConstants, UpdateConstants
from mvk.impl.python.datatype import IntegerType, StringType, TypeFactory, BooleanType, FloatType, TypeType, AnyType, InfiniteType
from mvk.impl.python.datavalue import MappingValue, LocationValue, StringValue, IntegerValue, SequenceValue, BooleanValue, InfiniteValue, DataValueFactory, \
    FloatValue, AnyValue, TupleValue
from mvk.impl.python.exception import MvKKeyError
from mvk.impl.python.object import Model, ModelReference, Clabject, ClabjectReference, Attribute, Association, AssociationEnd, AssociationReference, Inherits, \
    Composition
from mvk.impl.python.python_representer import PythonRepresenter
from mvk.mvk import MvK
from mvk.impl.formalisms.StoreMapper import StoreMapper


class CacheTestCase(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName=methodName)
        self.mvk = MvK()

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.mvk.clear()

    def tearDown(self):
        self.mvk.clear()
        unittest.TestCase.tearDown(self)

    def create_petrinets(self):
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('Petrinets')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Place'),
                                                                               StringValue('Class.is_abstract'): BooleanValue(False),
                                                                               StringValue('Class.id_field'): StringValue('Place.name')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets.Place'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('tokens'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('IntegerType'),
                                                                               StringValue('Attribute.default'): IntegerValue(0)})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets.Place'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Transition'),
                                                                               StringValue('Class.is_abstract'): BooleanValue(False),
                                                                               StringValue('Class.id_field'): StringValue('Transition.name')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets.Transition'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.SimpleClassDiagrams.Association"),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('from_class'): LocationValue('formalisms.Petrinets.Place'),
                                                                               StringValue('to_class'): LocationValue('formalisms.Petrinets.Transition'),
                                                                               StringValue('Class.name'): StringValue('P2T'),
                                                                               StringValue('Class.is_abstract'): BooleanValue(False),
                                                                               StringValue('Class.id_field'): StringValue('P2T.name'),
                                                                               StringValue('Association.from_min'): IntegerValue(0),
                                                                               StringValue('Association.from_max'): InfiniteValue('+'),
                                                                               StringValue('Association.from_port'): StringValue('from_place'),
                                                                               StringValue('Association.to_min'): IntegerValue(0),
                                                                               StringValue('Association.to_max'): InfiniteValue('+'),
                                                                               StringValue('Association.to_port'): StringValue('to_transition')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets.P2T'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.SimpleClassDiagrams.Association"),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('from_class'): LocationValue('formalisms.Petrinets.Transition'),
                                                                               StringValue('to_class'): LocationValue('formalisms.Petrinets.Place'),
                                                                               StringValue('Class.name'): StringValue('T2P'),
                                                                               StringValue('Class.is_abstract'): BooleanValue(False),
                                                                               StringValue('Class.id_field'): StringValue('T2P.name'),
                                                                               StringValue('Association.from_min'): IntegerValue(0),
                                                                               StringValue('Association.from_max'): InfiniteValue('+'),
                                                                               StringValue('Association.from_port'): StringValue('from_transition'),
                                                                               StringValue('Association.to_min'): IntegerValue(0),
                                                                               StringValue('Association.to_max'): InfiniteValue('+'),
                                                                               StringValue('Association.to_port'): StringValue('to_place')})
                                      })
                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets.T2P'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        self.assertTrue(self.mvk.conforms_to(LocationValue('formalisms.Petrinets'), LocationValue('protected.formalisms.SimpleClassDiagrams')).get_result())


    def test_cache_read(self):
        self.create_petrinets()

        # First do an ordinary read of everything, hierarchically ordered
        self.assertTrue(self.mvk.read(LocationValue("")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Place")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Place.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Place.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Place.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Place.tokens")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Transition")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Transition.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Transition.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Transition.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Transition.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.P2T")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.P2T.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.T2P")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.T2P.name")).is_success())

        # Kill the cache ourself, note that this should normally not be done...
        self.mvk.read_cache.clear()

        # Now read again, but in a non-hierarchical order
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.P2T.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Place.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Place.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Place.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.T2P.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Place.tokens")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.P2T")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Transition")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Place")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Transition.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Transition.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Transition.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Transition.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.T2P")).is_success())

    def test_cache_update(self):
        self.create_petrinets()

        # First do an ordinary read of everything, hierarchically ordered
        self.assertTrue(self.mvk.read(LocationValue("")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Place")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Place.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Place.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Place.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Place.tokens")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Transition")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Transition.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Transition.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Transition.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Transition.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.P2T")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.P2T.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.T2P")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.T2P.name")).is_success())

        # Now update the name of the Petrinets formalism
        ul = self.mvk.update(
                MappingValue({UpdateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                              UpdateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets'),
                              UpdateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('My_Petrinets')})
                             })
                )
        self.assertTrue(ul.is_success(), ul)

        # Read again in non-hierarchical method, but now on the new name, mixed with on the old name
        # Reads on the old name should fail (but might still be in cache!)
        # Reads on the new name should succeed (but might not yet be in cache!)
        self.assertFalse(self.mvk.read(LocationValue("formalisms.Petrinets.P2T.name")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("formalisms.Petrinets.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.My_Petrinets.Transition")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.My_Petrinets.Place")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("formalisms.Petrinets.Place.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.My_Petrinets.Place.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("formalisms.Petrinets")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.My_Petrinets.Transition.Class.id_field")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("formalisms.Petrinets.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.My_Petrinets.P2T")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("formalisms.Petrinets.Place.Class.id_field")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("formalisms.Petrinets.Place.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.My_Petrinets.Place.tokens")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("formalisms.Petrinets.T2P.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.My_Petrinets.T2P")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.My_Petrinets.Transition.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.My_Petrinets.Place.name")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("formalisms.Petrinets.Place.tokens")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.My_Petrinets.Place.Class.id_field")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("formalisms.Petrinets.P2T")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.My_Petrinets.Transition.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.My_Petrinets.Transition.Class.name")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("formalisms.Petrinets.Transition")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("formalisms.Petrinets.Place")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("formalisms.Petrinets.Transition.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.My_Petrinets.T2P.name")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("formalisms.Petrinets.Transition.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.My_Petrinets.Place.Class.is_abstract")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("formalisms.Petrinets.Transition.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("formalisms.Petrinets.Transition.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.My_Petrinets.P2T.name")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("formalisms.Petrinets.T2P")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.My_Petrinets")).is_success())

    def test_cache_update_root(self):
        self.create_petrinets()

        # First do an ordinary read of everything, hierarchically ordered
        self.assertTrue(self.mvk.read(LocationValue("")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Place")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Place.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Place.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Place.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Place.tokens")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Transition")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Transition.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Transition.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Transition.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.Transition.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.P2T")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.P2T.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.T2P")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms.Petrinets.T2P.name")).is_success())

        # Now update the name of the Petrinets formalism
        ul = self.mvk.update(
                MappingValue({UpdateConstants.TYPE_KEY: LocationValue('mvk.object.Package'),
                              UpdateConstants.LOCATION_KEY: LocationValue('formalisms'),
                              UpdateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('formalisms_v2')})
                             })
                )
        self.assertTrue(ul.is_success(), ul)

        # Test again in different order
        # This is different from normal updates, as the topmost package doesn't have a link to destroy for invalidation
        self.assertFalse(self.mvk.read(LocationValue("formalisms.Petrinets.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms_v2")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms_v2.Petrinets")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms_v2.Petrinets.Place")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("formalisms.Petrinets.Transition.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms_v2.Petrinets.Place.name")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("formalisms.Petrinets.Transition")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms_v2.Petrinets.Place.Class.name")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("formalisms.Petrinets.P2T.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms_v2.Petrinets.Place.Class.is_abstract")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("formalisms.Petrinets.Place.tokens")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("formalisms.Petrinets.T2P.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms_v2.Petrinets.Place.Class.id_field")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("formalisms.Petrinets.P2T")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms_v2.Petrinets.Place.tokens")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("formalisms.Petrinets.Transition.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms_v2.Petrinets.Transition")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("formalisms.Petrinets.Place.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms_v2.Petrinets.Transition.name")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("formalisms.Petrinets")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("formalisms.Petrinets.Transition.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms_v2.Petrinets.Transition.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms_v2.Petrinets.Transition.Class.is_abstract")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("formalisms.Petrinets.Place.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms_v2.Petrinets.Transition.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms_v2.Petrinets.P2T")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("formalisms.Petrinets.Place.Class.is_abstract")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("formalisms")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms_v2.Petrinets.P2T.name")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("formalisms.Petrinets.Transition.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms_v2.Petrinets.T2P")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("formalisms.Petrinets.T2P")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("formalisms_v2.Petrinets.T2P.name")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("formalisms.Petrinets.Place")).is_success())

#if __name__ == "__main__":
def runTests():
    unittest.main()
