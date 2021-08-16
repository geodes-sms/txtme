'''
Created on 17-jun.-2014

@author: Simon
'''

from mvk.impl.python.changelog import MvKCreateLog, MvKCreateCompositeLog
from mvk.impl.python.constants import CreateConstants, UpdateConstants
from mvk.impl.python.datatype import StringType
from mvk.impl.python.datavalue import LocationValue, StringValue, MappingValue, TupleValue, IntegerValue, BooleanValue
from mvk.impl.python.exception import MvKParameterError, MvKTypeError, MvKKeyError, MvKException
from mvk.impl.python.python_representer import PythonRepresenter
import mvk.interfaces.datavalue
from mvk.interfaces.physical_mapper import PhysicalMapper


class StoreMapper(PhysicalMapper):
    def __init__(self, **kwds):
        super(StoreMapper, self).__init__(**kwds)
        self.phys_attribute_mapping = MappingValue({LocationValue('Store.name'): TupleValue((StringValue('name'),)),
                                                    LocationValue('attributes.name'): TupleValue((StringValue('name'),)),
                                                    LocationValue('Element.id'): TupleValue((StringValue('name'),)),
                                                    LocationValue('Attribute.name'): TupleValue((StringValue('name'),)),
                                                    LocationValue('Attribute.type'): TupleValue((StringValue('type'),)),
                                                    LocationValue('Attribute.default'): TupleValue((StringValue('default'),)),
                                                    })
        self.phys_actions_update = MappingValue({LocationValue('Store.name'): StringValue('set_name'),
                                                 LocationValue('attributes.name'): StringValue('set_name'),
                                                 LocationValue('Element.id'): StringValue('set_name'),
                                                 LocationValue('Attribute.name'): StringValue('set_name'),
                                                 LocationValue('Attribute.type'): StringValue('set_type'),
                                                 LocationValue('Attribute.default'): StringValue('set_default')})

    def __create_store(self, params):
        attributes = params[CreateConstants.ATTRS_KEY]
        attributes[StringValue('type_model')] = params[CreateConstants.TYPE_KEY]
        from mvk.mvk import MvK
        cl = MvK().create(MappingValue({CreateConstants.LOCATION_KEY: params[CreateConstants.LOCATION_KEY],
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.object.Model'),
                                        CreateConstants.ATTRS_KEY: attributes
                                        })
                          )
        a_cl = self.__create_attribute(MappingValue({CreateConstants.LOCATION_KEY: params[CreateConstants.LOCATION_KEY] + StringValue('.') + attributes[StringValue('Store.name')],
                                                     CreateConstants.TYPE_KEY: LocationValue('formalisms.Store.Attribute'),
                                                     CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                                              StringValue('Attribute.type'): StringType(),
                                                                                              StringValue('Attribute.default'): StringValue('')})
                                                     })
                                       )
        if not a_cl.is_success():
            cl.set_status_code(a_cl.get_status_code())
            cl.set_status_message(a_cl.get_status_message())
        if cl.is_success():
            loc = params[CreateConstants.LOCATION_KEY] + (StringValue('.') if params[CreateConstants.LOCATION_KEY] != StringValue('') else StringValue('')) + attributes[StringValue('name')]
            MvK().register_mapper(loc, StoreFormalismMapper(tm_loc=loc))
        return cl

    def __create_class(self, params):
        attributes = params[CreateConstants.ATTRS_KEY]
        attributes[StringValue('class')] = params[CreateConstants.TYPE_KEY]
        attributes[StringValue('abstract')] = BooleanValue(False)
        from mvk.mvk import MvK
        cl = MvK().create(MappingValue({CreateConstants.LOCATION_KEY: params[CreateConstants.LOCATION_KEY],
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                        CreateConstants.ATTRS_KEY: attributes
                                        })
                          )
        return cl

    def __create_association(self, params):
        attributes = params[CreateConstants.ATTRS_KEY]
        attributes[StringValue('class')] = params[CreateConstants.TYPE_KEY]
        attributes[StringValue('abstract')] = BooleanValue(False)
        from mvk.mvk import MvK
        t = MvK().read(params[CreateConstants.TYPE_KEY]).get_item()
        t_f_m = t.get_from_multiplicity()
        attributes[StringValue('from_multiplicity')] = MappingValue({StringValue('port_name'): t_f_m.get_port_name(),
                                                                     StringValue('lower'): t_f_m.get_lower(),
                                                                     StringValue('upper'): t_f_m.get_upper(),
                                                                     StringValue('ordered'): t_f_m.is_ordered()})
        t_t_m = t.get_to_multiplicity()
        attributes[StringValue('to_multiplicity')] = MappingValue({StringValue('port_name'): t_t_m.get_port_name(),
                                                                     StringValue('lower'): t_t_m.get_lower(),
                                                                     StringValue('upper'): t_t_m.get_upper(),
                                                                     StringValue('ordered'): t_t_m.is_ordered()})
        return MvK().create(MappingValue({CreateConstants.LOCATION_KEY: params[CreateConstants.LOCATION_KEY],
                                          CreateConstants.TYPE_KEY: LocationValue('mvk.object.Association'),
                                          CreateConstants.ATTRS_KEY: attributes
                                          })
                            )

    def __create_attribute(self, params):
        attributes = params[CreateConstants.ATTRS_KEY]
        attributes[StringValue('class')] = params[CreateConstants.TYPE_KEY]
        attributes[StringValue('lower')] = IntegerValue(1)
        attributes[StringValue('upper')] = IntegerValue(1)
        attributes[StringValue('potency')] = IntegerValue(1)
        from mvk.mvk import MvK
        from mvk.impl.python.object import ClabjectReference
        cl = MvK().create(MappingValue({CreateConstants.LOCATION_KEY: params[CreateConstants.LOCATION_KEY],
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.object.Attribute'),
                                        CreateConstants.ATTRS_KEY: attributes
                                        })
                          )
        if not cl.is_success():
            return cl
        idx = params[CreateConstants.LOCATION_KEY].rfind(StringValue('.'))
        from_class = params[CreateConstants.LOCATION_KEY]
        to_attr = params[CreateConstants.LOCATION_KEY] + StringValue('.') + attributes[StringValue('Attribute.name')]
        loc = MvK().read(params[CreateConstants.LOCATION_KEY]).get_item()
        a_cl = MvK().create(MappingValue({CreateConstants.LOCATION_KEY: params[CreateConstants.LOCATION_KEY] if isinstance(loc, mvk.interfaces.object.Model) else params[CreateConstants.LOCATION_KEY].substring(stop=idx),
                                          CreateConstants.TYPE_KEY: LocationValue('mvk.object.Composition'),
                                          CreateConstants.ATTRS_KEY: MappingValue({StringValue('attributes.name'): ClabjectReference(from_class).get_name() + StringValue('_a_') + attributes[StringValue('Attribute.name')],
                                                                                   StringValue('potency'): IntegerValue(0),
                                                                                   StringValue('class'): LocationValue('formalisms.Store.attributes'),
                                                                                   StringValue('from_el'): from_class,
                                                                                   StringValue('to_attr'): to_attr
                                                                                   })
                                          })
                            )
        if not a_cl.is_success():
            cl.set_status_code(a_cl.get_status_code())
            cl.set_status_message(a_cl.get_status_message())
        return cl

    def __create_unknown(self, params):
        cl = MvKCreateLog()
        cl.set_status_code(CreateConstants.BAD_REQUEST_CODE)
        cl.set_status_message(StringValue('Unknown type!'))
        return cl

    def create(self, params):
        types = {LocationValue('formalisms.Store'): self.__create_store,
                 LocationValue('formalisms.Store.Product'): self.__create_class,
                 LocationValue('formalisms.Store.Creator'): self.__create_class,
                 LocationValue('formalisms.Store.created'): self.__create_association,
                 LocationValue('formalisms.Store.Attribute'): self.__create_attribute,}
        return types.get(params[CreateConstants.TYPE_KEY], self.__create_unknown)(params)

    def read(self, location):
        raise NotImplementedError()

    def update(self, params):
        types = {LocationValue('formalisms.Store'): PythonRepresenter.MODEL,
                 LocationValue('formalisms.Store.Product'): PythonRepresenter.CLABJECT,
                 LocationValue('formalisms.Store.Creator'): PythonRepresenter.CLABJECT,
                 LocationValue('formalisms.Store.created'): PythonRepresenter.ASSOCIATION,
                 LocationValue('formalisms.Store.Attribute'): PythonRepresenter.ATTRIBUTE}
        from mvk.mvk import MvK
        params[UpdateConstants.TYPE_KEY] = types[params[UpdateConstants.TYPE_KEY]]
        item = MvK().read(params[UpdateConstants.LOCATION_KEY]).get_item()
        cl = item.update(params)
        if params[UpdateConstants.TYPE_KEY] == PythonRepresenter.MODEL and StringValue('name') in params[UpdateConstants.ATTRS_KEY] and cl.is_success():
            try:
                MvK().unregister_mapper(params[UpdateConstants.LOCATION_KEY])
            except Exception:
                ''' TODO: This is here because someone's parent might be updated (a Package, which this mapper does not know about). '''
                pass
            MvK().register_mapper(item.get_location(),
                                  StoreFormalismMapper(tm_loc=item.get_location()))
        return cl

    def delete(self, location):
        raise NotImplementedError()

    def get_physical_attribute_mapping(self):
        return self.phys_attribute_mapping

    def get_physical_update_actions(self):
        return self.phys_actions_update


class StoreFormalismMapper(PhysicalMapper):
    def __init__(self, tm_loc, **kwds):
        assert (isinstance(tm_loc, mvk.interfaces.datavalue.LocationValue) and
                isinstance(tm_loc.typed_by(), mvk.interfaces.datatype.LocationType))
        from mvk.mvk import MvK
        self.tm_loc = tm_loc
        tm_log = MvK().read(self.tm_loc)
        assert tm_log.is_success(), tm_log
        self.tm = tm_log.get_item()
        super(StoreFormalismMapper, self).__init__(**kwds)

    def create(self, params):
        types = {LocationValue('formalisms.Store'): PythonRepresenter.MODEL,
                 LocationValue('formalisms.Store.Product'): PythonRepresenter.CLABJECT,
                 LocationValue('formalisms.Store.Creator'): PythonRepresenter.CLABJECT,
                 LocationValue('formalisms.Store.created'): PythonRepresenter.ASSOCIATION}
        from mvk.mvk import MvK
        type_to_create = MvK().read(params[CreateConstants.TYPE_KEY]).get_item()
        attributes = params[CreateConstants.ATTRS_KEY]
        if types[type_to_create.typed_by().get_location()] == PythonRepresenter.MODEL:
            attributes[StringValue('type_model')] = params[CreateConstants.TYPE_KEY]
        else:
            attributes[StringValue('class')] = params[CreateConstants.TYPE_KEY]
        attributes[StringValue('potency')] = type_to_create.get_potency() - IntegerValue(1)
        return MvK().create(MappingValue({CreateConstants.LOCATION_KEY: params[CreateConstants.LOCATION_KEY],
                                          CreateConstants.TYPE_KEY: types[type_to_create.typed_by().get_location()],
                                          CreateConstants.ATTRS_KEY: attributes
                                          }))

    def read(self, location):
        raise NotImplementedError()

    def update(self, params):
        types = {LocationValue('formalisms.Store'): PythonRepresenter.MODEL,
                 LocationValue('formalisms.Store.Product'): PythonRepresenter.CLABJECT,
                 LocationValue('formalisms.Store.Creator'): PythonRepresenter.CLABJECT,
                 LocationValue('formalisms.Store.created'): PythonRepresenter.ASSOCIATION}
        from mvk.mvk import MvK
        type_to_update = MvK().read(params[CreateConstants.TYPE_KEY]).get_item()
        params[UpdateConstants.TYPE_KEY] = types[type_to_update.typed_by().get_location()]
        item = MvK().read(params[UpdateConstants.LOCATION_KEY]).get_item()
        return item.update(params)

    def delete(self, params):
        raise NotImplementedError()

    def get_physical_attribute_mapping(self):
        phys_attribute_mapping = MappingValue({self.tm.get_name() + StringValue('.') + StringValue('name'): TupleValue((StringValue('name'),))})
        it = self.tm.get_elements().__iter__()
        while it.has_next():
            el = self.tm.get_element(it.next())
            if el.get_potency() > IntegerValue(0):
                try:
                    id_field = el.get_attribute(StringValue('Element.id_field')).get_value()
                    phys_attribute_mapping[id_field] = TupleValue((StringValue('name'),))
                except MvKKeyError:
                    assert el.is_abstract()
        return phys_attribute_mapping

    def get_physical_update_actions(self):
        phys_update_actions = MappingValue({self.tm.get_name() + StringValue('.') + StringValue('name'): StringValue('set_name')})
        it = self.tm.get_elements().__iter__()
        while it.has_next():
            el = self.tm.get_element(it.next())
            if el.get_potency() > IntegerValue(0):
                id_field = el.get_attribute(StringValue('Element.id_field')).get_value()
                phys_update_actions[id_field] = StringValue('set_name')
        return phys_update_actions
