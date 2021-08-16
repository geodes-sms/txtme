"""
Base class for grammar returned by visitor that creates Grammars from parse trees
"""
import re
class BaseGrammar(object):
    def __init__(self):
        self.rules = {}
        self.tokens = {}

    def classToStr(self, className):
        """
        returns a string that can be written to file
        so that the grammar may be saved after having been generated
        """
        text = 'class ' + className + '(object):\n'
        text+= '\tdef __init__(self):\n'
        text+= '\t\tself.rules = {\n'
        l = len(self.rules.keys()) - 1
        i = 0
        for k in self.rules:
            r = '\'' + k + '\': ' + str(self.rules[k])
            if i < l:
                r += ','
            text +=  '\t\t\t' + r + '\n'
            i += 1
        text+= '\t\t}\n\n'
        text+= '\t\tself.tokens = {\n'
        l = len(self.tokens.keys()) - 1
        i = 0
        for k in self.tokens: #TODO TEST THIS WITH TOKENS AND ESCAPE STRINGS
            r = '\'' + k + '\': { \'type\': \'token\', \'reg\': r\'' +  self.tokens[k]['reg'].decode()+ '\', '
            r += '\'errortext\': \'' + self.tokens[k]['errortext']+ '\''
            if "hidden" in  self.tokens[k]:
                r+= ', \'hidden\': ' + str(self.tokens[k]['hidden'])
            r+= '}'
            if i < l:
                r += ','
            text +=  '\t\t\t' + r + '\n'
            i += 1
        text+= '\t\t}\n'
        return text

    def __isInList(self, val, l):
        for i in l:
            if isinstance(i, list):
                if self.__isInList(val, i):
                    return True
            elif isinstance(val, basestring) and val == i:
                return True
        return False

    def getRulesContaining(self, value):
        """
        Return a list of every production rule that contains value as a member
        :param value:
        :return:
        """
        ret = []
        for rule in self.rules:
            body = self.rules[rule]["body"]
            if self.__isInList(value, body):
                ret.append(rule)
        return ret


    def getInverseMapping(self):
        """
        Returns a dictionary key: list where key is a rule or token name, and list contains all the rules that contain those
        NOTE: this will not include anonmymous
        :return:
        """
        ret = {}
        for token in self.tokens:
            ret[token] = self.getRulesContaining('$'+token)

        for rule in self.rules:
            ret[rule] = self.getRulesContaining('@'+rule)

        return ret