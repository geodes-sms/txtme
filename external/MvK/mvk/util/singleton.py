"""
Created on 9-jan.-2014

@author: Simon
"""


class _Singleton(type):
    def __init__(cls, name, bases, dict):
        super(_Singleton, cls).__init__(name, bases, dict)
        cls.instance = None

    def __call__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = super(_Singleton, cls).__call__(*args, **kw)
        return cls.instance


class Singleton(object):
    """ Any class which inherits from Singleton can be instantiated by calling
    the constructor will ensure only a single object is created. any further
    attempts to instantiate new objects will return the existing singleton
    object without invoking the constructor."""
    __metaclass__ = _Singleton
    # The method below is to maintain backwards compatibility
    _instance = None

    @classmethod
    def get_instance(cls, *args, **kargs):
        if cls._instance is None:
            if len(args) > 0:
                if len(kargs) > 0:
                    cls._instance = cls(*args, **kargs)
                else:
                    cls._instance = cls(*args)
            else:
                if len(kargs) > 0:
                    cls._instance = cls(**kargs)
                else:
                    cls._instance = cls()
        return cls._instance
