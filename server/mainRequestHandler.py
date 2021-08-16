"""
The application our server is running

adapted by:
Daniel Riegelhaupt, 2014
"""

from responseSerializer import ResponseSerializer
from saveLoadRequestHandler import SaveLoadRequestHandler
from grammarRequestHandler import GrammarRequestHandler
import json

from mvk.mvk import MvK

class MainRequestHandler():
    """
    The main (POST) request handler of our server application
    it handles general request and passes specific request to their handlers
    """
    INSTANCE = None

    def __init__(self, tempSaveDirectory):
        self.__isOpen = True
        self.__modelVerse = MvK()

        self.__saveLoadReqHandlerDict = SaveLoadRequestHandler(tempSaveDirectory)
        self.__grammarReqHandlerDict = {'default': GrammarRequestHandler(self.__modelVerse)}

    def __closeAfterDelete(self,reqDic):
        ret = False
        if reqDic.has_key('editor_id'): #if there is an editor id only close that editor
            editorId = self.__grammarReqHandlerDict[str(reqDic['editor_id'])]
            if self.__grammarReqHandlerDict.has_key(editorId):
                del self.__grammarReqHandlerDict[editorId]

                keys = self.__grammarReqHandlerDict.keys()
                l = len(keys)

                if l == 0 or (l ==1 and (keys[0] == 'default')): #if after delete there are no more editors orthe only one left is defualt ,close evrything
                    ret =  True
        else: #if there is no editro id close the whole thing
            ret = True

        return ret


    #process a request from the server
    def processRequest(self, request):
        #input the key value pairs in the dictionary
        reqDic = json.loads(request)

        #if the dictionary contains a command procees the command request accordingly
        if reqDic.has_key('command'):
            if reqDic['command'] == 'save':
                return self.__saveLoadReqHandlerDict.processSaveRequest(reqDic)
            elif reqDic['command'] == 'load':
                return self.__saveLoadReqHandlerDict.processLoadRequest(reqDic)
            elif reqDic['command'] == 'close':
                if self.__closeAfterDelete(reqDic):
                    self.__isOpen = False
                return ResponseSerializer.success({"message": "close command received"})
            else:
                return ResponseSerializer.error("ERROR unknown command!")
        elif reqDic.has_key('grammar_command'):
            #get the editor id
            editorId = 'default'
            if reqDic.has_key('editor_id'):
                editorId = str(reqDic['editor_id'])
            else:
                print 'Warning. no editor id specified, will use editor id \'defualt\''

            #create a grammar request handler for the new editor
            if not self.__grammarReqHandlerDict.has_key(editorId):
                self.__grammarReqHandlerDict[editorId] = GrammarRequestHandler(self.__modelVerse)

            #finnaly process the request
            if reqDic['grammar_command'] == 'load_grammar':
                print "received load grammar request from", editorId
                return self.__grammarReqHandlerDict[editorId].proccessLoadGrammarRequest(reqDic)
            #elif reqDic['grammar_command'] == 'keywords_request':  #this might be better in GET ?
            #    return self.__grammarReqHandler.processKeywordsRequest(reqDic)
            elif reqDic['grammar_command'] == 'check_text':
                return self.__grammarReqHandlerDict[editorId].processCheckTextRequest(reqDic)
            elif reqDic['grammar_command'] == 'auto_complete':
                return self.__grammarReqHandlerDict[editorId].processAutoCompleteRequest(reqDic)
            else:
                return ResponseSerializer.error("ERROR unknown grammar command: '" + reqDic['grammar_command']+ "'!")
        else:
            return ResponseSerializer.error("ERROR parameter missing: 'command'!")

    # the server can query the application to know if it is still open
    def getIsOpen(self):
        return self.__isOpen