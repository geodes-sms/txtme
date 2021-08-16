'''
Created on 19-mrt.-2014

@author: Simon
'''


class PhysicalMapper(object):
    """
    A physical mapper maps linguistic types of a user-defined metamodel
    onto physical types. Basically, a physical mapper uses another
    physical mappers and routes its requests to it. At the top, there
    is the 'Representer', which actually represents physical concepts
    in certain media.
    Note that the layout of 'params' can differ from formalism to
    formalism, although it ALWAYS has these three entries:
        - location
        - type
        - attributes
    The only way in which the layout can differ is the contents of the
    attributes entry.
    """
    def create(self, params):
        raise NotImplementedError()

    def read(self, location):
        raise NotImplementedError()

    def update(self, params):
        raise NotImplementedError()

    def delete(self, location):
        raise NotImplementedError()

    def get_physical_attribute_mapping(self):
        raise NotImplementedError()

    def get_physical_update_actions(self):
        raise NotImplementedError()
