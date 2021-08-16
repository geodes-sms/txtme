from mvk.impl.python.constants import CreateConstants, UpdateConstants
from mvk.impl.python.datatype import IntegerType, StringType, TypeFactory, BooleanType, FloatType, TypeType, AnyType, InfiniteType
from mvk.impl.python.datavalue import MappingValue, LocationValue, StringValue, IntegerValue, SequenceValue, BooleanValue, InfiniteValue, DataValueFactory, FloatValue, AnyValue, TupleValue
from mvk.impl.python.object import Model, ModelReference, Clabject, ClabjectReference, Attribute, Association, AssociationEnd, AssociationReference, Inherits, Composition
from mvk.mvk import MvK
from mvk.impl.formalisms.StoreMapper import StoreMapper
from mvk.impl.python.util.jsonserializer import MvKEncoder

from pythonBenchmark.mvkWrapper import MvKWrapper

class MvKTest():
    def noop(self, *args, **kwargs):
        pass

    def clear(self):
        self.mvk.clear()

    def __getattr__(self, name):
        return self.noop

    def __init__(self):
        self.mvk = MvKWrapper("localhost", "8000", "http")
        #self.mvk = MvK()
        self.mvk.clear()

    def create_petrinets(self):
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('Petrinets')})
                                      })
                        )
        self.mvk.read(LocationValue('formalisms.Petrinets'))
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        self.mvk.read(LocationValue('formalisms.Petrinets.name'))
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Place'),
                                                                               StringValue('Class.is_abstract'): BooleanValue(False),
                                                                               StringValue('Class.id_field'): StringValue('Place.name')})
                                      })
                        )
        self.mvk.read(LocationValue('formalisms.Petrinets.Place'))
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets.Place'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('tokens'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('IntegerType'),
                                                                               StringValue('Attribute.default'): IntegerValue(0)})
                                      })
                        )
        self.mvk.read(LocationValue('formalisms.Petrinets.Place.tokens'))
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets.Place'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        self.mvk.read(LocationValue('formalisms.Petrinets.Place.name'))
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Transition'),
                                                                               StringValue('Class.is_abstract'): BooleanValue(False),
                                                                               StringValue('Class.id_field'): StringValue('Transition.name')})
                                      })
                        )
        self.mvk.read(LocationValue('formalisms.Petrinets.Transition'))
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets.Transition'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        self.mvk.read(LocationValue('formalisms.Petrinets.Transition.name'))
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
        self.mvk.read(LocationValue('formalisms.Petrinets.P2T'))
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets.P2T'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        self.mvk.read(LocationValue('formalisms.Petrinets.P2T.name'))
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
        self.mvk.read(LocationValue('formalisms.Petrinets.T2P'))
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets.T2P'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        self.mvk.read(LocationValue('formalisms.Petrinets.T2P.name'))
        self.mvk.conforms_to(LocationValue('formalisms.Petrinets'), LocationValue('protected.formalisms.SimpleClassDiagrams'))

        # Read everything
        self.mvk.read(LocationValue('formalisms.Petrinets'))
        self.mvk.read(LocationValue('formalisms.Petrinets.name'))
        self.mvk.read(LocationValue('formalisms.Petrinets.Place'))
        self.mvk.read(LocationValue('formalisms.Petrinets.Place.tokens'))
        self.mvk.read(LocationValue('formalisms.Petrinets.Place.name'))
        self.mvk.read(LocationValue('formalisms.Petrinets.Transition'))
        self.mvk.read(LocationValue('formalisms.Petrinets.Transition.name'))
        self.mvk.read(LocationValue('formalisms.Petrinets.P2T'))
        self.mvk.read(LocationValue('formalisms.Petrinets.P2T.name'))
        self.mvk.read(LocationValue('formalisms.Petrinets.T2P'))
        self.mvk.read(LocationValue('formalisms.Petrinets.T2P.name'))

    def test_create(self):
        ''' Let's create the most used example ever... A Petrinets formalism! '''
        ''' First, the Petrinets type model, which should conform to SCD. '''
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('Petrinets')})
                                           })
                             )
        self.mvk.read(LocationValue('formalisms.Petrinets'))
        self.mvk.read(LocationValue('formalisms.Petrinets.name'))

        ''' Then, some classes... '''
        """ PLACE """
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
        self.mvk.read(LocationValue('formalisms.Petrinets.Place.Class.name'))
        self.mvk.read(LocationValue('formalisms.Petrinets.Place.Class.is_abstract'))
        self.mvk.read(LocationValue('formalisms.Petrinets.Place.Class.id_field'))
        self.mvk.read(LocationValue('formalisms.Petrinets.Place'))

        """ TRANSITION """
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Transition'),
                                                                                    StringValue('Class.is_abstract'): BooleanValue(False),
                                                                                    StringValue('Class.id_field'): StringValue('Transition.name')})
                                           })
                             )
        self.mvk.read(LocationValue('formalisms.Petrinets.Transition.Class.name'))
        self.mvk.read(LocationValue('formalisms.Petrinets.Transition.Class.is_abstract'))
        self.mvk.read(LocationValue('formalisms.Petrinets.Transition.Class.id_field'))
        self.mvk.read(LocationValue('formalisms.Petrinets.Transition'))

        """ P2T """
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.SimpleClassDiagrams.Association"),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('to_class'): LocationValue('formalisms.Petrinets.Transition'),
                                                                                    StringValue('from_class'): LocationValue('formalisms.Petrinets.Place'),
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
        self.mvk.read(LocationValue('formalisms.Petrinets.P2T'))

        """ T2P """
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
        self.mvk.read(LocationValue('formalisms.Petrinets.T2P'))

    def test_instantiation(self):
        self.create_petrinets()
        ''' Let's create an instance of a Petrinet... '''
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.Petrinets'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Petrinets.name'): StringValue('myPetrinet')})
                                           })
                             )
        self.mvk.read(LocationValue('models.myPetrinet'))

        ''' p1 should get the default value for the attribute 'tokens' '''
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.Petrinets.Place'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.myPetrinet'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Place.name'): StringValue('p1')})
                                           })
                             )
        self.mvk.read(LocationValue('models.myPetrinet.p1'))

        ''' p2 gets a value for 'tokens' '''
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.Petrinets.Place'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.myPetrinet'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Place.name'): StringValue('p2'),
                                                                                    StringValue('Place.tokens'): IntegerValue(10)})
                                           })
                             )
        self.mvk.read(LocationValue('models.myPetrinet.p2'))

        ''' instantiating transition '''
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.Petrinets.Transition'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.myPetrinet'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Transition.name'): StringValue('t1')})
                                           })
                             )
        self.mvk.read(LocationValue('models.myPetrinet.t1'))

        ''' instantiating P2T '''
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.Petrinets.P2T'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.myPetrinet'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('P2T.name'): StringValue('p2_to_t1'),
                                                                                    StringValue('from_place'): LocationValue('models.myPetrinet.p2'),
                                                                                    StringValue('to_transition'): LocationValue('models.myPetrinet.t1')})
                                           })
                             )
        self.mvk.read(LocationValue('models.myPetrinet.p2_to_t1'))

        ''' instantiating T2P '''
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.Petrinets.T2P'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.myPetrinet'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('T2P.name'): StringValue('t1_to_p1'),
                                                                                    StringValue('from_transition'): LocationValue('models.myPetrinet.t1'),
                                                                                    StringValue('to_place'): LocationValue('models.myPetrinet.p1')})
                                           })
                             )
        self.mvk.read(LocationValue('models.myPetrinet.t1_to_p1'))

        ''' conformance check '''
        self.mvk.conforms_to(LocationValue('models.myPetrinet'), LocationValue('formalisms.Petrinets'))

    def test_errors(self):
        self.create_petrinets()
        ''' Let's try to break some stuff... '''

        ''' Create an already existing Model '''
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('Petrinets')})
                                           })
                             )

        ''' Create an already existing Clabject '''
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Place'),
                                                                                    StringValue('Class.is_abstract'): BooleanValue(True),
                                                                                    StringValue('Class.id_field'): StringValue('Place.name')})
                                           })
                             )
        self.mvk.read(LocationValue('formalisms.Petrinets.Place'))

        ''' Create an already existing Association '''
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Association'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('from_class'): LocationValue('formalisms.Petrinets.Place'),
                                                                                    StringValue('to_class'): LocationValue('formalisms.Petrinets.Transition'),
                                                                                    StringValue('Class.name'): StringValue('P2T'),
                                                                                    StringValue('Class.is_abstract'): BooleanValue(True),
                                                                                    StringValue('Class.id_field'): StringValue('P2T.name'),
                                                                                    StringValue('Association.from_min'): IntegerValue(0),
                                                                                    StringValue('Association.from_max'): InfiniteValue('+'),
                                                                                    StringValue('Association.from_port'): StringValue('from_place'),
                                                                                    StringValue('Association.to_min'): IntegerValue(0),
                                                                                    StringValue('Association.to_max'): InfiniteValue('+'),
                                                                                    StringValue('Association.to_port'): StringValue('to_transition')}
                                                                                   )}
                                          )
                             )
        self.mvk.read(LocationValue('formalisms.Petrinets.P2T'))

        ''' Create an already existing Attribute '''
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets.Place'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('tokens'),
                                                                                    StringValue('Attribute.type'): TypeFactory.get_type('IntegerType'),
                                                                                    StringValue('Attribute.default'): IntegerValue(-1)})
                                           })
                             )
        self.mvk.read(LocationValue('formalisms.Petrinets.Place.tokens'))

        ''' Create an element in an invalid location. '''
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.CBD'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Block'),
                                                                                    StringValue('Class.is_abstract'): BooleanValue(True),
                                                                                    StringValue('Class.id_field'): StringValue('Place.name')})
                                           })
                             )

        ''' Read from invalid locations. '''
        self.mvk.read(LocationValue('formalisms..'))
        self.mvk.read(LocationValue('formalisms.'))

        ''' Try to create a model in a package which does not yet exist.
        However, the package is named the same as a clabject in the parent
        package.'''
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets.Place'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('TestModel')})
                                           })
                             )
        self.mvk.read(LocationValue('formalisms.Petrinets.Place.TestClabject'))

    def test_inheritance(self):
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('TestSubTyping')})
                                               })
                                 )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Element'),
                                                                                        StringValue('Class.is_abstract'): BooleanValue(True)})
                                               })
                                 )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                                   CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping.Element'),
                                                   CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('an_int'),
                                                                                            StringValue('Attribute.type'): TypeFactory.get_type('IntegerType'),
                                                                                            StringValue('Attribute.default'): IntegerValue(0)})
                                                   })
                                     )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                                  CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping.Element'),
                                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('a_str'),
                                                                                           StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                                           StringValue('Attribute.default'): StringValue('test')})
                                                  })
                                    )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                                        CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping'),
                                                        CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('LocationElement'),
                                                                                                 StringValue('Class.is_abstract'): BooleanValue(True)})
                                                        })
                                          )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                                     CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping.LocationElement'),
                                                     CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('location'),
                                                                                              StringValue('Attribute.type'): TypeFactory.get_type('TupleType(IntegerType, IntegerType)'),
                                                                                              StringValue('Attribute.default'): DataValueFactory.create_instance((0, 0))})
                                                     })
                                       )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('le_i_el'),
                                                                                        StringValue('from_class'): LocationValue('formalisms.TestSubTyping.LocationElement'),
                                                                                        StringValue('to_class'): LocationValue('formalisms.TestSubTyping.Element')})
                                               })
                                 )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                                     CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping'),
                                                     CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('NamedElement'),
                                                                                              StringValue('Class.is_abstract'): BooleanValue(True),
                                                                                              StringValue('Class.id_field'): StringValue('NamedElement.name')})
                                                     })
                                       )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                                     CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping.NamedElement'),
                                                     CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                                              StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                                              StringValue('Attribute.default'): StringValue('')})
                                                     })
                                       )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('ne_i_el'),
                                                                                        StringValue('from_class'): LocationValue('formalisms.TestSubTyping.NamedElement'),
                                                                                        StringValue('to_class'): LocationValue('formalisms.TestSubTyping.Element')})
                                               })
                                 )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping'),
                                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Character'),
                                                                                               StringValue('Class.is_abstract'): BooleanValue(False)})
                                                      })
                                        )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                                     CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping.Character'),
                                                     CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('fighting_strength'),
                                                                                              StringValue('Attribute.type'): TypeFactory.get_type('IntegerType'),
                                                                                              StringValue('Attribute.default'): IntegerValue(100)})
                                                     })
                                       )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('c_i_ne'),
                                                                                        StringValue('from_class'): LocationValue('formalisms.TestSubTyping.Character'),
                                                                                        StringValue('to_class'): LocationValue('formalisms.TestSubTyping.NamedElement')})
                                               })
                                 )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('c_i_le'),
                                                                                        StringValue('from_class'): LocationValue('formalisms.TestSubTyping.Character'),
                                                                                        StringValue('to_class'): LocationValue('formalisms.TestSubTyping.LocationElement')})
                                               })
                                 )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                                 CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping'),
                                                 CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Hero'),
                                                                                          StringValue('Class.is_abstract'): BooleanValue(False)})
                                                 })
                                   )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                                   CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping.Hero'),
                                                   CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('points'),
                                                                                            StringValue('Attribute.type'): TypeFactory.get_type('IntegerType'),
                                                                                            StringValue('Attribute.default'): IntegerValue(0)})
                                                   })
                                     )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('h_i_c'),
                                                                                        StringValue('from_class'): LocationValue('formalisms.TestSubTyping.Hero'),
                                                                                        StringValue('to_class'): LocationValue('formalisms.TestSubTyping.Character')})
                                               })
                                 )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                                 CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping'),
                                                 CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Door'),
                                                                                          StringValue('Class.is_abstract'): BooleanValue(False)})
                                                 })
                                   )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping.Door'),
                                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('is_locked'),
                                                                                               StringValue('Attribute.type'): TypeFactory.get_type('BooleanType'),
                                                                                               StringValue('Attribute.default'): BooleanValue(False)})
                                                      })
                                     )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('d_i_ne'),
                                                                                        StringValue('from_class'): LocationValue('formalisms.TestSubTyping.Door'),
                                                                                        StringValue('to_class'): LocationValue('formalisms.TestSubTyping.NamedElement')})
                                               })
                                 )
        self.mvk.read(LocationValue('formalisms.TestSubTyping.le_i_el'))
        self.mvk.read(LocationValue('formalisms.TestSubTyping.Element'))
        self.mvk.read(LocationValue('formalisms.TestSubTyping.NamedElement'))
        self.mvk.read(LocationValue('formalisms.TestSubTyping.LocationElement'))
        self.mvk.read(LocationValue('formalisms.TestSubTyping.Character'))
        self.mvk.read(LocationValue('formalisms.TestSubTyping.Hero'))
        self.mvk.read(LocationValue('formalisms.TestSubTyping.Door'))

        ''' As the locations differ, it will check whether their contents
        are equal. '''
        self.mvk.read(LocationValue('formalisms.TestSubTyping'))

        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.TestSubTyping'),
                                                                  CreateConstants.LOCATION_KEY: LocationValue('models'),
                                                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('TestSubTyping.name'): StringValue('testModel')})
                                                                  })
                                                    )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.TestSubTyping.Hero'),
                                                         CreateConstants.LOCATION_KEY: LocationValue('models.testModel'),
                                                         CreateConstants.ATTRS_KEY: MappingValue({StringValue('NamedElement.name'): StringValue('Simon')})
                                                         })
                                           )
        self.mvk.read(LocationValue('models.testModel.Simon'))

    def test_composition(self):
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('mvk.object.Model'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('TestComposition'),
                                                                                        StringValue('type_model'): LocationValue('mvk.object')})
                                               })
                                 )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                                CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestComposition'),
                                                CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('Car'),
                                                                                         StringValue('abstract'): BooleanValue(False),
                                                                                         StringValue('class'): LocationValue('mvk.object.Clabject')})
                                                })
                                 )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                                  CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestComposition'),
                                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('Wheel'),
                                                                                           StringValue('abstract'): BooleanValue(False),
                                                                                           StringValue('class'): LocationValue('mvk.object.Clabject')})
                                                  })
                                    )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue("mvk.object.Composition"),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestComposition'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('from_multiplicity'): MappingValue({StringValue('node'): LocationValue('formalisms.TestComposition.Car'),
                                                                                                                                    StringValue('port_name'): StringValue('from_car'),
                                                                                                                                    StringValue('lower'): IntegerValue(1),
                                                                                                                                    StringValue('upper'): IntegerValue(1)}),
                                                                                    StringValue('to_multiplicity'): MappingValue({StringValue('node'): LocationValue('formalisms.TestComposition.Wheel'),
                                                                                                                                  StringValue('port_name'): StringValue('to_wheel'),
                                                                                                                                  StringValue('lower'): IntegerValue(2),
                                                                                                                                  StringValue('upper'): IntegerValue(4)}),
                                                                                    StringValue('class'): LocationValue('mvk.object.Composition'),
                                                                                    StringValue('name'): StringValue('car_wheel'),
                                                                                    StringValue('abstract'): BooleanValue(False)})
                                           })
                             )

    def test_delete(self):
        self.create_petrinets()
        self.mvk.delete(LocationValue('formalisms.Petrinets.Place.tokens'))
        self.mvk.read(LocationValue('formalisms.Petrinets.Place.tokens'))
        self.mvk.delete(LocationValue('formalisms.Petrinets.Place'))
        self.mvk.read(LocationValue('formalisms.Petrinets.Place'))
        self.mvk.delete(LocationValue('formalisms.Petrinets.P2T'))
        self.mvk.read(LocationValue('formalisms.Petrinets.P2T'))
        self.mvk.delete(LocationValue('formalisms.Petrinets.T2P'))
        self.mvk.read(LocationValue('formalisms.Petrinets.T2P'))
        self.mvk.delete(LocationValue('formalisms.Petrinets'))
        self.mvk.read(LocationValue('formalisms.Petrinets.Transition'))
        self.mvk.read(LocationValue('formalisms.Petrinets.P2T'))
        self.mvk.read(LocationValue('formalisms.Petrinets'))

    def test_update(self):
        self.create_petrinets()
        ''' update association '''
        self.mvk.update(MappingValue({UpdateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Association'),
                                           UpdateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets.P2T'),
                                           UpdateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('PlaceToTransition')})
                                           })
                             )
        self.mvk.read(LocationValue('formalisms.Petrinets.P2T'))
        self.mvk.read(LocationValue('formalisms.Petrinets.PlaceToTransition'))

        ''' update association ends '''
        self.mvk.update(MappingValue({UpdateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Association'),
                                           UpdateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets.PlaceToTransition'),
                                           UpdateConstants.ATTRS_KEY: MappingValue({StringValue('from_class'): LocationValue('formalisms.Petrinets.Transition'),
                                                                                    StringValue('to_class'): LocationValue('formalisms.Petrinets.Place'),
                                                                                    StringValue('Class.name'): StringValue('TransitionToPlace'),
                                                                                    StringValue('Association.from_port'): StringValue('from_transition'),
                                                                                    StringValue('Association.from_min'): IntegerValue(3),
                                                                                    StringValue('Association.from_max'): IntegerValue(10),
                                                                                    StringValue('Association.to_port'): StringValue('to_place'),
                                                                                    StringValue('Association.to_min'): IntegerValue(5),
                                                                                    StringValue('Association.to_max'): IntegerValue(15)})
                                           })
                             )
        self.mvk.read(LocationValue('formalisms.Petrinets.PlaceToTransition'))
        self.mvk.read(LocationValue('formalisms.Petrinets.TransitionToPlace'))
        self.mvk.read(LocationValue('formalisms.Petrinets.Transition'))
        self.mvk.read(LocationValue('formalisms.Petrinets.Place'))

        ''' update class '''
        self.mvk.update(MappingValue({UpdateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                           UpdateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets.Place'),
                                           UpdateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('MyPlaais')})
                                           })
                             )
        self.mvk.read(LocationValue('formalisms.Petrinets.Place'))
        self.mvk.read(LocationValue('formalisms.Petrinets.MyPlaais'))

        ''' update attribute '''
        self.mvk.update(MappingValue({UpdateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                           UpdateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets.MyPlaais.tokens'),
                                           UpdateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('plaais_tokens'),
                                                                                    StringValue('Attribute.type'): TypeFactory.get_type("FloatType"),
                                                                                    StringValue('Attribute.default'): FloatValue(5.0)})
                                           }))
        self.mvk.read(LocationValue('formalisms.Petrinets.MyPlaais.tokens'))
        self.mvk.read(LocationValue('formalisms.Petrinets.Place.tokens'))
        self.mvk.read(LocationValue('formalisms.Petrinets.MyPlaais.plaais_tokens'))

        ''' update package '''
        self.mvk.update(MappingValue({UpdateConstants.TYPE_KEY: LocationValue('mvk.object.Package'),
                                           UpdateConstants.LOCATION_KEY: LocationValue('formalisms'),
                                           UpdateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('my_formalisms')})
                                           })
                             )
        self.mvk.read(LocationValue('formalisms'))
        self.mvk.read(LocationValue('my_formalisms'))

        ''' update model '''
        self.mvk.update(MappingValue({UpdateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                           UpdateConstants.LOCATION_KEY: LocationValue('my_formalisms.Petrinets'),
                                           UpdateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('PetrinetFormalism')})
                                           })
                             )
        self.mvk.read(LocationValue('my_formalisms.Petrinets'))
        self.mvk.read(LocationValue('my_formalisms.PetrinetFormalism'))

    def test_action_language(self):
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
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('ActionLanguage.name'): StringValue('test_model')})
                                           })
                             )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Function'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Function.name'): StringValue('f'),
                                                                                    StringValue('Function.type'): TypeFactory.get_type('StringType')})
                                           })
                             )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Parameter'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Parameter.name'): StringValue('a'),
                                                                                    StringValue('Parameter.type'): TypeFactory.get_type('IntegerType'),
                                                                                    StringValue('Parameter.parameter_type'): StringValue('in')})
                                           })
                             )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Parameter'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Parameter.name'): StringValue('b'),
                                                                                    StringValue('Parameter.type'): TypeFactory.get_type('FloatType'),
                                                                                    StringValue('Parameter.parameter_type'): StringValue('in')})
                                           })
                             )
        '''
        package test
            model test_model:
                string f(a: int, b: float) {
                    int i = 5
        '''
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.DeclarationStatement'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Statement.name'): StringValue('decl_i')})
                                           })
                             )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Identifier'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.decl_i'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Expression.name'): StringValue('i')})
                                           })
                             )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Constant'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.decl_i'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Expression.name'): StringValue('five'),
                                                                                    StringValue('Constant.value'): IntegerValue(5)})
                                           })
                             )
        '''
        package test
            model test_model:
                string f(a: int, b: float) {
                    int i = 5
                    while i > 0:
        '''
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.WhileLoop'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Statement.name'): StringValue('while_1')})
                                           })
                             )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.GreaterThan'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Expression.name'): StringValue('while_1_expr')})
                                           })
                             )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Navigation'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1.while_1_expr'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Expression.name'): StringValue('i'),
                                                                                    StringValue('Navigation.path'): LocationValue('i')})
                                           })
                             )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Constant'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1.while_1_expr'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Expression.name'): StringValue('zero'),
                                                                                    StringValue('Navigation.value'): IntegerValue(0)})
                                           })
                             )
        '''
        package test
            model test_model:
                string f(a: int, b: float) {
                    int i = 5
                    while i > 0:
                        b = b + mvk.g(c=5)
        '''
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.ExpressionStatement'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1.body'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Statement.name'): StringValue('e_s_1')})
                                           })
                             )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Assignment'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1.body.e_s_1'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Expression.name'): StringValue('a_e_1')})
                                           })
                             )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Assignment'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Expression.name'): StringValue('b'),
                                                                                    StringValue('Identifier.type'): FloatType()})
                                           })
                             )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Plus'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Expression.name'): StringValue('b_plus_g')})
                                           })
                             )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Navigation'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1.b_plus_g'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Expression.name'): StringValue('b'),
                                                                                    StringValue('Navigation.path'): LocationValue('b')})
                                           })
                             )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.FunctionCall'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1.b_plus_g'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Expression.name'): StringValue('g')})
                                           })
                             )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Navigation'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1.b_plus_g.g'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Expression.name'): StringValue('mvk'),
                                                                                    StringValue('Navigation.path'): LocationValue('mvk')})
                                           })
                             )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Argument'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1.b_plus_g.g'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Argument.name'): StringValue('c'),
                                                                                    StringValue('Argument.key'): LocationValue('c')})
                                           })
                             )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Constant'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1.b_plus_g.g.c'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Expression.name'): StringValue('five'),
                                                                                    StringValue('Constant.value'): IntegerValue(5)})
                                           })
                             )
        '''
        package test
            model test_model:
                string f(a: int, b: float) {
                    int i = 5
                    while i > 0:
                        b = b + mvk.g(c=5)
                        i = i - 1
                    if b > 100:
        '''
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.IfStatement'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Statement.name'): StringValue('ifstmt_1')})
                                           })
                             )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.GreaterThan'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.ifstmt_1'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Expression.name'): StringValue('ifstmt_1_expr')})
                                           })
                             )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Navigation'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.ifstmt_1.ifstmt_1_expr'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Expression.name'): StringValue('b'),
                                                                                    StringValue('Navigation.path'): LocationValue('b')})
                                           })
                             )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Constant'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.ifstmt_1.ifstmt_1_expr'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Expression.name'): StringValue('onehundred'),
                                                                                    StringValue('Navigation.value'): IntegerValue(100)})
                                           })
                             )
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
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.ReturnStatement'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.ifstmt_1.ifbody'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Statement.name'): StringValue('r_s_1')})
                                           })
                             )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Navigation'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.ifstmt_1.ifbody.r_s_1'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Expression.name'): StringValue('b'),
                                                                                    StringValue('Navigation.path'): LocationValue('b')})
                                           })
                             )
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
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.ReturnStatement'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.ifstmt_1.elsebody'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Statement.name'): StringValue('r_s_2')})
                                           })
                             )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Minus'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.ifstmt_1.elsebody.r_s_2'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Expression.name'): StringValue('zero_minus_b')})
                                           })
                             )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Constant'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.ifstmt_1.elsebody.r_s_2.zero_minus_b'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Expression.name'): StringValue('zero'),
                                                                                    StringValue('Constant.value'): IntegerValue(0)})
                                           })
                             )
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Navigation'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.ifstmt_1.elsebody.r_s_2.zero_minus_b'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Expression.name'): StringValue('b'),
                                                                                    StringValue('Navigation.path'): LocationValue('b')})
                                           })
                             )

    def test_interface_methods(self):
        self.create_petrinets()
        loc = LocationValue('formalisms.Petrinets.Place')
        p = self.mvk.read(loc).get_item()
        for m in ['get_name',
                  'get_parent',
                  'get_short_location',
                  'typed_by',
                  'get_potency',
                  'get_attributes',
                  'get_functions',
                  'get_out_associations',
                  'get_all_out_associations',
                  'get_in_associations',
                  'get_all_in_associations',
                  'get_all_associations',
                  'get_outgoing_elements',
                  'get_incoming_elements',
                  'get_neighbors',
                  'get_lower',
                  'get_upper',
                  'is_ordered',
                  'is_abstract',
                  'get_specialise_classes',
                  'get_super_classes',
                  'get_all_specialise_classes',
                  'get_all_super_classes',
                  'get_all_attributes']:
            l = self.mvk.evaluate(StringValue(m), loc)
        self.mvk.evaluate(StringValue('get_node'), loc)
        self.mvk.evaluate(StringValue('get_attribute'), loc, attr_loc=StringValue('tokens'))
        self.mvk.evaluate(StringValue('__eq__'), loc, loc)
        self.mvk.evaluate(StringValue('__ne__'), loc, LocationValue('formalisms.Petrinets.Transition'))
        self.mvk.evaluate(StringValue('get_element'), LocationValue('formalisms.Petrinets'), name=StringValue('Place'))

mvktest = MvKTest()
mvktest.clear()
mvktest.test_create()
mvktest.clear()
mvktest.test_instantiation()
mvktest.clear()
mvktest.test_errors()
mvktest.clear()
mvktest.test_inheritance()
mvktest.clear()
mvktest.test_composition()
mvktest.clear()
mvktest.test_delete()
mvktest.clear()
mvktest.test_update()
mvktest.clear()
mvktest.test_action_language()
mvktest.clear()
mvktest.test_interface_methods()
