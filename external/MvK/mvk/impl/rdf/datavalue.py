"""
Created on 28-dec.-2013

@author: Simon
"""
import math
from numbers import Number

from rdflib.graph import Graph
from rdflib.term import BNode, Literal

from mvk.impl.python.datatype import VoidType, AnyType, BooleanType, \
    IntegerType, FloatType, StringType, TupleType, SequenceType, SetType, \
    MappingType, Type, TypeFactory, LocationType, UnionType
import mvk.impl.python.datavalue
from mvk.impl.python.element import Element
from mvk.impl.python.exception import MvKTypeError, MvKKeyError, MvKIndexError, \
    MvKValueError, MvKStopIteration
from mvk.impl.rdf import rdf_graph
import mvk.interfaces.datavalue
from mvk.interfaces.exception import MvKZeroDivisionError
from mvk.util.logger import get_logger


logger = get_logger('datavalue')


class SimpleDataValue(Element, mvk.interfaces.datavalue.DataValue):
    """ === CONSTRUCTOR === """
    def __init__(self, graph, node_id, **kwds):
        assert logger.debug('Constructing DataValue with id %s' % str(node_id))
        self.graph = graph
        self.node_id = node_id
        super(SimpleDataValue, self).__init__(**kwds)

    """ === PUBLIC INTERFACE === """
    def __eq__(self, other):
        return ((super(SimpleDataValue, self).__eq__(other)) and
                (DataValueFactory.create_instance(data=isinstance(other, mvk.interfaces.datavalue.DataValue),
                                                  datacls=BooleanValue)))

    """ === RDF SPECIFIC === """
    def get_value(self):
        return list(self.graph.triples((self.node_id, Literal('val'), None)))[0][2].toPython()

    def __repr__(self):
        return repr(self.get_value())

    def get_node_id(self):
        return self.node_id


class VoidValue(SimpleDataValue, mvk.interfaces.datavalue.VoidValue):
    """ === CONSTRUCTOR === """
    def __init__(self):
        assert logger.debug('Constructing VoidValue')
        super(VoidValue, self).__init__()

    """ === PUBLIC INTERFACE === """
    def typed_by(self):
        return VoidType()

    def __eq__(self, other):
        return ((super(VoidValue, self).__eq__(other)) and
                (DataValueFactory.create_instance(data=isinstance(other.typed_by(), mvk.interfaces.datatype.VoidType), datacls=BooleanValue)))


class AnyValue(SimpleDataValue, mvk.interfaces.datavalue.AnyValue):
    """ === CONSTRUCTOR === """
    def __init__(self):
        assert logger.debug('Constructing AnyValue')
        super(AnyValue, self).__init__()

    """ === PUBLIC INTERFACE === """
    def typed_by(self):
        return AnyType()

    def __eq__(self, other):
        return ((super(AnyValue, self).__eq__(other)) and
                (BooleanValue(isinstance(other.typed_by(), mvk.interfaces.datatype.AnyType))))


class HashableValue(Element, mvk.interfaces.datavalue.HashableValue):
    """
    Used to distinguish those values that can be used as
    values in SetValues, and as keys in MappingValues.
    """

    """ === PYTHON SPECIFIC === """
    def __hash__(self):
        return hash(self.get_value())


class NumericValue(SimpleDataValue, HashableValue, mvk.interfaces.datavalue.NumericValue):
    """ === PUBLIC INTERFACE === """
    def __add__(self, other):
        if not (isinstance(other, mvk.interfaces.datavalue.NumericValue) and
                isinstance(other.typed_by(), mvk.interfaces.datatype.NumericType)):
            raise MvKTypeError(StringValue('Expected a NumericValue'))
        return DataValueFactory.create_instance(data=self.get_value() + other.get_value(), datacls=self.__class__)

    def __sub__(self, other):
        if not (isinstance(other, mvk.interfaces.datavalue.NumericValue) and
                isinstance(other.typed_by(), mvk.interfaces.datatype.NumericType)):
            raise MvKTypeError(StringValue('Expected a NumericValue'))
        return DataValueFactory.create_instance(data=self.get_value() - other.get_value(), datacls=self.__class__)

    def __mul__(self, other):
        if not (isinstance(other, mvk.interfaces.datavalue.NumericValue) and
                isinstance(other.typed_by(), mvk.interfaces.datatype.NumericType)):
            raise MvKTypeError(StringValue('Expected a NumericValue'))
        return DataValueFactory.create_instance(data=self.get_value() * other.get_value(), datacls=self.__class__)

    def __div__(self, other):
        if not (isinstance(other, mvk.interfaces.datavalue.NumericValue) and
                isinstance(other.typed_by(), mvk.interfaces.datatype.NumericType)):
            raise MvKTypeError(StringValue('Expected a NumericValue'))
        try:
            return DataValueFactory.create_instance(data=self.get_value() / other.get_value(), datacls=self.__class__)
        except ZeroDivisionError:
            raise MvKZeroDivisionError()

    def __mod__(self, other):
        if not (isinstance(other, mvk.interfaces.datavalue.NumericValue) and
                isinstance(other.typed_by(), mvk.interfaces.datatype.NumericType)):
            raise MvKTypeError(StringValue('Expected a NumericValue'))
        try:
            return DataValueFactory.create_instance(data=self.get_value() % other.get_value(), datacls=self.__class__)
        except ZeroDivisionError:
            raise MvKZeroDivisionError()

    def __and__(self, other):
        if not (isinstance(other, mvk.interfaces.datavalue.NumericValue) and
                isinstance(other.typed_by(), mvk.interfaces.datatype.NumericType)):
            raise MvKTypeError(StringValue('Expected a NumericValue'))
        if self.get_value():
            return other
        else:
            return self

    def __or__(self, other):
        if not (isinstance(other, mvk.interfaces.datavalue.NumericValue) and
                isinstance(other.typed_by(), mvk.interfaces.datatype.NumericType)):
            raise MvKTypeError(StringValue('Expected a NumericValue'))
        if self.get_value():
            return self
        else:
            return other

    def __neg__(self):
        return DataValueFactory.create_instance(data=-self.get_value(), datacls=self.__class__)

    def __pos__(self):
        return DataValueFactory.create_instance(data=+self.get_value(), datacls=self.__class__)

    def __abs__(self):
        return DataValueFactory.create_instance(data=abs(self.get_value()), datacls=self.__class__)

    def __lt__(self, other):
        if not (isinstance(other, mvk.interfaces.datavalue.NumericValue) and
                isinstance(other.typed_by(), mvk.interfaces.datatype.NumericType)):
            raise MvKTypeError(StringValue('Expected a NumericValue'))
        return DataValueFactory.create_instance(data=self.get_value() < other.get_value())

    def __le__(self, other):
        if not (isinstance(other, mvk.interfaces.datavalue.NumericValue) and
                isinstance(other.typed_by(), mvk.interfaces.datatype.NumericType)):
            raise MvKTypeError(StringValue('Expected a NumericValue'))
        return DataValueFactory.create_instance(data=self.get_value() <= other.get_value())

    def __gt__(self, other):
        if not (isinstance(other, mvk.interfaces.datavalue.NumericValue) and
                isinstance(other.typed_by(), mvk.interfaces.datatype.NumericType)):
            raise MvKTypeError(StringValue('Expected a NumericValue'))
        return DataValueFactory.create_instance(data=self.get_value() > other.get_value())

    def __ge__(self, other):
        if not (isinstance(other, mvk.interfaces.datavalue.NumericValue) and
                isinstance(other.typed_by(), mvk.interfaces.datatype.NumericType)):
            raise MvKTypeError(StringValue('Expected a NumericValue'))
        return DataValueFactory.create_instance(data=self.get_value() >= other.get_value())

    def __eq__(self, other):
        return ((super(NumericValue, self).__eq__(other)) and
                (DataValueFactory.create_instance(data=self.get_value() == other.get_value(), datacls=BooleanValue)))

    def floor(self):
        return DataValueFactory.create_instance(data=math.floor(self.get_value()), datacls=FloatValue)

    def ceil(self):
        return DataValueFactory.create_instance(data=math.ceil(self.get_value()), datacls=FloatValue)

    def trunc(self):
        return DataValueFactory.create_instance(data=int(self.get_value()), datacls=IntegerValue)

    def nonzero(self):
        return DataValueFactory.create_instance(data=self.get_value() != 0, datacls=BooleanValue)

    """ == PYTHON SPECIFIC == """
    def __nonzero__(self):
        return self.get_value() != 0


class BooleanValue(NumericValue, mvk.interfaces.datavalue.BooleanValue):
    """ === CONSTRUCTOR === """
    def __init__(self, graph, node_id, **kwds):
        assert logger.debug('Constructing BooleanValue')
        super(BooleanValue, self).__init__(graph=graph,
                                           node_id=node_id,
                                           **kwds)

    """ === PUBLIC INTERFACE === """
    def typed_by(self):
        return BooleanType()

    def get_value(self):
        return bool(super(BooleanValue, self).get_value())


class IntegerValue(NumericValue, mvk.interfaces.datavalue.IntegerValue):
    """ === CONSTRUCTOR === """
    def __init__(self, graph, node_id, **kwds):
        assert logger.debug('Constructing IntegerValue')
        super(IntegerValue, self).__init__(graph=graph,
                                           node_id=node_id,
                                           **kwds)

    """ === PUBLIC INTERFACE === """
    def typed_by(self):
        return IntegerType()

    def get_value(self):
        return int(super(IntegerValue, self).get_value())


class FloatValue(NumericValue, mvk.interfaces.datavalue.FloatValue):
    """ === CONSTRUCTOR === """
    def __init__(self, graph, node_id, **kwds):
        assert logger.debug('Constructing FloatValue')
        super(FloatValue, self).__init__(graph=graph,
                                         node_id=node_id,
                                         **kwds)

    """ === PUBLIC INTERFACE === """
    def typed_by(self):
        return FloatType()

    def get_value(self):
        return float(super(FloatValue, self).get_value())


class StringValue(SimpleDataValue, HashableValue, mvk.interfaces.datavalue.StringValue):
    """ === CONSTRUCTOR === """
    def __init__(self, graph, node_id, **kwds):
        assert logger.debug('Constructing StringValue')
        super(StringValue, self).__init__(graph=graph,
                                          node_id=node_id,
                                          **kwds)

    """ === PUBLIC INTERFACE === """
    def typed_by(self):
        return StringType()

    def count(self, a_str):
        if not (isinstance(a_str, mvk.interfaces.datavalue.StringValue) and
                isinstance(a_str.typed_by(), mvk.interfaces.datatype.StringType)):
            raise MvKTypeError(StringValue('Expected a StringValue'))
        return DataValueFactory.create_instance(data=self.get_value().count(a_str.get_value()))

    def find(self, a_str):
        if not (isinstance(a_str, mvk.interfaces.datavalue.StringValue) and
                isinstance(a_str.typed_by(), mvk.interfaces.datatype.StringType)):
            raise MvKTypeError(StringValue('Expected a StringValue'))
        return DataValueFactory.create_instance(data=self.get_value().find(a_str.get_value()))

    def rfind(self, a_str):
        if not (isinstance(a_str, mvk.interfaces.datavalue.StringValue) and
                isinstance(a_str.typed_by(), mvk.interfaces.datatype.StringType)):
            raise MvKTypeError(StringValue('Expected a StringValue'))
        return DataValueFactory.create_instance(data=self.get_value().rfind(a_str.get_value()))

    def replace(self, from_str, to_str, max_replacements=None):
        if not (isinstance(from_str, mvk.interfaces.datavalue.StringValue) and
                isinstance(from_str.typed_by(), mvk.interfaces.datatype.StringType)):
            raise MvKTypeError(StringValue('Expected a StringValue'))
        if not (isinstance(to_str, mvk.interfaces.datavalue.StringValue) and
                isinstance(to_str.typed_by(), mvk.interfaces.datatype.StringType)):
            raise MvKTypeError(StringValue('Expected a StringValue'))
        if max_replacements is None:
            return DataValueFactory.create_instance(data=self.get_value().replace(from_str.get_value(),
                                                                                  to_str.get_value()))
        else:
            if not (isinstance(max_replacements, mvk.interfaces.datavalue.IntegerValue) and
                    isinstance(max_replacements.typed_by(), mvk.interfaces.datatype.IntegerType)):
                raise MvKTypeError(StringValue('Expected a IntegerValue'))
            return DataValueFactory.create_instance(data=self.get_value().replace(from_str.get_value(),
                                                                                  to_str.get_value(),
                                                                                  max_replacements.get_value()))

    def strip(self, chars=None):
        if chars is None:
            return self.__class__(self.get_value().strip())
        else:
            if not (isinstance(chars, mvk.interfaces.datavalue.StringValue) and
                    isinstance(chars.typed_by(), mvk.interfaces.datatype.StringType)):
                raise MvKTypeError(StringValue('Expected a StringValue'))
            return DataValueFactory.create_instance(data=self.get_value().strip(chars.get_value()))

    def rstrip(self, chars=None):
        if chars is None:
            return self.__class__(self.get_value().rstrip())
        else:
            if not (isinstance(chars, mvk.interfaces.datavalue.StringValue) and
                    isinstance(chars.typed_by(), mvk.interfaces.datatype.StringType)):
                raise MvKTypeError(StringValue('Expected a StringValue'))
            return DataValueFactory.create_instance(data=self.get_value().rstrip(chars.get_value()))

    def lstrip(self, chars=None):
        if chars is None:
            return self.__class__(self.get_value().lstrip())
        else:
            if not (isinstance(chars, mvk.interfaces.datavalue.StringValue) and
                    isinstance(chars.typed_by(), mvk.interfaces.datatype.StringType)):
                raise MvKTypeError(StringValue('Expected a StringValue'))
            return DataValueFactory.create_instance(data=self.get_value().lstrip(chars.get_value()))

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
            return DataValueFactory.create_instance(data=[self.__class__(val) for val in self.get_value().split(sep, max_splits)])
        else:
            return DataValueFactory.create_instance(data=[self.__class__(val) for val in self.get_value().split(sep)])

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
            return DataValueFactory.create_instance(data=[self.__class__(val) for val in self.get_value().rsplit(sep, max_splits)])
        else:
            return DataValueFactory.create_instance(data=[self.__class__(val) for val in self.get_value().rsplit(sep)])

    def lower(self):
        return self.__class__(self.get_value().lower())

    def upper(self):
        return self.__class__(self.get_value().upper())

    def swapcase(self):
        return self.__class__(self.get_value().swapcase())

    def title(self):
        return self.__class__(self.get_value().title())

    def capitalize(self):
        return self.__class__(self.get_value().capitalize())

    def len(self):
        return IntegerValue(len(self.get_value()))

    def __add__(self, other):
        if not (isinstance(other, StringValue) and
                isinstance(other.typed_by(), mvk.interfaces.datatype.StringType)):
            raise MvKTypeError(StringValue('Expected a StringValue'))
        return DataValueFactory.create_instance(data=self.get_value() + other.get_value())

    def __eq__(self, other):
        return ((super(StringValue, self).__eq__(other)) and
                (DataValueFactory.create_instance(data=isinstance(other.typed_by(), StringType),
                                                  datacls=BooleanValue)) and
                (DataValueFactory.create_instance(data=self.get_value() == other.get_value(),
                                                  datacls=BooleanValue)))

    def get_value(self):
        return str(super(StringValue, self).get_value())


class LocationValue(StringValue, mvk.interfaces.datavalue.LocationValue):
    """ === PUBLIC INTERFACE === """
    def typed_by(self):
        return LocationType()

    def __eq__(self, other):
        return ((super(LocationValue, self).__eq__(other)) and
                (BooleanValue(isinstance(other.typed_by(), StringType))) and
                (BooleanValue(self.get_value() == other.get_value())))


class CompositeValue(Element, mvk.interfaces.datavalue.CompositeValue):
    """ === CONSTRUCTOR === """
    def __init__(self, graph, node_id, **kwds):
        assert logger.debug('Constructing DataValue with id %s' % str(node_id))
        self.graph = graph
        self.node_id = node_id
        super(CompositeValue, self).__init__(**kwds)

    """ === PUBLIC INTERFACE === """
    def len(self):
        return DataValueFactory.create_instance(len(self.get_value()),
                                                IntegerValue)

    def __iter__(self):
        return Iterator(self)

    def __contains__(self, key):
        raise NotImplementedError()

    def get_node_id(self):
        return self.node_id

    def get_value(self):
        raise NotImplementedError()


class TupleValue(CompositeValue, HashableValue,
                 mvk.interfaces.datavalue.TupleValue):
    """ === CONSTRUCTOR === """
    def __init__(self, graph, node_id, **kwds):
        assert logger.debug('Constructing TupleValue')
        super(TupleValue, self).__init__(graph=graph,
                                         node_id=node_id,
                                         **kwds)
        self.l_type = TupleType(types=mvk.impl.python.datavalue.SequenceValue([el.typed_by() for el in self.get_value()]))

    """ === PUBLIC INTERFACE === """
    def typed_by(self):
        return self.l_type

    def __getitem__(self, index):
        if not (isinstance(index, IntegerValue) and
                isinstance(index.typed_by(), mvk.interfaces.datatype.IntegerType)):
            raise MvKTypeError(StringValue('Tuple indices must be IntegerValues, not %s'
                                           % type(index)))
        val = list(self.graph.triples((self.node_id, Literal(index), None)))
        if len(val) == 0:
            assert logger.debug('IndexError in TupleValue.__getitem__ %s %s'
                                % (self.len(), index))
            raise MvKIndexError(StringValue('%s' % index))
        else:
            t = list(self.graph.triples((val[0], Literal('python_cls'), None)))
            return eval('%s(self.graph, val[0])' % t[0])

    def __eq__(self, other):
        if not (super(TupleValue, self).__eq__(other) and
                isinstance(other.typed_by(), TupleType) and
                self.len() == other.len()):
            return DataValueFactory.create_instance(data=False)
        it_self = self.__iter__()
        it_other = other.__iter__()
        while (it_self.has_next()):
            if not it_self.next() == it_other.next():
                return DataValueFactory.create_instance(data=False)
        return DataValueFactory.create_instance(data=True)

    def get_value(self):
        triples = sorted(list(self.graph.triples((self.node_id, None, None))),
                         key=lambda x: x[1])
        values = []
        for t in triples:
            if t[1] != Literal('python_cls'):
                python_cls = list(self.graph.triples((t[2],
                                                      Literal('python_cls'),
                                                      None)))[0][2].toPython()
                values.append(eval('%s(self.graph, t[2])' % python_cls))
        return tuple(values)


def _get_type_from_set(typeset):
    if len(typeset) == 0:
        return AnyType()
    elif len(typeset) == 1:
        return typeset.pop()
    else:
        return UnionType(types=mvk.impl.python.datavalue.SequenceValue(value=list(typeset)))


class SequenceValue(CompositeValue, mvk.interfaces.datavalue.SequenceValue):
    """ === CONSTRUCTOR === """
    def __init__(self, graph, node_id, **kwds):
        assert logger.debug('Constructing SequenceValue')
        """ list(value) is called to copy the list """
        super(SequenceValue, self).__init__(graph=graph,
                                            node_id=node_id,
                                            **kwds)
        self.l_type = SequenceType(basetype=_get_type_from_set(set([el.typed_by() for el in self.get_value()])))

    """ === PUBLIC INTERFACE === """
    def typed_by(self):
        return self.l_type

    def __getitem__(self, index):
        if not (isinstance(index, mvk.interfaces.datavalue.IntegerValue) and
                isinstance(index.typed_by(), mvk.interfaces.datatype.IntegerType)):
            raise MvKTypeError(StringValue('SequenceValue indices must be IntegerValues, not %s'
                               % type(index)))
        try:
            return self.value[index.get_value()]
        except IndexError:
            raise MvKIndexError(StringValue('SequenceValue index out of range'))

    def __setitem__(self, index, item):
        raise NotImplementedError()

    def __delitem__(self, index):
        raise NotImplementedError()

    def append(self, x):
        raise NotImplementedError()

    def extend(self, x):
        raise NotImplementedError()

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
        raise NotImplementedError()

    def pop(self):
        raise NotImplementedError()

    def remove(self, x):
        raise NotImplementedError()

    def reverse(self):
        raise NotImplementedError()

    def sort(self):
        raise NotImplementedError()

    def __eq__(self, other):
        if not (super(SequenceValue, self).__eq__(other) and
                isinstance(other.typed_by(), SequenceType) and
                self.len() == other.len()):
            return DataValueFactory.create_instance(data=False)
        it_self = self.__iter__()
        it_other = other.__iter__()
        while (it_self.has_next()):
            if not it_self.next() == it_other.next():
                return DataValueFactory.create_instance(data=False)
        return DataValueFactory.create_instance(data=True)

    def get_value(self):
        triples = sorted(list(self.graph.triples((self.node_id, None, None))),
                         key=lambda x: x[1])
        values = []
        for t in triples:
            if t[1] != Literal('python_cls'):
                python_cls = list(self.graph.triples((t[2],
                                                      Literal('python_cls'),
                                                      None)))[0][2].toPython()
                values.append(eval('%s(self.graph, t[2])' % python_cls))
        return list(values)


class SetValue(CompositeValue, mvk.interfaces.datavalue.SetValue):
    """ === CONSTRUCTOR === """
    def __init__(self, graph, node_id, **kwds):
        assert logger.debug('Constructing SetValue')
        super(SetValue, self).__init__(graph=graph,
                                       node_id=node_id,
                                       **kwds)
        self.l_type = SetType(basetype=_get_type_from_set(set([el.typed_by() for el in self.get_value()])))

    """ === PUBLIC INTERFACE === """
    def typed_by(self):
        return self.l_type

    def __contains__(self, key):
        if not (isinstance(key, mvk.interfaces.datavalue.HashableValue) and
                isinstance(key.typed_by(), mvk.interfaces.datatype.HashableType)):
            raise MvKTypeError(StringValue('Unhashable type: %s'
                                           % type(key)))
        return DataValueFactory.create_instance(data=key in self.value)

    def add(self, element):
        raise NotImplementedError()

    def remove(self, element):
        raise NotImplementedError()

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
        return SetValue(value=(self.value and setvalue.get_value()))

    def issubset(self, setvalue):
        if not (isinstance(setvalue, mvk.interfaces.datavalue.SetValue) and
                isinstance(setvalue.typed_by(), mvk.interfaces.datatype.SetType)):
            raise MvKTypeError(StringValue('Expected a SetValue, not a %s'
                                           % type(setvalue)))
        return DataValueFactory.create_instance(data=self.value <= setvalue.get_value())

    def issuperset(self, setvalue):
        if not (isinstance(setvalue, mvk.interfaces.datavalue.SetValue) and
                isinstance(setvalue.typed_by(), mvk.interfaces.datatype.SetType)):
            raise MvKTypeError(StringValue('Expected a SetValue, not a %s'
                                           % type(setvalue)))
        return DataValueFactory.create_instance(data=self.value >= setvalue.get_value())

    def __eq__(self, other):
        if not (super(SetValue, self).__eq__(other) and
                isinstance(other.typed_by(), SetType) and
                self.len() == other.len()):
            return DataValueFactory.create_instance(data=False)
        it_self = self.__iter__()
        while (it_self.has_next()):
            if not it_self.next() in other:
                return DataValueFactory.create_instance(data=False)
        return DataValueFactory.create_instance(data=True)

    def get_value(self):
        triples = set(self.graph.triples((self.node_id, Literal('item'), None)))
        values = set()
        for t in triples:
            if t[1] != Literal('python_cls'):
                python_cls = list(self.graph.triples((t[2],
                                                      Literal('python_cls'),
                                                      None)))[0][2].toPython()
                values.add(eval('%s(self.graph, t[2])' % python_cls))
        return values


class MappingValue(CompositeValue, mvk.interfaces.datavalue.MappingValue):
    """ === CONSTRUCTOR === """
    def __init__(self, graph, node_id, **kwds):
        """ dict(value) is called to copy the dict """
        super(MappingValue, self).__init__(graph=graph,
                                           node_id=node_id,
                                           **kwds)
        self.l_type = MappingType(keytype=_get_type_from_set(set([el.typed_by() for el in self.keys().get_value()])),
                                   valuetype=_get_type_from_set(set([el.typed_by() for el in self.values().get_value()])))

    """ === PUBLIC INTERFACE === """
    def typed_by(self):
        return self.l_type

    def __contains__(self, key):
        if not (isinstance(key, HashableValue) and
                isinstance(key.typed_by(), mvk.interfaces.datatype.HashableType)):
            raise MvKTypeError(StringValue('Unhashable type: %s' % type(key)))
        return DataValueFactory.create_instance(data=key in self.value)

    def __iter__(self):
        return Iterator(self.keys())

    def keys(self):
        return DataValueFactory.create_instance(data=set(self.get_value().keys()))

    def values(self):
        return DataValueFactory.create_instance(data=list(self.get_value().values()))

    def __getitem__(self, key):
        if not (isinstance(key, HashableValue) and
                isinstance(key.typed_by(), mvk.interfaces.datatype.HashableType)):
            raise MvKTypeError(StringValue('Unhashable type: %s' % type(key)))
        try:
            return self.get_value()[key]
        except KeyError:
            raise MvKKeyError(StringValue('%s' % key))

    def __setitem__(self, key, val):
        raise NotImplementedError()

    def __delitem__(self, key):
        raise NotImplementedError()

    def clear(self):
        raise NotImplementedError()

    def pop(self, key, default=None):
        raise NotImplementedError()

    def __eq__(self, other):
        if not (super(MappingValue, self).__eq__(other) and
                isinstance(other.typed_by(), MappingType) and
                self.len() == other.len()):
            return DataValueFactory.create_instance(data=False)
        it_self = self.__iter__()
        it_other = other.__iter__()
        while (it_self.has_next()):
            if not self[it_self.next()] == other[it_other.next()]:
                return DataValueFactory.create_instance(data=False)
        return DataValueFactory.create_instance(data=True)

    def get_value(self):
        triples = set(self.graph.triples((self.node_id, Literal('key'), None)))
        value = {}
        for t in triples:
            if t[1] != Literal('python_cls'):
                key_cls = list(self.graph.triples((t[2],
                                                   Literal('python_cls'),
                                                   None)))[0][2].toPython()
                val = list(self.graph.triples((t[2], Literal('m_val'), None)))[0][2]
                val_cls = list(self.graph.triples((val,
                                                   Literal('python_cls'),
                                                   None)))[0][2].toPython()
                value[eval('%s(self.graph, t[2])' % key_cls)] = eval('%s(self.graph, val)' % val_cls)
        return value


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
        return ((super(Iterator, self).__eq__(other)) and
                (BooleanValue(isinstance(other, Iterator))) and
                (id(self.original_iterable) == id(other.original_iterable)))


class ImmutableCompositeValue(CompositeValue,
                              mvk.interfaces.datavalue.ImmutableCompositeValue):
    pass


class ImmutableSequenceValue(SequenceValue, ImmutableCompositeValue,
                             mvk.interfaces.datavalue.ImmutableSequenceValue):
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


class ImmutableSetValue(SetValue, ImmutableCompositeValue,
                           mvk.interfaces.datavalue.ImmutableSetValue):
    def add(self, element):
        raise MvKTypeError(StringValue('ImmutableSetValue does not support \
                                        item addition.'))

    def remove(self, element):
        raise MvKTypeError(StringValue('ImmutableSetValue does not support \
                                        item deletion.'))


class ImmutableMappingValue(MappingValue, ImmutableCompositeValue,
                               mvk.interfaces.datavalue.ImmutableMappingValue):
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


class DataValueFactory(object):
    @classmethod
    def create_instance(cls, data, datacls=None):
        bnode = BNode()
        datatype = type(data)
        if datatype is int:
            datacls = datacls or IntegerValue
        if datatype is float:
            datacls = datacls or FloatValue
        elif datatype is str:
            datacls = datacls or StringValue
        elif datatype is bool:
            datacls = datacls or BooleanValue
        if datatype in [int, float, str, bool]:
            rdf_graph.g.add((bnode, Literal('val'), Literal(data)))
            rdf_graph.g.add((bnode, Literal('python_cls'), Literal(datacls.__name__)))
            return datacls(rdf_graph.g, bnode)
        elif datatype is set:
            rdf_graph.g.add((bnode, Literal('python_cls'), Literal('SetValue')))
            for d in data:
                d_instance = cls.create_instance(d)
                rdf_graph.g.add((bnode, Literal('item'), d_instance.get_node_id()))
            return SetValue(graph=rdf_graph.g,
                            node_id=bnode)
        elif datatype is tuple:
            rdf_graph.g.add((bnode, Literal('python_cls'), Literal('TupleValue')))
            for i, d in enumerate(data):
                d_instance = cls.create_instance(d)
                rdf_graph.g.add((bnode, Literal(i), d_instance.get_node_id()))
            return TupleValue(graph=rdf_graph.g,
                              node_id=bnode)
        elif datatype is list:
            rdf_graph.g.add((bnode, Literal('python_cls'), Literal('SequenceValue')))
            for i, d in enumerate(data):
                d_instance = cls.create_instance(d)
                rdf_graph.g.add((bnode, Literal(i), d_instance.get_node_id()))
            return SequenceValue(graph=rdf_graph.g,
                                 node_id=bnode)
        elif datatype is dict:
            rdf_graph.g.add((bnode, Literal('python_cls'), Literal('SequenceValue')))
            for k, v in data.iteritems():
                k_instance = cls.create_instance(k)
                v_instance = cls.create_instance(v)
                rdf_graph.g.add((bnode, Literal('key'), k_instance.get_node_id()))
                rdf_graph.g.add((k_instance.get_node_id(), Literal('m_val'), v_instance.get_node_id()))
            return MappingValue(graph=rdf_graph.g,
                                node_id=bnode)
        elif issubclass(datatype, Element):
            return data
        else:
            raise TypeError("Don't know what the resulting datavalue will be \
                            (implementation error): %s (from %s)"
                            % (datatype.__name__, data))

    @classmethod
    def create_instance_from_type(cls, atype, data):
        if not isinstance(atype, Type):
            raise TypeError('Can only create instances from Type, got %s'
                            % str(atype))

        """ TODO: Well, implement this! """
        return atype.create_instance(data)

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
