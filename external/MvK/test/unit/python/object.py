'''
Created on 18-feb.-2014

@author: Simon
'''
import time
import unittest

from mvk.impl.python.constants import CreateConstants
from mvk.impl.python.datatype import IntegerType, TupleType, TypeFactory, \
    StringType, BooleanType, FloatType, TypeType, AnyType
from mvk.impl.python.datavalue import StringValue, BooleanValue, IntegerValue, \
    LocationValue, DataValueFactory, ImmutableMappingValue, SequenceValue, \
    InfiniteValue, FloatValue, MappingValue, AnyValue
from mvk.impl.python.exception import MvKKeyError
from mvk.impl.python.object import Clabject, ClabjectReference, Association, \
    AssociationEnd, Attribute, Model, ModelReference, AssociationReference
from mvk.mvk import MvK


class ObjectTestCase(unittest.TestCase):
    def __init__(self, methodName='runTest'):
        unittest.TestCase.__init__(self, methodName=methodName)
        self.mvk = MvK()

    def setUp(self):
        unittest.TestCase.setUp(self)
        self.mvk.clear()

        ''' create a type model for Petrinets '''
        self.pntm = Model(name=StringValue("Petrinet"),
                          potency=IntegerValue(1),
                          l_type=ModelReference(path=LocationValue('protected.formalisms.SimpleClassDiagrams')))
        self.place = Clabject(name=StringValue("Place"),
                              l_type=ClabjectReference(path=LocationValue("protected.formalisms.SimpleClassDiagrams.Class")),
                              abstract=BooleanValue(False),
                              potency=IntegerValue(1))
        self.place.add_attribute(Attribute(name=StringValue("tokens"),
                                           the_type=IntegerType(),
                                           l_type=ClabjectReference(path=LocationValue("protected.formalisms.SimpleClassDiagrams.Attribute")),
                                           lower=IntegerValue(1),
                                           upper=IntegerValue(1),
                                           potency=IntegerValue(1),
                                           default=IntegerValue(0)))
        self.transition = Clabject(name=StringValue("Transition"),
                                   l_type=ClabjectReference(path=LocationValue("protected.formalisms.SimpleClassDiagrams.Class")),
                                   abstract=BooleanValue(False),
                                   potency=IntegerValue(1))
        self.p2t = Association(name=StringValue("P2T"),
                               l_type=AssociationReference(path=LocationValue("protected.formalisms.SimpleClassDiagrams.Association")),
                               abstract=BooleanValue(False),
                               potency=IntegerValue(1),
                               from_multiplicity=AssociationEnd(port_name=StringValue('from_place'),
                                                                node=self.place),
                               to_multiplicity=AssociationEnd(port_name=StringValue('to_transition'),
                                                              node=self.transition))
        self.t2p = Association(name=StringValue("T2P"),
                               l_type=AssociationReference(path=LocationValue("protected.formalisms.SimpleClassDiagrams.Association")),
                               abstract=BooleanValue(False),
                               potency=IntegerValue(1),
                               from_multiplicity=AssociationEnd(port_name=StringValue('from_transition'),
                                                                node=self.transition),
                               to_multiplicity=AssociationEnd(port_name=StringValue('to_place'),
                                                              node=self.place))
        self.pntm.add_elements([self.place, self.transition, self.p2t, self.t2p])

    def test_TM_instance(self):
        ''' create a Petrinet model '''
        pnm = Model(name=StringValue("aPetrinet"),
                    potency=IntegerValue(0),
                    l_type=ModelReference(path=LocationValue('Petrinets')))
        place = self.pntm.get_element(StringValue("Place"))
        ''' assert we got the right Place class '''
        self.assertEqual(place, self.place)
        p1 = Clabject(name=StringValue("p1"),
                      l_type=place,
                      potency=IntegerValue(0))
        p1.add_attribute(Attribute(name=StringValue('tokens'),
                                   value=IntegerValue(10),
                                   l_type=place.get_attribute(StringValue('tokens')),
                                   potency=IntegerValue(0)))
        self.assertEqual(p1.typed_by(), place)
        self.assertTrue(place.is_type_of(p1))
        p2 = Clabject(name=StringValue("p2"),
                      l_type=place,
                      potency=IntegerValue(0))
        p2.add_attribute(Attribute(name=StringValue('tokens'),
                                   value=IntegerValue(5),
                                   l_type=place.get_attribute(StringValue('tokens')),
                                   potency=IntegerValue(0)))
        self.assertEqual(p2.typed_by(), place)
        self.assertTrue(place.is_type_of(p2))
        transition = self.pntm.get_element(StringValue("Transition"))
        self.assertEqual(transition, self.transition)
        t1 = Clabject(name=StringValue("t1"),
                      l_type=transition,
                      potency=IntegerValue(0))
        self.assertEqual(t1.typed_by(), transition)
        self.assertTrue(transition.is_type_of(t1))
        p2t = self.pntm.get_element(StringValue("P2T"))
        self.assertEqual(p2t, self.p2t)
        p1_to_t1 = Association(name=StringValue("p1_to_t1"),
                               l_type=p2t,
                               potency=IntegerValue(0),
                               from_multiplicity=AssociationEnd(port_name=StringValue('from_place'),
                                                                node=p1),
                               to_multiplicity=AssociationEnd(port_name=StringValue('to_transition'),
                                                              node=t1))
        self.assertEqual(p1_to_t1.typed_by(), p2t)
        self.assertTrue(p2t.is_type_of(p1_to_t1))
        t2p = self.pntm.get_element(StringValue("T2P"))
        self.assertEqual(t2p, self.t2p)
        t1_to_p2 = Association(name=StringValue("t1_to_p2"),
                               l_type=t2p,
                               potency=IntegerValue(0),
                               from_multiplicity=AssociationEnd(port_name=StringValue('from_transition'),
                                                                node=t1),
                               to_multiplicity=AssociationEnd(port_name=StringValue('to_place'),
                                                              node=p2))
        self.assertEqual(t1_to_p2.typed_by(), t2p)
        self.assertTrue(t2p.is_type_of(t1_to_p2))
        pnm.add_elements([p1, p2, p1_to_t1, t1_to_p2])

    def assert_lists_eq_items(self, l1, l2):
        self.assertEqual(l1.len(), l2.len())
        it = l1.__iter__()
        while it.has_next():
            next_it = it.next()
            self.assertTrue(next_it in l2)

    def test_subtyping(self):
        tm = Model(name=StringValue("TestSubTyping"),
                   l_type=ModelReference(path=LocationValue('MMCL')),
                   potency=IntegerValue(1))
        el = Clabject(name=StringValue("Element"),
                      l_type=ClabjectReference(path=LocationValue('MMCL.Class')),
                      potency=IntegerValue(1),
                      abstract=BooleanValue(True))
        tm.add_element(el)
        self.assertEqual(el.get_parent(), tm)
        self.assertEqual(tm.get_element(StringValue("Element")), el)
        int_attr = Attribute(name=StringValue("an_int"),
                             l_type=ClabjectReference(path=LocationValue("MMCL.Attribute")),
                             potency=IntegerValue(1),
                             the_type=IntegerType(),
                             default=IntegerValue(0))
        el.add_attribute(int_attr)
        str_attr = Attribute(name=StringValue("a_str"),
                             l_type=ClabjectReference(path=LocationValue("MMCL.Attribute")),
                             potency=IntegerValue(1),
                             the_type=StringType(),
                             default=StringValue('test'))
        el.add_attribute(str_attr)
        location_el = Clabject(name=StringValue("LocationElement"),
                               l_type=ClabjectReference(path=LocationValue("MMCL.Class")),
                               potency=IntegerValue(1),
                               abstract=BooleanValue(True))
        tm.add_element(location_el)
        location_el.add_super_class(el)
        loc_attr = Attribute(name=StringValue("location"),
                             l_type=ClabjectReference(path=LocationValue("MMCL.Attribute")),
                             potency=IntegerValue(1),
                             the_type=TypeFactory.get_type("TupleType(IntegerType, IntegerType)"),
                             default=DataValueFactory.create_instance((0, 0)))
        location_el.add_attribute(loc_attr)
        named_el = Clabject(name=StringValue("NamedElement"),
                            l_type=ClabjectReference(path=LocationValue("MMCL.Class")),
                            potency=IntegerValue(1),
                            abstract=BooleanValue(True))
        tm.add_element(named_el)
        named_el.add_super_class(el)
        name_attr = Attribute(name=StringValue("name"),
                              l_type=ClabjectReference(path=LocationValue("MMCL.Attribute")),
                              potency=IntegerValue(1),
                              the_type=StringType(),
                              default=StringValue(''))
        named_el.add_attribute(name_attr)
        character = Clabject(name=StringValue("Character"),
                             l_type=ClabjectReference(path=LocationValue("MMCL.Class")),
                             potency=IntegerValue(1),
                             abstract=BooleanValue(False))
        tm.add_element(character)
        character.add_super_class(location_el)
        character.add_super_class(named_el)
        fs_attr = Attribute(name=StringValue("fighting_strength"),
                            l_type=ClabjectReference(path=LocationValue("MMCL.Attribute")),
                            potency=IntegerValue(1),
                            default=IntegerValue(100),
                            the_type=IntegerType())
        character.add_attribute(fs_attr)
        hero = Clabject(name=StringValue("Hero"),
                        l_type=ClabjectReference(path=LocationValue("MMCL.Class")),
                        potency=IntegerValue(1),
                        abstract=BooleanValue(False))
        tm.add_element(hero)
        hero.add_super_class(character)
        points_attr = Attribute(name=StringValue("points"),
                                l_type=ClabjectReference(path=LocationValue("MMCL.Attribute")),
                                potency=IntegerValue(1),
                                default=IntegerValue(0),
                                the_type=IntegerType())
        hero.add_attribute(points_attr)
        door = Clabject(name=StringValue("Door"),
                        l_type=ClabjectReference(path=LocationValue("MMCL.Class")),
                        potency=IntegerValue(1),
                        abstract=BooleanValue(False))
        tm.add_element(door)
        door.add_super_class(named_el)
        is_locked_attr = Attribute(name=StringValue("is_locked"),
                                   l_type=ClabjectReference(path=LocationValue("MMCL.Attribute")),
                                   potency=IntegerValue(1),
                                   default=BooleanValue(0),
                                   the_type=BooleanType())
        door.add_attribute(is_locked_attr)

        self.assertEqual(el.get_attribute(StringValue('an_int')), int_attr)
        self.assertEqual(el.get_attribute(StringValue('a_str')), str_attr)
        self.assertEqual(location_el.get_attribute(StringValue('location')), loc_attr)
        self.assertEqual(named_el.get_attribute(StringValue('name')), name_attr)
        self.assertEqual(character.get_attribute(StringValue('fighting_strength')), fs_attr)
        self.assertEqual(hero.get_attribute(StringValue('points')), points_attr)
        self.assertEqual(door.get_attribute(StringValue('is_locked')), is_locked_attr)

        self.assert_lists_eq_items(el.get_attributes(), SequenceValue(value=[int_attr, str_attr]))
        self.assert_lists_eq_items(location_el.get_attributes(), SequenceValue(value=[loc_attr]))
        self.assert_lists_eq_items(named_el.get_attributes(), SequenceValue(value=[name_attr]))
        self.assert_lists_eq_items(character.get_attributes(), SequenceValue(value=[fs_attr]))
        self.assert_lists_eq_items(hero.get_attributes(), SequenceValue(value=[points_attr]))
        self.assert_lists_eq_items(door.get_attributes(), SequenceValue(value=[is_locked_attr]))

        self.assert_lists_eq_items(el.get_all_attributes(), SequenceValue(value=[int_attr, str_attr]))
        self.assert_lists_eq_items(location_el.get_all_attributes(), SequenceValue(value=[int_attr, str_attr, loc_attr]))
        self.assert_lists_eq_items(named_el.get_all_attributes(), SequenceValue(value=[int_attr, str_attr, name_attr]))
        self.assert_lists_eq_items(character.get_all_attributes(), SequenceValue(value=[int_attr, str_attr, loc_attr, name_attr, fs_attr]))
        self.assert_lists_eq_items(hero.get_all_attributes(), SequenceValue(value=[int_attr, str_attr, loc_attr, name_attr, fs_attr, points_attr]))
        self.assert_lists_eq_items(door.get_all_attributes(), SequenceValue(value=[int_attr, str_attr, name_attr, is_locked_attr]))
        self.assertRaises(MvKKeyError, el.get_attribute, StringValue('location'))

        superclasses = {StringValue("Element"): ([], []),
                        StringValue("LocationElement"): ([el], [el]),
                        StringValue("NamedElement"): ([el], [el]),
                        StringValue("Character"): ([location_el, named_el],
                                                   [el, location_el, named_el]),
                        StringValue("Hero"): ([character],
                                              [el, location_el, named_el, character]),
                        StringValue("Door"): ([named_el],
                                              [el, named_el])}
        for n, e in superclasses.iteritems():
            read_el = tm.get_element(n)
            result = (read_el.get_super_classes(),
                      read_el.get_all_super_classes())
            for i in range(1):
                self.assert_lists_eq_items(result[i], SequenceValue(value=e[i]))

        subclasses = {StringValue("Element"): ([location_el, named_el],
                                               [location_el, named_el, character, hero, door]),
                      StringValue("LocationElement"): ([character],
                                                       [character, hero]),
                      StringValue("NamedElement"): ([character, door],
                                                    [character, hero, door]),
                      StringValue("Character"): ([hero], [hero]),
                      StringValue("Hero"): ([], []),
                      StringValue("Door"): ([], [])}

        for n, e in subclasses.iteritems():
            read_el = tm.get_element(n)
            result = (read_el.get_specialise_classes(),
                      read_el.get_all_specialise_classes())
            for i in range(1):
                self.assert_lists_eq_items(result[i], SequenceValue(value=e[i]))

    def test_associations(self):
        tm = Model(name=StringValue("TestAssociations"),
                   l_type=ModelReference(path=LocationValue('MMCL')),
                   potency=IntegerValue(1))
        living_being = Clabject(name=StringValue("LivingBeing"),
                                l_type=ClabjectReference(path=LocationValue('MMCL.Class')),
                                potency=IntegerValue(1),
                                abstract=BooleanValue(True))
        tm.add_element(living_being)
        food = Clabject(name=StringValue("Food"),
                        l_type=ClabjectReference(path=LocationValue("MMCL.Class")),
                        potency=IntegerValue(1),
                        abstract=BooleanValue(False))
        tm.add_element(food)
        person = Clabject(name=StringValue("Person"),
                          l_type=ClabjectReference(path=LocationValue("MMCL.Class")),
                          potency=IntegerValue(1),
                          abstract=BooleanValue(False))
        tm.add_element(person)
        person.add_super_class(living_being)
        dog = Clabject(name=StringValue("Dog"),
                       l_type=ClabjectReference(path=LocationValue("MMCL.Class")),
                       potency=IntegerValue(1),
                       abstract=BooleanValue(False))
        tm.add_element(dog)
        dog.add_super_class(living_being)
        man = Clabject(name=StringValue("Man"),
                       l_type=ClabjectReference(path=LocationValue("MMCL.Class")),
                       potency=IntegerValue(1),
                       abstract=BooleanValue(False))
        tm.add_element(man)
        man.add_super_class(person)
        man.add_super_class(dog)
        eats = Association(name=StringValue("eats"),
                           l_type=AssociationReference(path=LocationValue("MMCL.Association")),
                           potency=IntegerValue(1),
                           abstract=BooleanValue(False),
                           from_multiplicity=AssociationEnd(node=living_being,
                                                            port_name=StringValue('from_lb'),
                                                            lower=IntegerValue(0),
                                                            upper=InfiniteValue('+'),
                                                            ordered=BooleanValue(False)),
                           to_multiplicity=AssociationEnd(node=food,
                                                          port_name=StringValue('to_food'),
                                                          lower=IntegerValue(1),
                                                          upper=InfiniteValue('+'),
                                                          ordered=BooleanValue(False)))
        tm.add_element(eats)
        barfs = Association(name=StringValue("barfs"),
                            l_type=AssociationReference(path=LocationValue("MMCL.Association")),
                            potency=IntegerValue(1),
                            abstract=BooleanValue(False),
                            from_multiplicity=AssociationEnd(node=dog,
                                                             port_name=StringValue('from_dog'),
                                                             lower=IntegerValue(0),
                                                             upper=InfiniteValue('+'),
                                                             ordered=BooleanValue(False)),
                            to_multiplicity=AssociationEnd(node=food,
                                                           port_name=StringValue('to_food'),
                                                           lower=IntegerValue(0),
                                                           upper=InfiniteValue('+'),
                                                           ordered=BooleanValue(False)))
        tm.add_element(barfs)
        has_dog = Association(name=StringValue("hasDog"),
                              l_type=AssociationReference(path=LocationValue("MMCL.Association")),
                              potency=IntegerValue(1),
                              abstract=BooleanValue(False),
                              from_multiplicity=AssociationEnd(node=person,
                                                               port_name=StringValue('from_person'),
                                                               lower=IntegerValue(1),
                                                               upper=IntegerValue(1),
                                                               ordered=BooleanValue(False)),
                              to_multiplicity=AssociationEnd(node=dog,
                                                             port_name=StringValue('to_dog'),
                                                             lower=IntegerValue(0),
                                                             upper=InfiniteValue('+'),
                                                             ordered=BooleanValue(False)))
        tm.add_element(has_dog)
        likes = Association(name=StringValue("likes"),
                            l_type=AssociationReference(path=LocationValue("MMCL.Association")),
                            potency=IntegerValue(1),
                            abstract=BooleanValue(False),
                            from_multiplicity=AssociationEnd(node=man,
                                                             port_name=StringValue('from_man'),
                                                             lower=IntegerValue(0),
                                                             upper=InfiniteValue('+'),
                                                             ordered=BooleanValue(False)),
                            to_multiplicity=AssociationEnd(node=person,
                                                           port_name=StringValue('to_person'),
                                                           lower=IntegerValue(0),
                                                           upper=InfiniteValue('+'),
                                                           ordered=BooleanValue(False)))
        tm.add_element(likes)
        married_to = Association(name=StringValue("marriedTo"),
                                 l_type=AssociationReference(path=LocationValue("MMCL.Association")),
                                 potency=IntegerValue(1),
                                 abstract=BooleanValue(False),
                                 from_multiplicity=AssociationEnd(node=man,
                                                                  port_name=StringValue('from_man'),
                                                                  lower=IntegerValue(0),
                                                                  upper=IntegerValue(1),
                                                                  ordered=BooleanValue(False)),
                                 to_multiplicity=AssociationEnd(node=person,
                                                                port_name=StringValue('to_person'),
                                                                lower=IntegerValue(0),
                                                                upper=IntegerValue(1),
                                                                ordered=BooleanValue(False)))
        tm.add_element(married_to)
        friend = Association(name=StringValue("friend"),
                             l_type=AssociationReference(path=LocationValue("MMCL.Association")),
                             potency=IntegerValue(1),
                             abstract=BooleanValue(False),
                             from_multiplicity=AssociationEnd(node=man,
                                                              port_name=StringValue('from_man'),
                                                              lower=IntegerValue(0),
                                                              upper=InfiniteValue('+'),
                                                              ordered=BooleanValue(False)),
                             to_multiplicity=AssociationEnd(node=man,
                                                            port_name=StringValue('to_man'),
                                                            lower=IntegerValue(0),
                                                            upper=InfiniteValue('+'),
                                                            ordered=BooleanValue(False)))
        tm.add_element(friend)

        self.assert_lists_eq_items(living_being.get_out_associations(), SequenceValue(value=[eats]))
        self.assert_lists_eq_items(living_being.get_in_associations(), SequenceValue(value=[]))
        self.assert_lists_eq_items(living_being.get_outgoing_elements(), SequenceValue(value=[food]))
        self.assert_lists_eq_items(living_being.get_incoming_elements(), SequenceValue(value=[]))
        self.assert_lists_eq_items(living_being.get_neighbors(), SequenceValue(value=[food]))
        self.assert_lists_eq_items(living_being.get_all_out_associations(), SequenceValue(value=[eats]))
        self.assert_lists_eq_items(living_being.get_all_in_associations(), SequenceValue(value=[]))

        self.assert_lists_eq_items(food.get_out_associations(), SequenceValue(value=[]))
        self.assert_lists_eq_items(food.get_in_associations(), SequenceValue(value=[eats, barfs]))
        self.assert_lists_eq_items(food.get_outgoing_elements(), SequenceValue(value=[]))
        self.assert_lists_eq_items(food.get_incoming_elements(), SequenceValue(value=[living_being, dog]))
        self.assert_lists_eq_items(food.get_neighbors(), SequenceValue(value=[living_being, dog]))
        self.assert_lists_eq_items(food.get_all_out_associations(), SequenceValue(value=[]))
        self.assert_lists_eq_items(food.get_all_in_associations(), SequenceValue(value=[eats, barfs]))

        self.assert_lists_eq_items(dog.get_out_associations(), SequenceValue(value=[barfs]))
        self.assert_lists_eq_items(dog.get_in_associations(), SequenceValue(value=[has_dog]))
        self.assert_lists_eq_items(dog.get_outgoing_elements(), SequenceValue(value=[food]))
        self.assert_lists_eq_items(dog.get_incoming_elements(), SequenceValue(value=[person]))
        self.assert_lists_eq_items(dog.get_neighbors(), SequenceValue(value=[food, person]))
        self.assert_lists_eq_items(dog.get_all_out_associations(), SequenceValue(value=[barfs, eats]))
        self.assert_lists_eq_items(dog.get_all_in_associations(), SequenceValue(value=[has_dog]))

        self.assert_lists_eq_items(person.get_out_associations(), SequenceValue(value=[has_dog]))
        self.assert_lists_eq_items(person.get_in_associations(), SequenceValue(value=[likes, married_to]))
        self.assert_lists_eq_items(person.get_outgoing_elements(), SequenceValue(value=[dog]))
        self.assert_lists_eq_items(person.get_incoming_elements(), SequenceValue(value=[man]))
        self.assert_lists_eq_items(person.get_neighbors(), SequenceValue(value=[dog, man]))
        self.assert_lists_eq_items(person.get_all_out_associations(), SequenceValue(value=[eats, has_dog]))
        self.assert_lists_eq_items(person.get_all_in_associations(), SequenceValue(value=[likes, married_to]))

        self.assert_lists_eq_items(man.get_out_associations(), SequenceValue(value=[likes, married_to, friend]))
        self.assert_lists_eq_items(man.get_in_associations(), SequenceValue(value=[friend]))
        self.assert_lists_eq_items(man.get_outgoing_elements(), SequenceValue(value=[person, man]))
        self.assert_lists_eq_items(man.get_incoming_elements(), SequenceValue(value=[man]))
        self.assert_lists_eq_items(man.get_neighbors(), SequenceValue(value=[person, man]))
        self.assert_lists_eq_items(man.get_all_out_associations(), SequenceValue(value=[eats, barfs, has_dog, likes, married_to, friend]))
        self.assert_lists_eq_items(man.get_all_in_associations(), SequenceValue(value=[has_dog, married_to, likes, friend]))

        m = Model(name=StringValue("TestAssociationsInstance"),
                  l_type=tm,
                  potency=IntegerValue(0))
        tom = Clabject(name=StringValue("Tom"),
                       l_type=man,
                       potency=IntegerValue(0))
        mary = Clabject(name=StringValue("Mary"),
                        l_type=person,
                        potency=IntegerValue(0))
        toms_ex = Clabject(name=StringValue("TomsEx"),
                           l_type=person,
                           potency=IntegerValue(0))
        snoopy = Clabject(name=StringValue("Snoopy"),
                          l_type=dog,
                          potency=IntegerValue(0))
        broccoli = Clabject(name=StringValue("Broccoli"),
                            l_type=food,
                            potency=IntegerValue(0))
        hamburger = Clabject(name=StringValue("Hamburger"),
                             l_type=food,
                             potency=IntegerValue(0))
        dogfood = Clabject(name=StringValue("DogFood"),
                           l_type=food,
                           potency=IntegerValue(0))
        m.add_elements([tom, mary, toms_ex, snoopy, broccoli, hamburger, dogfood])
        tom_likes_mary = Association(name=StringValue("tom_likes_mary"),
                                     l_type=likes,
                                     potency=IntegerValue(0),
                                     from_multiplicity=AssociationEnd(port_name=StringValue('from_man'),
                                                                      node=tom),
                                     to_multiplicity=AssociationEnd(port_name=StringValue('to_person'),
                                                                    node=mary))
        tom_likes_his_ex = Association(name=StringValue("tom_likes_his_ex"),
                                       l_type=likes,
                                       potency=IntegerValue(0),
                                       from_multiplicity=AssociationEnd(port_name=StringValue('from_man'),
                                                                        node=tom),
                                       to_multiplicity=AssociationEnd(port_name=StringValue('to_person'),
                                                                      node=toms_ex))
        tom_married_to_mary = Association(name=StringValue("tom_married_to_mary"),
                                          l_type=married_to,
                                          potency=IntegerValue(0),
                                          from_multiplicity=AssociationEnd(port_name=StringValue('from_man'),
                                                                           node=tom),
                                          to_multiplicity=AssociationEnd(port_name=StringValue('to_person'),
                                                                         node=mary))
        tom_friend_of_tom = Association(name=StringValue("tom_friend_of_tom"),
                                        l_type=friend,
                                        potency=IntegerValue(0),
                                        from_multiplicity=AssociationEnd(port_name=StringValue('from_man'),
                                                                         node=tom),
                                        to_multiplicity=AssociationEnd(port_name=StringValue('to_man'),
                                                                       node=tom))
        mary_eats_broccoli = Association(name=StringValue("mary_eats_broccoli"),
                                         l_type=eats,
                                         potency=IntegerValue(0),
                                         from_multiplicity=AssociationEnd(port_name=StringValue('from_lb'),
                                                                          node=mary),
                                         to_multiplicity=AssociationEnd(port_name=StringValue('to_food'),
                                                                        node=broccoli))
        tom_barfs_broccoli = Association(name=StringValue("tom_barfs_broccoli"),
                                         l_type=barfs,
                                         potency=IntegerValue(0),
                                         from_multiplicity=AssociationEnd(port_name=StringValue('from_dog'),
                                                                          node=tom),
                                         to_multiplicity=AssociationEnd(port_name=StringValue('to_food'),
                                                                        node=broccoli))
        tom_owns_snoopy = Association(name=StringValue("tom_owns_snoopy"),
                                      l_type=has_dog,
                                      potency=IntegerValue(0),
                                      from_multiplicity=AssociationEnd(port_name=StringValue('from_person'),
                                                                       node=tom),
                                      to_multiplicity=AssociationEnd(port_name=StringValue('to_dog'),
                                                                     node=snoopy))
        tom_eats_dogfood = Association(name=StringValue("tom_eats_dogfood"),
                                       l_type=eats,
                                       potency=IntegerValue(0),
                                       from_multiplicity=AssociationEnd(port_name=StringValue('from_lb'),
                                                                        node=tom),
                                       to_multiplicity=AssociationEnd(port_name=StringValue('to_food'),
                                                                      node=dogfood))
        tom_eats_hamburger = Association(name=StringValue("tom_eats_hamburger"),
                                         l_type=eats,
                                         potency=IntegerValue(0),
                                         from_multiplicity=AssociationEnd(port_name=StringValue('from_lb'),
                                                                          node=tom),
                                         to_multiplicity=AssociationEnd(port_name=StringValue('to_food'),
                                                                        node=hamburger))
        snoopy_eats_dogfood = Association(name=StringValue("snoopy_eats_dogfood"),
                                          l_type=eats,
                                          potency=IntegerValue(0),
                                          from_multiplicity=AssociationEnd(port_name=StringValue('from_lb'),
                                                                           node=snoopy),
                                          to_multiplicity=AssociationEnd(port_name=StringValue('to_food'),
                                                                         node=dogfood))
        snoopy_barfs_dogfood = Association(name=StringValue("snoopy_barfs_dogfood"),
                                           l_type=barfs,
                                           potency=IntegerValue(0),
                                           from_multiplicity=AssociationEnd(port_name=StringValue('from_dog'),
                                                                            node=snoopy),
                                           to_multiplicity=AssociationEnd(port_name=StringValue('to_food'),
                                                                          node=dogfood))
        snoopy_barfs_broccoli = Association(name=StringValue("snoopy_barfs_broccoli"),
                                            l_type=barfs,
                                            potency=IntegerValue(0),
                                            from_multiplicity=AssociationEnd(port_name=StringValue('from_dog'),
                                                                             node=snoopy),
                                            to_multiplicity=AssociationEnd(port_name=StringValue('to_food'),
                                                                           node=broccoli))
        m.add_elements([tom_barfs_broccoli, tom_eats_dogfood, tom_eats_hamburger,
                        tom_likes_his_ex, tom_likes_mary, tom_married_to_mary,
                        tom_friend_of_tom, tom_owns_snoopy, mary_eats_broccoli,
                        snoopy_barfs_broccoli, snoopy_barfs_dogfood, snoopy_eats_dogfood])

        self.assert_lists_eq_items(tom.get_out_associations(), SequenceValue(value=[tom_barfs_broccoli,
                                                                                    tom_eats_dogfood,
                                                                                    tom_eats_hamburger,
                                                                                    tom_likes_his_ex,
                                                                                    tom_likes_mary,
                                                                                    tom_married_to_mary,
                                                                                    tom_owns_snoopy,
                                                                                    tom_friend_of_tom]))
        self.assert_lists_eq_items(tom.get_in_associations(), SequenceValue(value=[tom_friend_of_tom]))
        self.assert_lists_eq_items(tom.get_outgoing_elements(), SequenceValue(value=[broccoli,
                                                                                     dogfood,
                                                                                     hamburger,
                                                                                     toms_ex,
                                                                                     mary,
                                                                                     snoopy,
                                                                                     tom]))
        self.assert_lists_eq_items(tom.get_incoming_elements(), SequenceValue(value=[tom]))
        self.assert_lists_eq_items(tom.get_neighbors(), SequenceValue(value=[broccoli,
                                                                             dogfood,
                                                                             hamburger,
                                                                             toms_ex,
                                                                             mary,
                                                                             snoopy,
                                                                             tom]))

        self.assert_lists_eq_items(broccoli.get_out_associations(), SequenceValue(value=[]))
        self.assert_lists_eq_items(broccoli.get_in_associations(), SequenceValue(value=[tom_barfs_broccoli,
                                                                                        snoopy_barfs_broccoli,
                                                                                        mary_eats_broccoli]))
        self.assert_lists_eq_items(broccoli.get_outgoing_elements(), SequenceValue(value=[]))
        self.assert_lists_eq_items(broccoli.get_incoming_elements(), SequenceValue(value=[tom, mary, snoopy]))
        self.assert_lists_eq_items(broccoli.get_neighbors(), SequenceValue(value=[tom, mary, snoopy]))

        self.assert_lists_eq_items(mary.get_out_associations(), SequenceValue(value=[mary_eats_broccoli]))
        self.assert_lists_eq_items(mary.get_in_associations(), SequenceValue(value=[tom_likes_mary,
                                                                                    tom_married_to_mary]))
        self.assert_lists_eq_items(mary.get_outgoing_elements(), SequenceValue(value=[broccoli]))
        self.assert_lists_eq_items(mary.get_incoming_elements(), SequenceValue(value=[tom]))
        self.assert_lists_eq_items(mary.get_neighbors(), SequenceValue(value=[broccoli, tom]))

        self.assert_lists_eq_items(toms_ex.get_out_associations(), SequenceValue(value=[]))
        self.assert_lists_eq_items(toms_ex.get_in_associations(), SequenceValue(value=[tom_likes_his_ex]))
        self.assert_lists_eq_items(toms_ex.get_outgoing_elements(), SequenceValue(value=[]))
        self.assert_lists_eq_items(toms_ex.get_incoming_elements(), SequenceValue(value=[tom]))
        self.assert_lists_eq_items(toms_ex.get_neighbors(), SequenceValue(value=[tom]))

        self.assert_lists_eq_items(snoopy.get_out_associations(), SequenceValue(value=[snoopy_barfs_broccoli,
                                                                                       snoopy_barfs_dogfood,
                                                                                       snoopy_eats_dogfood]))
        self.assert_lists_eq_items(snoopy.get_in_associations(), SequenceValue(value=[tom_owns_snoopy]))
        self.assert_lists_eq_items(snoopy.get_outgoing_elements(), SequenceValue(value=[broccoli, dogfood]))
        self.assert_lists_eq_items(snoopy.get_incoming_elements(), SequenceValue(value=[tom]))
        self.assert_lists_eq_items(snoopy.get_neighbors(), SequenceValue(value=[broccoli, dogfood, tom]))

        self.assert_lists_eq_items(dogfood.get_out_associations(), SequenceValue(value=[]))
        self.assert_lists_eq_items(dogfood.get_in_associations(), SequenceValue(value=[tom_eats_dogfood,
                                                                                       snoopy_barfs_dogfood,
                                                                                       snoopy_eats_dogfood]))
        self.assert_lists_eq_items(dogfood.get_outgoing_elements(), SequenceValue(value=[]))
        self.assert_lists_eq_items(dogfood.get_incoming_elements(), SequenceValue(value=[tom, snoopy]))
        self.assert_lists_eq_items(dogfood.get_neighbors(), SequenceValue(value=[tom, snoopy]))

        self.assert_lists_eq_items(hamburger.get_out_associations(), SequenceValue(value=[]))
        self.assert_lists_eq_items(hamburger.get_in_associations(), SequenceValue(value=[tom_eats_hamburger]))
        self.assert_lists_eq_items(hamburger.get_outgoing_elements(), SequenceValue(value=[]))
        self.assert_lists_eq_items(hamburger.get_incoming_elements(), SequenceValue(value=[tom]))
        self.assert_lists_eq_items(hamburger.get_neighbors(), SequenceValue(value=[tom]))

    def test_multi_layer(self):
        store = Model(name=StringValue("Store"),
                      potency=IntegerValue(2),
                      l_type=ModelReference(path=LocationValue("MMCL")))
        product = Clabject(name=StringValue("Product"),
                           potency=IntegerValue(2),
                           l_type=ClabjectReference(path=LocationValue("MMCL.Class")),
                           abstract=BooleanValue(False),
                           lower=IntegerValue(1))
        vat = Attribute(name=StringValue("VAT"),
                        potency=IntegerValue(1),
                        the_type=FloatType(),
                        default=FloatValue(7.5),
                        l_type=ClabjectReference(path=LocationValue("MMCL.Attribute")))
        price = Attribute(name=StringValue("price"),
                          potency=IntegerValue(2),
                          the_type=FloatType(),
                          default=FloatValue(10),
                          l_type=ClabjectReference(path=LocationValue("MMCL.Attribute")))
        discount = Attribute(name=StringValue("discount"),
                             potency=IntegerValue(2),
                             the_type=FloatType(),
                             default=FloatValue(0),
                             l_type=ClabjectReference(path=LocationValue("MMCL.Attribute")))
        product.add_attributes([vat, price, discount])
        store.add_element(product)

        self.assertEqual(store.get_location(), LocationValue("Store"))
        self.assertEqual(product.get_location(), LocationValue("Store.Product"))
        self.assertEqual(vat.get_location(), LocationValue("Store.Product.VAT"))
        self.assertEqual(price.get_location(), LocationValue("Store.Product.price"))
        self.assertEqual(discount.get_location(), LocationValue("Store.Product.discount"))

        library = Model(name=StringValue("Library"),
                        potency=IntegerValue(1),
                        l_type=ModelReference(path=LocationValue("Store")))
        book = Clabject(name=StringValue("Book"),
                        potency=IntegerValue(1),
                        abstract=BooleanValue(False),
                        l_type=ClabjectReference(path=LocationValue("Store.Product")))
        book_vat = Attribute(name=StringValue("VAT"),
                             potency=IntegerValue(0),
                             l_type=vat,
                             value=FloatValue(7))
        ''' TODO: I'm not too sure about the l_types below. If we want strict
        metamodelling, I don't think we can reference anything from the MMCL
        here, although we kind of have to when introducing new attributes...
        Would fragments be a solution here? This could introduce the notion
        of 'Attribute' and 'Association' into the Store type model.

        Possible solution: maybe an attribute doesn't even have a linguistic
        type? Would that make sense?
            -> That would not solve the problem of being able to introduce
            new classes! '''
        book_price = Attribute(name=StringValue("price"),
                               potency=IntegerValue(1),
                               the_type=FloatType(),
                               default=FloatValue(10),
                               l_type=price)
        book_discount = Attribute(name=StringValue("discount"),
                                  potency=IntegerValue(1),
                                  the_type=FloatType(),
                                  default=FloatValue(0),
                                  l_type=discount)
        book_title = Attribute(name=StringValue("title"),
                               potency=IntegerValue(1),
                               the_type=StringType(),
                               default=StringValue(''),
                               l_type=ClabjectReference(path=LocationValue("MMCL.Attribute")))
        book.add_attributes([book_discount, book_price, book_title, book_vat])
        author = Clabject(name=StringValue("Author"),
                          potency=IntegerValue(1),
                          l_type=ClabjectReference(path=LocationValue("MMCL.Clabject")),
                          abstract=BooleanValue(False))
        author_name = Attribute(name=StringValue("name"),
                                potency=IntegerValue(1),
                                default=StringValue(''),
                                l_type=ClabjectReference(path=LocationValue("MMCL.Attribute")),
                                the_type=StringType())
        author.add_attribute(author_name)
        writer = Association(name=StringValue("writer"),
                             potency=IntegerValue(1),
                             abstract=BooleanValue(False),
                             l_type=ClabjectReference(path=LocationValue("MMCL.Clabject")),
                             from_multiplicity=AssociationEnd(node=book,
                                                              port_name=StringValue('from_book'),
                                                              lower=IntegerValue(0),
                                                              upper=InfiniteValue('+')),
                             to_multiplicity=AssociationEnd(node=author,
                                                            port_name=StringValue('to_author'),
                                                            lower=IntegerValue(1),
                                                            upper=InfiniteValue('+')))
        year = Attribute(name=StringValue("year"),
                         potency=IntegerValue(1),
                         l_type=ClabjectReference(path=LocationValue("MMCL.Attribute")),
                         the_type=IntegerType(),
                         default=IntegerValue(0))
        writer.add_attribute(year)
        library.add_elements([book, author, writer])

        my_library = Model(name=StringValue("MyLibrary"),
                           potency=IntegerValue(0),
                           l_type=ModelReference(path=LocationValue("Library")))
        moby_dick = Clabject(name=StringValue("MobyDick"),
                             potency=IntegerValue(0),
                             l_type=ClabjectReference(path=LocationValue("Library.Book")))
        moby_dick_title = Attribute(name=StringValue("title"),
                                    potency=IntegerValue(0),
                                    l_type=book_title,
                                    value=StringValue("Moby Dick"))
        moby_dick_discount = Attribute(name=StringValue("discount"),
                                    potency=IntegerValue(0),
                                    l_type=book_discount,
                                    value=IntegerValue(0))
        moby_dick_price = Attribute(name=StringValue("price"),
                                    potency=IntegerValue(0),
                                    l_type=book_price,
                                    value=IntegerValue(10))
        moby_dick.add_attributes([moby_dick_discount, moby_dick_price, moby_dick_title])
        hm = Clabject(name=StringValue("HM"),
                      potency=IntegerValue(0),
                      l_type=ClabjectReference(path=LocationValue("Library.Author")))
        hm_name = Attribute(name=StringValue("name"),
                            potency=IntegerValue(0),
                            l_type=author_name,
                            value=StringValue("Herman Melville"))
        hm.add_attribute(hm_name)
        moby_dick_written_by_hm = Association(name=StringValue("moby_dick_written_by_hm"),
                                              potency=IntegerValue(0),
                                              l_type=ClabjectReference(path=LocationValue("Library.writer")),
                                              from_multiplicity=AssociationEnd(port_name=StringValue('from_book'),
                                                                               node=moby_dick),
                                              to_multiplicity=AssociationEnd(port_name=StringValue('to_author'),
                                                                             node=hm))
        my_library.add_elements([moby_dick, hm, moby_dick_written_by_hm])

if __name__ == "__main__":
    unittest.main()