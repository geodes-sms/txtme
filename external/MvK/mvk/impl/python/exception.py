"""
Created on 3-jan.-2014

@author: Simon
"""
import mvk.interfaces.exception

class MvKException(Exception, mvk.interfaces.exception.MvKException):
    """ === CONSTRUCTOR === """
    def __init__(self, msg=None):
        from mvk.impl.python.datavalue import StringValue
        if msg is None:
            self.msg = StringValue('No exception message specified')
        else:
            assert isinstance(msg, StringValue)
            self.msg = msg

    """ === PUBLIC INTERFACE === """
    def get_message(self):
        return self.msg

    def __eq__(self, other):
        return (super(MvKException, self).__eq__(other) and
                isinstance(other, mvk.interfaces.exception.MvKException) and
                self.msg == other.get_message())

    """ === PYTHON SPECIFIC === """
    def __str__(self):
        return repr(self.msg)


class MvKStopIteration(MvKException, StopIteration):
    """ === PUBLIC INTERFACE === """
    def __eq__(self, other):
        return (super(MvKStopIteration, self).__eq__(other) and
                isinstance(other, mvk.interfaces.exception.MvKStopIteration))


class MvKStandardError(MvKException,
                       mvk.interfaces.exception.MvKStandardError):
    """ === PUBLIC INTERFACE === """
    def __eq__(self, other):
        return (super(MvKStandardError, self).__eq__(other) and
                isinstance(other, mvk.interfaces.exception.MvKStandardError))


class MvKArithmeticError(MvKStandardError,
                         mvk.interfaces.exception.MvKArithmeticError):
    """ === PUBLIC INTERFACE === """
    def __eq__(self, other):
        return (super(MvKArithmeticError, self).__eq__(other) and
                isinstance(other, mvk.interfaces.exception.MvKArithmeticError))


class MvKFloatingPointError(MvKArithmeticError,
                            mvk.interfaces.exception.MvKFloatingPointError):
    """ === PUBLIC INTERFACE === """
    def __eq__(self, other):
        return (super(MvKFloatingPointError, self).__eq__(other) and
                isinstance(other, mvk.interfaces.exception.MvKFloatingPointError))


class MvKOverflowError(MvKArithmeticError,
                       mvk.interfaces.exception.MvKOverflowError):
    """ === PUBLIC INTERFACE === """
    def __eq__(self, other):
        return (super(MvKOverflowError, self).__eq__(other) and
                isinstance(other, mvk.interfaces.exception.MvKOverflowError))


class MvKZeroDivisionError(MvKArithmeticError,
                           mvk.interfaces.exception.MvKZeroDivisionError):
    """ === PUBLIC INTERFACE === """
    def __eq__(self, other):
        return (super(MvKZeroDivisionError, self).__eq__(other) and
                isinstance(other, mvk.interfaces.exception.MvKZeroDivisionError))


class MvKAttributeError(MvKStandardError,
                        mvk.interfaces.exception.MvKAttributeError):
    """ === PUBLIC INTERFACE === """
    def __eq__(self, other):
        return (super(MvKAttributeError, self).__eq__(other) and
                isinstance(other, mvk.interfaces.exception.MvKAttributeError))


class MvKLookupError(MvKStandardError,
                     mvk.interfaces.exception.MvKLookupError):
    """ === PUBLIC INTERFACE === """
    def __eq__(self, other):
        return (super(MvKLookupError, self).__eq__(other) and
                isinstance(other, mvk.interfaces.exception.MvKLookupError))


class MvKIndexError(MvKLookupError,
                    mvk.interfaces.exception.MvKIndexError):
    """ === PUBLIC INTERFACE === """
    def __eq__(self, other):
        return (super(MvKIndexError, self).__eq__(other) and
                isinstance(other, mvk.interfaces.exception.MvKIndexError))


class MvKKeyError(MvKLookupError,
                  mvk.interfaces.exception.MvKKeyError):
    """ === PUBLIC INTERFACE === """
    def __eq__(self, other):
        return (super(MvKKeyError, self).__eq__(other) and
                isinstance(other, mvk.interfaces.exception.MvKKeyError))


class MvKNameError(MvKStandardError,
                   mvk.interfaces.exception.MvKNameError):
    """ === PUBLIC INTERFACE === """
    def __eq__(self, other):
        return (super(MvKNameError, self).__eq__(other) and
                isinstance(other, mvk.interfaces.exception.MvKNameError))


class MvKTypeError(MvKStandardError,
                   mvk.interfaces.exception.MvKTypeError):
    """ === PUBLIC INTERFACE === """
    def __eq__(self, other):
        return (super(MvKTypeError, self).__eq__(other) and
                isinstance(other, mvk.interfaces.exception.MvKTypeError))


class MvKValueError(MvKStandardError,
                    mvk.interfaces.exception.MvKValueError):
    """ === PUBLIC INTERFACE === """
    def __eq__(self, other):
        return (super(MvKValueError, self).__eq__(other) and
                isinstance(other, mvk.interfaces.exception.MvKValueError))


class MvKPotencyError(MvKStandardError,
                      mvk.interfaces.exception.MvKPotencyError):
    """ === PUBLIC INTERFACE === """
    def __eq__(self, other):
        return (super(MvKPotencyError, self).__eq__(other) and
                isinstance(other, mvk.interfaces.exception.MvKPotencyError))


class MvKParameterError(MvKStandardError,
                        mvk.interfaces.exception.MvKParameterError):
    """ === PUBLIC INTERFACE === """
    def __eq__(self, other):
        return (super(MvKParameterError, self).__eq__(other) and
                isinstance(other, mvk.interfaces.exception.MvKParameterError))
