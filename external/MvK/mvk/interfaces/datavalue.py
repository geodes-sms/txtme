"""
Created on 28-dec.-2013

@author: Simon
"""
from mvk.interfaces.element import Element


class DataValue(Element):
    pass


class VoidValue(DataValue):
    pass


class AnyValue(DataValue):
    pass


class HashableValue(DataValue):
    """
    Marker class. Used to distinguish those values that can be used as
    values in L{SetValue<mvk.interfaces.datavalue.SetValue>}s, and as keys
    in L{MappingValue<mvk.interfaces.datavalue.MappingValue>}s.
    """


class NumericValue(HashableValue):
    def __add__(self, other):
        """
        Returns the sum of this value and 'other'.
        @type other: L{NumericValue}
        @param other: The value to add to this value.
        @rtype: L{NumericValue}
        @return: The sum of both values.
        @raise MvKTypeError: If 'other' is not an instance of NumericValue.
        """
        raise NotImplementedError()

    def __sub__(self, other):
        """
        Returns the result of subtracting 'other' from this value.
        @type other: L{NumericValue}
        @param other: The value to subtract from this value.
        @rtype: L{NumericValue}
        @return: The difference of this value and 'other'.
        @raise MvKTypeError: If 'other' is not an instance of NumericValue.
        """
        raise NotImplementedError()

    def __mul__(self, other):
        """
        Returns the product of this value and 'other'.
        @type other: L{NumericValue}
        @param other: The value to multiply with this value.
        @rtype: L{NumericValue}
        @return: The product of this value and 'other'.
        @raise MvKTypeError: If 'other' is not an instance of NumericValue.
        """
        raise NotImplementedError()

    def __div__(self, other):
        """
        Returns the result of dividing this value with 'other'.
        @type other: L{NumericValue}
        @param other: The value to divide this value by.
        @rtype: L{NumericValue}
        @return: The quotient of this value and the value 'other'.
        @raise MvKTypeError: If 'other' is not an instance of L{NumericValue}.
        @raise MvKZeroDivisionError: If 'other' has a value of 0.
        """
        raise NotImplementedError()

    def __mod__(self, other):
        """
        Returns the remainder when dividing this value and 'other'.
        @type other: L{NumericValue}
        @param other: The value to divide this value by.
        @rtype: L{NumericValue}
        @return: The remainder when dividing this value with 'other'.
        @raise MvKTypeError: If 'other' is not an instance of L{NumericValue}.
        @raise MvKZeroDivisionError: If 'other' has a value of 0.
        """
        raise NotImplementedError()

    def __and__(self, other):
        """
        Careful! While in Python, this is the bitwise and operator '&',
        this function should implement the behaviour of the 'and' keyword.
        @type other: L{NumericValue}
        @param other: A value.
        @rtype: L{NumericValue}
        @return: 'other' if this value evaluates to True, otherwise this value.
        @raise MvKTypeError: If 'other' is not an instance of L{NumericValue}.
        """
        raise NotImplementedError()

    def __or__(self, other):
        """
        Careful! While in Python, this is the bitwise and operator '|',
        this function should implement the behaviour of the 'or' keyword.
        @type other: L{NumericValue}
        @param other: A value.
        @rtype: L{NumericValue}
        @return: This value if this value evaluates to True, otherwise 'other'.
        @raise MvKTypeError: If 'other' is not an instance of L{NumericValue}.
        """
        raise NotImplementedError()

    def __neg__(self):
        """
        Returns the negation of this value.
        @rtype: L{NumericValue}
        @return: The negation of this value.
        """
        raise NotImplementedError()

    def __pos__(self):
        """
        Returns this value.
        @rtype: L{NumericValue}
        @return: This value.
        """
        raise NotImplementedError()

    def __abs__(self):
        """
        Returns the absolute value of this value.
        @rtype: L{NumericValue}
        @return: The absolute value of this value.
        """
        raise NotImplementedError()

    def __lt__(self, other):
        """
        The < operator.
        @rtype: L{BooleanValue<mvk.interfaces.datavalue.BooleanValue>}
        @return: BooleanValue(True) if this < other, else BooleanValue(False).
        @raise MvKTypeError: If 'other' is not an instance of L{NumericValue}.
        """
        raise NotImplementedError()

    def __le__(self, other):
        """
        The <= operator.
        @rtype: L{BooleanValue<mvk.interfaces.datavalue.BooleanValue>}
        @return: BooleanValue(True) if this <= other, else BooleanValue(False).
        @raise MvKTypeError: if 'other' is not an instance of L{NumericValue}.
        """
        raise NotImplementedError()

    def __gt__(self, other):
        """
        The > operator.
        @rtype: L{BooleanValue<mvk.interfaces.datavalue.BooleanValue>}
        @return: BooleanValue(True) if this > other, else BooleanValue(False).
        @raise MvKTypeError: if 'other' is not an instance of L{NumericValue}.
        """
        raise NotImplementedError()

    def __ge__(self, other):
        """
        The >= operator.
        @rtype: L{BooleanValue<mvk.interfaces.datavalue.BooleanValue>}
        @return: BooleanValue(True) if this >= other, else BooleanValue(False).
        @raise MvKTypeError: if 'other' is not an instance of L{NumericValue}.
        """
        raise NotImplementedError()

    def floor(self):
        """
        Returns the largest integral value that is smaller than
        or equal to this value.
        @rtype: L{FloatValue}
        @return: The largest integral value that is smaller than or equal to
                 this value.
        """
        raise NotImplementedError()

    def ceil(self):
        """
        Returns the smallest integer value that is larger than
        or equal to this value.
        @rtype: L{IntegerValue}
        @return: The smallest integral value that is larger than or equal
                 to this value.
        """
        raise NotImplementedError()

    def trunc(self):
        """
        Returns the largest integral value that is smaller than
        or equal to this value.
        @rtype: L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}
        @return: the largest integral value that is smaller than
                 or equal to this value.
        """
        raise NotImplementedError()

    def nonzero(self):
        """
        Test for 'trueness'.
        @rtype: L{BooleanValue}
        @return: BooleanValue(True) if this value differs from 0,
                 else BooleanValue(False).
        """
        raise NotImplementedError()


class BooleanValue(NumericValue):
    pass


class IntegerValue(NumericValue):
    pass


class EnumValue(IntegerValue):
    pass


class FloatValue(NumericValue):
    pass


class InfiniteValue(FloatValue):
    """ -inf is smaller than any other number, and +inf is larger than
    any other value. Any arithmetical operation defined on numeric values
    should be well-defined. """
    pass


class StringValue(HashableValue):
    def count(self, a_str):
        """
        Counts the number of occurences of 'a_str' in this value.
        @type a_str: L{StringValue}
        @param a_str: A string.
        @rtype: L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}
        @return: The number of times 'a_str' occurs in this value.
        @raise MvKTypeError: If 'a_str' is not a L{StringValue}.
        """
        raise NotImplementedError()

    def find(self, a_str, start=None, end=None):
        """
        Returns the index of the substring 'a_str' in this value.
        The search starts at the left end of the string.
        @type a_str: L{StringValue}
        @param a_str: A string.
        @type start: L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}
        @param start: (OPTIONAL) The index to start looking.
        @type end: L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}
        @param end: (OPTIONAL) The index to stop looking.
        @rtype: L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}
        @return: the index of the substring 'a_str' in this value.
        @raise MvKTypeError: If 'a_str' is not a L{StringValue}.
        """
        raise NotImplementedError()

    def rfind(self, a_str, start=None, end=None):
        """
        Returns the index of the substring 'a_str' in this value.
        The search starts at the right end of the string.
        @type a_str: L{StringValue}
        @param a_str: A string.
        @type start: L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}
        @param start: (OPTIONAL) The index to start looking.
        @type end: L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}
        @param end: (OPTIONAL) The index to stop looking.
        @rtype: L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}
        @return: The index of the substring 'a_str' in this value.
        @raise MvKTypeError: If 'a_str' is not a L{StringValue}.
        """
        raise NotImplementedError()

    def replace(self, from_str, to_str, max_replacements=None):
        """
        Replaces all occurrences of 'from_str' with 'to_str'. If
        the optional parameter 'max_replacements' is passed, only performs
        the replacement this amount of times.
        @type from_str: L{StringValue}
        @param from_str: A string.
        @type to_str: L{StringValue}
        @param to_str: A string.
        @type max_replacements: L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}
        @param max_replacements: (OPTIONAL) An integer, specifying the
                                 number of times the source string should be
                                 replaced with the destination string.
        @rtype: L{StringValue}
        @return: The result of replacing the string 'from_str' with the
                 string 'to_str', 'max_replacements' number of times.
        @raise MvKTypeError: If 'from_str' or 'to_str' is not a L{StringValue},
                              or when 'max_replacements' is passed and it is not
                              an L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}.
        """
        raise NotImplementedError()

    def strip(self, chars=None):
        """
        Return a copy of the string with leading and trailing characters removed.
        If 'chars' is omitted or None, whitespace characters are removed.
        If given and not None, the characters in the string will be stripped
        from the both ends of this value.
        @type chars: L{StringValue}
        @param chars: (OPTIONAL) A string.
        @rtype: L{StringValue}
        @return: the result of stripping the characters in 'chars'
                 from both ends of this value.
        @raise MvKTypeError: If 'chars' is passed and is not a L{StringValue}.
        """
        raise NotImplementedError()

    def rstrip(self, chars=None):
        """
        Return a copy of the string with trailing characters removed.
        If 'chars' is omitted or None, whitespace characters are removed.
        If given and not None, the characters in the string will be stripped
        from the end of this value.
        @type chars: L{StringValue}
        @param chars: (OPTIONAL) A string.
        @rtype: L{StringValue}
        @return: The result of stripping the characters in 'chars'
                 from the end of this value.
        @raise MvKTypeError: If 'chars' is passed and is not a L{StringValue}.
        """
        raise NotImplementedError()

    def lstrip(self, chars=None):
        """
        Return a copy of the string with leading characters removed.
        If 'chars' is omitted or None, whitespace characters are removed.
        If given and not None, chars must be a StringValue; the characters in
        the string will be stripped from the beginning of the StringValue
        this method is called on.
        @type chars: L{StringValue}
        @param chars: (OPTIONAL) A string.
        @rtype: L{StringValue}
        @return: The result of stripping the characters in 'chars'
                 from the beginning of this value.
        @raise MvKTypeError: If 'chars' is passed and is not a L{StringValue}.
        """
        raise NotImplementedError()

    def split(self, sep=None, max_splits=None):
        """
        Return a list of the words of this string. If the optional second
        argument 'sep' is absent or None, the words are separated by arbitrary
        strings of whitespace characters (space, tab, newline, return,
        formfeed). If the second argument 'sep' is present and not None,
        it specifies a string to be used as the word separator. The
        returned list will then have one more item than the number of
        non-overlapping occurrences of the separator in the string.
        If 'max_splits' is given, at most max_splits number of splits occur,
        and the remainder of the string is returned as the final element of
        the list (thus, the list will have at most max_splits+1 elements).
        If 'max_splits' is not specified or -1, then there is no limit on the
        number of splits (all possible splits are made).

        The behavior of split on an empty string depends on the value of 'sep'.
        If 'sep' is not specified, or specified as None, the result will be an
        empty list. If 'sep' is specified as any string, the result will be a
        list containing one element which is an empty string.
        @type sep: L{StringValue}
        @param sep: (OPTIONAL) Separator.
        @type max_splits: L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}
        @param max_splits: (OPTIONAL) Specifies how many splits can be made.
        @rtype: L{SequenceValue<mvk.interfaces.datavalue.SequenceValue>}
        @return: The splitted string.
        @raise MvKTypeError: If 'sep' is passed, but is not a L{StringValue},
                             or if 'max_splits' is passed, but is not an
                             L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}.
        """
        raise NotImplementedError()

    def rsplit(self, sep=None, max_splits=None):
        """
        Return a list of the words of this string, scanning it from the end.
        To all intents and purposes, the resulting list of words is the same
        as returned by split(), except when the optional third argument
        'max_splits' is explicitly specified and nonzero. If 'max_splits'
        is given, at most max_splits number of splits - the rightmost ones -
        occur, and the remainder of the string is returned as the first element
        of the list (thus, the list will have at most max_splits+1 elements).
        @type sep: L{StringValue}
        @param sep: Optional separator.
        @type max_splits: L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}
        @param max_splits: Optional maximum number of splits.
        @rtype: L{SequenceValue<mvk.interfaces.datavalue.SequenceValue>}
        @return: The splitted string.
        @raise MvKTypeError: If 'sep' is passed, but is not a L{StringValue},
                             or if 'max_splits' is passed, but is not an
                             L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}.
        """
        raise NotImplementedError()

    def substring(self, start=None, stop=None):
        """
        Returns a substring of this string, starting at the character on
        position 'start' (inclusive) and ending on chraceter 'end' (exclusive).
        @type start: L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}
        @param start: Optional start index.
        @type stop: L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}
        @param stop: Optional end index.
        @rtype: L{StringValue}
        @return: The substring.
        @raise MvKTypeError: If 'start' is passed, but is not an
                             L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>},
                             or if 'stop' is passed, but is not an
                             L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}.
        """
        raise NotImplementedError()

    def startswith(self, prefix, start=None, stop=None):
        """
        Return True if string starts with the prefix, otherwise return False.
        With optional start, test string beginning at that position. With
        optional end, stop comparing string at that position.
        @type prefix: L{StringValue}
        @param prefix: The prefix to look for.
        @type start: L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}
        @param start: Optional start index.
        @type stop: L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}
        @param stop: Optional end index.
        @rtype: L{BooleanValue<mvk.interfaces.datavalue.BooleanValue>}
        @return: True if string starts with the prefix, otherwise return False.
        @raise MvKTypeError: If prefix is not a L{StringValue}, or
                             if 'start' is passed, but is not an
                             L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>},
                             or if 'stop' is passed, but is not an
                             L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}.
        """
        raise NotImplementedError()

    def lower(self):
        """
        Return a copy of this string with all the cased characters
        converted to lowercase.
        @rtype: L{StringValue}
        @return: A copy of this string with all the cased characters
                 converted to lowercase.
        """
        raise NotImplementedError()

    def upper(self):
        """
        Return a copy of this string with all the cased characters
        converted to uppercase.
        @rtype: L{StringValue}
        @return: A copy of this string with all the cased characters
                 converted to lowercase.
        """
        raise NotImplementedError()

    def swapcase(self):
        """
        Return a copy of the string with uppercase characters converted to
        lowercase and vice versa.
        @rtype: L{StringValue}
        @return: A copy of this string with uppercase characters
                 converted to lowercase and vice versa.
        """
        raise NotImplementedError()

    def title(self):
        """
        Return a titlecased version of this string where words start with an
        uppercase character and the remaining characters are lowercase.
        @rtype: L{StringValue}
        @return: A titlecased version of this string where words start with an
                 uppercase character and the remaining characters are lowercase.
        """
        raise NotImplementedError()

    def capitalize(self):
        """
        Return a copy of this string with its first character capitalized and
        the rest lowercased.
        @rtype: L{StringValue}
        @return: A copy of this string with its first character
                 capitalized and the rest lowercased.
        """
        raise NotImplementedError()

    def len(self):
        """
        Returns the length of this string.
        @rtype: L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}
        @return: The length of this string.
        """
        raise NotImplementedError()

    def __add__(self, other):
        """
        Returns the concatenation of this string with the string 'other'.
        @type other: L{StringValue}
        @param other: A string.
        @rtype: L{StringValue}
        @return: The concatenation of this string with 'other'.
        @raise MvKTypeError: If 'other' is not a L{StringValue}.
        """
        raise NotImplementedError()


class LocationValue(StringValue):
    pass


class CompositeValue(DataValue):
    def len(self):
        """
        Returns the length of this value.
        @rtype: L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}
        @return: The length of this value.
        """
        raise NotImplementedError()

    def __iter__(self):
        """
        Returns an iterator over this value.
        @rtype: L{Iterator<mvk.interfaces.datavalue.Iterator>}
        @return: An iterator over this value.
        """
        raise NotImplementedError()

    def __contains__(self, key):
        """
        Returns BooleanValue(True) if 'key' is in this value,
        else BooleanValue(False).
        @type key: L{Element<mvk.interfaces.element.Element>}
        @param key: An element.
        @rtype: L{BooleanValue<mvk.interfaces.datavalue.BooleanValue>}
        @return: BooleanValue(True) if 'key' is in this value,
                 else BooleanValue(False)
        """
        raise NotImplementedError()


class TupleValue(CompositeValue, HashableValue):
    def __getitem__(self, index):
        """
        Returns the item at the corresponding index.
        @type index: L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}
        @param index: An integer.
        @rtype: L{Element<mvk.interfaces.element.Element>}
        @return: The item in this value at index 'index'.
        @raise MvKTypeError: If 'index' is not an 
                             L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}
        @raise MvKIndexError: If the index is out of the range of this value.
        """
        raise NotImplementedError()


class SequenceValue(CompositeValue):
    def __getitem__(self, index):
        """
        Returns the item at the corresponding index.
        @type index: L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}
        @param index: An integer.
        @rtype: L{Element<mvk.interfaces.element.Element>}
        @return: The item in this value at index 'index'.
        @raise MvKTypeError: If 'index' is not an 
                             L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}
        @raise MvKIndexError: If the index is out of the range of this value.
        """
        raise NotImplementedError()

    def __setitem__(self, index, item):
        """
        Sets the value at index 'index' to 'item'.
        @type index: L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}
        @param index: An integer.
        @type item: L{Element<mvk.interfaces.element.Element>}
        @param item: An item.
        @raise MvKTypeError: If 'index' is not an 
                             L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}
        @raise MvKIndexError: If the index is out of the range of this value.
        """
        raise NotImplementedError()

    def __delitem__(self, index):
        """
        Deletes the item at an index.
        @type index: L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}
        @param index: An integer.
        @raise MvKTypeError: If 'index' is not an 
                             L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}.
        @raise MvKIndexError: If the index is out of the range of this value.
        """
        raise NotImplementedError()

    def append(self, x):
        """
        Appends an item to this value.
        @type x: L{Element<mvk.interfaces.element.Element>}
        @param x: An item.
        """
        raise NotImplementedError()

    def extend(self, x):
        """
        Extends the list with the elements of a composite value.
        @type x: L{CompositeValue<mvk.interfaces.datavalue.CompositeValue>}
        @param x: A composite value.
        @raise MvKTypeError: If 'x' is not a 
                             L{CompositeValue<mvk.interfaces.datavalue.CompositeValue>}.
        """
        raise NotImplementedError()

    def count(self, x):
        """
        Returns the number of times the element 'x' is found in this list.
        @type x: L{Element<mvk.interfaces.element.Element>}
        @param x: An element.
        @rtype: L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}
        @return: The number of times the element 'x' is found in this list.
        """
        raise NotImplementedError()

    def index(self, value, start, stop):
        """
        Returns  the index in the list of the first item whose value is 'value'.
        @type value: L{Element<mvk.interfaces.element.Element>}
        @param value: An element.
        @type start: L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}
        @param start: (OPTIONAL) The index on which to start the search.
        @type stop: L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}
        @param stop: (OPTIONAL) The index on which to end the search.
        @rtype: L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}
        @return: The index in the list of the first item whose value is 'value'.
        @raise MvKTypeError: If start or stop are given and are not an
                             L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}.
        @raise MvKValueError: If the value was not found.
        """
        raise NotImplementedError()

    def insert(self, index, x):
        """
        Inserts a value at a specific index.
        @type index: L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}
        @param index: the index on which to insert the element
        @type x: L{Element<mvk.interfaces.element.Element>}
        @param x: An element.
        @raise MvKTypeError: If 'index' is not a
                             L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}.
        """
        raise NotImplementedError()

    def pop(self):
        """
        Removes and returns the last item of this list.
        @rtype: L{Element<mvk.interfaces.element.Element>}
        @return: The last item of this list.
        @raise MvKIndexError: If called on an empty list.
        """
        raise NotImplementedError()

    def remove(self, x):
        """
        Remove the first item from the list whose value is 'x'.
        @type x: L{Element<mvk.interfaces.element.Element>}
        @param x: An element.
        @raise MvKValueError: If 'x' is not found in this list.
        """
        raise NotImplementedError()

    def reverse(self):
        """
        Reverses the elements of the list, in place.
        """
        raise NotImplementedError()

    def sort(self):
        """
        Sort the items of the list, in place.
        """
        raise NotImplementedError()

    def __add__(self, other):
        """
        Returns the concatenation of this list with the list 'other'.
        @type other: L{SequenceValue}
        @param other: A list.
        @rtype: L{SequenceValue}
        @return: The concatenation of this list with 'other'.
        @raise MvKTypeError: If 'other' is not a L{SequenceValue}.
        """
        raise NotImplementedError()


class SetValue(CompositeValue):
    def add(self, element):
        """
        Adds an element to this set.
        @type element: L{HashableValue<mvk.interfaces.datavalue.HashableValue>}
        @param element: A hashable value.
        @raise MvKTypeError: If 'element' is not a HashableValue.
        """
        raise NotImplementedError()

    def remove(self, element):
        """
        Removes an element from this set.
        @type element: L{HashableValue<mvk.interfaces.datavalue.HashableValue>}
        @param element: A hashable value.
        @raise MvKTypeError: If 'element' is not a HashableValue.
        @raise MvKKeyError: If 'element' is not found in this set.
        """
        raise NotImplementedError()

    def union(self, setvalue):
        """
        Return a new set with elements from both this and the passed set.
        @type setvalue: L{SetValue}
        @param setvalue: A set.
        @rtype: L{SetValue}
        @return: A new SetValue with elements from both this and the passed set.
        @raise MvKTypeError: If 'setvalue' is not a SetValue.
        """
        raise NotImplementedError()

    def difference(self, setvalue):
        """
        Return a new set with elements in this set that are not in the other.
        @type setvalue: L{SetValue}
        @param setvalue: A set.
        @rtype: L{SetValue}
        @return: A new set with elements in this set that are not in the other.
        @raise MvKTypeError: If 'setvalue' is not a SetValue.
        """
        raise NotImplementedError()

    def symmetric_difference(self, setvalue):
        """
        Return a new set with elements that are in either set, but not in both.
        @type setvalue: L{SetValue}
        @param setvalue: A set.
        @rtype: L{SetValue}
        @return: A new set with elements that are in either set, but not in both.
        @raise MvKTypeError: If 'setvalue' is not a SetValue.
        """
        raise NotImplementedError()

    def intersection(self, setvalue):
        """
        Return a new set with elements common to both sets.
        @type setvalue: L{SetValue}
        @param setvalue: A set
        @rtype: L{SetValue}
        @return: A new SetValue with elements common to both sets.
        @raise MvKTypeError: If 'setvalue' is not a SetValue.
        """
        raise NotImplementedError()

    def issubset(self, setvalue):
        """
        Test whether every element in this set is in the other.
        @type setvalue: L{SetValue}
        @param setvalue: A set.
        @rtype: L{BooleanValue<mvk.interfaces.datavalue.BooleanValue>}
        @return: BooleanValue(True) if every element in this SetValue is in
                 the other, else BooleanValue(False).
        @raise MvKTypeError: If 'setvalue' is not a SetValue.
        """
        raise NotImplementedError()

    def issuperset(self, setvalue):
        """
        Test whether every element in 'setvalue' is in this set.
        @type setvalue: L{SetValue}
        @param setvalue: A set.
        @rtype: L{BooleanValue<mvk.interfaces.datavalue.BooleanValue>}
        @return: BooleanValue(True) if every element in 'setvalue' is in
                 this SetValue, else BooleanValue(False).
        @raise MvKTypeError: If 'setvalue' is not a SetValue.
        """
        raise NotImplementedError()


class MappingValue(CompositeValue):
    def keys(self):
        """
        Returns the collection of keys of this dictionary.
        @rtype: L{CompositeValue<mvk.interfaces.datavalue.CompositeValue>}
        @return: A composite value, containing the keys of this dictionary.
        """
        raise NotImplementedError()

    def values(self):
        """
        Returns the collection of values of this dictionary.
        @rtype: L{CompositeValue<mvk.interfaces.datavalue.CompositeValue>}
        @return: A composite value, containing the values of this dictionary.
        """
        raise NotImplementedError()

    def __getitem__(self, key):
        """
        Returns the item of this dictionary with key 'key'.
        @type key: L{HashableValue<mvk.interfaces.datavalue.HashableValue>}
        @param key: A hashable value.
        @rtype: L{Element<mvk.interfaces.element.Element>}
        @return: The item of this MappingValue with key 'key'.
        @raise MvKTypeError: If 'key' is not a HashableValue.
        @raise MvKKeyError: If the key was not found.
        """
        raise NotImplementedError()

    def __setitem__(self, key, val):
        """
        Sets the item with key 'key' to the passed value.
        @type key: L{HashableValue<mvk.interfaces.datavalue.HashableValue>}
        @param key: A hashable value.
        @type val: L{Element<mvk.interfaces.element.Element>}
        @param val: An element.
        @raise MvKTypeError: If 'key' is not a HashableValue.
        """
        raise NotImplementedError()

    def __delitem__(self, key):
        """
        Removes the item of this dictionary with key 'key'.
        @type key: L{HashableValue<mvk.interfaces.datavalue.HashableValue>}
        @param key: A hashable value.
        @raise MvKTypeError: If 'key' is not a HashableValue.
        @raise MvKKeyError - If the key was not found.
        """
        raise NotImplementedError()

    def clear(self):
        """
        Clears all keys and values from this MappingValue.
        """
        raise NotImplementedError()

    def pop(self, key, default=None):
        """
        If 'key' is in the dictionary, remove it and return its value,
        else return 'default'.
        @type key: L{HashableValue<mvk.interfaces.datavalue.HashableValue>}
        @param key: A hashable value.
        @type default: L{Element<mvk.interfaces.element.Element>}
        @param default - (OPTIONAL) A default return value.
        @rtype: L{Element<mvk.interfaces.element.Element>}
        @return: The item of this dictionary with key 'key', if 'key' is
                 in this dictionary, else 'default'
        @raise MvKTypeError: If 'key' is not a HashableValue.
        @raise MvKKeyError: If 'key' is not in the MappingValue and 'default' is not given.
        """
        raise NotImplementedError()


class Iterator(Element):
    def has_next(self):
        """
        Test whether the iterator has a next element.
        @rtype: L{BooleanValue<mvk.interfaces.datavalue.BooleanValue>}
        @return: BooleanValue(True) if there is a next elememt, else BooleanValue(False).
        """
        raise NotImplementedError()

    def next(self):
        """
        Returns the next element, if there is one.
        @rtype: L{Element<mvk.interfaces.element.Element>}
        @return: The next element of this Iterator.
        @raise MvKStopIteration: If there is no next element.
        """
        raise NotImplementedError()


class ImmutableCompositeValue(CompositeValue):
    pass


class ImmutableSequenceValue(SequenceValue, ImmutableCompositeValue):
    def __setitem__(self, index, item):
        """
        @raise MvKTypeError: Always, unsupported operation.
        """
        raise NotImplementedError()

    def __delitem__(self, index):
        """
        @raise MvKTypeError: Always, unsupported operation.
        """
        raise NotImplementedError()

    def append(self, x):
        """
        @raise MvKTypeError: Always, unsupported operation.
        """
        raise NotImplementedError()

    def extend(self, x):
        """
        @raise MvKTypeError: Always, unsupported operation.
        """
        raise NotImplementedError()

    def insert(self, index, x):
        """
        @raise MvKTypeError: Always, unsupported operation.
        """
        raise NotImplementedError()

    def pop(self):
        """
        @raise MvKTypeError: Always, unsupported operation.
        """
        raise NotImplementedError()

    def remove(self, x):
        """
        @raise MvKTypeError: Always, unsupported operation.
        """
        raise NotImplementedError()

    def reverse(self):
        """
        @raise MvKTypeError: Always, unsupported operation.
        """
        raise NotImplementedError()

    def sort(self):
        """
        @raise MvKTypeError: Always, unsupported operation.
        """
        raise NotImplementedError()


class ImmutableSetValue(SetValue, ImmutableCompositeValue):
    def add(self, element):
        """
        @raise MvKTypeError: Always, unsupported operation.
        """
        raise NotImplementedError()

    def remove(self, element):
        """
        @raise MvKTypeError: Always, unsupported operation.
        """
        raise NotImplementedError()


class ImmutableMappingValue(MappingValue, ImmutableCompositeValue):
    def __setitem__(self, key, val):
        """
        @raise MvKTypeError: Always, unsupported operation.
        """
        raise NotImplementedError()

    def __delitem__(self, key):
        """
        @raise MvKTypeError: Always, unsupported operation.
        """
        raise NotImplementedError()

    def clear(self):
        """
        @raise MvKTypeError: Always, unsupported operation.
        """
        raise NotImplementedError()

    def pop(self, key, default=None):
        """
        @raise MvKTypeError: Always, unsupported operation.
        """
        raise NotImplementedError()
