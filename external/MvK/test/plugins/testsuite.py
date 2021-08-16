'''
Created on 10-feb.-2014

@author: Simon
'''
import logging
import unittest

from test.testsuitecommon import TestSuiteCommon
import test.plugins.transformation.testsuite


class TestSuite(TestSuiteCommon):
    def get_suite(self):
        test_suites = [test.plugins.transformation.testsuite.TestSuite()]
        suite = unittest.TestSuite()
        for s in test_suites:
            suite.addTests(s.get_suite())
        return suite

if __name__ == '__main__':
    TestSuite().run_tests()
