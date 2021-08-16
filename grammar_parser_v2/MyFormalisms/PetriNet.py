# -*- coding: utf-8 -*-

from mvk.impl.python.constants import CreateConstants, UpdateConstants
from mvk.impl.python.datatype import TypeFactory, Type, IntegerType, StringType, \
    BooleanType, FloatType
from mvk.impl.python.datavalue import MappingValue, \
    LocationValue, StringValue, FloatValue, \
    IntegerValue, BooleanValue, InfiniteValue, Iterator
from mvk.impl.python.object import ClabjectReference, Clabject
from mvk.mvk import MvK
import sys

class Gen():

    def __init__(self, modelVerseKernel = None):
        self.mvk = None
        if modelVerseKernel:
            self.mvk = modelVerseKernel
        else:
            self.mvk = MvK()

    def instance(self):
        cl = self.mvk.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams'),
        CreateConstants.LOCATION_KEY: LocationValue('MyFormalisms'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('SimpleClassDiagrams.name'): StringValue('PetriNet')})
        }))
        cl = self.mvk.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
        CreateConstants.LOCATION_KEY: LocationValue('MyFormalisms.PetriNet'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Attribute.name'): StringValue('name'),
        StringValue('Attribute.type'): StringType(),
        StringValue('Attribute.default'): StringValue('')})
        }))
        cl = self.mvk.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
        CreateConstants.LOCATION_KEY: LocationValue('MyFormalisms.PetriNet'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Class.is_abstract'): BooleanValue(False),
        StringValue('Class.name'): StringValue('Transition'),
        StringValue('Class.id_field'): StringValue('Transition.name')})
        }))
        cl = self.mvk.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
        CreateConstants.LOCATION_KEY: LocationValue('MyFormalisms.PetriNet.Transition'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Attribute.name'): StringValue('name'),
        StringValue('Attribute.type'): StringType()})
        }))
        cl = self.mvk.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Class'),
        CreateConstants.LOCATION_KEY: LocationValue('MyFormalisms.PetriNet'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Class.is_abstract'): BooleanValue(False),
        StringValue('Class.name'): StringValue('Place'),
        StringValue('Class.id_field'): StringValue('Place.name')})
        }))
        cl = self.mvk.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
        CreateConstants.LOCATION_KEY: LocationValue('MyFormalisms.PetriNet.Place'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Attribute.name'): StringValue('token'),
        StringValue('Attribute.type'): IntegerType(),
        StringValue('Attribute.default'): IntegerValue(0)})
        }))
        cl = self.mvk.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
        CreateConstants.LOCATION_KEY: LocationValue('MyFormalisms.PetriNet.Place'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Attribute.name'): StringValue('capacity'),
        StringValue('Attribute.type'): IntegerType(),
        StringValue('Attribute.default'): IntegerValue(sys.maxint)})
        }))
        cl = self.mvk.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
        CreateConstants.LOCATION_KEY: LocationValue('MyFormalisms.PetriNet.Place'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Attribute.name'): StringValue('name'),
        StringValue('Attribute.type'): StringType()})
        }))
        cl = self.mvk.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Association'),
        CreateConstants.LOCATION_KEY: LocationValue('MyFormalisms.PetriNet'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Association.to_max'): InfiniteValue('inf'),
        StringValue('Association.from_max'): InfiniteValue('inf'),
        StringValue('Association.from_port'): StringValue('from_transition'),
        StringValue('Association.to_min'): IntegerValue(0),
        StringValue('Class.name'): StringValue('OutArc'),
        StringValue('Association.to_port'): StringValue('to_place'),
        StringValue('Class.is_abstract'): BooleanValue(True),
        StringValue('Association.from_min'): IntegerValue(0),
        StringValue('Class.id_field'): StringValue('OutArc.name'),
        StringValue('from_class'): LocationValue('MyFormalisms.PetriNet.Transition'),
        StringValue('to_class'): LocationValue('MyFormalisms.PetriNet.Place')})
        }))
        cl = self.mvk.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
        CreateConstants.LOCATION_KEY: LocationValue('MyFormalisms.PetriNet.OutArc'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Attribute.name'): StringValue('name'),
        StringValue('Attribute.type'): StringType()})
        }))
        cl = self.mvk.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
        CreateConstants.LOCATION_KEY: LocationValue('MyFormalisms.PetriNet.OutArc'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Attribute.name'): StringValue('weight'),
        StringValue('Attribute.type'): IntegerType(),
        StringValue('Attribute.default'): IntegerValue(1)})
        }))
        cl = self.mvk.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Association'),
        CreateConstants.LOCATION_KEY: LocationValue('MyFormalisms.PetriNet'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Association.to_max'): InfiniteValue('inf'),
        StringValue('Association.from_max'): InfiniteValue('inf'),
        StringValue('Association.from_port'): StringValue('from_place'),
        StringValue('Association.to_min'): IntegerValue(0),
        StringValue('Class.name'): StringValue('InArc'),
        StringValue('Association.to_port'): StringValue('to_transition'),
        StringValue('Class.is_abstract'): BooleanValue(True),
        StringValue('Association.from_min'): IntegerValue(0),
        StringValue('Class.id_field'): StringValue('InArc.name'),
        StringValue('from_class'): LocationValue('MyFormalisms.PetriNet.Place'),
        StringValue('to_class'): LocationValue('MyFormalisms.PetriNet.Transition')})
        }))
        cl = self.mvk.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
        CreateConstants.LOCATION_KEY: LocationValue('MyFormalisms.PetriNet.InArc'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Attribute.name'): StringValue('name'),
        StringValue('Attribute.type'): StringType()})
        }))
        cl = self.mvk.create(MappingValue({
        CreateConstants.TYPE_KEY: LocationValue('protected.formalisms.SimpleClassDiagrams.Attribute'),
        CreateConstants.LOCATION_KEY: LocationValue('MyFormalisms.PetriNet.InArc'),
        CreateConstants.ATTRS_KEY: MappingValue({
        StringValue('Attribute.name'): StringValue('weight'),
        StringValue('Attribute.type'): IntegerType(),
        StringValue('Attribute.default'): IntegerValue(1)})
        }))