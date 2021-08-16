"""
Created on 28-dec.-2013

@author: Simon
"""
from mvk.interfaces.physical_mapper import PhysicalMapper


class Representer(PhysicalMapper):
    """
    Interface class for a representer. Its task is to map physical
    concepts of the physical type model onto
    objects in a certain medium, such as instances of Python classes,
    database entries, nodes
    and edges in a graph, etc. For documentation on the interface
    methods, see L{MvK<mvk.mvk.MvK>}
    """
    def create(self, params):
        raise NotImplementedError()

    def read(self, location):
        raise NotImplementedError()

    def update(self, params):
        raise NotImplementedError()

    def delete(self, location):
        raise NotImplementedError()

    def clear(self):
        raise NotImplementedError()

    def backup(self, filename=None):
        raise NotImplementedError()

    def restore(self):
        raise NotImplementedError()

    def apply(self, op_name, params):
        raise NotImplementedError()
