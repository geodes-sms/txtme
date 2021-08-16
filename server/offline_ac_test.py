__author__ = 'daniel'

#import grammarRequestHandler
import sys, os
from grammarRequestHandler import *
from mvk.mvk import MvK

def read(n, *args):
  CUR_PATH = os.path.split(__file__)[0]
  with open(os.path.join(CUR_PATH, n), *args, encoding='utf-8') as f:
    return f.read()

def main():

    #####
    #SETUP
    #####

    gramReqHndlr = GrammarRequestHandler(MvK())

    #the 2 input files, the python versions of the dictionaries that would be gotten by the POST request in json for

    #in the future the name of the grammar will refer to something from the modelverse for the moment they  are hardcoded grammar files
    #the value of the key- value pair are therefore empty but the hardcoded will only load if the keys are there
    loadGrammarReqDic = {}
    #loadGrammarReqDic["grammar"] = 'grammar_parser_v2/grammars/examples/petrinet.g'
    loadGrammarReqDic["grammar"] = 'grammar_parser_v2/grammars/examples/petrinet.g'
    loadGrammarReqDic["metamap"] = 'grammar_parser_v2/grammars/examples/petrinet.g'
    loadGrammarReqDic["styledef"] = 'grammar_parser_v2/models/examples/petri_style.st'
    loadGrammarReqDic["stylemap"] = 'grammar_parser_v2/models/examples/petri_style.st'

    loadGrammarReqDic2 = {}
    loadGrammarReqDic2["grammar"] = 'grammar_parser_v2/grammars/examples/petrinet.g'
    loadGrammarReqDic2["metamap"] = '' #testing autcomplete witouth metamodel
    loadGrammarReqDic2["styledef"] = ''
    loadGrammarReqDic2["stylemap"] = ''

    #both mapper and grammat are in the same file otherwise we need another dictionary key for the mapper

    #"""
    #this is the input that will be gotten by the editor
    text = "Petrinet test\n"
    text += "//this is a comment\n"
    text += "Place p0;\n"
    text += "Transition t0;\n"
    text += "Arc a0: from p0 to t0;\n"
    #text += "t0 to p0 Arc a0;"
    text += "end"
    #"""

    acReqDic = {}
    acReqDic["input"] =  text
    acReqDic["position"] = {"line": 3, "column" : 9}
    #acReqDic["position"] = {"line": 5, "column" : 19}
    #acReqDic["position"] = {"line": 3, "column" : 1}


    ertext = "Petrinet test\n"
    ertext += "//this is a comment\n"
    ertext += "Place p0;\n"
    ertext += "Transition t0;\n"
    ertext += "Arc a0: from p0 to \n"
    ertext += ""

    acErrorReqDic = {}
    acErrorReqDic["input"] =  ertext
    acErrorReqDic["position"] = {"line": 5, "column" : 19}


    ertext2 = "Petrinet test\n"
    ertext2 += "//this is a comment\n"
    ertext2 += "Place p0 ;\n"

    acErrorReqDic2 = {}
    acErrorReqDic2["input"] =  ertext2
    acErrorReqDic2["position"] = {"line": 3, "column" : 9}

    ertext3 = "Petrinet test\n" #test to test that AC will not give a syntax error because of the p but will treat is a part of the word currently being written
    ertext3 += "P\n" #P folowd by a space and postion line 2 col 3 must give a syntax error

    acErrorReqDic3 = {}
    acErrorReqDic3["input"] =  ertext3
    acErrorReqDic3["position"] = {"line": 2, "column" : 2}

    ertext3 = "Petrinet test\n" #test to test that AC will give a syntax error because of the p followed by a space
    ertext3 += "P \n"

    acErrorReqDic3 = {}
    acErrorReqDic3["input"] =  ertext3
    acErrorReqDic3["position"] = {"line": 2, "column" : 3}

    #NOT AC just here to check partial results
    text0 = "Petrinet test\n"
    text0 += "Place p0;\n"
    text0 += "Arc a: from p0 to;\n"
    text0 += "end"

    errorReqDic = {}
    errorReqDic["input"] =  text0

    ######
    #TEST
    #####

    #TEST with metamodel
    def testMeta():
        # 1) load the grammar
        loadRet = gramReqHndlr.proccessLoadGrammarRequest(loadGrammarReqDic)
        print "response for load request: ", loadRet

         # 2) read the text
        #ret = gramReqHndlr.processAutoCompleteRequest(acReqDic)
        #acErrorReqDic["position"] = {"line": 4, "column" : 11}
        ret = gramReqHndlr.processAutoCompleteRequest(acErrorReqDic) #reference test
        print ret
        ret = gramReqHndlr.processAutoCompleteRequest(acErrorReqDic2) #tokens test
        print ret
        ret = gramReqHndlr.processAutoCompleteRequest(acErrorReqDic3) #syntax error test
        print ret

    def testNoMeta():
        #test without meta model
        loadRet = gramReqHndlr.proccessLoadGrammarRequest(loadGrammarReqDic2)
        print "response for load request: ", loadRet
        #acErrorReqDic["position"] = {"line": 4, "column" : 11}
        ret = gramReqHndlr.processAutoCompleteRequest(acErrorReqDic)
        print ret

    testMeta()
    #testNoMeta()
if __name__ == '__main__':
    sys.exit(main())