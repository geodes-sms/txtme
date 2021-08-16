"""
Author Daniel Riegelhaupt
October 2014

A visitor that creates a style mapping combining the style definition given by the style definition visitor and the mapping file read.
"""

from visitor import  Visitor
from hutnparser import Tree

#SOME RULE NAME CONSTANTES

STYLE_MAP_TOP = "style_mapping"
STYLE_MAP_RULE = "style_map"
TYPE = "type"
PATH_NAME = "path_name" #name of the rule, token or keyword group we want to map a style to
STYLE_NAME = "style_name" #the name of the style we want to map to the item

#type values: for the moment only keywors, rule and tokne dont need to e added specifcally
KEYWORDS = "@Keywords"
DEFAULT = "@Default"
ERROR = "@Error"

class StyleMappingVisitor(Visitor):

    def __init__(self, defs):
        self.defs = defs
        self.map = {}
        self.warnings = []

    def visit(self, tree):
        if self.isTree(tree):
            for elem in tree.tail:
                if elem.head == STYLE_MAP_TOP:
                    self.mapStyles(elem)
        self.applyDefs()
        return self.map

    def getWarnings(self):
        return self.warnings

    def applyDefs(self):
        for key in self.map.keys():
            item = self.map[key]
            if self.defs.has_key(item['style']):
                item['style'] = self.defs[item['style']]
            else:
                err = "style: " +  item['style'] + " is not defined"
                #item['style'] = None #TODO maybe this should be done or maybe in another part we should validate css
                self.warnings.append(err)


    def getDotName(self, tree):
        #path_name = IDEN (DOT IDEN)* do we simply merge token values
        name = ""
        for elem in tree.tail:
            name += self.getTokenValue(elem)
        return name

    def mapStyles(self, tree):
        for elem in tree.tail:
            if elem.head == STYLE_MAP_RULE:
                path = ""
                style = ""
                keywords = False
                default = False
                error = False
                for child in elem.tail:
                    if child.head == TYPE:
                        type = self.getTokenValue(child)
                        if  type == KEYWORDS:
                            keywords = True
                        elif type == DEFAULT:
                            default = True
                        elif type == ERROR:
                            error = True

                    elif child.head == PATH_NAME:
                        path = self.getDotName(child)
                    elif child.head == STYLE_NAME:
                        style = self.getTokenValue(child)
                    else:
                        pass

                if  default:
                    self.map[DEFAULT] = { "style" : style, "keywords_bool" : False }
                elif error:
                    self.map[ERROR] = { "style" : style, "keywords_bool" : False }
                else:
                    self.map[path] = { "style" : style, "keywords_bool" : keywords }