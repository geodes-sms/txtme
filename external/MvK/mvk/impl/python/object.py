"""
Created on 28-dec.-2013

@author: Simon
"""
import logging
import traceback

from mvk.impl.python.changelog import MvKCreateLog, MvKReadLog, MvKCompositeLog, MvKDeleteLog, MvKUpdateLog, MvKCompositeLog, MvKCreateCompositeLog, LogConstants, MvKDeleteCompositeLog
from mvk.impl.python.constants import CreateConstants, ReadConstants, DeleteConstants, UpdateConstants
from mvk.impl.python.datatype import Type, PackageType
from mvk.impl.python.datavalue import ImmutableSequenceValue, IntegerValue, StringValue, InfiniteValue, BooleanValue, SequenceValue, ImmutableMappingValue, \
    MappingValue, LocationValue, SetValue
from mvk.impl.python.element import NamedElement, TypedElement, Element
from mvk.impl.python.exception import MvKKeyError, MvKTypeError, MvKNameError, MvKValueError, MvKPotencyError, MvKLookupError, MvKException, MvKParameterError
from mvk.interfaces.datatype import IntegerType, BooleanType, LocationType, StringType, InfiniteType
import mvk.interfaces.object
from mvk.util.logger import get_logger
from mvk.util.utility_functions import lists_eq_items

logger = get_logger('object')

def remove_cache(location):
    from mvk.mvk import MvK
    try:
        del MvK.read_cache[location]
    except KeyError:
        pass

class Package(NamedElement, mvk.interfaces.object.Package):
    """ === CONSTRUCTOR === """
    def __init__(self, **kwds):
        self.name_lookup = MappingValue(value={})
        self.my_type = PackageType()
        super(Package, self).__init__(**kwds)

    """ === PUBLIC INTERFACE === """
    def typed_by(self):
        return self.my_type

    def get_elements(self):
        return ImmutableMappingValue(self.name_lookup)

    def get_element(self, name):
        if not isinstance(name, mvk.interfaces.datavalue.StringValue):
            raise MvKTypeError(StringValue('Expected a StringValue, received a %s' % type(name)))
        try:
            return self.name_lookup[name]
        except KeyError:
            raise MvKNameError(StringValue('Element with name %s not found in package' % name))

    def __eq__(self, other):
        return (BooleanValue(id(self) == id(other)) or
                ((BooleanValue(isinstance(other, mvk.interfaces.object.Package))) and
                 (self.get_location() == other.get_location() or
                 (super(Package, self).__eq__(other) and
                  self.get_elements() == other.get_elements()))))

    """ === PYTHON SPECIFIC === """
    def set_name(self, name):
        old_name = self.get_name()
        if old_name != name:
            super(Package, self).set_name(name)
            if self.get_parent() is not None:
                self.get_parent().update_element(old_name, self)

    def add_element(self, element):
        '''
        Adds an element to this model. Automatically sets the parent
        of the newly added element to this model.
        @type element: L{NamedElement<mvk.interfaces.element.NamedElement>}
        @param element: A named element.
        @raise MvKNameError: If an element with the same name already exists.
        '''
        assert isinstance(element, mvk.interfaces.element.NamedElement)
        if element.get_name() in self.name_lookup:
            raise MvKNameError(StringValue('An element with name %s already \
                                            exists in package %s.' %
                                            (element.get_name(), self.get_name())))
        self.name_lookup[element.get_name()] = element
        element.set_parent(self)
        assert element.get_parent() == self

    def add_elements(self, elements):
        '''
        Adds a list of elements to this model.
        @type elements: list
        @param elements: A list of L{NamedElement<mvk.interfaces.element.NamedElement>}s.
        @raise MvKNameError: If one of the elements has the same name as an element in this package.
        '''
        names = SetValue(set([el.get_name() for el in elements]))
        name_check = names.intersection(self.name_lookup.keys())
        if not name_check.len() == IntegerValue(0):
            raise MvKNameError(StringValue('Elements with name(s) %s already \
                                            exist in package %s.' %
                                            (name_check, self.get_name())))
        for el in elements:
            self.add_element(el)

    def remove_element(self, name):
        '''
        Removes the element with given name from this model. It is an error
        if no element with the given name exists in the model. Also sets the
        parent of the removed element to None.
        @type name: L{StringValue<mvk.interfaces.datavalue.StringValue>}
        @param name: The name of the element to be removed from this model.
        @raise MvKKeyError: If the element with given name was not found in
        this model.
        '''
        import mvk.interfaces.datavalue
        assert (isinstance(name, mvk.interfaces.datavalue.StringValue) and
                isinstance(name.typed_by(), mvk.interfaces.datatype.StringType))
        assert logger.debug('Removing element %s from package %s.' %
                            (name, self.get_name()))
        if not name in self.name_lookup:
            raise MvKKeyError(StringValue('Element not found!'))
        self.name_lookup[name].set_parent(None)
        del self.name_lookup[name]

    def update_element(self, old_name, element):
        '''
        Removes the element with name 'old_name', and adds the given element.
        @type old_name: L{StringValue<mvk.interfaces.datavalue.StringValue>}
        @param old_name: The old name of the element.
        @type element: L{NamedElement<mvk.interfaces.element.NamedElement>}
        @raise MvKKeyError: If the element with name 'old_name' was not found.
        '''
        assert (isinstance(old_name, mvk.interfaces.datavalue.StringValue) and
                isinstance(old_name.typed_by(), mvk.interfaces.datatype.StringType))
        assert isinstance(element, NamedElement)
        ''' we do a check on the location, because 'element.get_parent() == self'
        would also return True if the contents are equal '''
        assert (element.get_parent() is None or
                element.get_parent().get_location() == self.get_location())
        if not old_name in self.name_lookup:
            raise MvKKeyError(StringValue('Element not found!'))
        if element.get_name() in self.name_lookup:
            raise MvKNameError(StringValue('Element with name %s already \
                                            exist in package %s.' %
                                            (element.get_name(), self.get_name())))
        del self.name_lookup[old_name]
        self.name_lookup[element.get_name()] = element

    """ === CRUD === """
    @classmethod
    def _check_params_create(cls, params):
        cl = MvKCreateLog()
        if not (isinstance(params, mvk.interfaces.datavalue.MappingValue) and
                isinstance(params.typed_by(), mvk.interfaces.datatype.MappingType)):
            cl.set_status_code(CreateConstants.MALFORMED_REQUEST_CODE)
            cl.set_status_message(StringValue('Expected a MappingValue'))
            return cl
        try:
            cls._check_param(params,
                             CreateConstants.LOCATION_KEY,
                             mvk.interfaces.datavalue.LocationValue,
                             mvk.interfaces.datatype.LocationType)
            cls._check_param(params,
                             CreateConstants.ATTRS_KEY,
                             mvk.interfaces.datavalue.MappingValue,
                             mvk.interfaces.datatype.MappingType)
            attributes = params[CreateConstants.ATTRS_KEY]
            cls._check_param(attributes,
                             StringValue('name'),
                             mvk.interfaces.datavalue.StringValue,
                             mvk.interfaces.datatype.StringType)
        except MvKException, e:
            cl.set_status_code(CreateConstants.BAD_REQUEST_CODE)
            cl.set_status_message(e.get_message())
            return cl
        return None

    @classmethod
    def _create(cls, params):
        from mvk.impl.python.python_representer import PythonRepresenter
        ''' Initialize needed changelog values. '''
        cl = MvKCreateLog()
        location = params[CreateConstants.LOCATION_KEY]
        physical_type = PythonRepresenter.PACKAGE
        cl.set_location(location)
        cl.set_type(physical_type)
        cl.set_status_code(CreateConstants.SUCCESS_CODE)
        cl.set_status_message(StringValue('Success!'))

        ''' Create the new package. '''
        attributes = params[CreateConstants.ATTRS_KEY]
        name = attributes[StringValue('name')]
        p = Package(name=name)
        cl.add_attr_change(StringValue('name'), p.get_name())
        cl.set_name(p.get_name())

        ''' Try setting the parent.  '''
        from mvk.mvk import MvK
        parent_log = MvK().read(location)
        ''' If the parent does not exist, create a package on that location. '''
        if not parent_log.is_success():
            splitted = location.rsplit(StringValue('.'), max_splits=IntegerValue(1))
            params = MappingValue({})
            params[CreateConstants.TYPE_KEY] = PythonRepresenter.PACKAGE
            c_attributes = MappingValue({})
            if splitted.len() == IntegerValue(1):
                ''' We're creating a package at the top level. '''
                params[CreateConstants.LOCATION_KEY] = LocationValue('')
                c_attributes[StringValue('name')] = splitted[IntegerValue(0)]
            else:
                ''' We're creating a package inside another package. '''
                params[CreateConstants.LOCATION_KEY] = splitted[IntegerValue(0)]
                c_attributes[StringValue('name')] = splitted[IntegerValue(1)]
            params[CreateConstants.ATTRS_KEY] = c_attributes
            ''' Actually create the package. '''
            create_log = MvK().create(params)
            if not create_log.is_success():
                ''' TODO: revert! '''
                cl.set_status_code(create_log.get_status_code())
                cl.set_status_message(create_log.get_status_message())
                return cl
            composite_log = MvKCreateCompositeLog()
            composite_log.add_log(create_log)
            composite_log.add_log(cl)
            composite_log.set_location(cl.get_location())
            composite_log.set_type(cl.get_type())
            cl = composite_log
            ''' The parent now exists! '''
            parent_log = MvK().read(location)
            if not parent_log.is_success():
                cl.set_status_code(LogConstants.INTERNAL_ERROR_CODE)
                cl.set_status_message(StringValue("Internal error: automatically created node does not exist!"))

        parent = parent_log.get_item()
        if not isinstance(parent, mvk.interfaces.object.Package):
            cl.set_status_code(CreateConstants.BAD_REQUEST_CODE)
            cl.set_status_message(StringValue('Can only create a Package \
                                               inside a Package.'))
        else:
            assert logger.debug('Adding new package %s to package %s.' %
                                (p.get_name(), parent.get_name()))
            try:
                parent.add_element(p)
                cl.set_status_code(CreateConstants.SUCCESS_CODE)
                cl.set_status_message(StringValue('Success'))
            except MvKNameError, e:
                cl.set_status_code(CreateConstants.BAD_REQUEST_CODE)
                cl.set_status_message(e.get_message())

        ''' Return changelog. '''
        return cl

    @classmethod
    def _check_params_update(cls, params):
        cl = MvKUpdateLog()
        if not (isinstance(params, mvk.interfaces.datavalue.MappingValue) and
                isinstance(params.typed_by(), mvk.interfaces.datatype.MappingType)):
            cl.set_status_code(UpdateConstants.MALFORMED_REQUEST_CODE)
            cl.set_status_message(StringValue('Expected a MappingValue'))
            return cl
        try:
            cls._check_param(params,
                             CreateConstants.ATTRS_KEY,
                             mvk.interfaces.datavalue.MappingValue,
                             mvk.interfaces.datatype.MappingType)
            attributes = params[CreateConstants.ATTRS_KEY]
            cls._check_param(attributes,
                             StringValue('name'),
                             mvk.interfaces.datavalue.StringValue,
                             mvk.interfaces.datatype.StringType,
                             req=None)
        except MvKException, e:
            cl.set_status_code(UpdateConstants.BAD_REQUEST_CODE)
            cl.set_status_message(e.get_message())
            return cl
        return None

    def _update(self, params):
        from mvk.impl.python.python_representer import PythonRepresenter
        cl = MvKUpdateLog()
        cl.set_type(PythonRepresenter.PACKAGE)

        attributes = params[UpdateConstants.ATTRS_KEY]
        for name in attributes:
            if name == StringValue('name'):
                new_val = attributes[name]
                cl.add_attr_change(name, self.get_name(), new_val)
                self.set_name(new_val)
            else:
                cl.set_location(self.get_location())
                cl.set_status_code(UpdateConstants.BAD_REQUEST_CODE)
                cl.set_status_message(StringValue('Don\'t know how to update package\'s physical attribute %s.' %
                                                  name))
                return cl

        ''' This second set_location in case name was changed. '''
        cl.set_location(self.get_location())
        cl.set_status_code(UpdateConstants.SUCCESS_CODE)
        cl.set_status_message(StringValue('Successfully updated Attribute.'))
        return cl

    def parent_renamed(self, old_path, new_path):
        self.location = None
        for elem in self.name_lookup:
            self.name_lookup[elem].parent_renamed(old_path, new_path)

    def read(self, location):
        from mvk.impl.python.python_representer import PythonRepresenter
        assert (isinstance(location, LocationValue) and
                isinstance(location.typed_by(), LocationType))

        assert logger.debug('Package.read %s' % location)

        rl = MvKReadLog()
        if location == LocationValue(''):
            ''' Base case. '''
            rl.set_item(self)
            rl.set_location(self.get_location())
            rl.set_type(PythonRepresenter.PACKAGE)
            rl.set_status_code(ReadConstants.SUCCESS_CODE)
            rl.set_status_message(StringValue('Success!'))
            return rl
        elif location.startswith(StringValue('.')):
            rl.set_status_code(ReadConstants.BAD_REQUEST_CODE)
            rl.set_status_message(StringValue('Malformed location %s.' % location))
            return rl
        else:
            idx = location.find(StringValue('.'))
            el_name = location if idx == IntegerValue(-1) else location.substring(stop=idx)
            if not el_name in self.name_lookup:
                assert logger.error('Element with name %s not found in package %s.' %
                                    (el_name, self.get_location()))
                rl.set_location(self.get_location() + LocationValue('.') + el_name)
                rl.set_status_code(ReadConstants.NOT_FOUND_CODE)
                rl.set_status_message(StringValue('Element with name %s not found in package %s.' %
                                                  (el_name, self.get_location())))
                return rl
            else:
                substr = location.substring(start=idx + IntegerValue(1))
                if substr == LocationValue(''):
                    rl.set_status_code(ReadConstants.BAD_REQUEST_CODE)
                    rl.set_status_message(StringValue('Malformed location %s.' % substr))
                    return rl
                return self.name_lookup[el_name].read(LocationValue('') if idx == IntegerValue(-1) else substr)

    def delete(self):
        '''
        TODO: Make this representation-independent (is that possible?)
        -> Probably the public interfaces of all elements in the object
        package need to include CRUD operations...
        '''
        from mvk.impl.python.python_representer import PythonRepresenter
        cl = MvKDeleteCompositeLog()
        cl.set_location(self.get_location())
        cl.set_type(PythonRepresenter.PACKAGE)

        dl = MvKDeleteLog()
        dl.set_location(self.get_location())
        dl.set_type(PythonRepresenter.PACKAGE)
        dl.set_item(self)
        for item in self.name_lookup:
            elem = self.name_lookup[item]
            cl.add_log(elem.delete())
        try:
            if self.get_parent() is None:
                # Parent must be the root package
                from mvk.mvk import MvK
                MvK().read(LocationValue("")).get_item().remove_element(self.get_name())
            else:
                self.get_parent().remove_element(self.get_name())
            remove_cache(self.get_location())
            dl.set_status_code(DeleteConstants.SUCCESS_CODE)
            dl.set_status_message(StringValue('Success!'))
        except MvKKeyError:
            dl.set_status_code(DeleteConstants.NOT_FOUND_CODE)
            dl.set_status_message(StringValue('Element to delete not found.'))
        cl.add_log(dl)
        cl.set_status_code(dl.get_status_code())
        cl.set_status_message(dl.get_status_message())
        return cl


class Node(Type, NamedElement, mvk.interfaces.object.Node):
    def __init__(self, l_type, potency=None, **kwds):
        assert isinstance(l_type, mvk.interfaces.object.Node)
        self.l_type = l_type
        if potency is None:
            potency = IntegerValue(0)
        self.set_potency(potency)
        ''' mapping of loc:assoc '''
        self.in_associations = MappingValue(value={})
        self.out_associations = MappingValue(value={})
        ''' mapping of attr-name:attr '''
        self.attributes = MappingValue(value={})
        ''' mapping of function-name:function '''
        self.functions = MappingValue(value={})
        super(Node, self).__init__(**kwds)

    """ === PUBLIC INTERFACE === """
    def get_potency(self):
        return self.potency

    def typed_by(self):
        return self.l_type

    def parent_renamed(self, old_path, new_path):
        # update all values
        self.location = None
        for val in self.in_associations:
            if val.startswith(old_path):
                old_val = val
                val = new_path + LocationValue(old_val.get_value()[old_path.len().get_value():])
                self.in_associations[val] = self.in_associations[old_val]
                del self.in_associations[old_val]
        for val in self.out_associations:
            if val.startswith(old_path):
                old_val = val
                val = new_path + LocationValue(old_val.get_value()[old_path.len().get_value():])
                self.out_associations[val] = self.out_associations[old_val]
                del self.out_associations[old_val]
        for val in self.attributes:
            self.attributes[val].parent_renamed(old_path, new_path)
        if hasattr(self, "name_lookup"):
            for elem in self.name_lookup:
                self.name_lookup[elem].parent_renamed(old_path, new_path)

    def __eq__(self, other):
        if not isinstance(other, mvk.interfaces.object.Node):
            return BooleanValue(False)
        elif BooleanValue(id(self) == id(other)) or \
             self.get_location() == other.get_location():
            return BooleanValue(True)
        elif self.get_location().startswith(LocationValue('mvk')) or other.get_location().startswith(LocationValue('mvk')):
            '''
            Special case: one or both of the elements are elements of
            the physical type model, but they are not on the same location.
            That means they are not equal.
            '''
            return BooleanValue(False)

        if logger.isEnabledFor(logging.DEBUG):
            try:
                assert logger.debug('in Node.__eq__() %s' % self.get_location())
                assert logger.debug('isinstance %s' %
                                    isinstance(other, mvk.interfaces.object.Node))
                assert logger.debug('typed_by %s ?= %s (%s)' %
                                    (self.typed_by(), other.typed_by(),
                                     self.typed_by() == other.typed_by()))
                assert logger.debug('potency %s ?= %s (%s)' %
                                    (self.get_potency(), other.get_potency(),
                                     self.get_potency() == other.get_potency()))
                assert logger.debug('%s %s attributes %s' %
                                    (self.get_location(), other.get_location(),
                                     lists_eq_items(self.get_attributes(), other.get_attributes())))
                assert logger.debug('%s ?= %s' % (self.get_attributes(), other.get_attributes()))
                assert logger.debug('%s %s in_associations %s' %
                                    (self.get_location(), other.get_location(),
                                     lists_eq_items(self.get_in_associations(), other.get_in_associations())))
                assert logger.debug('%s ?= %s' % (self.get_in_associations(), other.get_in_associations()))
                assert logger.debug('%s %s out_associations %s' %
                                    (self.get_location(), other.get_location(),
                                     lists_eq_items(self.get_out_associations(), other.get_out_associations())))
                assert logger.debug('%s ?= %s' % (self.get_out_associations(), other.get_out_associations()))
                assert logger.debug('%s %s functions %s' %
                                    (self.get_location(), other.get_location(),
                                     lists_eq_items(self.get_functions(), other.get_functions())))
                assert logger.debug('%s ?= %s' % (self.get_functions(), other.get_functions()))
            except Exception:
                assert logger.error(traceback.format_exc())

        return (super(Node, self).__eq__(other) and
                self.typed_by() == other.typed_by() and
                self.get_potency() == other.get_potency() and
                lists_eq_items(self.get_attributes(), other.get_attributes()) and
                lists_eq_items(self.get_in_associations(), other.get_in_associations()) and
                lists_eq_items(self.get_out_associations(), other.get_out_associations()) and
                lists_eq_items(self.get_functions(), other.get_functions()))

    def get_attributes(self):
        return ImmutableSequenceValue(self.attributes.values())

    def get_all_attributes(self):
        return ImmutableSequenceValue(self.attributes.values())

    def get_attribute(self, attr_name):
        assert (isinstance(attr_name, mvk.interfaces.datavalue.StringValue) and
                isinstance(attr_name.typed_by(), StringType))
        if attr_name in self.attributes:
            return self.attributes[attr_name]
        raise MvKKeyError(StringValue('Attribute %s not found!' % attr_name))

    def get_functions(self):
        return ImmutableSequenceValue(self.functions.values())

    def get_function(self, f_name):
        assert (isinstance(f_name, mvk.interfaces.datavalue.StringValue) and
                isinstance(f_name.typed_by(), StringType))
        if f_name in self.functions:
            return self.functions[f_name]
        raise MvKKeyError(StringValue('Function %s not found!' % f_name))

    def get_out_associations(self):
        return ImmutableSequenceValue(self.out_associations.values())

    def get_in_associations(self):
        return ImmutableSequenceValue(self.in_associations.values())

    def get_outgoing_elements(self):
        return ImmutableSequenceValue(SequenceValue(value=list(set([a.get_to_multiplicity().get_node() for a in self.out_associations.values().get_value()]))))

    def get_incoming_elements(self):
        return ImmutableSequenceValue(SequenceValue(value=list(set([a.get_from_multiplicity().get_node() for a in self.in_associations.values().get_value()]))))

    def get_neighbors(self):
        inc = self.get_incoming_elements()
        out = self.get_outgoing_elements()
        result = SequenceValue(value=inc.get_value())
        for i in out:
            if i not in result:
                result.append(i)
        return ImmutableSequenceValue(result)

    ''' == PYTHON SPECIFIC == '''
    def set_potency(self, potency):
        '''
        Sets the potency value for this node.
        @type potency: L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>} or
                       L{InfiniteValue<mvk.interfaces.datavalue.InfiniteValue>}
        @param potency: The new potency value for this node.
        '''
        assert ((isinstance(potency, mvk.interfaces.datavalue.IntegerValue) and
                isinstance(potency.typed_by(), IntegerType)) or
                (isinstance(potency, mvk.interfaces.datavalue.InfiniteValue) and
                isinstance(potency.typed_by(), InfiniteType)))
        assert potency >= IntegerValue(0)
        self.potency = potency

    def add_in_association(self, association):
        '''
        Adds an incoming association to this node. Careful: needs to be
        kept in sync with the source clabject's outgoing associations.
        @type association: L{Association<mvk.interfaces.object.Association>}
        @param association: An incoming association.
        '''
        assert isinstance(association, mvk.interfaces.object.Association)
        old_len = self.in_associations.len()
        self.in_associations[association.get_location()] = association
        assert self.in_associations.len() == old_len + IntegerValue(1)

    def add_out_association(self, association):
        '''
        Adds an outgoing association to this node. Careful: needs to be
        kept in sync with the target clabject's incoming associations.
        @type association: L{Association<mvk.interfaces.object.Association>}
        @param association: An outgoing association.
        '''
        assert isinstance(association, mvk.interfaces.object.Association)
        old_len = self.out_associations.len()
        self.out_associations[association.get_location()] = association
        assert self.out_associations.len() == old_len + IntegerValue(1)

    def remove_in_association(self, association_location):
        '''
        Removes an incoming association from this node. It is an error
        if no such association is defined for this node. Careful: needs to
        be kept in sync with the source clabject's outgoing associations.
        @type association_location: L{LocationValue<mvk.interfaces.datavalue.LocationValue>}
        @param association_location: The location of the association.
        @raise MvKKeyError: If no association with given location is defined
        for this node.
        '''
        assert (isinstance(association_location, mvk.interfaces.datavalue.LocationValue) and
                isinstance(association_location.typed_by(), LocationType))
        if not association_location in self.in_associations:
            raise MvKKeyError(StringValue('Association not found!'))
        del self.in_associations[association_location]

    def update_in_association(self, old_location, association):
        '''
        Removes the incoming association with location 'old_location' and
        replaces it with 'association'.
        @type old_location: L{LocationValue<mvk.interfaces.datavalue.LocationValue>}
        @param old_location: The old location of the association to update.
        @raise MvKKeyError: If the association cannot be found.
        '''
        assert (isinstance(old_location, mvk.interfaces.datavalue.LocationValue) and
                isinstance(old_location.typed_by(), LocationType))
        assert isinstance(association, mvk.interfaces.object.Association)
        if not old_location in self.in_associations:
            raise MvKKeyError(StringValue('Association not found!'))
        del self.in_associations[old_location]
        self.in_associations[association.get_location()] = association

    def remove_out_association(self, association_location):
        '''
        Removes an outgoing association from this node. It is an error
        if no such association is defined for this node. Careful: needs to
        be kept in sync with the target clabject's incoming associations.
        @type association_location: L{LocationValue<mvk.interfaces.datavalue.LocationValue>}
        @param association_location: The location of the association.
        @raise MvKKeyError: If no association with given location is defined
        for this node.
        '''
        assert (isinstance(association_location, mvk.interfaces.datavalue.LocationValue) and
                isinstance(association_location.typed_by(), LocationType))
        if not association_location in self.out_associations:
            raise MvKKeyError(StringValue('Association not found!'))
        del self.out_associations[association_location]

    def update_out_association(self, old_location, association):
        '''
        Removes the outgoing association with location 'old_location' and
        replaces it with 'association'.
        @type old_location: L{LocationValue<mvk.interfaces.datavalue.LocationValue>}
        @param old_location: The old location of the association to update.
        @raise MvKKeyError: If the association cannot be found.
        '''
        assert (isinstance(old_location, mvk.interfaces.datavalue.LocationValue) and
                isinstance(old_location.typed_by(), LocationType))
        assert isinstance(association, mvk.interfaces.object.Association)
        if not old_location in self.out_associations:
            raise MvKKeyError(StringValue('Association not found!'))
        del self.out_associations[old_location]
        self.out_associations[association.get_location()] = association

    def add_attribute(self, attr):
        '''
        Adds an attribute to this node. Automatically sets the parent
        of the newly added attribute to this node.
        @type attr: L{Attribute<mvk.interfaces.object.Attribute>}
        @param attr: The new attribute.
        @raise MvKNameError: If an attribute with the same name already exists.
        '''
        assert isinstance(attr, mvk.interfaces.object.Attribute)
        if attr.get_name() in self.attributes:
            raise MvKNameError(StringValue('An attribute with the name %s \
                                            already exists in node %s' %
                                            (attr.get_name(), self.get_name())))
        if attr.get_name() in self.functions:
            raise MvKNameError(StringValue('A function with the name %s \
                                            already exists in node %s' %
                                            (attr.get_name(), self.get_name())))
        attr.set_parent(self)
        self.attributes[attr.get_name()] = attr

    def add_attributes(self, attrs):
        '''
        Adds a list of attributes to this node. Automatically sets the
        parent of the newly added attributes to this node.
        @type attrs: list
        @param attrs: A list of L{Attribute<mvk.interfaces.object.Attribute>}s.
        @raise MvKNameError: If an attribute with the same name already exists.
        '''
        assert isinstance(attrs, list)
        names = SetValue(set([a.get_name() for a in attrs]))
        name_check = names.intersection(self.attributes.keys().union(self.functions.keys()))
        if not name_check.len() == IntegerValue(0):
            raise MvKNameError(StringValue('Attributes with name(s) %s already \
                                            exist in node %s.' %
                                            (name_check, self.get_name())))
        for attr in attrs:
            self.add_attribute(attr)

    def add_function(self, func):
        '''
        Adds an attribute to this node. Automatically sets the parent
        of the newly added attribute to this node.
        @type attr: L{Attribute<mvk.interfaces.object.Attribute>}
        @param attr: The new attribute.
        @raise MvKNameError: If an attribute with the same name already exists.
        '''
        assert isinstance(func, mvk.interfaces.action.Function)
        if func.get_name() in self.functions:
            raise MvKNameError(StringValue('A function with the name %s \
                                            already exists in node %s' %
                                            (func.get_name(), self.get_name())))
        elif func.get_name() in self.attributes:
            raise MvKNameError(StringValue('An attribute with the name %s \
                                            already exists in node %s' %
                                            (func.get_name(), self.get_name())))
        func.set_parent(self)
        self.functions[func.get_name()] = func

    def add_functions(self, funcs):
        '''
        Adds a list of attributes to this node. Automatically sets the
        parent of the newly added attributes to this node.
        @type attrs: list
        @param attrs: A list of L{Attribute<mvk.interfaces.object.Attribute>}s.
        @raise MvKNameError: If an attribute with the same name already exists.
        '''
        assert isinstance(funcs, list)
        names = SetValue(set([f.get_name() for f in funcs]))
        name_check = names.intersection(self.functions.keys().union(self.attributes.keys()))
        if not name_check.len() == IntegerValue(0):
            raise MvKNameError(StringValue('Functions with name(s) %s already \
                                            exist in clabject %s.' %
                                            (name_check, self.get_name())))
        for f in funcs:
            self.add_function(f)

    def remove_function(self, func_name):
        '''
        Removes an function from this node. It is an error if no function
        with the given name is found.
        @type attr_name: L{StringValue<mvk.interfaces.datavalue.StringValue>}
        @param attr_name: The name of the attribute to remove.
        @raises MvKKeyError: If the function was not found.
        '''
        assert (isinstance(func_name, mvk.interfaces.datavalue.StringValue) and
                isinstance(func_name.typed_by(), mvk.interfaces.datatype.StringType))
        if not func_name in self.functions:
            raise MvKKeyError(StringValue('A function with the name %s \
                                           does not exist in node %s' %
                                           (func_name, self.get_name())))
        del self.functions[func_name]

    def remove_attribute(self, attr_name):
        '''
        Removes an attribute from this node. It is an error if no attribute
        with the given name is found.
        @type attr_name: L{StringValue<mvk.interfaces.datavalue.StringValue>}
        @param attr_name: The name of the attribute to remove.
        @raises MvKKeyError: If the attribute was not found.
        '''
        assert (isinstance(attr_name, mvk.interfaces.datavalue.StringValue) and
                isinstance(attr_name.typed_by(), mvk.interfaces.datatype.StringType))
        if attr_name not in self.attributes:
            raise MvKKeyError(StringValue('Attribute not found!'))
        del self.attributes[attr_name]

    def update_attribute(self, old_name, attr):
        assert (isinstance(old_name, mvk.interfaces.datavalue.StringValue) and
                isinstance(old_name.typed_by(), StringType))
        assert isinstance(attr, Attribute)
        assert attr.get_parent() == self
        if old_name == attr.get_name():
            return
        if not old_name in self.attributes:
            raise MvKKeyError(StringValue('Attribute not found!'))
        if attr.get_name() in self.attributes:
            raise MvKNameError(StringValue('An attribute with the name %s \
                                            already exists in node %s' %
                                            (attr.get_name(), self.get_name())))
        del self.attributes[old_name]
        self.attributes[attr.get_name()] = attr

    """ === CRUD === """
    @classmethod
    def _add_to_parent(cls, inst, parent):
        ''' This method is called when a newly created element is added to its parent. As the parent can be of different physical types (model, clabject,
        expression statement, ...), this method ensures the newly created instance is added to the correct parent. '''
        raise NotImplementedError()

    def _remove_from_parent(self):
        ''' This method is called when an element is removed from its parent. As the parent can be of different physical types (model, clabject,
        expression statement, ...), this method ensures the instance is removed correctly. '''
        raise NotImplementedError()

    @classmethod
    def _create_inst(cls, params, cl):
        attributes = params[CreateConstants.ATTRS_KEY]
        name = attributes[StringValue('name')]
        if not StringValue('potency') in attributes:
            if not attributes[StringValue('class')].startswith(StringValue('mvk')):
                attributes[StringValue('potency')] = ClabjectReference(path=attributes[StringValue('class')]).get_potency() - IntegerValue(1)
        potency = attributes[StringValue('potency')] if StringValue('potency') in attributes else None
        clz = attributes[StringValue('class')]
        assert logger.debug('Creating %s with name %s, potency %s, type %s' %
                            (cls.__name__, name, potency, clz))
        n = cls(name=name, potency=potency,
                l_type=ClabjectReference(path=clz))
        cl.add_attr_change(StringValue('name'), n.get_name())
        cl.add_attr_change(StringValue('potency'), n.get_potency())
        cl.add_attr_change(StringValue('class'), n.typed_by().get_location())
        return n

    @classmethod
    def _check_params_create(cls, params):
        cl = MvKCreateLog()
        if not (isinstance(params, mvk.interfaces.datavalue.MappingValue) and
                isinstance(params.typed_by(), mvk.interfaces.datatype.MappingType)):
            cl.set_status_code(CreateConstants.MALFORMED_REQUEST_CODE)
            cl.set_status_message(StringValue('Expected a MappingValue'))
            return cl
        try:
            c_params = MappingValue({})
            for k in params:
                ''' TODO: Here, a deep copy has to be made. For example, all entries which are themselves mapping values need to be deep-copied. '''
                c_params[k] = params[k]
            cls._check_param(c_params,
                             CreateConstants.LOCATION_KEY,
                             mvk.interfaces.datavalue.LocationValue,
                             mvk.interfaces.datatype.LocationType)
            cls._check_param(c_params,
                             CreateConstants.TYPE_KEY,
                             mvk.interfaces.datavalue.LocationValue,
                             mvk.interfaces.datatype.LocationType)
            cls._check_param(c_params,
                             CreateConstants.ATTRS_KEY,
                             mvk.interfaces.datavalue.MappingValue,
                             mvk.interfaces.datatype.MappingType)
            attributes = c_params[CreateConstants.ATTRS_KEY]
            cls._check_param(attributes,
                             StringValue('class'),
                             mvk.interfaces.datavalue.LocationValue,
                             mvk.interfaces.datatype.LocationType)
            ''' Here, check the attributes of the type, and how they are mapped
            onto physical attributes. '''
            if not attributes[StringValue('class')].startswith(LocationValue('mvk')):
                from mvk.mvk import MvK
                the_type = attributes[StringValue('class')]
                phys_mapper = MvK().get_physical_mapper(the_type)
                type_rl = MvK().read(the_type)
                if not type_rl.is_success():
                    cl.set_status_code(type_rl.get_status_code())
                    cl.set_status_message(type_rl.get_status_message())
                    return cl
                t = type_rl.get_item()
                assert isinstance(t, mvk.interfaces.object.Clabject)
                for attr in t.get_all_attributes():
                    assert logger.debug('%s is an attribute of %s' %
                                        (attr.get_name(), t))
                    if attr.get_potency() > IntegerValue(0):
                        try:
                            attr_name = attr.get_short_location()
                            assert logger.debug('Looking for %s in %s...' % (attr_name, phys_mapper.get_physical_attribute_mapping()))
                            m = phys_mapper.get_physical_attribute_mapping()[attr_name]
                            assert m.len() == IntegerValue(1)
                            if attr_name in attributes:
                                attributes[m[IntegerValue(0)]] = attributes[attr_name]
                            else:
                                attributes[m[IntegerValue(0)]] = attr.get_default()
                            ''' TODO: Delete attributes[m[IntegerValue(0)]] if attr_name != m[IntegerValue(0)]? '''
                        except MvKKeyError, e:
                            assert logger.debug('%s not found in %s' %
                                         (attr_name, phys_mapper.get_physical_attribute_mapping()))
            cls._check_param(attributes,
                             StringValue('name'),
                             mvk.interfaces.datavalue.StringValue,
                             mvk.interfaces.datatype.StringType)
            cls._check_param(attributes,
                             StringValue('potency'),
                             (mvk.interfaces.datavalue.IntegerValue,
                              mvk.interfaces.datavalue.InfiniteValue),
                             (mvk.interfaces.datatype.IntegerType,
                              mvk.interfaces.datatype.InfiniteType),
                             req=False,
                             extra_check=lambda x: None if x >= IntegerValue(0) else StringValue('Potency value needs to be >= 0!'))
        except MvKException, e:
            cl.set_status_code(CreateConstants.BAD_REQUEST_CODE)
            cl.set_status_message(e.get_message())
            return cl
        return None

    @classmethod
    def _create(cls, params):
        ''' Should never be called directly: 'cls' is the actual subclass of Node to be created. '''
        assert logger.debug('In Node._create %s' % params)
        ''' Initialize needed changelog values. '''
        cl = MvKCreateLog()
        location = params[CreateConstants.LOCATION_KEY]
        the_type = params[CreateConstants.TYPE_KEY]
        cl.set_location(location)
        cl.set_type(the_type)
        return_log = MvKCreateCompositeLog()
        return_log.set_location(cl.get_location())
        return_log.set_type(cl.get_type())

        ''' Create new node. '''
        attributes = params[CreateConstants.ATTRS_KEY]
        clz = attributes[StringValue('class')]
        n = cls._create_inst(params, cl)
        cl.set_name(n.get_name())
        return_log.set_name(n.get_name())

        ''' Try setting the parent.  '''
        from mvk.mvk import MvK
        parent_log = MvK().read(location)
        if not parent_log.is_success():
            return_log.set_status_code(parent_log.get_status_code())
            return_log.set_status_message(parent_log.get_status_message())
            return return_log
        parent = parent_log.get_item()
        assert logger.debug('Setting parent to %s' % parent.get_location())
        try:
            cls._add_to_parent(n, parent)
            cl.set_location(parent_log.get_location())
            cl.set_status_code(CreateConstants.SUCCESS_CODE)
            cl.set_status_message(StringValue('Success!'))
        except MvKNameError, e:
            cl.set_status_code(CreateConstants.BAD_REQUEST_CODE)
            cl.set_status_message(e.get_message())
            return cl
        return_log.add_log(cl)

        '''
        Time for attributes which need to be instantiated from the type.
        '''
        if not clz.startswith(LocationValue('mvk')):
            try:
                all_attributes = n.typed_by().get_all_attributes()
            except MvKLookupError:
                ''' TODO: This has to do with classes which are not yet
                created in the modelverse. Do we want to have it like this? '''
                all_attributes = SequenceValue([])
            for a in all_attributes:
                potency = a.get_potency()
                if (potency > IntegerValue(0) and
                    (potency != IntegerValue(1) or a.get_short_location() in attributes or a.get_lower() > IntegerValue(0))):
                    c_attributes = MappingValue({StringValue('name'): a.get_short_location(),
                                                 StringValue('class'): a.get_location()})
                    c_params = MappingValue({CreateConstants.LOCATION_KEY: n.get_location(),
                                             CreateConstants.ATTRS_KEY: c_attributes})
                    if potency > IntegerValue(1):
                        c_attributes[StringValue('default')] = a.get_default()
                        c_attributes[StringValue('potency')] = potency - IntegerValue(1)
                        c_attributes[StringValue('lower')] = a.get_lower()
                        c_attributes[StringValue('upper')] = a.get_upper()
                        c_attributes[StringValue('ordered')] = a.is_ordered()
                    elif potency == IntegerValue(1):
                        if a.get_short_location() in attributes:
                            c_attributes[StringValue('value')] = attributes[a.get_short_location()]
                        else:
                            c_attributes[StringValue('value')] = a.get_default()
                    else:
                        c_attributes[StringValue('value')] = a.get_value()
                    assert logger.debug('Creating attribute with attributes %s in Node %s.' %
                                        (c_attributes, n.get_location()))
                    a_cl = Attribute.create(c_params)
                    if not a_cl.is_success():
                        ''' Something went wrong creating the attribute, undo
                        changes already performed... '''
                        n.delete()
                        return_log.set_status_code(a_cl.get_status_code())
                        return_log.set_status_message(a_cl.get_status_message())
                        return return_log
                    return_log.add_log(a_cl)

        return_log.set_status_code(CreateConstants.SUCCESS_CODE)
        return_log.set_status_message(StringValue("Success"))

        ''' Return changelog. '''
        return return_log

    @classmethod
    def _check_params_update(cls, params):
        cl = MvKUpdateLog()
        if not (isinstance(params, mvk.interfaces.datavalue.MappingValue) and
                isinstance(params.typed_by(), mvk.interfaces.datatype.MappingType)):
            cl.set_status_code(UpdateConstants.MALFORMED_REQUEST_CODE)
            cl.set_status_message(StringValue('Expected a MappingValue'))
            return cl
        try:
            cls._check_param(params,
                             CreateConstants.ATTRS_KEY,
                             mvk.interfaces.datavalue.MappingValue,
                             mvk.interfaces.datatype.MappingType)
            attributes = params[CreateConstants.ATTRS_KEY]
            cls._check_param(attributes,
                             StringValue('name'),
                             mvk.interfaces.datavalue.StringValue,
                             mvk.interfaces.datatype.StringType,
                             req=False)
            cls._check_param(attributes,
                             StringValue('potency'),
                             (mvk.interfaces.datavalue.IntegerValue,
                              mvk.interfaces.datavalue.InfiniteValue),
                             (mvk.interfaces.datatype.IntegerType,
                              mvk.interfaces.datatype.InfiniteType),
                             req=False,
                             extra_check=lambda x: None if x >= IntegerValue(0) else StringValue('potency value needs to be >= 0'))
        except MvKException, e:
            cl.set_status_code(UpdateConstants.BAD_REQUEST_CODE)
            cl.set_status_message(e.get_message())
            return cl
        return None

    def _update(self, params):
        from mvk.impl.python.python_representer import PythonRepresenter
        cl = MvKUpdateLog()
        cl.set_location(self.get_location())
        cl.set_type(self.typed_by())

        attributes = params[UpdateConstants.ATTRS_KEY]
        try:
            for name in attributes:
                if self.typed_by().get_location().startswith(StringValue('mvk')):
                    if name == StringValue('name'):
                        new_val = attributes[name]
                        cl.add_attr_change(name, self.get_name(), new_val)
                        self.set_name(new_val)
                    elif name == StringValue('potency'):
                        new_val = attributes[name]
                        cl.add_attr_change(name, self.get_potency(), new_val)
                        self.set_potency(new_val)
                    else:
                        ''' TODO: revert! '''
                        cl.set_status_code(UpdateConstants.BAD_REQUEST_CODE)
                        cl.set_status_message(StringValue('Don\'t know how to update clabject\'s physical attribute %s.' %
                                                          name))
                        return cl
                else:
                    attr = self.get_attribute(name)
                    old_val = attr.get_value()
                    new_val = attributes[name]
                    attr.set_value(new_val)
                    from mvk.mvk import MvK
                    u_actions = MvK().get_physical_mapper(self.typed_by().get_location()).get_physical_update_actions()
                    if name in u_actions:
                        eval('self.%s(new_val)' % str(u_actions[name]))
                    cl.add_attr_change(name, old_val, new_val)
            cl.set_status_code(UpdateConstants.SUCCESS_CODE)
            cl.set_status_message(StringValue('Successfully updated node.'))
        except MvKKeyError, e:
            ''' TODO: revert! '''
            cl.set_status_code(UpdateConstants.NOT_FOUND_CODE)
            cl.set_status_message(e.get_message())
        except MvKValueError, e:
            ''' TODO: revert! '''
            cl.set_status_code(UpdateConstants.NOT_FOUND_CODE)
            cl.set_status_message(e.get_message())
        except MvKPotencyError, e:
            ''' TODO: revert! '''
            cl.set_status_code(UpdateConstants.BAD_REQUEST_CODE)
            cl.set_status_message(e.get_message())

        ''' This second set_location in case name was changed. '''
        cl.set_location(self.get_location())
        return cl

    def read(self, location):
        assert (isinstance(location, LocationValue) and
                isinstance(location.typed_by(), LocationType))

        rl = MvKReadLog()
        if location == LocationValue(''):
            ''' Base case. '''
            rl.set_item(self)
            rl.set_location(self.get_location())
            rl.set_status_code(ReadConstants.SUCCESS_CODE)
            rl.set_type(self.typed_by().get_location())
            rl.set_status_message(StringValue('Success!'))
            return rl
        else:
            idx = location.find(StringValue('.'))
            el_name = location if idx == IntegerValue(-1) else location.substring(stop=idx)
            if el_name in self.attributes:
                return self.get_attribute(el_name).read(LocationValue('') if idx == IntegerValue(-1) else location.substring(start=idx + IntegerValue(1)))
            elif location in self.attributes:
                return self.get_attribute(location).read(LocationValue(''))
            elif el_name in self.functions:
                return self.get_function(el_name).read(LocationValue('') if idx == IntegerValue(-1) else location.substring(start=idx + IntegerValue(1)))
            else:
                for a in self.get_out_associations():
                    if isinstance(a, mvk.interfaces.object.Composition):
                        n = a.get_to_multiplicity().get_node()
                        if n.get_name() == el_name:
                            return n.read(LocationValue('') if idx == IntegerValue(-1) else location.substring(start=idx + IntegerValue(1)))

                assert logger.error('Element with name %s not found in node %s.' %
                                    (el_name, self.get_location()))
                rl.set_location(self.get_location() + LocationValue('.') + el_name)
                rl.set_status_code(ReadConstants.NOT_FOUND_CODE)
                rl.set_status_message(StringValue('Element with name %s not found in node %s.' %
                                                  (el_name, self.get_location())))
                return rl

    def delete(self):
        '''
        TODO: Make this representation-independent (is that possible?)
        -> Probably the public interface needs to include CRUD operations...
        '''
        return_log = MvKDeleteCompositeLog()
        location = self.get_location()

        attrs = {}
        # Save all attributes with potency 0 in the attributes of the model
        for attr in self.get_all_attributes():
            if attr.get_potency() == IntegerValue(0):
                attrs[attr.get_name()] = attr.get_value()
                remove_cache(attr.get_location())
                # NOTE don't delete the attributes in themself, as they might contain some information that needs to be kept to the end

        for a in self.get_out_associations():
            if isinstance(a, mvk.interfaces.object.Composition) and a.get_to_multiplicity().get_node().get_potency() == IntegerValue(0):
                # Save out associations which link to an attribute with potency 0
                # but don't include them in the changelogs
                attrs[attr.get_name()] = attr.get_value()
                cl = a.delete()
                if not cl.is_success():
                    return cl
            else:
                # These are deleted and shouldn't be included in the create parameters
                cl = a.delete()
                #TODO temporarily we skip composition links from the create
                if not isinstance(a, mvk.interfaces.object.Composition):
                    return_log.add_log(cl)
                if not cl.is_success():
                    return_log.set_status_code(cl.get_status_code())
                    return_log.set_status_message(cl.get_status_message())
                    return cl
        attrs = MappingValue(attrs)

        for assoc in self.get_in_associations():
            if isinstance(assoc, mvk.interfaces.object.Composition) and assoc.get_to_multiplicity().get_node() == self:
                cl = assoc.delete(propagate=BooleanValue(False))
            else:
                cl = assoc.delete()
            #TODO temporarily we skip composition links from the create
            if not isinstance(assoc, mvk.interfaces.object.Composition):
                return_log.add_log(cl)
            if not cl.is_success():
                return_log.set_status_code(cl.get_status_code())
                return_log.set_status_message(cl.get_status_message())
                return cl
        
        #TODO dirty...
        if hasattr(self, "name_lookup"):
            for item in self.name_lookup:
                elem = self.name_lookup[item]
                if isinstance(elem, mvk.interfaces.object.Association):
                    cl = elem.delete()
                    return_log.add_log(cl)
            for item in self.name_lookup:
                elem = self.name_lookup[item]
                cl = elem.delete()
                return_log.add_log(cl)

        cl = MvKDeleteLog()
        cl.set_status_code(DeleteConstants.SUCCESS_CODE)
        cl.set_status_message(StringValue('Success!'))
        try:
            cl.set_location(self.get_location())
            cl.set_item(self)
            for key in attrs:
                cl.add_attr(key, attrs[key])
            cl.set_type(self.typed_by().get_location())
            if self.parent is not None:
                self._remove_from_parent()
            remove_cache(location)
        except MvKKeyError:
            cl.set_status_code(DeleteConstants.NOT_FOUND_CODE)
            cl.set_status_message(StringValue('Element to delete not found.'))
        return_log.add_log(cl)
        return_log.set_status_code(cl.get_status_code())
        return_log.set_status_message(cl.get_status_message())
        return return_log


class Model(Node, Package, mvk.interfaces.object.Model):
    """ === CONSTRUCTOR === """
    def __init__(self, potency=None, **kwds):
        assert logger.debug('Constructing Model')
        if potency is None:
            potency = InfiniteValue('+')
        super(Model, self).__init__(potency=potency, **kwds)

    """ === PUBLIC INTERFACE === """
    def is_type_of(self, el):
        return isinstance(el, Model) and el.typed_by() == self

    def __eq__(self, other):
        if logger.isEnabledFor(logging.DEBUG):
            try:
                assert logger.debug('in Model.__eq__() %s' % self.get_location())
                assert logger.debug('isinstance %s' %
                                    isinstance(other, mvk.interfaces.object.Model))
                assert logger.debug('elements %s ?= %s (%s)' %
                                    (self.get_elements(), other.get_elements(),
                                     self.get_elements() == other.get_elements()))
            except Exception:
                assert logger.error(traceback.format_exc())

        return (BooleanValue(isinstance(other, mvk.interfaces.object.Model)) and
                super(Model, self).__eq__(other))

    """ === CRUD === """
    @classmethod
    def _check_params_create(cls, params):
        cl = MvKCreateLog()
        if not (isinstance(params, mvk.interfaces.datavalue.MappingValue) and
                isinstance(params.typed_by(), mvk.interfaces.datatype.MappingType)):
            cl.set_status_code(CreateConstants.MALFORMED_REQUEST_CODE)
            cl.set_status_message(StringValue('Expected a MappingValue'))
            return cl
        try:
            cls._check_param(params,
                             CreateConstants.LOCATION_KEY,
                             mvk.interfaces.datavalue.LocationValue,
                             mvk.interfaces.datatype.LocationType)
            cls._check_param(params,
                             CreateConstants.TYPE_KEY,
                             mvk.interfaces.datavalue.LocationValue,
                             mvk.interfaces.datatype.LocationType)
            cls._check_param(params,
                             CreateConstants.ATTRS_KEY,
                             mvk.interfaces.datavalue.MappingValue,
                             mvk.interfaces.datatype.MappingType)
            attributes = params[CreateConstants.ATTRS_KEY]
            cls._check_param(attributes,
                             StringValue('type_model'),
                             mvk.interfaces.datavalue.LocationValue,
                             mvk.interfaces.datatype.LocationType)
            ''' Here, check the attributes of the type, and how they are mapped
            onto physical attributes. '''
            if not attributes[StringValue('type_model')].startswith(LocationValue('mvk.object')):
                from mvk.mvk import MvK
                the_type = attributes[StringValue('type_model')]
                phys_mapper = MvK().get_physical_mapper(the_type)
                type_rl = MvK().read(the_type)
                if not type_rl.is_success():
                    cl.set_status_code(type_rl.get_status_code())
                    cl.set_status_message(type_rl.get_status_message())
                    return cl
                t = type_rl.get_item()
                assert isinstance(t, mvk.interfaces.object.Model)
                for attr in t.get_attributes():
                    assert logger.debug('%s is an attribute of %s' %
                                        (attr.get_name(), t))
                    if attr.get_potency() > IntegerValue(0):
                        try:
                            attr_name = attr.get_short_location()
                            assert logger.debug('Looking for %s in %s...' % (attr_name, phys_mapper.get_physical_attribute_mapping()))
                            m = phys_mapper.get_physical_attribute_mapping()[attr_name]
                            assert m.len() == IntegerValue(1)
                            if attr_name in attributes:
                                attributes[m[IntegerValue(0)]] = attributes[attr_name]
                            else:
                                attributes[m[IntegerValue(0)]] = attr.get_default()
                            ''' TODO: Delete attributes[m[IntegerValue(0)]] if attr_name != m[IntegerValue(0)]? '''
                        except MvKKeyError, e:
                            assert logger.debug('%s not found in %s' %
                                         (attr_name, phys_mapper.get_physical_attribute_mapping()))
            cls._check_param(attributes,
                             StringValue('name'),
                             mvk.interfaces.datavalue.StringValue,
                             mvk.interfaces.datatype.StringType)
            cls._check_param(attributes,
                             StringValue('potency'),
                             (mvk.interfaces.datavalue.IntegerValue,
                              mvk.interfaces.datavalue.InfiniteValue),
                             (mvk.interfaces.datatype.IntegerType,
                              mvk.interfaces.datatype.InfiniteType),
                             req=False,
                             extra_check=lambda x: None if x >= IntegerValue(0) else StringValue('Potency value needs to be >= 0!'))
        except MvKException, e:
            cl.set_status_code(CreateConstants.BAD_REQUEST_CODE)
            cl.set_status_message(e.get_message())
            return cl
        return None

    @classmethod
    def _create(cls, params):
        ''' TODO: Whenever something goes wrong, undo whatever was done
        already. Need to have reverting implemented, though. '''
        from mvk.impl.python.python_representer import PythonRepresenter
        ''' Initialize needed changelog values. '''
        cl = MvKCreateLog()
        location = params[CreateConstants.LOCATION_KEY]
        the_type = params[CreateConstants.TYPE_KEY]
        cl.set_location(location)
        cl.set_type(the_type)
        return_log = MvKCreateCompositeLog()
        return_log.set_location(cl.get_location())
        return_log.set_type(cl.get_type())

        ''' Create new model. '''
        attributes = params[CreateConstants.ATTRS_KEY]
        name = attributes[StringValue('name')]
        if not StringValue('potency') in attributes:
            if not attributes[StringValue('type_model')].startswith(StringValue('mvk')):
                attributes[StringValue('potency')] = ClabjectReference(path=attributes[StringValue('type_model')]).get_potency() - IntegerValue(1)
        potency = attributes[StringValue('potency')] if StringValue('potency') in attributes else None
        type_model = attributes[StringValue('type_model')]
        m = Model(name=name, potency=potency, l_type=ModelReference(path=type_model))
        cl.set_name(m.get_name())
        cl.add_attr_change(StringValue('name'), m.get_name())
        cl.add_attr_change(StringValue('potency'), m.get_potency())
        cl.add_attr_change(StringValue('type_model'), m.typed_by().get_location())
        cl.set_status_code(CreateConstants.SUCCESS_CODE)
        cl.set_status_message(StringValue('Success'))

        ''' Try setting the parent.  '''
        from mvk.mvk import MvK
        parent_log = MvK().read(location)
        ''' If the parent does not exist, create a package on that location. '''
        if not parent_log.is_success():
            splitted = location.rsplit(StringValue('.'), IntegerValue(1))
            params = MappingValue({})
            params[CreateConstants.TYPE_KEY] = PythonRepresenter.PACKAGE
            c_attributes = MappingValue({})
            if splitted.len() == IntegerValue(1):
                ''' We're creating a package at the top level. '''
                params[CreateConstants.LOCATION_KEY] = LocationValue('')
                c_attributes[StringValue('name')] = splitted[IntegerValue(0)]
            else:
                ''' We're creating a package inside another package. '''
                params[CreateConstants.LOCATION_KEY] = splitted[IntegerValue(0)]
                c_attributes[StringValue('name')] = splitted[IntegerValue(1)]
            params[CreateConstants.ATTRS_KEY] = c_attributes
            ''' Actually create the package. '''
            create_log = MvK().create(params)
            if not create_log.is_success():
                ''' TODO: revert! '''
                cl.set_status_code(create_log.get_status_code())
                cl.set_status_message(create_log.get_status_message())
                return cl
            return_log.add_log(create_log)
            ''' The parent now exists! '''
            parent_log = MvK().read(location)

        parent = parent_log.get_item()
        if not isinstance(parent, mvk.interfaces.object.Package):
            cl.set_status_code(CreateConstants.BAD_REQUEST_CODE)
            cl.set_status_message(StringValue('Can only create a Model \
                                               inside a package.'))
            return_log.add_log(cl)
            return return_log
        else:
            assert logger.debug('Adding new model %s to package %s.' %
                                (m.get_name(), parent.get_name()))
            try:
                parent.add_element(m)
                cl.set_status_code(CreateConstants.SUCCESS_CODE)
                cl.set_status_message(StringValue('Success'))
                return_log.add_log(cl)
            except MvKNameError, e:
                cl.set_status_code(CreateConstants.BAD_REQUEST_CODE)
                cl.set_status_message(e.get_message())
                return_log.add_log(cl)
                return_log.set_status_code(cl.get_status_code())
                return_log.set_status_message(cl.get_status_message())
                return return_log

        '''
        Time for attributes which need to be instantiated from the type.
        '''
        if not type_model.startswith(LocationValue('mvk.object')):
            try:
                all_attributes = m.typed_by().get_attributes()
            except MvKLookupError:
                ''' TODO: This has to do with classes which are not yet
                created in the modelverse. Do we want to have it like this? '''
                all_attributes = SequenceValue([])
            for a in all_attributes:
                potency = a.get_potency()
                if (potency > IntegerValue(0) and
                    (potency != IntegerValue(1) or a.get_short_location() in attributes or a.get_lower() > IntegerValue(0))):
                    c_attributes = MappingValue({StringValue('name'): a.get_short_location(),
                                                 StringValue('class'): a.get_location()})
                    c_params = MappingValue({CreateConstants.LOCATION_KEY: m.get_location(),
                                             CreateConstants.ATTRS_KEY: c_attributes})
                    if potency > IntegerValue(1):
                        c_attributes[StringValue('default')] = a.get_default()
                        c_attributes[StringValue('potency')] = potency - IntegerValue(1)
                        c_attributes[StringValue('lower')] = a.get_lower()
                        c_attributes[StringValue('upper')] = a.get_upper()
                        c_attributes[StringValue('ordered')] = a.is_ordered()
                    elif potency == IntegerValue(1):
                        if a.get_short_location() in attributes:
                            c_attributes[StringValue('value')] = attributes[a.get_short_location()]
                        else:
                            c_attributes[StringValue('value')] = a.get_default()
                    else:
                        c_attributes[StringValue('value')] = a.get_value()
                    assert logger.debug('Creating attribute with attributes %s in Model %s.' %
                                        (c_attributes, m.get_location()))
                    a_cl = Attribute.create(c_params)
                    if not a_cl.is_success():
                        ''' Something went wrong creating the attribute, undo
                        changes already performed... '''
                        return_log.set_status_code(a_cl.get_status_code())
                        return_log.set_status_message(a_cl.get_status_message())
                        return return_log
                    return_log.add_log(a_cl)

        ''' Return changelog. '''
        return_log.set_status_code(CreateConstants.SUCCESS_CODE)
        return_log.set_status_message(StringValue('Success!'))
        return return_log

    @classmethod
    def _check_params_update(cls, params):
        cl = MvKUpdateLog()
        if not (isinstance(params, mvk.interfaces.datavalue.MappingValue) and
                isinstance(params.typed_by(), mvk.interfaces.datatype.MappingType)):
            cl.set_status_code(UpdateConstants.MALFORMED_REQUEST_CODE)
            cl.set_status_message(StringValue('Expected a MappingValue'))
            return cl
        try:
            cls._check_param(params,
                             CreateConstants.ATTRS_KEY,
                             mvk.interfaces.datavalue.MappingValue,
                             mvk.interfaces.datatype.MappingType)
            attributes = params[CreateConstants.ATTRS_KEY]
            cls._check_param(attributes,
                             StringValue('name'),
                             mvk.interfaces.datavalue.StringValue,
                             mvk.interfaces.datatype.StringType,
                             req=False)
            cls._check_param(attributes,
                             StringValue('potency'),
                             (mvk.interfaces.datavalue.IntegerValue,
                              mvk.interfaces.datavalue.InfiniteValue),
                             (mvk.interfaces.datatype.IntegerType,
                              mvk.interfaces.datatype.InfiniteType),
                             req=False,
                             extra_check=lambda x: None if x >= IntegerValue(0) else StringValue('Potency value needs to be >= 0!'))
        except MvKException, e:
            cl.set_status_code(UpdateConstants.BAD_REQUEST_CODE)
            cl.set_status_message(e.get_message())
            return cl
        return None

    def _update(self, params):
        from mvk.impl.python.python_representer import PythonRepresenter
        cl = MvKUpdateLog()
        cl.set_location(self.get_location())
        cl.set_type(self.typed_by().get_location())

        attributes = params[UpdateConstants.ATTRS_KEY]
        for name in attributes:
            if self.typed_by().get_location().startswith(LocationValue('mvk.object')):
                if name == StringValue('name'):
                    new_val = attributes[name]
                    cl.add_attr_change(name, self.get_name(), new_val)
                    self.set_name(new_val)
                elif name == StringValue('potency'):
                    new_val = attributes[name]
                    cl.add_attr_change(name, self.get_potency(), new_val)
                    self.set_potency(new_val)
                else:
                    cl.set_status_code(UpdateConstants.BAD_REQUEST_CODE)
                    cl.set_status_message(StringValue('Don\'t know how to update model\'s physical attribute %s.' %
                                                      name))
                    return cl
            else:
                attr = self.get_attribute(name)
                old_val = attr.get_value()
                new_val = attributes[name]
                attr.set_value(new_val)
                from mvk.mvk import MvK
                u_actions = MvK().get_physical_mapper(self.typed_by().get_location()).get_physical_update_actions()
                if name in u_actions:
                    eval('self.%s(new_val)' % str(u_actions[name]))
                cl.add_attr_change(name, old_val, new_val)

        ''' This second set_location in case name was changed. '''
        cl.set_location(self.get_location())
        cl.set_status_code(UpdateConstants.SUCCESS_CODE)
        cl.set_status_message(StringValue('Successfully updated Attribute.'))
        return cl

    def read(self, location):
        assert (isinstance(location, LocationValue) and
                isinstance(location.typed_by(), LocationType))

        rl = MvKReadLog()
        if location == LocationValue(''):
            ''' Base case. '''
            rl.set_item(self)
            rl.set_location(self.get_location())
            rl.set_type(self.typed_by().get_location())
            rl.set_status_code(ReadConstants.SUCCESS_CODE)
            rl.set_status_message(StringValue('Success!'))
            return rl
        else:
            idx = location.find(StringValue('.'))
            el_name = location if idx == IntegerValue(-1) else location.substring(stop=idx)
            if el_name in self.name_lookup:
                return self.name_lookup[el_name].read(LocationValue('') if idx == IntegerValue(-1) else location.substring(start=idx + IntegerValue(1)))
            else:
                rl = Node.read(self, location)
                if rl.is_success():
                    return rl
                assert logger.error('Element with name %s not found in model %s.' %
                                    (el_name, self.get_location()))
                rl.set_status_message(StringValue('Element with name %s not found in model %s.' %
                                                  (el_name, self.get_location())))
                return rl

    def _remove_from_parent(self):
        self.get_parent().remove_element(self.get_name())

    def delete(self):
        return Node.delete(self)


class ModelReference(Model, mvk.interfaces.object.ModelReference):
    """ === CONSTRUCTOR === """
    def __init__(self, path, **kwds):
        assert (isinstance(path, mvk.interfaces.datavalue.LocationValue) and
                isinstance(path.typed_by(), LocationType))
        self.path = path

    """ === PUBLIC INTERFACE === """
    def dereference(self):
        ''' TODO: This breaks the Liskov substitution principle, what to do
        about this? We can't silently fail... And we need to allow references
        to items which do not yet exist in the modelverse... '''
        from mvk.mvk import MvK
        rl = MvK().read(self.path)
        if rl.is_success():
            return rl.get_item()
        else:
            raise MvKLookupError(StringValue('Element on path %s not found.' %
                                             self.path))

    def get_name(self):
        return self.dereference().get_name()

    def get_location(self):
        return self.path

    def get_parent(self):
        return self.dereference().get_parent()

    def get_path(self):
        return self.path

    def get_potency(self):
        return self.dereference().get_potency()

    def get_elements(self):
        return self.dereference().get_elements()

    def get_element(self, name):
        return self.dereference().get_element(name)

    def typed_by(self):
        return self.dereference().typed_by()

    def is_type_of(self, el):
        return self.dereference().is_type_of(el)

    def get_attributes(self):
        return self.dereference().get_attributes()

    def get_all_attributes(self):
        return self.dereference().get_all_attributes()

    def get_attribute(self, attr_loc):
        return self.dereference().get_attribute(attr_loc)

    def get_out_associations(self):
        return self.dereference().get_out_associations()

    def get_in_associations(self):
        return self.dereference().get_in_associations()

    def get_outgoing_elements(self):
        return self.dereference().get_outgoing_elements()

    def get_incoming_elements(self):
        return self.dereference().get_incoming_elements()

    def get_neighbors(self):
        return self.dereference().get_neighbors()

    """ === PYTHON SPECIFIC === """
    def add_element(self, element):
        self.dereference().add_element(element)

    def add_elements(self, elements):
        self.dereference().add_elements(elements)

    def remove_element(self, name):
        self.dereference().remove_element(name)

    def update_element(self, name):
        self.dereference().update_element(name)

    def set_potency(self, potency):
        self.dereference().set_potency(potency)

    def set_name(self, name):
        self.dereference().set_name(name)

    def set_parent(self, parent):
        self.dereference().set_parent(parent)

    def add_in_association(self, association):
        self.dereference().add_in_association(association)

    def add_out_association(self, association):
        self.dereference().add_in_association(association)

    def remove_in_association(self, association_location):
        self.dereference().remove_in_association(association_location)

    def update_in_association(self, old_location, association):
        self.dereference().update_in_association(old_location, association)

    def remove_out_association(self, association_location):
        self.dereference().remove_out_association(association_location)

    def update_out_association(self, old_location, association):
        self.dereference().update_out_association(old_location, association)

    def add_attribute(self, attr):
        self.dereference().add_attribute(attr)

    def add_attributes(self, attrs):
        self.dereference().add_attributes(attrs)

    def remove_attribute(self, attr_name):
        self.dereference().remove_attribute(attr_name)

    def update_attribute(self, old_name, attr):
        self.dereference().update_attribute(old_name, attr)

    def __repr__(self):
        ''' TODO: Remove this, once dereference is stable. '''
        return 'ModelReference(%s)' % self.path


class Multiplicity(Element,
                   mvk.interfaces.object.Multiplicity):
    ''' == CONSTRUCTOR == '''
    def __init__(self, lower=None, upper=None, ordered=None, **kwargs):
        if lower is None:
            lower = IntegerValue(0)
        if upper is None:
            upper = InfiniteValue('+')
        if ordered is None:
            ordered = BooleanValue(False)
        self.set_lower(lower)
        self.set_upper(upper)
        self.set_ordered(ordered)
        super(Multiplicity, self).__init__(**kwargs)

    """ == PUBLIC INTERFACE == """
    def get_lower(self):
        return self.lower

    def get_upper(self):
        return self.upper

    def is_ordered(self):
        return self.ordered

    def typed_by(self):
        '''
        This is not implemented, because basically, we will never need the
        type of a Multiplicity. It doesn't matter, because it either
        acts as an association end (in which case, it is actually an attribute
        of the association, or more precisely, all the attributes of the
        multiplicity can be brought over as properties of the association), or
        as base class for Clabject and Attribute, in which case it is quite
        abstract.
        '''
        raise NotImplementedError()

    def __eq__(self, other):
        if logger.isEnabledFor(logging.DEBUG):
            try:
                assert logger.debug('in Multiplicity.__eq__()')
                assert logger.debug('lower %s ?= %s' %
                                    (self.get_lower(), other.get_lower()))
                assert logger.debug('upper %s ?= %s' %
                                    (self.get_upper(), other.get_upper()))
                assert logger.debug('ordered %s ?= %s' %
                                    (self.is_ordered(), other.is_ordered()))
            except Exception:
                assert logger.error(traceback.format_exc())

        return (BooleanValue(isinstance(other, Multiplicity)) and
                self.get_lower() == other.get_lower() and
                self.get_upper() == other.get_upper() and
                self.is_ordered() == other.is_ordered())

    """ == PYTHON SPECIFIC == """
    def set_lower(self, lower):
        '''
        Sets the lower bound of this multiplicity.
        @type lower: L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}
        @param lower: The new lower bound of this multiplicity.
        '''
        assert (isinstance(lower, mvk.interfaces.datavalue.IntegerValue) and
                isinstance(lower.typed_by(), IntegerType))
        assert lower >= IntegerValue(0)
        self.lower = lower

    def set_upper(self, upper):
        '''
        Sets the upper bound of this multiplicity.
        @type upper: L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}
        @param upper: The new lower bound of this multiplicity.
        '''
        assert ((isinstance(upper, mvk.interfaces.datavalue.IntegerValue) and
                isinstance(upper.typed_by(), IntegerType)) or
                (isinstance(upper, mvk.interfaces.datavalue.InfiniteValue) and
                isinstance(upper.typed_by(), InfiniteType)))
        assert upper >= IntegerValue(0)
        self.upper = upper

    def set_ordered(self, ordered):
        '''
        Sets whether or not this multiplicity is ordered.
        @type ordered: L{BooleanValue<mvk.interfaces.datavalue.BooleanValue>}
        @param ordered: Whether or not this multiplicity is ordered.
        '''
        assert (isinstance(ordered, mvk.interfaces.datavalue.BooleanValue) and
                isinstance(ordered.typed_by(), BooleanType))
        self.ordered = ordered


class Clabject(Node, Multiplicity, mvk.interfaces.object.Clabject):
    """ == CONSTRUCTOR == """
    def __init__(self, abstract=None, potency=None, **kwds):
        if potency is None:
            potency = InfiniteValue('+')
        super(Clabject, self).__init__(potency=potency, **kwds)
        assert (not abstract is None) or potency == IntegerValue(0)
        if abstract is None:
            assert potency == IntegerValue(0)
            self.set_abstract(BooleanValue(False))
        else:
            self.set_abstract(abstract)
        ''' mapping of loc:clabject '''
        self.superclasses = MappingValue(value={})
        self.specialiseclasses = MappingValue(value={})
        self.name_lookup = MappingValue(value={})

    """ == PUBLIC INTERFACE == """
    def get_potency(self):
        return self.potency

    def is_abstract(self):
        if not self.get_potency() > IntegerValue(0):
            raise MvKPotencyError(StringValue('Potency should be > 0'))
        return self.abstract

    def get_specialise_classes(self):
        if not self.get_potency() > IntegerValue(0):
            raise MvKPotencyError(StringValue('Potency should be > 0'))
        return ImmutableSequenceValue(self.specialiseclasses.values())

    def get_super_classes(self):
        if not self.get_potency() > IntegerValue(0):
            raise MvKPotencyError(StringValue('Potency should be > 0'))
        return ImmutableSequenceValue(self.superclasses.values())

    def get_all_specialise_classes(self):
        if not self.get_potency() > IntegerValue(0):
            raise MvKPotencyError(StringValue('Potency should be > 0'))

        def get_all_specialise_classes_helper():
            return_value = MappingValue(value=self.specialiseclasses.get_value())
            for sp_c in self.specialiseclasses.values().get_value():
                specialiseclasses = sp_c.get_all_specialise_classes()
                for s in specialiseclasses:
                    if s.get_location() not in return_value:
                        return_value[s.get_name()] = s
            return return_value

        return ImmutableSequenceValue(get_all_specialise_classes_helper().values())

    def get_all_super_classes(self):
        if not self.get_potency() > IntegerValue(0):
            raise MvKPotencyError(StringValue('Potency should be > 0'))

        def get_all_super_classes_helper():
            return_value = MappingValue(value=self.superclasses.get_value())
            for sp_c in self.superclasses.values().get_value():
                superclasses = sp_c.get_all_super_classes()
                for s in superclasses:
                    if s.get_location() not in return_value:
                        return_value[s.get_location()] = s
            return return_value

        return ImmutableSequenceValue(get_all_super_classes_helper().values())

    def get_all_attributes(self):
        def get_all_attributes_helper():
            return_value = dict(self.attributes.get_value())
            super_classes = self.superclasses.values().get_value()
            for s in super_classes:
                for a in s.get_all_attributes():
                    if a.get_short_location() not in return_value:
                        return_value[a.get_short_location()] = a
            return return_value

        return ImmutableSequenceValue(SequenceValue(value=get_all_attributes_helper().values()))

    def get_attribute(self, attr_loc):
        assert (isinstance(attr_loc, mvk.interfaces.datavalue.StringValue) and
                isinstance(attr_loc.typed_by(), StringType))
        if attr_loc in self.attributes:
            return self.attributes[attr_loc]
        if self.potency > IntegerValue(0):
            for sc in self.superclasses.values().get_value():
                try:
                    return sc.get_attribute(attr_loc)
                except MvKKeyError:
                    pass
        raise MvKKeyError(StringValue('Attribute %s not found!' % attr_loc))

    def issubclass(self, other):
        if not self.get_potency() > IntegerValue(0):
            raise MvKPotencyError(StringValue('Potency should be > 0'))
        assert isinstance(other, mvk.interfaces.object.Clabject)
        return other == self or self in other.get_all_specialise_classes()

    def issuperclass(self, other):
        if not self.get_potency() > IntegerValue(0):
            raise MvKPotencyError(StringValue('Potency should be > 0'))
        assert isinstance(other, mvk.interfaces.object.Clabject)
        return other == self or self in other.get_all_super_classes()

    def is_type_of(self, el):
        t = el.typed_by()
        return (isinstance(t, mvk.interfaces.object.Clabject) and
                t.issubclass(self))

    def get_all_out_associations(self):
        if self.get_potency() == IntegerValue(0):
            return self.get_out_associations()

        def get_all_out_associations_helper():
            return_value = MappingValue(value=self.out_associations.get_value())
            for sp_c in self.superclasses.values().get_value():
                for o_a in sp_c.get_all_out_associations():
                    if o_a.get_location() not in return_value:
                        return_value[o_a.get_location()] = o_a
            return return_value

        return ImmutableSequenceValue(get_all_out_associations_helper().values())

    def get_all_in_associations(self):
        if self.get_potency() == IntegerValue(0):
            return self.get_in_associations()

        def get_all_in_associations_helper():
            return_value = MappingValue(value=self.in_associations.get_value())
            for sp_c in self.superclasses.values().get_value():
                for i_a in sp_c.get_all_in_associations():
                    if i_a.get_location() not in return_value:
                        return_value[i_a.get_location()] = i_a
            return return_value

        return ImmutableSequenceValue(get_all_in_associations_helper().values())

    def get_all_associations(self):
        return ImmutableSequenceValue(self.get_all_out_associations() +
                                      self.get_all_in_associations())

    def get_elements(self):
        return ImmutableMappingValue(self.name_lookup)

    def get_element(self, name):
        if not isinstance(name, mvk.interfaces.datavalue.StringValue):
            raise MvKTypeError(StringValue('Expected a StringValue, received a %s' % type(name)))
        try:
            return self.name_lookup[name]
        except KeyError:
            raise MvKNameError(StringValue('Element with name %s not found in package' % name))

    def __eq__(self, other):
        if not isinstance(other, mvk.interfaces.object.Clabject):
            return BooleanValue(False)
        elif BooleanValue(id(self) == id(other)) or \
              self.get_location() == other.get_location():
            if logger.isEnabledFor(logging.DEBUG):
                assert logger.debug('in Clabject.__eq__ %s' % self.get_location())
                assert logger.debug('Elements on the same location %s!' %
                                    self.get_location())
            return BooleanValue(True)
        elif self.get_location().startswith(LocationValue('mvk')) or other.get_location().startswith(LocationValue('mvk')):
            '''
            Special case: one or both of the elements are elements of
            the physical type model, but they are not on the same location.
            That means they are not equal.
            '''
            return BooleanValue(False)

        attribute_fun_self = self.__class__.get_attributes if self.get_potency() == IntegerValue(0) else self.__class__.get_all_attributes
        in_assoc_fun_self = self.__class__.get_in_associations if self.get_potency() == IntegerValue(0) else self.__class__.get_all_in_associations
        out_assoc_fun_self = self.__class__.get_out_associations if self.get_potency() == IntegerValue(0) else self.__class__.get_all_out_associations

        attribute_fun_other = other.__class__.get_attributes if other.get_potency() == IntegerValue(0) else other.__class__.get_all_attributes
        in_assoc_fun_other = other.__class__.get_in_associations if other.get_potency() == IntegerValue(0) else other.__class__.get_all_in_associations
        out_assoc_fun_other = other.__class__.get_out_associations if other.get_potency() == IntegerValue(0) else other.__class__.get_all_out_associations

        if logger.isEnabledFor(logging.DEBUG):
            try:
                assert logger.debug('in Clabject.__eq__ (%s =? %s)' %
                                    (self.get_location(), other.get_location()))
                assert logger.debug('%s %s isinstance %s' %
                                    (self.get_location(), other.get_location(),
                                     isinstance(other, Clabject)))
                assert logger.debug('%s %s abstract %s' %
                                    ((self.get_location(), other.get_location(),
                                     (self.get_potency() == IntegerValue(0) or
                                      self.is_abstract() == other.is_abstract()))))
                assert logger.debug('%s %s superclasses %s' %
                                    (self.get_location(), other.get_location(),
                                     ((self.get_potency() == IntegerValue(0) or
                                      lists_eq_items(self.get_all_super_classes(), other.get_all_super_classes())))))
                assert logger.debug('%s %s attributes %s' %
                                    (self.get_location(), other.get_location(),
                                     lists_eq_items(attribute_fun_self(self), attribute_fun_other(other))))
                assert logger.debug('%s %s in_associations %s' %
                                    (self.get_location(), other.get_location(),
                                     lists_eq_items(in_assoc_fun_self(self), in_assoc_fun_other(other))))
                assert logger.debug('%s ?= %s' % (in_assoc_fun_self(self), in_assoc_fun_other(other)))
                assert logger.debug('%s %s out_associations %s' %
                                    (self.get_location(), other.get_location(),
                                     lists_eq_items(out_assoc_fun_self(self), out_assoc_fun_other(other))))
                assert logger.debug('%s ?= %s' % (out_assoc_fun_self(self), out_assoc_fun_other(other)))
            except Exception:
                assert logger.error(traceback.format_exc())

        try:
            return (super(Clabject, self).__eq__(other) and
                    (self.get_potency() == IntegerValue(0) or self.is_abstract() == other.is_abstract()) and
                    (self.get_potency() == IntegerValue(0) or lists_eq_items(self.get_all_super_classes(), other.get_all_super_classes())) and
                    lists_eq_items(attribute_fun_self(self), attribute_fun_other(other)) and
                    lists_eq_items(in_assoc_fun_self(self), in_assoc_fun_other(other)) and
                    lists_eq_items(out_assoc_fun_self(self), out_assoc_fun_other(other)))
        except MvKLookupError:
            pass

    """ == PYTHON SPECIFIC == """
    def set_name(self, name):
        old_name = self.get_name()
        if old_name != name:
            super(Clabject, self).set_name(name)
            if self.get_parent() is not None:
                self.get_parent().update_element(old_name, self)

    def add_super_class(self, superclass):
        '''
        Adds a super class to this clabject. Automatically keeps the
        super class's specialise classes in sync.
        @type superclass: L{Clabject<mvk.interfaces.object.Clabject>}
        @param superclass: The new superclass.
        @raises MvKPotencyError: If this clabject's potency value is 0.
        '''
        assert isinstance(superclass, mvk.interfaces.object.Clabject)
        if self.potency == IntegerValue(0):
            raise MvKPotencyError(StringValue('Cannot add a superclass to a clabject with potency 0!'))
        self.superclasses[superclass.get_location()] = superclass
        superclass.add_specialise_class(self)

    def add_specialise_class(self, subclass):
        '''
        Adds a subclass to this clabject. NEVER class this, instead
        call subclass.add_super_class()
        @type subclass: L{Clabject<mvk.interfaces.object.Clabject>}
        @param subclass: The new subclass.
        @raises MvKPotencyError: If this clabject's potency value is 0.
        '''
        assert isinstance(subclass, mvk.interfaces.object.Clabject)
        if self.potency == IntegerValue(0):
            raise MvKPotencyError(StringValue('Cannot add a subclass to a clabject with potency 0!'))
        self.specialiseclasses[subclass.get_location()] = subclass

    def remove_superclass(self, superclass_location):
        '''
        Remove a super class from this clabject. Automatically keeps the
        super class's specialise classes in sync.
        @type superclass_location: L{LocationValue<mvk.interfaces.datavalue.LocationValue>}
        @param superclass_location: The location of the superclass to remove.
        @raises MvKPotencyError: If this clabject's potency value is 0.
        '''
        assert (isinstance(superclass_location, mvk.interfaces.datavalue.LocationValue) and
                isinstance(superclass_location.typed_by(), LocationType))
        if self.potency == IntegerValue(0):
            raise MvKPotencyError(StringValue('Cannot remove a superclass from a clabject with potency 0!'))
        try:
            sc = self.superclasses[superclass_location]
            del self.superclasses[superclass_location]
            sc.remove_specialiseclass(self.get_location())
        except ValueError:
            raise MvKValueError(StringValue('Superclass not found!'))

    def remove_specialiseclass(self, subclass_location):
        '''
        Removes a subclass from this clabject. NEVER class this, instead
        call subclass.remove_superclass()
        @type subclass_location: L{LocationValue<mvk.interfaces.datavalue.LocationValue>}
        @param superclass_location: The location of the subclass to remove.
        @raises MvKPotencyError: If this clabject's potency value is 0.
        '''
        assert (isinstance(subclass_location, mvk.interfaces.datavalue.LocationValue) and
                isinstance(subclass_location.typed_by(), LocationType))
        if self.potency == IntegerValue(0):
            raise MvKPotencyError(StringValue('Cannot remove a subclass to a clabject with potency 0!'))
        try:
            del self.specialiseclasses[subclass_location]
        except ValueError:
            raise MvKValueError(StringValue('Subclass not found!'))

    def set_abstract(self, abstract):
        '''
        Sets whether or not this clabject is abstract. Only works for
        clabjects that have a type facet.
        @type abstract: L{BooleanValue<mvk.interfaces.datavalue.BooleanValue>}
        @param abstract: Whether or not this clabject is abstract.
        @raises MvKPotencyError: If this clabject's potency value is 0.
        '''
        if abstract == BooleanValue(True) and self.potency == IntegerValue(0):
            raise MvKPotencyError(StringValue('A clabject with potency 0 cannot be abstract!'))
        assert(isinstance(abstract, mvk.interfaces.datavalue.BooleanValue) and
               isinstance(abstract.typed_by(), BooleanType))
        self.abstract = abstract

    def __repr__(self):
        return '(Clabject) %s %s@%s(%s)' % (self.typed_by(), self.get_location(),
                                            self.get_potency(),
                                            '' if self.get_potency() == IntegerValue(0) else self.get_super_classes())

    def add_element(self, element):
        '''
        Adds an element to this clabject. Automatically sets the parent
        of the newly added element to this clabject.
        @type element: L{NamedElement<mvk.interfaces.element.NamedElement>}
        @param element: A named element.
        @raise MvKNameError: If an element with the same name already exists.
        '''
        assert isinstance(element, mvk.interfaces.element.NamedElement)
        if element.get_name() in self.name_lookup:
            raise MvKNameError(StringValue('An element with name %s already \
                                            exists in clabject %s.' %
                                            (element.get_name(), self.get_name())))
        self.name_lookup[element.get_name()] = element
        element.set_parent(self)
        assert element.get_parent() == self

    def add_elements(self, elements):
        '''
        Adds a list of elements to this clabject.
        @type elements: list
        @param elements: A list of L{NamedElement<mvk.interfaces.element.NamedElement>}s.
        @raise MvKNameError: If one of the elements has the same name as an element in this clabject.
        '''
        names = SetValue(set([el.get_name() for el in elements]))
        name_check = names.intersection(self.name_lookup.keys())
        if not name_check.len() == IntegerValue(0):
            raise MvKNameError(StringValue('Elements with name(s) %s already \
                                            exist in clabject %s.' %
                                            (name_check, self.get_name())))
        for el in elements:
            self.add_element(el)

    def remove_element(self, name):
        '''
        Removes the element with given name from this clabject. It is an error
        if no element with the given name exists in the model. Also sets the
        parent of the removed element to None.
        @type name: L{StringValue<mvk.interfaces.datavalue.StringValue>}
        @param name: The name of the element to be removed from this clabject.
        @raise MvKKeyError: If the element with given name was not found in
        this clabject.
        '''
        import mvk.interfaces.datavalue
        assert (isinstance(name, mvk.interfaces.datavalue.StringValue) and
                isinstance(name.typed_by(), mvk.interfaces.datatype.StringType))
        assert logger.debug('Removing element %s from clabject %s.' %
                            (name, self.get_name()))
        if not name in self.name_lookup:
            raise MvKKeyError(StringValue('Element not found!'))
        self.name_lookup[name].set_parent(None)
        del self.name_lookup[name]

    def update_element(self, old_name, element):
        '''
        Removes the element with name 'old_name', and adds the given element.
        @type old_name: L{StringValue<mvk.interfaces.datavalue.StringValue>}
        @param old_name: The old name of the element.
        @type element: L{NamedElement<mvk.interfaces.element.NamedElement>}
        @raise MvKKeyError: If the element with name 'old_name' was not found.
        '''
        assert (isinstance(old_name, mvk.interfaces.datavalue.StringValue) and
                isinstance(old_name.typed_by(), mvk.interfaces.datatype.StringType))
        assert isinstance(element, NamedElement)
        ''' we do a check on the location, because 'element.get_parent() == self'
        would also return True if the contents are equal '''
        assert (element.get_parent() is None or
                element.get_parent().get_location() == self.get_location())
        if not old_name in self.name_lookup:
            raise MvKKeyError(StringValue('Element not found!'))
        if element.get_name() in self.name_lookup:
            raise MvKNameError(StringValue('Element with name %s already \
                                            exist in clabject %s.' %
                                            (element.get_name(), self.get_name())))
        del self.name_lookup[old_name]
        self.name_lookup[element.get_name()] = element

    """ === CRUD === """
    @classmethod
    def _check_params_create(cls, params):
        cl = MvKCreateLog()
        if not (isinstance(params, mvk.interfaces.datavalue.MappingValue) and
                isinstance(params.typed_by(), mvk.interfaces.datatype.MappingType)):
            cl.set_status_code(CreateConstants.MALFORMED_REQUEST_CODE)
            cl.set_status_message(StringValue('Expected a MappingValue'))
            return cl
        try:
            c_params = MappingValue({})
            for k in params:
                c_params[k] = params[k]
            cls._check_param(c_params,
                             CreateConstants.LOCATION_KEY,
                             mvk.interfaces.datavalue.LocationValue,
                             mvk.interfaces.datatype.LocationType)
            cls._check_param(c_params,
                             CreateConstants.TYPE_KEY,
                             mvk.interfaces.datavalue.LocationValue,
                             mvk.interfaces.datatype.LocationType)
            cls._check_param(c_params,
                             CreateConstants.ATTRS_KEY,
                             mvk.interfaces.datavalue.MappingValue,
                             mvk.interfaces.datatype.MappingType)
            attributes = c_params[CreateConstants.ATTRS_KEY]
            cls._check_param(attributes,
                             StringValue('class'),
                             mvk.interfaces.datavalue.LocationValue,
                             mvk.interfaces.datatype.LocationType)
            ''' Here, check the attributes of the type, and how they are mapped
            onto physical attributes. '''
            if not attributes[StringValue('class')].startswith(LocationValue('mvk.object')):
                from mvk.mvk import MvK
                the_type = attributes[StringValue('class')]
                phys_mapper = MvK().get_physical_mapper(the_type)
                type_rl = MvK().read(the_type)
                if not type_rl.is_success():
                    cl.set_status_code(type_rl.get_status_code())
                    cl.set_status_message(type_rl.get_status_message())
                    return cl
                t = type_rl.get_item()
                assert isinstance(t, mvk.interfaces.object.Clabject)
                for attr in t.get_all_attributes():
                    assert logger.debug('%s is an attribute of %s' %
                                        (attr.get_name(), t))
                    if attr.get_potency() > IntegerValue(0):
                        try:
                            attr_name = attr.get_short_location()
                            assert logger.debug('Looking for %s in %s...' % (attr_name, phys_mapper.get_physical_attribute_mapping()))
                            m = phys_mapper.get_physical_attribute_mapping()[attr_name]
                            assert m.len() == IntegerValue(1)
                            if attr_name in attributes:
                                attributes[m[IntegerValue(0)]] = attributes[attr_name]
                            else:
                                attributes[m[IntegerValue(0)]] = attr.get_default()
                            ''' TODO: Delete attributes[m[IntegerValue(0)]] if attr_name != m[IntegerValue(0)]? '''
                        except MvKKeyError, e:
                            assert logger.debug('%s not found in %s' %
                                         (attr_name, phys_mapper.get_physical_attribute_mapping()))
            cls._check_param(attributes,
                             StringValue('name'),
                             mvk.interfaces.datavalue.StringValue,
                             mvk.interfaces.datatype.StringType)
            cls._check_param(attributes,
                             StringValue('potency'),
                             (mvk.interfaces.datavalue.IntegerValue,
                              mvk.interfaces.datavalue.InfiniteValue),
                             (mvk.interfaces.datatype.IntegerType,
                              mvk.interfaces.datatype.InfiniteType),
                             req=False,
                             extra_check=lambda x: None if x >= IntegerValue(0) else StringValue('Potency value needs to be >= 0!'))
            cls._check_param(attributes,
                             StringValue('lower'),
                             mvk.interfaces.datavalue.IntegerValue,
                             mvk.interfaces.datatype.IntegerType,
                             req=False,
                             extra_check=lambda x: None if x >= IntegerValue(0) and x < InfiniteValue('+') else StringValue('Lower value needs to be >= 0 and < +inf!'))
            cls._check_param(attributes,
                             StringValue('upper'),
                             (mvk.interfaces.datavalue.IntegerValue,
                              mvk.interfaces.datavalue.InfiniteValue),
                             (mvk.interfaces.datatype.IntegerType,
                              mvk.interfaces.datatype.InfiniteType),
                             req=False,
                             extra_check=lambda x: None if x >= IntegerValue(0) else StringValue('Upper value needs to be >= 0!'))
            cls._check_param(attributes,
                             StringValue('ordered'),
                             mvk.interfaces.datavalue.BooleanValue,
                             mvk.interfaces.datatype.BooleanType,
                             req=False)
            cls._check_param(attributes,
                             StringValue('abstract'),
                             mvk.interfaces.datavalue.BooleanValue,
                             mvk.interfaces.datatype.BooleanType,
                             req=(StringValue('potency') not in attributes or
                                  attributes[StringValue('potency')] is None or
                                  attributes[StringValue('potency')] > IntegerValue(0)))
        except MvKException, e:
            cl.set_status_code(CreateConstants.BAD_REQUEST_CODE)
            cl.set_status_message(e.get_message())
            return cl
        return None

    @classmethod
    def _create(cls, params):
        assert logger.debug('In Clabject._create %s' % params)
        ''' Initialize needed changelog values. '''
        from mvk.impl.python.python_representer import PythonRepresenter
        cl = MvKCreateLog()
        location = params[CreateConstants.LOCATION_KEY]
        the_type = params[CreateConstants.TYPE_KEY]
        cl.set_location(location)
        cl.set_type(the_type)
        return_log = MvKCreateCompositeLog()
        return_log.set_location(cl.get_location())
        return_log.set_type(cl.get_type())

        ''' Create new clabject. '''
        attributes = params[CreateConstants.ATTRS_KEY]
        name = attributes[StringValue('name')]
        if not StringValue('potency') in attributes:
            if not attributes[StringValue('class')].startswith(StringValue('mvk')):
                attributes[StringValue('potency')] = ClabjectReference(path=attributes[StringValue('class')]).get_potency() - IntegerValue(1)
        potency = attributes[StringValue('potency')] if StringValue('potency') in attributes else None
        clz = attributes[StringValue('class')]
        if potency is None or potency > IntegerValue(0):
            lower = attributes[StringValue('lower')] if StringValue('lower') in attributes else None
            upper = attributes[StringValue('upper')] if StringValue('upper') in attributes else None
            ordered = attributes[StringValue('ordered')] if StringValue('ordered') in attributes else None
            abstract = attributes[StringValue('abstract')] if StringValue('abstract') in attributes else None
            assert logger.debug('Creating Clabject with name %s, potency %s, type %s, lower %s, upper %s, ordered %s, abstract %s' %
                                (name, potency, clz, lower, upper, ordered, abstract))
            c = Clabject(name=name, potency=potency,
                         l_type=ClabjectReference(path=clz),
                         lower=lower, upper=upper,
                         ordered=ordered, abstract=abstract)
            if StringValue('superclasses') in attributes:
                for val in attributes[StringValue('superclasses')]:
                    c.add_super_class(ClabjectReference(path=val))
            cl.add_attr_change(StringValue('lower'), c.get_lower())
            cl.add_attr_change(StringValue('upper'), c.get_upper())
            cl.add_attr_change(StringValue('ordered'), c.is_ordered())
            cl.add_attr_change(StringValue('abstract'), c.is_abstract())
        else:
            assert logger.debug('Creating Clabject with name %s, potency %s, type %s' %
                                (name, potency, clz))
            c = Clabject(name=name, potency=potency,
                         l_type=ClabjectReference(path=clz))
        cl.set_name(c.get_name())
        cl.add_attr_change(StringValue('name'), c.get_name())
        cl.add_attr_change(StringValue('potency'), c.get_potency())
        cl.add_attr_change(StringValue('class'), c.typed_by().get_location())
        return_log.set_name(c.get_name())

        ''' Try setting the parent.  '''
        from mvk.mvk import MvK
        parent_log = MvK().read(location)
        if not parent_log.is_success():
            return_log.set_status_code(parent_log.get_status_code())
            return_log.set_status_message(parent_log.get_status_message())
            return return_log
        parent = parent_log.get_item()
        assert logger.debug('Setting parent to %s' % parent.get_location())
        '''
        if not isinstance(parent, mvk.interfaces.object.Model):
            return_log.set_status_code(CreateConstants.BAD_REQUEST_CODE)
            return_log.set_status_message(StringValue('Can only create a Clabject \
                                                       inside a Model.'))
            return return_log
        '''
        if isinstance(parent, mvk.interfaces.object.Model) or isinstance(parent, mvk.interfaces.object.Clabject):
            try:
                parent.add_element(c)
                cl.set_location(parent_log.get_location())
                cl.set_status_code(CreateConstants.SUCCESS_CODE)
                cl.set_status_message(StringValue('Success!'))
            except MvKNameError, e:
                cl.set_status_code(CreateConstants.BAD_REQUEST_CODE)
                cl.set_status_message(e.get_message())
                return cl
        '''
        elif isinstance(parent, mvk.interfaces.object.Clabject):
            rl = parent.read(LocationValue('') + c.get_name())
            if rl.is_success():
                cl.set_status_code(CreateConstants.BAD_REQUEST_CODE)
                cl.set_status_message(StringValue('Element with name %s already exists in %s.' % (str(c.get_name()), str(parent.get_location))))
                return cl
            else:
                # We only set the parent here because we know that a child clabject will always be added through a composition link. It's not necessary to keep any other
                # information in the parent.
                cl.set_location(parent_log.get_location())
                cl.set_status_code(CreateConstants.SUCCESS_CODE)
                cl.set_status_message(StringValue('Success!'))
                c.set_parent(parent)
        '''
        return_log.add_log(cl)

        '''
        Time for attributes which need to be instantiated from the type.
        '''
        if not clz.startswith(LocationValue('mvk.object')):
            try:
                all_attributes = c.typed_by().get_all_attributes()
            except MvKLookupError:
                ''' TODO: This has to do with classes which are not yet
                created in the modelverse. Do we want to have it like this? '''
                all_attributes = SequenceValue([])
            for a in all_attributes:
                potency = a.get_potency()
                if (potency > IntegerValue(0) and
                    (potency != IntegerValue(1) or a.get_short_location() in attributes or a.get_lower() > IntegerValue(0))):
                    c_attributes = MappingValue({StringValue('name'): a.get_short_location(),
                                                 StringValue('class'): a.get_location()})
                    c_params = MappingValue({CreateConstants.LOCATION_KEY: c.get_location(),
                                             CreateConstants.ATTRS_KEY: c_attributes})
                    if potency > IntegerValue(1):
                        c_attributes[StringValue('default')] = a.get_default()
                        c_attributes[StringValue('potency')] = potency - IntegerValue(1)
                        c_attributes[StringValue('lower')] = a.get_lower()
                        c_attributes[StringValue('upper')] = a.get_upper()
                        c_attributes[StringValue('ordered')] = a.is_ordered()
                    elif potency == IntegerValue(1):
                        if a.get_short_location() in attributes:
                            c_attributes[StringValue('value')] = attributes[a.get_short_location()]
                        else:
                            c_attributes[StringValue('value')] = a.get_default()
                    else:
                        c_attributes[StringValue('value')] = a.get_value()
                    assert logger.debug('Creating attribute with attributes %s in Clabject %s.' %
                                        (c_attributes, c.get_location()))
                    a_cl = Attribute.create(c_params)
                    if not a_cl.is_success():
                        ''' Something went wrong creating the attribute, undo
                        changes already performed... '''
                        c.delete()
                        return_log.set_status_code(a_cl.get_status_code())
                        return_log.set_status_message(a_cl.get_status_message())
                        return return_log
                    return_log.add_log(a_cl)

        return_log.set_status_code(CreateConstants.SUCCESS_CODE)
        return_log.set_status_message(StringValue("Success"))

        ''' Return changelog. '''
        return return_log

    @classmethod
    def _check_params_update(cls, params):
        cl = MvKUpdateLog()
        if not (isinstance(params, mvk.interfaces.datavalue.MappingValue) and
                isinstance(params.typed_by(), mvk.interfaces.datatype.MappingType)):
            cl.set_status_code(UpdateConstants.MALFORMED_REQUEST_CODE)
            cl.set_status_message(StringValue('Expected a MappingValue'))
            return cl
        try:
            cls._check_param(params,
                             CreateConstants.ATTRS_KEY,
                             mvk.interfaces.datavalue.MappingValue,
                             mvk.interfaces.datatype.MappingType)
            attributes = params[CreateConstants.ATTRS_KEY]
            cls._check_param(attributes,
                             StringValue('name'),
                             mvk.interfaces.datavalue.StringValue,
                             mvk.interfaces.datatype.StringType,
                             req=False)
            cls._check_param(attributes,
                             StringValue('potency'),
                             (mvk.interfaces.datavalue.IntegerValue,
                              mvk.interfaces.datavalue.InfiniteValue),
                             (mvk.interfaces.datatype.IntegerType,
                              mvk.interfaces.datatype.InfiniteType),
                             req=False,
                             extra_check=lambda x: None if x >= IntegerValue(0) else StringValue('potency value needs to be >= 0'))
            cls._check_param(attributes,
                             StringValue('lower'),
                             mvk.interfaces.datavalue.IntegerValue,
                             mvk.interfaces.datatype.IntegerType,
                             req=False,
                             extra_check=lambda x: None if x >= IntegerValue(0) and x < InfiniteValue('+') else StringValue('Lower value needs to be >= 0 and < +inf!'))
            cls._check_param(attributes,
                             StringValue('upper'),
                             (mvk.interfaces.datavalue.IntegerValue,
                              mvk.interfaces.datavalue.InfiniteValue),
                             (mvk.interfaces.datatype.IntegerType,
                              mvk.interfaces.datatype.InfiniteType),
                             req=False,
                             extra_check=lambda x: None if x >= IntegerValue(0) else StringValue('upper value needs to be >= 0 and < +inf!'))
            cls._check_param(attributes,
                             StringValue('ordered'),
                             mvk.interfaces.datavalue.BooleanValue,
                             mvk.interfaces.datatype.BooleanType,
                             req=False)
            cls._check_param(attributes,
                             StringValue('abstract'),
                             mvk.interfaces.datavalue.BooleanValue,
                             mvk.interfaces.datatype.BooleanType,
                             req=False)
        except MvKException, e:
            cl.set_status_code(UpdateConstants.BAD_REQUEST_CODE)
            cl.set_status_message(e.get_message())
            return cl
        return None

    def _update(self, params):
        from mvk.impl.python.python_representer import PythonRepresenter
        cl = MvKUpdateLog()
        cl.set_location(self.get_location())
        cl.set_type(self.typed_by().get_location())

        attributes = params[UpdateConstants.ATTRS_KEY]
        try:
            for name in attributes:
                if self.typed_by().get_location().startswith(StringValue('mvk')):
                    if name == StringValue('name'):
                        new_val = attributes[name]
                        cl.add_attr_change(name, self.get_name(), new_val)
                        self.set_name(new_val)
                    elif name == StringValue('potency'):
                        new_val = attributes[name]
                        cl.add_attr_change(name, self.get_potency(), new_val)
                        self.set_potency(new_val)
                    elif name == StringValue('lower'):
                        new_val = attributes[name]
                        cl.add_attr_change(name, self.get_potency(), new_val)
                        self.set_lower(new_val)
                    elif name == StringValue('upper'):
                        new_val = attributes[name]
                        cl.add_attr_change(name, self.get_potency(), new_val)
                        self.set_upper(new_val)
                    elif name == StringValue('ordered'):
                        new_val = attributes[name]
                        cl.add_attr_change(name, self.get_potency(), new_val)
                        self.set_ordered(new_val)
                    elif name == StringValue('abstract'):
                        new_val = attributes[name]
                        cl.add_attr_change(name, self.get_potency(), new_val)
                        self.set_abstract(new_val)
                    else:
                        ''' TODO: revert! '''
                        cl.set_status_code(UpdateConstants.BAD_REQUEST_CODE)
                        cl.set_status_message(StringValue('Don\'t know how to update clabject\'s physical attribute %s.' %
                                                          name))
                        return cl
                else:
                    attr = self.get_attribute(name)
                    old_val = attr.get_value()
                    new_val = attributes[name]
                    attr.set_value(new_val)
                    from mvk.mvk import MvK
                    u_actions = MvK().get_physical_mapper(self.typed_by().get_location()).get_physical_update_actions()
                    if name in u_actions:
                        eval('self.%s(new_val)' % str(u_actions[name]))
                    cl.add_attr_change(name, old_val, new_val)
            cl.set_status_code(UpdateConstants.SUCCESS_CODE)
            cl.set_status_message(StringValue('Successfully updated clabject.'))
        except MvKKeyError, e:
            ''' TODO: revert! '''
            cl.set_status_code(UpdateConstants.NOT_FOUND_CODE)
            cl.set_status_message(e.get_message())
        except MvKValueError, e:
            ''' TODO: revert! '''
            cl.set_status_code(UpdateConstants.NOT_FOUND_CODE)
            cl.set_status_message(e.get_message())
        except MvKPotencyError, e:
            ''' TODO: revert! '''
            cl.set_status_code(UpdateConstants.BAD_REQUEST_CODE)
            cl.set_status_message(e.get_message())

        ''' This second set_location in case name was changed. '''
        cl.set_location(self.get_location())
        return cl

    def read(self, location):
        if location != LocationValue(''):
            idx = location.find(StringValue('.'))
            el_name = location if idx == IntegerValue(-1) else location.substring(stop=idx)
            if el_name in self.name_lookup:
                return self.name_lookup[el_name].read(LocationValue('') if idx == IntegerValue(-1) else location.substring(start=idx + IntegerValue(1)))
        return Node.read(self, location)

    def _remove_from_parent(self):
        if isinstance(self.get_parent(), mvk.interfaces.object.Model):
            self.get_parent().remove_element(self.get_name())
        else:
            self.set_parent(None)

    def delete(self):
        return Node.delete(self)


class ClabjectReference(Clabject, mvk.interfaces.object.ClabjectReference):
    """ == CONSTRUCTOR == """
    def __init__(self, path, **kwds):
        assert (isinstance(path, mvk.interfaces.datavalue.LocationValue) and
                isinstance(path.typed_by(), LocationType))
        self.path = path

    """ == PUBLIC INTERFACE == """
    def dereference(self):
        ''' TODO: This breaks the Liskov substitution principle, what to do
        about this? We can't silently fail... And we need to allow references
        to items which do not yet exist in the modelverse... '''
        from mvk.mvk import MvK
        rl = MvK().read(self.path)
        if rl.is_success():
            return rl.get_item()
        else:
            raise MvKLookupError(StringValue('Element on path %s not found.' %
                                             self.path))

    def get_path(self):
        return self.path

    def is_abstract(self):
        return self.dereference().is_abstract()

    def get_specialise_classes(self):
        return self.dereference().get_specialise_classes()

    def get_super_classes(self):
        return self.dereference().get_super_classes()

    def get_all_specialise_classes(self):
        return self.dereference().get_all_specialise_classes()

    def get_all_super_classes(self):
        return self.dereference().get_all_super_classes()

    def get_attributes(self):
        return self.dereference().get_attributes()

    def get_all_attributes(self):
        return self.dereference().get_all_attributes()

    def get_attribute(self, attr_name):
        return self.dereference().get_attribute(attr_name)

    def typed_by(self):
        return self.dereference().typed_by()

    def is_type_of(self, el):
        return self.dereference().is_type_of(el)

    def get_out_associations(self):
        return self.dereference().get_out_associations()

    def get_in_associations(self):
        return self.dereference().get_in_associations()

    def get_all_out_associations(self):
        return self.dereference().get_all_out_associations()

    def get_all_in_associations(self):
        return self.dereference().get_all_in_associations()

    def get_outgoing_elements(self):
        return self.dereference().get_outgoing_elements()

    def get_incoming_elements(self):
        return self.dereference().get_incoming_elements()

    def get_neighbors(self):
        return self.dereference().get_neighbors()

    def get_functions(self):
        return self.dereference().get_functions()

    def get_function(self, f_name):
        return self.dereference().get_function(f_name)

    def get_potency(self):
        return self.dereference().get_potency()

    def get_lower(self):
        return self.dereference().get_lower()

    def get_upper(self):
        return self.dereference().get_upper()

    def is_ordered(self):
        return self.dereference().is_ordered()

    def get_name(self):
        return self.dereference().get_name()

    def get_location(self):
        return self.path

    def get_parent(self):
        return self.dereference().get_parent()

    """ == PYTHON SPECIFIC == """
    def set_potency(self, potency):
        self.dereference().set_potency(potency)

    def add_in_association(self, association):
        self.dereference().add_in_association(association)

    def add_out_association(self, association):
        self.dereference().add_out_association(association)

    def remove_out_association(self, association_location):
        self.dereference().remove_out_association(association_location)

    def remove_in_association(self, association_location):
        self.dereference().remove_in_association(association_location)

    def update_out_association(self, old_name, association):
        self.dereference().update_out_association(old_name, association)

    def update_in_association(self, old_name, association):
        self.dereference().update_in_association(old_name, association)

    def add_super_class(self, superclass):
        self.dereference().add_super_class(superclass)

    def add_specialise_class(self, subclass):
        self.dereference().add_specialise_class(subclass)

    def remove_superclass(self, superclass):
        self.dereference().remove_superclass(superclass)

    def add_attribute(self, attr):
        self.dereference().add_attribute(attr)

    def remove_attribute(self, prop_name):
        self.dereference().remove_attribute(prop_name)

    def update_attribute(self, old_name, attribute):
        self.dereference().update_attribute(old_name, attribute)

    def set_abstract(self, abstract):
        self.dereference().set_abstract(abstract)

    def set_name(self, name):
        self.dereference().set_name(name)

    def set_parent(self, parent):
        self.dereference().set_parent(parent)

    def __repr__(self):
        ''' TODO: Remove this once dereference is implemented. Maybe? '''
        return 'ClabjectReference(%s)' % self.path


class Attribute(Node, TypedElement, Multiplicity,
                mvk.interfaces.object.Attribute):
    """ == CONSTRUCTOR == """
    def __init__(self, l_type=None, the_type=None, potency=None, default=None,
                 value=None, lower=None, upper=None, **kwargs):
        if potency is None:
            potency = IntegerValue(1)
        if lower is None:
            lower = IntegerValue(1)
        if upper is None:
            upper = IntegerValue(1)  # differs from Multiplicity default
        if potency == IntegerValue(0):
            assert isinstance(l_type, mvk.interfaces.object.Attribute)
            the_type = l_type.get_type()
        else:
            assert the_type is not None
        super(Attribute, self).__init__(l_type=l_type, lower=lower, upper=upper,
                                        the_type=the_type, potency=potency, **kwargs)
        assert self.get_attributes()
        if potency > IntegerValue(0):
            assert default is not None
            self.set_default(default)
        else:
            assert value is not None
            self.set_value(value)

    """ == PUBLIC INTERFACE == """
    def get_potency(self):
        return self.potency

    def get_default(self):
        if self.get_potency() <= IntegerValue(0):
            raise MvKPotencyError(StringValue('Potency value should be larger than 0'))
        return self.default

    def get_value(self):
        if not self.get_potency() == IntegerValue(0):
            raise MvKPotencyError(StringValue('Potency value should be 0'))
        ''' TODO: Here, if value is uninitialized (i.e., self.value does
        not exist yet, it should be initialized before returned. '''
        return self.value

    def typed_by(self):
        return self.l_type

    def is_type_of(self, el):
        return (isinstance(el, mvk.interfaces.object.Attribute) and
                el.typed_by() == self)

    def __eq__(self, other):
        if logger.isEnabledFor(logging.DEBUG):
            try:
                assert logger.debug('in Attribute.__eq__()')
                assert logger.debug('isinstance %s' % isinstance(other, Attribute))
                assert logger.debug('name %s ?= %s (%s)' %
                                    (self.get_name(), other.get_name(),
                                     self.get_name() == other.get_name()))
                assert logger.debug('potency %s ?= %s (%s)' %
                                    (self.get_potency(), other.get_potency(),
                                     self.get_potency() == other.get_potency()))
                if self.get_potency() == other.get_potency():
                    assert logger.debug('value %s ?= %s (%s)' %
                                        ((self.default, other.get_default(), self.default == other.get_default()) if self.get_potency() > IntegerValue(0) else (self.get_value(), other.get_value(), self.get_value() == other.get_value())))
            except Exception:
                assert logger.error(traceback.format_exc())

        return BooleanValue(id(self) == id(other)) or (
                BooleanValue(isinstance(other, Attribute)) and
                 (self.get_location() == other.get_location() or
                  (super(Attribute, self).__eq__(other) and
                   self.potency == other.get_potency() and
                   ((self.potency > IntegerValue(0) and self.default == other.get_default()) or
                    (self.potency == IntegerValue(0) and self.value == other.get_value())))))

    """ == PYTHON SPECIFIC == """
    def set_name(self, name):
        old_name = self.get_name()
        if old_name != name:
            super(Attribute, self).set_name(name)
            if self.get_parent() is not None:
                self.get_parent().update_attribute(old_name, self)

    def set_potency(self, potency):
        '''
        Sets the potency value for this attribute.
        @type potency: L{IntegerValue<mvk.interfaces.datavalue.IntegerValue>}
        @param potency: The new potency value for this attribute.
        '''
        assert (isinstance(potency, mvk.interfaces.datavalue.IntegerValue) and
                isinstance(potency.typed_by(), IntegerType))
        assert potency >= IntegerValue(0)
        self.potency = potency

    def set_default(self, default):
        '''
        Sets the default value for this attribute.
        @type default: L{Element<mvk.interfaces.element.Element>}
        @param default: The new default value for this attribute.
        @raise MvKPotencyError: If the potency value of this attribute is 0.
        '''

        """ TODO: (Possibly) Assert that default is an instance of the type
        of this Attribute. """
        if self.get_potency() == IntegerValue(0):
            raise MvKPotencyError(StringValue('Potency value should not be 0'))
        self.default = default

    def set_value(self, value):
        '''
        Sets the value of this attribute.
        @type value: L{Element<mvk.interfaces.element.Element>}
        @param value: The new value of this attribute.
        @raise MvKPotencyError: If the potency value of this attribute is > 0.
        '''

        """ TODO: (Possibly) Assert that value is an instance of the type
        of this Attribute. """
        if not self.get_potency() == IntegerValue(0):
            raise MvKPotencyError(StringValue('Potency value should be 0'))
        self.value = value

    def __repr__(self):
        return 'Attribute %s@%s (%s)' % (self.get_name(), self.get_potency(), self.get_default() if self.get_potency() > IntegerValue(0) else self.get_value())

    """ === CRUD === """
    @classmethod
    def _check_params_create(cls, params):
        cl = MvKCreateLog()
        if not (isinstance(params, mvk.interfaces.datavalue.MappingValue) and
                isinstance(params.typed_by(), mvk.interfaces.datatype.MappingType)):
            cl.set_status_code(CreateConstants.MALFORMED_REQUEST_CODE)
            cl.set_status_message(StringValue('Expected a MappingValue'))
            return cl
        try:
            c_params = MappingValue({})
            for k in params:
                c_params[k] = params[k]
            cls._check_param(c_params,
                             CreateConstants.LOCATION_KEY,
                             mvk.interfaces.datavalue.LocationValue,
                             mvk.interfaces.datatype.LocationType)
            cls._check_param(c_params,
                             CreateConstants.TYPE_KEY,
                             mvk.interfaces.datavalue.LocationValue,
                             mvk.interfaces.datatype.LocationType,
                             req=False)
            cls._check_param(c_params,
                             CreateConstants.ATTRS_KEY,
                             mvk.interfaces.datavalue.MappingValue,
                             mvk.interfaces.datatype.MappingType)
            attributes = params[CreateConstants.ATTRS_KEY]
            cls._check_param(attributes,
                             StringValue('class'),
                             mvk.interfaces.datavalue.LocationValue,
                             mvk.interfaces.datatype.LocationType)
            ''' Here, check the attributes of the type, and how they are mapped
            onto physical attributes. '''
            if not attributes[StringValue('class')].startswith(LocationValue('mvk.object')):
                from mvk.mvk import MvK
                the_type = attributes[StringValue('class')]
                phys_mapper = MvK().get_physical_mapper(the_type)
                type_rl = MvK().read(the_type)
                if not type_rl.is_success():
                    cl.set_status_code(type_rl.get_status_code())
                    cl.set_status_message(type_rl.get_status_message())
                    return cl
                t = type_rl.get_item()
                if isinstance(t, mvk.interfaces.object.Clabject):
                    for attr in t.get_all_attributes():
                        if attr.get_potency() > IntegerValue(0):
                            try:
                                attr_name = attr.get_short_location()
                                assert logger.debug('Looking for %s in %s...' % (attr_name, phys_mapper.get_physical_attribute_mapping()))
                                m = phys_mapper.get_physical_attribute_mapping()[attr_name]
                                assert m.len() == IntegerValue(1)
                                if attr_name in attributes:
                                    attributes[m[IntegerValue(0)]] = attributes[attr_name]
                                else:
                                    attributes[m[IntegerValue(0)]] = attr.get_default()
                                ''' TODO: Delete attributes[m[IntegerValue(0)]] if attr_name != m[IntegerValue(0)]? '''
                            except MvKKeyError, e:
                                cl.set_status_code(CreateConstants.NOT_FOUND_CODE)
                                cl.set_status_message(e.get_message())
                                return cl
                elif isinstance(t, mvk.interfaces.object.Attribute):
                    if not StringValue('name') in attributes:
                        attributes[StringValue('name')] = t.get_name()
            cls._check_param(attributes,
                             StringValue('name'),
                             mvk.interfaces.datavalue.StringValue,
                             mvk.interfaces.datatype.StringType)
            cls._check_param(attributes,
                             StringValue('type'),
                             mvk.interfaces.datatype.Type,
                             req=False)
            cls._check_param(attributes,
                             StringValue('potency'),
                             mvk.interfaces.datavalue.IntegerValue,
                             mvk.interfaces.datatype.IntegerType,
                             req=False,
                             extra_check=lambda x: None if x >= IntegerValue(0) and x < InfiniteValue('+') else StringValue('potency value needs to be >= 0 and < +inf!'))
            cls._check_param(attributes,
                             StringValue('default'),
                             mvk.interfaces.element.Element,
                             req=False)
            cls._check_param(attributes,
                             StringValue('value'),
                             mvk.interfaces.element.Element,
                             req=False)
            cls._check_param(attributes,
                             StringValue('lower'),
                             mvk.interfaces.datavalue.IntegerValue,
                             mvk.interfaces.datatype.IntegerType,
                             req=False,
                             extra_check=lambda x: None if x >= IntegerValue(0) and x < InfiniteValue('+') else StringValue('Lower value needs to be >= 0 and < +inf!'))
            cls._check_param(attributes,
                             StringValue('upper'),
                             (mvk.interfaces.datavalue.IntegerValue,
                              mvk.interfaces.datavalue.InfiniteValue),
                             (mvk.interfaces.datatype.IntegerType,
                              mvk.interfaces.datatype.InfiniteType),
                             req=False,
                             extra_check=lambda x: None if x >= IntegerValue(0) else StringValue('upper value needs to be >= 0!'))
            cls._check_param(attributes,
                             StringValue('ordered'),
                             mvk.interfaces.datavalue.BooleanValue,
                             mvk.interfaces.datatype.BooleanType,
                             req=False)
        except MvKException, e:
            cl.set_status_code(CreateConstants.BAD_REQUEST_CODE)
            cl.set_status_message(e.get_message())
            return cl
        return None

    @classmethod
    def _create(cls, params):
        assert logger.debug('In Attribute._create with params %s' % params)
        from mvk.impl.python.python_representer import PythonRepresenter
        ''' Initialize needed changelog values. '''
        cl = MvKCreateLog()
        location = params[CreateConstants.LOCATION_KEY]
        cl.set_location(location)
        return_log = MvKCreateCompositeLog()
        return_log.set_location(cl.get_location())
        location = params[CreateConstants.LOCATION_KEY]

        ''' Try getting the parent. If it does not exist, it's an error. '''
        from mvk.mvk import MvK
        parent_log = MvK().read(location)
        if not parent_log.is_success():
            cl.set_status_code(parent_log.get_status_code())
            cl.set_status_message(parent_log.get_status_message())
            return_log.set_status_code(cl.get_status_code())
            return_log.set_status_message(cl.get_status_message())
            return return_log
        parent = parent_log.get_item()

        if not isinstance(parent, mvk.interfaces.object.Node):
            cl.set_status_code(CreateConstants.BAD_REQUEST_CODE)
            cl.set_status_message(StringValue('Can only create an Attribute \
                                               inside a Node.'))
            return_log.set_status_code(cl.get_status_code())
            return_log.set_status_message(cl.get_status_message())
            return return_log

        attributes = params[CreateConstants.ATTRS_KEY]
        name = attributes[StringValue('name')]
        given_potency = attributes[StringValue('potency')] if StringValue('potency') in attributes else None
        cls = attributes[StringValue('class')]

        ''' If the type is given, use that. Otherwise, look at
        the parent's type's attributes. If it has no attribute with
        the same name, it is an error. '''
        if StringValue('type') in attributes:
            the_type = attributes[StringValue('type')]
            ltype = ClabjectReference(cls)
            if given_potency is None:
                cl.set_status_code(CreateConstants.BAD_REQUEST_CODE)
                cl.set_status_message(StringValue('Need a potency value!'))
                return_log.set_status_code(cl.get_status_code())
                return_log.set_status_message(cl.get_status_message())
                return return_log
            potency = given_potency
        else:
            ''' Look in the type of the parent. '''
            parent_type = parent.typed_by()
            try:
                lookup_name = name
                if name.find(StringValue('.')) != IntegerValue(-1):
                    seq = SequenceValue([parent_type])
                    if isinstance(parent_type, mvk.interfaces.object.Clabject):
                        seq = seq + parent_type.get_all_super_classes()
                    for ptype in seq:
                        parent_type_name = ptype.get_name()
                        if name.startswith(parent_type_name + StringValue('.')):
                            lookup_name = name.substring(start=parent_type_name.len() + IntegerValue(1))
                            break
                ltype = parent_type.get_attribute(lookup_name)
                if isinstance(ltype, Attribute):
                    the_type = ltype.get_type()
                else:
                    cl.set_status_code(CreateConstants.BAD_REQUEST_CODE)
                    cl.set_status_message(StringValue('Unable to infer the type \
                                                       of the attribute!'))
                    return_log.set_status_code(cl.get_status_code())
                    return_log.set_status_message(cl.get_status_message())
                    return return_log
            except MvKKeyError:
                cl.set_status_code(CreateConstants.NOT_FOUND_CODE)
                cl.set_status_message(StringValue('No attribute definition \
                                                   for %s was found, unable to \
                                                   deduce type.' %
                                                   name))
                return_log.set_status_code(cl.get_status_code())
                return_log.set_status_message(cl.get_status_message())
                return return_log

            ltype_potency = ltype.get_potency()
            if ltype_potency == IntegerValue(0):
                cl.set_status_code(CreateConstants.BAD_REQUEST_CODE)
                cl.set_status_message(StringValue('Can only instantiate \
                                                   attributes with potency \
                                                   value > 1.'))
                return_log.set_status_code(cl.get_status_code())
                return_log.set_status_message(cl.get_status_message())
                return return_log
            potency = ltype_potency - IntegerValue(1)
            if given_potency is not None and potency != given_potency:
                cl.set_status_code(CreateConstants.BAD_REQUEST_CODE)
                cl.set_status_message(StringValue('Given potency %s does not \
                                                   correspond with expected \
                                                   potency %s.' %
                                                   (given_potency, potency)))
                return_log.set_status_code(cl.get_status_code())
                return_log.set_status_message(cl.get_status_message())
                return return_log

        cl.set_type(ltype)
        return_log.set_type(ltype.get_location())

        ''' Create new attribute. '''
        if potency == IntegerValue(0):
            a = Attribute(name=name, potency=potency,
                          l_type=ltype, the_type=the_type,
                          value=attributes[StringValue('value')])
            cl.add_attr_change(StringValue('value'), a.get_value())
        elif potency > IntegerValue(0):
            lower = attributes[StringValue('lower')] if StringValue('lower') in attributes else None
            upper = attributes[StringValue('upper')] if StringValue('upper') in attributes else None
            ordered = attributes[StringValue('ordered')] if StringValue('ordered') in attributes else None
            a = Attribute(name=name, potency=potency, l_type=ltype,
                          the_type=the_type, lower=lower, upper=upper,
                          ordered=ordered, default=attributes[StringValue('default')])
            cl.add_attr_change(StringValue('lower'), a.get_lower())
            cl.add_attr_change(StringValue('upper'), a.get_upper())
            cl.add_attr_change(StringValue('ordered'), a.is_ordered())
            cl.add_attr_change(StringValue('default'), a.get_default())
        else:
            cl.set_status_code(CreateConstants.BAD_REQUEST_CODE)
            cl.set_status_message(StringValue('Potency value cannot be smaller than 0! (%s)' %
                                              potency))
            return_log.set_status_code(cl.get_status_code())
            return_log.set_status_message(cl.get_status_message())
            return return_log

        cl.set_name(a.get_name())
        cl.set_type(a.typed_by().get_location())
        cl.add_attr_change(StringValue('type'), StringValue(str(a.get_type())))
        cl.add_attr_change(StringValue('name'), a.get_name())
        cl.add_attr_change(StringValue('potency'), a.get_potency())
        cl.add_attr_change(StringValue('class'), a.typed_by().get_location())

        ''' Set the parent.  '''
        try:
            parent.add_attribute(a)
            cl.set_location(parent_log.get_location())
            cl.set_status_code(CreateConstants.SUCCESS_CODE)
            cl.set_status_message(StringValue("Success!"))
        except MvKNameError, e:
            cl.set_status_code(CreateConstants.BAD_REQUEST_CODE)
            cl.set_status_message(e.get_message())
            return_log.set_status_code(cl.get_status_code())
            return_log.set_status_message(cl.get_status_message())
            return return_log

        return_log.add_log(cl)

        if potency > IntegerValue(0):
            '''
            Time for attributes which need to be instantiated from the type.
            '''
            if not a.typed_by().get_location().startswith(LocationValue('mvk.object')):
                try:
                    all_attributes = a.typed_by().get_all_attributes() if isinstance(a.typed_by(), mvk.interfaces.object.Clabject) else a.typed_by().get_attributes()
                except MvKLookupError:
                    ''' TODO: This has to do with classes which are not yet
                    created in the modelverse. Do we want to have it like this? '''
                    all_attributes = SequenceValue([])
                for attr in all_attributes:
                    potency = attr.get_potency()
                    if (potency > IntegerValue(0) and
                        (potency != IntegerValue(1) or attr.get_short_location() in attributes or attr.get_lower() > IntegerValue(0))):
                        c_attributes = MappingValue({StringValue('name'): attr.get_short_location(),
                                                     StringValue('class'): attr.get_location()})
                        c_params = MappingValue({CreateConstants.LOCATION_KEY: a.get_location(),
                                                 CreateConstants.ATTRS_KEY: c_attributes})
                        if potency > IntegerValue(1):
                            c_attributes[StringValue('default')] = attr.get_default()
                            c_attributes[StringValue('potency')] = potency - IntegerValue(1)
                            c_attributes[StringValue('lower')] = attr.get_lower()
                            c_attributes[StringValue('upper')] = attr.get_upper()
                            c_attributes[StringValue('ordered')] = attr.is_ordered()
                        elif potency == IntegerValue(1):
                            if attr.get_short_location() in attributes:
                                c_attributes[StringValue('value')] = attributes[attr.get_short_location()]
                            else:
                                c_attributes[StringValue('value')] = attr.get_default()
                        else:
                            c_attributes[StringValue('value')] = attr.get_value()
                        assert logger.debug('Creating attribute with attributes %s in Attribute %s.' %
                                            (c_attributes, a.get_location()))
                        a_cl = Attribute.create(c_params)
                        if not a_cl.is_success():
                            ''' Something went wrong creating the attribute, undo
                            changes already performed... '''
                            a.delete()
                            return_log.set_status_code(a_cl.get_status_code())
                            return_log.set_status_message(a_cl.get_status_message())
                            return return_log
                        return_log.add_log(a_cl)

        return_log.set_status_code(CreateConstants.SUCCESS_CODE)
        return_log.set_status_message(StringValue('Success!'))
        ''' Return changelog. '''
        return return_log

    @classmethod
    def _check_params_update(cls, params):
        cl = MvKUpdateLog()
        if not (isinstance(params, mvk.interfaces.datavalue.MappingValue) and
                isinstance(params.typed_by(), mvk.interfaces.datatype.MappingType)):
            cl.set_status_code(UpdateConstants.MALFORMED_REQUEST_CODE)
            cl.set_status_message(StringValue('Expected a MappingValue'))
            return cl
        try:
            cls._check_param(params,
                             CreateConstants.ATTRS_KEY,
                             mvk.interfaces.datavalue.MappingValue,
                             mvk.interfaces.datatype.MappingType)
            attributes = params[CreateConstants.ATTRS_KEY]
            cls._check_param(attributes,
                             StringValue('name'),
                             mvk.interfaces.datavalue.StringValue,
                             mvk.interfaces.datatype.StringType,
                             req=False)
            cls._check_param(attributes,
                             StringValue('type'),
                             mvk.interfaces.datatype.Type,
                             req=False)
            cls._check_param(attributes,
                             StringValue('potency'),
                             mvk.interfaces.datavalue.IntegerValue,
                             mvk.interfaces.datatype.IntegerType,
                             req=False,
                             extra_check=lambda x: None if x >= IntegerValue(0) and x < InfiniteValue('+') else StringValue('potency value needs to be >= 0 and < +inf!'))
            cls._check_param(attributes,
                             StringValue('lower'),
                             mvk.interfaces.datavalue.IntegerValue,
                             mvk.interfaces.datatype.IntegerType,
                             req=False,
                             extra_check=lambda x: None if x >= IntegerValue(0) and x < InfiniteValue('+') else StringValue('Lower value needs to be >= 0 and < +inf!'))
            cls._check_param(attributes,
                             StringValue('upper'),
                             (mvk.interfaces.datavalue.IntegerValue,
                              mvk.interfaces.datavalue.InfiniteValue),
                             (mvk.interfaces.datatype.IntegerType,
                              mvk.interfaces.datatype.InfiniteType),
                             req=False,
                             extra_check=lambda x: None if x >= IntegerValue(0) else StringValue('upper value needs to be >= 0!'))
            cls._check_param(attributes,
                             StringValue('ordered'),
                             mvk.interfaces.datavalue.BooleanValue,
                             mvk.interfaces.datatype.BooleanType,
                             req=False)
        except MvKException, e:
            cl.set_status_code(UpdateConstants.BAD_REQUEST_CODE)
            cl.set_status_message(e.get_message())
            return cl
        return None

    def _update(self, params):
        from mvk.impl.python.python_representer import PythonRepresenter
        cl = MvKUpdateLog()
        cl.set_location(self.get_location())
        cl.set_type(self.typed_by().get_location())

        from mvk.mvk import MvK
        attributes = params[UpdateConstants.ATTRS_KEY]
        try:
            for name in attributes:
                if name == StringValue('value'):
                    new_val = attributes[name]
                    cl.add_attr_change(name, self.get_value(), new_val)
                    self.set_value(new_val)
                    t_loc = self.typed_by().get_location()
                    if not t_loc.startswith(LocationValue('mvk.object')):
                        phys_mapper = MvK().get_physical_mapper(t_loc)
                        action = phys_mapper.get_physical_update_actions()[t_loc]
                        eval('self.get_parent().%s(new_val)' % action)
                elif self.typed_by().get_location().startswith(StringValue('mvk')):
                    if name == StringValue('name'):
                        new_val = attributes[name]
                        cl.add_attr_change(name, self.get_name(), new_val)
                        self.set_name(new_val)
                    elif name == StringValue('potency'):
                        new_val = attributes[name]
                        cl.add_attr_change(name, self.get_potency(), new_val)
                        self.set_potency(new_val)
                    elif name == StringValue('default'):
                        new_val = attributes[name]
                        cl.add_attr_change(name, self.get_default(), new_val)
                        self.set_default(new_val)
                    elif name == StringValue('type'):
                        new_val = attributes[name]
                        cl.add_attr_change(name, self.get_type(), new_val)
                        self.set_type(new_val)
                    else:
                        cl.set_status_code(UpdateConstants.BAD_REQUEST_CODE)
                        cl.set_status_message(StringValue('Don\'t know how to update attribute\'s physical attribute %s.' %
                                                          name))
                        return cl
                else:
                    attr = self.get_attribute(name)
                    old_val = attr.get_value()
                    new_val = attributes[name]
                    attr.set_value(new_val)
                    u_actions = MvK().get_physical_mapper(self.typed_by().get_location()).get_physical_update_actions()
                    if name in u_actions:
                        eval('self.%s(new_val)' % str(u_actions[name]))
                    cl.add_attr_change(name, old_val, new_val)
        except MvKPotencyError, e:
            ''' TODO: revert! '''
            cl.set_status_code(UpdateConstants.BAD_REQUEST_CODE)
            cl.set_status_message(e.get_message())
            return cl

        ''' This second set_location in case name was changed. '''
        cl.set_location(self.get_location())
        cl.set_status_code(UpdateConstants.SUCCESS_CODE)
        cl.set_status_message(StringValue('Successfully updated Attribute.'))
        return cl

    def read(self, location):
        return Node.read(self, location)

    def _remove_from_parent(self):
        self.get_parent().remove_attribute(self.get_name())

    def delete(self):
        return Node.delete(self)

class AssociationEnd(Multiplicity,
                     mvk.interfaces.object.AssociationEnd):
    def __init__(self, node, port_name, **kwargs):
        self.set_node(node)
        self.set_port_name(port_name)
        super(AssociationEnd, self).__init__(**kwargs)

    """ == PUBLIC INTERFACE == """
    def get_node(self):
        return self.node

    def get_port_name(self):
        return self.port_name

    def typed_by(self):
        ''' same comment as Multiplicity.typed_by() '''
        raise NotImplementedError()

    def __eq__(self, other):
        ''' We do not check whether the clabject are equal, simply because a
        clabject checks its outgoing and incoming associations and this would
        cause an infinite loop. '''
        if logger.isEnabledFor(logging.DEBUG):
            try:
                assert logger.debug('in AssociationEnd.__eq__()')
                assert logger.debug('port_name %s ?= %s (%s)' %
                                    (self.get_port_name(), other.get_port_name(),
                                     self.get_port_name() == other.get_port_name()))
            except Exception:
                assert logger.error(traceback.format_exc())

        return (super(AssociationEnd, self).__eq__(other) and
                BooleanValue(isinstance(other, AssociationEnd)) and
                self.get_port_name() == other.get_port_name())

    """ == PYTHON SPECIFIC == """
    def set_node(self, node):
        '''
        Sets the node of this association end.
        @type clabject: L{Node<mvk.interfaces.object.Clabject>}
        @param clabject: The node of this association end.
        '''
        assert isinstance(node, mvk.interfaces.object.Node)
        self.node = node

    def set_port_name(self, port_name):
        '''
        Sets the clabject of this association end.
        @type clabject: L{Clabject<mvk.interfaces.object.Clabject>}
        @param clabject: The clabject of this association end.
        '''
        assert ((port_name is None) or
                (isinstance(port_name, mvk.interfaces.datavalue.StringValue) and
                 isinstance(port_name.typed_by(), mvk.interfaces.datatype.StringType)))
        self.port_name = port_name


class Association(Clabject,
                  mvk.interfaces.object.Association):
    """ == CONSTRUCTOR == """
    def __init__(self, from_multiplicity, to_multiplicity, **kwargs):
        self.set_from_multiplicity(from_multiplicity)
        self.set_to_multiplicity(to_multiplicity)
        super(Association, self).__init__(**kwargs)
        self.from_multiplicity.get_node().add_out_association(self)
        self.to_multiplicity.get_node().add_in_association(self)

    """ == PUBLIC INTERFACE == """
    def get_from_multiplicity(self):
        return self.from_multiplicity

    def get_to_multiplicity(self):
        return self.to_multiplicity

    def __eq__(self, other):
        if logger.isEnabledFor(logging.DEBUG):
            try:
                assert logger.debug('in Association.__eq__(%s %s)' %
                                    (self.get_location(), other.get_location()))
                assert logger.debug('%s %s isinstance %s' %
                                    (self.get_location(), other.get_location(),
                                     isinstance(other, mvk.interfaces.object.Association)))
                if isinstance(other, mvk.interfaces.object.Association):
                    assert logger.debug('%s %s from_multiplicity %s ?= %s (%s)' %
                                        (self.get_location(), other.get_location(),
                                         self.get_from_multiplicity(), other.get_from_multiplicity(),
                                         self.get_from_multiplicity() == other.get_from_multiplicity()))
                    assert logger.debug('%s %s to_multiplicity %s ?= %s (%s)' %
                                        (self.get_location(), other.get_location(),
                                         self.get_to_multiplicity(), other.get_to_multiplicity(),
                                         self.get_to_multiplicity() == other.get_to_multiplicity()))
            except Exception:
                assert logger.error(traceback.format_exc())

        return (BooleanValue(id(self) == id(other)) or
                (BooleanValue(isinstance(other, mvk.interfaces.object.Association)) and
                 (self.get_location() == other.get_location() or
                  (super(Association, self).__eq__(other) and
                   self.get_from_multiplicity() == other.get_from_multiplicity() and
                   self.get_to_multiplicity() == other.get_to_multiplicity()))))

    """ == PYTHON SPECIFIC == """
    def set_name(self, name):
        old_location = self.get_location()
        if name != self.get_name():
            super(Association, self).set_name(name)
            self.get_from_multiplicity().get_node().update_out_association(old_location, self)
            self.get_to_multiplicity().get_node().update_in_association(old_location, self)

    def set_parent(self, parent):
        old_location = self.get_location()
        super(Association, self).set_parent(parent)
        if parent is not None:
            ''' We overwrite set_parent because the location of the association
            changes, which means the entries in the in- and outgoing clabjects
            have to be updated. If 'parent' is None, however, it means the
            association is deleted, and no updating has to be performed. '''
            self.get_from_multiplicity().get_node().update_out_association(old_location, self)
            self.get_to_multiplicity().get_node().update_in_association(old_location, self)

    def set_from_multiplicity(self, from_multiplicity):
        '''
        Sets the from multiplicity of this association.
        @type from_multiplicity: L{Multiplicity<mvk.interfaces.object.Multiplicity>}
        @param from_multiplicity: The from multiplicity of this association.
        '''
        assert isinstance(from_multiplicity, Multiplicity)
        self.from_multiplicity = from_multiplicity

    def set_to_multiplicity(self, to_multiplicity):
        '''
        Sets the to multiplicity of this association.
        @type from_multiplicity: L{Multiplicity<mvk.interfaces.object.Multiplicity>}
        @param from_multiplicity: The to multiplicity of this association.
        '''
        assert isinstance(to_multiplicity, Multiplicity)
        self.to_multiplicity = to_multiplicity

    """ === CRUD === """
    @classmethod
    def _check_params_create(cls, params):
        cl = MvKCreateLog()
        if not (isinstance(params, mvk.interfaces.datavalue.MappingValue) and
                isinstance(params.typed_by(), mvk.interfaces.datatype.MappingType)):
            cl.set_status_code(CreateConstants.MALFORMED_REQUEST_CODE)
            cl.set_status_message(StringValue('Expected a MappingValue'))
            return cl
        try:
            c_params = MappingValue({})
            for k in params:
                c_params[k] = params[k]
            cls._check_param(c_params,
                             CreateConstants.LOCATION_KEY,
                             mvk.interfaces.datavalue.LocationValue,
                             mvk.interfaces.datatype.LocationType)
            cls._check_param(c_params,
                             CreateConstants.TYPE_KEY,
                             mvk.interfaces.datavalue.LocationValue,
                             mvk.interfaces.datatype.LocationType)
            cls._check_param(c_params,
                             CreateConstants.ATTRS_KEY,
                             mvk.interfaces.datavalue.MappingValue,
                             mvk.interfaces.datatype.MappingType)
            attributes = params[CreateConstants.ATTRS_KEY]
            cls._check_param(attributes,
                             StringValue('class'),
                             mvk.interfaces.datavalue.LocationValue,
                             mvk.interfaces.datatype.LocationType)
            ''' Here, check the attributes of the type, and how they are mapped
            onto physical attributes. '''
            if not attributes[StringValue('class')].startswith(LocationValue('mvk.object')):
                from mvk.mvk import MvK
                the_type = attributes[StringValue('class')]
                phys_mapper = MvK().get_physical_mapper(the_type)
                type_rl = MvK().read(the_type)
                if not type_rl.is_success():
                    cl.set_status_code(type_rl.get_status_code())
                    cl.set_status_message(type_rl.get_status_message())
                    return cl
                t = type_rl.get_item()
                assert isinstance(t, mvk.interfaces.object.Association)
                if not StringValue('from_multiplicity') in attributes:
                    attributes[StringValue('from_multiplicity')] = MappingValue({})
                if not StringValue('to_multiplicity') in attributes:
                    attributes[StringValue('to_multiplicity')] = MappingValue({})
                from_multiplicy = t.get_from_multiplicity()
                if from_multiplicy.get_port_name() in attributes:
                    attributes[StringValue('from_multiplicity')][StringValue('node')] = attributes[from_multiplicy.get_port_name()]
                    attributes[StringValue('from_multiplicity')][StringValue('port_name')] = from_multiplicy.get_port_name()
                to_multiplicity = t.get_to_multiplicity()
                if to_multiplicity.get_port_name() in attributes:
                    attributes[StringValue('to_multiplicity')][StringValue('node')] = attributes[to_multiplicity.get_port_name()]
                    attributes[StringValue('to_multiplicity')][StringValue('port_name')] = to_multiplicity.get_port_name()
                assert logger.debug('from_multiplicity port name = %s, to_multiplicity port name = %s' %
                                    (from_multiplicy.get_port_name(),
                                     to_multiplicity.get_port_name()))
                assert logger.debug('from_multiplicity = %s, to_multiplicity = %s' %
                                    (attributes[StringValue('from_multiplicity')],
                                     attributes[StringValue('to_multiplicity')]))
                assert logger.debug('Getting all attributes from %s' % t.get_location())
                for attr in t.get_all_attributes():
                    try:
                        attr_name = attr.get_short_location()
                        assert logger.debug('Looking for %s in %s... (%s)' %
                                            (attr_name, phys_mapper.get_physical_attribute_mapping(),
                                             attr_name in phys_mapper.get_physical_attribute_mapping()))
                        m = phys_mapper.get_physical_attribute_mapping()[attr_name]
                        curr_map = attributes
                        i = IntegerValue(0)
                        while m.len() > i + IntegerValue(1):
                            if not m[i] in curr_map:
                                curr_map[m[i]] = MappingValue({})
                            curr_map = curr_map[m[i]]
                            i = i + IntegerValue(1)
                        if attr_name in attributes:
                            assert logger.debug('Setting %s to %s.' %
                                                (attr_name, attributes[attr_name]))
                            curr_map[m[i]] = attributes[attr_name]
                        else:
                            assert logger.debug('Setting %s to default value %s.' %
                                                (attr_name, attr.get_default()))
                            curr_map[m[i]] = attr.get_default()
                        ''' TODO: Delete attributes[m[i]] if attr_name != m[i]? '''
                    except MvKKeyError, e:
                        assert logger.debug('%s not found in %s' %
                                     (attr_name, phys_mapper.get_physical_attribute_mapping()))
            cls._check_param(attributes,
                             StringValue('name'),
                             mvk.interfaces.datavalue.StringValue,
                             mvk.interfaces.datatype.StringType)
            cls._check_param(attributes,
                             StringValue('potency'),
                             (mvk.interfaces.datavalue.IntegerValue,
                              mvk.interfaces.datavalue.InfiniteValue),
                             (mvk.interfaces.datatype.IntegerType,
                              mvk.interfaces.datatype.InfiniteType),
                             req=False,
                             extra_check=lambda x: None if x >= IntegerValue(0) else StringValue('potency value needs to be >= 0!'))
            cls._check_param(attributes,
                             StringValue('lower'),
                             mvk.interfaces.datavalue.IntegerValue,
                             mvk.interfaces.datatype.IntegerType,
                             req=False,
                             extra_check=lambda x: None if x >= IntegerValue(0) and x < InfiniteValue('+') else StringValue('Lower value needs to be >= 0 and < +inf!'))
            cls._check_param(attributes,
                             StringValue('upper'),
                             (mvk.interfaces.datavalue.IntegerValue,
                              mvk.interfaces.datavalue.InfiniteValue),
                             (mvk.interfaces.datatype.IntegerType,
                              mvk.interfaces.datatype.InfiniteType),
                             req=False,
                             extra_check=lambda x: None if x >= IntegerValue(0) else StringValue('upper value needs to be >=!'))
            cls._check_param(attributes,
                             StringValue('ordered'),
                             mvk.interfaces.datavalue.BooleanValue,
                             mvk.interfaces.datatype.BooleanType,
                             req=False)
            cls._check_param(attributes,
                             StringValue('abstract'),
                             mvk.interfaces.datavalue.BooleanValue,
                             mvk.interfaces.datatype.BooleanType,
                             req=(StringValue('potency') not in attributes or
                                  attributes[StringValue('potency')] is None or
                                  attributes[StringValue('potency')] > IntegerValue(0)))
            cls._check_param(attributes,
                             StringValue('from_multiplicity'),
                             mvk.interfaces.datavalue.MappingValue,
                             mvk.interfaces.datatype.MappingType)
            from_multiplicity = attributes[StringValue('from_multiplicity')]
            cls._check_param(from_multiplicity,
                             StringValue('node'),
                             mvk.interfaces.datavalue.LocationValue,
                             mvk.interfaces.datatype.LocationType)
            cls._check_param(from_multiplicity,
                             StringValue('port_name'),
                             mvk.interfaces.datavalue.StringValue,
                             mvk.interfaces.datatype.StringType,
                             req=(StringValue('potency') not in attributes or
                                  attributes[StringValue('potency')] is None or
                                  attributes[StringValue('potency')] > IntegerValue(0)))
            cls._check_param(from_multiplicity,
                             StringValue('lower'),
                             mvk.interfaces.datavalue.IntegerValue,
                             mvk.interfaces.datatype.IntegerType,
                             req=False,
                             extra_check=lambda x: None if x >= IntegerValue(0) and x < InfiniteValue('+') else StringValue('Lower value needs to be >= 0 and < +inf!'))
            cls._check_param(from_multiplicity,
                             StringValue('upper'),
                             (mvk.interfaces.datavalue.IntegerValue,
                              mvk.interfaces.datavalue.InfiniteValue),
                             (mvk.interfaces.datatype.IntegerType,
                              mvk.interfaces.datatype.InfiniteType),
                             req=False,
                             extra_check=lambda x: None if x >= IntegerValue(0) else StringValue('upper value needs to be >= 0!'))
            cls._check_param(from_multiplicity,
                             StringValue('ordered'),
                             mvk.interfaces.datavalue.BooleanValue,
                             mvk.interfaces.datatype.BooleanType,
                             req=False)
            cls._check_param(attributes,
                             StringValue('to_multiplicity'),
                             mvk.interfaces.datavalue.MappingValue,
                             mvk.interfaces.datatype.MappingType)
            to_multiplicity = attributes[StringValue('to_multiplicity')]
            cls._check_param(to_multiplicity,
                             StringValue('node'),
                             mvk.interfaces.datavalue.LocationValue,
                             mvk.interfaces.datatype.LocationType)
            cls._check_param(to_multiplicity,
                             StringValue('port_name'),
                             mvk.interfaces.datavalue.StringValue,
                             mvk.interfaces.datatype.StringType,
                             req=(StringValue('potency') not in attributes or
                                  attributes[StringValue('potency')] is None or
                                  attributes[StringValue('potency')] > IntegerValue(0)))
            cls._check_param(to_multiplicity,
                             StringValue('lower'),
                             mvk.interfaces.datavalue.IntegerValue,
                             mvk.interfaces.datatype.IntegerType,
                             req=False,
                             extra_check=lambda x: None if x >= IntegerValue(0) and x < InfiniteValue('+') else StringValue('Lower value needs to be >= 0 and < +inf!'))
            cls._check_param(to_multiplicity,
                             StringValue('upper'),
                             (mvk.interfaces.datavalue.IntegerValue,
                              mvk.interfaces.datavalue.InfiniteValue),
                             (mvk.interfaces.datatype.IntegerType,
                              mvk.interfaces.datatype.InfiniteType),
                             req=False,
                             extra_check=lambda x: None if x >= IntegerValue(0) else StringValue('upper value needs to be >= 0!'))
            cls._check_param(to_multiplicity,
                             StringValue('ordered'),
                             mvk.interfaces.datavalue.BooleanValue,
                             mvk.interfaces.datatype.BooleanType,
                             req=False)
        except MvKException, e:
            cl.set_status_code(CreateConstants.BAD_REQUEST_CODE)
            cl.set_status_message(e.get_message())
            return cl
        return None

    @classmethod
    def _create(cls, params, python_cls=None):
        if python_cls is None:
            python_cls = Association
        ''' TODO: This is almost the same as Clabject._create, maybe
        refactor in some way? '''
        ''' Initialize needed changelog values. '''
        from mvk.mvk import MvK
        cl = MvKCreateLog()
        location = params[CreateConstants.LOCATION_KEY]
        the_type = params[CreateConstants.TYPE_KEY]
        cl.set_location(location)
        cl.set_type(the_type)
        return_log = MvKCreateCompositeLog()
        return_log.set_type(cl.get_type())
        return_log.set_location(cl.get_location())

        ''' Create new association. '''
        attributes = params[CreateConstants.ATTRS_KEY]
        f_m = attributes[StringValue('from_multiplicity')]
        f_m_cl_log = MvK().read(f_m[StringValue('node')])
        if not f_m_cl_log.is_success():
            cl.set_status_code(f_m_cl_log.get_status_code())
            cl.set_status_message(f_m_cl_log.get_status_message())
            return cl
        f_m_cl = f_m_cl_log.get_item()
        f_m_lower = f_m[StringValue('lower')] if StringValue('lower') in f_m else None
        f_m_upper = f_m[StringValue('upper')] if StringValue('upper') in f_m else None
        f_m_ordered = f_m[StringValue('ordered')] if StringValue('ordered') in f_m else None
        f_m_port_name = f_m[StringValue('port_name')] if StringValue('port_name') in f_m else None
        f_m_end = AssociationEnd(node=f_m_cl, port_name=f_m_port_name,
                                 lower=f_m_lower, upper=f_m_upper,
                                 ordered=f_m_ordered)
        t_m = attributes[StringValue('to_multiplicity')]
        t_m_cl_log = MvK().read(t_m[StringValue('node')])
        if not t_m_cl_log.is_success():
            cl.set_status_code(t_m_cl_log.get_status_code())
            cl.set_status_message(t_m_cl_log.get_status_message())
            return cl
        t_m_cl = t_m_cl_log.get_item()
        t_m_lower = t_m[StringValue('lower')] if StringValue('lower') in t_m else None
        t_m_upper = t_m[StringValue('upper')] if StringValue('upper') in t_m else None
        t_m_ordered = t_m[StringValue('ordered')] if StringValue('ordered') in t_m else None
        t_m_port_name = t_m[StringValue('port_name')] if StringValue('port_name') in t_m else None
        t_m_end = AssociationEnd(node=t_m_cl, port_name=t_m_port_name,
                                 lower=t_m_lower, upper=t_m_upper,
                                 ordered=t_m_ordered)
        name = attributes[StringValue('name')]
        if not StringValue('potency') in attributes:
            if not attributes[StringValue('class')].startswith(StringValue('mvk')):
                attributes[StringValue('potency')] = ClabjectReference(path=attributes[StringValue('class')]).get_potency() - IntegerValue(1)
        potency = attributes[StringValue('potency')] if StringValue('potency') in attributes else None
        clz = attributes[StringValue('class')]
        if potency is None or potency > IntegerValue(0):
            lower = attributes[StringValue('lower')] if StringValue('lower') in attributes else None
            upper = attributes[StringValue('upper')] if StringValue('upper') in attributes else None
            ordered = attributes[StringValue('ordered')] if StringValue('ordered') in attributes else None
            abstract = attributes[StringValue('abstract')] if StringValue('abstract') in attributes else None
            try:
                a = python_cls(name=name, potency=potency,
                               l_type=AssociationReference(clz),
                               lower=lower, upper=upper,
                               ordered=ordered, abstract=abstract,
                               from_multiplicity=f_m_end,
                               to_multiplicity=t_m_end)
            except MvKLookupError, e:
                return_log.set_status_code(CreateConstants.NOT_FOUND_CODE)
                return_log.set_status_message(e.get_message())
                return return_log
            cl.add_attr_change(StringValue('lower'), a.get_lower())
            cl.add_attr_change(StringValue('upper'), a.get_upper())
            cl.add_attr_change(StringValue('ordered'), a.is_ordered())
            cl.add_attr_change(StringValue('abstract'), a.is_abstract())
        else:
            try:
                a = python_cls(name=name, potency=potency,
                               l_type=AssociationReference(clz),
                               from_multiplicity=f_m_end,
                               to_multiplicity=t_m_end)
            except MvKLookupError, e:
                return_log.set_status_code(CreateConstants.NOT_FOUND_CODE)
                return_log.set_status_message(e.get_message())
                return return_log
        cl.set_name(a.get_name())
        cl.add_attr_change(StringValue('name'), a.get_name())
        cl.add_attr_change(StringValue('potency'), a.get_potency())
        cl.add_attr_change(StringValue('class'), a.typed_by().get_location())
        from_multiplicity = a.get_from_multiplicity()
        cl.add_attr_change(StringValue('from_multiplicity'), MappingValue({StringValue('node'): from_multiplicity.get_node().get_location(),
                                                                           StringValue('lower'): from_multiplicity.get_lower(),
                                                                           StringValue('upper'): from_multiplicity.get_upper(),
                                                                           StringValue('ordered'): from_multiplicity.is_ordered()}))
        to_multiplicity = a.get_to_multiplicity()
        cl.add_attr_change(StringValue('to_multiplicity'), MappingValue({StringValue('node'): to_multiplicity.get_node().get_location(),
                                                                         StringValue('lower'): to_multiplicity.get_lower(),
                                                                         StringValue('upper'): to_multiplicity.get_upper(),
                                                                         StringValue('ordered'): to_multiplicity.is_ordered()}))

        ''' Try setting the parent.  '''
        parent_log = MvK().read(location)
        if not parent_log.is_success():
            return_log.set_status_code(parent_log.get_status_code())
            return_log.set_status_message(parent_log.get_status_message())
            return return_log
        parent = parent_log.get_item()
        if not (isinstance(parent, mvk.interfaces.object.Model) or isinstance(parent, mvk.interfaces.object.Clabject)):
            return_log.set_status_code(CreateConstants.BAD_REQUEST_CODE)
            return_log.set_status_message(StringValue('Can only create an Association \
                                                       inside a Model or a Clabject.'))
            return return_log
        else:
            try:
                parent.add_element(a)
                cl.set_location(parent_log.get_location())
                cl.set_status_code(CreateConstants.SUCCESS_CODE)
                cl.set_status_message(StringValue('Success!'))
            except MvKNameError, e:
                cl.set_status_code(CreateConstants.BAD_REQUEST_CODE)
                cl.set_status_message(e.get_message())
                return cl
        return_log.add_log(cl)

        '''
        Time for attributes which need to be copied from the type.
        '''
        if the_type != a.get_location():
            try:
                all_attributes = a.typed_by().get_all_attributes()
            except MvKLookupError:
                ''' TODO: This has to do with classes which are not yet
                created in the modelverse. Do we want to have it like this? '''
                all_attributes = SequenceValue([])
            for attr in all_attributes:
                potency = attr.get_potency()
                if (potency > IntegerValue(0) and
                    (potency != IntegerValue(1) or attr.get_short_location() in attributes or attr.get_lower() > IntegerValue(0))):
                    c_attributes = MappingValue({StringValue('name'): attr.get_short_location(),
                                                 StringValue('class'): attr.get_location()})
                    c_params = MappingValue({CreateConstants.LOCATION_KEY: a.get_location(),
                                             CreateConstants.ATTRS_KEY: c_attributes})
                    if potency > IntegerValue(1):
                        c_attributes[StringValue('default')] = attr.get_default()
                        c_attributes[StringValue('potency')] = potency - IntegerValue(1)
                        c_attributes[StringValue('lower')] = attr.get_lower()
                        c_attributes[StringValue('upper')] = attr.get_upper()
                        c_attributes[StringValue('ordered')] = attr.is_ordered()
                    elif potency == IntegerValue(1):
                        if attr.get_short_location() in attributes:
                            c_attributes[StringValue('value')] = attributes[attr.get_short_location()]
                        else:
                            c_attributes[StringValue('value')] = attr.get_default()
                    else:
                        c_attributes[StringValue('value')] = attr.get_value()
                    a_cl = Attribute.create(c_params)
                    if not a_cl.is_success():
                        ''' Something went wrong creating the attribute, undo
                        changes already performed... '''
                        a.delete()
                        return_log.set_status_code(a_cl.get_status_code())
                        return_log.set_status_message(a_cl.get_status_message())
                        return return_log
                    return_log.add_log(a_cl)

        return_log.set_status_code(CreateConstants.SUCCESS_CODE)
        return_log.set_status_message(StringValue("Success"))

        ''' Return changelog. '''
        return return_log

    @classmethod
    def _check_params_update(cls, params):
        cl = MvKUpdateLog()
        if not (isinstance(params, mvk.interfaces.datavalue.MappingValue) and
                isinstance(params.typed_by(), mvk.interfaces.datatype.MappingType)):
            cl.set_status_code(UpdateConstants.MALFORMED_REQUEST_CODE)
            cl.set_status_message(StringValue('Expected a MappingValue'))
            return cl
        try:
            cls._check_param(params,
                             CreateConstants.ATTRS_KEY,
                             mvk.interfaces.datavalue.MappingValue,
                             mvk.interfaces.datatype.MappingType)
            attributes = params[CreateConstants.ATTRS_KEY]
            cls._check_param(attributes,
                             StringValue('name'),
                             mvk.interfaces.datavalue.StringValue,
                             mvk.interfaces.datatype.StringType,
                             req=False)
            cls._check_param(attributes,
                             StringValue('potency'),
                             (mvk.interfaces.datavalue.IntegerValue,
                              mvk.interfaces.datavalue.InfiniteValue),
                             (mvk.interfaces.datatype.IntegerType,
                              mvk.interfaces.datatype.InfiniteType),
                             req=False,
                             extra_check=lambda x: None if x >= IntegerValue(0) else StringValue('potency value needs to be >= 0!'))
            cls._check_param(attributes,
                             StringValue('lower'),
                             mvk.interfaces.datavalue.IntegerValue,
                             mvk.interfaces.datatype.IntegerType,
                             req=False,
                             extra_check=lambda x: None if x >= IntegerValue(0) and x < InfiniteValue('+') else StringValue('Lower value needs to be >= 0 and < +inf!'))
            cls._check_param(attributes,
                             StringValue('upper'),
                             (mvk.interfaces.datavalue.IntegerValue,
                              mvk.interfaces.datavalue.InfiniteValue),
                             (mvk.interfaces.datatype.IntegerType,
                              mvk.interfaces.datatype.InfiniteType),
                             req=False,
                             extra_check=lambda x: None if x >= IntegerValue(0) else StringValue('upper value needs to be >= 0!'))
            cls._check_param(attributes,
                             StringValue('ordered'),
                             mvk.interfaces.datavalue.BooleanValue,
                             mvk.interfaces.datatype.BooleanType,
                             req=False)
            cls._check_param(attributes,
                             StringValue('abstract'),
                             mvk.interfaces.datavalue.BooleanValue,
                             mvk.interfaces.datatype.BooleanType,
                             req=False)
            cls._check_param(attributes,
                             StringValue('from_multiplicity'),
                             mvk.interfaces.datavalue.MappingValue,
                             mvk.interfaces.datatype.MappingType,
                             req=False)
            if StringValue('from_multiplicity') in attributes:
                from_multiplicity = attributes[StringValue('from_multiplicity')]
                cls._check_param(from_multiplicity,
                                 StringValue('node'),
                                 mvk.interfaces.datavalue.LocationValue,
                                 mvk.interfaces.datatype.LocationType,
                                 req=False)
                cls._check_param(from_multiplicity,
                                 StringValue('lower'),
                                 mvk.interfaces.datavalue.IntegerValue,
                                 mvk.interfaces.datatype.IntegerType,
                                 req=False,
                                 extra_check=lambda x: None if x >= IntegerValue(0) and x < InfiniteValue('+') else StringValue('Lower value needs to be >= 0 and < +inf!'))
                cls._check_param(from_multiplicity,
                                 StringValue('upper'),
                                 (mvk.interfaces.datavalue.IntegerValue,
                                  mvk.interfaces.datavalue.InfiniteValue),
                                 (mvk.interfaces.datatype.IntegerType,
                                  mvk.interfaces.datatype.InfiniteType),
                                 req=False,
                                 extra_check=lambda x: None if x >= IntegerValue(0) else StringValue('upper value needs to be >= 0!'))
                cls._check_param(from_multiplicity,
                                 StringValue('ordered'),
                                 mvk.interfaces.datavalue.BooleanValue,
                                 mvk.interfaces.datatype.BooleanType,
                                 req=False)
            cls._check_param(attributes,
                             StringValue('to_multiplicity'),
                             mvk.interfaces.datavalue.MappingValue,
                             mvk.interfaces.datatype.MappingType,
                             req=False)
            if StringValue('to_multiplicity') in attributes:
                to_multiplicity = attributes[StringValue('to_multiplicity')]
                cls._check_param(to_multiplicity, StringValue('node'),
                                 mvk.interfaces.datavalue.LocationValue,
                                 mvk.interfaces.datatype.LocationType,
                                 req=False)
                cls._check_param(to_multiplicity,
                                 StringValue('lower'),
                                 mvk.interfaces.datavalue.IntegerValue,
                                 mvk.interfaces.datatype.IntegerType,
                                 req=False,
                                 extra_check=lambda x: None if x >= IntegerValue(0) and x < InfiniteValue('+') else StringValue('Lower value needs to be >= 0 and < +inf!'))
                cls._check_param(to_multiplicity,
                                 StringValue('upper'),
                                 (mvk.interfaces.datavalue.IntegerValue,
                                  mvk.interfaces.datavalue.InfiniteValue),
                                 (mvk.interfaces.datatype.IntegerType,
                                  mvk.interfaces.datatype.InfiniteType),
                                 req=False,
                                 extra_check=lambda x: None if x >= IntegerValue(0) and x < InfiniteValue('+') else StringValue('upper value needs to be >= 0!'))
                cls._check_param(to_multiplicity,
                                 StringValue('ordered'),
                                 mvk.interfaces.datavalue.BooleanValue,
                                 mvk.interfaces.datatype.BooleanType,
                                 req=False)
        except MvKException, e:
            cl.set_status_code(UpdateConstants.BAD_REQUEST_CODE)
            cl.set_status_message(e.get_message())
            return cl
        return None

    def _update(self, params):
        from mvk.impl.python.python_representer import PythonRepresenter
        cl = MvKUpdateLog()
        cl.set_location(self.get_location())
        cl.set_type(self.typed_by().get_location())

        attributes = params[UpdateConstants.ATTRS_KEY]
        try:
            for name in attributes:
                if self.typed_by().get_location().startswith(StringValue('mvk')):
                    if name == StringValue('name'):
                        new_val = attributes[name]
                        cl.add_attr_change(name, self.get_name(), new_val)
                        self.set_name(new_val)
                    elif name == StringValue('potency'):
                        new_val = attributes[name]
                        cl.add_attr_change(name, self.get_potency(), new_val)
                        self.set_potency(new_val)
                    elif name == StringValue('lower'):
                        new_val = attributes[name]
                        cl.add_attr_change(name, self.get_potency(), new_val)
                        self.set_lower(new_val)
                    elif name == StringValue('upper'):
                        new_val = attributes[name]
                        cl.add_attr_change(name, self.get_potency(), new_val)
                        self.set_upper(new_val)
                    elif name == StringValue('ordered'):
                        new_val = attributes[name]
                        cl.add_attr_change(name, self.get_potency(), new_val)
                        self.set_ordered(new_val)
                    elif name == StringValue('abstract'):
                        new_val = attributes[name]
                        cl.add_attr_change(name, self.get_potency(), new_val)
                        self.set_abstract(new_val)
                    elif name == StringValue('from_multiplicity'):
                        f_m = attributes[name]
                        clabject = ClabjectReference(f_m[StringValue('node')])
                        lower = f_m[StringValue('lower')] if StringValue('lower') in f_m else None
                        upper = f_m[StringValue('upper')] if StringValue('upper') in f_m else None
                        ordered = f_m[StringValue('ordered')] if StringValue('ordered') in f_m else None
                        new_val = AssociationEnd(node=clabject, lower=lower,
                                                 upper=upper, ordered=ordered)
                        old_val = self.get_from_multiplicity()
                        if old_val.get_node() != clabject:
                            old_val.get_node().remove_out_association(self.get_location())
                            clabject.add_out_association(self)
                        self.set_from_multiplicity(new_val)
                        cl.add_attr_change(name,
                                           MappingValue({StringValue('node'): old_val.get_node().get_location(),
                                                         StringValue('lower'): old_val.get_lower(),
                                                         StringValue('upper'): old_val.get_upper(),
                                                         StringValue('ordered'): old_val.is_ordered}),
                                           attributes[name])
                    elif name == StringValue('to_multiplicity'):
                        t_m = attributes[name]
                        clabject = ClabjectReference(t_m[StringValue('node')])
                        lower = t_m[StringValue('lower')] if StringValue('lower') in t_m else None
                        upper = t_m[StringValue('upper')] if StringValue('upper') in t_m else None
                        ordered = t_m[StringValue('ordered')] if StringValue('ordered') in t_m else None
                        new_val = AssociationEnd(node=clabject, lower=lower,
                                                 upper=upper, ordered=ordered)
                        old_val = self.get_to_multiplicity()
                        if old_val.get_node() != clabject:
                            old_val.get_node().remove_in_association(self.get_location())
                            clabject.add_in_association(self)
                        self.set_to_multiplicity(new_val)
                        cl.add_attr_change(name,
                                           MappingValue({StringValue('node'): old_val.get_node().get_location(),
                                                         StringValue('lower'): old_val.get_lower(),
                                                         StringValue('upper'): old_val.get_upper(),
                                                         StringValue('ordered'): old_val.is_ordered}),
                                           attributes[name])
                    else:
                        ''' TODO: revert! '''
                        cl.set_status_code(UpdateConstants.BAD_REQUEST_CODE)
                        cl.set_status_message(StringValue('Don\'t know how to update association\'s physical attribute %s.' %
                                                          name))
                        return cl
                else:
                    if name == self.typed_by().get_from_multiplicity().get_port_name():
                        old_val = self.get_from_multiplicity().get_node()
                        new_val = ClabjectReference(path=attributes[name])
                        if old_val != new_val:
                            old_val.remove_out_association(self.get_location())
                        self.get_from_multiplicity().set_node(new_val)
                        new_val.add_out_association(self)
                        old_val = old_val.get_location()
                        new_val = new_val.get_location()
                    elif name == self.typed_by().get_to_multiplicity().get_port_name():
                        old_val = self.get_to_multiplicity().get_node()
                        new_val = ClabjectReference(path=attributes[name])
                        if old_val != new_val:
                            old_val.remove_in_association(self.get_location())
                        self.get_to_multiplicity().set_node(new_val)
                        new_val.add_in_association(self)
                        old_val = old_val.get_location()
                        new_val = new_val.get_location()
                    else:
                        attr = self.get_attribute(name)
                        old_val = attr.get_value()
                        new_val = attributes[name]
                        attr.set_value(new_val)
                        from mvk.mvk import MvK
                        u_actions = MvK().get_physical_mapper(self.typed_by().get_location()).get_physical_update_actions()
                        if name in u_actions:
                            eval('self.%s(new_val)' % str(u_actions[name]))
                    cl.add_attr_change(name, old_val, new_val)
            cl.set_status_code(UpdateConstants.SUCCESS_CODE)
            cl.set_status_message(StringValue('Successfully updated association.'))
        except MvKKeyError, e:
            ''' TODO: revert! '''
            cl.set_status_code(UpdateConstants.NOT_FOUND_CODE)
            cl.set_status_message(e.get_message())
        except MvKValueError, e:
            ''' TODO: revert! '''
            cl.set_status_code(UpdateConstants.NOT_FOUND_CODE)
            cl.set_status_message(e.get_message())
        except MvKPotencyError, e:
            ''' TODO: revert! '''
            cl.set_status_code(UpdateConstants.BAD_REQUEST_CODE)
            cl.set_status_message(e.get_message())

        ''' This second set_location in case name was changed. '''
        cl.set_location(self.get_location())
        return cl

    def read(self, location):
        ''' For now, the read is exactly the same as Clabject's read. '''
        return Clabject.read(self, location)

    def delete(self):
        loc = self.get_location()
        cl = Clabject.delete(self)
        if cl.is_success():
            self.get_from_multiplicity().get_node().remove_out_association(loc)
            self.get_to_multiplicity().get_node().remove_in_association(loc)
        return cl


class AssociationReference(Association, ClabjectReference,
                           mvk.interfaces.object.AssociationReference):
    """ == CONSTRUCTOR == """
    def __init__(self, path, **kwds):
        ClabjectReference.__init__(self, path, **kwds)

    """ == PUBLIC INTERFACE == """
    def get_from_multiplicity(self):
        return self.dereference().get_from_multiplicity()

    def get_to_multiplicity(self):
        return self.dereference().get_to_multiplicity()

    """ == PYTHON SPECIFIC == """
    def set_from_multiplicity(self, from_multiplicity):
        self.dereference().set_from_multiplicity(from_multiplicity)

    def set_to_multiplicity(self, to_multiplicity):
        self.dereference().set_to_multiplicity(to_multiplicity)


class Composition(Association,
                  mvk.interfaces.object.Composition):
    def __eq__(self, other):
        return (super(Composition, self).__eq__(other) and
                BooleanValue(isinstance(other, Composition)))

    @classmethod
    def _create(cls, params):
        return Association._create(params, python_cls=cls)

    def delete(self, propagate=BooleanValue(True)):
        cl = super(Composition, self).delete()
        if cl.is_success() and propagate:
            return_log = self.get_to_multiplicity().get_node().delete()
        else:
            return_log = cl
        return return_log


class Aggregation(Association,
                  mvk.interfaces.object.Aggregation):
    def __eq__(self, other):
        return (super(Aggregation, self).__eq__(other) and
                BooleanValue(isinstance(other, Aggregation)))

    @classmethod
    def _create(cls, params):
        return Association._create(params, python_cls=cls)

    def delete(self):
        return super(Aggregation, self).delete()


class Inherits(Association,
               mvk.interfaces.object.Inherits):
    def __eq__(self, other):
        return (BooleanValue(isinstance(other, mvk.interfaces.object.Inherits)) and
                super(Inherits, self).__eq__(other))

    @classmethod
    def _check_params_create(cls, params):
        if CreateConstants.ATTRS_KEY in params:
            params[CreateConstants.ATTRS_KEY][StringValue('potency')] = IntegerValue(0)
        return Association._check_params_create(params)

    @classmethod
    def _create(cls, params):
        cl = Association._create(params, python_cls=Inherits)
        if cl.is_success():
            from mvk.mvk import MvK
            MvK().read(params[CreateConstants.ATTRS_KEY][StringValue('from_multiplicity')][StringValue('node')]).get_item().add_super_class(ClabjectReference(params[CreateConstants.ATTRS_KEY][StringValue('to_multiplicity')][StringValue('node')]))
        return cl

    @classmethod
    def _check_params_update(cls, params):
        if CreateConstants.ATTRS_KEY in params:
            raise MvKParameterError(StringValue('Cannot update the potency value of an Inheritance link!'))

    @classmethod
    def _update(cls, params):
        return Association._update(params)

    def delete(self):
        cl = Association.delete(self)
        if cl.is_success():
            self.get_from_multiplicity().get_node().remove_superclass(self.get_to_multiplicity().get_node().get_location())
        return cl
