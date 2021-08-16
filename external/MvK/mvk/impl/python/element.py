"""
Created on 3-jan.-2014

@author: Simon
"""
from types import NoneType

from mvk.impl.python.exception import MvKParameterError
import mvk.interfaces.element
from mvk.util.logger import get_logger


logger = get_logger('element')


class Element(mvk.interfaces.element.Element):
    """ === PUBLIC INTERFACE === """
    def __eq__(self, other):
        from mvk.impl.python.datavalue import BooleanValue
        return BooleanValue(isinstance(other,  mvk.interfaces.element.Element))

    def __ne__(self, other):
        return not self.__eq__(other)

    """ === PYTHON SPECIFIC === """
    def __repr__(self):
        return self.__class__.__name__

    def __hash__(self):
        """ Implemented to ensure that all Elements can be added to Python
        sets. It is not very efficient but leads to more readable, and,
        hopefully, more efficient code.
        !!! DO NOT MISUSE !!! In the worst case, each element will have to
        be checked for equality, which can be a costly operation. """
        return hash(self.__class__.__name__)

    """ === CRUD === """
    @classmethod
    def create(cls, params):
        """
        Creates an element.
        @type params: L{MappingValue<mvk.interfaces.datavalue.MappingValue>}
        @param params: The parameters for creating the element.
        @rtype: L{MvKCreateLog<mvk.interfaces.changelog.MvKCreateLog>}
        or L{MvKCompositeLog<mvk.interfaces.changelog.MvKCompositeLog>}
        @return: The changelog, describing what was created.
        """
        cl = cls._check_params_create(params)
        if cl is not None:
            return cl
        return cls._create(params)

    @classmethod
    def create_raw(cls, params):
        # By default, we just issue a normal create
        return cls.create(params)

    @classmethod
    def _check_param(cls, params, name, ph_type,
                     l_type=None, req=True, extra_check=lambda x: None):
        if name in params:
            val = params[name]
            if not (isinstance(val, ph_type) and
                    ((l_type is None) or isinstance(val.typed_by(), l_type))):
                from mvk.impl.python.exception import MvKTypeError
                from mvk.impl.python.datavalue import StringValue
                raise MvKTypeError(StringValue('Expected %s to be of type %s (%s), not %s (%s).' %
                                   (name, ph_type, l_type, val.__class__.__name__, val.typed_by())))
            extra = extra_check(val)
            if extra:
                from mvk.impl.python.exception import MvKParameterError
                raise MvKParameterError(extra)
        elif req:
            from mvk.impl.python.exception import MvKKeyError
            from mvk.impl.python.datavalue import StringValue
            raise MvKKeyError(StringValue('Expected %s as a parameter.' % name))

    @classmethod
    def _check_params_create(cls, params):
        raise NotImplementedError()

    @classmethod
    def _create(cls, params):
        raise NotImplementedError()

    def update(self, params):
        """
        Updates an element.
        @type params: L{MappingValue<mvk.interfaces.datavalue.MappingValue>}
        @param params: The parameters for creating the element.
        @rtype: L{MvKUpdateLog<mvk.interfaces.changelog.MvKCreateLog>}
        @return: The changelog, describing what was changed.
        """
        cl = self.__class__._check_params_update(params)
        if cl is not None:
            return cl
        return self._update(params)

    @classmethod
    def _check_params_update(cls, params):
        raise NotImplementedError()

    def _update(self, params):
        raise NotImplementedError()

    def read(self, location):
        """
        Reads an element from the modelverse.
        @type location: L{LocationValue<mvk.interfaces.datavalue.LocationValue>}
        @param location: The location of the element to be read.
        @rtype: L{MvKReadLog<mvk.interfaces.changelog.MvKReadLog>}
        @return: The changelog, describing the read element.
        """
        raise NotImplementedError()

    def delete(self):
        """
        Deletes an element from the modelverse.
        @rtype: L{MvKDeleteLog<mvk.interfaces.changelog.MvKDeleteLog>}
        @return: The changelog, describing the deleted element.
        """
        raise NotImplementedError()


class NamedElement(Element, mvk.interfaces.element.NamedElement):
    """ === CONSTRUCTOR === """
    def __init__(self, name, **kwds):
        assert logger.debug('Constructing NamedElement with name %s' % name)
        assert isinstance(name, mvk.interfaces.datavalue.StringValue)
        self.name = name
        self.parent = None  # needs to be set explicitly using set_parent
        super(NamedElement, self).__init__(**kwds)

    """ === PUBLIC INTERFACE === """
    def get_name(self):
        return self.name

    def get_parent(self):
        return self.parent

    def get_location(self):
        if (not hasattr(self, "location")) or (self.location is None):
            from mvk.impl.python.datavalue import LocationValue
            if self.parent is None:
                self.location = LocationValue(self.name.get_value())
            else:
                self.location = self.parent.get_location() + LocationValue('.') + self.name
        return self.location

    def get_short_location(self):
        from mvk.impl.python.datavalue import LocationValue, StringValue, IntegerValue
        if self.parent is None or self.name.find(StringValue('.')) != IntegerValue(-1):
            return LocationValue(self.name.get_value())
        else:
            return self.parent.get_name() + LocationValue('.') + self.name

    def __eq__(self, other):
        from mvk.impl.python.datavalue import BooleanValue
        return ((super(NamedElement, self).__eq__(other)) and
                (BooleanValue(isinstance(other, mvk.interfaces.element.NamedElement))) and
                (self.get_name() == other.get_name()))

    """ === PYTHON SPECIFIC === """
    def set_name(self, name):
        assert (isinstance(name, mvk.interfaces.datavalue.StringValue) and
                isinstance(name.typed_by(), mvk.interfaces.datatype.StringType))
        from mvk.mvk import MvK
        try:
            old_name = self.get_location()
            del MvK.read_cache[self.name]
        except:
            # Possibly we don't even have a name yet...
            pass
        # Flush cache
        self.location = None
        self.name = name
        self.parent_renamed(old_name, self.get_location())

    def parent_renamed(self, old_path, new_path):
        raise NotImplementedError()

    def set_parent(self, parent):
        assert isinstance(parent, (NamedElement, NoneType))
        if parent is not None:
            # Clear location cache
            #NOTE resetting parent is not possible, only clearing
            self.location = None
        self.parent = parent


class TypedElement(Element, mvk.interfaces.element.TypedElement):
    """ === CONSTRUCTOR === """
    def __init__(self, the_type, **kwds):
        assert logger.debug('Constructing TypedElement with type %s' % the_type)
        assert isinstance(the_type, mvk.interfaces.datatype.Type)
        self.type = the_type
        super(TypedElement, self).__init__(**kwds)

    """ === PUBLIC INTERFACE === """
    def get_type(self):
        return self.type

    def __eq__(self, other):
        from mvk.impl.python.datavalue import BooleanValue
        return ((super(TypedElement, self).__eq__(other)) and
                (BooleanValue(isinstance(other, mvk.interfaces.element.TypedElement))) and
                (self.type == other.get_type()))

    def set_type(self, new_type):
        assert isinstance(new_type, mvk.interfaces.datatype.Type)
        self.type = new_type
