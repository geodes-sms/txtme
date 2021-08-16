"""
Created on 6-jan.-2014

@author: Simon
"""
import logging
import unittest

from mvk.impl.python.datatype import IntegerType, VoidType, AnyType, FloatType, \
    StringType, BooleanType, SetType, SequenceType, UnionType, TypeType, \
    TypeFactory, TupleType, MappingType, EnumType, IteratorType
from mvk.impl.python.datavalue import SequenceValue
from mvk.util import logger
from mvk.util.logger import get_logger


logger = get_logger()


class DataTypeTestCase(unittest.TestCase):
    def test_factory(self):
        tests = [
                     ('VoidType', VoidType()),
                     ('AnyType', AnyType()),
                     ('FloatType', FloatType()),
                     ('StringType', StringType()),
                     ('BooleanType', BooleanType()),
                     ('IntegerType', IntegerType()),
                     ('TypeType', TypeType()),
                     ('SequenceType[FloatType]', SequenceType(basetype=FloatType())),
                     ('SetType[IntegerType]', SetType(basetype=IntegerType())),
                     ('MappingType(IntegerType: FloatType)', MappingType(keytype=IntegerType(), valuetype=FloatType())),
                     ('UnionType(BooleanType, StringType)', UnionType(types=SequenceValue(value=[BooleanType(), StringType()]))),
                     ('SequenceType[UnionType(SetType[IntegerType], MappingType(StringType: MappingType(IntegerType: FloatType)))]', SequenceType(basetype=UnionType(types=SequenceValue(value = [SetType(basetype=IntegerType()),
                                                                                                                                                                                                  MappingType(keytype=StringType(),
                                                                                                                                                                                                              valuetype = MappingType(keytype=IntegerType(),
                                                                                                                                                                                                                                      valuetype=FloatType()))])))),
                     ('enum Animals{Cat, Dog}', EnumType(values=['Cat', 'Dog'])),
                     ('iterator<IntegerType>', IteratorType(IntegerType()))
                 ]
        self.assertEquals(TypeType(), TypeType())
        for t in tests:
            assert logger.debug('Parsing %s' % t[0])
            returned_type = TypeFactory.get_type(t[0])
            self.assertEquals(t[1], returned_type)


if __name__ == "__main__":
    unittest.main()
