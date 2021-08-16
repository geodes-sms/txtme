"""
Created on 28-dec.-2013

@author: Simon
"""
from mvk.interfaces.element import Element, NamedElement


class Type(Element):
    """ Top-level Type class. All types need to subclass this class. """
    def is_type_of(self, el):
        """
        Checks whether the passed element is typed by this type.
        @type el: L{Element<mvk.interfaces.element.Element>}
        @param el: An element.
        @rtype: L{BooleanValue<mvk.interfaces.datavalue.BooleanValue>}
        @return: BooleanValue(True) if element is an instance of this type,
                 else BooleanValue(False).
        """
        raise NotImplementedError()


class PackageType(Type):
    pass


class TypeType(Type):
    pass


class DataType(Type):
    pass


class VoidType(DataType):
    pass


class AnyType(DataType):
    pass


class HashableType(DataType):
    pass


class StringType(HashableType):
    pass


class LocationType(StringType):
    pass


class NumericType(HashableType):
    pass


class BooleanType(NumericType):
    pass


class IntegerType(NumericType):
    pass


class FloatType(NumericType):
    pass


class InfiniteType(FloatType):
    pass


class SingleBaseType(DataType):
    def get_basetype(self):
        """
        @rtype: L{Type<mvk.interfaces.datatype.Type>}
        @return: The basetype of this type.
        """
        raise NotImplementedError()


class SetType(SingleBaseType):
    pass


class SequenceType(SingleBaseType):
    pass


class CompositeType(DataType):
    def get_types(self):
        """
        @rtype: L{SequenceValue<mvk.interfaces.datavalue.SequenceValue>}
        @return: The sequence of types this type is composed of.
        """
        raise NotImplementedError()


class UnionType(CompositeType):
    pass


class TupleType(CompositeType, HashableType):
    pass


class MappingType(DataType):
    def get_keytype(self):
        """
        @rtype: L{HashableType<mvk.interfaces.datatype.HashableType>}
        @return: The type of the keys of this mapping type.
        """
        raise NotImplementedError()

    def get_valuetype(self):
        """
        @rtype: L{Type<mvk.interfaces.datatype.Type>}
        @return: The type of the values of this mapping type.
        """
        raise NotImplementedError()


class IteratorType(DataType):
    def get_iterated_type(self):
        """
        @rtype: L{Type<mvk.interfaces.datatype.Type>}
        @return: The type which this iterator can iterate over.
        """
        raise NotImplementedError()


class UserDefinedType(DataType, NamedElement):
    pass


class EnumType(UserDefinedType):
    def get_val(self, name):
        """
        @type name: L{StringValue<mvk.interfaces.datavalue.StringValue>}
        @param name: A string.
        @rtype: L{EnumValue<mvk.interfaces.datavalue.EnumValue>}
        @return: The value with given name.
        @raise L{MvKNameError<mvk.interfaces.exception.MvKNameError>}: If the name is not defined in this EnumType.
        @raise L{MvKTypeError<mvk.interfaces.exception.MvKTypeError>}: If 'name' is not a string.
        """
        raise NotImplementedError()

    def get_name(self, val):
        """
        @type val: L{EnumValue<mvk.interfaces.datavalue.EnumValue>}
        @param val: An enumeration value.
        @rtype: L{StringValue<mvk.interfaces.datavalue.StringValue>}
        @return: The name corresponding to the given value.
        @raise L{MvKValueError<mvk.interfaces.exception.MvKValueError>}: If the value is not defined in this EnumType.
        @raise L{MvKTypeError<mvk.interfaces.exception.MvKTypeError>}: If 'val' is not an enumeration value.
        """
        raise NotImplementedError()

    def get_values(self):
        """
        @rtype: L{ImmutableMappingValue<mvk.interfaces.datavalue.ImmutableMappingValue>}
        @return: The mapping between names and enum values.
        """
        raise NotImplementedError()
