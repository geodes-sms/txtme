"""
Author Daniel Riegelhaupt
October 2014

A base class for the visitors
"""

from hutnparser import Tree

class Visitor(object):
    """
    A base class containing helper methods that evert visitor will need.
    along with the one method every visitor has in common namely: visit
    """
    def visit( self, tree):
        raise NotImplementedError( "Any visitor must implement a visit method" )

    """
    The way the data structure is: a token is a tree with a tail containing a single string
    so it isn't enough to just check for isinstance tree
    """
    def isTree(self, item):
        ret = False
        if isinstance(item, Tree):
            if len(item.tail) > 1:
                ret = True
            elif len(item.tail) == 1 and isinstance(item.tail[0], Tree):
                ret = True
        return ret

    def isToken(self,item):
        ret = False
        if isinstance(item, Tree):
            if len(item.tail) == 1 and isinstance(item.tail[0], basestring):
                ret = True
        return ret

    def getTokenValue(self, item):
        #in a rule like Place : place_name ....,
        # place_name : LOWER_LETTER
        #and item is place_name than the value is at the bottom of place_name -> LOWER_LETTER -> value
        #USE ONLY WHEN SURE YOU ARE EXPECTING A TOKEN VALUE
        while item and isinstance(item, Tree):
            item = item.tail[0]
        return str(item)