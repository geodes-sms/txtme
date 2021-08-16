# -*- coding: utf-8 -*-

from mvk.impl.python.constants import CreateConstants, UpdateConstants
from mvk.impl.python.datatype import TypeFactory, Type, IntegerType, StringType, \
    BooleanType, FloatType
from mvk.impl.python.datavalue import MappingValue, \
    LocationValue, StringValue, FloatValue, \
    IntegerValue, BooleanValue, InfiniteValue, Iterator
from mvk.impl.python.object import ClabjectReference, Clabject
from mvk.mvk import MvK


class Gen(object):
    def __init__(self):
        self.mvk = MvK()

    def instance(self):
        print('addNameToLabel(Model, protected.formalisms.SimpleClassDiagrams)')
        print('addNameToLabel(ActionModel, protected.formalisms.ActionLanguage)')
        print('addElement(MyFormalisms, protected.formalisms.SimpleClassDiagrams, {u"name": {"type": "StringType", "value": u"PetriNet"}})')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.SimpleClassDiagrams"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("SimpleClassDiagrams.name"): StringValue("PetriNet")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addElement(MyFormalisms.PetriNet, Class, {u"name": {"type": "StringType", "value": u"Place"}, u"id_field": {"type": "StringType", "value": u"Place.name"}})')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.SimpleClassDiagrams.Class"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.PetriNet"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Class.name"): StringValue("Place"),
                StringValue("Class.id_field"): StringValue("Place.name")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addElement(MyFormalisms.PetriNet.Place, Attribute, {u"type": {"type": "Type", "value": u"String"}, u"name": {"type": "StringType", "value": u"name"}})')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.SimpleClassDiagrams.Attribute"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.PetriNet.Place"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Attribute.type"): StringType(),
                StringValue("Attribute.name"): StringValue("name")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addElement(MyFormalisms.PetriNet.Place, Attribute, {u"default": {"type": "IntegerType", "value": 0}, u"type": {"type": "Type", "value": u"Integer"}, u"name": {"type": "StringType", "value": u"token"}})')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.SimpleClassDiagrams.Attribute"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.PetriNet.Place"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Attribute.type"): IntegerType(),
                StringValue("Attribute.default"): IntegerValue(0),
                StringValue("Attribute.name"): StringValue("token")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addElement(MyFormalisms.PetriNet, Class, {u"name": {"type": "StringType", "value": u"Transition"}, u"id_field": {"type": "StringType", "value": u"Transition.name"}})')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.SimpleClassDiagrams.Class"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.PetriNet"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Class.name"): StringValue("Transition"),
                StringValue("Class.id_field"): StringValue("Transition.name")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addElement(MyFormalisms.PetriNet.Transition, Attribute, {u"type": {"type": "Type", "value": u"String"}, u"name": {"type": "StringType", "value": u"name"}})')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.SimpleClassDiagrams.Attribute"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.PetriNet.Transition"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Attribute.type"): StringType(),
                StringValue("Attribute.name"): StringValue("name")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addElement(MyFormalisms.PetriNet, Association, {u"from_max": {"type": "CardType", "value": u"*"}, u"name": {"type": "StringType", "value": u"InArc"}, u"to_port": {"type": "StringType", "value": u"to_transition"}, u"to_max": {"type": "CardType", "value": u"*"}, u"from_min": {"type": "IntegerType", "value": 0}, u"id_field": {"type": "StringType", "value": u"InArc.name"}, u"from_port": {"type": "StringType", "value": u"from_place"}, u"to_min": {"type": "IntegerType", "value": 0}, u"to_class": {"type": "NamedType", "value": u"Transition"}, u"from_class": {"type": "NamedType", "value": u"Place"}, u"is_abstract": {"type": "BooleanType", "value": True}})')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.SimpleClassDiagrams.Association"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.PetriNet"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Association.to_min"): IntegerValue(0),
                StringValue("Association.to_port"): StringValue("to_transition"),
                StringValue("Association.from_port"): StringValue("from_place"),
                StringValue("to_class"): LocationValue("MyFormalisms.PetriNet.Transition"),
                StringValue("Association.from_min"): IntegerValue(0),
                StringValue("from_class"): LocationValue("MyFormalisms.PetriNet.Place"),
                StringValue("Class.name"): StringValue("InArc"),
                StringValue("Class.id_field"): StringValue("InArc.name"),
                StringValue("Association.to_max"): InfiniteValue("inf"),
                StringValue("Class.is_abstract"): BooleanValue(True),
                StringValue("Association.from_max"): InfiniteValue("inf")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addElement(MyFormalisms.PetriNet.InArc, Attribute, {u"type": {"type": "Type", "value": u"String"}, u"name": {"type": "StringType", "value": u"name"}})')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.SimpleClassDiagrams.Attribute"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.PetriNet.InArc"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Attribute.type"): StringType(),
                StringValue("Attribute.name"): StringValue("name")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addElement(MyFormalisms.PetriNet.InArc, Attribute, {u"default": {"type": "IntegerType", "value": 1}, u"type": {"type": "Type", "value": u"Integer"}, u"name": {"type": "StringType", "value": u"weight"}})')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.SimpleClassDiagrams.Attribute"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.PetriNet.InArc"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Attribute.type"): IntegerType(),
                StringValue("Attribute.default"): IntegerValue(1),
                StringValue("Attribute.name"): StringValue("weight")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addElement(MyFormalisms.PetriNet, Association, {u"from_max": {"type": "CardType", "value": u"*"}, u"name": {"type": "StringType", "value": u"OutArc"}, u"to_port": {"type": "StringType", "value": u"to_place"}, u"to_max": {"type": "CardType", "value": u"*"}, u"from_min": {"type": "IntegerType", "value": 0}, u"id_field": {"type": "StringType", "value": u"OutArc.name"}, u"from_port": {"type": "StringType", "value": u"from_transition"}, u"to_min": {"type": "IntegerType", "value": 0}, u"to_class": {"type": "NamedType", "value": u"Place"}, u"from_class": {"type": "NamedType", "value": u"Transition"}, u"is_abstract": {"type": "BooleanType", "value": True}})')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.SimpleClassDiagrams.Association"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.PetriNet"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Association.to_min"): IntegerValue(0),
                StringValue("Association.to_port"): StringValue("to_place"),
                StringValue("Association.from_port"): StringValue("from_transition"),
                StringValue("to_class"): LocationValue("MyFormalisms.PetriNet.Place"),
                StringValue("Association.from_min"): IntegerValue(0),
                StringValue("from_class"): LocationValue("MyFormalisms.PetriNet.Transition"),
                StringValue("Class.name"): StringValue("OutArc"),
                StringValue("Class.id_field"): StringValue("OutArc.name"),
                StringValue("Association.to_max"): InfiniteValue("inf"),
                StringValue("Class.is_abstract"): BooleanValue(True),
                StringValue("Association.from_max"): InfiniteValue("inf")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addElement(MyFormalisms.PetriNet.OutArc, Attribute, {u"type": {"type": "Type", "value": u"String"}, u"name": {"type": "StringType", "value": u"name"}})')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.SimpleClassDiagrams.Attribute"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.PetriNet.OutArc"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Attribute.type"): StringType(),
                StringValue("Attribute.name"): StringValue("name")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addElement(MyFormalisms.PetriNet.OutArc, Attribute, {u"default": {"type": "IntegerType", "value": 1}, u"type": {"type": "Type", "value": u"Integer"}, u"name": {"type": "StringType", "value": u"weight"}})')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.SimpleClassDiagrams.Attribute"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.PetriNet.OutArc"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Attribute.type"): IntegerType(),
                StringValue("Attribute.default"): IntegerValue(1),
                StringValue("Attribute.name"): StringValue("weight")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addElement(MyFormalisms, PetriNet, {u"name": {"type": "StringType", "value": u"pnInstance"}})')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("MyFormalisms.PetriNet"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("PetriNet.name"): StringValue("pnInstance")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addElement(MyFormalisms.pnInstance, Place, {u"token": {"type": "IntegerType", "value": 1}, u"name": {"type": "StringType", "value": u"ab"}})')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("MyFormalisms.PetriNet.Place"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.pnInstance"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Place.name"): StringValue("ab"),
                StringValue("Place.token"): IntegerValue(1)
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addElement(MyFormalisms.pnInstance, Place, {u"token": {"type": "IntegerType", "value": 2}, u"name": {"type": "StringType", "value": u"ba"}})')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("MyFormalisms.PetriNet.Place"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.pnInstance"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Place.name"): StringValue("ba"),
                StringValue("Place.token"): IntegerValue(2)
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addElement(MyFormalisms.pnInstance, Transition, {u"name": {"type": "StringType", "value": u"t1"}})')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("MyFormalisms.PetriNet.Transition"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.pnInstance"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Transition.name"): StringValue("t1")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addElement(MyFormalisms.pnInstance, InArc, {u"to_transition": {"type": "NamedType", "value": u"t1"}, u"name": {"type": "StringType", "value": u"p2t"}, u"from_place": {"type": "NamedType", "value": u"ab"}})')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("MyFormalisms.PetriNet.InArc"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.pnInstance"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("InArc.name"): StringValue("p2t"),
                StringValue("to_transition"): LocationValue("MyFormalisms.pnInstance.t1"),
                StringValue("from_place"): LocationValue("MyFormalisms.pnInstance.ab")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addElement(MyFormalisms.pnInstance, OutArc, {u"from_transition": {"type": "NamedType", "value": u"t1"}, u"name": {"type": "StringType", "value": u"t2p"}, u"to_place": {"type": "NamedType", "value": u"ab"}})')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("MyFormalisms.PetriNet.OutArc"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.pnInstance"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("from_transition"): LocationValue("MyFormalisms.pnInstance.t1"),
                StringValue("OutArc.name"): StringValue("t2p"),
                StringValue("to_place"): LocationValue("MyFormalisms.pnInstance.ab")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addElement(MyFormalisms, protected.formalisms.ActionLanguage, {u"name": {"type": "StringType", "value": u"Utilities"}})')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("ActionLanguage.name"): StringValue("Utilities")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addFunction(MyFormalisms.Utilities, z, PetriNet.Place)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Function"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Function.type"): ClabjectReference(LocationValue("MyFormalisms.PetriNet.Place")),
                StringValue("Function.name"): StringValue("z")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addFunctionParameter(MyFormalisms.Utilities, z, a, Integer, in)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Parameter"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Parameter.parameter_type"): StringValue("in"),
                StringValue("Parameter.name"): StringValue("a"),
                StringValue("Parameter.type"): IntegerType()
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addFunctionParameter(MyFormalisms.Utilities, z, b, Boolean, inout)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Parameter"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Parameter.parameter_type"): StringValue("inout"),
                StringValue("Parameter.name"): StringValue("b"),
                StringValue("Parameter.type"): BooleanType()
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addFunctionParameter(MyFormalisms.Utilities, z, c, String, out)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Parameter"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Parameter.parameter_type"): StringValue("out"),
                StringValue("Parameter.name"): StringValue("c"),
                StringValue("Parameter.type"): StringType()
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addDeclarationStm(MyFormalisms.Utilities.z.body, type_declaration1)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.DeclarationStatement"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Statement.name"): StringValue("type_declaration1")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addIdentifier(MyFormalisms.Utilities.z.body.type_declaration1, PetriNet.Place, p1)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Identifier"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.type_declaration1"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("p1"),
                StringValue("Identifier.type"): ClabjectReference(LocationValue("MyFormalisms.PetriNet.Place"))
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addFunctionCall(MyFormalisms.Utilities.z.body.type_declaration1, funccall_expr2, PetriNet.Place)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.FunctionCall"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.type_declaration1"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("funccall_expr2"),
                StringValue("FunctionCall.function_name"): StringValue("PetriNet.Place")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addArgument(MyFormalisms.Utilities.z.body.type_declaration1.funccall_expr2, argument3, token)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Argument"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.type_declaration1.funccall_expr2"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Argument.key"): StringValue("token"),
                StringValue("Argument.name"): StringValue("argument3")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addConstant(MyFormalisms.Utilities.z.body.type_declaration1.funccall_expr2.argument3, atomvalue4, 2, IntegerType)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Constant"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.type_declaration1.funccall_expr2.argument3"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("atomvalue4"),
                StringValue("Constant.value"): IntegerValue(2),
                StringValue("Constant.type"): IntegerType()
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addExpressionStatement(MyFormalisms.Utilities.z.body, expression5)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.ExpressionStatement"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Statement.name"): StringValue("expression5")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addAssignmentStm(MyFormalisms.Utilities.z.body.expression5, assignment6)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Assignment"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.expression5"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("assignment6")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addNavigation(MyFormalisms.Utilities.z.body.expression5.assignment6, navigation7, p1.token)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Navigation"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.expression5.assignment6"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("navigation7"),
                StringValue("Navigation.path"): LocationValue("p1.token")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addSum(MyFormalisms.Utilities.z.body.expression5.assignment6, sumexpr8)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Plus"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.expression5.assignment6"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("sumexpr8")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addNavigation(MyFormalisms.Utilities.z.body.expression5.assignment6.sumexpr8, navigation9, p1.token)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Navigation"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.expression5.assignment6.sumexpr8"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("navigation9"),
                StringValue("Navigation.path"): LocationValue("p1.token")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addNavigation(MyFormalisms.Utilities.z.body.expression5.assignment6.sumexpr8, navigation10, a)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Navigation"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.expression5.assignment6.sumexpr8"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("navigation10"),
                StringValue("Navigation.path"): LocationValue("a")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addExpressionStatement(MyFormalisms.Utilities.z.body, expression11)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.ExpressionStatement"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Statement.name"): StringValue("expression11")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addFunctionCall(MyFormalisms.Utilities.z.body.expression11, funccall_expr12, mvk.create)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.FunctionCall"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.expression11"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("funccall_expr12"),
                StringValue("FunctionCall.function_name"): StringValue("mvk.create")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addArgument(MyFormalisms.Utilities.z.body.expression11.funccall_expr12, argument13, )')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Argument"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.expression11.funccall_expr12"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Argument.key"): StringValue(""),
                StringValue("Argument.name"): StringValue("argument13")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addNavigation(MyFormalisms.Utilities.z.body.expression11.funccall_expr12.argument13, navigation14, p1)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Navigation"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.expression11.funccall_expr12.argument13"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("navigation14"),
                StringValue("Navigation.path"): LocationValue("p1")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addArgument(MyFormalisms.Utilities.z.body.expression11.funccall_expr12, argument15, )')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Argument"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.expression11.funccall_expr12"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Argument.key"): StringValue(""),
                StringValue("Argument.name"): StringValue("argument15")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addNavigation(MyFormalisms.Utilities.z.body.expression11.funccall_expr12.argument15, navigation16, pnInstance)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Navigation"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.expression11.funccall_expr12.argument15"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("navigation16"),
                StringValue("Navigation.path"): LocationValue("pnInstance")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addArgument(MyFormalisms.Utilities.z.body.expression11.funccall_expr12, argument17, )')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Argument"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.expression11.funccall_expr12"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Argument.key"): StringValue(""),
                StringValue("Argument.name"): StringValue("argument17")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addConstant(MyFormalisms.Utilities.z.body.expression11.funccall_expr12.argument17, atomvalue18, newplace, StringType)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Constant"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.expression11.funccall_expr12.argument17"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("atomvalue18"),
                StringValue("Constant.value"): StringValue("newplace"),
                StringValue("Constant.type"): StringType()
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addDeclarationStm(MyFormalisms.Utilities.z.body, type_declaration19)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.DeclarationStatement"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Statement.name"): StringValue("type_declaration19")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addIdentifier(MyFormalisms.Utilities.z.body.type_declaration19, PetriNet.Place, p3)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Identifier"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.type_declaration19"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("p3"),
                StringValue("Identifier.type"): ClabjectReference(LocationValue("MyFormalisms.PetriNet.Place"))
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addFunctionCall(MyFormalisms.Utilities.z.body.type_declaration19, funccall_expr20, mvk.read)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.FunctionCall"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.type_declaration19"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("funccall_expr20"),
                StringValue("FunctionCall.function_name"): StringValue("mvk.read")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addArgument(MyFormalisms.Utilities.z.body.type_declaration19.funccall_expr20, argument21, )')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Argument"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.type_declaration19.funccall_expr20"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Argument.key"): StringValue(""),
                StringValue("Argument.name"): StringValue("argument21")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addConstant(MyFormalisms.Utilities.z.body.type_declaration19.funccall_expr20.argument21, atomvalue22, MyFormalisms.pnInstance.newplace, StringType)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Constant"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.type_declaration19.funccall_expr20.argument21"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("atomvalue22"),
                StringValue("Constant.value"): StringValue("MyFormalisms.pnInstance.newplace"),
                StringValue("Constant.type"): StringType()
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addDeclarationStm(MyFormalisms.Utilities.z.body, type_declaration23)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.DeclarationStatement"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Statement.name"): StringValue("type_declaration23")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addIdentifier(MyFormalisms.Utilities.z.body.type_declaration23, PetriNet.Place, p2)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Identifier"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.type_declaration23"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("p2"),
                StringValue("Identifier.type"): ClabjectReference(LocationValue("MyFormalisms.PetriNet.Place"))
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addNavigation(MyFormalisms.Utilities.z.body.type_declaration23, navigation24, pnInstance.newplace)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Navigation"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.type_declaration23"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("navigation24"),
                StringValue("Navigation.path"): LocationValue("pnInstance.newplace")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addDeclarationStm(MyFormalisms.Utilities.z.body, type_declaration25)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.DeclarationStatement"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Statement.name"): StringValue("type_declaration25")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addIdentifier(MyFormalisms.Utilities.z.body.type_declaration25, PetriNet.Transition, t2)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Identifier"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.type_declaration25"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("t2"),
                StringValue("Identifier.type"): ClabjectReference(LocationValue("MyFormalisms.PetriNet.Transition"))
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addFunctionCall(MyFormalisms.Utilities.z.body.type_declaration25, funccall_expr26, PetriNet.Transition)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.FunctionCall"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.type_declaration25"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("funccall_expr26"),
                StringValue("FunctionCall.function_name"): StringValue("PetriNet.Transition")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addArgument(MyFormalisms.Utilities.z.body.type_declaration25.funccall_expr26, argument27, name)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Argument"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.type_declaration25.funccall_expr26"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Argument.key"): StringValue("name"),
                StringValue("Argument.name"): StringValue("argument27")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addConstant(MyFormalisms.Utilities.z.body.type_declaration25.funccall_expr26.argument27, atomvalue28, t2, StringType)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Constant"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.type_declaration25.funccall_expr26.argument27"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("atomvalue28"),
                StringValue("Constant.value"): StringValue("t2"),
                StringValue("Constant.type"): StringType()
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addExpressionStatement(MyFormalisms.Utilities.z.body, expression29)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.ExpressionStatement"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Statement.name"): StringValue("expression29")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addFunctionCall(MyFormalisms.Utilities.z.body.expression29, funccall_expr30, mvk.create)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.FunctionCall"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.expression29"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("funccall_expr30"),
                StringValue("FunctionCall.function_name"): StringValue("mvk.create")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addArgument(MyFormalisms.Utilities.z.body.expression29.funccall_expr30, argument31, )')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Argument"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.expression29.funccall_expr30"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Argument.key"): StringValue(""),
                StringValue("Argument.name"): StringValue("argument31")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addNavigation(MyFormalisms.Utilities.z.body.expression29.funccall_expr30.argument31, navigation32, t2)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Navigation"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.expression29.funccall_expr30.argument31"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("navigation32"),
                StringValue("Navigation.path"): LocationValue("t2")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addArgument(MyFormalisms.Utilities.z.body.expression29.funccall_expr30, argument33, )')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Argument"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.expression29.funccall_expr30"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Argument.key"): StringValue(""),
                StringValue("Argument.name"): StringValue("argument33")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addNavigation(MyFormalisms.Utilities.z.body.expression29.funccall_expr30.argument33, navigation34, pnInstance)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Navigation"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.expression29.funccall_expr30.argument33"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("navigation34"),
                StringValue("Navigation.path"): LocationValue("pnInstance")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addArgument(MyFormalisms.Utilities.z.body.expression29.funccall_expr30, argument35, )')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Argument"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.expression29.funccall_expr30"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Argument.key"): StringValue(""),
                StringValue("Argument.name"): StringValue("argument35")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addConstant(MyFormalisms.Utilities.z.body.expression29.funccall_expr30.argument35, atomvalue36, t2, StringType)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Constant"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.expression29.funccall_expr30.argument35"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("atomvalue36"),
                StringValue("Constant.value"): StringValue("t2"),
                StringValue("Constant.type"): StringType()
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addDeclarationStm(MyFormalisms.Utilities.z.body, type_declaration37)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.DeclarationStatement"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Statement.name"): StringValue("type_declaration37")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addIdentifier(MyFormalisms.Utilities.z.body.type_declaration37, PetriNet.InArc, out_t)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Identifier"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.type_declaration37"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("out_t"),
                StringValue("Identifier.type"): ClabjectReference(LocationValue("MyFormalisms.PetriNet.InArc"))
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addFunctionCall(MyFormalisms.Utilities.z.body.type_declaration37, funccall_expr38, PetriNet.InArc)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.FunctionCall"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.type_declaration37"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("funccall_expr38"),
                StringValue("FunctionCall.function_name"): StringValue("PetriNet.InArc")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addArgument(MyFormalisms.Utilities.z.body.type_declaration37.funccall_expr38, argument39, from_place)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Argument"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.type_declaration37.funccall_expr38"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Argument.key"): StringValue("from_place"),
                StringValue("Argument.name"): StringValue("argument39")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addNavigation(MyFormalisms.Utilities.z.body.type_declaration37.funccall_expr38.argument39, navigation40, pnInstance.newplace)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Navigation"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.type_declaration37.funccall_expr38.argument39"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("navigation40"),
                StringValue("Navigation.path"): LocationValue("pnInstance.newplace")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addArgument(MyFormalisms.Utilities.z.body.type_declaration37.funccall_expr38, argument41, to_transition)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Argument"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.type_declaration37.funccall_expr38"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Argument.key"): StringValue("to_transition"),
                StringValue("Argument.name"): StringValue("argument41")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addNavigation(MyFormalisms.Utilities.z.body.type_declaration37.funccall_expr38.argument41, navigation42, pnInstance.t2)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Navigation"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.type_declaration37.funccall_expr38.argument41"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("navigation42"),
                StringValue("Navigation.path"): LocationValue("pnInstance.t2")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addExpressionStatement(MyFormalisms.Utilities.z.body, expression43)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.ExpressionStatement"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Statement.name"): StringValue("expression43")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addFunctionCall(MyFormalisms.Utilities.z.body.expression43, funccall_expr44, mvk.create)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.FunctionCall"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.expression43"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("funccall_expr44"),
                StringValue("FunctionCall.function_name"): StringValue("mvk.create")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addArgument(MyFormalisms.Utilities.z.body.expression43.funccall_expr44, argument45, )')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Argument"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.expression43.funccall_expr44"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Argument.key"): StringValue(""),
                StringValue("Argument.name"): StringValue("argument45")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addNavigation(MyFormalisms.Utilities.z.body.expression43.funccall_expr44.argument45, navigation46, out_t)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Navigation"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.expression43.funccall_expr44.argument45"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("navigation46"),
                StringValue("Navigation.path"): LocationValue("out_t")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addArgument(MyFormalisms.Utilities.z.body.expression43.funccall_expr44, argument47, )')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Argument"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.expression43.funccall_expr44"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Argument.key"): StringValue(""),
                StringValue("Argument.name"): StringValue("argument47")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addNavigation(MyFormalisms.Utilities.z.body.expression43.funccall_expr44.argument47, navigation48, pnInstance)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Navigation"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.expression43.funccall_expr44.argument47"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("navigation48"),
                StringValue("Navigation.path"): LocationValue("pnInstance")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addArgument(MyFormalisms.Utilities.z.body.expression43.funccall_expr44, argument49, )')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Argument"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.expression43.funccall_expr44"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Argument.key"): StringValue(""),
                StringValue("Argument.name"): StringValue("argument49")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addConstant(MyFormalisms.Utilities.z.body.expression43.funccall_expr44.argument49, atomvalue50, out_t, StringType)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Constant"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.expression43.funccall_expr44.argument49"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("atomvalue50"),
                StringValue("Constant.value"): StringValue("out_t"),
                StringValue("Constant.type"): StringType()
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addReturnStm(MyFormalisms.Utilities.z.body, return_stm51)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.ReturnStatement"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Statement.name"): StringValue("return_stm51")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addFunctionCall(MyFormalisms.Utilities.z.body.return_stm51, funccall_expr52, joinTransitions)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.FunctionCall"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.return_stm51"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("funccall_expr52"),
                StringValue("FunctionCall.function_name"): StringValue("joinTransitions")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addArgument(MyFormalisms.Utilities.z.body.return_stm51.funccall_expr52, argument53, )')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Argument"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.return_stm51.funccall_expr52"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Argument.key"): StringValue(""),
                StringValue("Argument.name"): StringValue("argument53")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addNavigation(MyFormalisms.Utilities.z.body.return_stm51.funccall_expr52.argument53, navigation54, pnInstance.t1)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Navigation"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.return_stm51.funccall_expr52.argument53"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("navigation54"),
                StringValue("Navigation.path"): LocationValue("pnInstance.t1")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addArgument(MyFormalisms.Utilities.z.body.return_stm51.funccall_expr52, argument55, )')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Argument"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.return_stm51.funccall_expr52"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Argument.key"): StringValue(""),
                StringValue("Argument.name"): StringValue("argument55")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addNavigation(MyFormalisms.Utilities.z.body.return_stm51.funccall_expr52.argument55, navigation56, pnInstance.t2)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Navigation"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.z.body.return_stm51.funccall_expr52.argument55"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("navigation56"),
                StringValue("Navigation.path"): LocationValue("pnInstance.t2")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addFunction(MyFormalisms.Utilities, joinTransitions, PetriNet.Place)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Function"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Function.type"): ClabjectReference(LocationValue("MyFormalisms.PetriNet.Place")),
                StringValue("Function.name"): StringValue("joinTransitions")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addFunctionParameter(MyFormalisms.Utilities, joinTransitions, f1, PetriNet.Transition, in)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Parameter"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Parameter.parameter_type"): StringValue("in"),
                StringValue("Parameter.name"): StringValue("f1"),
                StringValue("Parameter.type"): ClabjectReference(LocationValue("MyFormalisms.PetriNet.Transition"))
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addFunctionParameter(MyFormalisms.Utilities, joinTransitions, f2, PetriNet.Transition, in)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Parameter"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Parameter.parameter_type"): StringValue("in"),
                StringValue("Parameter.name"): StringValue("f2"),
                StringValue("Parameter.type"): ClabjectReference(LocationValue("MyFormalisms.PetriNet.Transition"))
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addDeclarationStm(MyFormalisms.Utilities.joinTransitions.body, type_declaration58)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.DeclarationStatement"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Statement.name"): StringValue("type_declaration58")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addIdentifier(MyFormalisms.Utilities.joinTransitions.body.type_declaration58, PetriNet.Place, p)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Identifier"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body.type_declaration58"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("p"),
                StringValue("Identifier.type"): ClabjectReference(LocationValue("MyFormalisms.PetriNet.Place"))
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addExpressionStatement(MyFormalisms.Utilities.joinTransitions.body, expression59)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.ExpressionStatement"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Statement.name"): StringValue("expression59")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addFunctionCall(MyFormalisms.Utilities.joinTransitions.body.expression59, funccall_expr60, mvk.create)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.FunctionCall"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body.expression59"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("funccall_expr60"),
                StringValue("FunctionCall.function_name"): StringValue("mvk.create")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addArgument(MyFormalisms.Utilities.joinTransitions.body.expression59.funccall_expr60, argument61, )')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Argument"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body.expression59.funccall_expr60"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Argument.key"): StringValue(""),
                StringValue("Argument.name"): StringValue("argument61")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addNavigation(MyFormalisms.Utilities.joinTransitions.body.expression59.funccall_expr60.argument61, navigation62, p)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Navigation"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body.expression59.funccall_expr60.argument61"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("navigation62"),
                StringValue("Navigation.path"): LocationValue("p")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addArgument(MyFormalisms.Utilities.joinTransitions.body.expression59.funccall_expr60, argument63, )')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Argument"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body.expression59.funccall_expr60"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Argument.key"): StringValue(""),
                StringValue("Argument.name"): StringValue("argument63")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addNavigation(MyFormalisms.Utilities.joinTransitions.body.expression59.funccall_expr60.argument63, navigation64, pnInstance)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Navigation"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body.expression59.funccall_expr60.argument63"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("navigation64"),
                StringValue("Navigation.path"): LocationValue("pnInstance")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addArgument(MyFormalisms.Utilities.joinTransitions.body.expression59.funccall_expr60, argument65, )')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Argument"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body.expression59.funccall_expr60"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Argument.key"): StringValue(""),
                StringValue("Argument.name"): StringValue("argument65")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addConstant(MyFormalisms.Utilities.joinTransitions.body.expression59.funccall_expr60.argument65, atomvalue66, rep, StringType)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Constant"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body.expression59.funccall_expr60.argument65"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("atomvalue66"),
                StringValue("Constant.value"): StringValue("rep"),
                StringValue("Constant.type"): StringType()
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addDeclarationStm(MyFormalisms.Utilities.joinTransitions.body, type_declaration67)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.DeclarationStatement"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Statement.name"): StringValue("type_declaration67")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addIdentifier(MyFormalisms.Utilities.joinTransitions.body.type_declaration67, PetriNet.OutArc, a)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Identifier"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body.type_declaration67"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("a"),
                StringValue("Identifier.type"): ClabjectReference(LocationValue("MyFormalisms.PetriNet.OutArc"))
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addFunctionCall(MyFormalisms.Utilities.joinTransitions.body.type_declaration67, funccall_expr68, PetriNet.OutArc)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.FunctionCall"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body.type_declaration67"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("funccall_expr68"),
                StringValue("FunctionCall.function_name"): StringValue("PetriNet.OutArc")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addArgument(MyFormalisms.Utilities.joinTransitions.body.type_declaration67.funccall_expr68, argument69, from_transition)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Argument"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body.type_declaration67.funccall_expr68"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Argument.key"): StringValue("from_transition"),
                StringValue("Argument.name"): StringValue("argument69")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addNavigation(MyFormalisms.Utilities.joinTransitions.body.type_declaration67.funccall_expr68.argument69, navigation70, f1)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Navigation"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body.type_declaration67.funccall_expr68.argument69"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("navigation70"),
                StringValue("Navigation.path"): LocationValue("f1")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addArgument(MyFormalisms.Utilities.joinTransitions.body.type_declaration67.funccall_expr68, argument71, to_place)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Argument"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body.type_declaration67.funccall_expr68"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Argument.key"): StringValue("to_place"),
                StringValue("Argument.name"): StringValue("argument71")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addNavigation(MyFormalisms.Utilities.joinTransitions.body.type_declaration67.funccall_expr68.argument71, navigation72, rep)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Navigation"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body.type_declaration67.funccall_expr68.argument71"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("navigation72"),
                StringValue("Navigation.path"): LocationValue("rep")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addExpressionStatement(MyFormalisms.Utilities.joinTransitions.body, expression73)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.ExpressionStatement"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Statement.name"): StringValue("expression73")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addFunctionCall(MyFormalisms.Utilities.joinTransitions.body.expression73, funccall_expr74, mvk.create)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.FunctionCall"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body.expression73"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("funccall_expr74"),
                StringValue("FunctionCall.function_name"): StringValue("mvk.create")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addArgument(MyFormalisms.Utilities.joinTransitions.body.expression73.funccall_expr74, argument75, )')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Argument"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body.expression73.funccall_expr74"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Argument.key"): StringValue(""),
                StringValue("Argument.name"): StringValue("argument75")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addNavigation(MyFormalisms.Utilities.joinTransitions.body.expression73.funccall_expr74.argument75, navigation76, a)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Navigation"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body.expression73.funccall_expr74.argument75"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("navigation76"),
                StringValue("Navigation.path"): LocationValue("a")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addArgument(MyFormalisms.Utilities.joinTransitions.body.expression73.funccall_expr74, argument77, )')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Argument"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body.expression73.funccall_expr74"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Argument.key"): StringValue(""),
                StringValue("Argument.name"): StringValue("argument77")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addNavigation(MyFormalisms.Utilities.joinTransitions.body.expression73.funccall_expr74.argument77, navigation78, pnInstance)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Navigation"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body.expression73.funccall_expr74.argument77"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("navigation78"),
                StringValue("Navigation.path"): LocationValue("pnInstance")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addArgument(MyFormalisms.Utilities.joinTransitions.body.expression73.funccall_expr74, argument79, )')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Argument"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body.expression73.funccall_expr74"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Argument.key"): StringValue(""),
                StringValue("Argument.name"): StringValue("argument79")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addConstant(MyFormalisms.Utilities.joinTransitions.body.expression73.funccall_expr74.argument79, atomvalue80, in_rep1, StringType)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Constant"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body.expression73.funccall_expr74.argument79"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("atomvalue80"),
                StringValue("Constant.value"): StringValue("in_rep1"),
                StringValue("Constant.type"): StringType()
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addDeclarationStm(MyFormalisms.Utilities.joinTransitions.body, type_declaration81)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.DeclarationStatement"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Statement.name"): StringValue("type_declaration81")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addIdentifier(MyFormalisms.Utilities.joinTransitions.body.type_declaration81, PetriNet.OutArc, b)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Identifier"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body.type_declaration81"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("b"),
                StringValue("Identifier.type"): ClabjectReference(LocationValue("MyFormalisms.PetriNet.OutArc"))
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addFunctionCall(MyFormalisms.Utilities.joinTransitions.body.type_declaration81, funccall_expr82, PetriNet.OutArc)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.FunctionCall"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body.type_declaration81"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("funccall_expr82"),
                StringValue("FunctionCall.function_name"): StringValue("PetriNet.OutArc")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addArgument(MyFormalisms.Utilities.joinTransitions.body.type_declaration81.funccall_expr82, argument83, from_transition)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Argument"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body.type_declaration81.funccall_expr82"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Argument.key"): StringValue("from_transition"),
                StringValue("Argument.name"): StringValue("argument83")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addNavigation(MyFormalisms.Utilities.joinTransitions.body.type_declaration81.funccall_expr82.argument83, navigation84, f2)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Navigation"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body.type_declaration81.funccall_expr82.argument83"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("navigation84"),
                StringValue("Navigation.path"): LocationValue("f2")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addArgument(MyFormalisms.Utilities.joinTransitions.body.type_declaration81.funccall_expr82, argument85, to_place)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Argument"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body.type_declaration81.funccall_expr82"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Argument.key"): StringValue("to_place"),
                StringValue("Argument.name"): StringValue("argument85")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addNavigation(MyFormalisms.Utilities.joinTransitions.body.type_declaration81.funccall_expr82.argument85, navigation86, rep)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Navigation"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body.type_declaration81.funccall_expr82.argument85"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("navigation86"),
                StringValue("Navigation.path"): LocationValue("rep")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addExpressionStatement(MyFormalisms.Utilities.joinTransitions.body, expression87)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.ExpressionStatement"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Statement.name"): StringValue("expression87")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addFunctionCall(MyFormalisms.Utilities.joinTransitions.body.expression87, funccall_expr88, mvk.create)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.FunctionCall"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body.expression87"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("funccall_expr88"),
                StringValue("FunctionCall.function_name"): StringValue("mvk.create")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addArgument(MyFormalisms.Utilities.joinTransitions.body.expression87.funccall_expr88, argument89, )')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Argument"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body.expression87.funccall_expr88"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Argument.key"): StringValue(""),
                StringValue("Argument.name"): StringValue("argument89")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addNavigation(MyFormalisms.Utilities.joinTransitions.body.expression87.funccall_expr88.argument89, navigation90, b)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Navigation"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body.expression87.funccall_expr88.argument89"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("navigation90"),
                StringValue("Navigation.path"): LocationValue("b")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addArgument(MyFormalisms.Utilities.joinTransitions.body.expression87.funccall_expr88, argument91, )')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Argument"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body.expression87.funccall_expr88"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Argument.key"): StringValue(""),
                StringValue("Argument.name"): StringValue("argument91")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addNavigation(MyFormalisms.Utilities.joinTransitions.body.expression87.funccall_expr88.argument91, navigation92, pnInstance)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Navigation"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body.expression87.funccall_expr88.argument91"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("navigation92"),
                StringValue("Navigation.path"): LocationValue("pnInstance")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addArgument(MyFormalisms.Utilities.joinTransitions.body.expression87.funccall_expr88, argument93, )')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Argument"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body.expression87.funccall_expr88"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Argument.key"): StringValue(""),
                StringValue("Argument.name"): StringValue("argument93")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addConstant(MyFormalisms.Utilities.joinTransitions.body.expression87.funccall_expr88.argument93, atomvalue94, in_rep2, StringType)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Constant"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body.expression87.funccall_expr88.argument93"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("atomvalue94"),
                StringValue("Constant.value"): StringValue("in_rep2"),
                StringValue("Constant.type"): StringType()
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addReturnStm(MyFormalisms.Utilities.joinTransitions.body, return_stm95)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.ReturnStatement"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Statement.name"): StringValue("return_stm95")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

        print('addNavigation(MyFormalisms.Utilities.joinTransitions.body.return_stm95, navigation96, p)')
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue("protected.formalisms.ActionLanguage.Navigation"),
            CreateConstants.LOCATION_KEY: LocationValue("MyFormalisms.Utilities.joinTransitions.body.return_stm95"),
            CreateConstants.ATTRS_KEY: MappingValue({
                StringValue("Expression.name"): StringValue("navigation96"),
                StringValue("Navigation.path"): LocationValue("p")
            })
        }))
        if(cl.is_success()):
            print('\t: cl.is_success() = True')
        else:
            print('\t: cl.is_success() = False')
            print(cl.get_status_message())

if __name__ == "__main__":
    Gen().instance()
