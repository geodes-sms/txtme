"""
Daniel Riegelhaupt
February 2015
A visitor that  sets all Positions correctly
This is used by the partial Tree fuser
"""

from position import  Position
from visitor import Visitor
from hutnparser import Tree

class PositionVisitor(Visitor):

    def visit(self, tree):
        """
        visitss atree composed of partial trees and makes sure that every level has the correct positions
        Notate that as at the very least all tokens already have a correct position
        :param tree: a tree composed of partial trees
        :return: that same tree but with correct position
        """
        self.defaultPos = Position(-1,-1)
        self.__fillNodes(tree)
        return tree

    def __fillNodeInner(self,elem):
        """
        Sets the interval of an element
        """
        if self.isToken(elem) or elem.startpos != self.defaultPos:
            return (elem.startpos , elem.endpos)
        else:
            endI = len(elem.tail)
            leftMost = self.__fillNodeInner(elem.tail[0])
            rightMost = leftMost
            if endI > 1:
                rightMost = self.__fillNodeInner(elem.tail[endI-1])

            #the interval of a node is the start of the leftmost child and the end of the rightmost child
            elem.startpos = leftMost[0]
            elem.endpos = rightMost[1]
            return (elem.startpos , elem.endpos)

    def __fillNodes(self, tree):
        """
        fill every nodes and every child node
        """
        if self.isTree(tree):
            self.__fillNodeInner(tree)
            for elem in tree.tail:
                self.__fillNodes(elem)