"""
Daniel Riegelhaupt - august 2014
v2 October 2014

This visitor is responsible for visiting the Grammar and extracting the mapping information
needed to map the grammar to an instance of a model
"""

from hutnparser import Tree
from visitor import Visitor

#some constants
#the neames of the rules in our meta grammar that correspond to the mappingg of formalism, class, etc...
MAPPER_TOP = "mapper"
MODEL_RULE_NAME = "model_mapping_rule"
MODEL_CHILD = "mapping_rules"
CLASS_RULE_NAME = "class_mapping_rule"
ASSOC_RULE_NAME = "assoc_mapping_rule"
ATTR_RULE_NAME = "attr_mapping_rule"
REF_RULE_NAME = "ref_mapping_rule"

#the name of the rule part that corresponds to the elements being mapped
#for example assume A is being mapped to class B than A is the PRODUCTION name and B is the CONCEPT name
PRODUCTION_NAME = "prod_name"
CONCEPT_NAME = "concept_name"


class ModelMappingVisitor(Visitor):
    """
    This visitor is responsible for visiting the Grammar and extracting the mapping information
    needed to map the grammar to an instance of a model
    author Daniel Riegelhaupt
    """

    def __init__(self):
        self.map = {}

    def visit(self, tree):
        """
        travers the given tree to return the mapping to a model
        :param tree: an STree
        :return: a map containing the semantic mapping
        """
        if self.isTree(tree):
            for child in tree.tail:
                if self.isTree(child) and child.head == MAPPER_TOP:
                    #mapper = 0 'mapper' 1:{ 2: top level mapping rule  3:}
                    self.toMap(child.tail[2])
                    break #no need to travers the tree further after having found the mapper
            return self.map

    def __getName(self, tree):
        t = tree.tail[0]
        if self.isTree(t) and t.head == "path":
            name = self.__tailToString(t.tail)
        return name

    def __tailToString(self, tail):
        """
        create a string from a list of TokenValues
        :param tail: the tail of an STree should contain only TokenValue (which a subclass of String)
        """
        ret = ""
        for elem in tail:
            #print 'tail to str:', elem.head
            if self.isToken(elem):
                ret += self.getTokenValue(elem)
            #else:
            #    print elem.head , " IS NOT TOKEN "#, elem.tail[0].head.tail[0]
            #    ret += "f"#elem.tail[0].head
        return ret

    def __mapAttr(self, tree, prefix):
        t = {}
        t[ATTR_RULE_NAME] = "Attribute"
        t[REF_RULE_NAME] = "Reference"

        rule = ""
        name = ""

        if tree.head == REF_RULE_NAME:
            #for the moment we assume that ref only means association (the HUTN project does the same)
            prefix += ".Association"

        for elem in tree.tail:
            #print elem
            if self.isTree(elem):
                #a name is an instance of rule path.
                # path contains the leaves that form the name
                if elem.head == PRODUCTION_NAME:
                    rule = self.__getName(elem)
                elif elem.head == CONCEPT_NAME:
                    name = self.__getName(elem)

        name = prefix + '.' + name
        self.map[rule] = {"type" : t[tree.head] , "mapping": name }


    def __mapConcept(self, tree):
        t = {}
        t[CLASS_RULE_NAME] = "Class"
        t[ASSOC_RULE_NAME] = "Association"


        conceptRule =""
        conceptName = ""

        for elem in tree.tail:
            if self.isTree(elem):
                if elem.head == PRODUCTION_NAME:
                    conceptRule = self.__getName(elem)
                elif elem.head == CONCEPT_NAME:
                    conceptName = self.__getName(elem)

                    #NOTE maybe create a map with constants instead of writting the string Class or Association , or even better method instead of the dictionary
                    self.map[conceptRule] = {"type" : t[tree.head] , "mapping": conceptName }

                for elem in tree.tail:
                    if self.isTree(elem):
                        if elem.head == ATTR_RULE_NAME or elem.head == REF_RULE_NAME:
                            self.__mapAttr(elem, conceptName)

    def toMap(self, tree):
        if tree.head == MODEL_RULE_NAME:
            formRule = ""
            formFullName = ""
            prefix = ""
            for elem in tree.tail:
                #this for loops work because things are described in order first the production name than the concept name and then the children
                #so we can fill in variables we need for the next one
                if self.isTree(elem):
                    if elem.head == PRODUCTION_NAME:
                        formRule = self.__getName(elem)
                    elif elem.head == CONCEPT_NAME:
                        formFullName = self.__getName(elem)
                        #NOTE maybe create a map with constants instead of writting the string Formalisn , or even better method instead of the dictionary
                        self.map[formRule] = {"type" : "Model" , "mapping": formFullName }
                        index = formFullName.rfind('.')
                        prefix = formFullName
                        if index != -1:
                            prefix = formFullName[index+1:]

                    elif elem.head == MODEL_CHILD:
                        elem2 = elem.tail[0]
                        if elem2.head == ATTR_RULE_NAME:
                            self.__mapAttr(elem2, prefix)
                        elif elem2.head == CLASS_RULE_NAME or elem2.head == ASSOC_RULE_NAME:
                            self.__mapConcept(elem2)