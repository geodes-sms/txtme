import unittest

from mvk.impl.python.constants import CreateConstants, UpdateConstants
from mvk.impl.python.datatype import IntegerType, StringType, TypeFactory, BooleanType, FloatType, TypeType, AnyType, InfiniteType
from mvk.impl.python.datavalue import MappingValue, LocationValue, StringValue, IntegerValue, SequenceValue, BooleanValue, InfiniteValue, DataValueFactory, FloatValue, AnyValue, TupleValue
from mvk.impl.python.object import Model, ModelReference, Clabject, ClabjectReference, Attribute, Association, AssociationEnd, AssociationReference, Inherits, Composition
from mvk.mvk import MvK
from mvk.impl.formalisms.StoreMapper import StoreMapper
from mvk.impl.python.util.jsonserializer import MvKEncoder

import time
import random

d = {}

class MvKTest(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName=methodName)
        self.mvk = MvK()
        self.num = 30

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.mvk.clear()
        random.seed(1)
        self.create_petrinets()

    def tearDown(self):
        self.mvk.clear()
        unittest.TestCase.tearDown(self)

    def read(self, loc, mustpass = True):
        log = self.mvk.read(loc)
        if not log.is_success() and mustpass:
            raise Exception(log)
        elif log.is_success() and not mustpass:
            raise Exception(log)
        return log

    def create(self, loc):
        log = self.mvk.create(loc)
        if not log.is_success():
            raise Exception(log)
        return log

    def update(self, loc):
        log = self.mvk.update(loc)
        if not log.is_success():
            raise Exception(log)
        return log

    def delete(self, loc):
        log = self.mvk.delete(loc)
        if not log.is_success():
            raise Exception(log)
        return log

    def evaluate(self, func, *args, **kwargs):
        log = self.mvk.evaluate(func, *args, **kwargs)
        if not log.is_success():
            raise Exception(log)
        return log

    def clear(self):
        log = self.mvk.clear()
        return log

    def conforms_to(self, model, type_model):
        log = self.mvk.conforms_to(model, type_model)
        if not log.is_success():
            raise Exception(log)
        return log

    def create_petrinets(self):
        self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('Petrinets')})
                                      })
                        )
        self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Place'),
                                                                               StringValue('Class.is_abstract'): BooleanValue(False),
                                                                               StringValue('Class.id_field'): StringValue('Place.name')})
                                      })
                        )
        self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets.Place'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('tokens'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('IntegerType'),
                                                                               StringValue('Attribute.default'): IntegerValue(0)})
                                      })
                        )
        self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets.Place'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Transition'),
                                                                               StringValue('Class.is_abstract'): BooleanValue(False),
                                                                               StringValue('Class.id_field'): StringValue('Transition.name')})
                                      })
                        )
        self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets.Transition'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.SimpleClassDiagrams.Association"),
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
        self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets.P2T'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )
        self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.SimpleClassDiagrams.Association"),
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
        self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.Petrinets.T2P'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                               StringValue('Attribute.type'): TypeFactory.get_type('StringType'),
                                                                               StringValue('Attribute.default'): StringValue('')})
                                      })
                        )

    def packageTest(self, num):
        # Create the list of packages to create
        packagelist = []
        per_level = 10

        # Use 10 packages per level
        for p in range(per_level):
            packagelist.append(("base", str(p)))
        rem_packages = num - per_level
        
        for level in packagelist:
            # Add per_level packages to the current list and continue
            if rem_packages < 0:
                break
            for p in range(per_level):
                packagelist.append((level[0] + "." + level[1], str(p)))
            rem_packages -= per_level

        # Start timing and create all of them in order
        begin = time.time()
        for package, name in packagelist:
            self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('mvk.object.Package'),
                                          CreateConstants.LOCATION_KEY: LocationValue(package),
                                          CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue(name)})
                                          })
                             )
        create_packages_time = time.time() - begin

        # Now read all of them, their values might be cached somehow
        # Though we should read in a random way to avoid bias
        readlist = list(packagelist)
        random.shuffle(readlist)
        # Fill the cache
        for package, name in readlist:
            self.read(LocationValue("%s.%s" %(package, name)))

        # Shuffle again
        random.shuffle(readlist)
        begin = time.time()
        for package, name in readlist:
            self.read(LocationValue("%s.%s" %(package, name)))
        read_cached_packages_time = time.time() - begin

        # And update some of their names now, depth first to prevent awkward algorithms here
        packagelist = [(loc, "%s_new" % name) for loc, name in packagelist]
        begin = time.time()
        for package, name in reversed(packagelist):
            self.update(MappingValue({UpdateConstants.TYPE_KEY: LocationValue('mvk.object.Package'),
                                          UpdateConstants.LOCATION_KEY: LocationValue("%s.%s" % (package, name[:-4])),
                                          UpdateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue(name)})
                                          })
                            )
        update_packages_time = time.time() - begin

        # Now read all again, again random order
        # Due to the updates, reads will be uncached!
        packagelist = [(loc.replace('.', '_new.').replace('base_new', 'base') + "_new", name) for loc, name in packagelist]
        packagelist = [("base" if loc == "base_new" else loc, name) for loc, name in packagelist]
        readlist = list(packagelist)
        random.shuffle(readlist)
        begin = time.time()
        for package, name in readlist:
            self.read(LocationValue("%s.%s" %(package, name)))
        read_uncached_packages_time = time.time() - begin

        # Delete all packages by removing the per_level root packages
        begin = time.time()
        for package, name in reversed(packagelist):
            self.delete(LocationValue("%s.%s" % (package, name)))
        delete_packages_time = time.time() - begin

        # Now do failing reads for packages
        random.shuffle(readlist)
        begin = time.time()
        for package, name in readlist:
            self.read(LocationValue("%s.%s" %(package, name)), mustpass=False)
        read_removed_packages_time = time.time() - begin

        return (create_packages_time, 
                read_cached_packages_time, 
                update_packages_time, 
                read_uncached_packages_time, 
                delete_packages_time, 
                read_removed_packages_time)

    def modelTest(self, num):
        # Create the list of models to create
        modellist = [("my_models", str(name)) for name in range(num)]

        # Start timing and create all of them in order
        begin = time.time()
        for model, name in modellist:
            self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.Petrinets'),
                                          CreateConstants.LOCATION_KEY: LocationValue(model),
                                          CreateConstants.ATTRS_KEY: MappingValue({StringValue('Petrinets.name'): StringValue(name)})
                                          })
                             )
        create_models_time = time.time() - begin

        # Now read all of them, their values might be cached somehow
        # Though we should read in a random way to avoid bias
        readlist = list(modellist)
        random.shuffle(readlist)
        for package, name in readlist:
            self.read(LocationValue("%s.%s" %(package, name)))

        random.shuffle(readlist)
        begin = time.time()
        for package, name in readlist:
            self.read(LocationValue("%s.%s" %(package, name)))
        read_cached_models_time = time.time() - begin

        # And update some of their names now, depth first to prevent awkward algorithms here
        modellist = [(loc, "%s_new" % name) for loc, name in modellist]
        begin = time.time()
        for package, name in reversed(modellist):
            self.update(MappingValue({UpdateConstants.TYPE_KEY: LocationValue('formalisms.Petrinets'),
                                          UpdateConstants.LOCATION_KEY: LocationValue("%s.%s" % (package, name[:-4])),
                                          UpdateConstants.ATTRS_KEY: MappingValue({StringValue('Petrinets.name'): StringValue(name)})
                                          })
                            )
        update_models_time = time.time() - begin

        # Now read all again, again random order
        # Due to the updates, reads will be uncached!
        readlist = list(modellist)
        random.shuffle(readlist)
        begin = time.time()
        for package, name in readlist:
            self.read(LocationValue("%s.%s" % (package, name)))
        read_uncached_models_time = time.time() - begin

        # Delete all models
        begin = time.time()
        for model, name in reversed(modellist):
            self.delete(LocationValue("%s.%s" % (model, name)))
        delete_models_time = time.time() - begin

        # Now do failing reads for models
        random.shuffle(readlist)
        begin = time.time()
        for package, name in readlist:
            self.read(LocationValue("%s.%s" %(package, name)), mustpass=False)
        read_removed_models_time = time.time() - begin

        return (create_models_time, 
                read_cached_models_time, 
                update_models_time, 
                read_uncached_models_time, 
                delete_models_time, 
                read_removed_models_time)

    def clabjectTest(self, num):
        # Create the list of models to create
        self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.Petrinets'),
                                      CreateConstants.LOCATION_KEY: LocationValue("my_models"),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Petrinets.name'): StringValue("my_clabjects")})
                                      })
                        )
        clabjectlist = [("my_models.my_clabjects", str(name)) for name in range(num)]

        # Start timing and create all of them in order
        begin = time.time()
        for model, name in clabjectlist:
            self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.Petrinets.Place'),
                                          CreateConstants.LOCATION_KEY: LocationValue(model),
                                          CreateConstants.ATTRS_KEY: MappingValue({StringValue('Place.name'): StringValue(name)})
                                          })
                             )
        create_clabjects_time = time.time() - begin

        # Now read all of them, their values might be cached somehow
        # Though we should read in a random way to avoid bias
        readlist = list(clabjectlist)
        random.shuffle(readlist)
        for package, name in readlist:
            self.read(LocationValue("%s.%s" %(package, name)))

        random.shuffle(readlist)
        begin = time.time()
        for package, name in readlist:
            self.read(LocationValue("%s.%s" %(package, name)))
        read_cached_clabjects_time = time.time() - begin

        # And update some of their names now, depth first to prevent awkward algorithms here
        clabjectlist = [(loc, "%s_new" % name) for loc, name in clabjectlist]
        begin = time.time()
        for package, name in reversed(clabjectlist):
            self.update(MappingValue({UpdateConstants.TYPE_KEY: LocationValue('formalisms.Petrinets.Place'),
                                          UpdateConstants.LOCATION_KEY: LocationValue("%s.%s" % (package, name[:-4])),
                                          UpdateConstants.ATTRS_KEY: MappingValue({StringValue('Place.name'): StringValue(name)})
                                          })
                            )
        update_clabjects_time = time.time() - begin

        # Now read all again, again random order
        # Due to the updates, reads will be uncached!
        readlist = list(clabjectlist)
        random.shuffle(readlist)
        begin = time.time()
        for package, name in readlist:
            self.read(LocationValue("%s.%s" % (package, name)))
        read_uncached_clabjects_time = time.time() - begin

        # Delete all clabjects
        begin = time.time()
        for model, name in reversed(clabjectlist):
            self.delete(LocationValue("%s.%s" % (model, name)))
        delete_clabjects_time = time.time() - begin

        # Now do failing reads for models
        random.shuffle(readlist)
        begin = time.time()
        for package, name in readlist:
            self.read(LocationValue("%s.%s" %(package, name)), mustpass=False)
        read_removed_clabjects_time = time.time() - begin

        return (create_clabjects_time, 
                read_cached_clabjects_time, 
                update_clabjects_time, 
                read_uncached_clabjects_time, 
                delete_clabjects_time, 
                read_removed_clabjects_time)

    def associationTest(self, num):
        self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.Petrinets'),
                                      CreateConstants.LOCATION_KEY: LocationValue("my_models"),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Petrinets.name'): StringValue("my_clabjects")})
                                      })
                        )
        # Create some clabjects to connect first
        # This happens untimed of course
        placelist = [("my_models.my_clabjects", "place%s" % name) for name in range(num)]
        transitionlist = [("my_models.my_clabjects", "transition%s" % name) for name in range(num)]
        for model, name in placelist:
            self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.Petrinets.Place'),
                                          CreateConstants.LOCATION_KEY: LocationValue(model),
                                          CreateConstants.ATTRS_KEY: MappingValue({StringValue('Place.name'): StringValue(name)})
                                          })
                             )
        for model, name in transitionlist:
            self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.Petrinets.Transition'),
                                          CreateConstants.LOCATION_KEY: LocationValue(model),
                                          CreateConstants.ATTRS_KEY: MappingValue({StringValue('Transition.name'): StringValue(name)})
                                          })
                             )

        associationlist = [("my_models.my_clabjects", str(name)) for name in range(num)]

        # Start timing and create all of them in order
        begin = time.time()
        for model, name in associationlist:
            self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.Petrinets.P2T'),
                                          CreateConstants.LOCATION_KEY: LocationValue(model),
                                          CreateConstants.ATTRS_KEY: MappingValue({StringValue('P2T.name'): StringValue(name),
                                                                                   StringValue('from_place'): LocationValue(model + ".place" + name),
                                                                                   StringValue('to_transition'): LocationValue(model + ".transition" + name)})
                                          })
                            )
        create_associations_time = time.time() - begin

        # Now read all of them, their values might be cached somehow
        # Though we should read in a random way to avoid bias
        readlist = list(associationlist)
        random.shuffle(readlist)
        for package, name in readlist:
            self.read(LocationValue("%s.%s" %(package, name)))

        random.shuffle(readlist)
        begin = time.time()
        for package, name in readlist:
            self.read(LocationValue("%s.%s" %(package, name)))
        read_cached_associations_time = time.time() - begin

        # And update some of their names now, depth first to prevent awkward algorithms here
        associationlist = [(loc, "%s_new" % name) for loc, name in associationlist]
        begin = time.time()
        for package, name in reversed(associationlist):
            self.update(MappingValue({CreateConstants.TYPE_KEY: LocationValue('formalisms.Petrinets.P2T'),
                                          CreateConstants.LOCATION_KEY: LocationValue("%s.%s" % (package, name[:-4])),
                                          CreateConstants.ATTRS_KEY: MappingValue({StringValue('P2T.name'): StringValue(name),
                                                                                   StringValue('from_place'): LocationValue(model + ".place" + name[:-4]),
                                                                                   StringValue('to_transition'): LocationValue(model + ".transition" + name[:-4])})
                                          })
                            )
        update_associations_time = time.time() - begin

        # Now read all again, again random order
        # Due to the updates, reads will be uncached!
        readlist = list(associationlist)
        random.shuffle(readlist)
        begin = time.time()
        for package, name in readlist:
            self.read(LocationValue("%s.%s" % (package, name)))
        read_uncached_associations_time = time.time() - begin

        # Delete all clabjects
        begin = time.time()
        for model, name in reversed(associationlist):
            self.delete(LocationValue("%s.%s" % (model, name)))
        delete_associations_time = time.time() - begin

        # Now do failing reads for models
        random.shuffle(readlist)
        begin = time.time()
        for package, name in readlist:
            self.read(LocationValue("%s.%s" %(package, name)), mustpass=False)
        read_removed_associations_time = time.time() - begin

        return (create_associations_time, 
                read_cached_associations_time, 
                update_associations_time, 
                read_uncached_associations_time, 
                delete_associations_time, 
                read_removed_associations_time)

    def attributeTest(self, num):
        self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('Megamodel')})
                                      })
                        )
        self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                      CreateConstants.LOCATION_KEY: LocationValue('formalisms.Megamodel'),
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('clabject'),
                                                                               StringValue('Class.is_abstract'): BooleanValue(False),
                                                                               StringValue('Class.id_field'): StringValue('Model.name')})
                                      })
                        )

        # Create the list of models to create
        attrlist = [str(name) for name in range(num)]

        begin = time.time()
        for attr in attrlist:
            self.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                          CreateConstants.LOCATION_KEY: LocationValue('formalisms.Megamodel.clabject'),
                                          CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue(attr),
                                                                                   StringValue('Attribute.type'): TypeFactory.get_type('IntegerType'),
                                                                                   StringValue('Attribute.default'): IntegerValue(0)})
                                          })
                             )
        create_attributes_time = time.time() - begin

        # Now read all of them, their values might be cached somehow
        # Though we should read in a random way to avoid bias
        readlist = list(attrlist)
        random.shuffle(readlist)
        for attr in readlist:
            self.read(LocationValue("formalisms.Megamodel.clabject.%s" % attr))

        random.shuffle(readlist)
        begin = time.time()
        for attr in readlist:
            self.read(LocationValue("formalisms.Megamodel.clabject.%s" % attr))
        read_cached_attributes_time = time.time() - begin

        # Update values
        begin = time.time()
        for attr in attrlist:
            self.update(MappingValue({UpdateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                          UpdateConstants.LOCATION_KEY: LocationValue("formalisms.Megamodel.clabject.%s" % attr),
                                          UpdateConstants.ATTRS_KEY: MappingValue({StringValue("Attribute.name"): StringValue(attr)})
                                          })
                       )
        update_attributes_time = time.time() - begin

        # Invalidate the cache
        self.update(MappingValue({UpdateConstants.TYPE_KEY: LocationValue('mvk.object.Package'),
                                      UpdateConstants.LOCATION_KEY: LocationValue("formalisms"),
                                      UpdateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue("my_new_formalisms")})
                                      })
                       )

        # Now read all again, again random order
        # Due to the updates, reads will be uncached!
        random.shuffle(readlist)
        begin = time.time()
        for attr in readlist:
            self.read(LocationValue("my_new_formalisms.Megamodel.clabject.%s" % attr))
        read_uncached_attributes_time = time.time() - begin

        # Delete all clabjects
        begin = time.time()
        for attr in attrlist:
            self.delete(LocationValue("my_new_formalisms.Megamodel.clabject.%s" % attr))
        delete_attributes_time = time.time() - begin

        # Now do failing reads for models
        random.shuffle(readlist)
        begin = time.time()
        for attr in readlist:
            self.read(LocationValue("my_new_formalisms.Megamodel.clabject.%s" % attr), mustpass=False)
        read_removed_attributes_time = time.time() - begin

        return (create_attributes_time, 
                read_cached_attributes_time, 
                update_attributes_time, 
                read_uncached_attributes_time, 
                delete_attributes_time, 
                read_removed_attributes_time)

    def conformance(self, num):
        model = LocationValue("formalisms.Petrinets")
        type_model = LocationValue("protected.formalisms.SimpleClassDiagrams")
        begin = time.time()
        for i in range(num):
            self.conforms_to(model, type_model)
        return time.time() - begin

    def test_package_CRUD(self):
        d["package"] = self.packageTest(self.num)

    def test_model_CRUD(self):
        d["model"] = self.modelTest(self.num)

    def test_clabject_CRUD(self):
        d["clabject"] = self.clabjectTest(self.num)

    def test_association_CRUD(self):
        d["association"] = self.associationTest(self.num)

    def test_attribute_CRUD(self):
        d["attribute"] = self.attributeTest(self.num)

def printResults():
    def convert(values, num):
        return [float(v*1000)/num for v in values]

    def printResults(physicaltype, values, num):
        c = convert(values, num)
        print("%10s\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f" % (physicaltype, c[0], c[1], c[2], c[3], c[4], c[5]))

    print("%10s\tC\tRc\tU\tRnc\tD\tRf" % "type")
    for v in ["package", "model", "clabject", "association", "attribute"]:
        printResults(v, d[v], 30)

def runTests():
    unittest.main()
