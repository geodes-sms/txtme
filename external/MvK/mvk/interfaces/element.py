"""
Created on 28-dec.-2013

@author: Simon
"""


class Element(object):
    """
    The top-level class, only defines an equality method, signifying that
    all elements in the metaverse can be tested on equality.
    """
    def __eq__(self, other):
        """
        Test for equality with any other element.
        @type other: L{Element}
        @param other: The element which we want to test equality with.
        @rtype: L{BooleanValue<mvk.interfaces.datavalue.BooleanValue>}
        @return: BooleanValue(True) if 'other' is equal to this element,
                 otherwise BooleanValue(False).
        """
        raise NotImplementedError()

    def __ne__(self, other):
        """
        Test for unequality with any other element.
        @type other: L{Element}
        @param other: The element which we want to test unequality with.
        @rtype: L{BooleanValue<mvk.interfaces.datavalue.BooleanValue>}
        @return: BooleanValue(True) if 'other' is not equal to this element,
                 otherwise BooleanValue(False).
        """
        raise NotImplementedError()

    def typed_by(self):
        """
        Returns the type by which this element is typed.
        @rtype: L{Type<mvk.interfaces.datatype.Type>}
        @return: The type by which this element is typed.
        """
        raise NotImplementedError()


class NamedElement(Element):
    """
    A named element has a name, and a location. Its location depends on its
    parent (which is a Package). If the element has no parent, its location
    equals its name. Otherwise, it should take into account the location
    of its parent.
    """
    def get_name(self):
        """
        Getter for the name attribute.
        @rtype: L{StringValue<mvk.interfaces.datavalue.StringValue>}
        @return: The name of this element.
        """
        raise NotImplementedError()

    def get_location(self):
        """
        Getter for the location of this element.
        @rtype: L{LocationValue<mvk.interfaces.datavalue.LocationValue>}
        @return: The location of this element.
        """
        raise NotImplementedError()

    def get_short_location(self):
        """
        Getter for the location of this element, restricted to its parent. So
        it is equal to <parent name>.<attribute name>
        @rtype: L{LocationValue<mvk.interfaces.datavalue.LocationValue>}
        @return: The short location of this element.
        """
        raise NotImplementedError()

    def get_parent(self):
        """
        Getter for the parent of this element.
        @rtype: L{NamedElement}
        @return: The parent of this element.
        """
        raise NotImplementedError()


class TypedElement(Element):
    """
    An element which is typed.
    """
    def get_type(self):
        """
        Getter for the type attribute.
        @rtype: L{Type<mvk.interfaces.datatype.Type>}
        @return: The type of this element.
        """
        raise NotImplementedError()
