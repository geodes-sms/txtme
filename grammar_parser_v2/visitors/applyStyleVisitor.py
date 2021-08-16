"""
Author Daniel Riegelhaupt
December 2014

A visitor that takes the styles give by the style defintion and style mapping
and applies them to the keywords an parse tree.
"""

from visitor import Visitor

class ApplyStyleVisitor(Visitor):

    def __init__(self, stylemap, keywordsName = None):
        self.styleMap = stylemap
        self.__stylePosList = []
        if keywordsName: #keywords are optional
            # #a list of keywords is simply shorthand for tokens, we now insert the tokens normally into the stylemap
            for collection in keywordsName.keys():
                if (collection in self.styleMap) and self.styleMap[collection]["keywords_bool"]:
                    st = self.styleMap[collection]['style']
                    del self.styleMap[collection]#we remove the collection name and add items instead
                    for name in keywordsName[collection]:
                        self.styleMap[name] = {'style': st }
                elif ('*' in self.styleMap) and self.styleMap['*']["keywords_bool"]:#generic keywords if the keyword collection name is not defined butthere is a star use this
                    st = self.styleMap['*']['style']
                    for name in keywordsName[collection]:
                        self.styleMap[name] = {'style': st }

                if '*' in self.styleMap:
                    del self.styleMap['*']

    def visit(self,tree):
        """
        Visit the parse tree and return a list with style positions
        :param tree: an instance of a (parse) Tree
        :return: a List whose elements are { startpos , endpos , style} where both pos are {line, column} and style is a (css) string
        """
        self.__stylePosList = []
        self.__innerVisit(tree)
        return self.__stylePosList

    def __innerVisit(self, tree):
        #note the tree given here must already have a path attribute in the nodes and leaves
        # (done in the modelCreatorVistor at the time of writing but might change to separate visitor
        # so that we can also apply styles without creating a model)
        if hasattr(tree,'path'): # a token value will have no path + this makes sure that the tree went trough the visitor first
            found = []
            st = None
            cnt = 0
            t = tree.path
            #print t
            for key in self.styleMap.keys():

                if tree.path.endswith(key) and hasattr(tree, "startpos"):
                    #print "KEY found:" , key
                    found.append(key)

            ln = len(found)
            st = ""
            type =""
            if ln == 1:
                st = self.styleMap[found[0]]["style"]
                type = found[0]
            elif ln > 1:
                st = self.styleMap[found[0]]["style"]
                type = found[0]
                cnt = found[0].count('.')
                for i in range(1,ln):
                    #the results can only be in the same list if the end the same way
                    #the more dots there are, the more a name is specific
                    #the most specific name gets chosen
                    f = found[i].count('.')
                    if  f > cnt:
                        st = self.styleMap[found[i]]["style"]
                        type = found[i]
                        cnt = f

            if st:
                start = { 'line': tree.startpos['line'], 'column' : tree.startpos['column']}
                end = { 'line': tree.endpos['line'], 'column' :tree.endpos['column']}
                #TODO type is added more for the debugger than for the editor might remove it in final version
                t = { 'startpos' : start , 'endpos': end, 'style': st, 'type' : type}
                self.__stylePosList.append( t )

            for child in tree.tail:
                self.__innerVisit(child)