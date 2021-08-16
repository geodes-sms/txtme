"""
Created on 28-dec.-2013

@author: Simon
"""

#TODO global logger might be problematic

import logging
import logging.config
import os


initialized = False


class LoggerWrapper(object):
    def __init__(self, logger):
        self.l = logger

    def isEnabledFor(self, level):
        return self.l.isEnabledFor(level)

    def log(self, level, msg):
        """
        Do the actual logging at the specified level, but save it in case no logger exists yet

        :param level: string representation of the function to call on the logger
        :param msg: the message to log
        :returns: True -- to allow it as an assert statement
        """
        getattr(self.l, level)(msg)
        return True

    def debug(self, msg):
        """
        Debug logging statement

        :param msg: the message to print
        :returns: True -- to allow it as an assert statement
        """
        return self.log("debug", str(msg))

    def info(self, msg):
        """
        Informational logging statement

        :param msg: the message to print
        :returns: True -- to allow it as an assert statement
        """
        return self.log("info", str(msg))

    def warn(self, msg):
        """
        Warning logging statement

        :param msg: the message to print
        :returns: True -- to allow it as an assert statement
        """
        return self.log("warn", str(msg))

    def error(self, msg):
        """
        Error logging statement

        :param msg: the message to print
        :returns: True -- to allow it as an assert statement
        """
        return self.log("error", str(msg))


def initialize():
    global initialized
    dirname = os.path.dirname(__file__)
    logging.config.fileConfig(dirname[:dirname.rfind('mvk') + 4] + 'logging.conf')
    initialized = True


def get_logger(name=None):
    global initialized
    if not initialized:
        initialize()
    return LoggerWrapper(logging.getLogger(name))
