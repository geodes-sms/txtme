'''
Created on 10-feb.-2014

@author: Simon
'''
import unittest


class TestSuiteCommon:
    def get_suite(self):
        raise NotImplementedError()

    def run_tests(self):
        try:
            import coverage
            cov = coverage.coverage()
            cov.start()
        except ImportError:
            pass

        unittest.TextTestRunner(verbosity=2).run(self.get_suite())

        try:
            cov.stop()
            cov.save()

            cov.html_report()
        except NameError:
            pass
