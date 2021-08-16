"""
Created on 3-jan.-2014

@author: Simon
"""
import unittest

import mvk.impl.python.datavalue
from mvk.impl.python.datatype import TupleType, IntegerType, SequenceType, \
    SetType, MappingType, StringType, TypeType, BooleanType, FloatType, TypeFactory, \
    AnyType, VoidType, UnionType, LocationType
from mvk.impl.python.exception import MvKKeyError, MvKIndexError, MvKTypeError, \
    MvKValueError
from mvk.impl.rdf.datavalue import VoidValue, AnyValue, BooleanValue, \
    IntegerValue, FloatValue, StringValue, TupleValue, SequenceValue, SetValue, \
    MappingValue, DataValueFactory, LocationValue
from mvk.interfaces.exception import MvKZeroDivisionError
from mvk.util import logger


class DataValueTestCase(unittest.TestCase):
    def test_factory(self):
        self.assertEquals(DataValueFactory.create_instance(1).get_value(), 1)
        self.assertEquals(DataValueFactory.create_instance(1),
                          mvk.impl.python.datavalue.IntegerValue(1))
        self.assertEquals(DataValueFactory.create_instance((1, 2, 3)),
                          mvk.impl.python.datavalue.TupleValue((mvk.impl.python.datavalue.IntegerValue(1),
                                                                mvk.impl.python.datavalue.IntegerValue(2),
                                                                mvk.impl.python.datavalue.IntegerValue(3))))
        self.assertEquals(DataValueFactory.create_instance([1, 2, 3]),
                          mvk.impl.python.datavalue.SequenceValue([mvk.impl.python.datavalue.IntegerValue(1),
                                                                   mvk.impl.python.datavalue.IntegerValue(2),
                                                                   mvk.impl.python.datavalue.IntegerValue(3)]))
        self.assertEquals(DataValueFactory.create_instance(set([1, 2, 3])),
                          mvk.impl.python.datavalue.SetValue(set([mvk.impl.python.datavalue.IntegerValue(1),
                                                                  mvk.impl.python.datavalue.IntegerValue(2),
                                                                  mvk.impl.python.datavalue.IntegerValue(3)])))
        self.assertEquals(DataValueFactory.create_instance([1, 2, 3, [4, 5, 6]]),
                          mvk.impl.python.datavalue.SequenceValue([mvk.impl.python.datavalue.IntegerValue(1),
                                                                   mvk.impl.python.datavalue.IntegerValue(2),
                                                                   mvk.impl.python.datavalue.IntegerValue(3),
                                                                   mvk.impl.python.datavalue.SequenceValue([mvk.impl.python.datavalue.IntegerValue(4),
                                                                                                            mvk.impl.python.datavalue.IntegerValue(5),
                                                                                                            mvk.impl.python.datavalue.IntegerValue(6)])]))
        self.assertEquals(DataValueFactory.create_instance({1: '1', 2: '2', 3: '3'}),
                          mvk.impl.python.datavalue.MappingValue({mvk.impl.python.datavalue.IntegerValue(1): mvk.impl.python.datavalue.StringValue('1'),
                                                                  mvk.impl.python.datavalue.IntegerValue(2): mvk.impl.python.datavalue.StringValue('2'),
                                                                  mvk.impl.python.datavalue.IntegerValue(3): mvk.impl.python.datavalue.StringValue('3')}))


if __name__ == "__main__":
    unittest.main()
