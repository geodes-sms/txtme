'''
Created on 12-mrt.-2014

@author: Simon
'''
import time
import unittest
import datetime

from pylab import *
from random import randint

from mvk.impl.python.constants import CreateConstants
from mvk.impl.python.datatype import TypeFactory, StringType, BooleanType, \
    TypeType, AnyType, IntegerType
from mvk.impl.python.datavalue import LocationValue, MappingValue, StringValue, \
    IntegerValue, BooleanValue, SequenceValue, AnyValue, InfiniteValue
from mvk.impl.python.python_representer import PythonRepresenter
from mvk.mvk import MvK


def visualize(x, y, x_label, y_label, the_title, filename):
    figure()
    plot(x, y)
    xlabel(x_label)
    ylabel(y_label)
    title(the_title)
    savefig("results/%s_%s.png" % (filename, datetime.datetime.now().strftime("%y_%m_%d_%H_%M_%S")))


def test_create_models(mvk, number_of_steps=10, stepsize=100):
    location = LocationValue('test_package')
    create_times = []
    read_times = []
    k = 0
    for i in range(number_of_steps):
        now = time.time()
        nr_of_models = (i + 1) * stepsize
        for j in range(nr_of_models):
            k += 1
            cl = mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                               CreateConstants.LOCATION_KEY: location,
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue(str(k))})
                                               })
                                 )
            assert cl.is_success(), cl
        t = time.time() - now
        create_times.append(t)
        print 'Time to create %i models: %s seconds.' % (nr_of_models, t)
        now = time.time()
        mvk.read(LocationValue('test_package.%s' % randint(0, nr_of_models - 1)))
        t = time.time() - now
        read_times.append(t)
        print 'Time to read a random model: %s seconds' % (t)
    visualize([(i + 1) * stepsize for i in range(number_of_steps)], create_times, 'number of models', 'time in seconds', 'Creating Models', ('create_models_%i' % nr_of_models))
    visualize([(i + 1) * stepsize for i in range(number_of_steps)], read_times, 'number of models', 'time in seconds', 'Reading Model', ('read_models_%i' % nr_of_models))


def test_create_model(mvk, number_of_steps=10, stepsize=100):
    location = LocationValue('test_package')
    create_times = []
    k = 0
    for i in range(number_of_steps):
        nr_of_models = (i + 1) * stepsize
        for j in range(nr_of_models - 1):
            k += 1
            cl = mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                          CreateConstants.LOCATION_KEY: location,
                                          CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue(str(k))})
                                          })
                            )
            assert cl.is_success(), cl
        now = time.time()
        k += 1
        cl = mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                      CreateConstants.LOCATION_KEY: location,
                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue(str(k))})
                                      })
                        )
        assert cl.is_success(), cl
        t = time.time() - now
        create_times.append(t)
        print 'Time to create model with %i other models: %s seconds.' % (nr_of_models, t)
    visualize([(i + 1) * stepsize for i in range(number_of_steps)], create_times, 'number of models', 'time in seconds', 'Creating 1 Model', ('create_model_%i' % nr_of_models))


def test_create_clabjects(mvk, number_of_steps=10, stepsize=100):
    create_times = []
    read_times = []
    k = 0
    mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                  CreateConstants.LOCATION_KEY: LocationValue(''),
                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('test_model')})
                                  })
                    )
    for i in range(number_of_steps):
        now = time.time()
        nr_of_clabjects = (i + 1) * stepsize
        for j in range(nr_of_clabjects):
            k += 1
            cl = mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                               CreateConstants.LOCATION_KEY: LocationValue('test_model'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Place_%s' % k),
                                                                                        StringValue('Class.is_abstract'): BooleanValue(False)})
                                               })
                                 )
            assert cl.is_success()
            cl = mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                               CreateConstants.LOCATION_KEY: LocationValue('test_model.Place_%s' % k),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('tokens'),
                                                                                        StringValue('Attribute.type'): TypeFactory.get_type('IntegerType'),
                                                                                        StringValue('Attribute.default'): IntegerValue(0)})
                                               })
                                 )
        t = time.time() - now
        create_times.append(t)
        print 'Time to create %i clabjects: %s seconds.' % (nr_of_clabjects, t)
        now = time.time()
        mvk.read(LocationValue('test_model.Clabject_%s' % randint(0, nr_of_clabjects - 1)))
        t = time.time() - now
        read_times.append(t)
        print 'Time to read a random clabject: %s seconds' % (t)
    visualize([(i + 1) * stepsize for i in range(number_of_steps)], create_times, 'number of clabjects', 'time in seconds', 'Creating Clabjects', ('create_clabjects_%i' % nr_of_clabjects))
    visualize([(i + 1) * stepsize for i in range(number_of_steps)], read_times, 'number of clabjects', 'time in seconds', 'Reading Clabject', ('read_clabjects_%i' % nr_of_clabjects))


def test_package_depth(mvk, depth=5, stepsize=1, size=5):
    def populate_modelverse(depth, pkg, size):
        if depth > 0:
            for i in range(size):
                curr_pkg = ""
                if pkg == "":
                    curr_pkg = str(i)
                else:
                    curr_pkg = pkg + "." + str(i)
                cl = mvk.create(MappingValue({CreateConstants.TYPE_KEY: PythonRepresenter.PACKAGE,
                                              CreateConstants.LOCATION_KEY: LocationValue(pkg),
                                              CreateConstants.ATTRS_KEY: MappingValue({StringValue('name'): StringValue(str(i))})
                                              })
                                )
                assert cl.is_success(), cl
                populate_modelverse(depth - 1, curr_pkg, size)

    def find_in_modelverse(depth, count):
        # find the middle package
        pkg = str(count / 2)
        curr_pkg = pkg
        for _ in range(depth - 1):
            curr_pkg += "." + pkg

        mvk.read(LocationValue(curr_pkg))

    create_times = []
    read_times = []
    curr_depth = stepsize
    while curr_depth <= depth:
        mvk.clear()
        now = time.time()
        populate_modelverse(curr_depth, "", size)
        t = time.time() - now
        print 'Time on depth %i: %s' % (curr_depth, t)
        create_times.append(t)
        now = time.time()
        find_in_modelverse(curr_depth, size)
        t = time.time() - now
        read_times.append(t)
        curr_depth += stepsize
    visualize([pow(size, (i + 1) * stepsize) for i in range(depth)], create_times, 'number of packages', 'time in seconds', 'Creating Packages', ('depth_create_%i' % depth))
    visualize([pow(size, (i + 1) * stepsize) for i in range(depth)], read_times, 'number of packages', 'time in seconds', 'Reading Packages', ('depth_read_%i' % depth))


def test_connectivity(mvk, number_of_steps=10, stepsize=100):
    create_times = []
    created_objects_list = []
    read_times = []
    association_len = []
    k = 0
    mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
                                  CreateConstants.LOCATION_KEY: LocationValue(''),
                                  CreateConstants.ATTRS_KEY: MappingValue({StringValue('SimpleClassDiagrams.name'): StringValue('test_model')})
                                  })
                    )
    for i in range(number_of_steps):
        connected_items = {}
        now = time.time()
        nr_of_clabjects = (i + 1) * stepsize
        created_objects = nr_of_clabjects
        for j in range(nr_of_clabjects):
            k += 1
            connected_items[k] = []
            cl = mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                                               CreateConstants.LOCATION_KEY: LocationValue('test_model'),
                                               CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.name'): StringValue('Place_%s' % k),
                                                                                        StringValue('Class.is_abstract'): BooleanValue(False)})
                                               })
                                 )
            assert cl.is_success(), cl
            for l in range(j):
                cl = mvk.create(MappingValue({CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'),
                                                   CreateConstants.LOCATION_KEY: LocationValue('test_model'),
                                                   CreateConstants.ATTRS_KEY: MappingValue({StringValue('Inheritance.name'): StringValue('%s_i_%s' % (k, k - l - 1)),
                                                                                            StringValue('from_class'): LocationValue('test_model.Place_%s' % k),
                                                                                            StringValue('to_class'): LocationValue('test_model.Place_%s' % (k - l - 1))})
                                                   })
                                     )
                assert cl.is_success(), cl
                created_objects += 1
                connected_items[k].append(k - l - 1)
        created_objects_list.append(created_objects)
        t = time.time() - now
        create_times.append(t)
        print 'Time to create %i clabjects, and connect them: %s seconds.' % (nr_of_clabjects, t)
        now = time.time()
        all_assocs = mvk.read(LocationValue('test_model.Place_%s' % k)).get_item().get_all_associations()
        association_len.append(all_assocs.len().get_value())
        print 'Number of associations: %i' % all_assocs.len().get_value()
        t = time.time() - now
        read_times.append(t)
        print 'Time to get all associations from a clabject: %s seconds' % (t)
    visualize(created_objects_list, create_times, 'number of elements', 'time in seconds', 'Creating and Connecting Clabjects', ('create_and_connect_clabjects_%i' % nr_of_clabjects))
    visualize(created_objects_list, read_times, 'number of elements', 'time in seconds', 'Get All Associations', ('get_all_associations_%i' % nr_of_clabjects))
    visualize(created_objects_list, read_times, 'number of elements', 'number of associations', 'Get All Associations', ('get_all_associations_length_%i' % nr_of_clabjects))

if __name__ == "__main__":
    mvk = MvK()
    while True:
        data = raw_input('>>> ').split(' ')
        mvk.clear()
        globals()[data[0]](mvk, *[int(i) for i in data[1:]])
