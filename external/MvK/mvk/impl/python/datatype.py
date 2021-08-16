"""
Created on 28-dec.-2013

@author: Simon
"""

import operator

from mvk.impl.python.element import Element
from mvk.impl.python.exception import MvKTypeError, MvKValueError
import mvk.interfaces.datatype
from mvk.lib.pyparsing import Word, alphas, Forward, Group, delimitedList, \
    Suppress, alphanums
from mvk.util.logger import get_logger

logger = get_logger('datatype')

class Type(Element, mvk.interfaces.datatype.Type):
    """ === PUBLIC INTERFACE === """
    def typed_by(self):
        return TypeType()

    """ === PYTHON SPECIFIC === """
    def __repr__(self):
        return self.__class__.__name__


class PackageType(Type, mvk.interfaces.datatype.PackageType):
    """ === PUBLIC INTERFACE === """
    def is_type_of(self, el):
        from mvk.impl.python.datavalue import BooleanValue
        return BooleanValue(isinstance(el.typed_by(),
                                       mvk.interfaces.datatype.PackageType))

    def __eq__(self, other):
        from mvk.impl.python.datavalue import BooleanValue
        return (super(PackageType, self).__eq__(other) and
                BooleanValue(isinstance(other, mvk.interfaces.datatype.PackageType)))


class TypeType(Type, mvk.interfaces.datatype.TypeType):
    """ === PUBLIC INTERFACE === """
    def is_type_of(self, el):
        from mvk.impl.python.datavalue import BooleanValue
        return BooleanValue(isinstance(el.typed_by(),
                                       mvk.interfaces.datatype.Type))

    def __eq__(self, other):
        from mvk.impl.python.datavalue import BooleanValue
        return (super(TypeType, self).__eq__(other) and
                BooleanValue(isinstance(other, mvk.interfaces.datatype.TypeType)))


class DataType(Type, mvk.interfaces.datatype.DataType):
    pass


class VoidType(DataType, mvk.interfaces.datatype.VoidType):
    """ === PUBLIC INTERFACE === """
    def is_type_of(self, el):
        from mvk.impl.python.datavalue import BooleanValue
        return BooleanValue(isinstance(el.typed_by(),
                                       mvk.interfaces.datatype.VoidType))

    def __eq__(self, other):
        from mvk.impl.python.datavalue import BooleanValue
        return (super(VoidType, self).__eq__(other) and
                BooleanValue(isinstance(other, mvk.interfaces.datatype.VoidType)))


class AnyType(DataType, mvk.interfaces.datatype.AnyType):
    """ === PUBLIC INTERFACE === """
    def is_type_of(self, el):
        from mvk.impl.python.datavalue import BooleanValue
        """ We return True here, because something which is typed by AnyType
        can have any value assigned to it. """
        return BooleanValue(True)

    def __eq__(self, other):
        from mvk.impl.python.datavalue import BooleanValue
        return (super(AnyType, self).__eq__(other) and
                BooleanValue(isinstance(other, mvk.interfaces.datatype.AnyType)))


class StringType(DataType, mvk.interfaces.datatype.StringType):
    """ === PUBLIC INTERFACE === """
    def is_type_of(self, el):
        from mvk.impl.python.datavalue import BooleanValue
        return BooleanValue(isinstance(el.typed_by(),
                                       mvk.interfaces.datatype.StringType))

    def __eq__(self, other):
        from mvk.impl.python.datavalue import BooleanValue
        return BooleanValue(isinstance(other, mvk.interfaces.datatype.StringType))


class LocationType(StringType, mvk.interfaces.datatype.LocationType):
    """ === PUBLIC INTERFACE === """
    def is_type_of(self, el):
        from mvk.impl.python.datavalue import BooleanValue
        return BooleanValue(isinstance(el.typed_by(),
                                       mvk.interfaces.datatype.LocationType))

    def __eq__(self, other):
        from mvk.impl.python.datavalue import BooleanValue
        return BooleanValue(isinstance(other, mvk.interfaces.datatype.LocationType))


class NumericType(DataType, mvk.interfaces.datatype.NumericType):
    pass


class BooleanType(NumericType, mvk.interfaces.datatype.BooleanType):
    """ === PUBLIC INTERFACE === """
    def is_type_of(self, el):
        from mvk.impl.python.datavalue import BooleanValue
        return BooleanValue(isinstance(el.typed_by(),
                                       mvk.interfaces.datatype.BooleanType))

    def __eq__(self, other):
        from mvk.impl.python.datavalue import BooleanValue
        return BooleanValue(isinstance(other, mvk.interfaces.datatype.BooleanType))


class IntegerType(NumericType, mvk.interfaces.datatype.IntegerType):
    """ === PUBLIC INTERFACE === """
    def is_type_of(self, el):
        from mvk.impl.python.datavalue import BooleanValue
        return BooleanValue(isinstance(el.typed_by(),
                                       mvk.interfaces.datatype.IntegerType))

    def __eq__(self, other):
        from mvk.impl.python.datavalue import BooleanValue
        return BooleanValue(isinstance(other, mvk.interfaces.datatype.IntegerType))


class FloatType(NumericType, mvk.interfaces.datatype.FloatType):
    """ === PUBLIC INTERFACE === """
    def is_type_of(self, el):
        from mvk.impl.python.datavalue import BooleanValue
        return BooleanValue(isinstance(el.typed_by(), mvk.interfaces.datatype.FloatType))

    def __eq__(self, other):
        from mvk.impl.python.datavalue import BooleanValue
        return BooleanValue(isinstance(other, mvk.interfaces.datatype.FloatType))


class InfiniteType(FloatType, mvk.interfaces.datatype.InfiniteType):
    """ === PUBLIC INTERFACE === """
    def is_type_of(self, el):
        from mvk.impl.python.datavalue import BooleanValue
        return BooleanValue(isinstance(el.typed_by(),
                                       mvk.interfaces.datatype.InfiniteType))

    def __eq__(self, other):
        from mvk.impl.python.datavalue import BooleanValue
        return BooleanValue(isinstance(other, mvk.interfaces.datatype.InfiniteType))


class SingleBaseType(DataType, mvk.interfaces.datatype.SingleBaseType):
    """ === CONSTRUCTOR === """
    def __init__(self, basetype, **kwds):
        assert isinstance(basetype, mvk.interfaces.datatype.Type)
        assert logger.debug('Constructing SingleBaseType with basetype %s'
                            % basetype)
        self.basetype = basetype

    """ === PUBLIC INTERFACE === """
    def get_basetype(self):
        return self.basetype

    def __eq__(self, other):
        from mvk.impl.python.datavalue import BooleanValue
        return BooleanValue(isinstance(other, SingleBaseType)) and self.get_basetype() == other.get_basetype()

    """ === PYTHON SPECIFIC === """
    def __repr__(self):
        return '%s[%s]' % (self.__class__.__name__, str(self.basetype))


class SetType(SingleBaseType, mvk.interfaces.datatype.SetType):
    """ === PUBLIC INTERFACE === """
    def is_type_of(self, el):
        from mvk.impl.python.datavalue import BooleanValue
        el_type = el.typed_by()
        if not (isinstance(el, mvk.interfaces.datavalue.SetValue) and
                isinstance(el_type, mvk.interfaces.datatype.SetType)):
            return BooleanValue(False)
        for elem in el:
            if not self.basetype.is_type_of(elem):
                return BooleanValue(False)

        return BooleanValue(True)

    def __eq__(self, other):
        from mvk.impl.python.datavalue import BooleanValue
        return (super(SetType, self).__eq__(other) and
                BooleanValue(isinstance(other, mvk.interfaces.datatype.SetType)))


class SequenceType(SingleBaseType, mvk.interfaces.datatype.SequenceType):
    """ === PUBLIC INTERFACE === """
    def is_type_of(self, el):
        from mvk.impl.python.datavalue import BooleanValue
        el_type = el.typed_by()
        if not (isinstance(el, mvk.interfaces.datavalue.SequenceValue) and
                isinstance(el_type, mvk.interfaces.datatype.SequenceType)):
            return BooleanValue(False)
        for elem in el:
            if not self.basetype.is_type_of(elem):
                return BooleanValue(False)
        
        return BooleanValue(True)

    def __eq__(self, other):
        from mvk.impl.python.datavalue import BooleanValue
        return (super(SequenceType, self).__eq__(other) and
                BooleanValue(isinstance(other, mvk.interfaces.datatype.SequenceType)))


class CompositeType(DataType, mvk.interfaces.datatype.CompositeType):
    """ === CONSTRUCTOR === """
    def __init__(self, types, **kwds):
        assert (isinstance(types, mvk.interfaces.datavalue.SequenceValue))
        '''
        TODO: Reinstate this, but right now, typed_by() has some unwanted
        effects when references are made to clabjects that don't exist.
        assert (isinstance(types, mvk.interfaces.datavalue.SequenceValue) and
                isinstance(types.typed_by(), mvk.interfaces.datatype.SequenceType))
        '''
        assert logger.debug('Constructing CompositeType with types %s'
                            % types)
        self.types = types
        super(CompositeType, self).__init__(**kwds)

    """ === PUBLIC INTERFACE === """
    def get_types(self):
        from mvk.impl.python.datavalue import SequenceValue, ImmutableSequenceValue
        return ImmutableSequenceValue(SequenceValue(value=self.types.get_value()))

    def __eq__(self, other):
        from mvk.impl.python.datavalue import BooleanValue
        from mvk.util.utility_functions import lists_eq_items
        return (BooleanValue(isinstance(other, mvk.interfaces.datatype.CompositeType)) and
                lists_eq_items(self.get_types(), other.get_types()))

    """ === PYTHON SPECIFIC === """
    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, ', '.join([str(t) for t in self.types.get_value()]))


class UnionType(CompositeType, mvk.interfaces.datatype.UnionType):
    """ === PUBLIC INTERFACE === """
    def is_type_of(self, el):
        from mvk.impl.python.datavalue import BooleanValue
        return reduce(operator.add,
                      map(lambda t: t.is_type_of(el),
                          self.get_types().get_value()),
                      BooleanValue(False))

    def __eq__(self, other):
        from mvk.impl.python.datavalue import BooleanValue
        return (super(UnionType, self).__eq__(other) and
                BooleanValue(isinstance(other, mvk.interfaces.datatype.UnionType)))


class TupleType(CompositeType, mvk.interfaces.datatype.TupleType):
    """ === PUBLIC INTERFACE === """
    def is_type_of(self, el):
        from mvk.impl.python.datavalue import BooleanValue
        el_type = el.typed_by()
        if not (isinstance(el, mvk.interfaces.datavalue.TupleValue) and
                isinstance(el_type, mvk.interfaces.datatype.TupleType) and
                el.len() == self.types.len()):
            return BooleanValue(False)
        for t, elem in zip(self.get_types(), el):
            if not t.is_type_of(elem):
                return BooleanValue(False)

        return BooleanValue(True)

    def __eq__(self, other):
        from mvk.impl.python.datavalue import BooleanValue
        return (super(TupleType, self).__eq__(other) and
                BooleanValue(isinstance(other, mvk.interfaces.datatype.TupleType)))


class MappingType(DataType, mvk.interfaces.datatype.MappingType):
    """ === CONSTRUCTOR === """
    def __init__(self, keytype=None, valuetype=None, **kwds):
        if keytype is None:
            keytype = AnyType()
        if valuetype is None:
            valuetype = AnyType()
        assert logger.debug('Constructing MappingType with keytype %s and valuetype %s'
                            % (keytype, valuetype))
        self.keytype = keytype
        self.valuetype = valuetype
        super(MappingType, self).__init__(**kwds)

    """ === PUBLIC INTERFACE === """
    def get_keytype(self):
        return self.keytype

    def get_valuetype(self):
        return self.valuetype

    def is_type_of(self, el):
        from mvk.impl.python.datavalue import BooleanValue
        el_type = el.typed_by()
        if not (isinstance(el, mvk.interfaces.datavalue.MappingValue) and
                isinstance(el_type, mvk.interfaces.datatype.MappingType)):
            return BooleanValue(False)
        for elem in el:
            if not (self.keytype.is_type_of(elem) and
                    self.valuetype.is_type_of(el[elem])):
                return BooleanValue(False)

        return BooleanValue(True)

    def __eq__(self, other):
        from mvk.impl.python.datavalue import BooleanValue
        return BooleanValue(isinstance(other, MappingType)) and \
                self.get_keytype() == other.get_keytype() and \
                self.get_valuetype() == other.get_valuetype()

    """ === PYTHON SPECIFIC === """
    def __repr__(self):
        return '%s(%s: %s)' % (self.__class__.__name__,
                               str(self.keytype),
                               str(self.valuetype))


class IteratorType(DataType, mvk.interfaces.datatype.Type):
    """ === CONSTRUCTOR === """
    def __init__(self, iteratedtype=None, **kwds):
        if iteratedtype is None:
            iteratedtype = AnyType()
        assert logger.debug('Constructing IteratorType with iteratedtype %s'
                            % iteratedtype)
        self.iteratedtype = iteratedtype
        super(IteratorType, self).__init__(**kwds)

    """ === PUBLIC INTERFACE === """
    def get_iterated_type(self):
        return self.iteratedtype

    """ === PYTHON SPECIFIC === """
    def __repr__(self):
        return 'Iterator<%s>' % self.iteratedtype


class UserDefinedType(DataType, mvk.interfaces.datatype.UserDefinedType):
    pass


class EnumType(UserDefinedType, mvk.interfaces.datatype.EnumType):
    """ === CONSTRUCTOR === """
    def __init__(self, values, **kwds):
        assert isinstance(values, list)
        from mvk.impl.python.datavalue import StringValue, EnumValue, MappingValue, ImmutableMappingValue
        dictval = {}
        self.valuesrev = {}
        for i, v in enumerate(values):
            e_val = EnumValue(l_type=self, value=(i + 1))
            dictval[StringValue(v)] = e_val
            self.valuesrev[e_val] = StringValue(v)
        self.values = ImmutableMappingValue(MappingValue(value=dictval))

    """ === PUBLIC INTERFACE === """
    def get_val(self, name):
        from mvk.impl.python.datavalue import StringValue
        if not (isinstance(name, StringValue) and
                isinstance(name.typed_by(), StringType)):
            raise MvKTypeError(StringValue('expected a string'))
        try:
            return self.values[name]
        except ValueError:
            raise MvKValueError()

    def get_name(self, val):
        from mvk.impl.python.datavalue import EnumValue, StringValue
        if not (isinstance(val, EnumValue) and
                val.typed_by() == self):
            raise MvKTypeError(StringValue('expected an enum value'))
        try:
            return self.valuesrev[val]
        except ValueError:
            raise MvKValueError()

    def get_values(self):
        return self.values

    def is_type_of(self, el):
        from mvk.interfaces.datavalue import EnumValue
        return isinstance(el, EnumValue) and el.typed_by() == self

    def __eq__(self, other):
        from mvk.impl.python.datavalue import BooleanValue
        return (super(EnumType, self).__eq__(other) and
                BooleanValue(isinstance(other, mvk.interfaces.datatype.EnumType)) and
                self.get_values() == other.get_values())


class TypeFactory(object):
    __types = {}
    LPAREN = Suppress("(")
    LBRACK = Suppress("[")
    RBRACK = Suppress("]")
    RPAREN = Suppress(")")
    CURLYL = Suppress("{")
    CURLYR = Suppress("}")
    LESSTHAN = Suppress("<")
    GREATERTHAN = Suppress(">")
    COLON = Suppress(":")
    ENUM = Suppress("enum")
    ITERATOR = Suppress("iterator")
    ID = Word(alphas + "_", alphanums + "_")

    type_decl = Forward()
    type_id = Word(alphas)
    primitive_type = type_id.copy().setParseAction(lambda t: TypeFactory.get_primitive_type(t[0]))
    single_basetype = (type_id + LBRACK + type_decl + RBRACK).setParseAction(lambda t: TypeFactory.get_single_base_type(t[0], t[1]))
    composite_type = (type_id + LPAREN + Group(delimitedList(type_decl)) + RPAREN).setParseAction(lambda t: TypeFactory.get_composite_type(t[0], t[1].asList()))
    mapping_type = (type_id + LPAREN + type_decl + COLON + type_decl + RPAREN).setParseAction(lambda t: TypeFactory.get_mapping_type(t[0], t[1], t[2]))
    iterator_type = (ITERATOR + LESSTHAN + type_decl + GREATERTHAN).setParseAction(lambda t: TypeFactory.get_iterator_type(t[0]))
    enum_type = (ENUM + ID + CURLYL + Group(delimitedList(ID)) + CURLYR).setParseAction(lambda t: TypeFactory.get_enum_type(t[0], t[1].asList()))

    type_decl << (single_basetype | composite_type | mapping_type | enum_type | iterator_type | primitive_type)

    @classmethod
    def get_type(cls, typename):
        """
        Returns the type corresponding to the type name passed as paremeter.
        The paremeter 'typename' can have the following forms (examples in brackets):
             - PrimitiveType (FloatType, IntegerType, ...)
             - SingleBaseType\[Type\] (SequenceType[IntegerType])
             - CompositeType\(Type[, Type]*\) (TupleType(IntegerType, FloatType))
             - MappingType\(Type: Type\) (MappingType(IntegerType: StringType))
             - enum ID\{ID[, ID]*\}
             - iterator\<Type\>
        @type typename: string
        @param typename: The name of the type.
        @rtype: L{Type<mvk.interfaces.datatype.Type>}
        @return: The type corresponding to the type specified in 'typename'.
        """
        assert isinstance(typename, str)
        return cls.type_decl.parseWithTabs().parseString(typename).asList()[0]

    @classmethod
    def get_primitive_type(cls, typename):
        """
        Returns the primitive type with name 'typename'.
        """
        assert isinstance(typename, str)
        try:
            assert logger.debug('get_primitive_type(%s)' % typename)
            if not typename in cls.__types:
                cls.__types[typename] = eval('%s()' % typename)
            return cls.__types[typename]
        except Exception, e:
            assert logger.error(str(e))
            raise e

    @classmethod
    def get_single_base_type(cls, typename, basetype):
        """
        Returns the type with name 'typename', and base type 'basetype'.
        @type typename: string
        @param typename: The name of the type.
        @type basetype: L{Type<mvk.interfaces.datatype.Type>}
        @param basetype: The base type of the single base type.
        @rtype: L{SingleBaseType<mvk.interfaces.datatype.SingleBaseType>}
        @return: An instance of the type with name 'typename' and base type 'basetype' 
        """
        assert isinstance(typename, str)
        assert isinstance(basetype, Type)
        try:
            assert logger.debug('get_single_base_type(%s, %s)' % (typename, basetype))
            typestr = '%s[%s]' % (typename, basetype)
            if not typestr in cls.__types:
                cls.__types[typestr] = eval('%s(basetype)' % typename)
            return cls.__types[typestr]
        except Exception, e:
            assert logger.error(str(e))
            raise e

    @classmethod
    def get_composite_type(cls, typename, types=[]):
        """
        Returns the type with name 'typename', composed of the types in 'types'.
        @type typename: string
        @param typename: The name of the type.
        @type types: list
        @param types: The list of types that the type is composed of.
        @rtype: L{CompositeType<mvk.interfaces.datatype.CompositeType>}
        @return: An instance of the type with name 'typename' and composed of the types in 'types'.
        """
        assert isinstance(typename, str)
        assert isinstance(types, list)
        assert reduce(operator.mul, map(lambda t: isinstance(t, Type), types), True)
        try:
            assert logger.debug('get_composite_type(%s, (%s))' % (typename, ', '.join([str(t) for t in types])))
            typestr = '%s(%s)' % (typename, ','.join([str(t) for t in types]))
            if not typestr in cls.__types:
                from mvk.impl.python.datavalue import SequenceValue
                new_type = eval('%s(types=SequenceValue(value=types))' % typename)
                cls.__types[typestr] = new_type
            return cls.__types[typestr]
        except Exception, e:
            assert logger.error(str(e))
            raise e

    @classmethod
    def get_mapping_type(cls, typename, keytype, valtype):
        """
        Returns the type with name 'typename', with key type 'keytype' and value type 'valtype'.
        @type typename: string
        @param typename: The name of the type.
        @type keytype: L{Type<mvk.interfaces.datatype.Type>}
        @param keytype: The key type of the type.
        @type valtype: L{Type<mvk.interfaces.datatype.Type>}
        @param valtype: The value type of the type.
        @rtype: L{MappingType<mvk.interfaces.datatype.MappingType>}
        @return: An instance of the type with name 'typename', key type 'keytype' and value type 'valtype'.
        """
        try:
            assert logger.debug('get_mapping_type(%s, (%s: %s))' % (typename, str(keytype), str(valtype)))
            typestr = '%s(%s: %s)' % (typename, str(keytype), str(valtype))
            if not typestr in cls.__types:
                cls.__types[typestr] = eval('%s(keytype=keytype, valuetype=valtype)' % typename)
            return cls.__types[typestr]
        except Exception, e:
            assert logger.error(str(e))
            raise e

    @classmethod
    def get_iterator_type(cls, iteratedtype):
        """
        Returns the iterator type with iterated type 'iteratedtype'.
        @type iteratedtype: L{Type<mvk.interfaces.datatype.Type>}
        @param iteratedtype: The iterated type of the iterator type.
        @rtype: L{IteratorType<mvk.interfaces.datatype.IteratorType>}
        @return: An instance of the iterator type with iterated type 'iteratedtype'.
        """
        assert isinstance(iteratedtype, Type)
        try:
            assert logger.debug('get_iterator_type(%s)' % iteratedtype)
            typestr = 'iterator<%s>' % iteratedtype
            if not typestr in cls.__types:
                cls.__types[typestr] = IteratorType(iteratedtype)
            return cls.__types[typestr]
        except Exception, e:
            assert logger.error(str(e))
            raise e

    @classmethod
    def get_enum_type(cls, typename, values):
        """
        Returns the enum type with name 'typename', consisting of values in 'values'.
        @type typename: string
        @param typename: The name of the type.
        @type values: list
        @param values: The values in this enumeration.
        @rtype: L{EnumType<mvk.interfaces.datatype.EnumType>}
        @return: The enum type with name 'typename' and with values 'values'.
        """
        assert isinstance(typename, str)
        assert isinstance(values, list)
        assert reduce(operator.mul, map(lambda v: isinstance(v, str), values), True)
        try:
            assert logger.debug('get_enum_type(%s, (%s))' % (typename, values))
            return EnumType(values)
        except Exception, e:
            assert logger.error(str(e))
            raise e
