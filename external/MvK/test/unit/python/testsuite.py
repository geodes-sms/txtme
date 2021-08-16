"""
Created on 3-jan.-2014

@author: Simon
"""
import unittest

from test.testsuitecommon import TestSuiteCommon
from test.unit.python.action import ActionTestCase
from test.unit.python.datatype import DataTypeTestCase
from test.unit.python.datavalue import DataValueTestCase
from test.unit.python.object import ObjectTestCase
from test.unit.python.serialization import TestSerialization
from test.unit.python.changelog import TestChangelog


class TestSuite(TestSuiteCommon):
    def get_suite(self):
        test_modules = [DataValueTestCase,
                        DataTypeTestCase,
                        ObjectTestCase,
                        TestSerialization,
                        TestChangelog,
                        ActionTestCase]
        suite = unittest.TestSuite()
        for t_m in test_modules:
            suite.addTests(unittest.TestLoader().loadTestsFromTestCase(t_m))
        return suite


if __name__ == '__main__':
    TestSuite().run_tests()
