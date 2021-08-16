"""
Author Daniel Riegelhaupt
Date October 2014

A visitor that takes a tree returned by the parser parsing a grammar
and returns a structure that the parser can use to parse files written in that grammar
"""
from hutnparser import * #we  import the parser for constant, and the Tree Class
from baseGrammar import BaseGrammar
from visitor import Visitor
from time import time


# a method that transforms the dic structure this visitors must generate to a string
# used for debugging or testing purposes
def dicToStr(dic):
    text = ""
    keys = dic.keys()
    last = None
    if len(keys) > 0:
        last = keys[-1]
    for key in dic.keys():
        text +=  "'" + key + "': "
        val = dic[key]
        if isinstance(val, dict):
            text += " { " + dicToStr(val) +" }, \n"
        else:
            text += str(val)
            if key != last:
                text += ", "
    return text


#some constants rule names
START_RULE = "start"
GRAMMAR_RULE = "grammar"
PROD_RULE = "production_rule"

RULE_DEF = "rule_definition"
RULE_NAME = "rule_name"
RULE_RHS = "rule_right_hand_side"

TOKEN_DEF = "token_definition"
TOKEN_COLLECTION = "token_collection"
TOKEN_SUB_COLLECTION = "token_sub_collection"
TOKEN_NAME= "token_name"
TOKEN_VALUE = "token_value"

KEYWORD_TYPE = "keywords"
MESSAGE = "message"

MODIFIER = "modifier"
IMPL_MOD = "IMPLICIT_MOD" #token name  not a rule name
CMNT_MOD = "COMMENT_MOD" #token name  not a rule name

#for rhs rules
CARD_RULE = "cardinality"
MINUS= "MINUS" #token name  not a rule name
INT = "INT" #token name  not a rule name

OPER = "OPER"
OR = "OR"
LPAR = "LPAR"
RPAR = "RPAR"

#parser constants
TOKEN_TYPE = Parser.Constants.Token
PROD_TYPE=  Parser.Constants.Production


class GrammarCompilerVisitor(Visitor):
    """
    A visitor that takes a tree returned by the parser after having parsed a grammar
    and returns a structure that the parser can use to parse files written in that grammar
    """
    def __init__(self):
        self.tokens = {}
        self.rules = {}
        self.keywords = {}
        self.keywordsName = {}
        self.implicit = []

    def visit(self, tree):
        if self.isTree(tree):
            if tree.head == START_RULE:
                for item in tree.tail:
                    #print "ITEM", item.head, " is tree: ", self.isTree(item)
                    if self.isTree(item) and item.head == GRAMMAR_RULE:
                        self.visitGrammar(item)
                    #elif self.isTree(item, Tree) and item.head == MAPPER_RULE:
                    #    self.visitMapper(item)
                    #    TODO or maybe in a complete separate visitor depending on how complex this one gets

        self.addImplicit()
        #print "Tokens: "
        #print dicToStr(self.tokens)
        #print "rules: "
        #print dicToStr(self.rules)

        class Grammar(BaseGrammar):
            def __init__(me):
                me.rules = self.rules
                me.tokens = self.tokens


        #print self.keywords
        return Grammar

    def getKeywordsValue(self):
        return self.keywords

    def getKeywordsName(self):
        return self.keywordsName

    def visitGrammar(self,tree):
        if self.isTree(tree):
            for child in tree.tail:
                if self.isTree(child):
                    rule = child.head
                    if rule == PROD_RULE: #a grammar consists of prod rules and a prod rule can be a rule or token
                        self.visitGrammar(child)
                    elif rule == RULE_DEF: #top level rule definition
                        self.visitRule(child)
                    elif rule == TOKEN_COLLECTION: #part of th grammar where tokens are defined as a def or collection
                        self.visitTokens(child)
                    else:
                        print 'Encountered unexpected rule type in grammar rule. type: ', rule

    def visitRule(self,tree):
        if self.isTree(tree):
            name = ''
            body = ''
            msg = ''
            for child in tree.tail:
                if self.isTree(child):
                    rule = child.head
                    if rule == RULE_NAME:
                       name = self.getTokenValue(child)
                       # print name
                    elif rule == RULE_RHS:
                        body = self.createRHS(child)
                    elif rule == MESSAGE: #part of th grammar where tokens are defined as a def or collection
                        #the child  0 is @Msg or Message
                        #child 1 is a token of type REGEXP and his tail contains the value
                        msg = self.getTokenValue(child.tail[1])
                    else:
                        print 'Encountered unexpected rule type in rule definition. type: ', rule

            if name and body:
                if msg:
                    msg = msg[1:-1] #remove the quotes
                else: #if there was no message
                    msg = name #then the message is the name f the rule
                self.addRule(name, body, msg)

    def createRHS(self, tree):
        #the tree is right balanced and makes seeing what belongs with wht very difficult, to counter this we flatten
        #the rhs
        leaves = self.flattenRHS(tree)
        #print leaves
        rhs , i= self.innerRHS(leaves,0)
        #print rhs
        return rhs

    def startsWithOper(self,l):
        ret = False
        if isinstance(l, list) and len(l) >0:
            z = l[0]
            if not isinstance(z, list):
                if z == '.' or z == '?' or z == '*' or z == '+' or z =='|' or z.startswith('#'):
                    return True

    def innerRHS(self, leaves, index):
        i = index
        cont = True
        rhs = []
        parent = None #a temporary parent if tehre is an or
        nI = -1
        while (i >= 0 and i < len(leaves)) and cont:
            item = leaves[i]
            nI = -1

            if item.startswith('@') | item.startswith('$'): #token or rule
                rhs.append(item)

            elif item.startswith('#'): #cardinal
                temp = None
                if isinstance(rhs[-1],list): #if previous item is a list
                    if rhs[-1][0] == '.':
                        temp = rhs[-1][1:]
                    else:
                        temp = rhs[-1]

                    first = temp[0][0]
                    if first == '@' or first == '$':
                        temp[0] = temp[0][1:]
                    temp[0] = str(item + temp[0])
                    rhs[-1] = temp
                else:
                    print "Encountered cardinal after item but can only place cardinal after list"

            elif item.startswith('*') or item.startswith('+') or item.startswith('?'): #operator
                r = rhs[-1]
                if isinstance(r,list): #if previous item is a list #this means there were parenthesis
                    if self.startsWithOper(r):
                        rhs[-1] = [ item, r]
                    else:
                        rhs[-1] = [item] + r
                else:
                    rhs[-1] = [item] + [r]

            elif item.startswith('|'): #or
                if parent == None: #this is the first time we encounter a or on this level

                    if self.startsWithOper(rhs):
                        if len(rhs) == 2 and rhs[0] == '.':
                            rhs[0] == '|'
                        else:
                            rhs = ['|'] + [rhs]
                    elif len(rhs) ==  1:
                        rhs = ['|'] + rhs
                    else:
                        rhs = ['|', [ '.'] + rhs]

                    #we now temporally sve rhs as its own parent so that we can continue on this level
                    #we can not call this method recursively in this case because this would cause problems if we encounter a ) and need to go back a level
                    parent = rhs
                    rhs = []

                else: #this is at least the second time we encounter an or
                    #print "RHS untilnow" , rhs
                    parent = self.__appendToParent(parent,rhs)
                    rhs = [] #we reset the rhs agin to get whatever comes after

            elif item.startswith('('): #star of a sequence
                r ,nI = self.innerRHS(leaves,i+1)
                i = nI
                rhs.append(r)
            elif item.startswith(')'): #end of a sequence
                cont = False
            else: #anon token
                rhs.append(item)

            if nI == -1: #if that is the case i has already been updated
                i += 1

        #if we had an OR than before we exit this level we nake sure to append the current rhs to the full list
        ## and to return that
        if parent != None:
            rhs = self.__appendToParent(parent,rhs)

        #if the parentheses are top level we get this [[...]]
        #we only need one layer of []
        if len(rhs) == 1 and isinstance(rhs[0], list):
            rhs = rhs[0]

        if not self.startsWithOper(rhs):
            rhs = ['.'] + rhs

        for j in range( 1, len(rhs)):
            if isinstance(rhs[j], list) and len(rhs[j]) == 2 and rhs[j][0] == '.':
                rhs[j] = rhs[j][1]

        return rhs, i

    def __appendToParent(self, parent, rhs):
        if len(rhs) == 1:
            parent += rhs
        elif len(rhs) == 2:
            if self.startsWithOper(rhs):
                if rhs[0] == '.':
                    parent.append(rhs[0])
                else:
                    parent += rhs
            else:
                rhs = ['.'] + rhs
                parent += [rhs]

        elif rhs[0] == '.' or rhs[0].startswith('#'): #if bigger than two and a sequence or cardinal
            parent += [rhs]
        else:
            rhs = ['.'] + rhs
            parent += [rhs]

        return parent


    def flattenRHS(self, tree):
        rhs = []
        for item in tree.tail:
            head = item.head
            if self.isTree(item):
                if head == TOKEN_NAME: # a reference to a token
                    tok =  '$' + self.getTokenValue(item)
                    rhs.append(tok)

                elif head == TOKEN_VALUE: #an anonymous token, written directly in the rule
                    tok = self.getTokenValue(item)
                    rhs.append(tok[1:-1])

                elif head == RULE_NAME: #a reference to a rule
                    rule =  '@' + self.getTokenValue(item)
                    rhs.append(rule)

                elif head == CARD_RULE: #there is a cardinality operator
                    operator = '#'
                    extra = '('
                    for child in item.tail:
                        if child.head == MINUS:
                            extra += '-'
                        if child.head == INT:
                            extra += self.getTokenValue(child) + ')'
                            operator += extra
                    rhs.append(operator)

                elif head == RULE_RHS: # another rhs rule
                    r = self.flattenRHS(item)
                    rhs += r
                else:
                    pass
                    #print 'Encountered unexpected rule type in tree RHS with head: ', item.head
            elif self.isToken(item):
                #print "TOKEN INNER in rule:",  tree.head, "with name", item.head, " value", self.getTokenValue(item)
                head = item.head
                if head == OPER:
                    operator = self.getTokenValue(item)
                    rhs.append(operator)
                elif head == OR:
                    rhs.append('|')
                elif head == LPAR:
                    rhs.append('(')
                elif head == RPAR:
                   rhs.append(')')
                else:
                    pass
                    #print 'Encountered unexpected Token in RHS of kind: ', head
        return rhs

    def addImplicit(self):
        if self.implicit and self.rules.has_key('start'):

            t = str(time())
            t = t.replace('.','')[:-5]
            name = 'implicit_autogenerated_' + t
            #name + random number to avoid any conflicts with possible names

            impl=  ['|'] + self.implicit
            body = [ '*', impl ]
            msg = "Automatically generated 'Implict' rule"

            #we add it to the rules
            self.addRule(name, body, msg)
            self.rules['start']['interleave'] = ['?', '@' + name]


    def visitTokens(self,tree):
        if self.isTree(tree):
            for child in tree.tail:
                if self.isTree(child):
                    rule = child.head
                    if rule == TOKEN_DEF:
                        self.fillTokenInfo(child)
                    elif rule == TOKEN_SUB_COLLECTION:
                        #a collection is 0 type 1: 2 name 3 {  4 and further token_defs last }
                        colType  = self.getTokenValue(child.tail[0])
                        colName = self.getTokenValue(child.tail[2])
                        for item in child.tail[4:]:
                            if self.isTree(item) and item.head == TOKEN_DEF:
                                self.fillTokenInfo(item,colType, colName)
                    else: #token_collection_content is the  parent of both token def and token sub collection
                        self.visitTokens(child)

    def fillTokenInfo(self,tree, colType = None, colName = ''):
        name = ''
        val = ''
        msg = ''
        other_options = {}
        for item in tree.tail:
            if self.isTree(item):
                head = item.head
                if head == TOKEN_NAME:
                    #token name contains a child of type token uppercase and this child contains the actual value
                    name =  self.getTokenValue(item)
                elif head == TOKEN_VALUE:
                    val = self.getTokenValue(item)
                elif head == MESSAGE:
                    #the child  0 is @Msg or Message
                    #child 1 is a token of type REGEXP and his tail contains the value
                    msg = self.getTokenValue(item.tail[1])
                elif head == MODIFIER:
                    #the tail is the token, the head gives us the name we don't need the actual value
                    #especially since the actual value might change
                    if item.tail[0].head == IMPL_MOD:
                        self.implicit.append( '$' + name)
                    elif item.tail[0].head == CMNT_MOD:
                        self.implicit.append( '$' + name)
                        other_options['hidden'] = False #a comment should be kept in the tree by the parser even if other implicit tokens aren't
                    #else:
                        #pass
                        #TODO if there are multiple modifiers do something
        if name and val:
            if msg:
                msg = msg[1:-1] #remove the quotes
            else: #if there was no message
                msg = val[1:-1] #then the message is the value of the token, remove the quotes
            self.addToken(name, val, msg, other_options)
            if colType: #ifcollection type
                if colType == KEYWORD_TYPE:
                    if not colName in self.keywords:
                        self.keywords[colName] = { "values" : [], "style" : None} #style will be added by another visitor
                        self.keywordsName[colName] = []
                    self.keywords[colName]["values"].append(val[1:-1])
                    self.keywordsName[colName].append(name)
                #elsif: for the moment there are only keywords, but ig that changes add collection here


    def addToken(self, name, value, msg, extra = {}):
        r = re.compile(value)
        val = {'type': TOKEN_TYPE, 'reg': r.pattern[1:-1] , 'errortext': msg }
        if extra:
            for k in extra.keys():
                val[k] = extra[k]
        self.tokens[name] = val

    def addRule(self, name, rhs, msg):
        val = {'type': PROD_TYPE, 'body': rhs, 'errortext': msg }
        self.rules[name] = val