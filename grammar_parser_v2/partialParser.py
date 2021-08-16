"""
This is an adaptation of Bruno Barroca's hutnparser
The goal is to create a parser that given a list of partial results fuses them together.
and retuns the first tree that matches every result in the list.

Note that on the precondition that the partial results were obtained from the hutnparser there will always be a tree that covers everything
even if the tree is in fact incomplete.because the partial results returned are always up to the point were stuff were matched
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

    def reset(self):
        self.inputList = ""
        self.memotable = {}
        self.failure = {}
        self.lrstack = None
        self.heads = {}
        self.countcard = {}

    def parse(self, partialResults):
        self.reset() #Changed by Daniel receive text as param. instead of once at init so first we reset the fields
        self.inputList = partialResults
        results = self.applyrule('@start', 0)

        if (results == [] or results[0]['endpos'] < len(self.inputList)):
            print "Something unexpected happened, there should be a result"
        else:
            result = results[0]
            result.update({'status': Parser.Constants.Success})
            if result['tree'].head != 'start':
                result['tree'] = Tree('start', [result['tree']], result['tree'].startpos, result['tree'].endpos)
            result['tree'] = Parser.IgnorePostProcessor(self.rules, self.tokens).visit(result['tree'])
            #if self.linePosition: #Added by Daniel
            #    result['tree'] = Parser.PositionPostProcessor(self.convertToLineColumn).visit(result['tree'])
        return result

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
        if (j >= len(self.inputList)):
            errortext = ''
            if (rulename in self.tokens and 'errortext' in self.tokens[rulename]):
                errortext = self.tokens[rulename]['errortext']
            self.failure.update({rulename: {'startpos': j, 'text': errortext}})
            return []

        rule = self.tokens[rulename]
        mobj = re.match(rule['reg'], self.inputList[j:])
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
        qt = '\''
        name = qt + term + qt
        if (j >= len(self.inputList)):
            self.failure.update({ name : {'startpos': j, 'text': name}})
            return []

        mobj = re.match(term, self.inputList[j:])
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
        if (j >= len(self.inputList)):
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