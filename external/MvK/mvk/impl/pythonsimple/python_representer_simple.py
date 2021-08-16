"""
Created on 28-dec.-2013

@author: Simon
"""
from mvk.interfaces.representer import Representer


class PythonRepresenterSimple(Representer):
    """
    Implements the Representer interface. This representer maps
    elements onto their representations, which are Python objects.
    These objects are all of the same physical type: Clabject.
    """

    def __init__(self):
        """
        Constructor
        """
        super(PythonRepresenterSimple, self).__init__()
