import unittest
from mvk.impl.python.constants import CreateConstants, UpdateConstants
from mvk.impl.python.datatype import IntegerType, StringType, TypeFactory, BooleanType, FloatType, TypeType, AnyType, InfiniteType
from mvk.impl.python.datavalue import MappingValue, LocationValue, StringValue, IntegerValue, SequenceValue, BooleanValue, InfiniteValue, DataValueFactory, FloatValue, AnyValue, TupleValue
from mvk.impl.python.object import Model, ModelReference, Clabject, ClabjectReference, Attribute, Association, AssociationEnd, AssociationReference, Inherits, Composition
from mvk.mvk import MvK
from mvk.impl.formalisms.StoreMapper import StoreMapper
from mvk.impl.python.util.jsonserializer import MvKEncoder

class MvKWrapper(object):
    def __init__(self):
        self.mvk = MvK()
        self.encoder = MvKEncoder(deep=True)

    def conforms_to(self, *params, **params2):
        print("[\"conforms_to\", '[" + self.encoder.encode(params) + ", " + self.encoder.encode(params2) + "]'],")
        return self.mvk.conforms_to(*params, **params2)

    def evaluate(self, *params, **params2):
        print("[\"evaluate\", '[" + self.encoder.encode(params) + ", " + self.encoder.encode(params2) + "]'],")
        return self.mvk.evaluate(*params, **params2)

    def clear(self):
        print("[\"clear\", \"\"],")
        self.mvk.clear()

    def read(self, params):
        print("[\"read\", '" + self.encoder.encode(params) + "'],")
        return self.mvk.read(params)

    def create(self, params):
        print("[\"create\", '" + self.encoder.encode(params) + "'],")
        return self.mvk.create(params)

    def update(self, params):
        print("[\"update\", '" + self.encoder.encode(params) + "'],")
        return self.mvk.update(params)

    def delete(self, params):
        print("[\"delete\", '" + self.encoder.encode(params) + "'],")
        return self.mvk.delete(params)

class MvKTest():
    def noop(self, *args, **kwargs):
        pass

    def clear(self):
        self.mvk.clear()

    def __getattr__(self, name):
        return self.noop

    def __init__(self):
        self.mvk = MvKWrapper()
        self.mvk.clear()

    def create_petrinets(self):
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('Petrinets')})
                                      })
                        )
        self.assertTrue(self.mvk.read(LocationValue('formalisms.Petrinets')).is_success())
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        self.assertTrue(self.mvk.read(LocationValue('formalisms.Petrinets.name')).is_success())
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Place'),
                                                                               StringValue('Class.is_abstract'): BooleanValue(False),
                                                                               StringValue('Class.id_field'): StringValue('Place.name')})
                                      })
                        )
        self.assertTrue(self.mvk.read(LocationValue('formalisms.Petrinets.Place')).is_success())
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets.Place'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('tokens'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('IntegerType'),
                                                                               StringValue('Attribute.default'): IntegerValue(0)})
                                      })
                        )
        self.assertTrue(self.mvk.read(LocationValue('formalisms.Petrinets.Place.tokens')).is_success())
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets.Place'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        self.assertTrue(self.mvk.read(LocationValue('formalisms.Petrinets.Place.name')).is_success())
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Transition'),
                                                                               StringValue('Class.is_abstract'): BooleanValue(False),
                                                                               StringValue('Class.id_field'): StringValue('Transition.name')})
                                      })
                        )
        self.assertTrue(self.mvk.read(LocationValue('formalisms.Petrinets.Transition')).is_success())
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets.Transition'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        self.assertTrue(self.mvk.read(LocationValue('formalisms.Petrinets.Transition.name')).is_success())
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
        self.assertTrue(self.mvk.read(LocationValue('formalisms.Petrinets.P2T')).is_success())
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets.P2T'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        self.assertTrue(self.mvk.read(LocationValue('formalisms.Petrinets.P2T.name')).is_success())
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
        self.assertTrue(self.mvk.read(LocationValue('formalisms.Petrinets.T2P')).is_success())
        self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets.T2P'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        self.assertTrue(self.mvk.read(LocationValue('formalisms.Petrinets.T2P.name')).is_success())
        self.assertTrue(self.mvk.conforms_to(LocationValue('formalisms.Petrinets'), LocationValue('protected.formalisms.SimpleClassDiagrams')).get_result())

    def test_create(self):
        ''' Let's create the most used example ever... A Petrinets formalism! '''
        ''' First, the Petrinets type model, which should conform to SCD. '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('Petrinets')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        read_log_petrinets = self.mvk.read(LocationValue('formalisms.Petrinets'))
        self.assertTrue(read_log_petrinets.is_success())
        self.assertTrue(self.mvk.read(LocationValue('formalisms.Petrinets.name')).is_success())
        ref_model = Model(l_type=ModelReference(path=LocationValue('protected.formalisms.SimpleClassDiagrams')),
                          potency=IntegerValue(1),
                          name=StringValue('Petrinets'))
        ref_model.add_attribute(Attribute(name=StringValue("SimpleClassDiagrams.name"),
                                          the_type=StringType(),
                                          l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.name")).get_item(),
                                          potency=IntegerValue(0),
                                          value=StringValue('Petrinets')))
        name_attr = Attribute(name=StringValue("name"),
                              the_type=StringType(),
                              l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Attribute")).get_item(),
                              potency=IntegerValue(1),
                              default=StringValue(''))
        ref_model.add_attribute(name_attr)
        ref_model_to_name = Composition(name=StringValue("Petrinets_a_name"),
                                        l_type=AssociationReference(path=LocationValue("protected.formalisms.SimpleClassDiagrams.attributes")),
                                        potency=IntegerValue(0),
                                        from_multiplicity=AssociationEnd(port_name=StringValue('from_class'),
                                                                         node=ref_model),
                                        to_multiplicity=AssociationEnd(port_name=StringValue('to_attr'),
                                                                       node=name_attr))
        ref_model_to_name.add_attribute(Attribute(name=StringValue("attributes.name"),
                                                  the_type=StringType(),
                                                  l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.attributes.name")).get_item(),
                                                  value=StringValue('Petrinets_a_name'),
                                                  potency=IntegerValue(0)))
        ref_model.add_element(ref_model_to_name)
        self.assertEquals(read_log_petrinets.get_item(),
                          ref_model)

        ''' Then, some classes... '''
        """ PLACE """
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Place'),
                                                                                    StringValue('Class.is_abstract'): BooleanValue(False),
                                                                                    StringValue('Class.id_field'): StringValue('Place.name')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets.Place'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('tokens'),
                                                                                    StringValue('Attribute.type'): TypeFactory.get_type('IntegerType'),
                                                                                    StringValue('Attribute.default'): IntegerValue(0)})
                                           })
                        )
        self.assertTrue(cl.is_success())
        place = Clabject(name=StringValue("Place"),
                         l_type=ClabjectReference(path=LocationValue("protected.formalisms.SimpleClassDiagrams.Class")),
                         abstract=BooleanValue(False),
                         potency=IntegerValue(1))
        tokens_attr = Attribute(name=StringValue("tokens"),
                                the_type=IntegerType(),
                                l_type=ClabjectReference(path=LocationValue("protected.formalisms.SimpleClassDiagrams.Attribute")),
                                lower=IntegerValue(1),
                                upper=IntegerValue(1),
                                potency=IntegerValue(1),
                                default=IntegerValue(0))
        place.add_attribute(tokens_attr)
        place_to_ta = Composition(name=StringValue("Place_a_tokens"),
                                  l_type=AssociationReference(path=LocationValue("protected.formalisms.SimpleClassDiagrams.attributes")),
                                  potency=IntegerValue(0),
                                  from_multiplicity=AssociationEnd(port_name=StringValue('from_class'),
                                                                   node=place),
                                  to_multiplicity=AssociationEnd(port_name=StringValue('to_attr'),
                                                                 node=tokens_attr))
        ref_model.add_element(place_to_ta)
        place_to_ta.add_attribute(Attribute(name=StringValue("attributes.name"),
                                  the_type=StringType(),
                                  l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.attributes.name")).get_item(),
                                  value=StringValue('Place_a_tokens'),
                                  potency=IntegerValue(0)))
        read_log_tokens = self.mvk.read(LocationValue('formalisms.Petrinets.Place.tokens'))
        self.assertTrue(read_log_tokens.is_success())
        self.assertEquals(read_log_tokens.get_item(),
                          tokens_attr)
        name_attr = Attribute(name=StringValue("Class.name"),
                              the_type=StringType(),
                              l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Class.name")).get_item(),
                              value=StringValue('Place'),
                              potency=IntegerValue(0))
        place.add_attribute(name_attr)
        read_log_name = self.mvk.read(LocationValue('formalisms.Petrinets.Place.Class.name'))
        self.assertTrue(read_log_name.is_success(), read_log_name)
        self.assertEquals(read_log_name.get_item(),
                          name_attr)
        is_abstract_attr = Attribute(name=StringValue("Class.is_abstract"),
                                     the_type=IntegerType(),
                                     l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Class.is_abstract")).get_item(),
                                     value=BooleanValue(False),
                                     potency=IntegerValue(0))
        place.add_attribute(is_abstract_attr)
        read_log_is_abstract = self.mvk.read(LocationValue('formalisms.Petrinets.Place.Class.is_abstract'))
        self.assertTrue(read_log_is_abstract.is_success())
        self.assertEquals(read_log_is_abstract.get_item(),
                          is_abstract_attr)
        id_field_attr = Attribute(name=StringValue("Class.id_field"),
                                  the_type=StringType(),
                                  l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Class.id_field")).get_item(),
                                  value=StringValue('Place.name'),
                                  potency=IntegerValue(0))
        place.add_attribute(id_field_attr)
        read_log_id_field = self.mvk.read(LocationValue('formalisms.Petrinets.Place.Class.id_field'))
        self.assertTrue(read_log_id_field.is_success())
        self.assertEquals(read_log_id_field.get_item(),
                          id_field_attr)
        read_log_place = self.mvk.read(LocationValue('formalisms.Petrinets.Place'))
        self.assertTrue(read_log_place.is_success())
        self.assertEquals(read_log_place.get_item(),
                          place)

        """ TRANSITION """
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Transition'),
                                                                                    StringValue('Class.is_abstract'): BooleanValue(False),
                                                                                    StringValue('Class.id_field'): StringValue('Transition.name')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        transition = Clabject(name=StringValue("Transition"),
                              l_type=ClabjectReference(path=LocationValue("protected.formalisms.SimpleClassDiagrams.Class")),
                              abstract=BooleanValue(False),
                              potency=IntegerValue(1))
        name_attr = Attribute(name=StringValue("Class.name"),
                              the_type=StringType(),
                              l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Class.name")).get_item(),
                              value=StringValue('Transition'),
                              potency=IntegerValue(0))
        transition.add_attribute(name_attr)
        read_log_name = self.mvk.read(LocationValue('formalisms.Petrinets.Transition.Class.name'))
        self.assertTrue(read_log_name.is_success(), read_log_name)
        self.assertEquals(read_log_name.get_item(),
                          name_attr)
        is_abstract_attr = Attribute(name=StringValue("Class.is_abstract"),
                                     the_type=IntegerType(),
                                     l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Class.is_abstract")).get_item(),
                                     value=BooleanValue(False),
                                     potency=IntegerValue(0))
        transition.add_attribute(is_abstract_attr)
        read_log_is_abstract = self.mvk.read(LocationValue('formalisms.Petrinets.Transition.Class.is_abstract'))
        self.assertTrue(read_log_is_abstract.is_success())
        self.assertEquals(read_log_is_abstract.get_item(),
                          is_abstract_attr)
        id_field_attr = Attribute(name=StringValue("Class.id_field"),
                                  the_type=StringType(),
                                  l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Class.id_field")).get_item(),
                                  value=StringValue('Transition.name'),
                                  potency=IntegerValue(0))
        transition.add_attribute(id_field_attr)
        read_log_id_field = self.mvk.read(LocationValue('formalisms.Petrinets.Transition.Class.id_field'))
        self.assertTrue(read_log_id_field.is_success())
        self.assertEquals(read_log_id_field.get_item(),
                          id_field_attr)
        read_log_transition = self.mvk.read(LocationValue('formalisms.Petrinets.Transition'))
        self.assertTrue(read_log_transition.is_success())
        self.assertEquals(read_log_transition.get_item(),
                          transition)

        """ P2T """
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.SimpleClassDiagrams.Association"),
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
        self.assertTrue(cl.is_success(), cl)
        read_log_p2t = self.mvk.read(LocationValue('formalisms.Petrinets.P2T'))
        self.assertTrue(read_log_p2t.is_success())
        p2t = Association(name=StringValue("P2T"),
                          l_type=AssociationReference(path=LocationValue("protected.formalisms.SimpleClassDiagrams.Association")),
                          abstract=BooleanValue(False),
                          potency=IntegerValue(1),
                          from_multiplicity=AssociationEnd(port_name=StringValue('from_place'),
                                                           node=read_log_place.get_item()),
                          to_multiplicity=AssociationEnd(port_name=StringValue('to_transition'),
                                                         node=read_log_transition.get_item()))
        p2t.add_attribute(Attribute(name=StringValue("Class.name"),
                          the_type=StringType(),
                          l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Class.name")).get_item(),
                          value=StringValue('P2T'),
                          potency=IntegerValue(0)))
        p2t.add_attribute(Attribute(name=StringValue("Class.is_abstract"),
                          the_type=BooleanType(),
                          l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Class.is_abstract")).get_item(),
                          value=BooleanValue(False),
                          potency=IntegerValue(0)))
        p2t.add_attribute(Attribute(name=StringValue("Class.id_field"),
                          the_type=BooleanType(),
                          l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Class.id_field")).get_item(),
                          value=StringValue('P2T.name'),
                          potency=IntegerValue(0)))
        p2t.add_attribute(Attribute(name=StringValue("Association.from_min"),
                          the_type=IntegerType(),
                          l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Association.from_min")).get_item(),
                          value=IntegerValue(0),
                          potency=IntegerValue(0)))
        p2t.add_attribute(Attribute(name=StringValue("Association.from_max"),
                          the_type=InfiniteType(),
                          l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Association.from_max")).get_item(),
                          value=InfiniteValue('+'),
                          potency=IntegerValue(0)))
        p2t.add_attribute(Attribute(name=StringValue("Association.from_port"),
                          the_type=StringType(),
                          l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Association.from_port")).get_item(),
                          value=StringValue('from_place'),
                          potency=IntegerValue(0)))
        p2t.add_attribute(Attribute(name=StringValue("Association.to_min"),
                          the_type=IntegerType(),
                          l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Association.to_min")).get_item(),
                          value=IntegerValue(0),
                          potency=IntegerValue(0)))
        p2t.add_attribute(Attribute(name=StringValue("Association.to_max"),
                          the_type=InfiniteType(),
                          l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Association.to_max")).get_item(),
                          value=InfiniteValue('+'),
                          potency=IntegerValue(0)))
        p2t.add_attribute(Attribute(name=StringValue("Association.to_port"),
                          the_type=StringType(),
                          l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Association.to_port")).get_item(),
                          value=StringValue('to_transition'),
                          potency=IntegerValue(0)))
        self.assertEquals(read_log_p2t.get_item(),
                          p2t)

        """ T2P """
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.SimpleClassDiagrams.Association"),
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
        self.assertTrue(cl.is_success())
        read_log_t2p = self.mvk.read(LocationValue('formalisms.Petrinets.T2P'))
        self.assertTrue(read_log_t2p.is_success())
        t2p = Association(name=StringValue("T2P"),
                          l_type=AssociationReference(path=LocationValue("protected.formalisms.SimpleClassDiagrams.Association")),
                          abstract=BooleanValue(False),
                          potency=IntegerValue(1),
                          from_multiplicity=AssociationEnd(port_name=StringValue('from_transition'),
                                                           node=read_log_transition.get_item()),
                          to_multiplicity=AssociationEnd(port_name=StringValue('to_place'),
                                                         node=read_log_place.get_item()))
        t2p.add_attribute(Attribute(name=StringValue("Class.name"),
                          the_type=StringType(),
                          l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Class.name")).get_item(),
                          value=StringValue('T2P'),
                          potency=IntegerValue(0)))
        t2p.add_attribute(Attribute(name=StringValue("Class.is_abstract"),
                          the_type=BooleanType(),
                          l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Class.is_abstract")).get_item(),
                          value=BooleanValue(False),
                          potency=IntegerValue(0)))
        t2p.add_attribute(Attribute(name=StringValue("Class.id_field"),
                          the_type=BooleanType(),
                          l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Class.id_field")).get_item(),
                          value=StringValue('T2P.name'),
                          potency=IntegerValue(0)))
        t2p.add_attribute(Attribute(name=StringValue("Association.from_min"),
                          the_type=IntegerType(),
                          l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Association.from_min")).get_item(),
                          value=IntegerValue(0),
                          potency=IntegerValue(0)))
        t2p.add_attribute(Attribute(name=StringValue("Association.from_max"),
                          the_type=InfiniteType(),
                          l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Association.from_max")).get_item(),
                          value=InfiniteValue('+'),
                          potency=IntegerValue(0)))
        t2p.add_attribute(Attribute(name=StringValue("Association.from_port"),
                          the_type=StringType(),
                          l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Association.from_port")).get_item(),
                          value=StringValue('from_transition'),
                          potency=IntegerValue(0)))
        t2p.add_attribute(Attribute(name=StringValue("Association.to_min"),
                          the_type=IntegerType(),
                          l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Association.to_min")).get_item(),
                          value=IntegerValue(0),
                          potency=IntegerValue(0)))
        t2p.add_attribute(Attribute(name=StringValue("Association.to_max"),
                          the_type=InfiniteType(),
                          l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Association.to_max")).get_item(),
                          value=InfiniteValue('+'),
                          potency=IntegerValue(0)))
        t2p.add_attribute(Attribute(name=StringValue("Association.to_port"),
                          the_type=StringType(),
                          l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Association.to_port")).get_item(),
                          value=StringValue('to_place'),
                          potency=IntegerValue(0)))
        self.assertEquals(read_log_t2p.get_item(),
                          t2p)

    def test_instantiation(self):
        self.create_petrinets()
        ''' Let's create an instance of a Petrinet... '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.Petrinets'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Petrinets.name'): StringValue('myPetrinet')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        read_log_mypetrinet = self.mvk.read(LocationValue('models.myPetrinet'))
        self.assertTrue(read_log_mypetrinet.is_success())
        ref_model = Model(l_type=ModelReference(path=LocationValue('formalisms.Petrinets')),
                          potency=IntegerValue(0),
                          name=StringValue('myPetrinet'))
        ref_model.add_attribute(Attribute(name=StringValue("Petrinets.name"),
                                          the_type=StringType(),
                                          l_type=self.mvk.read(LocationValue("formalisms.Petrinets.name")).get_item(),
                                          potency=IntegerValue(0),
                                          value=StringValue('myPetrinet')))
        self.assertEquals(read_log_mypetrinet.get_item(),
                          ref_model)

        ''' p1 should get the default value for the attribute 'tokens' '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.Petrinets.Place'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.myPetrinet'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Place.name'): StringValue('p1')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        read_log_p1 = self.mvk.read(LocationValue('models.myPetrinet.p1'))
        self.assertTrue(read_log_p1.is_success())
        p1 = Clabject(name=StringValue("p1"),
                      l_type=ClabjectReference(path=LocationValue("formalisms.Petrinets.Place")),
                      potency=IntegerValue(0))
        p1.add_attribute(Attribute(name=StringValue("Place.tokens"),
                                   the_type=IntegerType(),
                                   l_type=self.mvk.read(LocationValue("formalisms.Petrinets.Place.tokens")).get_item(),
                                   potency=IntegerValue(0),
                                   value=IntegerValue(0)))
        p1.add_attribute(Attribute(name=StringValue("Place.name"),
                                   the_type=StringType(),
                                   l_type=self.mvk.read(LocationValue("formalisms.Petrinets.Place.name")).get_item(),
                                   potency=IntegerValue(0),
                                   value=StringValue('p1')))
        self.assertEquals(read_log_p1.get_item(), p1)

        ''' p2 gets a value for 'tokens' '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.Petrinets.Place'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.myPetrinet'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Place.name'): StringValue('p2'),
                                                                                    StringValue('Place.tokens'): IntegerValue(10)})
                                           })
                             )
        self.assertTrue(cl.is_success())
        read_log_p2 = self.mvk.read(LocationValue('models.myPetrinet.p2'))
        self.assertTrue(read_log_p1.is_success())
        p2 = Clabject(name=StringValue("p2"),
                      l_type=ClabjectReference(path=LocationValue("formalisms.Petrinets.Place")),
                      potency=IntegerValue(0))
        p2.add_attribute(Attribute(name=StringValue("Place.tokens"),
                                   the_type=IntegerType(),
                                   l_type=self.mvk.read(LocationValue("formalisms.Petrinets.Place.tokens")).get_item(),
                                   potency=IntegerValue(0),
                                   value=IntegerValue(10)))
        p2.add_attribute(Attribute(name=StringValue("Place.name"),
                                   the_type=StringType(),
                                   l_type=self.mvk.read(LocationValue("formalisms.Petrinets.Place.name")).get_item(),
                                   potency=IntegerValue(0),
                                   value=StringValue('p2')))
        self.assertEquals(read_log_p2.get_item(), p2)

        ''' instantiating transition '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.Petrinets.Transition'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.myPetrinet'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Transition.name'): StringValue('t1')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        read_log_t1 = self.mvk.read(LocationValue('models.myPetrinet.t1'))
        self.assertTrue(read_log_t1.is_success())
        t1 = Clabject(name=StringValue("t1"),
                      l_type=ClabjectReference(path=LocationValue("formalisms.Petrinets.Transition")),
                      potency=IntegerValue(0))
        t1.add_attribute(Attribute(name=StringValue("Transition.name"),
                                   the_type=IntegerType(),
                                   l_type=self.mvk.read(LocationValue("formalisms.Petrinets.Transition.name")).get_item(),
                                   potency=IntegerValue(0),
                                   value=StringValue('t1')))
        self.assertEquals(read_log_t1.get_item(), t1)

        ''' instantiating P2T '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.Petrinets.P2T'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.myPetrinet'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('P2T.name'): StringValue('p2_to_t1'),
                                                                                    StringValue('from_place'): LocationValue('models.myPetrinet.p2'),
                                                                                    StringValue('to_transition'): LocationValue('models.myPetrinet.t1')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        read_log_p2_to_t1 = self.mvk.read(LocationValue('models.myPetrinet.p2_to_t1'))
        self.assertTrue(read_log_p2_to_t1.is_success())
        p2_to_t1 = Association(name=StringValue("p2_to_t1"),
                               l_type=AssociationReference(path=LocationValue("formalisms.Petrinets.P2T")),
                               potency=IntegerValue(0),
                               from_multiplicity=AssociationEnd(node=read_log_p2.get_item(),
                                                                port_name=StringValue('from_place')),
                               to_multiplicity=AssociationEnd(node=read_log_t1.get_item(),
                                                                port_name=StringValue('to_transition')))
        p2_to_t1.add_attribute(Attribute(name=StringValue("P2T.name"),
                                         the_type=IntegerType(),
                                         l_type=self.mvk.read(LocationValue("formalisms.Petrinets.P2T.name")).get_item(),
                                         potency=IntegerValue(0),
                                         value=StringValue('p2_to_t1')))
        self.assertEquals(read_log_p2_to_t1.get_item(), p2_to_t1)

        ''' instantiating T2P '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.Petrinets.T2P'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.myPetrinet'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('T2P.name'): StringValue('t1_to_p1'),
                                                                                    StringValue('from_transition'): LocationValue('models.myPetrinet.t1'),
                                                                                    StringValue('to_place'): LocationValue('models.myPetrinet.p1')})
                                           })
                             )
        self.assertTrue(cl.is_success())
        read_log_t1_to_p1 = self.mvk.read(LocationValue('models.myPetrinet.t1_to_p1'))
        self.assertTrue(read_log_t1_to_p1.is_success())
        t1_to_p1 = Association(name=StringValue("t1_to_p1"),
                               l_type=AssociationReference(path=LocationValue("formalisms.Petrinets.T2P")),
                               potency=IntegerValue(0),
                               from_multiplicity=AssociationEnd(node=read_log_t1.get_item(),
                                                                port_name=StringValue('from_transition')),
                               to_multiplicity=AssociationEnd(node=read_log_p1.get_item(),
                                                              port_name=StringValue('to_place')))
        t1_to_p1.add_attribute(Attribute(name=StringValue("T2P.name"),
                                         the_type=IntegerType(),
                                         l_type=self.mvk.read(LocationValue("formalisms.Petrinets.T2P.name")).get_item(),
                                         potency=IntegerValue(0),
                                         value=StringValue('t1_to_p1')))
        self.assertEquals(read_log_t1_to_p1.get_item(), t1_to_p1)

        ''' conformance check '''
        c_log = self.mvk.conforms_to(LocationValue('models.myPetrinet'), LocationValue('formalisms.Petrinets'))
        self.assertTrue(c_log.is_success())
        self.assertTrue(c_log.get_result(), c_log.get_status_message())

    def test_errors(self):
        self.create_petrinets()
        ''' Let's try to break some stuff... '''

        ''' Create an already existing Model '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('Petrinets')})
                                           })
                             )
        self.assertFalse(cl.is_success())

        ''' Create an already existing Clabject '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Place'),
                                                                                    StringValue('Class.is_abstract'): BooleanValue(True),
                                                                                    StringValue('Class.id_field'): StringValue('Place.name')})
                                           })
                             )
        self.assertFalse(cl.is_success())
        self.assertEqual(self.mvk.read(LocationValue('formalisms.Petrinets.Place')).get_item().is_abstract(), BooleanValue(False))

        ''' Create an already existing Association '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Association'),
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
        self.assertFalse(cl.is_success())
        self.assertEqual(self.mvk.read(LocationValue('formalisms.Petrinets.P2T')).get_item().is_abstract(), BooleanValue(False))

        ''' Create an already existing Attribute '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets.Place'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('tokens'),
                                                                                    StringValue('Attribute.type'): TypeFactory.get_type('IntegerType'),
                                                                                    StringValue('Attribute.default'): IntegerValue(-1)})
                                           })
                             )
        self.assertFalse(cl.is_success())
        self.assertEqual(self.mvk.read(LocationValue('formalisms.Petrinets.Place.tokens')).get_item().get_default(), IntegerValue(0))

        ''' Create an element in an invalid location. '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.CBD'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Block'),
                                                                                    StringValue('Class.is_abstract'): BooleanValue(True),
                                                                                    StringValue('Class.id_field'): StringValue('Place.name')})
                                           })
                             )
        self.assertFalse(cl.is_success())

        ''' Read from invalid locations. '''
        rl = self.mvk.read(LocationValue('formalisms..'))
        self.assertFalse(rl.is_success())
        rl = self.mvk.read(LocationValue('formalisms.'))
        self.assertFalse(rl.is_success())

        ''' Try to create a model in a package which does not yet exist.
        However, the package is named the same as a clabject in the parent
        package.'''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                           CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets.Place'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('TestModel')})
                                           })
                             )
        self.assertFalse(cl.is_success())
        self.assertFalse(self.mvk.read(LocationValue('formalisms.Petrinets.Place.TestClabject')).is_success())

    def test_inheritance(self):
        tm = Model(name=StringValue("TestSubTyping"),
                   l_type=ModelReference(path=LocationValue('protected.formalisms.SimpleClassDiagrams')),
                   potency=IntegerValue(1))
        tm.add_attribute(Attribute(name=StringValue("SimpleClassDiagrams.name"),
                                   the_type=StringType(),
                                   l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.name")).get_item(),
                                   potency=IntegerValue(0),
                                   value=StringValue('TestSubTyping')))
        name_attr = Attribute(name=StringValue("name"),
                              the_type=StringType(),
                              l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Attribute")).get_item(),
                              potency=IntegerValue(1),
                              default=StringValue(''))
        tm.add_attribute(name_attr)
        tm_to_name = Composition(name=StringValue("TestSubTyping_a_name"),
                                 l_type=AssociationReference(path=LocationValue("protected.formalisms.SimpleClassDiagrams.attributes")),
                                 potency=IntegerValue(0),
                                 from_multiplicity=AssociationEnd(port_name=StringValue('from_class'),
                                                                  node=tm),
                                 to_multiplicity=AssociationEnd(port_name=StringValue('to_attr'),
                                                                node=name_attr))
        tm_to_name.add_attribute(Attribute(name=StringValue("attributes.name"),
                                           the_type=StringType(),
                                           l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.attributes.name")).get_item(),
                                           value=StringValue('TestSubTyping_a_name'),
                                           potency=IntegerValue(0)))
        tm.add_element(tm_to_name)
        el = Clabject(name=StringValue("Element"),
                      l_type=ClabjectReference(path=LocationValue('protected.formalisms.SimpleClassDiagrams.Class')),
                      potency=IntegerValue(1),
                      abstract=BooleanValue(True))
        el.add_attribute(Attribute(name=StringValue("Class.name"),
                                   the_type=StringType(),
                                   l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Class.name")).get_item(),
                                   value=StringValue('Element'),
                                   potency=IntegerValue(0))
                         )
        el.add_attribute(Attribute(name=StringValue("Class.is_abstract"),
                                   the_type=BooleanType(),
                                   l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Class.is_abstract")).get_item(),
                                   value=BooleanValue(True),
                                   potency=IntegerValue(0))
                         )
        tm.add_element(el)
        self.assertEqual(el.get_parent(), tm)
        self.assertEqual(tm.get_element(StringValue("Element")), el)
        int_attr = Attribute(name=StringValue("an_int"),
                             l_type=ClabjectReference(path=LocationValue("protected.formalisms.SimpleClassDiagrams.Attribute")),
                             potency=IntegerValue(1),
                             the_type=IntegerType(),
                             default=IntegerValue(0))
        el.add_attribute(int_attr)
        el_to_int_a = Composition(name=StringValue("Element_a_an_int"),
                                  l_type=AssociationReference(path=LocationValue("protected.formalisms.SimpleClassDiagrams.attributes")),
                                  potency=IntegerValue(0),
                                  from_multiplicity=AssociationEnd(port_name=StringValue('from_class'),
                                                                   node=el),
                                  to_multiplicity=AssociationEnd(port_name=StringValue('to_attr'),
                                                                 node=int_attr))
        tm.add_element(el_to_int_a)
        el_to_int_a.add_attribute(Attribute(name=StringValue("attributes.name"),
                                  the_type=StringType(),
                                  l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.attributes.name")).get_item(),
                                  value=StringValue('Element_a_an_int'),
                                  potency=IntegerValue(0)))
        str_attr = Attribute(name=StringValue("a_str"),
                             l_type=ClabjectReference(path=LocationValue("protected.formalisms.SimpleClassDiagrams.Attribute")),
                             potency=IntegerValue(1),
                             the_type=StringType(),
                             default=StringValue('test'))
        el.add_attribute(str_attr)
        el_to_str_a = Composition(name=StringValue("Element_a_a_str"),
                                  l_type=AssociationReference(path=LocationValue("protected.formalisms.SimpleClassDiagrams.attributes")),
                                  potency=IntegerValue(0),
                                  from_multiplicity=AssociationEnd(port_name=StringValue('from_class'),
                                                                   node=el),
                                  to_multiplicity=AssociationEnd(port_name=StringValue('to_attr'),
                                                                 node=str_attr))
        tm.add_element(el_to_str_a)
        el_to_str_a.add_attribute(Attribute(name=StringValue("attributes.name"),
                                  the_type=StringType(),
                                  l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.attributes.name")).get_item(),
                                  value=StringValue('Element_a_a_str'),
                                  potency=IntegerValue(0)))
        location_el = Clabject(name=StringValue("LocationElement"),
                               l_type=ClabjectReference(path=LocationValue("protected.formalisms.SimpleClassDiagrams.Class")),
                               potency=IntegerValue(1),
                               abstract=BooleanValue(True))
        location_el.add_attribute(Attribute(name=StringValue("Class.name"),
                                            the_type=StringType(),
                                            l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Class.name")).get_item(),
                                            value=StringValue('LocationElement'),
                                            potency=IntegerValue(0))
                                  )
        location_el.add_attribute(Attribute(name=StringValue("Class.is_abstract"),
                                            the_type=BooleanType(),
                                            l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Class.is_abstract")).get_item(),
                                            value=BooleanValue(True),
                                            potency=IntegerValue(0))
                                  )
        tm.add_element(location_el)
        le_i_el = Inherits(name=StringValue("le_i_el"),
                           l_type=AssociationReference(path=LocationValue("protected.formalisms.SimpleClassDiagrams.Inheritance")),
                           potency=IntegerValue(0),
                           from_multiplicity=AssociationEnd(node=location_el,
                                                            port_name=StringValue('from_class')),
                           to_multiplicity=AssociationEnd(node=el,
                                                          port_name=StringValue('to_class')))
        le_i_el.add_attribute(Attribute(name=StringValue("Inheritance.name"),
                                        the_type=StringType(),
                                        l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Inheritance.name")).get_item(),
                                        value=StringValue('le_i_el'),
                                        potency=IntegerValue(0))
                              )
        tm.add_element(le_i_el)
        location_el.add_super_class(el)
        loc_attr = Attribute(name=StringValue("location"),
                             l_type=ClabjectReference(path=LocationValue("protected.formalisms.SimpleClassDiagrams.Attribute")),
                             potency=IntegerValue(1),
                             the_type=TypeFactory.get_type("TupleType(IntegerType, IntegerType)"),
                             default=DataValueFactory.create_instance((0, 0)))
        location_el.add_attribute(loc_attr)
        loc_el_to_l = Composition(name=StringValue("LocationElement_a_location"),
                                  l_type=AssociationReference(path=LocationValue("protected.formalisms.SimpleClassDiagrams.attributes")),
                                  potency=IntegerValue(0),
                                  from_multiplicity=AssociationEnd(port_name=StringValue('from_class'),
                                                                   node=location_el),
                                  to_multiplicity=AssociationEnd(port_name=StringValue('to_attr'),
                                                                 node=loc_attr))
        tm.add_element(loc_el_to_l)
        loc_el_to_l.add_attribute(Attribute(name=StringValue("attributes.name"),
                                  the_type=StringType(),
                                  l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.attributes.name")).get_item(),
                                  value=StringValue('LocationElement_a_location'),
                                  potency=IntegerValue(0)))
        named_el = Clabject(name=StringValue("NamedElement"),
                            l_type=ClabjectReference(path=LocationValue("protected.formalisms.SimpleClassDiagrams.Class")),
                            potency=IntegerValue(1),
                            abstract=BooleanValue(True))
        named_el.add_attribute(Attribute(name=StringValue("Class.name"),
                                         the_type=StringType(),
                                         l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Class.name")).get_item(),
                                         value=StringValue('NamedElement'),
                                         potency=IntegerValue(0))
                               )
        named_el.add_attribute(Attribute(name=StringValue("Class.is_abstract"),
                                         the_type=BooleanType(),
                                         l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Class.is_abstract")).get_item(),
                                         value=BooleanValue(True),
                                         potency=IntegerValue(0))
                               )
        named_el.add_attribute(Attribute(name=StringValue("Class.id_field"),
                                         the_type=StringType(),
                                         l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Class.id_field")).get_item(),
                                         value=StringValue('NamedElement.name'),
                                         potency=IntegerValue(0))
                               )
        tm.add_element(named_el)
        ne_i_el = Inherits(name=StringValue("ne_i_el"),
                           l_type=AssociationReference(path=LocationValue("protected.formalisms.SimpleClassDiagrams.Inheritance")),
                           potency=IntegerValue(0),
                           from_multiplicity=AssociationEnd(node=named_el,
                                                            port_name=StringValue('from_class')),
                           to_multiplicity=AssociationEnd(node=el,
                                                          port_name=StringValue('to_class')))
        ne_i_el.add_attribute(Attribute(name=StringValue("Inheritance.name"),
                                        the_type=StringType(),
                                        l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Class.name")).get_item(),
                                        value=StringValue('ne_i_el'),
                                        potency=IntegerValue(0))
                              )
        tm.add_element(ne_i_el)
        named_el.add_super_class(el)
        name_attr = Attribute(name=StringValue("name"),
                              l_type=ClabjectReference(path=LocationValue("protected.formalisms.SimpleClassDiagrams.Attribute")),
                              potency=IntegerValue(1),
                              the_type=StringType(),
                              default=StringValue(''))
        named_el.add_attribute(name_attr)
        nam_el_to_n = Composition(name=StringValue("NamedElement_a_name"),
                                  l_type=AssociationReference(path=LocationValue("protected.formalisms.SimpleClassDiagrams.attributes")),
                                  potency=IntegerValue(0),
                                  from_multiplicity=AssociationEnd(port_name=StringValue('from_class'),
                                                                   node=named_el),
                                  to_multiplicity=AssociationEnd(port_name=StringValue('to_attr'),
                                                                 node=name_attr))
        tm.add_element(nam_el_to_n)
        nam_el_to_n.add_attribute(Attribute(name=StringValue("attributes.name"),
                                  the_type=StringType(),
                                  l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.attributes.name")).get_item(),
                                  value=StringValue('NamedElement_a_name'),
                                  potency=IntegerValue(0)))
        character = Clabject(name=StringValue("Character"),
                             l_type=ClabjectReference(path=LocationValue("protected.formalisms.SimpleClassDiagrams.Class")),
                             potency=IntegerValue(1),
                             abstract=BooleanValue(False))
        character.add_attribute(Attribute(name=StringValue("Class.name"),
                                          the_type=StringType(),
                                          l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Class.name")).get_item(),
                                          value=StringValue('Character'),
                                          potency=IntegerValue(0))
                                )
        character.add_attribute(Attribute(name=StringValue("Class.is_abstract"),
                                          the_type=BooleanType(),
                                          l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Class.is_abstract")).get_item(),
                                          value=BooleanValue(False),
                                          potency=IntegerValue(0))
                                )
        tm.add_element(character)
        c_i_le = Inherits(name=StringValue("c_i_le"),
                          l_type=AssociationReference(path=LocationValue("protected.formalisms.SimpleClassDiagrams.Inheritance")),
                          potency=IntegerValue(0),
                          from_multiplicity=AssociationEnd(node=character,
                                                           port_name=StringValue('from_class')),
                          to_multiplicity=AssociationEnd(node=location_el,
                                                         port_name=StringValue('to_class')))
        c_i_le.add_attribute(Attribute(name=StringValue("Inheritance.name"),
                                       the_type=StringType(),
                                       l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Class.name")).get_item(),
                                       value=StringValue('c_i_le'),
                                       potency=IntegerValue(0))
                             )
        tm.add_element(c_i_le)
        c_i_ne = Inherits(name=StringValue("c_i_ne"),
                          l_type=AssociationReference(path=LocationValue("protected.formalisms.SimpleClassDiagrams.Inheritance")),
                          potency=IntegerValue(0),
                          from_multiplicity=AssociationEnd(node=character,
                                                           port_name=StringValue('from_class')),
                          to_multiplicity=AssociationEnd(node=named_el,
                                                         port_name=StringValue('to_class')))
        c_i_ne.add_attribute(Attribute(name=StringValue("Inheritance.name"),
                                       the_type=StringType(),
                                       l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Class.name")).get_item(),
                                       value=StringValue('c_i_ne'),
                                       potency=IntegerValue(0))
                             )
        tm.add_element(c_i_ne)
        character.add_super_class(location_el)
        character.add_super_class(named_el)
        fs_attr = Attribute(name=StringValue("fighting_strength"),
                            l_type=ClabjectReference(path=LocationValue("protected.formalisms.SimpleClassDiagrams.Attribute")),
                            potency=IntegerValue(1),
                            default=IntegerValue(100),
                            the_type=IntegerType())
        character.add_attribute(fs_attr)
        char_to_fsa = Composition(name=StringValue("Character_a_fighting_strength"),
                                  l_type=AssociationReference(path=LocationValue("protected.formalisms.SimpleClassDiagrams.attributes")),
                                  potency=IntegerValue(0),
                                  from_multiplicity=AssociationEnd(port_name=StringValue('from_class'),
                                                                   node=character),
                                  to_multiplicity=AssociationEnd(port_name=StringValue('to_attr'),
                                                                 node=fs_attr))
        tm.add_element(char_to_fsa)
        char_to_fsa.add_attribute(Attribute(name=StringValue("attributes.name"),
                                  the_type=StringType(),
                                  l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.attributes.name")).get_item(),
                                  value=StringValue('Character_a_fighting_strength'),
                                  potency=IntegerValue(0)))
        hero = Clabject(name=StringValue("Hero"),
                        l_type=ClabjectReference(path=LocationValue("protected.formalisms.SimpleClassDiagrams.Class")),
                        potency=IntegerValue(1),
                        abstract=BooleanValue(False))
        hero.add_attribute(Attribute(name=StringValue("Class.name"),
                                     the_type=StringType(),
                                     l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Class.name")).get_item(),
                                     value=StringValue('Hero'),
                                     potency=IntegerValue(0))
                           )
        hero.add_attribute(Attribute(name=StringValue("Class.is_abstract"),
                                     the_type=BooleanType(),
                                     l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Class.is_abstract")).get_item(),
                                     value=BooleanValue(False),
                                     potency=IntegerValue(0))
                           )
        tm.add_element(hero)
        h_i_c = Inherits(name=StringValue("h_i_c"),
                         l_type=AssociationReference(path=LocationValue("protected.formalisms.SimpleClassDiagrams.Inheritance")),
                         potency=IntegerValue(0),
                         from_multiplicity=AssociationEnd(node=hero,
                                                          port_name=StringValue('from_class')),
                         to_multiplicity=AssociationEnd(node=character,
                                                        port_name=StringValue('to_class')))
        h_i_c.add_attribute(Attribute(name=StringValue("Inheritance.name"),
                                      the_type=StringType(),
                                      l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Class.name")).get_item(),
                                      value=StringValue('h_i_c'),
                                      potency=IntegerValue(0))
                            )
        tm.add_element(h_i_c)
        hero.add_super_class(character)
        points_attr = Attribute(name=StringValue("points"),
                                l_type=ClabjectReference(path=LocationValue("protected.formalisms.SimpleClassDiagrams.Attribute")),
                                potency=IntegerValue(1),
                                default=IntegerValue(0),
                                the_type=IntegerType())
        hero.add_attribute(points_attr)
        hero_to_pts = Composition(name=StringValue("Hero_a_points"),
                                  l_type=AssociationReference(path=LocationValue("protected.formalisms.SimpleClassDiagrams.attributes")),
                                  potency=IntegerValue(0),
                                  from_multiplicity=AssociationEnd(port_name=StringValue('from_class'),
                                                                   node=hero),
                                  to_multiplicity=AssociationEnd(port_name=StringValue('to_attr'),
                                                                 node=points_attr))
        tm.add_element(hero_to_pts)
        hero_to_pts.add_attribute(Attribute(name=StringValue("attributes.name"),
                                  the_type=StringType(),
                                  l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.attributes.name")).get_item(),
                                  value=StringValue('Hero_a_points'),
                                  potency=IntegerValue(0)))
        door = Clabject(name=StringValue("Door"),
                        l_type=ClabjectReference(path=LocationValue("protected.formalisms.SimpleClassDiagrams.Class")),
                        potency=IntegerValue(1),
                        abstract=BooleanValue(False))
        door.add_attribute(Attribute(name=StringValue("Class.name"),
                                     the_type=StringType(),
                                     l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Class.name")).get_item(),
                                     value=StringValue('Door'),
                                     potency=IntegerValue(0))
                           )
        door.add_attribute(Attribute(name=StringValue("Class.is_abstract"),
                                     the_type=BooleanType(),
                                     l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Class.is_abstract")).get_item(),
                                     value=BooleanValue(False),
                                     potency=IntegerValue(0))
                           )
        tm.add_element(door)
        d_i_ne = Inherits(name=StringValue("d_i_ne"),
                          l_type=AssociationReference(path=LocationValue("protected.formalisms.SimpleClassDiagrams.Inheritance")),
                          potency=IntegerValue(0),
                          from_multiplicity=AssociationEnd(node=door,
                                                           port_name=StringValue('from_class')),
                          to_multiplicity=AssociationEnd(node=named_el,
                                                         port_name=StringValue('to_class')))
        d_i_ne.add_attribute(Attribute(name=StringValue("Inheritance.name"),
                                       the_type=StringType(),
                                       l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.Class.name")).get_item(),
                                       value=StringValue('d_i_ne'),
                                       potency=IntegerValue(0))
                             )
        tm.add_element(d_i_ne)
        door.add_super_class(named_el)
        is_locked_attr = Attribute(name=StringValue("is_locked"),
                                   l_type=ClabjectReference(path=LocationValue("protected.formalisms.SimpleClassDiagrams.Attribute")),
                                   potency=IntegerValue(1),
                                   default=BooleanValue(0),
                                   the_type=BooleanType())
        door.add_attribute(is_locked_attr)
        door_to_isl = Composition(name=StringValue("Door_a_is_locked"),
                                  l_type=AssociationReference(path=LocationValue("protected.formalisms.SimpleClassDiagrams.attributes")),
                                  potency=IntegerValue(0),
                                  from_multiplicity=AssociationEnd(port_name=StringValue('from_class'),
                                                                   node=door),
                                  to_multiplicity=AssociationEnd(port_name=StringValue('to_attr'),
                                                                 node=is_locked_attr))
        tm.add_element(door_to_isl)
        door_to_isl.add_attribute(Attribute(name=StringValue("attributes.name"),
                                  the_type=StringType(),
                                  l_type=self.mvk.read(LocationValue("protected.formalisms.SimpleClassDiagrams.attributes.name")).get_item(),
                                  value=StringValue('Door_a_is_locked'),
                                  potency=IntegerValue(0)))

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
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('le_i_el'),
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
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('ne_i_el'),
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
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('c_i_ne'),
                                                                                        StringValue('from_class'): LocationValue('formalisms.TestSubTyping.Character'),
                                                                                        StringValue('to_class'): LocationValue('formalisms.TestSubTyping.NamedElement')})
                                               })
                                 )
        self.assertTrue(sc_log.is_success())
        sc_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestSubTyping'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('c_i_le'),
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
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('h_i_c'),
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
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('d_i_ne'),
                                                                                        StringValue('from_class'): LocationValue('formalisms.TestSubTyping.Door'),
                                                                                        StringValue('to_class'): LocationValue('formalisms.TestSubTyping.NamedElement')})
                                               })
                                 )
        self.assertTrue(sc_log.is_success(), sc_log)

        self.assertEqual(self.mvk.read(LocationValue('formalisms.TestSubTyping.le_i_el')).get_item(), tm.get_element(StringValue('le_i_el')))
        self.assertEqual(self.mvk.read(LocationValue('formalisms.TestSubTyping.Element')).get_item(), el)
        self.assertEqual(self.mvk.read(LocationValue('formalisms.TestSubTyping.NamedElement')).get_item(), named_el)
        self.assertEqual(self.mvk.read(LocationValue('formalisms.TestSubTyping.LocationElement')).get_item(), location_el)
        self.assertEqual(self.mvk.read(LocationValue('formalisms.TestSubTyping.Character')).get_item(), character)
        self.assertEqual(self.mvk.read(LocationValue('formalisms.TestSubTyping.Hero')).get_item(), hero)
        self.assertEqual(self.mvk.read(LocationValue('formalisms.TestSubTyping.Door')).get_item(), door)

        ''' As the locations differ, it will check whether their contents
        are equal. '''
        self.assertEqual(self.mvk.read(LocationValue('formalisms.TestSubTyping')).get_item(), tm)

        created_testsubtyping_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.TestSubTyping'),
                                                                  CreateConstants.LOCATION_KEY: LocationValue('models'),
                                                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('TestSubTyping.name'): StringValue('testModel')})
                                                                  })
                                                    )
        self.assertTrue(created_testsubtyping_log.is_success(), created_testsubtyping_log)

        created_hero_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.TestSubTyping.Hero'),
                                                         CreateConstants.LOCATION_KEY: LocationValue('models.testModel'),
                                                         CreateConstants.ATTRS_KEY: MappingValue({StringValue('NamedElement.name'): StringValue('Simon')})
                                                         })
                                           )
        self.assertTrue(created_hero_log.is_success(), created_hero_log)
        created_hero_read_log = self.mvk.read(LocationValue('models.testModel.Simon'))
        self.assertTrue(created_hero_read_log.is_success())
        created_hero = created_hero_read_log.get_item()
        self.assertEqual(created_hero.get_attribute(StringValue('Element.an_int')).get_value(), IntegerValue(0))
        self.assertEqual(created_hero.get_attribute(StringValue('Element.a_str')).get_value(), StringValue('test'))
        self.assertEqual(created_hero.get_attribute(StringValue('LocationElement.location')).get_value(), TupleValue((IntegerValue(0), IntegerValue(0))))
        self.assertEqual(created_hero.get_attribute(StringValue('NamedElement.name')).get_value(), StringValue('Simon'))
        self.assertEqual(created_hero.get_attribute(StringValue('Character.fighting_strength')).get_value(), IntegerValue(100))
        self.assertEqual(created_hero.get_attribute(StringValue('Hero.points')).get_value(), IntegerValue(0))

    def test_composition(self):
        tm_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('mvk.object.Model'),
                                               CreateConstants.LOCATION_KEY: LocationValue('formalisms'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('TestComposition'),
                                                                                        StringValue('type_model'): LocationValue('mvk.object')})
                                               })
                                 )
        self.assertTrue(tm_log.is_success(), tm_log)
        car_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                                CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestComposition'),
                                                CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('Car'),
                                                                                         StringValue('abstract'): BooleanValue(False),
                                                                                         StringValue('class'): LocationValue('mvk.object.Clabject')})
                                                })
                                 )
        self.assertTrue(car_log.is_success(), car_log)
        wheel_log = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                                  CreateConstants.LOCATION_KEY: LocationValue('formalisms.TestComposition'),
                                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('Wheel'),
                                                                                           StringValue('abstract'): BooleanValue(False),
                                                                                           StringValue('class'): LocationValue('mvk.object.Clabject')})
                                                  })
                                    )
        self.assertTrue(wheel_log.is_success(), wheel_log)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue("mvk.object.Composition"),
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
        self.assertTrue(cl.is_success(), cl)

    def test_delete(self):
        self.create_petrinets()
        self.assertTrue(self.mvk.delete(LocationValue('formalisms.Petrinets.Place.tokens')).is_success())
        self.assertFalse(self.mvk.read(LocationValue('formalisms.Petrinets.Place.tokens')).is_success())
        self.assertTrue(self.mvk.delete(LocationValue('formalisms.Petrinets.Place')).is_success())
        self.assertFalse(self.mvk.read(LocationValue('formalisms.Petrinets.Place')).is_success())
        self.assertFalse(self.mvk.delete(LocationValue('formalisms.Petrinets.P2T')).is_success())  # Already deleted with Place!
        self.assertFalse(self.mvk.read(LocationValue('formalisms.Petrinets.P2T')).is_success())
        self.assertFalse(self.mvk.delete(LocationValue('formalisms.Petrinets.T2P')).is_success())  # Already deleted with Place!
        self.assertFalse(self.mvk.read(LocationValue('formalisms.Petrinets.T2P')).is_success())
        self.assertTrue(self.mvk.delete(LocationValue('formalisms.Petrinets')).is_success())
        self.assertFalse(self.mvk.read(LocationValue('formalisms.Petrinets.Transition')).is_success())
        self.assertFalse(self.mvk.read(LocationValue('formalisms.Petrinets.P2T')).is_success())
        self.assertFalse(self.mvk.read(LocationValue('formalisms.Petrinets')).is_success())

    def test_update(self):
        self.create_petrinets()
        ''' update association '''
        ul = self.mvk.update(MappingValue({UpdateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Association'),
                                           UpdateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets.P2T'),
                                           UpdateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('PlaceToTransition')})
                                           })
                             )
        self.assertTrue(ul.is_success())
        self.assertFalse(self.mvk.read(LocationValue('formalisms.Petrinets.P2T')).is_success())
        place_to_transition_log = self.mvk.read(LocationValue('formalisms.Petrinets.PlaceToTransition'))
        self.assertTrue(place_to_transition_log.is_success())
        self.assertEqual(place_to_transition_log.get_item().get_name(), StringValue('PlaceToTransition'))
        self.assertTrue(place_to_transition_log.get_item() in self.mvk.read(LocationValue('formalisms.Petrinets.Place')).get_item().get_out_associations())
        self.assertTrue(place_to_transition_log.get_item() in self.mvk.read(LocationValue('formalisms.Petrinets.Transition')).get_item().get_in_associations())

        ''' update association ends '''
        ul = self.mvk.update(MappingValue({UpdateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Association'),
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
        self.assertTrue(ul.is_success(), ul)
        self.assertFalse(self.mvk.read(LocationValue('formalisms.Petrinets.PlaceToTransition')).is_success())
        transition_to_place_log = self.mvk.read(LocationValue('formalisms.Petrinets.TransitionToPlace'))
        self.assertTrue(transition_to_place_log.is_success())
        self.assertEqual(transition_to_place_log.get_item().get_name(), StringValue('TransitionToPlace'))
        t_to_p_from = transition_to_place_log.get_item().get_from_multiplicity()
        self.assertEqual(t_to_p_from.get_node(), self.mvk.read(LocationValue('formalisms.Petrinets.Transition')).get_item())
        self.assertEqual(t_to_p_from.get_port_name(), StringValue('from_transition'))
        self.assertEqual(t_to_p_from.get_lower(), IntegerValue(3))
        self.assertEqual(t_to_p_from.get_upper(), IntegerValue(10))
        t_to_p_to = transition_to_place_log.get_item().get_to_multiplicity()
        self.assertEqual(t_to_p_to.get_node(), self.mvk.read(LocationValue('formalisms.Petrinets.Place')).get_item())
        self.assertEqual(t_to_p_to.get_port_name(), StringValue('to_place'))
        self.assertEqual(t_to_p_to.get_lower(), IntegerValue(5))
        self.assertEqual(t_to_p_to.get_upper(), IntegerValue(15))

        ''' update class '''
        ul = self.mvk.update(MappingValue({UpdateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                           UpdateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets.Place'),
                                           UpdateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('MyPlaais')})
                                           })
                             )
        self.assertTrue(ul.is_success())
        self.assertFalse(self.mvk.read(LocationValue('formalisms.Petrinets.Place')).is_success())
        myplaais_log = self.mvk.read(LocationValue('formalisms.Petrinets.MyPlaais'))
        self.assertTrue(myplaais_log.is_success())
        self.assertEqual(myplaais_log.get_item().get_name(), StringValue('MyPlaais'))

        ''' update attribute '''
        ul = self.mvk.update(MappingValue({UpdateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                           UpdateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets.MyPlaais.tokens'),
                                           UpdateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('plaais_tokens'),
                                                                                    StringValue('Attribute.type'): TypeFactory.get_type("FloatType"),
                                                                                    StringValue('Attribute.default'): FloatValue(5.0)})
                                           }))
        self.assertTrue(ul.is_success(), ul)
        self.assertFalse(self.mvk.read(LocationValue('formalisms.Petrinets.MyPlaais.tokens')).is_success())
        self.assertFalse(self.mvk.read(LocationValue('formalisms.Petrinets.Place.tokens')).is_success())
        plaais_tokens_log = self.mvk.read(LocationValue('formalisms.Petrinets.MyPlaais.plaais_tokens'))
        self.assertTrue(plaais_tokens_log.is_success())
        self.assertEqual(plaais_tokens_log.get_item().get_name(), StringValue('plaais_tokens'))
        self.assertEqual(plaais_tokens_log.get_item().get_type(), FloatType())
        self.assertEqual(plaais_tokens_log.get_item().get_default(), FloatValue(5.0))

        ''' update package '''
        ul = self.mvk.update(MappingValue({UpdateConstants.TYPE_KEY: LocationValue('mvk.object.Package'),
                                           UpdateConstants.LOCATION_KEY: LocationValue('formalisms'),
                                           UpdateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue('my_formalisms')})
                                           })
                             )
        self.assertTrue(ul.is_success(), ul)
        self.assertFalse(self.mvk.read(LocationValue('formalisms')).is_success())
        my_formalisms_log = self.mvk.read(LocationValue('my_formalisms'))
        self.assertTrue(my_formalisms_log.is_success())
        self.assertEqual(my_formalisms_log.get_item().get_name(), StringValue('my_formalisms'))

        ''' update model '''
        ul = self.mvk.update(MappingValue({UpdateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                           UpdateConstants.LOCATION_KEY: LocationValue('my_formalisms.Petrinets'),
                                           UpdateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('PetrinetFormalism')})
                                           })
                             )
        self.assertTrue(ul.is_success())
        self.assertFalse(self.mvk.read(LocationValue('my_formalisms.Petrinets')).is_success())
        petrinet_formalism_log = self.mvk.read(LocationValue('my_formalisms.PetrinetFormalism'))
        self.assertTrue(petrinet_formalism_log.is_success())
        self.assertEqual(petrinet_formalism_log.get_item().get_name(), StringValue('PetrinetFormalism'))

    def test_backup(self):
        self.create_petrinets()
        old_root = self.mvk.run(StringValue('get_root'))
        self.mvk.backup()
        self.mvk.clear()
        self.mvk.backup()
        self.assertEqual(old_root, self.mvk.run(StringValue('get_root')))

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
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('ActionLanguage.name'): StringValue('test_model')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Function'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Function.name'): StringValue('f'),
                                                                                    StringValue('Function.type'): TypeFactory.get_type('StringType')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Parameter'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Parameter.name'): StringValue('a'),
                                                                                    StringValue('Parameter.type'): TypeFactory.get_type('IntegerType'),
                                                                                    StringValue('Parameter.parameter_type'): StringValue('in')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Parameter'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Parameter.name'): StringValue('b'),
                                                                                    StringValue('Parameter.type'): TypeFactory.get_type('FloatType'),
                                                                                    StringValue('Parameter.parameter_type'): StringValue('in')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        '''
        package test
            model test_model:
                string f(a: int, b: float) {
                    int i = 5
        '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.DeclarationStatement'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Statement.name'): StringValue('decl_i')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Identifier'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.decl_i'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Expression.name'): StringValue('i')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Constant'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.decl_i'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Expression.name'): StringValue('five'),
                                                                                    StringValue('Constant.value'): IntegerValue(5)})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        '''
        package test
            model test_model:
                string f(a: int, b: float) {
                    int i = 5
                    while i > 0:
        '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.WhileLoop'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Statement.name'): StringValue('while_1')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.GreaterThan'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Expression.name'): StringValue('while_1_expr')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Navigation'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1.while_1_expr'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Expression.name'): StringValue('i'),
                                                                                    StringValue('Navigation.path'): LocationValue('i')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Constant'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1.while_1_expr'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Expression.name'): StringValue('zero'),
                                                                                    StringValue('Navigation.value'): IntegerValue(0)})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        '''
        package test
            model test_model:
                string f(a: int, b: float) {
                    int i = 5
                    while i > 0:
                        b = b + mvk.g(c=5)
        '''
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.ExpressionStatement'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1.body'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Statement.name'): StringValue('e_s_1')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Assignment'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1.body.e_s_1'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Expression.name'): StringValue('a_e_1')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Assignment'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Expression.name'): StringValue('b'),
                                                                                    StringValue('Identifier.type'): FloatType()})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Plus'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Expression.name'): StringValue('b_plus_g')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Navigation'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1.b_plus_g'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Expression.name'): StringValue('b'),
                                                                                    StringValue('Navigation.path'): LocationValue('b')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.FunctionCall'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1.b_plus_g'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Expression.name'): StringValue('g')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Navigation'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1.b_plus_g.g'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Expression.name'): StringValue('mvk'),
                                                                                    StringValue('Navigation.path'): LocationValue('mvk')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Argument'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1.b_plus_g.g'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Argument.name'): StringValue('c'),
                                                                                    StringValue('Argument.key'): LocationValue('c')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Constant'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.while_1.body.e_s_1.a_e_1.b_plus_g.g.c'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Expression.name'): StringValue('five'),
                                                                                    StringValue('Constant.value'): IntegerValue(5)})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
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
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.IfStatement'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Statement.name'): StringValue('ifstmt_1')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.GreaterThan'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.ifstmt_1'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Expression.name'): StringValue('ifstmt_1_expr')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Navigation'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.ifstmt_1.ifstmt_1_expr'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Expression.name'): StringValue('b'),
                                                                                    StringValue('Navigation.path'): LocationValue('b')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Constant'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.ifstmt_1.ifstmt_1_expr'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Expression.name'): StringValue('onehundred'),
                                                                                    StringValue('Navigation.value'): IntegerValue(100)})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
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
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.ReturnStatement'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.ifstmt_1.ifbody'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Statement.name'): StringValue('r_s_1')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Navigation'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.ifstmt_1.ifbody.r_s_1'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Expression.name'): StringValue('b'),
                                                                                    StringValue('Navigation.path'): LocationValue('b')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
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
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.ReturnStatement'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.ifstmt_1.elsebody'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Statement.name'): StringValue('r_s_2')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Minus'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.ifstmt_1.elsebody.r_s_2'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Expression.name'): StringValue('zero_minus_b')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Constant'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.ifstmt_1.elsebody.r_s_2.zero_minus_b'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Expression.name'): StringValue('zero'),
                                                                                    StringValue('Constant.value'): IntegerValue(0)})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)
        cl = self.mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.ActionLanguage.Navigation'),
                                           CreateConstants.LOCATION_KEY: LocationValue('test.test_model.f.body.ifstmt_1.elsebody.r_s_2.zero_minus_b'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Expression.name'): StringValue('b'),
                                                                                    StringValue('Navigation.path'): LocationValue('b')})
                                           })
                             )
        self.assertTrue(cl.is_success(), cl)

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
            self.assertTrue(l.is_success(), l)
            self.assertEqual(getattr(p, m)(), l.get_result())
        self.assertFalse(self.mvk.evaluate(StringValue('get_node'), loc).is_success())
        self.assertEqual(self.mvk.evaluate(StringValue('get_attribute'), loc, attr_loc=StringValue('tokens')).get_result(), self.mvk.read(loc + LocationValue('.tokens')).get_item())
        self.assertTrue(self.mvk.evaluate(StringValue('__eq__'), loc, loc))
        self.assertTrue(self.mvk.evaluate(StringValue('__ne__'), loc, LocationValue('formalisms.Petrinets.Transition')))
        self.assertEquals(self.mvk.evaluate(StringValue('get_element'), LocationValue('formalisms.Petrinets'), name=StringValue('Place')).get_result(), p)

print("var tests = [")
mvktest = MvKTest()
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
print("[\"clear\", \"\"]]")
