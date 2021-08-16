from hutnparser import  Parser, Tree
from position import  Position
from copy import deepcopy
from visitors.postitionVisitor import PositionVisitor

class RuleTree(object):

    def __init__(self, name = None , prod = [], parent = None, parentIndex = -1):
        """
        :param name: The name of the rule. only fill in if part of the Parse tree. if it is a subrule give this value None
        :param prod: The production rule associate with the (sub)Rule
        :param parent: parent of the current rule or None if no parent
        :param parentIndex: the index this child has in the parent or -1 if no Parent
        """
        self.name = name #name of the rule  #Name of the Rule
        self.isSubRule = (self.name == None) # True if is subRule (a list within a rule) , False if this is a rule (part of the pars tree)
        self.parent = parent
        self.production = prod #the prodction rule itself
        self.currentIndex = -1 #current index in the tail #the current index we are checking
        self.partIndex = -1 #the index that we are currently going to check
        self.operator = self.getCurrentOperator(prod) #the operator of the (sub)rule
        self.parentIndex = parentIndex #the index of the rule in the parent
        self.children = [] #the subRules or actual rule children
        self.extra = {} #save extra info needed here , such as if the rule was a + was it al least found once ?

        if self.isSubRule:
            self.name = self.parent.name + '_@child' + str(parentIndex)

    def getCurrentOperator(self, l):
        ret = ""
        if isinstance(l, list):
            oper = l[0]
            if oper in [".","+","*","?", "|"]:
                ret = oper
                self.currentIndex = 1
            elif oper.startswith("#"):
                ret = "#"
                self.currentIndex = 0 #we need to check if the rule or token that is directly after the cardinality operator is also matched
        return ret


    """
    def getPath(self):
        p = ""

        if self.currentIndex != -1:
            prod = self.production[self.currentIndex]
            if isinstance(prod,basestring):
                p =  prod[1:]

        temp = self
        while temp:
            t = ''
            if not temp.isSubRule:
                t = temp.name
            else:
                prod = temp.parent.production[temp.parentIndex]
                if not isinstance(prod,list):
                    t = prod[1:]
            if t:
                if p:
                    p = t + '.' + p
                else:
                    p = t


            temp = temp.parent

        return p
    """

    def __eq__(self, other):
        ret = False
        if isinstance(other, RuleTree):
            ret = ( (self.name == other.name) and
                    (cmp(self.production, other.production) == 0) and
                    self.currentIndex == other.currentIndex and
                    self.partIndex == other.partIndex
                  )
        return ret

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        if not self.isSubRule:
            text = "<RuleTree " + self.name + " :"
        else:
            text = "<Subrule : "
        text += str(self.production)
        text += " at index " + str(self.currentIndex) +"(" + str(self.production[self.currentIndex]) + ")>"
        return text

class PartialTreeFuser(object):

    def __init__(self):
        self.implicitName = ''
        self.implicitList = []
        self.grammarInstance = None
        self.partList = []
        self.memoList = [] #a list of RuleTree that have been added to be checked already , so that we never check the same alternative twice for a single partial tree
        self.stopIndex = -1 #the index where we need to stop applying the rule at

        self.toMatchList = [] #the list we are examining

    def __ishiddenValue(self,val):
        hidden = False
        if ('$' + val) in self.implicitList:
            """
            for partial fusing we ignore een non hidden implictits
            as they do not matter and we will most likely get the grammar withouth interleaving as input

            if 'hidden' in self.grammarInstance.tokens[val]:
                if self.grammarInstance.tokens[val]["hidden"]:
                    hidden = True #there is a hidden setting and it is set to True
                else:
                    hidden = False #hidden setting is set to False. for example comments are implict but not hidden
            else:
                hidden = True #if there is no hidden param and in it is in the implict list it is considered hidden
            """
            hidden = True #no matter wheter hidden is set to true or not if it is implict it is diregarded here
        elif (val == self.implicitName):
            hidden = True
        return hidden

    def __preProcessPartials(self, partialList):
        #partial trees will always show the root even if it is something that should be hidden
        pList = []
        if partialList:
            if self.implicitList:
                for tree in partialList:
                    if tree and not self.__ishiddenValue(tree.head):
                        #a token can be in implict and not hidden (= comment)
                        if tree.head in ['|','*','?','+','.', "|"]: #if it is an operator we add the children seperatly to the list
                            if tree.tail:
                                for child in tree.tail:
                                    pList.append(child)

                        else:
                            pList.append(tree)
            else:
                for partial in partialList:
                    tree = partial['tree']
                    if tree:
                        pList.append( tree )
        return pList

    def __getHierarchy(self, parseTree):
        path = ''
        child = parseTree
        stop = False
        temp = None
        while child and not stop:
            if child.tail:
                temp = child.tail[-1]
                if not isinstance(temp,basestring):
                    setattr(temp,"parent", child)
                    child = temp
                else:
                    stop = True
            else:
                stop = True
        #now child is the most right child of the parseTree
        if child:
            path = child.head
            parent = child.parent
            while parent:
                path = parent.head + '.' + path
                parent = parent.parent
        return path

        #h = parseTree.head
        #parent = parseTree.parent
        #while parent:
        #    parseTree = parseTree.parent
        #    h = parseTree.head +'.' + h
        #    parent = parseTree.parent
        #return h


    def getRulesForStartTree(self):

        retValue = False

        firstTree = self.partList[0]
        setattr(firstTree, 'parent', None)
        firstTree = Tree("start",[] ,Position(-1,-1), Position(-1,-1))

        setattr(firstTree, 'parent', None)
        curRule = RuleTree('start', self.grammarInstance.rules['start']['body'])
        curRule.partIndex = 0 #we start matching with the first element of the lis

        self.stopAlternativesOnceFound = False #here we add every alternative once the tree has been matched so that we may continue later
        self.toMatchList.append((curRule,firstTree))
        self.memoList.append(curRule)

        toMatch = None
        stopBool = False

        temp = self.partList #we save the original partList for later
        self.partList  = self.__preProcessPartials(self.partList[0].tail) #and replace it by the children of the start rule
        self.stopIndex = len(self.partList)

        while self.toMatchList and not stopBool:
            toMatch = self.toMatchList[-1]
            if toMatch[0].partIndex < self.stopIndex:
                self.toMatchList = self.toMatchList[:-1]
                self.checkRule(toMatch[0], toMatch[1])
            else:
                stopBool = True
                self.stopAlternativesOnceFound = True #we indicate that as soon as a compatible parse tree is found we stop
                self.memoList = [] #evrything is reset
                self.partList = temp #partList is back to the original one

                tempList = []
                self.toMatchList.reverse()

                i = 0
                while i < len(self.toMatchList): #weextract all alternatives for the
                    if self.toMatchList[i][0].partIndex >= self.stopIndex:
                        self.toMatchList[i][0].partIndex = 1 #partIndex 0 is the one with the start rule we will check from this one
                        tempList +=  [self.toMatchList[i]] + tempList #we add the beginning
                        self.memoList.append(self.toMatchList[i][0])
                        i += 1
                    else:
                        i = len(self.toMatchList) #results with the wanted partial index will be sequential
                self.toMatchList = tempList #the match list is filled with whatever rules can be matched from the enf of the start rule
                self.stopIndex = len(self.partList) #the stopIndex is reset to the len of the original list
                retValue = (len(self.toMatchList) > 0) #there should be at least one alternative


        return retValue


    def fuse(self,partialList, grammarInstance, implicitRuleName="", modelNameRule=""):
        """
        A naive method that takes partial results and turns them into a one tree
        according to its best guess
        :param partialList: a list of Tree: the partial results we are trying to merge
        :param grammarInstance: the instance of the grammar we are using to reconstruct partial results
        :param implRuleName: the name of the rule that contains the implicitList
        :return: a Tree
        """
        self.grammarInstance = grammarInstance
        self.implicitName = implicitRuleName
        self.implicitList = []
        if self.implicitName and self.implicitName in self.grammarInstance.rules:
            body = self.grammarInstance.rules[self.implicitName]['body']
            #body = [*, [| ,,,,]]
            self.implicitList= body[1][1:]
        self.stopAlternativesOnceFound = True
        self.modelNameRule = modelNameRule

        #first remove any empties and implicit names
        tempPartList = []
        for partial in partialList:
            tempPartList.append(partial['tree'])
        self.partList = self.__preProcessPartials(tempPartList)
        self.stopIndex = len(self.partList)

        curRule = None
        retTree = None
        retArr = []
        if self.partList:
            if len(self.partList) > 1:
                #TODO REMOVE THIS
                #print "Partial trees to be analyzed are:\n"
                #for pTree in self.partList:
                #    Parser.PrettyPrinter().visit(pTree)

                #first we check if the first tree starts with a start rule
                hasStartResult = False
                if self.partList[0].head == "start":
                    hasStartResult = self.getRulesForStartTree()
                    if not hasStartResult:
                        retTree = self.partList[0]
                else:
                    retTree = Tree("start",[] ,Position(-1,-1), Position(-1,-1))
                    setattr(retTree, 'parent', None)
                    curRule = RuleTree('start', self.grammarInstance.rules['start']['body'])
                    curRule.partIndex = 0 #we start matching with the first element of the list
                    self.toMatchList.append((curRule,retTree))
                    self.memoList.append(curRule)
                    hasStartResult = True

                #first we fill start directly as much as possible, then we try to find children rule who fit into it.
                #the idea is the following:
                #all partial results fit into a tree (albeit incomplete), this is because it stops at the syntax error
                #so at the beginning we can try to fit everythin in the start rule until it is no longer a direct child


                stopBool = False
                if hasStartResult:
                    toMatch = None
                    while self.toMatchList and not stopBool:
                        toMatch = self.toMatchList[-1]
                        #if self.__getHierarchy(toMatch[1]) != self.modelNameRule and  toMatch[0].partIndex < self.stopIndex:
                        if toMatch[0].partIndex < self.stopIndex and not (self.modelNameRule in self.__getHierarchy(toMatch[1])):
                            #print "HIERARCHY" , self.__getHierarchy(toMatch[1])
                            #print "PATH", toMatch[0].getPath()
                            self.toMatchList = self.toMatchList[:-1]
                            self.checkRule(toMatch[0], toMatch[1])
                        else:
                            stopBool = True
                            #retTree = toMatch[1]
                            retArr.append(toMatch[1])
                            for i in range(toMatch[0].partIndex, self.stopIndex):
                                retArr.append(self.partList[i])


                if not stopBool:
                    print "Error Parse tree wasn't completely fused. This should not have happend"
                    #TODO return the biggest partial tree there is (rither form memotable or from things left to check)
                    #and return the rest the biggest partial tree is the partial tree whose partIndex is the biggest (as in already ahs the most partial trees insde)
                    #return the firstone encountered (tehre will proabably be more with the same result,) and than return from pList starting from partIndex


                if retArr:
                    ret = retArr[0]#retTree has no attribute parent by default but it was added while creating the tree
                    parent = ret.parent
                    while parent:
                        ret = ret.parent
                        parent = ret.parent

                    ret = PositionVisitor().visit(ret)
                    retArr[0] = ret

            elif len(self.partList) == 1: #in a case where there is extra text after a legal end the partial result will be a single full parse tree
                #retTree = self.partList[0]
                retArr = self.partList
        return retArr

    def getNextIndex(self, ruleTree, partialIndex, parseTree, found = True, isOR = False):
        """
        Get the next possible rules to check.
        PRECONDITION: only call this method in situation where it is legal to find a next TERM (use find alternative for rules or lists)
        :param ruleTree: a RuleTree. the current rule being inspected, the one we want to find the next of
        :param partialIndex: the index of the partial that the new ruleTree(s) should check
        :param parseTree: the parse tree to which the partial who matches the returned rule should be appended
        :param found: boolean. if this is the end of a sequence it indicates it was succefully found in its entirety.
        note that if something is optional found can be set to true even if not found
        :param isOR: boolean. if we are looking for the next after an OR rule we do not want the direct next child because this is another OR we want the next of the parent
        :return: a list of tuples (ruleTree, parseTree).
        IMPORTANT: ruleTree member values will be changed ! if not desirable give a deepcopy of ruleTree as a parameter
        IMPORTANT: found only has meaning in limited cases (like last elements of sequences) this method assumes it has been called in legal sitautions
        so even if not found we can return alternatives
        """
        ret = []

        #TODO should this realy be checked here ?
        if found and ruleTree.operator == "#" and ruleTree.currentIndex == 0:
            ret.append( (deepcopy(ruleTree), deepcopy(parseTree)) )

        if not isOR and (ruleTree.currentIndex + 1 < len(ruleTree.production)):
            #in case of an OR we do not want the direct next child because it is another OR alternative
            #we will check this alternative but only if the continuation of this one doesnt work so it is checked separetly

            ruleTree.currentIndex +=1 #most basic case, next element on the same level
            #we stay on the same level so the parse tree stays the same as well
            ret.append( (deepcopy(ruleTree), deepcopy(parseTree)) )

        else: #this level is finished we try the parent and so on until we find a next
            parent = ruleTree.parent
            stop = False
            while parent and not stop:
                #TODO should there also be a case for # here (if parent index == 0 and parent.operator == # )
                #but it think that that cardinals can only be applied to tokens not sure, TODO ask Bruno
                index = ruleTree.parentIndex

                if parent.operator == '+': #if the parent operator is a +and we are in this else this means we are automatically at the end of a list
                    #because + can only have + can only have one direct element (that leemtn can be a list with sequence operator)
                    #meaning that if we somehow get here even with the while it was always because we were at the end of a rule/list (=subrule)

                    #if the value is already there do not change it. if it was found originally its ok it wasn't found now.
                    #if it wasn't found originally it should not be set now because + should match the first one at the very least
                    if not ("+Matched" in parent.extra):
                        parent.extra["+Matched"] = found #if the last item was fount the whole thing was found
                        #print "SET +MATCHED IN SETNEXT INDEX" #TODO REMOVE THIS PRINT AND ELSE
                    else:
                        pass
                        #print "DID NOT NEED TO SET +MATCHEDBECAUSE IT WAS ALREADY MATCHED"

                if found and parent.operator == '|': #note that this is note the same as isOr this means an ancestor of the current sequence is an OR while isOr means the current one is an OR
                    #we only overwrite if found. if not found but a previous one was found this can stary found and if nothing was found this will never be set
                    parent.extra["|Matched"] = True

                if (ruleTree.operator == '|') and \
                        (("|Matched" not in ruleTree.extra) or (not ruleTree.extra["|Matched"])) :
                    #basically if we are here that means we are at the end of a sequnece, if OR wasnt found than none of them were found.
                    #we need to stop, there are no valid alternatives. alt least one OR choice needs to match
                    ret = []
                    break

                if not ruleTree.isSubRule:
                    #if the current rule tree is a rule the fact that we go one up means going one up in the parse tree
                    parseTree = parseTree.parent

                if ( (parent.operator != '|' or  (parent.operator == '|' and ("|Matched" in parent.extra) and parent.extra["|Matched"]))
                    and   ((index + 1) < len(parent.production)) ):
                    #we try the next child of the parentTree
                    stop = True #normal case we need to stop now

                    if parent.operator == '|':
                        stop = False #if the parent is an OR then index+1 is a next or-option hoewever if one was already matched we need to try the next ancestors child so we cant stop

                    ruleTree = ruleTree.parent
                    parent = ruleTree.parent
                    ruleTree.currentIndex = index + 1
                    ret.append( (deepcopy(ruleTree), deepcopy(parseTree)) )
                else:
                    #we try the whole parent again if the end has been reached and the sequnece was succefully matcehd
                    if parent.operator in ["+","*"]:
                        #note that found must not be true for this for example [* [. foo  [+bar] ]]
                        #if the partial input is foobarfoo after we read bar for the first time we will try again it will fail but we can return to foo even if it wasnt found
                        newParent = deepcopy(parent)
                        newParent.currentIndex = 1 #actaullt im pretty sure in this case it is already 1 but jsut to maek sure
                        ret.append( (newParent, deepcopy(parseTree)) )

                    ruleTree = ruleTree.parent
                    parent = ruleTree.parent

        for rule, parse in ret:
            rule.partIndex = partialIndex
        return ret

    def getOptionalNotFoundAlternative(self, ruleTree, partialIndex, parseTree):
        """
        This method provides an alternative to the current Rule part.
        The idea is to regard the current rule part as optional and not matched
        and simply get the next rule parts that need to be tried
        :param ruleTree: a RuleTree. the current rule being inspected, the one we want to find the next of
        :param partialIndex: the index of the partial that the new ruleTree(s) should check
        :param parseTree: the parse tree to which the partial who matches the returned rule should be appended
        :return: a list of tuples (ruleTree, parseTree).
        IMPORTANT: ruleTree member values will be changed ! if not desirable give a deepcopy of ruleTree as a parameter
        """

        ret = ()
        endBool = False
        if ruleTree.currentIndex + 1 < len(ruleTree.production):
            ruleTree.currentIndex +=1 #most basic case, next element on the same level
            #we stay on the same level so the parse tree stays the same as well
            ret = ( (deepcopy(ruleTree), deepcopy(parseTree)) )

        else: #this level is finished we try the parent and so on until we find a next
            parent = ruleTree.parent
            stop = False
            while parent and not stop:
                #but it think that that cardinals can only be applied to tokens not sure, TODO ask Bruno
                index = ruleTree.parentIndex

                if not ruleTree.isSubRule:
                    #if the current rule tree is a rule the fact that we go one up means going one up in the parse tree
                    parseTree = parseTree.parent

                if  (index + 1) < len(parent.production):
                    stop = True
                    ruleTree = ruleTree.parent
                    ruleTree.currentIndex = index + 1
                    ret = ( (deepcopy(ruleTree), deepcopy(parseTree)) )
                else:
                    ruleTree = ruleTree.parent
                    parent = ruleTree.parent
        if ret:
            ret[0].partIndex = partialIndex
        return ret

    def addToMatchList(self, toCheckList):
        """
        adds the current list in reverse order to the global list.
        reverse order because we always check the last added on the global list and the given list the first is the most important
        :param toCheckList:
        :return:
        """
        def debugPrint(tree):
            temp = tree
            parent = temp.parent
            while parent:
                temp = temp.parent
                parent = temp.parent

            Parser.PrettyPrinter().visit(temp)
            print "-------------------"


        foundEnd = False
        if toCheckList:
            toCheckList.reverse()
            #print "ADDED TEMP RESULTS ARE (note duplicates are normal)" #TODO REMOVE
            for item in toCheckList:
                if foundEnd:
                    #if we ask not to stop immeidatly at the first result we continue but we only add those result those alternatives that also are complete
                    if item[0].partIndex >= self.stopIndex:
                        self.toMatchList.append(item)
                        #debugPrint(item[1])  #TODO remove the printing

                else: #if not found (or self.Strop at first result in which case found willnever be set true)
                    self.toMatchList.append(item)
                    #debugPrint(item[1])  #TODO remove the printing


                    if item[0].partIndex >= self.stopIndex:
                        if self.stopAlternativesOnceFound:
                            break #if we encountered the stop condition we stop so that we won't check other alternatives first
                        else:
                            foundEnd = True

    def checkRule(self, curRuleTree, curParseTree):
        oper = curRuleTree.operator

        #print "WILL NOW TRY TO MATCH:" #TODO remove print
        #print "Patrial Tree ", str(curRuleTree.partIndex) , "(", self.partList[curRuleTree.partIndex].head,") to" ,  curRuleTree


        if oper == ".":#sequence , either this matches or it doesn't
            self.checkSequence(curRuleTree, curParseTree)
        elif oper == '*':
            self.checkZeroOrMore(curRuleTree,curParseTree)
        elif oper == '+':
            self.checkOneOrMore(curRuleTree,curParseTree)
        elif oper == '?':
            self.checkOptional(curRuleTree,curParseTree)
        elif oper == '|':
            self.checkOr(curRuleTree,curParseTree)
        elif oper == '#':
            self.checkCardinal(curRuleTree,curParseTree)

    def __preCheck(self, curRuleTree):
        curProdElem = curRuleTree.production[curRuleTree.currentIndex]
        curProdElemIsRule = False
        if isinstance(curProdElem, basestring):
            if curProdElem[0] == '@': #rule
                curProdElem = curProdElem[1:] #we only need to remove if rulename or named token, anonyous tokens do not start with $
                curProdElemIsRule = True
            elif curProdElem[0] == '$' or curProdElem[0] == '#': #named token or cardinal operator
                curProdElem = curProdElem[1:]
            else: #anon token has no $ keep curProdElem value as it is
                pass
        partialTree = self.partList[curRuleTree.partIndex]
        return curProdElem, curProdElemIsRule, partialTree

    def __createNewRule(self,curRuleTree, curProdElem, curParseTree):
        """
        creates a new rule as child of the current one and a parse tree needed to append things match in the new rule
        :param curRuleTree: the current rule
        :param curProdElem: the current production rule
        :param curParseTree: the current parse tree
        :return: new instances of rule and parse tree corresponding to the updated versions of the current tone by adding a child rule
        """

        #create a deep copy of the current rule tree to serve as parent for the child
        parentRuleTree = deepcopy(curRuleTree)
        newRuleTree = RuleTree(curProdElem, self.grammarInstance.rules[curProdElem]['body'], parentRuleTree, parentRuleTree.currentIndex)
        newRuleTree.partIndex = parentRuleTree.partIndex #the index we need to check remains the same since nothing was found we just go deeper in the grammar
        parentRuleTree.children.append(newRuleTree)

        parentParseTree = deepcopy(curParseTree)#the current parse tree is copied as a starting point for appending
        childParseTree = Tree(curProdElem,[],Position(-1,-1), Position(-1,-1))
        setattr(childParseTree, 'parent', parentParseTree)
        parentParseTree.tail.append(childParseTree)
        return newRuleTree , childParseTree

    def __createNewSubRule(self, curRuleTree, curProdElem, curParseTree):
        """
        creates a new subrule as child of the current rule and a parse tree needed to append things match in the new rule
        :param curRuleTree: the current rule
        :param curProdElem: the current production rule
        :param curParseTree: the current parse tree
        :return: new instances of rule and parse tree corresponding to the updated versions of the current tone by adding a child sub rule
        """
        #this is not a string but a sub rule, so we create a new RuleTree that starts at it first index, whit the current Rule Tree as its parent
        parentRuleTree = deepcopy(curRuleTree) #create a deep copy of the current rule tree
        #we do this so that the current state is preserved so that if the child finishes next will continue from the correct point
        newRuleTree = RuleTree(None, curProdElem, parentRuleTree, parentRuleTree.currentIndex) #create a new child rule tree and add the deepcopy as parent
        newRuleTree.partIndex = parentRuleTree.partIndex #the index we need to check remains the same since nothing was found we just go deeper in the grammar
        parentRuleTree.children.append(newRuleTree)
        parseTreeDC = deepcopy(curParseTree)#the current parse tree is copied as a starting point for appending,
        ## this is all we need to do because since this is a subRule it is only a grammar hierarchy not a parser one
        return newRuleTree , parseTreeDC

    def __appendPartialToCurrentParseTree(self, partialTree, currentParseTree):
        """
        merges the currentparste tree with the pinspected partial tree by appending the later to the former
        :param partialTree:
        :param currentParseTree:
        :return: a new instance of a parse tree representing the merged one
        """
        #create deep copies so that if this alternative doesn't pan out we can return to earlier versions
        partialTreeDC = deepcopy(partialTree)
        parseTreeDC = deepcopy(currentParseTree)

        #create a parent child relationship between the current parse tree and the partial tree examined
        parseTreeDC.tail.append(partialTreeDC)
        setattr(partialTreeDC, 'parent', parseTreeDC)
        return parseTreeDC

    def checkSequence(self, curRuleTree, curParseTree):
        """
        checks the  current rule according to the logic of a sequence
        :param curRuleTree: a rule tree, the rule part being checked
        :param curParseTree: a parse tree
        :return: nothing is returned
        """
        curProdElem, curProdElemIsRule, partialTree = self.__preCheck(curRuleTree)
        #curProdElem = the current element of the production rule that is being checked
        #curProdElemIsRule = whether or not that element corresponds to a rule (if false it is a token)
        #partialTree = the partial tree that we are trying to match to the rule
        toCheckList = [] #list of rule to check once this has been examined

        #match as a term
        if isinstance(curProdElem, basestring):
            if curProdElem == partialTree.head:

                #create a new parse tree that i the current one with the partial one appended
                newParseTree = self.__appendPartialToCurrentParseTree(partialTree,curParseTree)

                #create the next rule part to that needs to be checked
                curRuleTreeDC = deepcopy(curRuleTree) #deepcopy because the curRule is changed and we stillneed to check stuff here
                nextCheckList = self.getNextIndex(curRuleTreeDC, curRuleTree.partIndex + 1, newParseTree, True)

                if nextCheckList:
                    for tuple in nextCheckList:
                        if tuple[0] not in self.memoList: #check if the rule has not already been/is not already scheduled to be checked
                            self.memoList.append(tuple[0])
                            toCheckList.append(tuple)
                #TODO what if checkList is empty ? this means the end of the entire rule was reached, normally this cant happen here because this is by defintion partial results
                #but what if this method is  used for example trying to match startrule where there is already a start this means it is complete and some children have an * operator
            else:
                pass #this is a sequence and no results were found, we do not continue with the next token
                #NOTE TO MYSELF: #TODO remove this hint once this done
                #i keep having the idea that there needs to be a findNext whit found fale here so that for example optional can find next anyway
                #but then i remember that this will not work because tha partial index will not be the same this alternative needs to be set at option level



        if curProdElemIsRule or isinstance(curProdElem, list):

            newRuleTree = None
            newParseTree = None
            if curProdElemIsRule:
                newRuleTree, newParseTree = self.__createNewRule(curRuleTree, curProdElem, curParseTree)
            else:
                newRuleTree, newParseTree = self.__createNewSubRule(curRuleTree, curProdElem, curParseTree)

            if newRuleTree not in self.memoList:
                self.memoList.append(newRuleTree)
                toCheckList.append((newRuleTree, newParseTree))
                #in this case we simply send it to be tested next,
                #no alternative is provided since this is a sequence this either passes or not


        #we add the next possible rule parts (and the parse trees that go with them to the list of things to be checked)
        self.addToMatchList(toCheckList)

    def checkZeroOrMore(self, curRuleTree, curParseTree):
        """
        checks the  current rule according to the logic of a * (0 or more) operator
        :param curRuleTree: a rule tree, the rule part being checked
        :param curParseTree: a parse tree
        :return: nothing is returned
        """
        curProdElem, curProdElemIsRule, partialTree = self.__preCheck(curRuleTree)
        #curProdElem = the current element of the production rule that is being checked
        #curProdElemIsRule = whether or not that element corresponds to a rule (if false it is a token)
        #partialTree = the partial tree that we are trying to match to the rule
        toCheckList = [] #list of rule to check once this has been examined

        if isinstance(curProdElem, basestring):
            #match as term for operator * this can only mean [*, curProdElem] because if there were more curProdElem would be a subList wist a sequence operator
            if curProdElem == partialTree.head:

                newParseTree = self.__appendPartialToCurrentParseTree(partialTree,curParseTree)

                #it matched but we can try this again so we return the same tree with the same index to try again on next partial Tree
                nextRuleTree = deepcopy(curRuleTree)
                nextRuleTree.partIndex +=1

                #if ruleTreeDC not in self.memoList:
                if nextRuleTree not in self.memoList:
                    self.memoList.append(nextRuleTree)
                    toCheckList.append((nextRuleTree, newParseTree))

            else: #it didn't match, but * is optional so we simple we need to go to try to match the next one
                #create the next rule part to that needs to be checked
                curRuleTreeDC = deepcopy(curRuleTree) #deepcopy because the curRule is changed and we still need to check stuff here
                parseTreeDC = deepcopy(curParseTree)
                nextCheckList = self.getNextIndex(curRuleTreeDC, curRuleTree.partIndex, parseTreeDC, True)
                #this is a tern it doesnt matter that an * term wasnt found since it is optional

                if nextCheckList:
                    for tuple in nextCheckList:
                        if tuple[0] not in self.memoList: #check if the rule has not already been/is not already scheduled to be checked
                            self.memoList.append(tuple[0])
                            toCheckList.append(tuple)
                #TODO what if checkList is empty ? this means the end of the entire rule was reached, normally this cant happen here because this is by defintion partial results


        if curProdElemIsRule or isinstance(curProdElem, list): #mutually exclusive cases but same logic

            #create a new rule and start checking
            newRuleTree = None
            newParseTree = None
            if curProdElemIsRule:
                newRuleTree, newParseTree = self.__createNewRule(curRuleTree, curProdElem, curParseTree)
            else:
                newRuleTree, newParseTree = self.__createNewSubRule(curRuleTree, curProdElem, curParseTree)

            if newRuleTree not in self.memoList:
                self.memoList.append(newRuleTree)
                toCheckList.append((newRuleTree, newParseTree))

            #provide an alternative if this fails
            curRuleTreeDC = deepcopy(curRuleTree)
            altTuple = self.getOptionalNotFoundAlternative( curRuleTreeDC, curRuleTree.partIndex, curParseTree)

            if altTuple and altTuple[0] not in self.memoList:
                self.memoList.append(altTuple[0])
                toCheckList.append(altTuple)

        self.addToMatchList(toCheckList)

    def checkOneOrMore(self, curRuleTree, curParseTree):
        """
        checks the  current rule according to the logic of a + one or more operator
        :param curRuleTree: a rule tree, the rule part being checked
        :param curParseTree: a parse tree
        :return: nothing is returned
        """
        curProdElem, curProdElemIsRule, partialTree = self.__preCheck(curRuleTree)
        #curProdElem = the current element of the production rule that is being checked
        #curProdElemIsRule = whether or not that element corresponds to a rule (if false it is a token)
        #partialTree = the partial tree that we are trying to match to the rule
        toCheckList = [] #list of rule to check once this has been examined
        if isinstance(curProdElem, basestring):
            if curProdElem == partialTree.head:
                newParseTree = self.__appendPartialToCurrentParseTree(partialTree,curParseTree)

                #it matched but we can try this again so we return the same tree with the same index to try again on next partial Tree
                nextRuleTree = deepcopy(curRuleTree)
                nextRuleTree.partIndex +=1
                nextRuleTree.extra["+Matched"] = True

                #if ruleTreeDC not in self.memoList:
                if nextRuleTree not in self.memoList:
                    self.memoList.append(nextRuleTree)
                    toCheckList.append((nextRuleTree, newParseTree))
            else:
                #A + needs to be matched at least once before
                if ("+Matched" in curRuleTree.extra) and curRuleTree.extra["+Matched"]:
                    #if we already found an instance once it isn't a failure that we didnt find it again.
                    #we try the next rule part
                    #create the next rule part to that needs to be checked
                    curRuleTreeDC = deepcopy(curRuleTree) #deepcopy because the curRule is changed and we stillneed to check stuff here
                    parseTreeDC = deepcopy(curParseTree)
                    nextCheckList = self.getNextIndex(curRuleTreeDC, curRuleTree.partIndex, parseTreeDC, False)

                    if nextCheckList:
                        for tuple in nextCheckList:
                            if tuple[0] not in self.memoList: #check if the rule has not already been/is not already scheduled to be checked
                                self.memoList.append(tuple[0])
                                toCheckList.append(tuple)
                else:
                    #this was the first time we tried + and it failed, + must match at least once, this is a failure
                    pass
                    #return the initial values:
                    # match = false, tree is is still the current one with the same index
                    # and the end has not been reached


        #if passes, try again with next partial on the list (this means the next after the inner sequence has been read not the curren tnext index)
        #(try next will return this) automatically if it passes , so just let it all happen
        #need to somehow marked that it passed at least once
        #if it fails but matched at least once it needs try the sibling of + with this index
        #if it failed but didnt match  pass, this is done
        if curProdElemIsRule or isinstance(curProdElem, list): #mutually exclusive cases but same logic

            #create a new rule and start checking
            newRuleTree = None
            newParseTree = None
            if curProdElemIsRule:
                newRuleTree, newParseTree = self.__createNewRule(curRuleTree, curProdElem, curParseTree)
            else:
                newRuleTree, newParseTree = self.__createNewSubRule(curRuleTree, curProdElem, curParseTree)

            if newRuleTree not in self.memoList:
                self.memoList.append(newRuleTree)
                toCheckList.append((newRuleTree, newParseTree))

            #provide an alternative if this fails
            #we can only provide the alternative if it has succeeded at least once. (+ is 1 or  more)
            # +Matched is set in setNextIndex because this is when terms are checked and we can see if the whole sequence has matched
            if ("+Matched" in curRuleTree.extra) and curRuleTree.extra["+Matched"]:

                curRuleTreeDC = deepcopy(curRuleTree)
                altTuple = self.getOptionalNotFoundAlternative( curRuleTreeDC, curRuleTree.partIndex, curParseTree) #instead of trying the new tree find an alternative on the current one
                #print "+MATCHED CURTREE: SO WE WILL ADD ALT:" , altTuple[0] #TODO remove print


                if altTuple and altTuple[0] not in self.memoList:
                    self.memoList.append(altTuple[0])
                    toCheckList.append(altTuple)

        self.addToMatchList(toCheckList)

    def checkOptional(self, curRuleTree,curParseTree):
        """
        checks the  current rule according to the logic of ? optional
        :param curRuleTree: a rule tree, the rule part being checked
        :param curParseTree: a parse tree
        :return: nothing is returned
        """
        curProdElem, curProdElemIsRule, partialTree = self.__preCheck(curRuleTree)
        #curProdElem = the current element of the production rule that is being checked
        #curProdElemIsRule = whether or not that element corresponds to a rule (if false it is a token)
        #partialTree = the partial tree that we are trying to match to the rule
        toCheckList = [] #list of rule to check once this has been examined

        if isinstance(curProdElem, basestring):
            if curProdElem == partialTree.head:

                #create a new parse tree that is the current one with the partial one appended
                newParseTree = self.__appendPartialToCurrentParseTree(partialTree,curParseTree)

                #create the next rule part to that needs to be checked
                curRuleTreeDC = deepcopy(curRuleTree) #deepcopy because the curRule is changed and we stillneed to check stuff here
                nextCheckList = self.getNextIndex(curRuleTreeDC, curRuleTree.partIndex + 1, newParseTree, True) #it matched we want to match the next partial index

                if nextCheckList:
                    for tuple in nextCheckList:
                        if tuple[0] not in self.memoList: #check if the rule has not already been/is not already scheduled to be checked
                            self.memoList.append(tuple[0])
                            toCheckList.append(tuple)

            else: #it didn't match, but ? is optional so we simple we need to go to try to match the next rule part
                #create the next rule part to that needs to be checked
                curRuleTreeDC = deepcopy(curRuleTree) #deepcopy because the curRule is changed and we still need to check stuff here
                parseTreeDC = deepcopy(curParseTree)
                nextCheckList = self.getNextIndex(curRuleTreeDC, curRuleTree.partIndex , parseTreeDC, True) #it dindt match we want to match the ame partial index to something else
                #this is a term it doesnt matter that an optional  term wasn't found

                if nextCheckList:
                    for tuple in nextCheckList:
                        if tuple[0] not in self.memoList: #check if the rule has not already been/is not already scheduled to be checked
                            self.memoList.append(tuple[0])
                            toCheckList.append(tuple)
                #TODO what if checkList is empty ? this means the end of the entire rule was reached, normally this cant happen here because this is by defintion partial results

        if curProdElemIsRule or isinstance(curProdElem, list): #mutually exclusive cases but same logic

            #create a new rule and start checking
            newRuleTree = None
            newParseTree = None
            if curProdElemIsRule:
                newRuleTree, newParseTree = self.__createNewRule(curRuleTree, curProdElem, curParseTree)
            else:
                newRuleTree, newParseTree = self.__createNewSubRule(curRuleTree, curProdElem, curParseTree)

            if newRuleTree not in self.memoList:
                self.memoList.append(newRuleTree)
                toCheckList.append((newRuleTree, newParseTree))

            #provide an alternative if this fails
            curRuleTreeDC = deepcopy(curRuleTree)
            altTuple = self.getOptionalNotFoundAlternative( curRuleTreeDC, curRuleTree.partIndex, curParseTree)

            if altTuple and altTuple[0] not in self.memoList:
                self.memoList.append(altTuple[0])
                toCheckList.append(altTuple)



        self.addToMatchList(toCheckList)

    def checkOr(self, curRuleTree, curParseTree):
        """
        checks the  current rule according to the logic of | Or operator
        :param curRuleTree: a rule tree, the rule part being checked
        :param curParseTree: a parse tree
        :return: nothing is returned
        """
        curProdElem, curProdElemIsRule, partialTree = self.__preCheck(curRuleTree)
        #curProdElem = the current element of the production rule that is being checked
        #curProdElemIsRule = whether or not that element corresponds to a rule (if false it is a token)
        #partialTree = the partial tree that we are trying to match to the rule
        toCheckList = [] #list of rule to check once this has been examined


        if isinstance(curProdElem, basestring):
            nextPartIndex = 0
            nextParseTree = None
            if curProdElem == partialTree.head:

                #create a new parse tree that is the current one with the partial one appended
                newParseTree = self.__appendPartialToCurrentParseTree(partialTree,curParseTree)

                #create the next rule part to that needs to be checked
                curRuleTreeDC = deepcopy(curRuleTree) #deepcopy because the curRule is changed and we stillneed to check stuff here
                curRuleTreeDC.extra["|Matched"] = True
                nextCheckList = self.getNextIndex(curRuleTreeDC, curRuleTree.partIndex + 1, newParseTree, True, True)
                #the first true is found, the second true is because this is an or and we do not want the next direct sibling yet (it will be given as alternative not as first choice)

                if nextCheckList:
                    for tuple in nextCheckList:
                        if tuple[0] not in self.memoList: #check if the rule has not already been/is not already scheduled to be checked
                            self.memoList.append(tuple[0])
                            toCheckList.append(tuple)

                nextPartIndex = curRuleTree.partIndex + 1
                nextParseTree = newParseTree
            else:
                #next we add as an alternative the next direct sibling
                nextPartIndex = curRuleTree.partIndex
                nextParseTree = curParseTree

            #wheter it failed or not if there is a next direct sibling (another OR option)
            #we add it to the list to be tried
            if curRuleTree.currentIndex +1  < len(curRuleTree.production):
                altRuleTree = deepcopy(curRuleTree)
                altRuleTree.currentIndex += 1
                altRuleTree.partIndex =  nextPartIndex
                altParseTree = deepcopy(nextParseTree)

                if altRuleTree not in self.memoList:
                    toCheckList.append((altRuleTree, altParseTree))

        if curProdElemIsRule or isinstance(curProdElem, list): #mutually exclusive cases but same logic
        #TODO CHECK THIS SCENARIO AND MAYBE DO SONMETHING WITH |MATCHED
            #create a new rule and start checking
            newRuleTree = None
            newParseTree = None
            if curProdElemIsRule:
                newRuleTree, newParseTree = self.__createNewRule(curRuleTree, curProdElem, curParseTree)
            else:
                newRuleTree, newParseTree = self.__createNewSubRule(curRuleTree, curProdElem, curParseTree)

            if newRuleTree not in self.memoList:
                self.memoList.append(newRuleTree)
                toCheckList.append((newRuleTree, newParseTree))

                #if found:
                #MARK  AS FOUND
                #  try the thing after the OR (with partIndex+1)
                #and set as aleternative the next child of OR (with Partindex+1)

                #if not found
                #try the next elemtn of or (with partIndex same)
                #if last elemten and not found
                #pass

            #provide an alternative wheter it fails or succeeds we need to try the next or sibling
            if curRuleTree.currentIndex +1  < len(curRuleTree.production):
                altRuleTree = deepcopy(curRuleTree)
                altRuleTree.currentIndex += 1
                altParseTree = deepcopy(curParseTree)

                if altRuleTree not in self.memoList:
                    toCheckList.append((altRuleTree, altParseTree))


        self.addToMatchList(toCheckList)

    def checkCardinal(self, curRuleTree, curParseTree):
        """
        checks the  current rule according to the logic of a # cardinal operator
        :param curRuleTree: a rule tree, the rule part being checked
        :param curParseTree: a parse tree
        :return: nothing is returned
        """
        curProdElem, curProdElemIsRule, partialTree = self.__preCheck(curRuleTree)
        #curProdElem = the current element of the production rule that is being checked
        #curProdElemIsRule = whether or not that element corresponds to a rule (if false it is a token)
        #partialTree = the partial tree that we are trying to match to the rule
        toCheckList = [] #list of rule to check once this has been examined
        self.addToMatchList(toCheckList)
