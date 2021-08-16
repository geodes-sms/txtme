__author__ = 'daniel'

#import grammarRequestHandler
import sys, os
from grammarRequestHandler import *
from saveLoadRequestHandler import *
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

    #both mapper and grammar are in the same file otherwise we need another dictionary key for the mapper


    #"""
    #this is the input that will be gotten by the editor
    text = "Petrinet test\n"
    text += "//this is a comment\n"
    text += "Place p0;\n"
    text += "Transition t0;\n"
    text += "end"
    #"""
    #text = read("grammar_parser_v2/models/examples/petri_badv2.pn")

    readFileReqDic = {}
    readFileReqDic["input"] = text

    text2 = "Petrinet test\n"
    text2 += "//this is a comment\n"
    text2 += "Place p0;\n"
    text2 += "end"

    readFileReqDic2 = {}
    readFileReqDic2["input"] = text2


    text3 = "Petrinet test\n"
    text3 += "Place p0;\n"
    text3 += "Arc a: from p0 to t0;\n"
    text3 += "end"
    #text3 = "sdsdsdsdsd\n"

    readFileReqDic3 = {}
    readFileReqDic3["input"] = text3

    text4 = "Petrinet test\n"
    text4 += "Place p0;\n"
    text4 += "Transition t0;\n"
    text4 += "Arc a0: from p0 to t0;\n"
    #text4 += "end"

    readFileReqDic4 = {}
    readFileReqDic4["input"] = text4

    ######
    #TEST
    #####

    def test1():
        # 1) load the grammar
        loadRet = gramReqHndlr.proccessLoadGrammarRequest(loadGrammarReqDic)
        print "response for load request: ", loadRet
        """
        # 2) read the text the first time
        ret = gramReqHndlr.processCheckTextRequest(readFileReqDic)
        print "response reading 1: ", ret , "\n"
        # 3) read the same text a second time , things will go wrong here
        ret = gramReqHndlr.processCheckTextRequest(readFileReqDic)
        print "response reading 2: ", ret
        ret = gramReqHndlr.processCheckTextRequest(readFileReqDic2)
        print "response reading 3: ", ret
        """

         # 2) read the text the first time
        #ret = gramReqHndlr.processCheckTextRequest(readFileReqDic3)
        #print ret
        ret = gramReqHndlr.processCheckTextRequest(readFileReqDic4)
        print ret


    ##########################################

    #test temporary creation
    textRead1 = "Petrinet test\n"
    textRead1 +="Place p0;\n"
    textRead1 +="Place p1;\n"
    textRead1 +="Transition t0;\n"
    textRead1 +="Arc from p0 to p1;\n" #syntax error here will cause a half created model, not the fact that we are connecting two places
    textRead1 +="end"


    textRead2 = "Petrinet test\n"
    textRead2 +="Place p0;\n"
    textRead2 +="Place p1;\n"
    textRead2 +="Transition t0;\n"
    textRead2 +="Arc a0: from p0 to p1;\n" #syntax model repaired
    textRead2 +="end"


    textRead3 = "Petrinet test\n"
    textRead3 +="Place p0;\n"
    textRead3 +="Place p1;\n"
    textRead3 +="Transition t0;\n"
    textRead3 +="Arc a0: from p0 to t0;\n" #syntax model repaired
    textRead3 +="end"

    textRead4 = "Petrinet test\n"
    textRead4 +="Place p0;\n"


    readFileReqDic4 = {}
    readFileReqDic4["input"] = textRead1

    readFileReqDic5 = {}
    readFileReqDic5["input"] = textRead2

    readFileReqDic6 = {}
    readFileReqDic6["input"] = textRead3

    readFileReqDic7 = {}
    readFileReqDic7["input"] = textRead4




    def test2():
        loadRet = gramReqHndlr.proccessLoadGrammarRequest(loadGrammarReqDic)
        print "response for load request: ", loadRet


        print "\n#### 1\n"
        ret = gramReqHndlr.processCheckTextRequest(readFileReqDic4)
        print "READ ONE: ",  ret

        print "\n#### 2\n"
        ret = gramReqHndlr.processCheckTextRequest(readFileReqDic6)
        print "READ TWO: ", ret

        print "\n#### 3\n"
        ret = gramReqHndlr.processCheckTextRequest(readFileReqDic5)
        print "READ THREE: ", ret

        print "\n#### 4\n"
        ret = gramReqHndlr.processCheckTextRequest(readFileReqDic7)
        print "READ FOUR: ", ret

        print "\n#### 5\n"
        ret = gramReqHndlr.processCheckTextRequest(readFileReqDic5)
        print "READ FIVE: ", ret

        print "\n#### 6\n"
        ret = gramReqHndlr.processCheckTextRequest(readFileReqDic7)
        print "READ SIX: ", ret


        print "\n#### 7\n"
        ret = gramReqHndlr.processCheckTextRequest(readFileReqDic4)
        print "READ SEVEN: ", ret
        #print "READ TWO should either be created or not created because name wasnt valid"
        #print "if the error message is: couldnt be created because name already exists the test has failed"

    def testSave():
        saveReqHndlr = SaveLoadRequestHandler('temp')

        saveReqDefault = {}
        saveReqDefault['filename'] = 'foobar.txt'
        #saveReqDefault['editor_id'] = ''
        saveReqDefault['content'] = 'foobar'

        saveReqId = {}
        saveReqId['filename'] = 'foobar2.txt'
        saveReqId['editor_id'] = 'subflodertest'
        saveReqId['content'] = 'foobar2'

        ret = saveReqHndlr.processSaveRequest(saveReqDefault)
        print ret
        ret = saveReqHndlr.processSaveRequest(saveReqId)
        print ret

    def testLoad():

        loadReqHndlr = SaveLoadRequestHandler('temp')

        loadReq = {}
        loadReq['filename'] = './temp/test_doc.txt'
        ret = loadReqHndlr.processLoadRequest(loadReq)
        print ret


    def testMultiLoadGrammar():

        textRead1 = "Petrinet test\n"
        textRead1 +="Place p0;\n"
        textRead1 +="Transition t0;\n"
        textRead1 +="end"

        loadRet = gramReqHndlr.proccessLoadGrammarRequest(loadGrammarReqDic)
        print "response for load request: ", loadRet

        readFileReqDic = {}
        readFileReqDic["input"] = textRead1
        ret = gramReqHndlr.processCheckTextRequest(readFileReqDic)
        print "response first check error", ret

        loadRet = gramReqHndlr.proccessLoadGrammarRequest(loadGrammarReqDic)
        print "response for load request: ", loadRet

        readFileReqDic = {}
        readFileReqDic["input"] = textRead1
        ret = gramReqHndlr.processCheckTextRequest(readFileReqDic)
        print "response first check error", ret

    def testLoadDefaulyStyle():
        loadGrammarReqDic3 = {}
        loadGrammarReqDic3["grammar"] = 'grammar_parser_v2/grammars/examples/meta_grammar.g'
        loadGrammarReqDic3["metamap"] = ''
        loadGrammarReqDic3["styledef"] = ''
        loadGrammarReqDic3["stylemap"] = ''
        loadRet = gramReqHndlr.proccessLoadGrammarRequest(loadGrammarReqDic3)
        print "response for load request: ", loadRet
        text = "grammar{\n"
        text+= "start: 'foo' 'bar';\n}"

        readFileReqDic = {}
        readFileReqDic["input"] = text
        ret = gramReqHndlr.processCheckTextRequest(readFileReqDic)
        print "response first check error", ret



    def testTokenCount(): #not a realtest jsut need to to know the token count of some text for the javascript testcases
        loadGrammarReqDic3 = {}
        loadGrammarReqDic3["grammar"] = 'grammar_parser_v2/grammars/examples/meta_grammar.g'
        loadGrammarReqDic3["metamap"] = ''
        loadGrammarReqDic3["styledef"] = ''
        loadGrammarReqDic3["stylemap"] = ''

        loadRet = gramReqHndlr.proccessLoadGrammarRequest(loadGrammarReqDic3)
        print "response for load request: ", loadRet

        #/*x is the number of repetition of a specif part of text. #lines = 3 + x*2 , #tokens = 20 +x*10
        #X must be at least once or model will be illegal (check error will return an error)
        #x = 1 => 5 lines , 30 tokens
        #x = 8 => 19 lines,   100 tokens
        #x = 48 => 99 lines,  500 tokens
        #x = 98 => 199 lines, 1000 tokens

        #x = 98
        #input = "Petrinet test\n" #1 line, 4 tokens
        #for  i in range(x):   #2 lines , 10 tokens
        #    input += "Place p" + str(i) + ";\n"
        #    input += "Transition t" + str(i) + ";\n"
        #input += "Arc a0 : from p0 to t0;\n" # 1 line, 15 tokens
        #input += "end"; #1 line, 1 token

        input = "grammar{\n"
        input +="    start: PETRINET name ( place_decl | transition_decl | arc_decl ) * END;\n\n"
        input +="    place_decl: PLACE name place_def? SEMICOL;\n\n"
        input +="    place_def: LCBR (tokens_def (COMMA capacity_def)?|capacity_def(COMMA tokens_def)?) RCBR;\n"
        input +="    capacity_def: CAPACITY COLON integer;\n"
        input +="    tokens_def: TOKENS COLON integer;\n"
        input +="    transition_decl: TRANSITION name SEMICOL;\n\n"
        input +="    arc_decl: ARC name weight_def? COLON FROM source TO destination SEMICOL;\n\n"
        input +="    weight_def: LCBR WEIGHT COLON integer RCBR;\n\n"
        input +="    name: IDENTIFIER;\n"
        input +="    source: IDENTIFIER;\n"
        input +="    destination: IDENTIFIER;\n"
        input +="    integer: DIGIT+;\n\n"

        input +="    start: PETRINET name ( place_decl | transition_decl | arc_decl ) * END;\n\n"
        input +="    place_decl: PLACE name place_def? SEMICOL;\n\n"
        input +="    place_def: LCBR (tokens_def (COMMA capacity_def)?|capacity_def(COMMA tokens_def)?) RCBR;\n"
        input +="    capacity_def: CAPACITY COLON integer;\n"
        input +="    tokens_def: TOKENS COLON integer;\n"
        input +="    transition_decl: TRANSITION name SEMICOL;\n\n"
        input +="    arc_decl: ARC name weight_def? COLON FROM source TO destination SEMICOL;\n\n"
        input +="    weight_def: LCBR WEIGHT COLON integer RCBR;\n\n"
        input +="    name: IDENTIFIER;\n"
        input +="    source: IDENTIFIER;\n"
        input +="    destination: IDENTIFIER;\n"
        input +="    integer: DIGIT+;\n\n"

        input +="    start: PETRINET name ( place_decl | transition_decl | arc_decl ) * END;\n\n"
        input +="    place_decl: PLACE name place_def? SEMICOL;\n\n"
        input +="    place_def: LCBR (tokens_def (COMMA capacity_def)?|capacity_def(COMMA tokens_def)?) RCBR;\n"
        input +="    capacity_def: CAPACITY COLON integer;\n"
        input +="    tokens_def: TOKENS COLON integer;\n"
        input +="    transition_decl: TRANSITION name SEMICOL;\n\n"
        input +="    arc_decl: ARC name weight_def? COLON FROM source TO destination SEMICOL;\n\n"
        input +="    weight_def: LCBR WEIGHT COLON integer RCBR;\n\n"
        input +="    name: IDENTIFIER;\n"
        input +="    source: IDENTIFIER;\n"
        input +="    destination: IDENTIFIER;\n"
        input +="    integer: DIGIT+;\n\n"




        input +="    tokens{\n"
        input +="       // TOKENS (written in CAPS)\n"
        input +="       IDENTIFIER: '[a-zA-Z_][a-zA-Z_0-9]*' @Msg 'Identifier';\n\n"
        input +="       keywords:pn{\n"
        input +="           PETRINET: 'Petrinet';\n"
        input +="           PLACE: 'Place';\n"
        input +="           TRANSITION: 'Transition';\n"
        input +="           ARC: 'Arc';\n"
        input +="           WEIGHT: 'weight';\n"
        input +="           CAPACITY: 'capacity';\n"
        input +="           TOKENS: 'tokens';\n"
        input +="           PETRINET: 'Petrinet';\n"
        input +="           PLACE: 'Place';\n"
        input +="           TRANSITION: 'Transition';\n"
        input +="           ARC: 'Arc';\n"
        input +="           WEIGHT: 'weight';\n"
        input +="           CAPACITY: 'capacity';\n"
        input +="           TOKENS: 'tokens';\n"
        input +="       }\n\n"
        input +="       keywords:general{\n"
        input +="           END: 'end';\n"
        input +="           FROM: 'from';\n"
        input +="           TO: 'to';\n"
        input +="       }\n\n"
        input +="       COLON: ':';\n"
        input +="       LPAR: '\(' @Msg '(';\n"
        input +="       RPAR: '\)' @Msg ')';\n"
        input +="       COMMA: ',';\n"
        input +="       SEMICOL: ';';\n"
        input +="       LCBR: '\{' @Msg '{';\n"
        input +="       RCBR: '\}' @Msg '}';\n\n"
        input +="       DIGIT: '[0-9]' @Msg 'Digit';\n\n"
        input +="       NEWLINE: '(\\n?\\n[\\t ]*)+' @Impl @Msg 'New Line';\n"
        input +="       LINE_CONT: '\\\\[\\t \\f]*\\n?\\n' @Impl @Msg 'Line Continuation';\n"
        input +="       WS: '[\\t \\f]+' @Impl @Msg 'White Space';\n"
        input +="       COMMENT: '//[^\\n]*' @Cmnt @Msg 'Comment';\n"
        input +="    }\n"
        input +="}\n\n"
        input +="mapper{\n\n"
        input +="    start -> @Model MyFormalisms.PetriNet{\n"
        input +="        start.name -> @Attr name;\n\n"
        input +="        place_decl -> @Class Place {\n"
        input +="            place_decl.name -> @Attr name;\n"
        input +="            tokens_def.integer -> @Attr token;\n"
        input +="            capacity_def.integer -> @Attr capacity;\n"
        input +="        }\n\n"
        input +="        transition_decl-> @Class Transition {\n"
        input +="            transition_decl.name -> @Attr name;\n"
        input +="        }\n\n"
        input +="        arc_decl-> @Assoc InArc{\n"
        input +="            arc_decl.name -> @Attr name;\n"
        input +="            weight_def.integer -> @Attr weight;\n"
        input +="            arc_decl.source -> @Ref from_port;\n"
        input +="            arc_decl.destination -> @Ref to_port;\n"
        input +="        }\n"
        input +="     start.name -> @Attr name;\n\n"
        input +="        place_decl -> @Class Place {\n"
        input +="            place_decl.name -> @Attr name;\n"
        input +="            tokens_def.integer -> @Attr token;\n"
        input +="            capacity_def.integer -> @Attr capacity;\n"
        input +="        }\n\n"
        input +="        transition_decl-> @Class Transition {\n"
        input +="            transition_decl.name -> @Attr name;\n"
        input +="        }\n\n"
        input +="        arc_decl-> @Assoc InArc{\n"
        input +="            arc_decl.name -> @Attr name;\n"
        input +="            weight_def.integer -> @Attr weight ;\n"
        input +="            arc_decl.source -> @Ref from_port ;\n"
        input +="        }\n"



        input +="    }\n"
        input +="}"


        readFileReqDic = {}
        readFileReqDic["input"] = input
        ret = gramReqHndlr.processCheckTextRequest(readFileReqDic)
        print "response first check error", ret

    def testJSTestCase():
        textRead1 = "Petrinet test\n"
        textRead1 +="Place p0;\n"
        textRead1 +="Transition t0;\n"
        textRead1 +="Place p1;\n"
        textRead1 +="Transition t1;\n"
        textRead1 +="Place p2;\n"
        textRead1 +="Transition t2;\n"
        textRead1 +="Place p3;\n"
        textRead1 +="Transition t3;\n"
        textRead1 +="Place p4;\n"
        textRead1 +="Transition t4;\n"
        textRead1 +="Place p5;\n"
        textRead1 +="Transition t5;\n"
        textRead1 +="Place p6;\n"
        textRead1 +="Transition t6;\n"
        textRead1 +="Place p7;\n"
        textRead1 +="Transition t7;\n"
        textRead1 +="Arc a0 : from p0 to t0;\n" #syntax model repaired
        textRead1 +="end"


        loadRet = gramReqHndlr.proccessLoadGrammarRequest(loadGrammarReqDic)
        print "response for load request: ", loadRet

        readFileReqDic = {}
        readFileReqDic["input"] = textRead1
        ret = gramReqHndlr.processCheckTextRequest(readFileReqDic)
        print "response  check error 1", ret

        acReqDic = {}
        acReqDic["input"] =  textRead1
        acReqDic["position"] = {"line": 18, "column" : 20}

        acRet = gramReqHndlr.processAutoCompleteRequest(acReqDic)
        print "acresponse", acRet


        #loadRet = gramReqHndlr.proccessLoadGrammarRequest(loadGrammarReqDic)
        #print "response for load request: ", loadRet

        #ret = gramReqHndlr.processCheckTextRequest(readFileReqDic)
        #print "response  check error 2", ret


    #test1()
    #test2()
    testJSTestCase()
    #testSave() #TESTSAVE MUST BE EXECUTED FROM THE ROOT of the project
    #testLoad()
    #testMultiLoadGrammar()
    #testLoadDefaulyStyle()
    #testTokenCount() #not a realtest jsut need to to know the token count of some text for the javascript testcases

if __name__ == '__main__':
    sys.exit(main())