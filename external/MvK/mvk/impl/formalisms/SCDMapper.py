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


class SCDMapper(PhysicalMapper):
    def __init__(self, **kwds):
        super(SCDMapper, self).__init__(**kwds)
        self.phys_attribute_mapping = MappingValue({LocationValue('SimpleClassDiagrams.name'): TupleValue((StringValue('name'),)),
                                                    LocationValue('Class.is_abstract'): TupleValue((StringValue('abstract'),)),
                                                    LocationValue('Class.name'): TupleValue((StringValue('name'),)),
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
                                                    LocationValue('Inheritance.name'): TupleValue((StringValue('name'),)),
                                                    LocationValue('attributes.name'): TupleValue((StringValue('name'),))
                                                    })
        self.phys_actions_update = MappingValue({LocationValue('SimpleClassDiagrams.name'): StringValue('set_name'),
                                                 LocationValue('Class.is_abstract'): StringValue('set_abstract'),
                                                 LocationValue('Class.name'): StringValue('set_name'),
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
                                                 LocationValue('Inheritance.name'): StringValue('set_name'),
                                                 LocationValue('attributes.name'): StringValue('set_name')})

    def __create_cd(self, params):
        attributes = params[CreateConstants.ATTRS_KEY]
        attributes[StringValue('type_model')] = params[CreateConstants.TYPE_KEY]
        attributes[StringValue('potency')] = IntegerValue(1)
        from mvk.mvk import MvK
        cl = MvK().create(MappingValue({CreateConstants.LOCATION_KEY: params[CreateConstants.LOCATION_KEY],
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.object.Model'),
                                        CreateConstants.ATTRS_KEY: attributes
                                        })
                          )
        a_cl = self.__create_attribute(MappingValue({CreateConstants.LOCATION_KEY: params[CreateConstants.LOCATION_KEY] + StringValue('.') + attributes[StringValue('SimpleClassDiagrams.name')],
                                                     CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
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
            MvK().register_mapper(loc, SCDFormalismMapper(tm_loc=loc))
        return cl

    def __create_class(self, params):
        attributes = params[CreateConstants.ATTRS_KEY]
        attributes[StringValue('class')] = params[CreateConstants.TYPE_KEY]
        attributes[StringValue('potency')] = IntegerValue(1)
        from mvk.mvk import MvK
        cl = MvK().create(MappingValue({CreateConstants.LOCATION_KEY: params[CreateConstants.LOCATION_KEY],
                                        CreateConstants.TYPE_KEY: LocationValue('mvk.object.Clabject'),
                                        CreateConstants.ATTRS_KEY: attributes
                                        })
                          )
        '''
        Commented out because this does not work. The idea was to create a default name attribute, as an identifier for Classes. However, this does not
        work if there already is a superclass of this class with an id_field attribute: then this one is created for nothing.

        if cl.is_success() and not attributes[StringValue('Class.is_abstract')]:
            item = MvK().read(params[CreateConstants.LOCATION_KEY] + StringValue('.') + attributes[StringValue('Class.name')]).get_item()
            create_attr = False
            try:
                attr = item.get_attribute(StringValue('Class.id_field'))
                val = attr.get_value()
                print item.get_name(), ' ', val
                if val == StringValue('') or val is None:
                    create_attr = True
            except MvKKeyError:
                create_attr = True
            if create_attr:
                MvK().update({CreateConstants.LOCATION_KEY: item.get_location(),
                              CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
                              CreateConstants.ATTRS_KEY: MappingValue({StringValue('Class.id_field'): item.get_name() + StringValue('.') + StringValue('name')})})
                self.__create_attribute(MappingValue({CreateConstants.LOCATION_KEY: params[CreateConstants.LOCATION_KEY] + StringValue('.') + attributes[StringValue('Class.name')],
                                                      CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
                                                      CreateConstants.ATTRS_KEY: MappingValue({StringValue('Attribute.name'): StringValue('name'),
                                                                                               StringValue('Attribute.type'): StringType(),
                                                                                               StringValue('Attribute.default'): StringValue('')})
                                                      })
                                        )
        '''
        return cl

    def __create_association(self, params, phys_type=LocationValue('mvk.object.Association')):
        attributes = params[CreateConstants.ATTRS_KEY]
        attributes[StringValue('class')] = params[CreateConstants.TYPE_KEY]
        attributes[StringValue('potency')] = IntegerValue(1)
        from mvk.mvk import MvK
        return MvK().create(MappingValue({CreateConstants.LOCATION_KEY: params[CreateConstants.LOCATION_KEY],
                                          CreateConstants.TYPE_KEY: phys_type,
                                          CreateConstants.ATTRS_KEY: attributes
                                          })
                            )

    def __create_attribute(self, params):
        attributes = params[CreateConstants.ATTRS_KEY]
        attributes[StringValue('class')] = params[CreateConstants.TYPE_KEY]
        attributes[StringValue('potency')] = IntegerValue(1)
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
                                          CreateConstants.ATTRS_KEY: MappingValue({StringValue('attributes.name'): ClabjectReference(from_class).typed_by().get_name() + ClabjectReference(from_class).get_name() + StringValue('_a_') + attributes[StringValue('Attribute.name')],
                                                                                   StringValue('potency'): IntegerValue(0),
                                                                                   StringValue('class'): LocationValue('protected.formalisms.SimpleClassDiagrams.attributes'),
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
        cl.set_status_message(StringValue('Unknown type: ' + str(params[StringValue('type')])))
        return cl

    def create(self, params):
        types = {LocationValue('protected.formalisms.SimpleClassDiagrams'): self.__create_cd,
                 LocationValue('protected.formalisms.SimpleClassDiagrams.Class'): self.__create_class,
                 LocationValue('protected.formalisms.SimpleClassDiagrams.Association'): self.__create_association,
                 LocationValue('protected.formalisms.SimpleClassDiagrams.Composition'): lambda params: self.__create_association(params, LocationValue('mvk.object.Composition')),
                 LocationValue('protected.formalisms.SimpleClassDiagrams.Aggregation'): lambda params: self.__create_association(params, LocationValue('mvk.object.Aggregation')),
                 LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'): self.__create_attribute,
                 LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'): self.__create_inheritance}
        return types.get(params[CreateConstants.TYPE_KEY], self.__create_unknown)(params)

    def read(self, location):
        raise NotImplementedError()

    def update(self, params):
        types = {LocationValue('protected.formalisms.SimpleClassDiagrams'): PythonRepresenter.MODEL,
                 LocationValue('protected.formalisms.SimpleClassDiagrams.Class'): PythonRepresenter.CLABJECT,
                 LocationValue('protected.formalisms.SimpleClassDiagrams.Association'): PythonRepresenter.ASSOCIATION,
                 LocationValue('protected.formalisms.SimpleClassDiagrams.Composition'): PythonRepresenter.COMPOSITION,
                 LocationValue('protected.formalisms.SimpleClassDiagrams.Aggregation'): PythonRepresenter.AGGREGATION,
                 LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'): PythonRepresenter.ATTRIBUTE,
                 LocationValue('protected.formalisms.SimpleClassDiagrams.Inheritance'): PythonRepresenter.INHERITS}
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
                                  SCDFormalismMapper(tm_loc=item.get_location()))
        return cl

    def delete(self, location):
        raise NotImplementedError()

    def get_physical_attribute_mapping(self):
        return self.phys_attribute_mapping

    def get_physical_update_actions(self):
        return self.phys_actions_update


class SCDFormalismMapper(PhysicalMapper):
    s = frozenset([LocationValue('protected.formalisms.SimpleClassDiagrams.Class'), LocationValue('protected.formalisms.SimpleClassDiagrams.Association'), LocationValue('protected.formalisms.SimpleClassDiagrams.Composition'), LocationValue('protected.formalisms.SimpleClassDiagrams.Aggregation')])
    id_field_cache = {}
    types = {LocationValue('protected.formalisms.SimpleClassDiagrams'): PythonRepresenter.MODEL,
             LocationValue('protected.formalisms.SimpleClassDiagrams.Class'): PythonRepresenter.CLABJECT,
             LocationValue('protected.formalisms.SimpleClassDiagrams.Association'): PythonRepresenter.ASSOCIATION,
             LocationValue('protected.formalisms.SimpleClassDiagrams.Composition'): PythonRepresenter.COMPOSITION,
             LocationValue('protected.formalisms.SimpleClassDiagrams.Aggregation'): PythonRepresenter.AGGREGATION,
             LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'): PythonRepresenter.ATTRIBUTE}

    def __init__(self, tm_loc, **kwds):
        assert (isinstance(tm_loc, mvk.interfaces.datavalue.LocationValue) and
                isinstance(tm_loc.typed_by(), mvk.interfaces.datatype.LocationType))
        from mvk.mvk import MvK
        self.tm_loc = tm_loc
        tm_log = MvK().read(self.tm_loc)
        assert tm_log.is_success(), tm_log
        self.tm = tm_log.get_item()
        super(SCDFormalismMapper, self).__init__(**kwds)

    def create(self, params):
        from mvk.mvk import MvK
        type_to_create = MvK().read(params[CreateConstants.TYPE_KEY]).get_item()
        attributes = params[CreateConstants.ATTRS_KEY]
        if SCDFormalismMapper.types[type_to_create.typed_by().get_location()] == PythonRepresenter.MODEL:
            attributes[StringValue('type_model')] = params[CreateConstants.TYPE_KEY]
        else:
            attributes[StringValue('class')] = params[CreateConstants.TYPE_KEY]
        attributes[StringValue('potency')] = IntegerValue(0)
        return MvK().create(MappingValue({CreateConstants.LOCATION_KEY: params[CreateConstants.LOCATION_KEY],
                                          CreateConstants.TYPE_KEY: SCDFormalismMapper.types[type_to_create.typed_by().get_location()],
                                          CreateConstants.ATTRS_KEY: attributes
                                          }))

    def read(self, location):
        raise NotImplementedError()

    def update(self, params):
        from mvk.mvk import MvK
        type_to_update = MvK().read(params[CreateConstants.TYPE_KEY]).get_item()
        params[UpdateConstants.TYPE_KEY] = SCDFormalismMapper.types[type_to_update.typed_by().get_location()]
        item = MvK().read(params[UpdateConstants.LOCATION_KEY]).get_item()
        return item.update(params)

    def delete(self, params):
        raise NotImplementedError()

    def get_physical_attribute_mapping(self):
        id_field_cache = SCDFormalismMapper.id_field_cache
        s = SCDFormalismMapper.s
        nametuple = TupleValue((StringValue("name"),))
        phys_attribute_mapping = {self.tm.get_name() + StringValue('.name'): nametuple}
        for el in self.tm.get_elements().get_value().values():
            # typed_by() always returns a reference, so exploit this
            # Though I admit that this is not that elegant...
            try:
                id_field = id_field_cache[id(el)]
                if id_field is None:
                    # Negative cache entry, so ignore
                    continue
            except KeyError:
                if el.typed_by().get_location() in s:
                    try:
                        id_field = id_field_cache[id(el)] = el.get_attribute(StringValue('Class.id_field')).get_value()
                    except:
                        # Something went wrong, so ignore
                        id_field_cache[id(el)] = None
                        continue
                else:
                    id_field_cache[id(el)] = None
                    continue
            phys_attribute_mapping[id_field] = nametuple
        return MappingValue(phys_attribute_mapping)

    def get_physical_update_actions(self):
        phys_update_actions = MappingValue({self.tm.get_name() + StringValue('.') + StringValue('name'): StringValue('set_name')})
        elements = self.tm.get_elements()
        for el_k in elements:
            el = elements[el_k]
            loc = el.typed_by().get_location()
            if loc in SCDFormalismMapper.s:
                id_field = el.get_attribute(StringValue('Class.id_field')).get_value()
                phys_update_actions[id_field] = StringValue('set_name')
        return phys_update_actions
