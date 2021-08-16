"""
Created on 3-jan.-2014

@author: Simon
"""
import unittest

from mvk.impl.python.datatype import TupleType, IntegerType, SequenceType, \
    SetType, MappingType, StringType, TypeType, BooleanType, FloatType, TypeFactory, \
    AnyType, VoidType, UnionType, LocationType, InfiniteType
from mvk.impl.python.datavalue import VoidValue, AnyValue, BooleanValue, \
    IntegerValue, FloatValue, StringValue, TupleValue, SequenceValue, SetValue, \
    MappingValue, DataValueFactory, LocationValue, EnumValue, InfiniteValue
from mvk.impl.python.exception import MvKKeyError, MvKIndexError, MvKTypeError, \
    MvKValueError
from mvk.interfaces.exception import MvKZeroDivisionError
from mvk.util import logger
from mvk.util.logger import get_logger


logger = get_logger()


class DataValueTestCase(unittest.TestCase):
    def test_constructors(self):
        VoidValue()
        AnyValue()
        BooleanValue(True)
        BooleanValue(False)
        IntegerValue(1)
        IntegerValue(0)
        IntegerValue(-1)
        FloatValue(1.0)
        FloatValue(0.0)
        FloatValue(-1.0)
        StringValue("")
        StringValue("Hello world!")
        TupleValue(value=(IntegerValue(1), IntegerValue(2), IntegerValue(3),))
        TupleValue(value=(IntegerValue(1),))
        TupleValue(value=())
        SequenceValue(value=[IntegerValue(1), IntegerValue(2), IntegerValue(3)])
        SequenceValue(value=[IntegerValue(1)])
        SequenceValue(value=[])
        SetValue(value=set([IntegerValue(1), IntegerValue(2), IntegerValue(3)]))
        SetValue(value=set([IntegerValue(1)]))
        SetValue(value=set([]))
        MappingValue(value={StringValue('1'): IntegerValue(1),
                            StringValue('2'): IntegerValue(2),
                            StringValue('3'): IntegerValue(3)})
        MappingValue(value={StringValue('1'): IntegerValue(1)})
        MappingValue(value={})

    def test_numeric_operations(self):
        values = [(IntegerValue(3), 3),
                  (IntegerValue(-7), -7),
                  (IntegerValue(0), 0),
                  (BooleanValue(True), True),
                  (BooleanValue(False), False),
                  (FloatValue(4.0), 4.0),
                  (FloatValue(-10.0), -10.0),
                  (FloatValue(0.0), 0.0)]
        type_errors = [StringValue('test'),
                       SequenceValue(value=[IntegerValue(1),
                                            IntegerValue(2),
                                            IntegerValue(3)])]

        operators = ['+', '-', '*', '/', '%']
        for o in operators:
            for i, val_i in enumerate(values):
                for j, val_j in enumerate(values[i:]):
                    assert logger.debug('%s %s %s' % (val_i[1], o, val_j[1]))
                    try:
                        self.assertEquals(eval('val_i[0] %s val_j[0]' % o),
                                          eval('val_i[0].__class__(val_i[1] %s val_j[1])' % o))
                    except MvKZeroDivisionError:
                        self.assertRaises(ZeroDivisionError, lambda x: eval('x[0] %s x[1]' % o), (val_i[1], val_j[1]))
                for t_e in type_errors:
                    self.assertRaises(MvKTypeError, lambda x: eval('x[0] %s x[1]' % o), (val_i[0], t_e))

        logical_operators = [('&', 'and'), ('|', 'or')]
        for o in logical_operators:
            for i, val_i in enumerate(values):
                for j, val_j in enumerate(values[i:]):
                    assert logger.debug('%s %s %s' % (val_i[1], o, val_j[1]))
                    res = eval('val_i[1] %s val_j[1]' % o[1])
                    if res is val_i[1]:
                        cls = val_i[0].__class__
                    else:
                        cls = val_j[0].__class__
                    self.assertEquals(eval('val_i[0] %s val_j[0]' % o[0]),
                                      cls(res))
                for t_e in type_errors:
                    self.assertRaises(MvKTypeError, lambda x: eval('x[0] %s x[1]' % o[0]), (val_i[0], t_e))

        comparison_operators = ['<', '<=', '>', '>=']
        for o in comparison_operators:
            for i, val_i in enumerate(values):
                for j, val_j in enumerate(values[i:]):
                    assert logger.debug('%s %s %s' % (val_i[1], o, val_j[1]))
                    self.assertEquals(eval('val_i[0] %s val_j[0]' % o),
                                      eval('BooleanValue(val_i[1] %s val_j[1])' % o))
                for t_e in type_errors:
                    self.assertRaises(MvKTypeError, lambda x: eval('x[0] %s x[1]' % o), (val_i[0], t_e))

        unary_operators = ['+%s', '-%s', 'abs(%s)']
        for o in unary_operators:
            for i, val_i in enumerate(values):
                assert logger.debug(o % val_i[1])
                self.assertEquals(eval(o % 'val_i[0]'),
                                  eval('%s(%s)' % (val_i[0].__class__.__name__, (o % 'val_i[1]'))))

        unary_math_operators = [('floor', 'FloatValue'), ('ceil', 'FloatValue'), ('trunc', 'IntegerValue')]
        import math
        for o in unary_math_operators:
            for i, val_i in enumerate(values):
                assert logger.debug('%s(%s)' % (o[0], val_i[1]))
                self.assertEquals(eval('val_i[0].%s()' % o[0]),
                                  eval('%s(math.%s(val_i[1]))' % (o[1], o[0])))

        for val_i in values:
            assert logger.debug('%s.nonzero()' % (val_i[1]))
            self.assertEquals(val_i[0].nonzero(),
                              BooleanValue(val_i[1]))

    def test_string_operations(self):
        strings = ['Hello world!',
                   '!',
                   'Hello',
                   'world!',
                   'o w',
                   'Model everything!',
                   'o',
                   'l',
                   'a']
        type_errors = [IntegerValue(0),
                       FloatValue(1.0),
                       BooleanValue(True),
                       SequenceValue(value=[IntegerValue(1),
                                            IntegerValue(2),
                                            IntegerValue(3)])]

        ints = [(None, -1),
                (IntegerValue(-1), -1),
                (IntegerValue(0), 0),
                (IntegerValue(2), 2)]

        unary_operators = ['lower',
                           'upper',
                           'swapcase',
                           'title',
                           'capitalize']
        for o in unary_operators:
            for str_i in strings:
                assert logger.debug('%s.%s()' % (str_i, o))
                self.assertEquals(eval('StringValue(str_i).%s()' % o),
                                  eval('StringValue(str_i.%s())' % o))
                self.assertEquals(IntegerValue(len(str_i)),
                                  StringValue(str_i).len())

        binary_operators_int = ['count',
                                'find',
                                'rfind']
        for o in binary_operators_int:
            for i, str_i in enumerate(strings):
                for j, str_j in enumerate(strings[i:]):
                    assert logger.debug('%s.%s(%s)' % (str_i, o, str_j))
                    self.assertEquals(eval('StringValue(str_i).%s(StringValue(str_j))' % o),
                                      eval('IntegerValue(str_i.%s(str_j))' % o))
                for t_e in type_errors:
                    self.assertRaises(MvKTypeError, lambda x: eval('StringValue(x[0]).%s(x[1])' % o), (str_i, t_e))

        binary_operators_str = ['strip',
                                'rstrip',
                                'lstrip']
        for o in binary_operators_str:
            for i, str_i in enumerate(strings):
                for str_j in strings[i:] + [None]:
                    assert logger.debug('%s.%s(%s)' % (str_i, o, str_j))
                    self.assertEquals(eval('StringValue(str_i).%s(None if str_j == None else StringValue(str_j))' % o),
                                      eval('StringValue(str_i.%s(str_j))' % o))
                for t_e in type_errors:
                    assert logger.debug('%s.%s(%s)' % (str_i, o, t_e))
                    self.assertRaises(MvKTypeError, (lambda s, x, t: eval('StringValue(s).%s(t)' % x)), str_i, o, t_e)

        for i, str_i in enumerate(strings):
            for str_j in strings[i:]:
                self.assertEquals(StringValue(str_i) + StringValue(str_j),
                                  StringValue(str_i + str_j))
            for t_e in type_errors:
                self.assertRaises(MvKTypeError, lambda s, t: StringValue(s) + t, str_i, t_e)

        ternary_operators = ['split',
                             'rsplit']
        for o in ternary_operators:
            for i, str_i in enumerate(strings):
                for str_j in strings[i:] + [None]:
                    for k in ints:
                        assert logger.debug('%s.%s(%s, %s)' % (str_i, o, str_j, str(k[1])))
                        self.assertEquals(eval('StringValue(str_i).%s(None if str_j == None else StringValue(str_j), k[0])' % o),
                                          eval('SequenceValue(value=[StringValue(val) for val in str_i.%s(str_j, k[1])])' % o))
                    self.assertRaises(MvKTypeError, lambda s, x: eval('StringValue(s).%s(StringValue(s), StringValue(s))' % x), str_i, o)
                for t_e in type_errors:
                    for k in ints:
                        self.assertRaises(MvKTypeError, lambda s, x, t, i: eval('StringValue(s).%s(t, i)' % x), str_i, o, t_e, k[0])

        quaternary_operators = ['replace']
        for o in quaternary_operators:
            for i, str_i in enumerate(strings):
                for str_j in strings[i:]:
                    for str_k in strings:
                        for l in ints:
                            assert logger.debug('%s.%s(%s, %s, %s)' % (str_i, o, str_j, str_k, str(l[1])))
                            self.assertEquals(eval('StringValue(str_i).%s(StringValue(str_j), StringValue(str_k), l[0])' % o),
                                              eval('StringValue(str_i.%s(str_j, str_k, l[1]))' % o))
                        self.assertRaises(MvKTypeError, lambda s, x, t, u, i: eval('StringValue(s).%s(StringValue(t), StringValue(u), StringValue(i))' % x), str_i, o, str_j, str_k, str_k)
                    for t_e in type_errors:
                        for l in ints:
                            assert logger.debug('%s.%s(%s, %s, %s)' % (str_i, o, str_j, t_e, str(l[1])))
                            self.assertRaises(MvKTypeError, lambda s, x, t, u, i: eval('StringValue(s).%s(StringValue(t), u, i)' % x), str_i, o, str_j, t_e, l[0])
                for t_e in type_errors:
                    for str_k in strings:
                        for l in ints:
                            assert logger.debug('%s.%s(%s, %s, %s)' % (str_i, o, t_e, str_k, str(l[1])))
                            self.assertRaises(MvKTypeError, lambda s, x, t, u, i: eval('StringValue(s).%s(t, StringValue(u), i)' % x), str_i, o, t_e, str_k, l[0])

    def test_tuple_operations(self):
        values = (IntegerValue(1),
                  StringValue("test"),
                  FloatValue(-1999),
                  BooleanValue(True),)
        t = TupleValue(value=values)
        self.assertEquals(IntegerValue(len(values)), t.len())
        self.assertRaises(MvKIndexError, t.__getitem__, IntegerValue(-5))
        self.assertRaises(MvKIndexError, t.__getitem__, IntegerValue(4))
        self.assertRaises(MvKTypeError, t.__getitem__, StringValue('4'))
        it = t.__iter__()
        for v in values:
            self.assertEquals(v, it.next())
            self.assertTrue(v in t)
        self.assertFalse(it.has_next())
        t = TupleValue()
        for v in values:
            self.assertFalse(v in t)

    def test_sequence_operations(self):
        int_values = [IntegerValue(1),
                      IntegerValue(-1999),
                      IntegerValue(0),
                      IntegerValue(0)]

        s = SequenceValue(value=int_values)
        self.assertEquals(IntegerValue(len(int_values)), s.len())
        self.assertRaises(MvKIndexError, s.__getitem__, IntegerValue(-5))
        self.assertRaises(MvKIndexError, s.__getitem__, IntegerValue(4))
        it = s.__iter__()
        for v in int_values:
            self.assertEquals(v, it.next())
            self.assertTrue(v in s)
        s_empty = SequenceValue()
        self.assertEquals(IntegerValue(0), s_empty.len())
        for v in int_values:
            self.assertFalse(v in s_empty)
        index_type_errors = [StringValue('1'),
                             FloatValue(-1999),
                             SequenceValue(value=[IntegerValue(1)])]
        for i_t_e in index_type_errors:
            self.assertRaises(MvKTypeError, s.__getitem__, i_t_e)
            self.assertRaises(MvKTypeError, s.__setitem__,
                              i_t_e, IntegerValue(1))
            self.assertRaises(MvKTypeError, s.__delitem__, i_t_e)
            self.assertRaises(MvKTypeError, s.index,
                              IntegerValue(1), i_t_e, IntegerValue(3))
            self.assertRaises(MvKTypeError, s.index,
                              IntegerValue(1), IntegerValue(3), i_t_e)
            self.assertRaises(MvKTypeError, s.insert, i_t_e, IntegerValue(1))
        s_len = s.len().get_value()
        for i in range(s_len):
            self.assertEquals(int_values[-(i + 1)], s.pop())
        self.assertEquals(IntegerValue(0), s.len())
        self.assertRaises(MvKIndexError, s.pop)
        for v in int_values:
            s.append(v)
            s.remove(v)
        self.assertEquals(IntegerValue(0), s.len())
        self.assertRaises(MvKValueError, s.remove, IntegerValue(888))
        s.extend(SequenceValue(value=int_values))
        self.assertEquals(IntegerValue(4), s.len())
        del s[IntegerValue(1)]
        self.assertEquals(IntegerValue(3), s.len())
        self.assertEquals(SequenceValue(value=[IntegerValue(1),
                                               IntegerValue(0),
                                               IntegerValue(0)]),
                          s)
        self.assertRaises(MvKIndexError, s.__delitem__, IntegerValue(3))
        self.assertRaises(MvKTypeError, s.extend, IntegerValue(5))
        self.assertRaises(MvKTypeError, s.extend, StringValue("123"))
        to_add = [IntegerValue(4), IntegerValue(5), IntegerValue(6)]
        s.extend(SetValue(value=set(to_add)))
        for i in to_add:
            self.assertTrue(i in s)
        s.append(IntegerValue(0))
        """ s == [1, 0, 0, 4, 5, 6, 0] """
        self.assertEquals(IntegerValue(1), s.index(IntegerValue(0)))
        self.assertEquals(IntegerValue(3), s.index(IntegerValue(4)))
        self.assertEquals(IntegerValue(6), s.index(IntegerValue(0), IntegerValue(3)))
        self.assertRaises(MvKValueError, s.index, IntegerValue(7))
        self.assertRaises(MvKValueError, s.index, IntegerValue(7), IntegerValue(0))
        self.assertRaises(MvKValueError, s.index, IntegerValue(7), IntegerValue(0), IntegerValue(-1))
        self.assertRaises(MvKValueError, s.index, IntegerValue(0), IntegerValue(3), IntegerValue(5))
        self.assertRaises(MvKValueError, s.index, IntegerValue(0), IntegerValue(1), IntegerValue(1))
        new_values = [
                        IntegerValue(-1000),
                        IntegerValue(500),
                        IntegerValue(35),
                        IntegerValue(500),
                        IntegerValue(335),
                        IntegerValue(0),
                        IntegerValue(0)
                      ]
        for i, val_i in enumerate(new_values):
            s[IntegerValue(i)] = val_i
        """ s == [-1000, 500, 35, 500, 335, 0, 0] """
        for i, val_i in enumerate(new_values):
            self.assertEquals(val_i, s[IntegerValue(i)])
        s.insert(IntegerValue(-1), IntegerValue(300))
        self.assertEquals(IntegerValue(8), s.len())
        self.assertEquals(IntegerValue(300), s[IntegerValue(6)])
        s.insert(IntegerValue(1), IntegerValue(345))
        self.assertEquals(IntegerValue(9), s.len())
        self.assertEquals(IntegerValue(345), s[IntegerValue(1)])
        """ s = [-1000, 345, 500, 35, 500, 335, 0, 300, 0] """
        s.remove(IntegerValue(0))
        self.assertEquals(IntegerValue(8), s.len())
        self.assertEquals(IntegerValue(300), s[IntegerValue(6)])
        s.reverse()
        self.assertEquals(SequenceValue(value=[IntegerValue(0),
                                               IntegerValue(300),
                                               IntegerValue(335),
                                               IntegerValue(500),
                                               IntegerValue(35),
                                               IntegerValue(500),
                                               IntegerValue(345),
                                               IntegerValue(-1000)]),
                          s)
        s.sort()
        self.assertEquals(SequenceValue(value=[IntegerValue(-1000),
                                               IntegerValue(0),
                                               IntegerValue(35),
                                               IntegerValue(300),
                                               IntegerValue(335),
                                               IntegerValue(345),
                                               IntegerValue(500),
                                               IntegerValue(500)]),
                          s)
        self.assertEquals(IntegerValue(2), s.count(IntegerValue(500)))
        self.assertRaises(MvKIndexError, s.__setitem__, IntegerValue(8),
                          IntegerValue(500))

    def test_set_operations(self):
        init_val = set([IntegerValue(1),
                        IntegerValue(0),
                        IntegerValue(-1000),
                        IntegerValue(5999),
                        IntegerValue(344)])
        s = SetValue(value=init_val)
        self.assertEquals(IntegerValue(5), s.len())
        it = s.__iter__()
        while it.has_next():
            val = it.next()
            self.assertTrue(val in s)
            old_len = s.len()
            s.add(val)
            self.assertEquals(s.len(), old_len)

        other_sets = [
                        set([]),
                        set([IntegerValue(1),
                             IntegerValue(5)]),
                        set([IntegerValue(1),
                             IntegerValue(0),
                             IntegerValue(-1000),
                             IntegerValue(5999),
                             IntegerValue(344)]),
                        set([IntegerValue(1),
                             IntegerValue(0),
                             IntegerValue(-1000),
                             IntegerValue(5999),
                             IntegerValue(344),
                             IntegerValue(20)])
                      ]
        binary_set_ops = ['union', 'difference', 'symmetric_difference', 'intersection']
        for o in binary_set_ops:
            for o_s in other_sets:
                self.assertEquals(eval('s.%s(SetValue(value=o_s))' % o),
                                  eval('SetValue(value=(init_val.%s(o_s)))' % o))
        binary_set_ops_bool = ['issubset', 'issuperset']
        for o in binary_set_ops_bool:
            for o_s in other_sets:
                self.assertEquals(eval('s.%s(SetValue(value=o_s))' % o),
                                  eval('BooleanValue(init_val.%s(o_s))' % o))

        s.add(IntegerValue(425))
        self.assertTrue(IntegerValue(425) in s)
        s.remove(IntegerValue(0))
        self.assertFalse(IntegerValue(0) in s)

        unhashable_values = [SequenceValue(value=[IntegerValue(1)]),
                             SetValue(value=set([IntegerValue(1)]))]
        need_hashable = ['add', 'remove', '__contains__']
        for o in need_hashable:
            for v in unhashable_values:
                self.assertRaises(MvKTypeError, lambda s, o, t: eval('s.%s(t)' % o), s, o, v)

        not_sets = [IntegerValue(1),
                    StringValue('test'),
                    SequenceValue(value=[IntegerValue(1)])]
        for o in set(binary_set_ops).union(set(binary_set_ops_bool)):
            for v in not_sets:
                self.assertRaises(MvKTypeError, lambda s, o, t: eval('s.%s(t)' % o), s, o, v)

    def test_mapping_operations(self):
        initvalue = {
                        IntegerValue(1): StringValue('1'),
                        IntegerValue(5): StringValue('5'),
                        IntegerValue(0): StringValue('0'),
                     }
        m = MappingValue(value=initvalue)
        it = m.__iter__()
        keys = SetValue(value=set([]))
        while it.has_next():
            key = it.next()
            keys.add(key)
            self.assertTrue(key in m)

        self.assertEquals(keys, m.keys())
        self.assertEquals(set([StringValue('1'),
                               StringValue('5'),
                               StringValue('0')]),
                          set(m.values().get_value()))

        m[IntegerValue(3)] = StringValue('100')
        self.assertEquals(IntegerValue(4), m.len())
        self.assertEquals(StringValue('100'), m[IntegerValue(3)])
        m[IntegerValue(0)] = StringValue('3')
        self.assertEquals(IntegerValue(4), m.len())
        self.assertEquals(StringValue('3'), m[IntegerValue(0)])
        del m[IntegerValue(0)]
        self.assertEquals(IntegerValue(3), m.len())
        self.assertRaises(MvKKeyError, m.__getitem__, IntegerValue(0))
        self.assertRaises(MvKKeyError, m.__delitem__, IntegerValue(0))
        self.assertEquals(StringValue('100'), m.pop(IntegerValue(3)))
        self.assertRaises(MvKKeyError, m.pop, IntegerValue(3))
        self.assertEquals(StringValue('100'), m.pop(IntegerValue(3), StringValue('100')))

        unhashable_values = [SequenceValue(value=[IntegerValue(1)]),
                             SetValue(value=set([IntegerValue(1)]))]
        need_hashable_b = ['__getitem__', '__delitem__', '__contains__', 'pop']
        need_hashable_t = ['__setitem__']
        for v in unhashable_values:
            for o in need_hashable_b:
                self.assertRaises(MvKTypeError, lambda m, o, t: eval('m.%s(t)' % o), m, o, v)
            for o in need_hashable_t:
                self.assertRaises(MvKTypeError, lambda m, o, t: eval('m.%s(t, IntegerValue(0))' % o), m, o, v)

        m.clear()
        self.assertEquals(IntegerValue(0), m.len())

    def test_numeric_equality(self):
        equal_values = [
                            (IntegerValue(1), IntegerValue(1)),
                            (FloatValue(1.0), FloatValue(1.0)),
                            (BooleanValue(True), BooleanValue(True)),
                            (BooleanValue(False), BooleanValue(False)),
                            (IntegerValue(1), BooleanValue(True)),
                            (IntegerValue(1), FloatValue(1.0)),
                            (FloatValue(1.0), BooleanValue(True)),
                            (FloatValue(0.0), BooleanValue(False)),
                            (FloatValue(5.0), IntegerValue(5)),
                            (IntegerValue(0), BooleanValue(False))
                        ]
        for e_v in equal_values:
            self.assertEquals(e_v[0], e_v[1])
        not_equal_values = [
                                (IntegerValue(1), IntegerValue(3)),
                                (FloatValue(1.0), FloatValue(1.1)),
                                (BooleanValue(True), BooleanValue(False)),
                            ]
        for n_e_v in not_equal_values:
            self.assertNotEquals(n_e_v[0], n_e_v[1])

    def test_string_equality(self):
        self.assertEquals(StringValue('hello'), StringValue('hello'))
        self.assertNotEquals(StringValue('hello'), StringValue('HELLO'))
        self.assertNotEquals(StringValue('hello'), StringValue('Hello'))
        self.assertEqual(LocationValue('a.b.c'), LocationValue('a.b.c'))
        self.assertEqual(StringValue('a.b.c'), LocationValue('a.b.c'))
        self.assertEqual(LocationValue('a.b.c'), StringValue('a.b.c'))

    def test_sequence_equality(self):
        self.assertEquals(SequenceValue(value=[]),
                          SequenceValue(value=[]))
        self.assertEquals(SequenceValue(value=[IntegerValue(1)]),
                          SequenceValue(value=[IntegerValue(1)]))
        self.assertEquals(SequenceValue(value=[IntegerValue(1), IntegerValue(3)]),
                          SequenceValue(value=[IntegerValue(1), IntegerValue(3)]))
        self.assertNotEquals(SequenceValue(value=[IntegerValue(1), IntegerValue(3)]),
                             SequenceValue(value=[IntegerValue(3), IntegerValue(1)]))

        self.assertEquals(SequenceValue(value=[SequenceValue(value=[IntegerValue(1), IntegerValue(3)]),
                                               SequenceValue(value=[IntegerValue(4), IntegerValue(5)])]),
                          SequenceValue(value=[SequenceValue(value=[IntegerValue(1), IntegerValue(3)]),
                                               SequenceValue(value=[IntegerValue(4), IntegerValue(5)])]))
        self.assertNotEquals(SequenceValue(value=[SequenceValue(value=[IntegerValue(1), IntegerValue(3)]),
                                                  SequenceValue(value=[IntegerValue(4), IntegerValue(5)])]),
                             SequenceValue(value=[SequenceValue(value=[IntegerValue(3), IntegerValue(1)]),
                                                  SequenceValue(value=[IntegerValue(4), IntegerValue(5)])]))

    def test_set_equality(self):
        self.assertEquals(SetValue(value=set([])),
                          SetValue(value=set([])))
        self.assertEquals(SetValue(value=set([IntegerValue(1)])),
                          SetValue(value=set([IntegerValue(1)])))
        self.assertEquals(SetValue(value=set([IntegerValue(1), IntegerValue(3)])),
                          SetValue(value=set([IntegerValue(1), IntegerValue(3)])))
        self.assertEquals(SetValue(value=set([IntegerValue(1), IntegerValue(3)])),
                          SetValue(value=set([IntegerValue(3), IntegerValue(1)])))

    def test_tuple_equality(self):
        self.assertEquals(TupleValue(value=()),
                          TupleValue(value=()))
        self.assertEquals(TupleValue(value=(IntegerValue(1), FloatValue(1.0), StringValue('hello'))),
                          TupleValue(value=(IntegerValue(1), FloatValue(1.0), StringValue('hello'))))
        self.assertNotEquals(TupleValue(value=(IntegerValue(1), FloatValue(1.0), StringValue('hello'))),
                             TupleValue(value=(IntegerValue(1), FloatValue(1.1), StringValue('hello'))))
        self.assertEquals(TupleValue(value=(TupleValue(value=(IntegerValue(1), BooleanValue(True))),
                                            IntegerValue(1), FloatValue(1.0), StringValue('hello'))),
                          TupleValue(value=(TupleValue(value=(IntegerValue(1), BooleanValue(True))),
                                            IntegerValue(1), FloatValue(1.0), StringValue('hello'))))

    def test_mapping_equality(self):
        self.assertEquals(MappingValue(value={}),
                          MappingValue(value={}))
        self.assertNotEquals(MappingValue(value={}),
                             MappingValue(value={IntegerValue(1): StringValue('test')}))
        self.assertEquals(MappingValue(value={IntegerValue(1): StringValue('test')}),
                          MappingValue(value={IntegerValue(1): StringValue('test')}))
        self.assertEquals(MappingValue(value={IntegerValue(2): StringValue('moretest'),
                                              IntegerValue(1): StringValue('test')}),
                          MappingValue(value={IntegerValue(1): StringValue('test'),
                                              IntegerValue(2): StringValue('moretest')}))
        self.assertEquals(MappingValue(value={StringValue('hello'): MappingValue(value={IntegerValue(1): StringValue('test'),
                                                                                        IntegerValue(2): StringValue('moretest')}),
                                              StringValue('world'): MappingValue(value={})}),
                          MappingValue(value={StringValue('hello'): MappingValue(value={IntegerValue(1): StringValue('test'),
                                                                                        IntegerValue(2): StringValue('moretest')}),
                                              StringValue('world'): MappingValue(value={})}))

    def test_other_equality(self):
        self.assertEqual(VoidValue(), VoidValue())
        self.assertEqual(AnyValue(), AnyValue())
        self.assertNotEqual(VoidValue(), AnyValue())
        self.assertNotEqual(AnyValue(), VoidValue())

    def test_factory(self):
        self.assertEqual(DataValueFactory.create_instance(1), IntegerValue(1))
        self.assertEqual(DataValueFactory.create_instance(1.0), FloatValue(1.0))
        self.assertEqual(DataValueFactory.create_instance(True), BooleanValue(True))
        self.assertEqual(DataValueFactory.create_instance('Hello world!'), StringValue('Hello world!'))
        self.assertEqual(DataValueFactory.create_instance([1, 2, 3]),
                         SequenceValue(value=[IntegerValue(1), IntegerValue(2), IntegerValue(3)]))
        self.assertEqual(DataValueFactory.create_instance(set([1, 2, 3])),
                         SetValue(value=set([IntegerValue(1), IntegerValue(2), IntegerValue(3)])))
        self.assertEqual(DataValueFactory.create_instance((1, 2, 3)),
                         TupleValue(value=(IntegerValue(1), IntegerValue(2), IntegerValue(3))))
        self.assertEqual(DataValueFactory.create_instance([(1, 2, 3), (4, 5, 6)]),
                         SequenceValue(value=[TupleValue(value=(IntegerValue(1), IntegerValue(2), IntegerValue(3))),
                                              TupleValue(value=(IntegerValue(4), IntegerValue(5), IntegerValue(6)))]))
        self.assertEqual(DataValueFactory.create_instance({1: '1', 2: '2', 3: '3'}),
                         MappingValue(value={IntegerValue(1): StringValue('1'),
                                             IntegerValue(2): StringValue('2'),
                                             IntegerValue(3): StringValue('3')}))

    def test_typing(self):
        tests = [(IntegerValue(0), IntegerType()),
                 (FloatValue(0.0), FloatType()),
                 (BooleanValue(False), BooleanType()),
                 (StringValue("Hello world!"), StringType()),
                 (AnyValue(), AnyType()),
                 (VoidValue(), VoidType()),
                 (LocationValue('a.b.c'), LocationType()),
                 (DataValueFactory.create_instance([1, 2, 3]), SequenceType(basetype=IntegerType())),
                 (DataValueFactory.create_instance(set([1, 2, 3])), SetType(basetype=IntegerType())),
                 (DataValueFactory.create_instance((1, 2.0, "3")), TupleType(types=SequenceValue(value=[IntegerType(), FloatType(), StringType()]))),
                 (SequenceValue(value=[IntegerType(), FloatType(), StringType()]), SequenceType(basetype=TypeType())),
                 (DataValueFactory.create_instance([1, 2.0, "Hi!"]), SequenceType(basetype=UnionType(types=SequenceValue(value=[IntegerType(), FloatType(), StringType()])))),
                 (DataValueFactory.create_instance([[1, 2], [3, 4]]), SequenceType(basetype=SequenceType(basetype=IntegerType())))]

        for t in tests:
            self.assertEqual(t[0].typed_by(), t[1])
            self.assertTrue(t[1].is_type_of(t[0]))

        tests = [(IntegerValue(0), FloatType()),
                 (FloatValue(0.0), IntegerType()),
                 (BooleanValue(True), IntegerType()),
                 (StringValue('0'), IntegerType()),
                 (AnyValue(), IntegerType()),
                 (VoidValue(), IntegerType()),
                 (LocationValue('a.b.c'), IntegerType()),
                 (DataValueFactory.create_instance([1, 2, 3]), SequenceType(basetype=StringType())),
                 (DataValueFactory.create_instance(set([1, 2, 3])), SetType(basetype=FloatType())),
                 (DataValueFactory.create_instance((1, 2.0, "3")), TupleType(types=SequenceValue(value=[IntegerType(), FloatType(), IntegerType()]))),
                 (SequenceValue(value=[IntegerType(), FloatType(), StringType()]), SequenceType(basetype=StringType())),
                 (DataValueFactory.create_instance([1, 2.0, "Hi!"]), SequenceType(basetype=UnionType(types=SequenceValue(value=[IntegerType(), FloatType(), VoidType()])))),
                 (DataValueFactory.create_instance([[1, 2], [3, 4]]), SequenceType(basetype=SetType(basetype=IntegerType())))]

        for t in tests:
            assert logger.debug(t)
            self.assertNotEquals(t[0].typed_by(), t[1])
            self.assertFalse(t[1].is_type_of(t[0]))

    def test_enums(self):
        myEnum = TypeFactory.get_type('enum Animals{Cat, Dog}')
        self.assertEquals(myEnum.get_val(StringValue('Cat')), EnumValue(l_type=myEnum, value=1))
        self.assertEquals(myEnum.get_name(myEnum.get_val(StringValue('Dog'))), StringValue('Dog'))

    def test_infinity(self):
        minf = InfiniteValue('-')
        pinf = InfiniteValue('+')
        nan = InfiniteValue('nan')
        self.assertEqual(minf.typed_by(), InfiniteType())
        self.assertEqual(pinf.typed_by(), InfiniteType())
        cmp_values = [IntegerValue(0),
                      IntegerValue(1),
                      IntegerValue(-1),
                      FloatValue(0.0),
                      FloatValue(1.0),
                      FloatValue(-1.0),
                      IntegerValue(99999999),
                      IntegerValue(-99999999)]
        for v in cmp_values:
            self.assertGreater(pinf, v)
            self.assertLess(minf, v)
        self.assertEqual(minf * IntegerValue(-1), pinf)
        self.assertEqual(pinf * IntegerValue(-1), minf)
        self.assertEqual(str(pinf * IntegerValue(0)), 'nan')

if __name__ == "__main__":
    unittest.main()
