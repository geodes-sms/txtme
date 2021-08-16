"""
Daniel Riegelhaupt
February 2015
A visitor that returns values for all instances of a token
"""

from visitor import Visitor

class TokenFinderVisitor(Visitor):

    def visit(self, tree, tokenName):
        self.retList = []
        self.__innerVisit(tree,tokenName)
        return self.retList

    def __innerVisit(self, tree, tokenName):
        if self.isTree(tree):
            for child in tree.tail:
                self.__innerVisit(child, tokenName)
        elif self.isToken(tree) and tree.head == tokenName:
            self.retList.append(tree.tail[0])