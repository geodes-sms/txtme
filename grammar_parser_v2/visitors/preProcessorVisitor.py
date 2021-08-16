"""
Author Daniel Riegelhaupt
December 2014

The preprocessor combines preprocessing of various visitors.
This has the advantages of reducing the number of time the whole parse tree is visited separately
as well as reducing dependencies between visitors. for example we can now apply styles without
needing to first apply the modelMapperVisitor,
"""
from visitor import Visitor
from hutnparser import Tree


class PreProcessorVisitor(Visitor):
    """
    TODO: path, position, parent

    """
    def visit(self, tree):
        """
        adds paths to the nodes. the paths correspond to the hierarchy and are of the form
        name (for the root)
        parentname.name for a child and recursively so

        we also add a link back to the parent node with the attribute parent.
        the root has parent None
        we do this so that we can search the tree better
        """
        #self.tokenCount = 0
        self.__innerVisit(tree)
        #print "NUMBER OF TOKENS = ", self.tokenCount
        return tree

    def __innerVisit(self,tree):
        if isinstance(tree, Tree):
            setattr(tree, "path", tree.head) #the root
            setattr(tree, "parent", None)
            if not isinstance(tree.tail, basestring): #tokens are allowed to have a path but not their value we cant go down
                for elem in tree.tail:
                    self.__fillPathAttr(elem, tree)
        #else:
        #    self.tokenCount += 1

    def __fillPathAttr(self, tree, parent):
        #helper method of __setPaths
        if isinstance(tree, Tree):
            nPath = parent.path + '.' +tree.head
            setattr(tree, "path", nPath)
            setattr(tree, "parent", parent)
            if not isinstance(tree.tail, basestring):
                for elem in tree.tail:
                    self.__fillPathAttr(elem, tree)
        #else:
        #    self.tokenCount += 1