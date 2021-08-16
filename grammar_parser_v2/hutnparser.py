"""
Author: Bruno Barroca
Date: October 2014
Description: A top down parser

Modifications by Daniel Riegelhaupt:
*removed test input
*changed pos to startpos because in my humble opinion it makes more sense to have a tupple (startpos, endpos) than (pos, endpos)
*aded parameters to init: tab_size, line_position, hide_implicit
 - see init comments for more info on all otions
 - line_position will change startpos and end Pos to instance of class Position. (changed december 2014)
*Added anonymous terminals: tokens do not have to be defined as tokens but can be typed directly in rules
*changed interleave function to be deep, and start on START
*changed position returned in tree to be relative to line numbers instead of the absolute one
 - Did the same for partialresults returned on syntax error change this is error results too
 - TODO check efficiency on the previous point checking the whole text for every position might be slow
*Changed usage , instead of Parser(input, grammar).pars() it is now Parser(grammar).parse(input)
 - Added a self.reset() method for fields that need to be initializes again when parsing a new input
*Changed findFailure and generateErrorReports:
 * i need the the rule/token name as well not only the error text
 * hidden  elements (like for example comments and newline ) are not included in error reports if hide_implicit is set to true
 * same for the interleave rule
"""

import re
from copy import deepcopy
from position import Position


class Tree(object):
    def __init__(self, head, tail, startpos, endpos):
        self.head = head
        self.tail = tail
        self.startpos = startpos
        self.endpos = endpos


class Parser(object):
    class Constants(object):
        Token = 'token'
        Production = 'prod'
        Success = 'success'
        Failure = 'failure'

    class LR(object):
        def __init__(self, seed, rulename, head, nextlr):
            self.seed = seed
            self.rule = rulename
            self.head = head
            self.next = nextlr

    class Head(object):
        def __init__(self, rulename, involved, evaluation):
            self.rule = rulename
            self.involved = involved
            self.evaluation = evaluation

    def __init__(self, grammar, **options):
        """
        creates a Parser for the given grammar
        :param grammar: An instance of the Grammar class
        :param options: the following options are supported:
            tab_size: default 1. sets the character size of a tab character
            hide_implicit: default False. when true implicit tokens are hidden from the returned parse tree and error message.
                           Note that this this option will not override rules or tokens where the hidden variable has already been set manually in the Grammar class
            line_position: default False. when true we use line, column Position object instead of absolute position integer in the parse tree for startpos and endpos
        """
        #changed by Daniel: members that need to be initialized each time parse is a called have been put in def reset()
        #that method is called when the parse() method is called
        self.rules = grammar.rules
        self.tokens = grammar.tokens
        self.implicitList = [] #added by Daniel, set in hideImplict so that we can review the implicit list in case of error messages
        self.implicitRuleName = ""

        #options Added by Daniel
        self.tabsize = int(options.pop('tab_size', 1)) #the character size of a tab
        self.hideImplicit = bool(options.pop('hide_implicit', False))
        #whether to hide implicit tokens and rules from the returned parse tree
        #Important note: this option will not override rules or tokens where the hidden variable has already been set manually
        self.linePosition = bool(options.pop('line_position', False))
        #if true the position of the returned parse tree will consist of a line and a column instead of the position in the string array

        #preprocess must happen after options, (after hideImplicit has been set)
        self.preprocess()

    def reset(self):
        self.input = ""
        self.memotable = {}
        self.failure = {}
        self.lrstack = None
        self.heads = {}
        self.countcard = {}


    def preprocess(self):
        #for elem in self.rules.keys(): #Changed by Daniel: we only check start because it's global
        elem = 'start'
        if elem in self.rules.keys():
            if ('interleave' in self.rules[elem]):
                ilist = self.rules[elem]['interleave']
                self.setHideImplicit(ilist, self.hideImplicit)
                self.interleave(self.rules[elem], ilist)

    def setHideImplicit(self, ilist, bool= False):
        if ilist:
            #ilist = ['?', '@rulename']
            rulename= ilist[1][1:]
            self.implicitRuleName = rulename #used to hide later error reports later
            if rulename in self.rules:
                self.rules[rulename]['hidden'] = bool #the rule itself should also be hidden
                body = self.rules[rulename]['body']
                #body = [*, [| ,,,,]]
                elems= body[1][1:]
                self.implicitList = elems
                for elem in elems:
                    l = None
                    error = ''
                    if elem[0] == '@':
                        l = self.rules
                        error =  ' rule not found in grammar rules.'
                    elif elem[0]== '$':
                        l = self.tokens
                        error =  ' token not found in grammar rules.'
                    #else: in this case it is an anonymous token,

                    if l:
                        name = elem[1:]
                        if name in l:
                            if not l[name].has_key('hidden'):
                                #this method will not override anything the user has explicitly specified in the structure
                                #if there is already a hidden value there it will be kept even if it is not the same one
                                #an examples use case is whitespaces vs comments:
                                #both can appear anywhere in the text and so are implicit in the grammar.
                                #however we dont want spaces in the tree but we do want the comments
                                l[name]['hidden'] = bool
                        else:
                             raise Exception(name + error)
                    #else: Anon token can't be ignored for the  moment unless we create an ignore list for it or something like that.

            else:
                raise Exception(rulename + ' rule not found in grammar rules.')


    def interleave(self, elem, ilist):
        #quick and simple interleaving method, will probably contain double interleaving
        #but this is as simple as i could make it without taking into account each and every case
        def quickInterLeave(lst, inter):
            newL = []
            newL.append(lst[0])
            isSeq = self.isSequence(lst[0])
            for item in lst[1:]:
                if (isinstance(item, list)):#a sublist
                    newL.append(quickInterLeave(item,inter))
                else:
                    if(item[0] == '@'): #rule
                        rulename = item [1:]
                        if rulename in self.rules:
                            rule = self.rules[rulename]
                            if not rule.has_key('visited') or rule['visited'] == False:
                                self.interleave(rule, inter)
                        else:
                            raise Exception(rulename + ' rule not found in grammar rules.')
                    """
                    Else:
                        pass
                    in this case it is a token or anon token we dont need to do anything special,
                    just add it to the list interleaved
                    """

                    if isSeq: # no need to complicate the data structure if the list is a sequence
                        if not newL[-1] == inter:
                            newL.append(inter)
                        newL.append(item)
                        newL.append(inter)
                    else:
                        newL.append(['.', inter,item ,inter])

                        """
                        This way in case the list is not a sequence this doesnt change the meaning of the list:
                        example: t1, t2 are tokens, i is an optional whitespace being intereleaved
                        [., t1, t2] ->  [., i ,t1, i, t2]
                        the meaning stays the same:
                        t1 and t2 both have ot be found for the rule to apply regardless of the ws
                        [|, t1, t2] ->  [|, i ,t1, i, t2]
                        the meaning changed: if i is encountered the or is satisfied:
                        so instead we do ->  [|, [., i ,t1, i,], [., i ,t2, i,]]

                        note that while inter has been added to the data stricture 4 times it will only match
                        for one option so it is not really duplicate.
                        another way of writing this can be [., inter [|, t1, t2], inter ] but this is easier said than
                        done especially for big (complex) data structures
                        """
            return newL

        #the first thing we do is say that the item has been visited this will avoid infinite loop due to recursion
        elem['visited'] = True
        if (not 'body' in elem):
            return

        ls = elem['body']
        newbody = quickInterLeave(ls,ilist)
        elem['body'] = newbody

    def parse(self, text):
        self.reset() #Changed by Daniel receive text as param. instead of once at init so first we reset the fields
        self.input = text
        results = self.applyrule('@start', 0)
        if (results == [] or results[0]['endpos'] < len(self.input)):
            result = self.generateErrorReport()
            for elem in result['partialresults']: #Added by Daniel there was no post processing on partial results. I need it
                if elem['tree']: #with partial results the tree can be None
                    elem['tree'] = Parser.IgnorePostProcessor(self.rules, self.tokens).visit(elem['tree'])
                    if self.linePosition:
                        elem['tree'] = Parser.PositionPostProcessor(self.convertToLineColumn).visit(elem['tree']) #Added by Daniel
        else:
            result = results[0]
            result.update({'status': Parser.Constants.Success})
            if result['tree'].head != 'start':
                result['tree'] = Tree('start', [result['tree']], result['tree'].startpos, result['tree'].endpos)
            result['tree'] = Parser.IgnorePostProcessor(self.rules, self.tokens).visit(result['tree'])
            if self.linePosition: #Added by Daniel
                result['tree'] = Parser.PositionPostProcessor(self.convertToLineColumn).visit(result['tree'])
        return result

    def convertToLineColumn(self, pos):
        line = 1
        column = 0
        l = len(self.input)
        for i in range(0, l):
            if (i > pos):
                break
            if self.input[i] == '\n':
                line += 1
                column = 0
            elif self.input[i] == '\t':
                column += self.tabsize #changed by Daniel: this used to be 4
            else:
                column += 1
        if pos >= l: #the end of the text
            """
            added by Daniel: needed for the case of the last word/character.
            Assume a text on one word 'foo'
            in absolute position the tree says word is from 1 to 4 (as always 'to' means not included)
            in this method we only count until the range so we would return line 1 col 1 to line 1 col 3
            but we need col 4
            we could just says pos == l but i think its better to say any position bigger than the text is simply the end of the text
            """
            column += 1
        return {'line': line, 'column': column}

    def findlargerresultat(self, pos):
        endpos = pos
        result = None
        for key in self.memotable.keys():
            elem = self.memotable[key]
            if (elem == []):
                continue
            if (elem[0]['startpos'] == pos and endpos < elem[0]['endpos']):
                endpos = elem[0]['endpos']
                result = elem[0]
        return result

    def generateErrorReport(self):
        # consult the memotable and collect contiguities until endpos
        endpos = len(self.input) - 1
        pos = 0
        elems = []
        while pos <= endpos:
            elem = self.findlargerresultat(pos)
            if (not elem or (elem and elem['endpos'] == pos)):
                break
            pos = elem['endpos']
            elems.append(elem)
        if (pos <= endpos):
            elems.append({'tree': None, 'startpos': pos, 'endpos': endpos})

        elem = self.getFirstBiggestSpan(elems)

        reasons = self.findFailure(elem['startpos'], elem['endpos'])
        if (reasons == []):
            pos -= 1
        else:
            pos = reasons[0]['startpos']
        read = self.input[pos:pos + 1]
        linecolumn = self.convertToLineColumn(pos)
        message = 'Syntax error at line ' + str(linecolumn['line']) + ' and column ' + str(linecolumn['column']) + '. '
        keys = []
        if (not reasons == []):
            first = True
            for reason in reasons:
                if (first):
                    message += 'Expected \'' + reason['text'] + '\''
                    first = False
                else:
                    message += ' or \'' + reason['text'] + '\''
                keys.append(reason['key'])
            message += '. Instead read: \'' + read + '\'.'
        else:
            message += 'Read: \'' + read + '\'.'

        return {'status': Parser.Constants.Failure, 'line': linecolumn['line'], 'column': linecolumn['column'],
                'text': message, 'partialresults': elems, 'grammarelements': keys, 'pos': pos}

    def getFirstBiggestSpan(self, elems):
        biggestspan = 0
        result = None
        for elem in elems:
            span = elem['endpos'] - elem['startpos']
            if (biggestspan < span):
                result = elem
                span = biggestspan
        return result

    def findFailure(self, pos, endpos):
        posreasons = []
        endposreasons = []

        #changed by Daniel:
        #* i need the key as well for autocomplete so in stead of appending elem i return a new dictionary with elem and the key inside
        #* checks both condition for posreasons and endposreasons in one for loop instead of 2
        #* do not cosider keys that are hidden


        for key in self.failure.keys():
            #keys are given starting either with $ for tokens or @ for rules
            #howver with the the given metagrammar Tokens are all caps and rules are all in small letters so there cant be an overlapp
            #and we can safely test both
            if ((self.hideImplicit and (('$' + key in self.implicitList) or ('@' + key in self.implicitList)
                or (key == self.implicitRuleName))) or (key in ['*','|','+','?','#'])
                or (key in self.rules)): #remove rulenames from error messages
                continue
            else:
                elem = self.failure[key]
                if (elem['startpos'] == pos and not elem['text'] == ''):
                    posreasons.append({'key': key, 'startpos': elem['startpos'] , 'text': elem['text'] })

                if (elem['startpos'] == endpos and not elem['text'] == ''):
                    endposreasons.append({'key': key, 'startpos': elem['startpos'] , 'text': elem['text'] })

        if (len(endposreasons) < len(posreasons)):
            return posreasons
        else:
            return endposreasons

    def setupLR(self, rule, elem):
        if (elem.head == None):
            elem.head = Parser.Head(rule, [], [])

        s = self.lrstack
        while s and not s.rule == elem.head.rule:
            s.head = elem.head
            if (not s.rule in elem.head.involved):
                elem.head.involved.append(s.rule)
            s = s.next

    def recall(self, rule, j):
        newresults = []
        if ((rule, j) in self.memotable):
            newresults = self.memotable[(rule, j)]

        h = None
        if (j in self.heads):
            h = self.heads[j]
        if (not h):
            return newresults

        if (newresults == [] and not rule in (h.involved + [h.rule])):
            return []  # [{'tree': [], 'startpos': j, 'endpos': j}]

        if (rule in h.evaluation):
            h.evaluation.remove(rule)
            newresults = self.eval(rule, j)
            self.memotable.update({(rule, j): newresults})

        return newresults

    def applyrule(self, rule, j):
        overallresults = []

        newresults = self.recall(rule, j)
        if (not newresults == []):
            memoresults = []
            for elem in newresults:
                if (isinstance(elem['tree'], Parser.LR)):
                    self.setupLR(rule, elem['tree'])
                    memoresults += elem['tree'].seed
                else:
                    overallresults.append(elem)
            if (not memoresults == []):
                self.memotable.update({(rule, j): memoresults})
                return memoresults
            return overallresults
        else:
            lr = Parser.LR([], rule, None, deepcopy(self.lrstack))
            self.lrstack = lr
            self.memotable.update({(rule, j): [{'tree': lr, 'startpos': j, 'endpos': j}]})

            newresults = self.eval(rule, j)
            self.lrstack = self.lrstack.next

            memoresults = []
            if ((rule, j) in self.memotable):
                memoresults = self.memotable[(rule, j)]
            for melem in memoresults:
                if (isinstance(melem['tree'], Parser.LR) and melem['tree'].head):
                    melem['tree'].seed = newresults
                    r = self.lr_answer(rule, j, melem)
                    if (not r == []):
                        overallresults += r
            if (overallresults != []):  # prefer grown results
                return overallresults

            self.memotable.update({(rule, j): newresults})
            return newresults

    def lr_answer(self, rule, pos, melem):
        h = melem['tree'].head
        if (not h.rule == rule):
            return melem['tree'].seed
        else:
            melems = melem['tree'].seed
            result = []
            for melem_i in melems:
                if (not melem_i['tree'] == None):
                    result.append(melem_i)
            if (result == []):
                return []
            else:
                newresult = []
                for melem_i in result:
                    newresult.append(self.growLR(rule, pos, melem_i, h))
                return newresult

    def growLR(self, rule, pos, melem, head=None):
        self.heads.update({pos: head})
        while (True):
            overallresults = []
            head.evaluation = deepcopy(head.involved)
            newresults = self.eval(rule, pos)
            for elem in newresults:
                if (elem['endpos'] > melem['endpos']):
                    melem = elem
                    overallresults.append(elem)
            if (overallresults == []):
                self.heads.update({pos: None})
                return melem
            self.memotable.update({(rule, pos): overallresults})

    def eval(self, rulename, j):

        if (not rulename.startswith('@') and
                not rulename.startswith('$')):
            #raise Exception('Plain terminals not allowed inside grammar rules: ' + str(rulename))
            #we create an anonymous token rule
            # we can write whatever we want as fake type as long as it is not equal to the type of the prodcution rule
            #or to that of the token
            rule = { 'type' : 'anonymous_token' }

        if (rulename[0] == '@'):
            rulename = rulename[1:]
            if (not rulename in self.rules):
                raise Exception(rulename + ' rule not found in grammar rules.')
            rule = self.rules[rulename]

        if (rulename[0] == '$'):
            rulename = rulename[1:]
            if (not rulename in self.tokens):
                raise Exception(rulename + ' token not found in grammar tokens.')
            rule = self.tokens[rulename]

        if (self.isType(rule, Parser.Constants.Production)):
            newresults = []
            results = self.eval_body(rulename, rule['body'], j)
            for r in results:
                if (r['tree']):
                    head = r['tree'].head
                    if(head == '*' or head == '+' or head == '?' or head == '|'):
                        newr = {'tree': Tree(rulename, [r['tree']], r['startpos'], r['endpos']), 'startpos': r['startpos'],
                         'endpos': r['endpos']}
                        r = newr
                newresults.append(r)
        elif (self.isType(rule, Parser.Constants.Token)):
            newresults = self.term(rulename, j)
        else: ##Changed by Daniel: if not a production rule or defined token we try an anonymous token:
            newresults = self.anonTerm(rulename, j)
        return newresults

    def eval_body(self, rulename, ls, j):
        if (self.isAlternative(ls[0])):
            return self.alt(rulename, ls[1:], j)
        elif (self.isSequence(ls[0])):
            return self.seq(rulename, ls[1:], j)
        elif (self.isOptional(ls[0])):
            return self.opt(rulename, ls[1:], j)
        elif (self.isMany(ls[0])):
            return self.many(rulename, ls[1:], j)
        elif (self.isMore(ls[0])):
            return self.more(rulename, ls[1:], j)
        elif (self.isCard(ls[0])):
            return self.card(rulename, ls[0][1:], ls[1:], j)
        raise Exception('Unrecognized grammar expression: ' + str(ls[0]))

    def isSequence(self, operator):
        return operator == '.'

    def isAlternative(self, operator):
        return operator == '|'

    def isMany(self, operator):
        return operator == '*'

    def isCard(self, operator):
        return operator.startswith('#')

    def isMore(self, operator):
        return operator == '+'

    def isOptional(self, operator):
        return operator == '?'

    def isType(self, rule, oftype):
        if (rule['type'] == oftype):
            return True

    def term(self, rulename, j):
        if (j >= len(self.input)):
            errortext = ''
            if (rulename in self.tokens and 'errortext' in self.tokens[rulename]):
                errortext = self.tokens[rulename]['errortext']
            self.failure.update({rulename: {'startpos': j, 'text': errortext}})
            return []

        rule = self.tokens[rulename]
        mobj = re.match(rule['reg'], self.input[j:])
        #Changed by daniel instead of re.match(reg) did re.match(re.compile(reg).patern)
        #this is to avoid problems with \ before i did this i had the match the character \ by doing [\\\\]
        # because to write only two slashes it would have to be r'[\\]' which cant be done directly in hte grammar so it had to be in string form
        #this way reading [\\] will be interpreted correctly instead of giving an error like it used to
        if (not mobj):
            # this is a failure! nice to register!
            self.failure.update({rulename: {'startpos': j, 'text': self.tokens[rulename]['errortext']}})
            return []
        return [{'tree': Tree(rulename, [mobj.group()], j, j + mobj.end()), 'startpos': j, 'endpos': j + mobj.end()}]

    def anonTerm(self, term, j):
        """
        #Changed by Daniel: added this whole method.
        Anonymous term to allow for direct terminals in rules
        (write 'Foo' directly instead of having to deine a FOO token)
        """
        name = term
        if (j >= len(self.input)):
            self.failure.update({ name : {'startpos': j, 'text': name}})
            return []

        mobj = re.match(term, self.input[j:])
        if (not mobj):
            # this is a failure! nice to register!
            self.failure.update({ name : {'startpos': j, 'text': name }})
            return []
        return [{'tree': Tree(name , [mobj.group()], j, j + mobj.end()), 'startpos': j, 'endpos': j + mobj.end()}]

    def many(self, rulename, ls, j):

        rule_i = ls[0]
        if (isinstance(rule_i, list)):
            results = self.eval_body('*', rule_i, j)
        else:
            results = self.applyrule(rule_i, j)

        if (results == []):
            return [{'tree': None, 'startpos': j, 'endpos': j}]

        seq = ['.'] + ls + [['*'] + ls]

        results = self.eval_body('*', seq, j)
        overall_results = []
        for r in results:
            if (r['tree']):
                if (len(r['tree'].tail) > 1):
                    left = r['tree'].tail[0]
                    right = r['tree'].tail[1].tail
                    r['tree'].tail = [left] + right
                overall_results.append(r)


        return overall_results

    def more(self, rulename, ls, j):

        rule_i = ls[0]
        if (isinstance(rule_i, list)):
            results = self.eval_body('+', rule_i, j)
        else:
            results = self.applyrule(rule_i, j)

        if (results == []):
            return []

        seq = ['.'] + ls + [['*'] + ls]

        results = self.eval_body('+', seq, j)
        overall_results = []
        for r in results:
            if (r['tree']):
                if (len(r['tree'].tail) > 1):
                    left = r['tree'].tail[0]
                    right = r['tree'].tail[1].tail
                    r['tree'].tail = [left] + right
                overall_results.append(r)

        return overall_results

    def opt(self, rulename, ls, j):
        if (j >= len(self.input)):
            errortext = ''
            if (rulename in self.rules and 'errortext' in self.rules[rulename]):
                errortext = self.rules[rulename]['errortext']
            else:
                for item in ls:
                    if (item[1:] in self.rules):
                        errortext = self.rules[item[1:]]['errortext']
            self.failure.update({rulename: {'startpos': j, 'text': errortext}})
            return [{'tree': None, 'startpos': j, 'endpos': j}]

        results = []
        rule_i = ls[0]
        if (isinstance(rule_i, list)):
            results = self.eval_body('?', rule_i, j)
        else:
            results = self.applyrule(rule_i, j)

        if (not results == []):
            return results

        # empty case
        return [{'tree': None, 'startpos': j, 'endpos': j}]

    def card(self, rulename, cardrule, ls, j):
        count = 0
        delta = 1
        #  a# a#(-1) #indent, #(-1)indent
        group = re.match('\((?P<delta>[-+]?\d+)\)(?P<rule>\S+)',cardrule)

        if(group):
            cardrule = group.group('rule')
            delta = int(group.group('delta'))

        if (not cardrule in self.countcard):
            count = delta
            self.countcard.update({cardrule: {j: count}})
        else:
            if not j in self.countcard[cardrule]:  # # if we already know the count for j, then ignore..
                d = self.countcard[cardrule]
                lastcount = 0
                for i in range(0, j):
                    if i in d:
                        lastcount = d[i]
                count = lastcount + delta
                d.update({j: count})
            else:
                count = self.countcard[cardrule][j]

        results = []
        rule_i = '@' + cardrule
        for i in range(0, count):
            if (results == []):
                if (isinstance(rule_i, list)):
                    newresults = self.eval_body(rulename, rule_i, j)
                else:
                    newresults = self.applyrule(rule_i, j)
                if (newresults == []):
                    del self.countcard[cardrule][j]
                    return []
                newresults = self.merge(rulename, newresults, {'startpos': j, 'endpos': j})
            else:
                for elem_p in results:
                    if (isinstance(rule_i, list)):
                        newresults = self.eval_body(rulename, rule_i, elem_p['endpos'])
                    else:
                        newresults = self.applyrule(rule_i, elem_p['endpos'])
                    if (newresults == []):
                        del self.countcard[cardrule][j]
                        return []
                    newresults = self.merge(rulename, newresults, elem_p)
            results = newresults

        for rule_i in ls:
            for elem_p in results:
                if (isinstance(rule_i, list)):
                    newresults = self.eval_body(rulename, rule_i, elem_p['endpos'])
                else:
                    newresults = self.applyrule(rule_i, elem_p['endpos'])
                if (newresults == []):
                    del self.countcard[cardrule][j]
                    return []
                newresults = self.merge(rulename, newresults, elem_p)
                results = newresults

        del self.countcard[cardrule][j]
        return results

    def seq(self, rulename, ls, j):
        results = []
        for rule_i in ls:
            if (results == []):
                if (isinstance(rule_i, list)):
                    newresults = self.eval_body(rulename, rule_i, j)
                else:
                    newresults = self.applyrule(rule_i, j)
                if (newresults == []):
                    return []
                newresults = self.merge(rulename, newresults, {'startpos': j, 'endpos': j})
            else:
                for elem_p in results:
                    if (isinstance(rule_i, list)):
                        newresults = self.eval_body(rulename, rule_i, elem_p['endpos'])
                    else:
                        newresults = self.applyrule(rule_i, elem_p['endpos'])
                    if (newresults == []):
                        return []
                    newresults = self.merge(rulename, newresults, elem_p)
            results = newresults
        return results

    def merge(self, rulename, newres, elem_p):
        results = []
        for elem_n in newres:
            tail = []
            if ('tree' in elem_p and elem_p['tree']):
                tail += elem_p['tree'].tail
            if ('tree' in elem_n and elem_n['tree']):
                tail.append(elem_n['tree'])
            value = {'tree': Tree(rulename, tail, elem_p['startpos'], elem_n['endpos']), 'startpos': elem_p['startpos'],
                     'endpos': elem_n['endpos']}
            results += [value]
        return results

    def alt(self, rulename, ls, j):
        overall_results = []
        results = []
        for rule_i in ls:
            if (isinstance(rule_i, list)):
                newresults = self.eval_body('|', rule_i, j)
            else:
                newresults = self.applyrule(rule_i, j)
            overall_results += newresults

        return overall_results

    class IgnorePostProcessor(object):
        def __init__(self, rules, tokens):
            self.rules = rules
            self.tokens = tokens

        def inner_visit(self, tree):
            results = []
            if (isinstance(tree, Tree)):
                if (self.isHidden(tree.head)):
                    for item in tree.tail:
                        ivlist = []
                        ivresult = self.inner_visit(item)
                        for elem in ivresult:
                            if (isinstance(elem, Tree)):
                                ivlist += [elem]
                        results += ivlist
                else:
                    tlist = []
                    for item in tree.tail:
                        tlist += self.inner_visit(item)
                    tree.tail = tlist
                    results += [tree]
                return results

            return [tree]

        def visit(self, tree):
            # start cannot be hidden
            tlist = []
            for item in tree.tail:
                tlist += self.inner_visit(item)
            tree.tail = tlist
            return tree

        def isHidden(self, head):
            if (head == '*' or head == '+' or head == '?' or head == '|'):
                return True
            if (head in self.rules):
                return 'hidden' in self.rules[head] and self.rules[head]['hidden']
            elif (head in self.tokens): #Changed by Daniel: added elif condition and return false otherwise, need for anon tokens
                return 'hidden' in self.tokens[head] and self.tokens[head]['hidden']
            else:
                return False

    class PositionPostProcessor(object):
        """
        This post processor changes absolute position (place in the parsed string )to a line, column position
        added by Daniel
        """
        """
        efficiency note:
        how effective is this. this might be slowing things down quit a bit having to calculate that for everything
        1) an alternative would be use the method only for the leaves, and that traverse the tree bottom up to  create
        the interval using the left most and right most children of each subtree. but since tat involves extra tree
        traversal that might not help that much.

        2) another thing that might improve efficiency is to create change the position calculating method:
        create one that doesnt scan the whole text for new line each time we calculate a position,
        but creates a table of them the first time.
        we can calculate the line by returning the index in the table of the the new line the closest to the given
        position and the column is the difference between the position of that newline and the column (maybe + or - 1,
        check that)
        in case this method doesn't slow things down too much ignore this
        """
        def __init__(self, method):
            self.calcPosMethod = method

        def inner_visit(self,tree):
            startDic = self.calcPosMethod(tree.startpos)
            endDic = self.calcPosMethod(tree.endpos)
            tree.startpos = Position(startDic["line"], startDic["column"])
            tree.endpos =  Position(endDic["line"], endDic["column"])
            for item in tree.tail:
                if (isinstance(item, Tree)):
                    self.inner_visit(item)

        def visit(self, tree):
            if tree:
                self.inner_visit(tree)
            return tree


    class DefaultPrinter(object):
        def __init__(self, output='console'):
            self.outputStream = ''
            self.output = output

        def inner_visit(self, tree):
            for item in tree.tail:
                if (isinstance(item, Tree)):
                    self.inner_visit(item)
                else:
                    self.outputStream += item

        def visit(self, tree):
            self.inner_visit(tree)
            if (self.output == 'console'):
                print self.outputStream

    class PrettyPrinter(object):
        def __init__(self, output='console'):
            self.outputStream = ''
            self.output = output
            self.tabcount = -1

        def tab(self):
            tabspace = ''
            for i in range(0, self.tabcount):
                tabspace += '    '
            return tabspace

        def inner_visit(self, tree):
            self.tabcount += 1
            self.outputStream += self.tab()
            self.outputStream += 'node ' + tree.head + ':\n'
            for item in tree.tail:
                if (isinstance(item, Tree)):
                    self.inner_visit(item)
                else:
                    self.tabcount += 1
                    self.outputStream += self.tab() + item + ' @' + str(tree.startpos) + ' to ' + str(
                        tree.endpos) + ' \n'
                    self.tabcount -= 1
            self.tabcount -= 1

        def visit(self, tree):
            self.inner_visit(tree)
            if (self.output == 'console'):
                print self.outputStream