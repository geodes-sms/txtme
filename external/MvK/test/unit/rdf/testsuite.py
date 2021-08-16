"""
Created on 3-jan.-2014

@author: Simon
"""
import unittest

from test.testsuitecommon import TestSuiteCommon
from test.unit.rdf.datavalue import DataValueTestCase


class TestSuite(TestSuiteCommon):
    def get_suite(self):
        test_modules = [DataValueTestCase]
        suite = unittest.TestSuite()
        for t_m in test_modules:
            suite.addTests(unittest.TestLoader().loadTestsFromTestCase(t_m))
        return suite

if __name__ == '__main__':
    TestSuite().run_tests()
