"""
Daniel Riegelhaupt
Sept 2014
"""

from responseSerializer import ResponseSerializer
from os.path import curdir, join, dirname, split, isfile
from os import makedirs
from codecs import open
import errno

class SaveLoadRequestHandler:

    def __init__(self, tmpSaveFolder = ""):
        #dirname will retrun the absolute path where this file is located
        #split will split the path into a head and a tail where tail is the last subfolder and head is everything before
        serverLocation = split(dirname(__file__))[1]
        #print serverLocation
        self.__tmpStorePath = join(curdir, serverLocation, tmpSaveFolder)

    def __createSubDir(self, subFolder):
        dir = join(self.__tmpStorePath,subFolder)
        try:
            makedirs(dir)
            return dir
        except OSError as exception:
            if exception.errno != errno.EEXIST: #if there is an error other than 'directory already exists'
                return self.__tmpStorePath #ignore the error and save to the default place which is the temp root
            else:
                return dir

    #process a save request
    def processSaveRequest(self,reqDic):
        if reqDic.has_key('file_name'):

            fileName = reqDic['file_name']

            saveDirectory = self.__tmpStorePath
            if reqDic.has_key('editor_id'):
                saveDirectory = self.__createSubDir(str(reqDic['editor_id']))

            if reqDic.has_key('content'):
                fileContent = reqDic['content']
                storePath = join(saveDirectory, fileName)
                with open(storePath, 'w') as f:
                    f.write(fileContent.encode('utf-8'))

                return ResponseSerializer.success({ 'save_path':storePath})
            else:
                return ResponseSerializer.error("ERROR parameter missing: 'content'!")
        else:
            return ResponseSerializer.error("ERROR parameter missing: 'file_name'!")

    def processLoadRequest(self, reqDic):
        if reqDic.has_key('file_name'):
            fileName = reqDic['file_name']
            if isfile(fileName):
                content = ''
                with open( fileName, encoding='utf-8') as f:
                    content = f.read()
                return ResponseSerializer.success({ 'file_name': fileName ,'file_content':content})
            else:
                return ResponseSerializer.error("ERROR file could not be found or is not a file: '" + str(fileName)+ "'!")
        else:
            return ResponseSerializer.error("ERROR parameter missing: 'file_name'!")
