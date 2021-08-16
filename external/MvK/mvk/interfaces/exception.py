"""
Created on 3-jan.-2014

@author: Simon
"""


class MvKException:
    def get_message(self):
        raise NotImplementedError()


class MvKStopIteration(MvKException):
    pass


class MvKStandardError(MvKException):
    pass


class MvKArithmeticError(MvKStandardError):
    pass


class MvKFloatingPointError(MvKArithmeticError):
    pass


class MvKOverflowError(MvKArithmeticError):
    pass


class MvKZeroDivisionError(MvKArithmeticError):
    pass


class MvKAttributeError(MvKStandardError):
    pass


class MvKLookupError(MvKStandardError):
    pass


class MvKIndexError(MvKLookupError):
    pass


class MvKKeyError(MvKLookupError):
    pass


class MvKNameError(MvKStandardError):
    pass


class MvKTypeError(MvKStandardError):
    pass


class MvKValueError(MvKStandardError):
    pass


class MvKPotencyError(MvKStandardError):
    pass


class MvKParameterError(MvKStandardError):
    pass
