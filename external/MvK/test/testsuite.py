'''
Created on 10-feb.-2014

@author: Simon
'''
import unittest

from test.testsuitecommon import TestSuiteCommon
import test.unit.testsuite
import test.system.testsuite
import test.plugins.testsuite


class TestSuite(TestSuiteCommon):
    def get_suite(self):
        test_suites = [test.unit.testsuite.TestSuite(),
                       test.system.testsuite.TestSuite(),
                       test.plugins.testsuite.TestSuite()]
        suite = unittest.TestSuite()
        for s in test_suites:
            suite.addTests(s.get_suite())
        return suite

if __name__ == '__main__':
    TestSuite().run_tests()
