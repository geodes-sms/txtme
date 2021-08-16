import unittest

from mvk.impl.python.datavalue import MappingValue, StringValue, IntegerValue, LocationValue, BooleanValue, InfiniteValue
from mvk.impl.python.datatype import StringType, IntegerType
from mvk.impl.python.constants import CreateConstants, UpdateConstants
from mvk.impl.python.util.jsonserializer import MvKEncoder
from mvk.impl.client.jsondeserializer import MvKDecoder
from mvk.mvk import MvK
from mvk.impl.python.changelog import MvKCompositeLog

class UndoTest(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName=methodName)
        self.mvk = MvK()
        self.jsonencoder = MvKEncoder()
        self.jsondecoder = MvKDecoder()

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.mvk.clear()

    def tearDown(self):
        self.mvk.clear()
        unittest.TestCase.tearDown(self)


    def create(self, params):
        # Serialize as if it was a network
        #return self.jsondecoder.decode(self.jsonencoder.encode(self.mvk.create(self.jsondecoder.decode(self.jsonencoder.encode(params)))))
        out = self.mvk.create(self.jsondecoder.decode(self.jsonencoder.encode(params)))
        enc = self.jsonencoder.encode(out)
        dec = self.jsondecoder.decode(enc)
        return dec

    def update(self, params):
        # Serialize as if it was a network
        return self.jsondecoder.decode(self.jsonencoder.encode(self.mvk.update(self.jsondecoder.decode(self.jsonencoder.encode(params)))))

    def read(self, params):
        # Serialize as if it was a network
        return self.jsondecoder.decode(self.jsonencoder.encode(self.mvk.read(self.jsondecoder.decode(self.jsonencoder.encode(params)))))

    def delete(self, params):
        # Serialize as if it was a network
        output = self.mvk.delete(self.jsondecoder.decode(self.jsonencoder.encode(params)))
        encoded = self.jsonencoder.encode(output)
        res = self.jsondecoder.decode(encoded)
        return res

    def processInverse(self, inverselist):
        cl = MvKCompositeLog()
        cl.set_status_code(IntegerValue(0))
        cl.set_status_message(StringValue("INVERTED"))
        for inverse in inverselist:
            if inverse[0] == "delete":
                log = self.delete(inverse[1])
            elif inverse[0] == "create":
                log = self.create(inverse[1])
            elif inverse[0] == "update":
                log = self.update(inverse[1])
            else:
                raise Exception("Unknown log: " + str(inverse))
            cl.add_log(log)
            if not log.is_success():
                self.fail(log)
        if cl.logs.len() == IntegerValue(1):
            return cl.logs[IntegerValue(0)]
        else:
            return cl

    def test_undo_package_create(self):
        cl = self.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue(""),
                                       CreateConstants.TYPE_KEY: StringValue("mvk.object.Package"),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue("name"): StringValue("a")})}))
        self.assertTrue(self.mvk.read(LocationValue("a")).is_success())
        inverse = cl.get_inverse()
        self.assertTrue(self.mvk.read(LocationValue("a")).is_success())
        cl = self.processInverse(inverse)
        self.assertFalse(self.mvk.read(LocationValue("a")).is_success())

    def test_undo_package_create_composite(self):
        cl = self.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue("a.b.c.d.e.f"),
                                       CreateConstants.TYPE_KEY: StringValue("mvk.object.Package"),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue("name"): StringValue("g")})}))
        self.assertTrue(self.mvk.read(LocationValue("a")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("a.b")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("a.b.c")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("a.b.c.d")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("a.b.c.d.e")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("a.b.c.d.e.f")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("a.b.c.d.e.f.g")).is_success())
        inverse = cl.get_inverse()
        self.assertTrue(self.mvk.read(LocationValue("a")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("a.b")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("a.b.c")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("a.b.c.d")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("a.b.c.d.e")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("a.b.c.d.e.f")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("a.b.c.d.e.f.g")).is_success())
        cl = self.processInverse(inverse)
        self.assertFalse(self.mvk.read(LocationValue("a")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("a.b")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("a.b.c")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("a.b.c.d")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("a.b.c.d.e")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("a.b.c.d.e.f")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("a.b.c.d.e.f.g")).is_success())

    def test_undo_package_update(self):
        cl = self.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue(""),
                                       CreateConstants.TYPE_KEY: StringValue("mvk.object.Package"),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue("name"): StringValue("a")})}))
        self.assertTrue(self.mvk.read(LocationValue("a")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("b")).is_success())

        ul = self.update(MappingValue({CreateConstants.LOCATION_KEY: LocationValue("a"),
                                       CreateConstants.TYPE_KEY: StringValue("mvk.object.Package"),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue("name"): StringValue("b")})}))
        # Make sure that the rename went well
        self.assertFalse(self.mvk.read(LocationValue("a")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("b")).is_success())

        inverse = ul.get_inverse()
        self.assertFalse(self.mvk.read(LocationValue("a")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("b")).is_success())

        cl = self.processInverse(inverse)
        # Rename should be undone now
        self.assertTrue(self.mvk.read(LocationValue("a")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("b")).is_success())

    def test_undo_and_redo_package_update(self):
        cl = self.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue(""),
                                       CreateConstants.TYPE_KEY: StringValue("mvk.object.Package"),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue("name"): StringValue("a")})}))
        self.assertTrue(self.mvk.read(LocationValue("a")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("b")).is_success())

        ul = self.update(MappingValue({CreateConstants.LOCATION_KEY: LocationValue("a"),
                                       CreateConstants.TYPE_KEY: StringValue("mvk.object.Package"),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue("name"): StringValue("b")})}))
        # Make sure that the rename went well
        self.assertFalse(self.mvk.read(LocationValue("a")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("b")).is_success())

        for i in range(10):
            # This code should be able to loop: alternate between an undo and redo 10 times
            self.assertFalse(self.mvk.read(LocationValue("a")).is_success())
            self.assertTrue(self.mvk.read(LocationValue("b")).is_success())

            ul = self.processInverse(ul.get_inverse())
            # Rename should be undone now
            self.assertTrue(self.mvk.read(LocationValue("a")).is_success())
            self.assertFalse(self.mvk.read(LocationValue("b")).is_success())

            # But now undo our undo (technically a redo)
            ul = self.processInverse(ul.get_inverse())

    def test_undo_twice_package(self):
        cl = self.create(MappingValue({CreateConstants.LOCATION_KEY: LocationValue(""),
                                       CreateConstants.TYPE_KEY: StringValue("mvk.object.Package"),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue("name"): StringValue("a")})}))
        ul = self.update(MappingValue({UpdateConstants.LOCATION_KEY: LocationValue("a"),
                                       UpdateConstants.TYPE_KEY: StringValue("mvk.object.Package"),
                                       UpdateConstants.ATTRS_KEY: MappingValue({StringValue("name"): StringValue("b")})}))
        self.assertFalse(self.mvk.read(LocationValue("a")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("b")).is_success())

        self.processInverse(ul.get_inverse())
        self.assertTrue(self.mvk.read(LocationValue("a")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("b")).is_success())

        self.processInverse(cl.get_inverse())
        self.assertFalse(self.mvk.read(LocationValue("a")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("b")).is_success())

    def test_undo_create_model(self):
        cl = self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                       CreateConstants.LOCATION_KEY: LocationValue('test_formalisms'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('Petrinets')})
                                       })
                        )
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.SimpleClassDiagrams.name")).is_success())

        self.processInverse(cl.get_inverse())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.SimpleClassDiagrams.name")).is_success())

    def test_undo_update_model(self):
        cl = self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                       CreateConstants.LOCATION_KEY: LocationValue('test_formalisms'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('Petrinets')})
                                       })
                        )
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.SimpleClassDiagrams.name")).is_success())
        ul = self.update(MappingValue({UpdateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                       UpdateConstants.LOCATION_KEY: LocationValue('test_formalisms.Petrinets'),
                                       UpdateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('extended_Petrinets')})
                                       })
                        )
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.extended_Petrinets")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.extended_Petrinets.SimpleClassDiagrams.name")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.SimpleClassDiagrams.name")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())

        # Now undo
        self.processInverse(ul.get_inverse())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.SimpleClassDiagrams.name")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.extended_Petrinets.SimpleClassDiagrams.name")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.extended_Petrinets")).is_success())

    def test_undo_delete_model(self):
        cl = self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                       CreateConstants.LOCATION_KEY: LocationValue('test_formalisms'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('Petrinets')})
                                       })
                        )
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.SimpleClassDiagrams.name")).is_success())

        dl = self.delete(LocationValue("test_formalisms.Petrinets"))
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.SimpleClassDiagrams.name")).is_success())

        # Undo the deletion
        self.processInverse(dl.get_inverse())
        # Now everything should be just like before
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.SimpleClassDiagrams.name")).is_success())

    def test_undo_create_clabject(self):
        self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                  CreateConstants.LOCATION_KEY: LocationValue('test_formalisms'),
                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('Petrinets')})
                                      })
                        )
        self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                  CreateConstants.LOCATION_KEY: LocationValue('test_formalisms.Petrinets'),
                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): StringType(),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        cl = self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                  CreateConstants.LOCATION_KEY: LocationValue('test_formalisms.Petrinets'),
                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Place'),
                                                                           StringValue('Class.is_abstract'): BooleanValue(False),
                                                                           StringValue('Class.id_field'): StringValue('Place.name')})
                                      })
                        )
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.id_field")).is_success())

        self.processInverse(cl.get_inverse())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.name")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.is_abstract")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.id_field")).is_success())

        self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                  CreateConstants.LOCATION_KEY: LocationValue('test_formalisms.Petrinets'),
                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Place'),
                                                                           StringValue('Class.is_abstract'): BooleanValue(False),
                                                                           StringValue('Class.id_field'): StringValue('Place.name')})
                                      })
                        )
        self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('test_formalisms.Petrinets.Place'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('tokens'),
                                                                               StringValue('Attribute.type'): IntegerType(),
                                                                               StringValue('Attribute.default'): IntegerValue(0)})
                                      })
                        )
        self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('test_formalisms.Petrinets.Place'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): StringType(),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.tokens")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())

        self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('test_formalisms.Petrinets'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Petrinets.name'): StringValue('myPetrinet')})
                                           })
                             )
        cl = self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('test_formalisms.Petrinets.Place'),
                                           CreateConstants.LOCATION_KEY: LocationValue('models.myPetrinet'),
                                           CreateConstants.ATTRS_KEY: MappingValue({StringValue('Place.name'): StringValue('p1'),
                                                                                    StringValue("tokens"): IntegerValue(5)})
                                           })
                             )

        self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.tokens")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models.myPetrinet")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models.myPetrinet.p1.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models.myPetrinet.p1.Place.tokens")).is_success())

        self.processInverse(cl.get_inverse())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.tokens")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models.myPetrinet")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("models.myPetrinet.p1.Place.name")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("models.myPetrinet.p1.Place.tokens")).is_success())

    def test_undo_update_clabject(self):
        self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                  CreateConstants.LOCATION_KEY: LocationValue('test_formalisms'),
                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('Petrinets')})
                                      })
                        )
        self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                  CreateConstants.LOCATION_KEY: LocationValue('test_formalisms.Petrinets'),
                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): StringType(),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                  CreateConstants.LOCATION_KEY: LocationValue('test_formalisms.Petrinets'),
                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Place'),
                                                                           StringValue('Class.is_abstract'): BooleanValue(False),
                                                                           StringValue('Class.id_field'): StringValue('Place.name')})
                                      })
                        )
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.id_field")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place2")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place2.Class.name")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place2.Class.is_abstract")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place2.Class.id_field")).is_success())

        ul = self.update(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                  CreateConstants.LOCATION_KEY: LocationValue('test_formalisms.Petrinets.Place'),
                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Place2'),
                                                                           StringValue('Class.is_abstract'): BooleanValue(False),
                                                                           StringValue('Class.id_field'): StringValue('Place2.name')})
                                      })
                        )
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.name")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.is_abstract")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place2")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place2.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place2.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place2.Class.id_field")).is_success())

        self.processInverse(ul.get_inverse())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.id_field")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place2")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place2.Class.name")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place2.Class.is_abstract")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place2.Class.id_field")).is_success())

        self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                  CreateConstants.LOCATION_KEY: LocationValue('test_formalisms.Petrinets'),
                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Place'),
                                                                           StringValue('Class.is_abstract'): BooleanValue(False),
                                                                           StringValue('Class.id_field'): StringValue('Place.name')})
                                      })
                        )
        self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('test_formalisms.Petrinets.Place'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('tokens'),
                                                                               StringValue('Attribute.type'): IntegerType(),
                                                                               StringValue('Attribute.default'): IntegerValue(0)})
                                      })
                        )
        self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('test_formalisms.Petrinets.Place'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): StringType(),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.tokens")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())

        self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('test_formalisms.Petrinets'),
                                  CreateConstants.LOCATION_KEY: LocationValue('models'),
                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('Petrinets.name'): StringValue('myPetrinet')})
                                 })
                   )
        self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('test_formalisms.Petrinets.Place'),
                                  CreateConstants.LOCATION_KEY: LocationValue('models.myPetrinet'),
                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('Place.name'): StringValue('p1'),
                                                                           StringValue("Place.tokens"): IntegerValue(1)})
                                 })
                   )
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.tokens")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models.myPetrinet")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models.myPetrinet.p1.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models.myPetrinet.p1.Place.tokens")).is_success())
        self.assertEquals(self.mvk.read(LocationValue("models.myPetrinet.p1.Place.tokens")).get_item().value, IntegerValue(1))

        ul1 = self.update(MappingValue({CreateConstants.TYPE_KEY: LocationValue('test_formalisms.Petrinets.Place'),
                                       CreateConstants.LOCATION_KEY: LocationValue('models.myPetrinet.p1'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue("Place.tokens"): IntegerValue(5)})
                                      })
                        )

        self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.tokens")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models.myPetrinet")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models.myPetrinet.p1.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models.myPetrinet.p1.Place.tokens")).is_success())
        self.assertEquals(self.mvk.read(LocationValue("models.myPetrinet.p1.Place.tokens")).get_item().value, IntegerValue(5))

        ul2 = self.update(MappingValue({CreateConstants.TYPE_KEY: LocationValue('test_formalisms.Petrinets.Place'),
                                       CreateConstants.LOCATION_KEY: LocationValue('models.myPetrinet.p1'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue("Place.name"): StringValue("p2")})
                                      })
                        )

        self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.tokens")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models.myPetrinet")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("models.myPetrinet.p1.Place.name")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("models.myPetrinet.p1.Place.tokens")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models.myPetrinet.p2.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models.myPetrinet.p2.Place.tokens")).is_success())
        self.assertEquals(self.mvk.read(LocationValue("models.myPetrinet.p2.Place.tokens")).get_item().value, IntegerValue(5))

        # Roll back the name change first
        self.processInverse(ul2.get_inverse())

        self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.tokens")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models.myPetrinet")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models.myPetrinet.p1.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models.myPetrinet.p1.Place.tokens")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("models.myPetrinet.p2.Place.name")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("models.myPetrinet.p2.Place.tokens")).is_success())
        self.assertEquals(self.mvk.read(LocationValue("models.myPetrinet.p1.Place.tokens")).get_item().value, IntegerValue(5))

        # And now the change to the number of tokens
        self.processInverse(ul1.get_inverse())
        
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.tokens")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models.myPetrinet")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models.myPetrinet.p1.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models.myPetrinet.p1.Place.tokens")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("models.myPetrinet.p2.Place.name")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("models.myPetrinet.p2.Place.tokens")).is_success())
        self.assertEquals(self.mvk.read(LocationValue("models.myPetrinet.p1.Place.tokens")).get_item().value, IntegerValue(1))

    def test_undo_delete_clabject(self):
        self.setupPetrinets()
        self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('test_formalisms.Petrinets'),
                                  CreateConstants.LOCATION_KEY: LocationValue('models'),
                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('Petrinets.name'): StringValue('myPetrinet')})
                                 })
                   )
        self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('test_formalisms.Petrinets.Place'),
                                  CreateConstants.LOCATION_KEY: LocationValue('models.myPetrinet'),
                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('Place.name'): StringValue('p1'),
                                                                           StringValue("Place.tokens"): IntegerValue(1)})
                                 })
                   )
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.tokens")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models.myPetrinet")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models.myPetrinet.p1")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models.myPetrinet.p1.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models.myPetrinet.p1.Place.tokens")).is_success())
        self.assertEquals(self.mvk.read(LocationValue("models.myPetrinet.p1.Place.tokens")).get_item().value, IntegerValue(1))

        # Delete the instantiation
        dl = self.delete(LocationValue("models.myPetrinet.p1"))
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.tokens")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models.myPetrinet")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("models.myPetrinet.p1")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("models.myPetrinet.p1.Place.name")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("models.myPetrinet.p1.Place.tokens")).is_success())

        self.processInverse(dl.get_inverse())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.tokens")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models.myPetrinet")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models.myPetrinet.p1")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models.myPetrinet.p1.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models.myPetrinet.p1.Place.tokens")).is_success())
        self.assertEquals(self.mvk.read(LocationValue("models.myPetrinet.p1.Place.tokens")).get_item().value, IntegerValue(1))

    def setupPetrinets(self):
        logs = []
        logs.append(self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                  CreateConstants.LOCATION_KEY: LocationValue('test_formalisms'),
                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('Petrinets')})
                                      })
                        ))
        logs.append(self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                  CreateConstants.LOCATION_KEY: LocationValue('test_formalisms.Petrinets'),
                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Place'),
                                                                           StringValue('Class.is_abstract'): BooleanValue(False),
                                                                           StringValue('Class.id_field'): StringValue('Place.name')})
                                      })
                        ))
        logs.append(self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('test_formalisms.Petrinets.Place'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('tokens'),
                                                                               StringValue('Attribute.type'): IntegerType(),
                                                                               StringValue('Attribute.default'): IntegerValue(0)})
                                      })
                        ))
        logs.append(self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('test_formalisms.Petrinets.Place'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): StringType(),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        ))
        logs.append(self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                      CreateConstants.LOCATION_KEY: LocationValue('test_formalisms.Petrinets'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Transition'),
                                                                               StringValue('Class.is_abstract'): BooleanValue(False),
                                                                               StringValue('Class.id_field'): StringValue('Transition.name')})
                                      })
                        ))
        logs.append(self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('test_formalisms.Petrinets.Transition'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): StringType(),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        ))
        logs.append(self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.SimpleClassDiagrams.Association"),
                                      CreateConstants.LOCATION_KEY: LocationValue('test_formalisms.Petrinets'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('from_class'): LocationValue('test_formalisms.Petrinets.Place'),
                                                                               StringValue('to_class'): LocationValue('test_formalisms.Petrinets.Transition'),
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
                        ))
        logs.append(self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('test_formalisms.Petrinets.P2T'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): StringType(),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        ))
        logs.append(self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.SimpleClassDiagrams.Association"),
                                      CreateConstants.LOCATION_KEY: LocationValue('test_formalisms.Petrinets'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('from_class'): LocationValue('test_formalisms.Petrinets.Transition'),
                                                                               StringValue('to_class'): LocationValue('test_formalisms.Petrinets.Place'),
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
                        ))
        logs.append(self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('test_formalisms.Petrinets.T2P'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): StringType(),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        ))
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.tokens")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.P2T")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.P2T.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.T2P")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.T2P.name")).is_success())
        return logs

    def test_undo_create_association(self):
        self.setupPetrinets()
        self.assertFalse(self.mvk.read(LocationValue("models")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("models.myPetrinet")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("models.myPetrinet.p1")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("models.myPetrinet.t1")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("models.myPetrinet.p1_to_t1")).is_success())

        # Now do some instantiations
        self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('test_formalisms.Petrinets'),
                                  CreateConstants.LOCATION_KEY: LocationValue('models'),
                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('Petrinets.name'): StringValue('myPetrinet')})
                                 })
                   )
        self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('test_formalisms.Petrinets.Place'),
                                  CreateConstants.LOCATION_KEY: LocationValue('models.myPetrinet'),
                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('Place.name'): StringValue('p1'),
                                                                           StringValue("Place.tokens"): IntegerValue(1)})
                                 })
                   )
        self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('test_formalisms.Petrinets.Transition'),
                                  CreateConstants.LOCATION_KEY: LocationValue('models.myPetrinet'),
                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('Transition.name'): StringValue('t1')})
                                 })
                   )
        cl = self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('test_formalisms.Petrinets.P2T'),
                                       CreateConstants.LOCATION_KEY: LocationValue('models.myPetrinet'),
                                       CreateConstants.ATTRS_KEY: MappingValue({StringValue('P2T.name'): StringValue('p1_to_t1'),
                                                                                StringValue('from_place'): LocationValue('models.myPetrinet.p1'),
                                                                                StringValue('to_transition'): LocationValue('models.myPetrinet.t1')
                                                                                })
                                      })
                         )
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.tokens")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models.myPetrinet")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models.myPetrinet.p1")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models.myPetrinet.t1")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models.myPetrinet.p1_to_t1")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models.myPetrinet.p1_to_t1.P2T.name")).is_success())

        self.processInverse(cl.get_inverse())
 
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.tokens")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models.myPetrinet")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models.myPetrinet.p1")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("models.myPetrinet.t1")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("models.myPetrinet.p1_to_t1")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("models.myPetrinet.p1_to_t1.P2T.name")).is_success())

    def test_undo_update_association(self):
        self.setupPetrinets()

        r = self.read(LocationValue("test_formalisms.Petrinets.Transition2Place"))
        self.assertFalse(r.is_success())
        r = self.read(LocationValue("test_formalisms.Petrinets.P2T"))
        self.assertTrue(r.is_success())
        t_to_p_from = r.get_item().from_multiplicity
        self.assertEqual(t_to_p_from.node, LocationValue('test_formalisms.Petrinets.Place'))
        self.assertEqual(t_to_p_from.port_name, StringValue('from_place'))
        self.assertEqual(t_to_p_from.lower, IntegerValue(0))
        self.assertEqual(t_to_p_from.upper, InfiniteValue('+'))
        t_to_p_to = r.get_item().to_multiplicity
        self.assertEqual(t_to_p_to.node, LocationValue('test_formalisms.Petrinets.Transition'))
        self.assertEqual(t_to_p_to.port_name, StringValue('to_transition'))
        self.assertEqual(t_to_p_to.lower, IntegerValue(0))
        self.assertEqual(t_to_p_to.upper, InfiniteValue('+'))

        ul = self.update(MappingValue({UpdateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Association'),
                                           UpdateConstants.LOCATION_KEY: LocationValue('test_formalisms.Petrinets.P2T'),
                                           UpdateConstants.ATTRS_KEY: MappingValue({StringValue('from_class'): LocationValue('test_formalisms.Petrinets.Transition'),
                                                                                    StringValue('to_class'): LocationValue('test_formalisms.Petrinets.Place'),
                                                                                    StringValue('Class.name'): StringValue('TransitionToPlace'),
                                                                                    StringValue('Association.from_port'): StringValue('from_transition'),
                                                                                    StringValue('Association.from_min'): IntegerValue(3),
                                                                                    StringValue('Association.from_max'): IntegerValue(10),
                                                                                    StringValue('Association.to_port'): StringValue('to_place'),
                                                                                    StringValue('Association.to_min'): IntegerValue(5),
                                                                                    StringValue('Association.to_max'): IntegerValue(15)})
                                           })
                             )

        r = self.read(LocationValue("test_formalisms.Petrinets.P2T"))
        self.assertFalse(r.is_success())
        r = self.read(LocationValue("test_formalisms.Petrinets.TransitionToPlace"))
        self.assertTrue(r.is_success())
        t_to_p_from = r.get_item().from_multiplicity
        self.assertEqual(t_to_p_from.node, LocationValue('test_formalisms.Petrinets.Transition'))
        self.assertEqual(t_to_p_from.port_name, StringValue('from_transition'))
        self.assertEqual(t_to_p_from.lower, IntegerValue(3))
        self.assertEqual(t_to_p_from.upper, IntegerValue(10))
        t_to_p_to = r.get_item().to_multiplicity
        self.assertEqual(t_to_p_to.node, LocationValue('test_formalisms.Petrinets.Place'))
        self.assertEqual(t_to_p_to.port_name, StringValue('to_place'))
        self.assertEqual(t_to_p_to.lower, IntegerValue(5))
        self.assertEqual(t_to_p_to.upper, IntegerValue(15))

        self.processInverse(ul.get_inverse())

        r = self.read(LocationValue("test_formalisms.Petrinets.Transition2Place"))
        self.assertFalse(r.is_success())
        r = self.read(LocationValue("test_formalisms.Petrinets.P2T"))
        self.assertTrue(r.is_success())
        t_to_p_from = r.get_item().from_multiplicity
        self.assertEqual(t_to_p_from.node, LocationValue('test_formalisms.Petrinets.Place'))
        self.assertEqual(t_to_p_from.port_name, StringValue('from_place'))
        self.assertEqual(t_to_p_from.lower, IntegerValue(0))
        self.assertEqual(t_to_p_from.upper, InfiniteValue('+'))
        t_to_p_to = r.get_item().to_multiplicity
        self.assertEqual(t_to_p_to.node, LocationValue('test_formalisms.Petrinets.Transition'))
        self.assertEqual(t_to_p_to.port_name, StringValue('to_transition'))
        self.assertEqual(t_to_p_to.lower, IntegerValue(0))
        self.assertEqual(t_to_p_to.upper, InfiniteValue('+'))

    def test_undo_delete_association(self):
        self.setupPetrinets()

        r = self.read(LocationValue("test_formalisms.Petrinets.P2T"))
        self.assertTrue(r.is_success())
        t_to_p_from = r.get_item().from_multiplicity
        self.assertEqual(t_to_p_from.node, LocationValue('test_formalisms.Petrinets.Place'))
        self.assertEqual(t_to_p_from.port_name, StringValue('from_place'))
        self.assertEqual(t_to_p_from.lower, IntegerValue(0))
        self.assertEqual(t_to_p_from.upper, InfiniteValue('+'))
        t_to_p_to = r.get_item().to_multiplicity
        self.assertEqual(t_to_p_to.node, LocationValue('test_formalisms.Petrinets.Transition'))
        self.assertEqual(t_to_p_to.port_name, StringValue('to_transition'))
        self.assertEqual(t_to_p_to.lower, IntegerValue(0))
        self.assertEqual(t_to_p_to.upper, InfiniteValue('+'))

        dl = self.delete(LocationValue('test_formalisms.Petrinets.P2T'))

        self.assertFalse(self.read(LocationValue("test_formalisms.Petrinets.P2T")).is_success())

        self.processInverse(dl.get_inverse())

        r = self.read(LocationValue("test_formalisms.Petrinets.Transition2Place"))
        self.assertFalse(r.is_success())
        r = self.read(LocationValue("test_formalisms.Petrinets.P2T"))
        self.assertTrue(r.is_success())
        t_to_p_from = r.get_item().from_multiplicity
        self.assertEqual(t_to_p_from.node, LocationValue('test_formalisms.Petrinets.Place'))
        self.assertEqual(t_to_p_from.port_name, StringValue('from_place'))
        self.assertEqual(t_to_p_from.lower, IntegerValue(0))
        self.assertEqual(t_to_p_from.upper, InfiniteValue('+'))
        t_to_p_to = r.get_item().to_multiplicity
        self.assertEqual(t_to_p_to.node, LocationValue('test_formalisms.Petrinets.Transition'))
        self.assertEqual(t_to_p_to.port_name, StringValue('to_transition'))
        self.assertEqual(t_to_p_to.lower, IntegerValue(0))
        self.assertEqual(t_to_p_to.upper, InfiniteValue('+'))

    def test_undo_redo_all(self):
        logs = self.setupPetrinets()

        # Now we should have ourself a petrinet formalism
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.tokens")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.id_field")).is_success())

        # But undo everything
        undo_logs = []
        for log in reversed(logs):
            undo_logs.append(self.processInverse(log.get_inverse()))

        # We should have nothing anymore
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.name")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.is_abstract")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.id_field")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.tokens")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.name")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.name")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.is_abstract")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.id_field")).is_success())

        # But now we redo everything!
        redo_logs = []
        for i, log in enumerate(reversed(undo_logs)):
            redo_logs.append(self.processInverse(log.get_inverse()))
            if not redo_logs[-1].is_success():
                self.fail(redo_logs[-1])

        # And everything should be back
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.tokens")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.id_field")).is_success())

    def test_undo_remove_model_chain(self):
        self.setupPetrinets()

        # The Petrinets model should be present, including all its clabjects (Place and Transition) and associations (P2T and T2P)
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.tokens")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.P2T")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.P2T.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.T2P")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.T2P.name")).is_success())

        dl = self.delete(LocationValue("test_formalisms.Petrinets"))
        
        # Everything in the model, including the model itself, should be removed
        # Of course, the empty package remains
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.name")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.is_abstract")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.id_field")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.tokens")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.name")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.name")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.is_abstract")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.id_field")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.P2T")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.P2T.name")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.T2P")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.T2P.name")).is_success())

        # Now revert the delete
        self.processInverse(dl.get_inverse())

        # The Petrinets model should be present again, including all its clabjects (Place and Transition) and associations (P2T and T2P)
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.tokens")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.P2T")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.P2T.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.T2P")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.T2P.name")).is_success())

    def test_undo_remove_nonempty_package(self):
        self.setupPetrinets()

        # The Petrinets model should be present, including all its clabjects (Place and Transition) and associations (P2T and T2P)
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.tokens")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.P2T")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.P2T.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.T2P")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.T2P.name")).is_success())

        dl = self.delete(LocationValue("test_formalisms"))
        
        # Everything in the model, including the model itself, should be removed
        # Of course, the empty package remains
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.name")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.is_abstract")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.id_field")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.tokens")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.name")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.name")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.is_abstract")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.id_field")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.P2T")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.P2T.name")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.T2P")).is_success())
        self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.T2P.name")).is_success())

        # Now revert the delete
        self.processInverse(dl.get_inverse())

        # The Petrinets model should be present again, including all its clabjects (Place and Transition) and associations (P2T and T2P)
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.tokens")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.P2T")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.P2T.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.T2P")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.T2P.name")).is_success())

    def test_undo_redo_partial(self):
        logs = self.setupPetrinets()

        # Now we should have ourself a petrinet formalism
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.tokens")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.P2T")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.P2T.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.T2P")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.T2P.name")).is_success())

        # But undo some logs and verify that the correct things are removed inbetween
        #  0 --> create Model Petrinets
        #  5 --> create Clabject Transition
        #  7 --> create Association P2T
        undo_logs = []
        for reverse_num, log in enumerate(reversed(logs)):
            undo_logs.append(self.processInverse(log.get_inverse()))
            num = len(logs) - reverse_num
        
            if num == 7:
                # Undo the creation of Association P2T and T2P
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.name")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.is_abstract")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.id_field")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.tokens")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.name")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.name")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.is_abstract")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.id_field")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.P2T")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.P2T.name")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.T2P")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.T2P.name")).is_success())
            elif num == 5:
                # Followed by the deletion of Clabject Transition
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.name")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.is_abstract")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.id_field")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.tokens")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.name")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.name")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.is_abstract")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.id_field")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.P2T")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.P2T.name")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.T2P")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.T2P.name")).is_success())
            elif num == 1:
                # And the deletion of everything
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.name")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.is_abstract")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.id_field")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.tokens")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.name")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.name")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.is_abstract")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.id_field")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.P2T")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.P2T.name")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.T2P")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.T2P.name")).is_success())

        # But now we redo everything!
        redo_logs = []
        for i, log in enumerate(reversed(undo_logs)):
            redo_logs.append(self.processInverse(log.get_inverse()))
            if not redo_logs[-1].is_success():
                self.fail(redo_logs[-1])

            if i == 0:
                # The recreation of the Model Petrinets
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.name")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.is_abstract")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.id_field")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.tokens")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.name")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.name")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.is_abstract")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.id_field")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.P2T")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.P2T.name")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.T2P")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.T2P.name")).is_success())
            elif i == 5:
                # Recreation of Clabject Transition (and Place)
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.name")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.is_abstract")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.id_field")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.tokens")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.name")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.name")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.is_abstract")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.id_field")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.P2T")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.P2T.name")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.T2P")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.T2P.name")).is_success())
            elif i == 7:
                # And recreation of P2T but not yet T2P
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.name")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.is_abstract")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.id_field")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.tokens")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.name")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.name")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.is_abstract")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.id_field")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.P2T")).is_success())
                self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.P2T.name")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.T2P")).is_success())
                self.assertFalse(self.mvk.read(LocationValue("test_formalisms.Petrinets.T2P.name")).is_success())

        # And everything should be back at the end
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.Class.id_field")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.tokens")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Place.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.name")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.is_abstract")).is_success())
        self.assertTrue(self.mvk.read(LocationValue("test_formalisms.Petrinets.Transition.Class.id_field")).is_success())


#if __name__ == "__main__":
def runTests():
    unittest.main()
