"""
Created on 3-jan.-2014

@author: Simon
"""
import logging
import unittest

from test.system.conformance_test import ConformanceTestCase
from test.system.modeleverything_test import TestEverything
from test.system.mvk_test import MvKTestCase
from test.system.cache_test import CacheTestCase
from test.system.undo import UndoTest
from test.system.benchmark import MvKTest
from test.system.composite_read import CompositeReadTest
from test.testsuitecommon import TestSuiteCommon

class TestSuite(TestSuiteCommon):
    def get_suite(self):
        test_modules = [MvKTestCase,
                        TestEverything,
                        UndoTest,
                        CacheTestCase,
                        MvKTest,
                        CompositeReadTest,
                        ConformanceTestCase]
        suite = unittest.TestSuite()
        for t_m in test_modules:
            suite.addTests(unittest.TestLoader().loadTestsFromTestCase(t_m))
        return suite


if __name__ == '__main__':
    TestSuite().run_tests()
