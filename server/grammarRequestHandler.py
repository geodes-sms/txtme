"""
Daniel Riegelhaupt
v2 October 2014
Last updated February 2015

The server application that ties all visitors and such together.
"""

#TODO some try catch block have been removed so that the exception are shown better on the console for debugging purposes
#they should be put back in the final version

from responseSerializer import ResponseSerializer
from os import getcwd
from os.path import join
from codecs import open
from copy import deepcopy
import re

#the grammar parser directory must be set in python path for those imports:
#for the moment the directory is PNeditor/grammar_parser_v2/
from hutnparser import Parser, Tree
from position import Position
from metaGrammar import MetaGrammar
from styleGrammar import StyleGrammar
from partialTreeFuser import PartialTreeFuser
from visitors.preProcessorVisitor import PreProcessorVisitor
from visitors.modelMappingVisitor import ModelMappingVisitor
from visitors.grammarCompilerVisitor import GrammarCompilerVisitor
from visitors.styleDefinitionVisitor import StyleDefinitionVisitor
from visitors.styleMappingVisitor import StyleMappingVisitor
from visitors.applyStyleVisitor import ApplyStyleVisitor
from visitors.mvkLayer import ModelDataVisitor
from visitors.tokenFinderVisitor import TokenFinderVisitor

DEFAULT_STYLE_FILE = 'grammar_parser_v2/models/examples/default.st'

class GrammarRequestHandler:

    def __init__(self, modelVerseInstance):
        self.__currentParser = None #the parser specifically generated for the grammar
        self.__currentParseTree = None #the parse tree of the current input (annotated by visitors)
        self.__metaModelGrammar = None #the grammar class retuned by the grammar compiler visitor , we save it to do auto complete searhces in it

        self.__keywordsValue = None #a list of keywords per category. used to give back to the user
        self.__keywordsName = None # alist of the tokennames per category (not their value), used for stylemapping
        self.__defaultStyle = ""
        self.__errorStyle = ""

        #self.__modelMap = None #the map gotten by visiting the parse tree that resulted from parsing a mapping with the meta grammar for mapping
        self.__styleMap = None #the map rules, tokens and keywords to styles
        self.__stylePosList = [] #the map containing the styles and their position in the text
        self.__mvkInstance = modelVerseInstance
        self.__mvkLayer = None

        self.__applyStyleVis = None
        #self.__initLoadMetaGrammar()
        self.__preProcessorVis = PreProcessorVisitor()


    def __initLoadMetaGrammar(self):
        pass
        #this method isn't needed anymore
        #both the meta grammar and the model mapping grammar are inside the MetaGrammar class

    def __read(self, file):
        #CUR_PATH = os.path.split(__file__)[0]
        with open(file, encoding='utf-8') as f:
            return f.read()

    def __parseStyles(self,reqDic):

        defName = reqDic["styledef"]
        mapName = reqDic["stylemap"]
        defText = ""
        mapText = ""

        try:
           defText = self.__read(defName)
        except Exception as e:
            #print e
            err = "Failed to read style definition file: '" + defName +"'. Details:\n" + str(e)
            return ResponseSerializer.error(err)

        styleParser = Parser(StyleGrammar(), hide_implicit = True)
        result = styleParser.parse(defText)
        if(result['status'] == Parser.Constants.Success):
            visitorDef = StyleDefinitionVisitor()
            styleDef = visitorDef.visit(result['tree'])
            visitorMap =  StyleMappingVisitor(styleDef)
            warnings = []

            if defName == mapName:
                self.__styleMap = visitorMap.visit(result['tree'])
                warnings = visitorMap.getWarnings()
            else:

                try:
                   mapText = self.__read(mapName)
                except Exception as e:
                    #print e
                    err = "Failed to read style map file: '" + mapName +"'. Details:\n" + str(e)
                    return ResponseSerializer.error(err)

                result2 = styleParser.parse(mapText)
                if(result2['status'] == Parser.Constants.Success):
                    self.__styleMap = visitorMap.visit(result2['tree'])
                    warnings = visitorMap.getWarnings()
                else:
                    err = "Failed to parse style map file: '" + mapName +"'. Details:\n" + result2['text']
                    return ResponseSerializer.error(err)

            #now that we have a map we map it to keywords
            if self.__keywordsValue:
                for key in self.__keywordsValue.keys():
                    if self.__styleMap.has_key(key) and self.__styleMap[key]['keywords_bool']:
                        self.__keywordsValue[key]['style'] = self.__styleMap[key]['style']
                    elif self.__styleMap.has_key('*') and self.__styleMap['*']['keywords_bool']: #if there is a global keyword highlighting style defined
                        self.__keywordsValue[key]['style'] = self.__styleMap['*']['style']
                    else:
                        warnings.append("keyword group: " +  key + " has no style defined")

            #set tdefault and error
            if '@Default' in self.__styleMap:
                self.__defaultStyle = self.__styleMap['@Default']['style']
            if '@Error' in self.__styleMap:
                self.__errorStyle = self.__styleMap['@Error']['style']

            #create a visitor to apply the style
            self.__applyStyleVis = ApplyStyleVisitor(self.__styleMap, self.__keywordsName)

            if warnings:
                err = "Warning! encountered the following problems while interpreting styles:\n"
                for w in warnings:
                    err += w +'\n'
                return ResponseSerializer.error(err)

            return True
        else:
            err = "Failed to parse style definition file: '" + defName +"'. Details:\n" + result['text']
            return ResponseSerializer.error(err)

    def proccessLoadGrammarRequest(self, reqDic):
        ret = ""
        grammarName =""
        metaName =""
        grammarText = ""
        metaText = ""

        #first we get the file
        if reqDic.has_key("grammar") and reqDic["grammar"]: #it is not enough the key is there the value must not be null or ""
            grammarName =  reqDic["grammar"]
            try:
                grammarText = self.__read(grammarName)
            except Exception as e:
                #print e
                err = "Failed to read grammar file: '" + grammarName +"'. Details:\n" + str(e)
                return ResponseSerializer.error(err)
        else:
            return ResponseSerializer.error("ERROR parameter missing: 'grammar'!")

        if self.__mvkLayer:
            #print "REMOVE OLD MODEL"
            self.__mvkLayer.clearModel()
            self.__mvkLayer = None
            #in case we already loaded a grammar we clear the current model from the mvk to avoid problems.
            #for example if this is called because we refreshed the webpage, creating the same model will cause errors

        #we try to read meta model mapping (this is optional hence no error message if missing)
        if reqDic.has_key("metamap") and reqDic["metamap"]: #it is not enough the key is there the value must not be null or ""
            metaName = reqDic["metamap"]
            if metaName != grammarName:
                try:
                    metaText = self.__read(metaName)
                except Exception as e:
                    #print e
                    err = "Failed to read meta model mapping file: '" + metaName +"'. Details:\n" + str(e)
                    return ResponseSerializer.error(err)
        else:
            print "WARNING parameter missing: 'metamap'! the text can still parse but no model will be created"


        #we parse the grammar and create the necessary meta data:
        #for the moment  grammar structure, mapping structure, keywords
        parser = Parser(MetaGrammar(), hide_implicit = True)
        result = parser.parse(grammarText)
        if(result['status'] == Parser.Constants.Success):
            try:
                tree = result['tree']
                compiler = GrammarCompilerVisitor()
                ModelGrammar = compiler.visit(tree)
                self.__metaModelGrammar = deepcopy(ModelGrammar())

                #the parser we use to parse input received, must negelect whitespaces and so on... and must return postions
                #using line and column (if not set returns absolute positions)
                self.__currentParser = Parser(ModelGrammar(), hide_implicit = True, line_position = True) #NOTE: Bruno if you want to keep whitespaces set  hide implicit to False here
                self.__keywordsValue = compiler.getKeywordsValue()
                self.__keywordsName = compiler.getKeywordsName()
                if metaName: #if a metaName has been given we create a metamodel mapping
                    try:
                        modelMap = None
                        if metaName == grammarName: #if they are in the same document we van use the same parse tree
                            modelMap = ModelMappingVisitor().visit(tree)
                        else: #we need to parse the document separetly
                            resultMeta = parser.parse(metaText)
                            if(resultMeta['status'] == Parser.Constants.Success):
                                treeMeta = resultMeta['tree']
                                modelMap = ModelMappingVisitor().visit(treeMeta)
                            else:
                                err = "Failed to parse meta model mapping file: '" + metaName +"'. Details:\n" + resultMeta['text']
                                return ResponseSerializer.error(err)

                        self.__mvkLayer = ModelDataVisitor(modelMap, self.__mvkInstance)
                    except Exception as e:
                        err = "Failed to instantiate meta model mapping: '" + metaName +"'. Details:\n" + str(e)
                        return ResponseSerializer.error(err)

            except Exception as e:
                err = "Failed to instantiate grammar: '" + grammarName +"'. Details:\n" + str(e)
                return ResponseSerializer.error(err)
        else:
            err = "Failed to parse grammar file: '" + grammarName +"'. Details:\n" + result['text']
            return ResponseSerializer.error(err)


        #next part is keywords
        if reqDic.has_key("stylemap") and reqDic["stylemap"]: #the key must be there and the value must not be null or empty
            if reqDic.has_key("styledef") and reqDic["styledef"]:
                pass
            else:
                print "WARNING parameter missing: 'styledef'! will use default one"
                reqDic["stylemap"] = DEFAULT_STYLE_FILE
                reqDic["styledef"] = DEFAULT_STYLE_FILE
        else:
            print "WARNING parameter missing: 'stylemap'! will use default one"
            reqDic["stylemap"] = DEFAULT_STYLE_FILE
            reqDic["styledef"] = DEFAULT_STYLE_FILE

        b = self.__parseStyles(reqDic)
        if not (isinstance(b,bool) and b == True): #bool needs to be of type boolean otherwise it is an error message
            return b

        #return ResponseSerializer.success()
        #print "LOAD GRAMMAR WAS A SUCCES, RETURNING"
        #print "keywords are: ", self.__keywordsValue
        return ResponseSerializer.success({"keywords": self.__keywordsValue , "default_style": self.__defaultStyle,
                                               "error_style" : self.__errorStyle})

    def processCheckTextRequest(self,reqDic):
        text = ""

        if reqDic.has_key("input"):
            text = reqDic["input"]
            #print "TEXT recieved = \n'" +text +"'"
        else:
            return ResponseSerializer.error("ERROR parameter missing: 'input'!")

        #try:
        if self.__currentParser:
            self.__stylePosList = [] #reset the style list in case we already had a previous one

            if self.__mvkLayer: #if there is a meta model mapping this will not be None
                self.__mvkLayer.resetData() #each time we parse we need to remove the previous data

            result = self.__currentParser.parse(text)
            if(result['status'] == Parser.Constants.Success):
                self.__currentParseTree = result['tree']
                self.__currentParseTree = self.__preProcessorVis.visit(self.__currentParseTree)

                errLog = []
                if self.__mvkLayer:
                    self.__mvkLayer.setAddingNewData()
                    modelData = self.__mvkLayer.visit(self.__currentParseTree) #TODO save mdoel data and use it for autocomplete TODO 2 maybe keep an old version also if the newer one is partial
                    #print "DEBUG:",  modelData.toStr()
                    errLog = self.__mvkLayer.updateModel()

                if self.__styleMap:
                    self.__stylePosList = self.__applyStyleVis.visit(self.__currentParseTree)

                #print "PRINTING ERROR LOG:"
                #print errLog
                #print "PRINTING STYLE LIST:"
                #print self.__stylePosList
                return ResponseSerializer.success({"error_log" : errLog , 'styles' : self.__stylePosList}) #the request was a succes the fact that there are syntax or semantic errors doesn't change it
            else:

                syntaxError = { 'error' : result['text']}
                syntaxError['error_position'] = { 'startpos': { 'line': result['line'], 'column' : result['column']} }
                eLog = [syntaxError] #first the syntax error
                partials = result['partialresults']

                fuser = PartialTreeFuser()
                rule = ''
                if self.__mvkLayer:
                    rule = self.__mvkLayer.getModelNameGrammarRule()

                treeAr = fuser.fuse(partials, self.__metaModelGrammar, self.__currentParser.implicitRuleName,rule)

                if self.__mvkLayer:
                    self.__mvkLayer.setAddingNewData()
                    for fusedTree in treeAr:
                        #print "Fused Tree:", Parser.PrettyPrinter().visit(fusedTree) #TODO comment this statement later
                        self.__preProcessorVis.visit(fusedTree)

                        modelData = self.__mvkLayer.visit(fusedTree)
                        #print modelData.toStr()

                        if self.__styleMap:
                            self.__stylePosList += self.__applyStyleVis.visit(fusedTree)
                    #print "DEBUG INCOMPL model data= " , modelData.toStr()
                    eLog += self.__mvkLayer.updateModel() #any mvk error per partial result
                    #print "PRINTING ERROR LOG:"
                    #print eLog
                elif self.__styleMap:
                    for fusedTree in treeAr:
                        self.__stylePosList += self.__applyStyleVis.visit(fusedTree)

                return ResponseSerializer.success({"error_log" : eLog, 'styles' : self.__stylePosList}) #the request was a succes the fact that there are syntax or semantic errors doesn't change it
        else:
            return ResponseSerializer.error("The grammar must be set before attempting to parse the text")

        #except Exception as e:
        #    err = "failed to parse the text due to an exception in the server. Details:\n" + str(e.message)
        #    print err
        #    return ResponseSerializer.error(err)

    """
    def processAutoCompleteRequest(self, reqDic):
        text = ""
        pos = None
        acPosition = None
        autoCompleteList = []
        if reqDic.has_key("input"):
            text = reqDic["input"]
            #print "TEXT recieved = \n'" +text +"'"
        else:
            return ResponseSerializer.error("ERROR parameter missing: 'input'!")

        if reqDic.has_key("position"):
            pos = reqDic["position"]
            #print "Position recieved = '" + str(pos) +"'"
            acPosition = Position(pos["line"], pos["column"])
        else:
            return ResponseSerializer.error("ERROR parameter missing: 'position'!")

        #try:
        if self.__currentParser:
            self.__autoCompleteList = [] #reset the list

            if self.__mvkLayer:
                self.__mvkLayer.resetData() #each time we parse we need to remove the previous data

            result = self.__currentParser.parse(text)

            suggestions , absPos = self.__getSuggestions(text, pos) #in the previous version this used to be only done for complete text
            #print "Autocpmlete suggestions: ", suggestions
            #however doing this with incompete text alos gives better result by forcing a syntax error at the given postion instead of letting it try to continue first the results are much better
            #the position inserted into a Position class object so that we can use comparison operators

            #we parse the tree the text this time witouth intentional syntax error to get the parsetree, datamodel and possible real syntax error
            if(result['status'] == Parser.Constants.Success):
                tree = result['tree']
                #Parser.PrettyPrinter().visit(tree) #TODO comment this statement later
                self.__preProcessorVis.visit(tree)

                modelData = None
                if self.__mvkLayer:
                    modelData = self.__mvkLayer.visit(tree) #TODO should we save it ???
                    #errLog = self.__mvkLayer.updateModel() #we do not need to create the model for autocomplete

                autoCompleteList = self.__autoComplete(suggestions, modelData,tree, acPosition, absPos)

                #print "Autocomplete list - branch complete text: ", autoCompleteList
                return ResponseSerializer.success({ "autocomplete_list": autoCompleteList, "position" : pos} )
            else:
                #print "syntax error", result["text"]
                errorPos = Position(result['line'], result['column'])

                #if the syntax error occurs before the given position
                if self.__isSyntaxError(text, errorPos, result["pos"], acPosition):
                    syntaxError = { 'error' : result['text']}
                    syntaxError['error_position'] = { 'startpos': { 'line': result['line'], 'column' : result['column']} }
                    eLog = [syntaxError]
                    return ResponseSerializer.success({"error_log" : eLog, 'styles' : []})
                    #Note in case of autocomplete we don't even try to use partial models etc.. we just want the syntax error fixed so we may try again

                else:
                    #TODO maybe use the partail results gotton from getSuggestions ?
                    partials = result['partialresults']

                    fuser = PartialTreeFuser()
                    newTree = fuser.fuse(partials, self.__metaModelGrammar, self.__currentParser.implicitRuleName)
                    modelData = None
                    if newTree and self.__mvkLayer:
                        self.__preProcessorVis.visit(newTree)
                        modelData = self.__mvkLayer.visit(newTree)
                        #print modelData.toStr() #TODO comment this statement later

                    #TODO maybe request old data also ???
                    autoCompleteList = self.__autoComplete( suggestions, modelData, newTree, acPosition, absPos)

                    #print "Autocomplete list - branch incomplete text: ", autoCompleteList
                    return ResponseSerializer.success({ "autocomplete_list": autoCompleteList, "postion":{"line" : result["line"], "column": result["column"]} })
                    #we do not simply return pos as postion because the error might have come from somewhere else
        else:
            return ResponseSerializer.error("The grammar must be set before attempting to parse the text")

        #except Exception as e:
        #    err = "failed to parse the text due to an exception in the server. Details:\n" + str(e.message)
        #    print err
        #    return ResponseSerializer.error(err)
    """

    def processAutoCompleteRequest(self, reqDic):
        #print "RECEIVED AC REQUEST"
        text = ""
        pos = None
        acPosition = None
        autoCompleteList = []
        if reqDic.has_key("input"):
            text = reqDic["input"]
            #print "TEXT recieved = \n'" +text +"'"
        else:
            return ResponseSerializer.error("ERROR parameter missing: 'input'!")

        if reqDic.has_key("position"):
            pos = reqDic["position"]
            #print "Position recieved = '" + str(pos) +"'"
            acPosition = Position(pos["line"], pos["column"])
        else:
            return ResponseSerializer.error("ERROR parameter missing: 'position'!")

        #try:
        if self.__currentParser:
            self.__autoCompleteList = [] #reset the list


            suggestions , isSyntaxError, errMsg, retPosLC, retPosAbs  = self.__getSuggestions(text, pos)
            #print "Autocpmlete suggestions: ", suggestions

            if isSyntaxError:
                syntaxError = { 'error' : errMsg}
                syntaxError['error_position'] = { 'startpos': {"line" : retPosLC["line"], "column": retPosLC["column"]}}
                eLog = [syntaxError]
                #print "AUTOCOMPLE ERROR:",  eLog
                return ResponseSerializer.success({"error_log" : eLog, 'styles' : []})

            else:
                autoCompleteList = self.__autoComplete( suggestions, text, retPosAbs)
                #print "AUTOCOMPLE LIST:",  autoCompleteList
                return ResponseSerializer.success({ "autocomplete_list": autoCompleteList, "postion": {"line" : retPosLC["line"], "column": retPosLC["column"]} })

        else:
            return ResponseSerializer.error("The grammar must be set before attempting to parse the text")

        #except Exception as e:
        #    err = "failed to parse the text due to an exception in the server. Details:\n" + str(e.message)
        #    print err
        #    return ResponseSerializer.error(err)


    def processKeywordsAndStyleRequest(self, reqDic):
        if self.__keywordsValue:
            return ResponseSerializer.success({"keywords": self.__keywordsValue , "default_style": self.__defaultStyle,
                                               "error_style" : self.__errorStyle})
        else:
            return ResponseSerializer.error("The style definition must be set before requesting style and keywords information")

    ###################################################################################
    #                              AUTOCOMPLETE LOGIC                                 #
    ###################################################################################


    def __posToAbsolute(self, input, pos):
        #converts a line colimn postion to an index in a string
        #this is the invert method to the Parser method that convert string position to line, column
        line = pos["line"]
        col = pos["column"]
        tabsize = self.__currentParser.tabsize #TODO use getter


        curLine = 1
        curCol = 0
        l = len(input)
        i = 0
        while curLine < line and i < l:
            if input[i] == '\n':
                curLine +=1
            i += 1

        if i >= l:
            return l

        while curCol < col and i < l:
            if  input[i] == "\t":
                curCol += tabsize
            elif input[i] == "\n": #in case we encounter a new line this means the given col was bigger than the line,we give the end of this line
                curCol +=1
                i += 1
                break
            else:
                curCol += 1
            i += 1

        return i-1

    def __isSyntaxError(self, text, errorPosLC, errorPosAbs, givenPosLC, givenPosAbs):
        """
        We determine if a given error is a syntax error or if it is part of the autocomplete request
        :param text: the original text
        :param errorPosLC: the error position as line column
        :param errorPosAbs: the error position as string index (node can be gotten from posToAbsolute(errorPosLC) but why bother if it is already known)
        :param givenPosLC: the position autocomplete was requested at
        :param givenPosAbs: the postion auto complete was requested at as a string index (node can be gotten from posToAbsolute(givenPosLC) but why bother if it is already known)
        :return: True if syntax error. False if part of autocomplete request
        """
        ret = True
        grammarInstance = self.__metaModelGrammar
        if errorPosLC < givenPosLC: #if the error position comes before the given position, it is almost definitely a syntax error
            if errorPosLC.line == givenPosLC.line: #however if they are on the same line there is a chance they are part of hte same word
                word = text[errorPosAbs:givenPosAbs]
                implicitList = self.__currentParser.implicitList #TODO use a getter
                regexToTest = []
                if implicitList:
                    for implicit in implicitList:
                        if implicit[1:] in grammarInstance.tokens.keys():
                            regexToTest.append(grammarInstance.tokens[implicit[1:]]["reg"])
                else:
                    regexToTest.append(r'\s') # if there is no impilict list  we search for any white space character

                found = False
                #print "REGEXES ARE:", regexToTest
                for regex in regexToTest:
                    matches = re.compile(regex).search(word)
                    if matches:
                        #print "REGEX", regex ," matched: ", matches.groups()
                        found = True
                        break

                if not found: #if there was no white space or implicit token found between them than it belongs to the same word and is no syntax error
                    ret = False
        else:
            ret = False

        return ret

    def __getSuggestions(self, input, acPos):

        """
        Since the text returned is correct, the easy way to get the list off possibilities
        is the add a new character to cause an error at the given position.
        the parser will return a list of expected grammar elements
        :param input: the text
        :param acPos: the position we need to add to
        :return: A list of grammar elements, or an emptylist,
                 if there was a syntax error before the autocomplet requested postion
                 and an error message, this is only usefull if there was a syntax error
        """
        retList = []
        retIsSyntaxError = True
        retError = ""
        retPosLC = {"line":-1, "column":-1}
        retPosAbs = -1
        index = self.__posToAbsolute(input,acPos)

        INPUT_CHAR = u"\u200E" # this is the character that is inserted inside correct text to cause a parsing error
        #INPUT_CHAR = u"\u260E"#use this for debug this is visible
        """
        \u200E is the LEFT-TO-RIGHT markup symbol, it will do nothing to the text, there is also no chance of it appearing to the text send by the editor since left allignment is handled by css anyway
        also latin text is already left to right so it changes nothing, as a test right to left markup was used in the middle of some text and printed, the text didnt change position.
        this character is therefore safe and willas a control character never appear in the grammar, so this charcter will cause an syntax error.
        """
        newInput = input[0:index] + INPUT_CHAR + input[index:]
        #print "\nNEW INPUT = \n", newInput # if testing in windows and printing use IDLE not command prompt because it cant disalay unicode
        result = self.__currentParser.parse(newInput)
        if(result['status'] == Parser.Constants.Failure):
            retList= result["grammarelements"] #the possibilities returned by the Parser
            retPosLC = Position(result['line'], result['column'])
            retPosAbs = result['pos']
            givenPosLC = Position(acPos['line'], acPos['column'])
            #we check to see if we have gotten a syntax error that is was not caused by auto complete
            retIsSyntaxError = self.__isSyntaxError(input, retPosLC, retPosAbs, givenPosLC, index) #index = givenPosAbs , rePosAbs = errorPosAbs
            retError = result['text']
            #even if autocomplete was done correctly this is important because the error might not be at the start of the word not exactly where we put it

        return retList , retIsSyntaxError, retError, retPosLC, retPosAbs

    def __tokenRegexToString(self, value):
        """
        We do not want autocomplete to return a string like: '[a-zA-Z_][a-zA-Z_0-9]*(?!r?"|r?\')'
        we only want string literals.
        :param value:
        :return: A string if it was convertereted correctly or the empty string
        """

        #regex used to check if value is a regex
        regexStr =  r"(?<![\\])[\.\^\$\*\+\?\{\}\[\]\|\(\)]|(?<![\\])[\\](?![\\abfnrtvx\'\"\d\.\^\$\*\+\?\{\}\[\]\|\(\)])"
        regex = re.compile(regexStr)
        """
        first part:
        (?<![\\]) not preceded by the character "\"
        [\.\^\$\*\+\?\{\}\[\]\|\(\)] : . ^ $ * + ? { } [ ]  | ( ) the list of characters that need to be escaped in a regular expresion in python (except for the slash)
        in other words :any of these character not preceded by a \ means it is a regular expresion

        OR

        second part:
        (?<![\\]) not preceded by the character "\"
        [\\] the character \
        (?![\\abfnrtvx\'\"\d\.\^\$\*\+\?\{\}\[\]\|\(\)])  and not followed by any of these characters
        the characters include string escape characters \n \t (new line and tab), ascci control character \a (bell) also regex special character \$ means the literal "$" not a regex
        as well as digits for hexa and octal notation. also note that this time the slash itself is included.
        so \\ isn't a regex.
        in other words if \ is found without a preceding \ and not followed by a one of the given character it is a regex
        (unfortunately this will also allow \\\ but that gives errros on parsing anyway so it will never be given as an input)
        """

        #regex used to check the value is the slash character
        regexSlashStr = r"\s*\[\s*[\\][\\]\s*\]\s*"
        regexSlash = re.compile(regexSlashStr)
        """
        The character slash can only be written as [\\] not simply as \\. otherwise we get a parse error.
        this is a regular expresion and the previous regex will indicate so.
        we test this manually here so that if [ \\ ] is matched the character '\' will be returned for autocomplete
        """

        #regex used to select the characters needed to be replaced when transforming from regex form to string
        toReplaceRegexStr = r"[\\]([\.\^\$\*\+\?\{\}\[\]\|\(\)])"
        """
        the character \ followed by .,^,$,*,+,?,{,},[,],|,(,),]
        must be replaced by only the character that follows
        """
        ret = ''
        #so first wetest the exception case:
        isSlashChar = regexSlash.match(value) #note named as bool , but technically an object or None
        isRegex = regex.search(value) #we just need to find an instance that matches in the string no matter where it is so search instead of match
        if isSlashChar:
            ret = "\\"
        elif isRegex:
            pass
        else:
            val = re.sub(toReplaceRegexStr, r'\1', value)
            ret = val

        return ret


    def __createModelDataAC(self, text):
        #each time we parse we need to remove the previous data
        modelData = None
        tree = None

        if self.__mvkLayer:
            self.__mvkLayer.resetData()
            self.__mvkLayer.setAddingNewData()

            result = self.__currentParser.parse(text)
            if(result['status'] == Parser.Constants.Success):
                tree = result['tree']
                #Parser.PrettyPrinter().visit(tree) #TODO comment this statement later
                self.__preProcessorVis.visit(tree)
                modelData = self.__mvkLayer.visit(tree)
            else:
                partials = result['partialresults']
                modelNameRule = self.__mvkLayer.getModelNameGrammarRule()
                if modelNameRule:
                    fuser = PartialTreeFuser()
                    treeAr = fuser.fuse(partials, self.__metaModelGrammar, self.__currentParser.implicitRuleName,modelNameRule)

                    for tree in treeAr:
                        self.__preProcessorVis.visit(tree)
                        modelData = self.__mvkLayer.visit(tree)
                        #print "Model data = ", modelData.toStr()
            #if tree:
            #    self.__preProcessorVis.visit(tree)
            #    modelData = self.__mvkLayer.visit(tree)

        return modelData

    def __autoComplete(self, suggestionList, text, absPos):
        """
        this is the version of autocomplete that should be used when autocomplete is asked on a completed text
        :param suggestionList: the list of suggestion from the parser
        :param text the parsed text
        :param absPos: the absolute position: the index of the error in the string, (not relative to any line number)
        :return: A list of tuples (value, bool) where value is an autocomplete suggestion and
        bool whether it should be selectable (True) or not (False) meaning the suggestion is only there as a hint
        """
        retSet = set() #a set because we want each suggestion to be unique, so even if we end up adding the same suggestion mutliple times. it will omly be kept one times

        map = None
        mappingKeys = []
        if self.__mvkLayer:
            map = self.__mvkLayer.getAugmentedModelMap()
            mappingKeys = map.keys()

        grammarInstance = self.__metaModelGrammar

        inverseMapping = grammarInstance.getInverseMapping() #maps tokens and rules to rules that contains them
        memoTable = self.__currentParser.memotable #TODO use a getter

        modelData = None

        for suggestion in suggestionList:
            m = re.compile('[A-Z_][A-Z_0-9]*').match(suggestion)
            if m: # A Token
                reg = grammarInstance.tokens[suggestion]["reg"]
                #print "TOKEN REGEX is:", reg
                st = self.__tokenRegexToString(reg)
                if st:
                    retSet.add((st, True))
                    #print "TOKEN STRING VERSION IS :", st
                else:
                    #print "TOKEN STRING VERSION IS : NONE"
                    resultCount = 0
                    if mappingKeys: #if there might be something we can map to
                        pathList = self.__getProbableHierarchy(suggestion, absPos, inverseMapping, memoTable)
                        #print "\tthe possible hierarchy is therefore: ", pathList
                        """
                        #For tokens we test 3 posibilites: the token itself , full hierarchy , hierarchy without token name
                        #so for example, IDENTIFIER, arc_declaration.destination.IDENTIFIER, arc_declaration.destination
                        #this is a descsion made of personal experience:
                        IDENTIFIER itself is unlikely to be mapped because it could belong to to many things
                        arc_declaration.destination.IDENTIFIER has already more chance; but if for example:
                        destination: IDENTIFIER (SLASH IDENTIFIER)*
                        in that case it is much more likely that 'destination' is mapped to something than destination.IDENTIFIER

                        because we check with endswith the cases IDENTIFER and  arc_declaration.destination.IDENTIFIER
                        will both return true in case something is mapped to IDENTIFIER so we only need to test
                        the full hierarchy and the hierarchy without the token name
                        """

                        toTestList = []
                        removeStr = '.'+ suggestion
                        for path in pathList:
                            toTestList.append(path)
                            index = path.rindex(removeStr)
                            shortPath = path[0:index]
                            toTestList.append(shortPath)

                        for path in toTestList:
                            for key in mappingKeys:
                                if (path.endswith(key)) and (map[key]["type"] == 'Reference'):
                                    resultCount += 1
                                    toMap = map[key]["refers_to"]
                                    #print "searching For instances of", toMap

                                    if not modelData: #if modelData wasn't created yet we do it now
                                        modelData= self.__createModelDataAC(text)

                                    #TODO in the future it might be better to check on the level given the position but for now checking the model level is enough
                                    if modelData: #if the model data was created and is not empty
                                        for child in modelData.children:
                                            if child.mapping == toMap:
                                                retSet.add((child.value, True))
                    else:
                        pass

                        #This works but i just dont like this behaviour its not consistent with the other ac behaviour
                        #tokenFinder = TokenFinderVisitor()
                        #tokenValues = tokenFinder.visit(tree, suggestion)
                        #resultCount = len(tokenValues)
                        #for value in tokenValues:
                        #    retSet.add((value, True))

                        #if there is no model data we just look at the instances of the given token kind, this will of course be less precis
                        #tokenInstances = self.__getTokenValues(tree, suggestion)

                    if  resultCount == 0:
                        #we add it as an unselectable hint
                        retSet.add((grammarInstance.tokens[suggestion]["errortext"],  False))

            elif not suggestion in grammarInstance.rules:
                #an anonymous token, written directly into the grammar, we add is a suggestion without the quotes
                retSet.add((suggestion[1:-1], True))
            else: # a rule
                resultCount = 0
                if mappingKeys: #if there might be something we can map to
                    #print "Suggestion is a rule:"
                    pathList = self.__getProbableHierarchy(suggestion, absPos, inverseMapping, memoTable)
                    resultCount = 0

                    #print "\tthe possible hierarchy is therefore: ", pathList

                    #For a rule we test all hierarchies and the rule itself, we do not test hierarchy without the rule
                    #but again since we test with ends with there is no need to have a sperate test for full hierarchy and rule itself
                    #so we just test the gotten results
                    toTestList = pathList #[suggestion] + pathList

                    for path in toTestList:
                        for key in mappingKeys:
                            if (path.endswith(key)) and (map[key]["type"] == 'Reference'):
                                resultCount += 1
                                toMap = map[key]["refers_to"]
                                #print "searching For instances of", toMap

                                if not modelData: #if modelData wasn't created yet we do it now
                                    modelData= self.__createModelDataAC(text)

                                #TODO in the future it might be better to check on the level given the position but for now checking the model level is enough
                                if modelData: #if the model data was created and is not empty
                                    for child in modelData.children:
                                        if child.mapping == toMap:
                                            retSet.add((child.value, True))
                if  resultCount == 0:
                    #add the rule error message as a suggestion
                    retSet.add((grammarInstance.rules[suggestion]["errortext"], False))

        retList = list(retSet)
        #print retList
        retList.sort()
        return retList

    def __getProbableHierarchy(self, itemName, pos, invMapping, memoTable):
        """
        :param itemName: the rule or token name
        :param pos: the absolute position. INTEGER not a postion class instance, because the memo table uses ints
        :param memoTable:
        :return:
        """

        # assume IDENTIFIER (child of destination which is itself child of arc declaration)
        # the memo table contains a IDENTIFIER and destination but not arc decl
        # we look at all the rules in the grammar that have an identifier: we find a couple
        # we look in the memo table to see if we find instance of a rule which covers the same postion (in this case only destination)
        # we then look at all the rules containing destination>
        # we look for it in the memo table containing with the same position.... ()
        # and we start again ...
        # when we do not find a rule it means it is the most probable parent missing (its missing because it wasn't matched)

        class MemoTree(object):
            #A class to save already visited paths to avoid infinte loops
            #in case of recurisve calls
            def __init__(me, key, p):
                me.key = key
                me.pos = p
                me.parent = None
                me.children = []

            def addChild(me, child):
                child.parent = me
                me.children.append(child)

            def isInPath(me, key, pos):

                if me.key == key and me.pos == pos:
                    return True
                else:
                    parent = me.parent
                    while parent:
                        if parent.key == key and parent.pos == pos:
                            return True
                        else:
                            parent = parent.parent
                    return False

            def getPath(me):
                pathAr = [me.key]
                parent = me.parent
                while parent:
                    pathAr.append(parent.key)
                    parent = parent.parent

                pathStr = pathAr[0]
                for i in range(1, len(pathAr)):
                    pathStr =   pathStr + '.' + pathAr[i]

                return pathStr

        #def getHierarchyHelper(key, startPos, endPos, parent):
        def getHierarchyHelper(key, startPos, parent):
            m = MemoTree(key,startPos)
            parent.addChild(m)
            rules = invMapping[key]
            h = []
            if rules:
                for rule in rules:
                    f = False # not found
                    for tup in memoTable.keys():
                        #tup[0] contains the name starting with @, tup[0] contains the
                        #we also make sure that the dictionary is filled , not empty
                        #if (tup[0][1:] == rule) and memoTable[tup]:
                        if (tup[0][1:] == rule) and (tup[1] == pos):
                            """
                            for elem in memoTable[tup]:
                                if (elem["startpos"] <= pos) and (elem["endpos"] >= pos): #if its there continue searching and add to the hierarchy
                                    if not m.isInPath(rule,elem["startpos"]): #if we havent ecnountered this before in this path
                                        f = True #found
                                        h += getHierarchyHelper(rule, elem["startpos"], elem["endpos"])
                                else:
                                    #this alternative has already been added to the path. we encounter it again
                                    ## because we are going in circles, abondon this branch and try something else
                                    pass
                            """
                            if tup[1] == pos:
                                found = True
                                #hierarchy += getHierarchyHelper(rule, elem["startpos"], elem["endpos"],m)
                                if not m.isInPath(rule,pos): #if we havent ecnountered this before in this path
                                        f = True #found
                                        h += getHierarchyHelper(rule, pos, m)

                    if not f:
                        path =   rule + '.' + m.getPath()
                        h.append(path)
            return h

        memoTree = MemoTree(itemName, pos)
        rules = invMapping[itemName]
        hierarchy = []
        if rules:
            for rule in rules:
                found  = False
                for tup in memoTable.keys():
                    #tup[0] contains the name starting with @, tup[0] contains the
                    #we also make sure that the dictionary is filled , not empty
                    #if (tup[0][1:] == rule) and memoTable[tup]:
                    if (tup[0][1:] == rule) and (tup[1] == pos):
                            #for elem in memoTable[tup]:
                            #if (elem["startpos"] <= pos) and (elem["endpos"] >= pos): #if its there continue searching and add to the hierarchy
                            found = True
                            #hierarchy += getHierarchyHelper(rule, elem["startpos"], elem["endpos"],memoTree)
                            hierarchy += getHierarchyHelper(rule, pos, memoTree)

                if not found:
                    path = rule + '.' + itemName
                    hierarchy.append(path)


        #print "RULES HIERARCHY =", hierarchy
        return hierarchy

    """
    this methods were here with the idea of trying to find the bext token to make sure that autcomplete did not propose stuff that was already there
    the problem was that this might cause unwanted removals in some cases were tokens can be repeated or when tokens are the same but part of a different rule
    so this was dropped.kept here in case a more complex wayof doing the same is added these can be a good starting point

    def __getNextToken(self,tree, token, pos, implicitList):

        #We get the next token that follows the given position,
        #:param tree: the current parse tree
        #:param pos an instance of the Position class
        #:return:
        def isTokenImpl(tok):
            t = "$" + tok.head
            return (t in implicitList)

        def getLeaves(tree ):
            #given a node find all its leaves
            ret = []
            if not isinstance(tree.tail[0], basestring):
                for elem in tree.tail:
                    ret += getLeaves(elem)
            else:
                ret.append(tree)
            return ret

        def getRightSibbling(tok):
            ret = None
            if tok.parent:
                parent = tok.parent
                index = parent.tail.index(tok)
                siblings = parent.tail[index+1:]
                if siblings:
                    ret = getLeaves(siblings[0])[0]
                else:
                    ret = getRightSibbling(parent)
            return ret


        ret = None
        sib = None
        if token:
            #print "Token at pos ", pos , ": ",  token.head,  " = " , str(token.tail[0])
            stop = False
            if pos <= token.startpos or pos < token.endpos:
                sib = token
            else:
                sib = getRightSibbling(token)

            while sib and not stop:
                if isTokenImpl(sib):
                    sib = getRightSibbling(sib)
                else:
                    stop = True
                    ret = sib
        else:
            #print "Current token is none"
            pass

        #if sib:
        #    print "Next sibling is: ",  sib.head,  " = " , str(sib.tail[0])
        return ret

    def __findTokenAtPosition(self, tree, pos):
        #return the token for the given position
        #:param tree:
        #:param pos:
        #:return: A tree node of a token, if the given position is before the first token  (leaf) return that and if after the last return None

        #first check extremities:
        if pos <= tree.startpos:
            #return the left most Token
            item = tree
            while item and not isinstance(item.tail[0], basestring):
                item = item.tail[0]
            return item

        elif pos >= tree.endpos:
            return None #even if equal ,endpos is not included in the tree
        else:
            return self.__findTokenAtPosHelper(tree,pos)

    def __findTokenAtPosHelper(self, tree,pos):
        if isinstance(tree, Tree):
            l = len(tree.tail)
            for i in range(l):
                child  = tree.tail[i]
                rightSibling = None
                if i + 1 < l:
                    rightSibling = tree.tail[i+1]

                if pos >= child.startpos and pos < child.endpos:
                    if child.tail and isinstance(child.tail[0], Tree):
                        return self.__findTokenAtPosHelper(child,pos)
                    else:
                        return child
                elif rightSibling: #if the given position is between tokens (remember this will most likely be called with implicit hidden so white spaces wont be in the tree)
                    if pos >= child.endpos and pos < rightSibling.startpos:
                        return child #return the left one
        return None
    """