"""
Created on 28-dec.-2013

@author: Simon
"""
import math
from numbers import Number

from mvk.impl.python.datatype import VoidType, AnyType, BooleanType, \
    IntegerType, FloatType, StringType, TupleType, SequenceType, SetType, \
    MappingType, Type, TypeFactory, LocationType, UnionType, InfiniteType
from mvk.impl.python.element import Element
from mvk.impl.python.exception import MvKTypeError, MvKKeyError, MvKIndexError, \
    MvKValueError, MvKStopIteration
import mvk.interfaces.datavalue
from mvk.interfaces.exception import MvKZeroDivisionError
from mvk.util.logger import get_logger
from inspect import isclass

logger = get_logger('datavalue')

class DataValue(Element, mvk.interfaces.datavalue.DataValue):
    """ === CONSTRUCTOR === """
    def __init__(self, value=None, **kwds):
        self.value = value
        #TODO this does not belong here...
        super(DataValue, self).__init__(**kwds)

    """ === PUBLIC INTERFACE === """
    def __eq__(self, other):
        return BooleanValue(isinstance(other, mvk.interfaces.datavalue.DataValue))

    """ === PYTHON SPECIFIC === """
    def get_value(self):
        return self.value

    def __repr__(self):
        return str(self.value)


class VoidValue(DataValue, mvk.interfaces.datavalue.VoidValue):
    """ === PUBLIC INTERFACE === """
    def typed_by(self):
        return VoidType()

    def __eq__(self, other):
        return BooleanValue(isinstance(other.typed_by(), mvk.interfaces.datatype.VoidType))


class AnyValue(DataValue, mvk.interfaces.datavalue.AnyValue):
    """ === PUBLIC INTERFACE === """
    def typed_by(self):
        return AnyType()

    def __eq__(self, other):
        return BooleanValue(isinstance(other.typed_by(), mvk.interfaces.datatype.AnyType))


class HashableValue(DataValue, mvk.interfaces.datavalue.HashableValue):
    """
    Used to distinguish those values that can be used as
    values in SetValues, and as keys in MappingValues.
    """

    """ === PYTHON SPECIFIC === """
    def __hash__(self):
        return hash(self.value)


class NumericValue(HashableValue, mvk.interfaces.datavalue.NumericValue):
    """ === PUBLIC INTERFACE === """
    def __add__(self, other):
        if not (isinstance(other, mvk.interfaces.datavalue.NumericValue) and
                isinstance(other.typed_by(), mvk.interfaces.datatype.NumericType)):
            raise MvKTypeError(StringValue('Expected a NumericValue'))
        return self.__class__(value=self.value + other.get_value())

    def __sub__(self, other):
        if not (isinstance(other, mvk.interfaces.datavalue.NumericValue) and
                isinstance(other.typed_by(), mvk.interfaces.datatype.NumericType)):
            raise MvKTypeError(StringValue('Expected a NumericValue'))
        return self.__class__(value=self.value - other.get_value())

    def __mul__(self, other):
        if not (isinstance(other, mvk.interfaces.datavalue.NumericValue) and
                isinstance(other.typed_by(), mvk.interfaces.datatype.NumericType)):
            raise MvKTypeError(StringValue('Expected a NumericValue'))
        return self.__class__(value=self.value * other.get_value())

    def __div__(self, other):
        if not (isinstance(other, mvk.interfaces.datavalue.NumericValue) and
                isinstance(other.typed_by(), mvk.interfaces.datatype.NumericType)):
            raise MvKTypeError(StringValue('Expected a NumericValue'))
        try:
            return self.__class__(value=self.value / other.get_value())
        except ZeroDivisionError:
            raise MvKZeroDivisionError()

    def __mod__(self, other):
        if not (isinstance(other, mvk.interfaces.datavalue.NumericValue) and
                isinstance(other.typed_by(), mvk.interfaces.datatype.NumericType)):
            raise MvKTypeError(StringValue('Expected a NumericValue'))
        try:
            return self.__class__(value=self.value % other.get_value())
        except ZeroDivisionError:
            raise MvKZeroDivisionError()

    def __and__(self, other):
        if not (isinstance(other, mvk.interfaces.datavalue.NumericValue) and
                isinstance(other.typed_by(), mvk.interfaces.datatype.NumericType)):
            raise MvKTypeError(StringValue('Expected a NumericValue'))
        if self.value:
            return other
        else:
            return self

    def __or__(self, other):
        if not (isinstance(other, mvk.interfaces.datavalue.NumericValue) and
                isinstance(other.typed_by(), mvk.interfaces.datatype.NumericType)):
            raise MvKTypeError(StringValue('Expected a NumericValue'))
        if self.value:
            return self
        else:
            return other

    def __neg__(self):
        return self.__class__(value=-self.value)

    def __pos__(self):
        return self.__class__(value=+self.value)

    def __abs__(self):
        return self.__class__(value=abs(self.value))

    def __lt__(self, other):
        if not (isinstance(other, mvk.interfaces.datavalue.NumericValue) and
                isinstance(other.typed_by(), mvk.interfaces.datatype.NumericType)):
            raise MvKTypeError(StringValue('Expected a NumericValue, not %s' % type(other)))
        return BooleanValue(value=self.value < other.get_value())

    def __le__(self, other):
        if not (isinstance(other, mvk.interfaces.datavalue.NumericValue) and
                isinstance(other.typed_by(), mvk.interfaces.datatype.NumericType)):
            raise MvKTypeError(StringValue('Expected a NumericValue'))
        return BooleanValue(value=self.value <= other.get_value())

    def __gt__(self, other):
        if not (isinstance(other, mvk.interfaces.datavalue.NumericValue) and
                isinstance(other.typed_by(), mvk.interfaces.datatype.NumericType)):
            raise MvKTypeError(StringValue('Expected a NumericValue'))
        return BooleanValue(value=self.value > other.get_value())

    def __ge__(self, other):
        if not (isinstance(other, mvk.interfaces.datavalue.NumericValue) and
                isinstance(other.typed_by(), mvk.interfaces.datatype.NumericType)):
            raise MvKTypeError(StringValue('Expected a NumericValue'))
        return BooleanValue(value=self.value >= other.get_value())

    def __eq__(self, other):
        return BooleanValue(isinstance(other, NumericValue) and self.value == other.get_value())

    def floor(self):
        return FloatValue(value=math.floor(self.value))

    def ceil(self):
        return FloatValue(value=math.ceil(self.value))

    def trunc(self):
        return IntegerValue(value=int(self.value))

    def nonzero(self):
        return BooleanValue(self.value != 0)

    """ == PYTHON SPECIFIC == """
    def __nonzero__(self):
        return self.value != 0


class BooleanValue(NumericValue, mvk.interfaces.datavalue.BooleanValue):
    """ === CONSTRUCTOR === """
    def __init__(self, value):
        assert isinstance(value, Number)
        self.value = bool(value)

    """ === PUBLIC INTERFACE === """
    def typed_by(self):
        return BooleanType()

    def __nonzero__(self):
        return self.value

    def nonzero(self):
        return self

class IntegerValue(NumericValue, mvk.interfaces.datavalue.IntegerValue):
    """ === CONSTRUCTOR === """
    def __init__(self, value, **kwds):
        assert isinstance(value, Number)
        self.value = int(value)

    """ === PUBLIC INTERFACE === """
    def typed_by(self):
        return IntegerType()


class EnumValue(IntegerValue, mvk.interfaces.datavalue.EnumValue):
    ''' === CONSTRUCTOR === '''
    def __init__(self, l_type, value, **kwds):
        assert isinstance(l_type, mvk.interfaces.datatype.EnumType)
        assert isinstance(value, int)
        self.l_type = l_type
        super(EnumValue, self).__init__(value=value, **kwds)

    """ === PUBLIC INTERFACE === """
    def typed_by(self):
        return self.l_type


class FloatValue(NumericValue, mvk.interfaces.datavalue.FloatValue):
    """ === CONSTRUCTOR === """
    def __init__(self, value, **kwds):
        assert isinstance(value, Number)
        self.value = float(value)

    """ === PUBLIC INTERFACE === """
    def typed_by(self):
        return FloatType()


class InfiniteValue(FloatValue, mvk.interfaces.datavalue.InfiniteValue):
    """ === CONSTRUCTOR === """
    def __init__(self, value, **kwds):
        assert (value in ['-', '+', '-inf', '+inf', 'inf', 'nan'] or
                isinstance(value, float))
        if isinstance(value, str) and len(value) == 1:
            value = '%sinf' % value
        super(InfiniteValue, self).__init__(value=float(value),
                                         **kwds)

    """ === PUBLIC INTERFACE === """
    def typed_by(self):
        return InfiniteType()


class StringValue(HashableValue, mvk.interfaces.datavalue.StringValue):
    """ === CONSTRUCTOR === """
    def __init__(self, value, **kwds):
        assert isinstance(value, (str, unicode))
        self.value = value

    """ === PUBLIC INTERFACE === """
    def typed_by(self):
        return StringType()

    def count(self, a_str):
        if not (isinstance(a_str, mvk.interfaces.datavalue.StringValue) and
                isinstance(a_str.typed_by(), mvk.interfaces.datatype.StringType)):
            raise MvKTypeError(StringValue('Expected a StringValue'))
        return IntegerValue(self.value.count(a_str.get_value()))

    def find(self, a_str, start=None, end=None):
        if not (isinstance(a_str, mvk.interfaces.datavalue.StringValue) and
                isinstance(a_str.typed_by(), mvk.interfaces.datatype.StringType)):
            raise MvKTypeError(StringValue('Expected a StringValue'))
        if start is None and end is None:
            return IntegerValue(self.value.find(a_str.get_value()))
        elif end is None:
            end = self.len()
        elif start is None:
            start = IntegerValue(0)
        if not (isinstance(start, mvk.interfaces.datavalue.IntegerValue) and
                isinstance(start.typed_by(), mvk.interfaces.datatype.IntegerType)):
            raise MvKTypeError(StringValue('Expected start index to be an IntegerValue'))
        if not (isinstance(end, mvk.interfaces.datavalue.IntegerValue) and
                isinstance(end.typed_by(), mvk.interfaces.datatype.IntegerType)):
            raise MvKTypeError(StringValue('Expected end index to be an IntegerValue'))
        return IntegerValue(self.value.find(a_str.get_value(),
                                            start.get_value(),
                                            end.get_value()))

    def rfind(self, a_str, start=None, end=None):
        if not (isinstance(a_str, mvk.interfaces.datavalue.StringValue) and
                isinstance(a_str.typed_by(), mvk.interfaces.datatype.StringType)):
            raise MvKTypeError(StringValue('Expected a StringValue'))
        if start is None:
            start = IntegerValue(0)
        if end is None:
            end = self.len()
        if not (isinstance(start, mvk.interfaces.datavalue.IntegerValue) and
                isinstance(start.typed_by(), mvk.interfaces.datatype.IntegerType)):
            raise MvKTypeError(StringValue('Expected start index to be an IntegerValue'))
        if not (isinstance(end, mvk.interfaces.datavalue.IntegerValue) and
                isinstance(end.typed_by(), mvk.interfaces.datatype.IntegerType)):
            raise MvKTypeError(StringValue('Expected end index to be an IntegerValue'))
        return IntegerValue(self.value.rfind(a_str.get_value(),
                                             start.get_value(),
                                             end.get_value()))

    def replace(self, from_str, to_str, max_replacements=None):
        if not (isinstance(from_str, mvk.interfaces.datavalue.StringValue) and
                isinstance(from_str.typed_by(), mvk.interfaces.datatype.StringType)):
            raise MvKTypeError(StringValue('Expected a StringValue'))
        if not (isinstance(to_str, mvk.interfaces.datavalue.StringValue) and
                isinstance(to_str.typed_by(), mvk.interfaces.datatype.StringType)):
            raise MvKTypeError(StringValue('Expected a StringValue'))
        if max_replacements is None:
            return self.__class__(self.value.replace(from_str.get_value(),
                                                     to_str.get_value()))
        else:
            if not (isinstance(max_replacements, mvk.interfaces.datavalue.IntegerValue) and
                    isinstance(max_replacements.typed_by(), mvk.interfaces.datatype.IntegerType)):
                raise MvKTypeError(StringValue('Expected a IntegerValue'))
            return self.__class__(self.value.replace(from_str.get_value(),
                                                  to_str.get_value(),
                                                  max_replacements.get_value()))

    def strip(self, chars=None):
        if chars is None:
            return self.__class__(self.value.strip())
        else:
            if not (isinstance(chars, mvk.interfaces.datavalue.StringValue) and
                    isinstance(chars.typed_by(), mvk.interfaces.datatype.StringType)):
                raise MvKTypeError(StringValue('Expected a StringValue'))
            return self.__class__(self.value.strip(chars.get_value()))

    def rstrip(self, chars=None):
        if chars is None:
            return self.__class__(self.value.rstrip())
        else:
            if not (isinstance(chars, mvk.interfaces.datavalue.StringValue) and
                    isinstance(chars.typed_by(), mvk.interfaces.datatype.StringType)):
                raise MvKTypeError(StringValue('Expected a StringValue'))
            return self.__class__(self.value.rstrip(chars.get_value()))

    def lstrip(self, chars=None):
        if chars is None:
            return self.__class__(self.value.lstrip())
        else:
            if not (isinstance(chars, mvk.interfaces.datavalue.StringValue) and
                    isinstance(chars.typed_by(), mvk.interfaces.datatype.StringType)):
                raise MvKTypeError(StringValue('Expected a StringValue'))
            return self.__class__(self.value.lstrip(chars.get_value()))

    def split(self, sep=None, max_splits=None):
        if sep is not None:
            if not (isinstance(sep, mvk.interfaces.datavalue.StringValue) and
                    isinstance(sep.typed_by(), mvk.interfaces.datatype.StringType)):
                raise MvKTypeError(StringValue('Expected a StringValue'))
            sep = sep.get_value()
        if max_splits is not None:
            if not (isinstance(max_splits, mvk.interfaces.datavalue.IntegerValue) and
                    isinstance(max_splits.typed_by(), mvk.interfaces.datatype.IntegerType)):
                raise MvKTypeError(StringValue('Expected a IntegerValue'))
            max_splits = max_splits.get_value()
            return SequenceValue(value=[self.__class__(val) for val in self.value.split(sep, max_splits)])
        else:
            return SequenceValue(value=[self.__class__(val) for val in self.value.split(sep)])

    def rsplit(self, sep=None, max_splits=None):
        if sep is not None:
            if not (isinstance(sep, mvk.interfaces.datavalue.StringValue) and
                    isinstance(sep.typed_by(), mvk.interfaces.datatype.StringType)):
                raise MvKTypeError(StringValue('Expected a StringValue'))
            sep = sep.get_value()
        if max_splits is not None:
            if not (isinstance(max_splits, mvk.interfaces.datavalue.IntegerValue) and
                    isinstance(max_splits.typed_by(), mvk.interfaces.datatype.IntegerType)):
                raise MvKTypeError(StringValue('Expected a IntegerValue'))
            max_splits = max_splits.get_value()
            return SequenceValue(value=[self.__class__(val) for val in self.value.rsplit(sep, max_splits)])
        else:
            return SequenceValue(value=[self.__class__(val) for val in self.value.rsplit(sep)])

    def substring(self, start=None, stop=None):
        if start is None:
            start = IntegerValue(0)
        if stop is None:
            stop = self.len()
        if not (isinstance(start, mvk.interfaces.datavalue.IntegerValue) and
                isinstance(start.typed_by(), mvk.interfaces.datatype.IntegerType)):
            raise MvKTypeError(StringValue('Expected start to be an IntegerValue'))
        if not (isinstance(stop, mvk.interfaces.datavalue.IntegerValue) and
                isinstance(stop.typed_by(), mvk.interfaces.datatype.IntegerType)):
            raise MvKTypeError(StringValue('Expected stop to be an IntegerValue'))
        return self.__class__(self.value[start.get_value():stop.get_value()])

    def startswith(self, prefix, start=None, stop=None):
        if not (isinstance(prefix, mvk.interfaces.datavalue.StringValue) and
                isinstance(prefix.typed_by(), mvk.interfaces.datatype.StringType)):
            raise MvKTypeError(StringValue('Expected prefix to be an StringValue'))
        if start is None:
            start = IntegerValue(0)
        if stop is None:
            stop = self.len()
        if not (isinstance(start, mvk.interfaces.datavalue.IntegerValue) and
                isinstance(start.typed_by(), mvk.interfaces.datatype.IntegerType)):
            raise MvKTypeError(StringValue('Expected start to be an IntegerValue'))
        if not (isinstance(stop, mvk.interfaces.datavalue.IntegerValue) and
                isinstance(stop.typed_by(), mvk.interfaces.datatype.IntegerType)):
            raise MvKTypeError(StringValue('Expected stop to be an IntegerValue'))
        return BooleanValue(self.value.startswith(prefix.get_value(),
                                                  start.get_value(),
                                                  stop.get_value()))

    def lower(self):
        return self.__class__(self.value.lower())

    def upper(self):
        return self.__class__(self.value.upper())

    def swapcase(self):
        return self.__class__(self.value.swapcase())

    def title(self):
        return self.__class__(self.value.title())

    def capitalize(self):
        return self.__class__(self.value.capitalize())

    def len(self):
        return IntegerValue(len(self.value))

    def __add__(self, other):
        if not (isinstance(other, StringValue) and
                isinstance(other.typed_by(), mvk.interfaces.datatype.StringType)):
            raise MvKTypeError(StringValue('Expected a StringValue'))
        return self.__class__(self.value + other.get_value())

    def __eq__(self, other):
        try:
            return BooleanValue(self.value == other.value)
        except:
            return BooleanValue(False)


class LocationValue(StringValue, mvk.interfaces.datavalue.LocationValue):
    """ === PUBLIC INTERFACE === """
    def typed_by(self):
        return LocationType()

class CompositeValue(DataValue, mvk.interfaces.datavalue.CompositeValue):
    """ === PUBLIC INTERFACE === """
    def len(self):
        return IntegerValue(len(self.value))

    def __iter__(self):
        return Iterator(self)

    def __contains__(self, key):
        return BooleanValue(key in self.value)


class TupleValue(CompositeValue, HashableValue,
                 mvk.interfaces.datavalue.TupleValue):
    """ === CONSTRUCTOR === """
    def __init__(self, value=None, **kwds):
        if value is None:
            value = ()
        assert isinstance(value, tuple)
        """ tuple(value) is called to copy the tuple """
        super(TupleValue, self).__init__(value=tuple(value), **kwds)

    """ === PUBLIC INTERFACE === """
    def typed_by(self):
        return TupleType(types=SequenceValue(value=[el.typed_by() for el in self.value]))

    def __getitem__(self, index):
        if not (isinstance(index, IntegerValue) and
                isinstance(index.typed_by(), mvk.interfaces.datatype.IntegerType)):
            raise MvKTypeError(StringValue('Tuple indices must be IntegerValues, not %s'
                                           % type(index)))
        try:
            return self.value[index.get_value()]
        except IndexError:
            assert logger.debug('IndexError in TupleValue.__getitem__ %s %s'
                                % (self.len(), index))
            raise MvKIndexError(StringValue('%s' % index))

    def __eq__(self, other):
        if not (BooleanValue(isinstance(other.typed_by(), TupleType)) and
                self.len() == other.len()):
            return BooleanValue(False)
        for elem1, elem2 in zip(self, other):
            if not (elem1 == elem2):
                return BooleanValue(False)
        return BooleanValue(True)


def _get_type_from_set(typeset):
    if len(typeset) == 0:
        return AnyType()
    elif len(typeset) == 1:
        return typeset.pop()
    else:
        return UnionType(types=SequenceValue(value=list(typeset)))


class SequenceValue(CompositeValue, mvk.interfaces.datavalue.SequenceValue):
    """ === CONSTRUCTOR === """
    def __init__(self, value=None, **kwds):
        if value is None:
            value = []
        assert isinstance(value, list)
        """ list(value) is called to copy the list """
        super(SequenceValue, self).__init__(value=list(value),
                                            **kwds)

    """ === PUBLIC INTERFACE === """
    def typed_by(self):
        return SequenceType(basetype=_get_type_from_set(set([el.typed_by() for el in self.value])))

    def __getitem__(self, index):
        try:
            return self.value[index.get_value()]
        except IndexError:
            raise MvKIndexError(StringValue('SequenceValue index out of range'))
        except TypeError:
            if not (isinstance(index, mvk.interfaces.datavalue.IntegerValue) and
                    isinstance(index.typed_by(), mvk.interfaces.datatype.IntegerType)):
                raise MvKTypeError(StringValue('SequenceValue indices must be IntegerValues, not %s'
                               % type(index)))
            else:
                raise

    def __setitem__(self, index, item):
        try:
            self.value[index.get_value()] = item
        except IndexError:
            raise MvKIndexError(StringValue('SequenceValue assignment index out of range'))
        except TypeError:
            if not (isinstance(index, mvk.interfaces.datavalue.IntegerValue) and
                    isinstance(index.typed_by(), mvk.interfaces.datatype.IntegerType)):
                raise MvKTypeError(StringValue('SequenceValue indices must be IntegerValues, not %s'
                               % type(index)))
            else:
                raise

    def __delitem__(self, index):
        try:
            del self.value[index.get_value()]
        except IndexError:
            raise MvKIndexError(StringValue('SequenceValue index out of range'))
        except TypeError:
            if not (isinstance(index, mvk.interfaces.datavalue.IntegerValue) and
                    isinstance(index.typed_by(), mvk.interfaces.datatype.IntegerType)):
                raise MvKTypeError(StringValue('SequenceValue indices must be IntegerValues, not %s'
                               % type(index)))
            else:
                raise

    def append(self, x):
        """ TODO: type checking """
        self.value.append(x)

    def extend(self, x):
        try:
            self.value.extend(x)
        except:
            raise MvKTypeError(StringValue('%s is not iterable' % type(x)))

    def count(self, x):
        return IntegerValue(self.value.count(x))

    def index(self, value, start=None, stop=None):
        if not (start is None):
            if not (isinstance(start, mvk.interfaces.datavalue.IntegerValue) and
                    isinstance(start.typed_by(), mvk.interfaces.datatype.IntegerType)):
                raise MvKTypeError(StringValue('SequenceValue indices must be \
                                                IntegerValues, not %s' % type(start)))
            start = start.get_value()
        if not (stop is None):
            if not (isinstance(stop, mvk.interfaces.datavalue.IntegerValue) and
                    isinstance(stop.typed_by(), mvk.interfaces.datatype.IntegerType)):
                raise MvKTypeError(StringValue('SequenceValue indices must be \
                                                IntegerValues, not %s' % type(stop)))
            stop = stop.get_value()
        try:
            if not (start is None) and not (stop is None):
                return IntegerValue(self.value.index(value, start, stop))
            elif not (start is None):
                return IntegerValue(self.value.index(value, start))
            else:
                return IntegerValue(self.value.index(value))
        except ValueError:
            raise MvKValueError

    def insert(self, index, x):
        """ TODO: type checking """
        if not (isinstance(index, mvk.interfaces.datavalue.IntegerValue) and
                isinstance(index.typed_by(), mvk.interfaces.datatype.IntegerType)):
            raise MvKTypeError(StringValue('SequenceValue indices must be \
                                            IntegerValues, not %s' % type(index)))
        self.value.insert(index.get_value(), x)

    def pop(self):
        try:
            return self.value.pop()
        except IndexError:
            raise MvKIndexError(StringValue('Pop from an empty list'))

    def remove(self, x):
        try:
            self.value.remove(x)
        except ValueError:
            raise MvKValueError(StringValue('%s not in list' % x))

    def reverse(self):
        self.value.reverse()

    def sort(self):
        self.value.sort()

    def __add__(self, other):
        if not (isinstance(other, mvk.interfaces.datavalue.SequenceValue) and
                isinstance(other.typed_by(), mvk.interfaces.datatype.SequenceType)):
            raise MvKTypeError('Expected a SequenceValue')
        return_value = SequenceValue(value=self.get_value())
        for it in other:
            return_value.append(it)
        return return_value

    def __eq__(self, other):
        if not (isinstance(other, mvk.interfaces.datavalue.SequenceValue)):
            return BooleanValue(False)
        if not (BooleanValue(isinstance(other.typed_by(), SequenceType)) and
                self.len() == other.len()):
            assert logger.debug('Sequencevalue lengths not equal (%s != %s)!' %
                                (self.len(), other.len()))
            return BooleanValue(False)
        for it_self, it_other in zip(self, other):
            if not (it_self == it_other):
                return BooleanValue(False)
        return BooleanValue(True)


class SetValue(CompositeValue, mvk.interfaces.datavalue.SetValue):
    """ === CONSTRUCTOR === """
    def __init__(self, value, **kwds):
        assert isinstance(value, set)
        for v in value:
            assert (isinstance(v, mvk.interfaces.datavalue.HashableValue) and
                    isinstance(v.typed_by(), mvk.interfaces.datatype.HashableType))
        """ set(value) is called to copy the set """
        super(SetValue, self).__init__(value=set(value), **kwds)

    """ === PUBLIC INTERFACE === """
    def typed_by(self):
        return SetType(basetype=_get_type_from_set(set([el.typed_by() for el in self.value])))

    def __contains__(self, key):
        if not (isinstance(key, mvk.interfaces.datavalue.HashableValue) and
                isinstance(key.typed_by(), mvk.interfaces.datatype.HashableType)):
            raise MvKTypeError(StringValue('Unhashable type: %s'
                                           % type(key)))
        return BooleanValue(key in self.value)

    def add(self, element):
        """ TODO: type checking """
        if not (isinstance(element, mvk.interfaces.datavalue.HashableValue) and
                isinstance(element.typed_by(), mvk.interfaces.datatype.HashableType)):
            raise MvKTypeError(StringValue('Unhashable type: %s'
                                           % type(element)))
        self.value.add(element)

    def remove(self, element):
        if not (isinstance(element, mvk.interfaces.datavalue.HashableValue) and
                isinstance(element.typed_by(), mvk.interfaces.datatype.HashableType)):
            raise MvKTypeError(StringValue('Unhashable type: %s'
                                           % type(element)))
        try:
            self.value.remove(element)
        except KeyError:
            raise MvKKeyError(StringValue('%s' % element))

    def union(self, setvalue):
        if not (isinstance(setvalue, mvk.interfaces.datavalue.SetValue) and
                isinstance(setvalue.typed_by(), mvk.interfaces.datatype.SetType)):
            raise MvKTypeError(StringValue('Expected a SetValue, not a %s'
                                           % type(setvalue)))
        return SetValue(value=(self.value | setvalue.get_value()))

    def difference(self, setvalue):
        if not (isinstance(setvalue, mvk.interfaces.datavalue.SetValue) and
                isinstance(setvalue.typed_by(), mvk.interfaces.datatype.SetType)):
            raise MvKTypeError(StringValue('Expected a SetValue, not a %s'
                                           % type(setvalue)))
        return SetValue(value=(self.value - setvalue.get_value()))

    def symmetric_difference(self, setvalue):
        if not (isinstance(setvalue, mvk.interfaces.datavalue.SetValue) and
                isinstance(setvalue.typed_by(), mvk.interfaces.datatype.SetType)):
            raise MvKTypeError(StringValue('Expected a SetValue, not a %s'
                                           % type(setvalue)))
        return SetValue(value=(self.value ^ setvalue.get_value()))

    def intersection(self, setvalue):
        if not (isinstance(setvalue, mvk.interfaces.datavalue.SetValue) and
                isinstance(setvalue.typed_by(), mvk.interfaces.datatype.SetType)):
            raise MvKTypeError(StringValue('Expected a SetValue, not a %s'
                                           % type(setvalue)))
        return SetValue(value=(self.value & setvalue.get_value()))

    def issubset(self, setvalue):
        if not (isinstance(setvalue, mvk.interfaces.datavalue.SetValue) and
                isinstance(setvalue.typed_by(), mvk.interfaces.datatype.SetType)):
            raise MvKTypeError(StringValue('Expected a SetValue, not a %s'
                                           % type(setvalue)))
        return BooleanValue(self.value <= setvalue.get_value())

    def issuperset(self, setvalue):
        if not (isinstance(setvalue, mvk.interfaces.datavalue.SetValue) and
                isinstance(setvalue.typed_by(), mvk.interfaces.datatype.SetType)):
            raise MvKTypeError(StringValue('Expected a SetValue, not a %s'
                                           % type(setvalue)))
        return BooleanValue(self.value >= setvalue.get_value())

    def __eq__(self, other):
        if not (BooleanValue(isinstance(other.typed_by(), SetType)) and
                self.len() == other.len()):
            return BooleanValue(False)
        for it in self:
            if it not in other:
                return BooleanValue(False)
        return BooleanValue(True)


class MappingValue(CompositeValue, mvk.interfaces.datavalue.MappingValue):
    """ === CONSTRUCTOR === """
    def __init__(self, value=None, **kwds):
        if value is None:
            value = {}
        assert isinstance(value, dict)
        """ dict(value) is called to copy the dict """
        super(MappingValue, self).__init__(value=dict(value), **kwds)

    """ === PUBLIC INTERFACE === """
    def typed_by(self):
        return MappingType(keytype=_get_type_from_set(set([el.typed_by() for el in self.value.keys()])),
                           valuetype=_get_type_from_set(set([el.typed_by() for el in self.value.values()])))

    def __contains__(self, key):
        if not (isinstance(key, HashableValue) and
                isinstance(key.typed_by(), mvk.interfaces.datatype.HashableType)):
            raise MvKTypeError(StringValue('Unhashable type: %s' % type(key)))
        return BooleanValue(key in self.value)

    def __iter__(self):
        return Iterator(self.keys())

    def keys(self):
        return SetValue(value=set(self.value.keys()))

    def values(self):
        return SequenceValue(value=list(self.value.values()))

    def __getitem__(self, key):
        try:
            return self.value[key]
        except KeyError:
            if not (isinstance(key, HashableValue) and
                    isinstance(key.typed_by(), mvk.interfaces.datatype.HashableType)):
                raise MvKTypeError(StringValue('Unhashable type: %s' % type(key)))
            raise MvKKeyError(StringValue('%s' % key))

    def __setitem__(self, key, val):
        """ TODO: type checking """
        if not (isinstance(key, HashableValue) and
                isinstance(key.typed_by(), mvk.interfaces.datatype.HashableType)):
            raise MvKTypeError(StringValue('Unhashable type: %s' % type(key)))
        self.value[key] = val

    def __delitem__(self, key):
        try:
            del self.value[key]
        except KeyError:
            if not (isinstance(key, HashableValue) and
                    isinstance(key.typed_by(), mvk.interfaces.datatype.HashableType)):
                raise MvKTypeError(StringValue('Unhashable type: %s' % type(key)))
            raise MvKKeyError(StringValue('%s' % key))

    def clear(self):
        self.value.clear()

    def pop(self, key, default=None):
        if not (isinstance(key, HashableValue) and
                isinstance(key.typed_by(), mvk.interfaces.datatype.HashableType)):
            raise MvKTypeError(StringValue('Unhashable type: %s' % type(key)))
        try:
            if default is None:
                return self.value.pop(key)
            else:
                return self.value.pop(key, default)
        except KeyError:
            raise MvKKeyError(StringValue('%s' % key))

    def __eq__(self, other):
        if not (BooleanValue(isinstance(other.typed_by(), MappingType)) and
                self.len() == other.len()):
            assert logger.debug('Lengths of MappingValues not equal (%s != %s)' %
                                (self.len(), other.len()))
            return BooleanValue(False)
        assert logger.debug('In MappingValue.__eq__()')
        for next in self:
            if not next in other:
                assert logger.debug('%s not found in other' % next)
                return BooleanValue(False)
            if not self[next] == other[next]:
                assert logger.debug('values with key %s differ' % next)
                return BooleanValue(False)
        return BooleanValue(True)


class Iterator(Element, mvk.interfaces.datavalue.Iterator):
    """ === CONSTRUCTOR === """
    def __init__(self, iterable):
        assert isinstance(iterable, SequenceValue) \
                or isinstance(iterable, TupleValue) \
                or isinstance(iterable, SetValue)
        self.original_iterable = iterable
        self.iterable = list(iterable.get_value())
        self.i = 0

    """ === PUBLIC INTERFACE === """
    def has_next(self):
        return self.i < len(self.iterable)

    def next(self):
        ret_value = None
        if self.has_next():
            ret_value = self.iterable[self.i]
            self.i = self.i + 1
        else:
            raise MvKStopIteration()
        return ret_value

    def __eq__(self, other):
        return BooleanValue(isinstance(other, Iterator) and
                id(self.original_iterable) == id(other.original_iterable))


class ImmutableCompositeValue(CompositeValue,
                              mvk.interfaces.datavalue.ImmutableCompositeValue):
    pass


class ImmutableSequenceValue(SequenceValue, ImmutableCompositeValue,
                             mvk.interfaces.datavalue.ImmutableSequenceValue):
    ''' Decorator for SequenceValue which does not allow editing. '''
    ''' == CONSTRUCTOR == '''
    def __init__(self, seq_val):
        assert isinstance(seq_val, mvk.interfaces.datavalue.SequenceValue)
        self.val = seq_val

    ''' == PUBLIC INTERFACE == '''
    def typed_by(self):
        return self.val.typed_by()

    def __getitem__(self, index):
        return self.val[index]

    def __setitem__(self, index, item):
        raise MvKTypeError(StringValue('ImmutableSequenceValue does not \
                                        support index assignment.'))

    def __delitem__(self, index):
        raise MvKTypeError(StringValue('ImmutableSequenceValue does not \
                                        support item deletion.'))

    def append(self, x):
        raise MvKTypeError(StringValue('ImmutableSequenceValue does not \
                                        support appending an item.'))

    def extend(self, x):
        raise MvKTypeError(StringValue('ImmutableSequenceValue does not \
                                        support extending.'))

    def count(self, x):
        return self.val.count(x)

    def index(self, value, start=None, stop=None):
        return self.val.index(value, start, stop)

    def insert(self, index, x):
        raise MvKTypeError(StringValue('ImmutableSequenceValue does not \
                                        support inserting an item.'))

    def pop(self):
        raise MvKTypeError(StringValue('ImmutableSequenceValue does not \
                                        support item deletion.'))

    def remove(self, x):
        raise MvKTypeError(StringValue('ImmutableSequenceValue does not \
                                        support item deletion.'))

    def reverse(self):
        raise MvKTypeError(StringValue('ImmutableSequenceValue does not \
                                        support reversing.'))

    def sort(self):
        raise MvKTypeError(StringValue('ImmutableSequenceValue does not \
                                        support in-place sorting.'))

    def __add__(self, other):
        return ImmutableSequenceValue(self.val + other)

    def len(self):
        return self.val.len()

    def __contains__(self, key):
        return key in self.val

    def __eq__(self, other):
        return self.val == other

    ''' == PYTHON SPECIFIC '''
    def get_value(self):
        return self.val.get_value()

    def __repr__(self):
        return repr(self.val)


class ImmutableSetValue(SetValue, ImmutableCompositeValue,
                        mvk.interfaces.datavalue.ImmutableSetValue):
    ''' Decorator for SetValue which does not allow editing. '''
    ''' == CONSTRUCTOR == '''
    def __init__(self, seq_val):
        assert (isinstance(seq_val, mvk.interfaces.datavalue.SetValue) and
                isinstance(seq_val.typed_by(), mvk.interfaces.datatype.SetType))
        self.val = seq_val

    ''' == PUBLIC INTERFACE == '''
    def typed_by(self):
        return self.val.typed_by()

    def __contains__(self, key):
        return key in self.val

    def add(self, element):
        raise MvKTypeError(StringValue('ImmutableSetValue does not support \
                                        item addition.'))

    def remove(self, element):
        raise MvKTypeError(StringValue('ImmutableSetValue does not support \
                                        item deletion.'))

    def union(self, setvalue):
        return ImmutableSetValue(self.val.union(setvalue))

    def difference(self, setvalue):
        return ImmutableSetValue(self.val.difference(setvalue))

    def symmetric_difference(self, setvalue):
        return ImmutableSetValue(self.val.symmetric_difference(setvalue))

    def intersection(self, setvalue):
        return ImmutableSetValue(self.val.intersection(setvalue))

    def issubset(self, setvalue):
        return self.val.issubset(setvalue)

    def issuperset(self, setvalue):
        return self.val.issuperset(setvalue)

    def len(self):
        return self.val.len()

    def __eq__(self, other):
        return self.val == other

    ''' == PYTHON SPECIFIC '''
    def get_value(self):
        return self.val.get_value()

    def __repr__(self):
        return repr(self.val)


class ImmutableMappingValue(MappingValue, ImmutableCompositeValue,
                            mvk.interfaces.datavalue.ImmutableMappingValue):
    ''' Decorator for MappingValue which does not allow editing. '''
    ''' == CONSTRUCTOR == '''
    def __init__(self, m_val):
        assert isinstance(m_val, mvk.interfaces.datavalue.MappingValue)
        self.val = m_val

    ''' == PUBLIC INTERFACE == '''
    def typed_by(self):
        return self.val.typed_by()

    def __contains__(self, key):
        return key in self.val

    def __iter__(self):
        return self.val.__iter__()

    def keys(self):
        return self.val.keys()

    def values(self):
        return self.val.values()

    def __getitem__(self, key):
        return self.val[key]

    def __setitem__(self, key, val):
        raise MvKTypeError(StringValue('ImmutableMappingValue does not support \
                                        key assignment.'))

    def __delitem__(self, key):
        raise MvKTypeError(StringValue('ImmutableMappingValue does not support \
                                        key deletion.'))

    def clear(self):
        raise MvKTypeError(StringValue('ImmutableMappingValue does not support \
                                        key deletion.'))

    def pop(self, key, default=None):
        raise MvKTypeError(StringValue('ImmutableMappingValue does not support \
                                        key deletion.'))

    def len(self):
        return self.val.len()

    def __eq__(self, other):
        return self.val == other

    ''' == PYTHON SPECIFIC '''
    def get_value(self):
        return self.val.get_value()

    def __repr__(self):
        return repr(self.val)


class DataValueFactory(object):
    @classmethod
    def create_instance(cls, data, datacls=None, immutable=False):
        if isinstance(data, mvk.interfaces.element.Element):
            return data
        datacls_to_data = {StringValue: str,
                           LocationValue: str,
                           IntegerValue: int,
                           FloatValue: float,
                           BooleanValue: lambda x: x == 'True' if isinstance(x, str) else bool(x)}
        if datacls is not None:
            if not isclass(datacls) or not issubclass(datacls, mvk.interfaces.datavalue.DataValue):
                from mvk.impl.python.changelog import MvKCreateCompositeLog, MvKCompositeLog, MvKDeleteLog, MvKCreateLog, MvKUpdateLog, MvKReadLog, MvKCRUDLog, MvKOperationLog, MvKLog, MvKDeleteCompositeLog
                datacls = eval(datacls)
            if datacls != AnyValue:
                if datacls in datacls_to_data:
                    data = datacls_to_data[datacls](data)
                return datacls(value=data)
            else:
                return AnyValue()
        datatype = type(data)
        if datatype is int:
            return IntegerValue(data)
        if datatype is float:
            return FloatValue(data)
        elif datatype is str:
            return StringValue(data)
        elif datatype is bool:
            return BooleanValue(data)
        elif datatype is set:
            s = SetValue(value=set([cls.create_instance(d) for d in data]))
            return ImmutableSetValue(s) if immutable else s
        elif datatype is tuple:
            return TupleValue(value=tuple([cls.create_instance(d) for d in data]))
        elif datatype is list:
            s = SequenceValue(value=list([cls.create_instance(d) for d in data]))
            return ImmutableSequenceValue(s) if immutable else s
        elif datatype is dict:
            m = MappingValue(value=dict(zip([cls.create_instance(k) for k in data.keys()],
                                            [cls.create_instance(v) for v in data.values()])))
            return ImmutableMappingValue(m) if immutable else m
        else:
            raise TypeError("Don't know what the resulting datavalue will be \
                            (implementation error): %s (from %s)"
                            % (datatype.__name__, data))

    @classmethod
    def create_instance_from_type(cls, type_name, data):
        assert isinstance(type_name, str)

        ''' TODO: Implement this, if it's useful. '''
        return TypeFactory.get_type(type_name).create_instance(data)

    @classmethod
    def get_datatype_string(cls, data):
        def get_datatype_from_set(datatype_set):
            if len(datatype_set) == 0:
                return 'AnyType'
            elif len(datatype_set) == 1:
                return datatype_set.pop()
            else:
                return 'UnionType(%s)' % ', '.join(datatype_set)

        datatype = type(data)
        if datatype is int:
            return 'IntegerType'
        if datatype is float:
            return 'FloatType'
        elif datatype is str:
            return 'StringType'
        elif datatype is bool:
            return 'BooleanType'
        elif datatype is set:
            types = set()
            for el in data:
                types.add(cls.get_datatype_string(el))
            return 'SetType[%s]' % get_datatype_from_set(types)
        elif datatype is list:
            types = set()
            for el in data:
                types.add(cls.get_datatype_string(el))
            return 'SequenceType[%s]' % get_datatype_from_set(types)
        elif datatype is tuple:
            return 'TupleType(%s)' % ', '.join([cls.get_datatype_string(v) for v in data])
        elif datatype is dict:
            keytypes = set()
            valuetypes = set()
            for k, v in data.iteritems():
                keytypes.add(cls.get_datatype_string(k))
                valuetypes.add(cls.get_datatype_string(v))
            return 'MappingType(%s: %s)' % (get_datatype_from_set(keytypes),
                                            get_datatype_from_set(valuetypes))

    @classmethod
    def get_datatype(cls, data):
        return TypeFactory.get_type(cls.get_datatype_string(data))
