'''
Created on 17-jun.-2014

@author: Simon
'''

'''
Created on 19-mrt.-2014

@author: Simon
'''

from mvk.impl.python.changelog import MvKCreateLog, MvKCreateCompositeLog
from mvk.impl.python.constants import CreateConstants, UpdateConstants
from mvk.impl.python.datatype import StringType
from mvk.impl.python.datavalue import LocationValue, StringValue, MappingValue, TupleValue, IntegerValue
from mvk.impl.python.exception import MvKParameterError, MvKTypeError, MvKKeyError, MvKException
from mvk.impl.python.python_representer import PythonRepresenter
import mvk.interfaces.datavalue
from mvk.interfaces.physical_mapper import PhysicalMapper


class MDMapper(PhysicalMapper):
    def __init__(self, **kwds):
        super(MDMapper, self).__init__(**kwds)
        self.phys_attribute_mapping = MappingValue({LocationValue('MultiDiagrams.name'): TupleValue((StringValue('name'),)),
                                                    LocationValue('MultiDiagrams.potency'): TupleValue((StringValue('potency'),)),
                                                    LocationValue('Clabject.is_abstract'): TupleValue((StringValue('abstract'),)),
                                                    LocationValue('Clabject.name'): TupleValue((StringValue('name'),)),
                                                    LocationValue('Clabject.potency'): TupleValue((StringValue('potency'),)),
                                                    LocationValue('Association.is_abstract'): TupleValue((StringValue('abstract'),)),
                                                    LocationValue('Association.name'): TupleValue((StringValue('name'),)),
                                                    LocationValue('Association.from_min'): TupleValue((StringValue('from_multiplicity'), StringValue('lower'),)),
                                                    LocationValue('Association.from_max'): TupleValue((StringValue('from_multiplicity'), StringValue('upper'),)),
                                                    LocationValue('Association.from_port'): TupleValue((StringValue('from_multiplicity'), StringValue('port_name'),)),
                                                    LocationValue('Association.to_min'): TupleValue((StringValue('to_multiplicity'), StringValue('lower'),)),
                                                    LocationValue('Association.to_max'): TupleValue((StringValue('to_multiplicity'), StringValue('upper'),)),
                                                    LocationValue('Association.to_port'): TupleValue((StringValue('to_multiplicity'), StringValue('port_name'),)),
                                                    LocationValue('Attribute.name'): TupleValue((StringValue('name'),)),
                                                    LocationValue('Attribute.type'): TupleValue((StringValue('type'),)),
                                                    LocationValue('Attribute.default'): TupleValue((StringValue('default'),)),
                                                    LocationValue('Attribute.potency'): TupleValue((StringValue('potency'),)),
                                                    LocationValue('Inheritance.name'): TupleValue((StringValue('name'),)),
                                                    LocationValue('attributes.name'): TupleValue((StringValue('name'),))
                                                    })
        self.phys_actions_update = MappingValue({LocationValue('MultiDiagrams.name'): StringValue('set_name'),
                                                 LocationValue('MultiDiagrams.potency'): TupleValue((StringValue('set_potency'),)),
                                                 LocationValue('Clabject.is_abstract'): StringValue('set_abstract'),
                                                 LocationValue('Clabject.name'): StringValue('set_name'),
                                                 LocationValue('Clabject.potency'): TupleValue((StringValue('set_potency'),)),
                                                 LocationValue('Association.is_abstract'): StringValue('set_abstract'),
                                                 LocationValue('Association.name'): StringValue('set_name'),
                                                 LocationValue('Association.from_min'): StringValue('get_from_multiplicity().set_lower'),
                                                 LocationValue('Association.from_max'): StringValue('get_from_multiplicity().set_upper'),
                                                 LocationValue('Association.from_port'): StringValue('get_from_multiplicity().set_port_name'),
                                                 LocationValue('Association.to_min'): StringValue('get_to_multiplicity().set_lower'),
                                                 LocationValue('Association.to_max'): StringValue('get_to_multiplicity().set_upper'),
                                                 LocationValue('Association.to_port'): StringValue('get_to_multiplicity().set_port_name'),
                                                 LocationValue('Attribute.name'): StringValue('set_name'),
                                                 LocationValue('Attribute.type'): StringValue('set_type'),
                                                 LocationValue('Attribute.default'): StringValue('set_default'),
                                                 LocationValue('Attribute.potency'): TupleValue((StringValue('set_potency'),)),
                                                 LocationValue('Inheritance.name'): StringValue('set_name'),
                                                 LocationValue('attributes.name'): StringValue('set_name')})

    def __create_md(self, params):
        attributes = params[CreateConstants.ATTRS_KEY]
        attributes[StringValue('type_model')] = params[CreateConstants.TYPE_KEY]
        from mvk.mvk import MvK
        cl = MvK().create(MappingValue({CreateConstants.LOCATION_KEY: params[CreateConstants.LOCATION_KEY],
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.object.Model'),
                                        CreateConstants.ATTRS_KEY: attributes
                                        })
                          )
        a_cl = self.__create_attribute(MappingValue({CreateConstants.LOCATION_KEY: params[CreateConstants.LOCATION_KEY] + StringValue('.') + attributes[StringValue('MultiDiagrams.name')],
                                                     CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.MultiDiagrams.Attribute'),
                                                     CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                                              StringValue('Attribute.type'): StringType(),
                                                                                              StringValue('Attribute.default'): StringValue('')})
                                                     })
                                       )
        if not a_cl.is_success():
            cl.set_status_code(a_cl.get_status_code())
            cl.set_status_message(a_cl.get_status_message())
        return cl

    def __create_class(self, params):
        attributes = params[CreateConstants.ATTRS_KEY]
        attributes[StringValue('class')] = params[CreateConstants.TYPE_KEY]
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
        from mvk.mvk import MvK
        return MvK().create(MappingValue({CreateConstants.LOCATION_KEY: params[CreateConstants.LOCATION_KEY],
                                          CreateConstants.TYPE_KEY: LocationValue('mvk.object.Association'),
                                          CreateConstants.ATTRS_KEY: attributes
                                          })
                            )

    def __create_composition(self, params):
        attributes = params[CreateConstants.ATTRS_KEY]
        attributes[StringValue('class')] = params[CreateConstants.TYPE_KEY]
        from mvk.mvk import MvK
        return MvK().create(MappingValue({CreateConstants.LOCATION_KEY: params[CreateConstants.LOCATION_KEY],
                                          CreateConstants.TYPE_KEY: LocationValue('mvk.object.Composition'),
                                          CreateConstants.ATTRS_KEY: attributes
                                          })
                            )

    def __create_aggregation(self, params):
        attributes = params[CreateConstants.ATTRS_KEY]
        attributes[StringValue('class')] = params[CreateConstants.TYPE_KEY]
        from mvk.mvk import MvK
        return MvK().create(MappingValue({CreateConstants.LOCATION_KEY: params[CreateConstants.LOCATION_KEY],
                                          CreateConstants.TYPE_KEY: LocationValue('mvk.object.Aggregation'),
                                          CreateConstants.ATTRS_KEY: attributes
                                          })
                            )

    def __create_attribute(self, params):
        attributes = params[CreateConstants.ATTRS_KEY]
        attributes[StringValue('class')] = params[CreateConstants.TYPE_KEY]
        attributes[StringValue('lower')] = IntegerValue(1)
        attributes[StringValue('upper')] = IntegerValue(1)
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
                                                                                   StringValue('class'): LocationValue('protected.formalisms.MultiDiagrams.attributes'),
                                                                                   StringValue('from_class'): from_class,
                                                                                   StringValue('to_attr'): to_attr
                                                                                   })
                                          })
                            )
        if not a_cl.is_success():
            cl.set_status_code(a_cl.get_status_code())
            cl.set_status_message(a_cl.get_status_message())
        return cl

    def __create_inheritance(self, params):
        attributes = params[CreateConstants.ATTRS_KEY]
        attributes[StringValue('class')] = params[CreateConstants.TYPE_KEY]
        from mvk.mvk import MvK
        return MvK().create(MappingValue({CreateConstants.LOCATION_KEY: params[CreateConstants.LOCATION_KEY],
                                          CreateConstants.TYPE_KEY: LocationValue('mvk.object.Inherits'),
                                          CreateConstants.ATTRS_KEY: attributes
                                          })
                            )

    def __create_unknown(self, params):
        cl = MvKCreateLog()
        cl.set_status_code(CreateConstants.BAD_REQUEST_CODE)
        cl.set_status_message(StringValue('Unknown type!'))
        return cl

    def create(self, params):
        types = {LocationValue('protected.formalisms.MultiDiagrams'): self.__create_md,
                 LocationValue('protected.formalisms.MultiDiagrams.Clabject'): self.__create_class,
                 LocationValue('protected.formalisms.MultiDiagrams.Association'): self.__create_association,
                 LocationValue('protected.formalisms.MultiDiagrams.Composition'): self.__create_composition,
                 LocationValue('protected.formalisms.MultiDiagrams.Aggregation'): self.__create_aggregation,
                 LocationValue('protected.formalisms.MultiDiagrams.Attribute'): self.__create_attribute,
                 LocationValue('protected.formalisms.MultiDiagrams.Inheritance'): self.__create_inheritance}
        return types.get(params[CreateConstants.TYPE_KEY], self.__create_unknown)(params)

    def read(self, location):
        raise NotImplementedError()

    def update(self, params):
        types = {LocationValue('protected.formalisms.MultiDiagrams'): PythonRepresenter.MODEL,
                 LocationValue('protected.formalisms.MultiDiagrams.Clabject'): PythonRepresenter.CLABJECT,
                 LocationValue('protected.formalisms.MultiDiagrams.Association'): PythonRepresenter.ASSOCIATION,
                 LocationValue('protected.formalisms.MultiDiagrams.Composition'): PythonRepresenter.COMPOSITION,
                 LocationValue('protected.formalisms.MultiDiagrams.Aggregation'): PythonRepresenter.AGGREGATION,
                 LocationValue('protected.formalisms.MultiDiagrams.Attribute'): PythonRepresenter.ATTRIBUTE,
                 LocationValue('protected.formalisms.MultiDiagrams.Inheritance'): PythonRepresenter.INHERITS}
        from mvk.mvk import MvK
        params[UpdateConstants.TYPE_KEY] = types[params[UpdateConstants.TYPE_KEY]]
        item = MvK().read(params[UpdateConstants.LOCATION_KEY]).get_item()
        return item.update(params)

    def delete(self, location):
        raise NotImplementedError()

    def get_physical_attribute_mapping(self):
        return self.phys_attribute_mapping

    def get_physical_update_actions(self):
        return self.phys_actions_update

'''
class MDFormalismMapper(PhysicalMapper):
    def __init__(self, tm_loc, **kwds):
        assert (isinstance(tm_loc, mvk.interfaces.datavalue.LocationValue) and
                isinstance(tm_loc.typed_by(), mvk.interfaces.datatype.LocationType))
        from mvk.mvk import MvK
        self.tm_loc = tm_loc
        tm_log = MvK().read(self.tm_loc)
        assert tm_log.is_success(), tm_log
        self.tm = tm_log.get_item()
        super(MDFormalismMapper, self).__init__(**kwds)

    def create(self, params):
        from mvk.mvk import MvK
        type_to_create = MvK().read(params[CreateConstants.TYPE_KEY]).get_item()
        phys_type = None
        attributes = params[CreateConstants.ATTRS_KEY]
        if isinstance(type_to_create, mvk.interfaces.object.Model):
            attributes[StringValue('type_model')] = params[CreateConstants.TYPE_KEY]
            phys_type = PythonRepresenter.MODEL
        elif isinstance(type_to_create, mvk.interfaces.object.Association):
            attributes[StringValue('class')] = params[CreateConstants.TYPE_KEY]
            phys_type = PythonRepresenter.ASSOCIATION
        elif isinstance(type_to_create, mvk.interfaces.object.Clabject):
            attributes[StringValue('class')] = params[CreateConstants.TYPE_KEY]
            phys_type = PythonRepresenter.CLABJECT
        elif isinstance(type_to_create, mvk.interfaces.object.Attribute):
            attributes[StringValue('class')] = params[CreateConstants.TYPE_KEY]
            phys_type = PythonRepresenter.ATTRIBUTE
        attributes[StringValue('potency')] = type_to_create.get_potency() - IntegerValue(1)
        cl = MvK().create(MappingValue({CreateConstants.LOCATION_KEY: params[CreateConstants.LOCATION_KEY],
                                        CreateConstants.TYPE_KEY: phys_type,
                                        CreateConstants.ATTRS_KEY: attributes
                                        }))
        if phys_type == PythonRepresenter.MODEL and attributes[StringValue('potency')] > IntegerValue(0):
            MvK().register_mapper(params[CreateConstants.LOCATION_KEY], MDFormalismMapper(tm_loc=params[CreateConstants.LOCATION_KEY]))
        return cl

    def read(self, location):
        raise NotImplementedError()

    def update(self, params):
        from mvk.mvk import MvK
        type_to_update = MvK().read(params[CreateConstants.TYPE_KEY]).get_item()
        phys_type = None
        if isinstance(type_to_update, mvk.interfaces.object.Model):
            phys_type = PythonRepresenter.MODEL
        elif isinstance(type_to_update, mvk.interfaces.object.Association):
            phys_type = PythonRepresenter.ASSOCIATION
        elif isinstance(type_to_update, mvk.interfaces.object.Clabject):
            phys_type = PythonRepresenter.CLABJECT
        elif isinstance(type_to_update, mvk.interfaces.object.Attribute):
            phys_type = PythonRepresenter.ATTRIBUTE
        params[UpdateConstants.TYPE_KEY] = phys_type
        item = MvK().read(params[UpdateConstants.LOCATION_KEY]).get_item()
        cl = item.update(params)
        if phys_type == PythonRepresenter.MODEL and StringValue('name') in params[UpdateConstants.ATTRS_KEY] and cl.is_success():
            try:
                MvK().unregister_mapper(params[UpdateConstants.LOCATION_KEY])
            except Exception:
                pass
            MvK().register_mapper(item.get_location(),
                                  MDFormalismMapper(tm_loc=item.get_location()))
        return cl

    def delete(self, params):
        raise NotImplementedError()

    def get_physical_attribute_mapping(self):
        phys_attribute_mapping = MappingValue({self.tm.get_name() + StringValue('.') + StringValue('name'): TupleValue((StringValue('name'),))})
        it = self.tm.get_elements().__iter__()
        while it.has_next():
            el = self.tm.get_element(it.next())
            if isinstance(el.typed_by(), mvk.interfaces.object.Association):
                try:
                    id_field = el.get_attribute(el.typed_by().get_attribute(StringValue('id_field')).get_short_location()).get_value()
                    phys_attribute_mapping[id_field] = TupleValue((StringValue('name'),))
                except MvKKeyError:
                    assert el.is_abstract()
            elif isinstance(el.typed_by(), mvk.interfaces.object.Clabject):
                try:
                    id_field = el.get_attribute(el.typed_by().get_attribute(StringValue('id_field')).get_short_location()).get_value()
                    phys_attribute_mapping[id_field] = TupleValue((StringValue('name'),))
                except MvKKeyError:
                    assert el.is_abstract()
        return phys_attribute_mapping

    def get_physical_update_actions(self):
        phys_update_actions = MappingValue({self.tm.get_name() + StringValue('.') + StringValue('name'): StringValue('set_name')})
        it = self.tm.get_elements().__iter__()
        while it.has_next():
            el = self.tm.get_element(it.next())
            if isinstance(el.typed_by(), mvk.interfaces.object.Association):
                id_field = el.get_attribute(el.typed_by().get_attribute(StringValue('id_field')).get_short_location()).get_value()
                phys_update_actions[id_field] = StringValue('set_name')
            elif isinstance(el.typed_by(), mvk.interfaces.object.Clabject):
                id_field = el.get_attribute(el.typed_by().get_attribute(StringValue('id_field')).get_short_location()).get_value()
                phys_update_actions[id_field] = StringValue('set_name')
        return phys_update_actions
'''
