"""
Author Daniel Riegelhaupt
October  2014

A vistitor that reads Style Defintion files and returns a map that can be used by the style mapper
"""

from visitor import  Visitor
from hutnparser import Tree


#SOME RULE NAME CONSTANTES

STYLE_DEF_TOP = "styles"
STYLE_DEF_RULE = "style_def"
STYLE_NAME = "class_name"
ATTR_DEF = "attr_def"

class StyleDefinitionVisitor(Visitor):

    def __init__(self):
        self.map = {}

    def visit(self, tree):
        if self.isTree(tree):
            for elem in tree.tail:
                if elem.head == STYLE_DEF_TOP:
                    self.mapStyles(elem)

        #print self.map
        return self.map

    def mapStyles(self, tree):
        for elem in tree.tail:
            if elem.head == STYLE_DEF_RULE:
                name = ""
                sdef = ""
                for child in elem.tail:
                    if child.head == STYLE_NAME:
                        name = self.getTokenValue(child)[1:] #1: to remove the dot
                    elif child.head == ATTR_DEF:
                        attrs = ""
                        for item in child.tail: #each attribute defintion is name:value in css so we simply keep those results litteraly
                            attrs += self.getTokenValue(item)
                        sdef += attrs + ';'
                        #sdef = self.getTokenValue(child)
                    else:
                        pass
                self.map[name] =  sdef