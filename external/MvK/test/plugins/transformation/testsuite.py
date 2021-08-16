"""
Created on 3-jan.-2014

@author: Simon
"""
import unittest

from test.plugins.transformation.test_matching import MatchTestCase
from test.plugins.transformation.test_mt import ModelTransformationTestCase
from test.plugins.transformation.test_rewriting import RewriteTestCase
from test.testsuitecommon import TestSuiteCommon


class TestSuite(TestSuiteCommon):
    def get_suite(self):
        test_modules = [MatchTestCase,
                        RewriteTestCase,
                        ModelTransformationTestCase]
        suite = unittest.TestSuite()
        for t_m in test_modules:
            suite.addTests(unittest.TestLoader().loadTestsFromTestCase(t_m))
        return suite


if __name__ == '__main__':
    TestSuite().run_tests()
