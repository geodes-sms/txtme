"""
Created on 28-dec.-2013

@author: Simon
"""
from mvk.interfaces.datatype import Type
from mvk.interfaces.element import NamedElement, TypedElement, Element


class Package(NamedElement):
    """
    A package groups elements (NamedElement). It is the parent of all its
    owned elements.
    """
    def get_elements(self):
        """
        Returns a collection of elements contained in this package.
        @rtype: L{CompositeValue<mvk.interfaces.datavalue.CompositeValue>}
        @return: All elements contained in this package.
        """
        raise NotImplementedError()

    def get_element(self, name):
        """
        Returns the element with a given name.
        @type name: L{StringValue<mvk.interfaces.datavalue.StringValue>}
        @param name: The name of the element.
        @rtype: L{NamedElement<mvk.element.NamedElement>}
        @return: The element with given name, if it is present.
        @raises MvKLookupError: When the element is not found.
        """
        raise NotImplementedError()


class Node(Type, NamedElement):
    def get_potency(self):
        """
        Returns the potency value of this node.
        @rtype: L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>} or
                L{InfiniteValue<mvk.interfaces.datavalue.InfiniteValue>}
        @return: The potency value of this model.
        """
        raise NotImplementedError()

    def get_attributes(self):
        """
        Returns this node's attributes.
        @rtype: L{SequenceValue<mvk.interfaces.datavalue.SequenceValue>}
        @return: All attributes of this class.
        """
        raise NotImplementedError()

    def get_attribute(self, attr_name):
        """
        Returns the attribute with a specific location.
        @type attr_name: L{StringValue<mvk.interfaces.datavalue.StringValue>}
        @param attr_name: The name of the attribute.
        @rtype: L{Attribute<mvk.interfaces.object.Attribute>}
        @return: The attribute with given name.
        @raise L{MvKKeyError<mvk.interfaces.exception.MvKKeyError>}: If the
        attribute with given name is not defined for this node.
        """
        raise NotImplementedError()

    def get_functions(self):
        """
        Returns this node's functions.
        @rtype: L{MappingValue<mvk.interfaces.datavalue.MappingValue>}
        @return: All attributes of this class.
        """
        raise NotImplementedError()

    def get_function(self, f_name):
        """
        Returns the function with a specific name.
        @type attr_name: L{StringValue<mvk.interfaces.datavalue.StringValue>}
        @param attr_name: The name of the function.
        @rtype: L{Function<mvk.interfaces.action.Function>}
        @return: The function with given name.
        @raise L{MvKKeyError<mvk.interfaces.exception.MvKKeyError>}: If the
        function with given name is not defined for this node.
        """
        raise NotImplementedError()

    def get_out_associations(self):
        """
        Returns the outgoing associations defined for this node.
        @rtype: L{CollectionValue<mvk.interfaces.datavalue.CollectionValue>}
        @return: The outgoing associations defined for this node.
        """
        raise NotImplementedError()

    def get_in_associations(self):
        """
        Returns the incoming associations defined for this node.
        @rtype: L{CollectionValue<mvk.interfaces.datavalue.CollectionValue>}
        @return: The incoming associations defined for this node.
        """
        raise NotImplementedError()

    def get_outgoing_elements(self):
        """
        Returns the elements connected to this node through an outgoing association.
        @rtype: L{CollectionValue<mvk.interfaces.datavalue.CollectionValue>}
        @return: The elements connected to this node through an outgoing association.
        """
        raise NotImplementedError()

    def get_incoming_elements(self):
        """
        Returns the elements connected to this node through an incoming association.
        @rtype: L{CollectionValue<mvk.interfaces.datavalue.CollectionValue>}
        @return: The elements connected to this node through an incoming association.
        """
        raise NotImplementedError()

    def get_neighbors(self):
        """
        Returns the elements connected to this node through either an
        incoming or outgoing association.
        @rtype: L{CollectionValue<mvk.interfaces.datavalue.CollectionValue>}
        @return: The elements connected to this node through either an
        incoming or outgoing association.
        """
        raise NotImplementedError()


class Model(Node, Package):
    """ A model is a package, and can also act as a type for other models. """
    pass


class ModelReference(Model):
    def dereference(self):
        """
        Returns the model this reference points to.
        @rtype: L{Model<mvk.interfaces.object.Model>}
        @return: The model this reference points to.
        """
        raise NotImplementedError()

    def get_path(self):
        """
        Returns this reference's path.
        @rtype: L{LocationValue<mvk.interfaces.datavalue.LocationValue>}
        @return: This reference's path.
        """
        raise NotImplementedError()


class Multiplicity(Element):
    def get_lower(self):
        """
        Returns the lower bound of this multiplicity.
        @rtype: L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}
        @return: The lower bound of this multiplicity.
        @raise L{MvKPotencyError<mvk.interfaces.exception.MvKPotencyError>}: If
        the potency value is 0.
        """
        raise NotImplementedError()

    def get_upper(self):
        """
        Returns the upper bound of this multiplicity.
        @rtype: L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}
        @return: The upper bound of this multiplicity.
        @raise L{MvKPotencyError<mvk.interfaces.exception.MvKPotencyError>}: If
        the potency value is 0.
        """
        raise NotImplementedError()

    def is_ordered(self):
        """
        Returns True of this multiplicity is ordered, else False.
        @rtype: L{BooleanValue<mvk.interfaces.datavalue.BooleanValue>}
        @return: Wheter or not this multiplicity is ordered.
        @raise L{MvKPotencyError<mvk.interfaces.exception.MvKPotencyError>}: If
        the potency value is 0.
        """
        raise NotImplementedError()


class Clabject(Node, Multiplicity):
    def get_elements(self):
        """
        Returns a collection of elements contained in this clabject.
        @rtype: L{CompositeValue<mvk.interfaces.datavalue.CompositeValue>}
        @return: All elements contained in this clabject.
        """
        raise NotImplementedError()

    def get_element(self, name):
        """
        Returns the element with a given name.
        @type name: L{StringValue<mvk.interfaces.datavalue.StringValue>}
        @param name: The name of the element.
        @rtype: L{NamedElement<mvk.element.NamedElement>}
        @return: The element with given name, if it is present.
        @raises MvKLookupError: When the element is not found.
        """
        raise NotImplementedError()

    def is_abstract(self):
        """
        Returns True if this clabject is abstract, else False.
        @rtype: L{BooleanValue<mvk.interfaces.datavalue.BooleanValue>}
        @return: Wheter or not this clabject is abstract.
        @raise L{MvKPotencyError<mvk.interfaces.exception.MvKPotencyError>}: If
        the potency value is 0.
        """
        raise NotImplementedError()

    def get_specialise_classes(self):
        """
        Returns classes that specialize this class.
        @rtype: L{CompositeValue<mvk.interfaces.datavalue.CompositeValue>}
        @return: All classes that specialize this class.
        @raise L{MvKPotencyError<mvk.interfaces.exception.MvKPotencyError>}: If
        the potency value is 0.
        """
        raise NotImplementedError()

    def get_super_classes(self):
        """
        Returns all superclasses of this class.
        @rtype: L{CompositeValue<mvk.interfaces.datavalue.CompositeValue>}
        @return: This class's superclasses.
        @raise L{MvKPotencyError<mvk.interfaces.exception.MvKPotencyError>}: If
        the potency value is 0. 
        """
        raise NotImplementedError()

    def get_all_specialise_classes(self):
        """
        Returns classes that specialize this class (recursive). This includes
        the classes that specialize this class's specialize classes, their
        specializations, and so forth.
        @rtype: L{CompositeValue<mvk.interfaces.datavalue.CompositeValue>}
        @return: All classes that specialize this class (recursive).
        @raise L{MvKPotencyError<mvk.interfaces.exception.MvKPotencyError>}: If
        the potency value is 0.
        """
        raise NotImplementedError()

    def get_all_super_classes(self):
        """
        Returns the superclasses of this class (recursive). This includes
        the superclass of this class's superclasses, their superclass,
        and so forth.
        @rtype: L{CompositeValue<mvk.interfaces.datavalue.CompositeValue>}
        @return: All superclasses of this class (recursive).
        @raise L{MvKPotencyError<mvk.interfaces.exception.MvKPotencyError>}: If
        the potency value is 0.
        """
        raise NotImplementedError()

    def get_all_attributes(self):
        """
        Returns this class's attributes (recursive). This includes all
        attributes of all the superclasses of this class.
        @rtype: L{MappingValue<mvk.interfaces.datavalue.MappingValue>}
        @return: All attributes of this class (recursive).
        """
        raise NotImplementedError()

    def issubclass(self, other):
        """
        Returns True if this class is a subclass of the other class, else False.
        @rtype: L{BooleanValue<mvk.interfaces.datavalue.BooleanValue>}
        @return: True if this class is a subclass of the other class, else False.
        @raise L{MvKPotencyError<mvk.interfaces.exception.MvKPotencyError>}: If
        the potency value is 0.
        """
        raise NotImplementedError()

    def issuperclass(self, other):
        """
        Returns True if this class is a subclass of the other class, else False.
        @rtype: L{BooleanValue<mvk.interfaces.datavalue.BooleanValue>}
        @return: True if this class is a subclass of the other class, else False.
        @raise L{MvKPotencyError<mvk.interfaces.exception.MvKPotencyError>}: If
        the potency value is 0.
        """
        raise NotImplementedError()

    def get_all_out_associations(self):
        """
        Returns the outgoing associations defined for this clabject and its
        super types.
        @rtype: L{CollectionValue<mvk.interfaces.datavalue.CollectionValue>}
        @return: The outgoing associations defined for this clabject.
        """
        raise NotImplementedError()

    def get_all_in_associations(self):
        """
        Returns the incoming associations defined for this clabject and its
        super types.
        @rtype: L{CollectionValue<mvk.interfaces.datavalue.CollectionValue>}
        @return: The outgoing associations defined for this clabject.
        """
        raise NotImplementedError()


class ClabjectReference(Clabject):
    def dereference(self):
        """
        Returns the clabject this reference points to.
        @rtype: L{Clabject<mvk.interfaces.object.Clabject>}
        @return: The clabject this reference points to.
        """
        raise NotImplementedError()

    def get_path(self):
        """
        Returns this reference's path.
        @rtype: L{LocationValue<mvk.interfaces.datavalue.LocationValue>}
        @return: This reference's path.
        """
        raise NotImplementedError()


class Attribute(Type, NamedElement, TypedElement, Multiplicity):
    def get_default(self):
        """
        Returns the default value of this attribute.
        @rtype: L{Element<mvk.interfaces.element.Element>}
        @return: The default value of this attribute.
        @raise L{MvKPotencyError<mvk.interfaces.exception.MvKPotencyError>}: If
        the potency value is 0.
        """
        raise NotImplementedError()

    def get_value(self):
        """
        Returns the actual value of this attribute.
        @rtype: L{Element<mvk.interfaces.element.Element>}
        @return: The actual value of this attribute.
        @raise L{MvKPotencyError<mvk.interfaces.exception.MvKPotencyError>}: If
        the potency value is not 0.
        """
        raise NotImplementedError()


class AssociationEnd(Multiplicity):
    def get_node(self):
        """
        Returns the node 'pointed to' by this association end.
        @rtype: L{Node<mvk.interfaces.object.Node>}
        @return The node 'pointed to' by this association end.
        """
        raise NotImplementedError()

    def get_port_name(self):
        """
        Returns the name of the port associated with this association end.
        @rtype: L{StringValue<mvk.interfaces.datavalue.StringValue>}
        @return: The port name of this association end.
        """
        raise NotImplementedError()


class Association(Clabject):
    def get_from_multiplicity(self):
        """
        Returns the multiplicity of the source of this association.
        @rtype: L{AssociationEnd<mvk.interfaces.object.AssociationEnd>}
        @return: The multiplicity of the source of this association.
        """
        raise NotImplementedError()

    def get_to_multiplicity(self):
        """
        Returns the multiplicity of the target of this association.
        @rtype: L{AssociationEnd<mvk.interfaces.object.AssociationEnd>}
        @return: The multiplicity of the target of this association.
        """
        raise NotImplementedError()


class AssociationReference(Association):
    def dereference(self):
        """
        Returns the association this reference points to.
        @rtype: L{Clabject<mvk.interfaces.object.Clabject>}
        @return: The clabject this reference points to.
        """
        raise NotImplementedError()

    def get_path(self):
        """
        Returns this reference's path.
        @rtype: L{LocationValue<mvk.interfaces.datavalue.LocationValue>}
        @return: This reference's path.
        """
        raise NotImplementedError()


class Composition(Association):
    pass


class Aggregation(Association):
    pass


class Inherits(Association):
    pass
