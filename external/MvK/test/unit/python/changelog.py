import unittest

from mvk.impl.python.changelog import *
from mvk.impl.python.datavalue import *
import mvk.impl.client.object as client_objects

class TestChangelog(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)

    def testInverseUpdate(self):
        ul = MvKUpdateLog()
        ul.set_status_code(UpdateConstants.SUCCESS_CODE)
        ul.set_status_message(StringValue("Success"))
        ul.set_type(LocationValue("mvk.object.Package"))
        ul.add_attr_change(StringValue("name"), StringValue("my_package"), StringValue("my_new_package"))
        ul.set_location(LocationValue("my_package.my_new_package"))
        ops = ul.get_inverse()
        self.assertEquals(len(ops), 1)
        op = ops[0]
        self.assertEquals(op[0], 'update')
        self.assertEquals(type(op[1]), MappingValue)
        self.assertEquals(op[1][UpdateConstants.TYPE_KEY], LocationValue("mvk.object.Package"))
        self.assertEquals(op[1][UpdateConstants.LOCATION_KEY], LocationValue("my_package.my_new_package"))
        self.assertEquals(op[1][UpdateConstants.ATTRS_KEY][StringValue("name")], StringValue("my_package"))

        ul.set_status_code(UpdateConstants.BAD_REQUEST_CODE)
        self.assertEquals(len(ul.get_inverse()), 0)

        ul = MvKUpdateLog()
        ul.set_status_code(UpdateConstants.SUCCESS_CODE)
        ul.set_status_message(StringValue("Success"))
        ul.set_type(LocationValue("mvk.object.Model"))
        ul.add_attr_change(StringValue("potency"), IntegerValue(0), IntegerValue(1))
        ul.set_location(LocationValue("my_package.my_model"))
        ops = ul.get_inverse()
        self.assertEquals(len(ops), 1)
        op = ops[0]
        self.assertEquals(op[0], 'update')
        self.assertEquals(type(op[1]), MappingValue)
        self.assertEquals(op[1][UpdateConstants.TYPE_KEY], LocationValue("mvk.object.Model"))
        self.assertEquals(op[1][UpdateConstants.LOCATION_KEY], LocationValue("my_package.my_model"))
        self.assertEquals(op[1][UpdateConstants.ATTRS_KEY][StringValue("potency")], IntegerValue(0))

        ul = MvKUpdateLog()
        ul.set_status_code(UpdateConstants.SUCCESS_CODE)
        ul.set_status_message(StringValue("Success"))
        ul.set_type(LocationValue("mvk.object.Model"))
        ul.add_attr_change(StringValue("val1"), IntegerValue(0), IntegerValue(5))
        ul.add_attr_change(StringValue("val2"), FloatValue(0), IntegerValue(2))
        ul.add_attr_change(StringValue("val3"), FloatValue(3), IntegerValue(0))
        ul.add_attr_change(StringValue("name"), StringValue("my_model"), StringValue("my_new_model"))
        ul.set_location(LocationValue("my_package.my_new_model"))
        ops = ul.get_inverse()
        self.assertEquals(len(ops), 1)
        op = ops[0]
        self.assertEquals(op[0], 'update')
        self.assertEquals(type(op[1]), MappingValue)
        self.assertEquals(op[1][UpdateConstants.TYPE_KEY], LocationValue("mvk.object.Model"))
        self.assertEquals(op[1][UpdateConstants.LOCATION_KEY], LocationValue("my_package.my_new_model"))
        self.assertEquals(op[1][UpdateConstants.ATTRS_KEY][StringValue("val1")], IntegerValue(0))
        self.assertEquals(op[1][UpdateConstants.ATTRS_KEY][StringValue("val2")], FloatValue(0))
        self.assertEquals(op[1][UpdateConstants.ATTRS_KEY][StringValue("val3")], FloatValue(3))
        self.assertEquals(op[1][UpdateConstants.ATTRS_KEY][StringValue("name")], StringValue("my_model"))

    def testInverseCreate(self):
        cl = MvKCreateLog()
        cl.set_status_code(CreateConstants.SUCCESS_CODE)
        cl.set_status_message(StringValue("Success"))
        cl.set_location(LocationValue("my_package.my_second_package"))
        cl.set_type(LocationValue("mvk.object.Package"))
        cl.set_name(StringValue("my_new_package"))
        ops = cl.get_inverse()
        self.assertEquals(len(ops), 1)
        op = ops[0]
        self.assertEquals(op[0], 'delete')
        self.assertEquals(op[1], LocationValue("my_package.my_second_package.my_new_package"))

        cl.set_status_code(CreateConstants.BAD_REQUEST_CODE)
        cl.set_status_message(StringValue("Fail"))
        ops = cl.get_inverse()
        self.assertEquals(len(ops), 0)

    def testInverseCreateComposite(self):
        cl = MvKCompositeLog()
        cl1 = MvKCreateLog()
        cl1.set_status_code(CreateConstants.SUCCESS_CODE)
        cl1.set_status_message(StringValue("Success"))
        cl1.set_location(LocationValue(""))
        cl1.set_type(LocationValue("mvk.object.Package"))
        cl1.set_name(StringValue("my_package"))
        cl.add_log(cl1)
        cl1 = MvKCreateLog()
        cl1.set_status_code(CreateConstants.SUCCESS_CODE)
        cl1.set_status_message(StringValue("Success"))
        cl1.set_location(LocationValue("my_package"))
        cl1.set_type(LocationValue("mvk.object.Package"))
        cl1.set_name(StringValue("my_outer_package"))
        cl.add_log(cl1)
        cl1 = MvKCreateLog()
        cl1.set_status_code(CreateConstants.SUCCESS_CODE)
        cl1.set_status_message(StringValue("Success"))
        cl1.set_location(LocationValue("my_package.my_outer_package"))
        cl1.set_type(LocationValue("mvk.object.Package"))
        cl1.set_name(StringValue("my_inner_package"))
        cl.add_log(cl1)
        cl1 = MvKCreateLog()
        cl1.set_status_code(CreateConstants.SUCCESS_CODE)
        cl1.set_status_message(StringValue("Success"))
        cl1.set_location(LocationValue("my_package.my_outer_package.my_inner_package"))
        cl1.set_type(LocationValue("mvk.object.Model"))
        cl1.set_name(StringValue("my_model"))
        cl.add_log(cl1)

        inverse = cl.get_inverse()
        self.assertEquals(len(inverse), 4)
        op = inverse[0]
        self.assertEquals(op[0], 'delete')
        self.assertEquals(op[1], LocationValue('my_package.my_outer_package.my_inner_package.my_model'))
        op = inverse[1]
        self.assertEquals(op[0], 'delete')
        self.assertEquals(op[1], LocationValue('my_package.my_outer_package.my_inner_package'))
        op = inverse[2]
        self.assertEquals(op[0], 'delete')
        self.assertEquals(op[1], LocationValue('my_package.my_outer_package'))
        op = inverse[3]
        self.assertEquals(op[0], 'delete')
        self.assertEquals(op[1], LocationValue('my_package'))

if __name__ == "__main__":
    unittest.main()
