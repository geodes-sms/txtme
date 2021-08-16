import mvk.interfaces.object

class BasicElement(mvk.interfaces.element.Element):
    def __init__(self, **kwargs):
        for x in kwargs:
            setattr(self, x, kwargs[x])

    def typed_by(self):
        return self.linguistic_type

    def __repr__(self):
        return "---" + str(self.__class__.__name__) + " -- " + str(self.__dict__) + " ---"

class Package(BasicElement):
    pass

class Model(BasicElement):
    pass

class Multiplicity(BasicElement):
    pass

class Clabject(BasicElement):
    pass

class Attribute(BasicElement):
    pass

class AssociationEnd(BasicElement):
    pass

class Association(Clabject):
    pass

class AssociationReference(BasicElement):
    pass

class Composition(Association):
    pass

class Aggregation(Association):
    pass

class Inherits(Association):
    pass
