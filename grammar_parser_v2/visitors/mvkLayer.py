"""
Daniel Riegelhaupt - August 2014
edited November 2014

this visitor extracts information to creates instances of a model based on a model mapping
(most likely received from a modelMappingVisitor)
"""

###MVK IMPORTS
from mvk.impl.python.constants import CreateConstants, UpdateConstants
from mvk.impl.python.datatype import TypeFactory, Type, IntegerType, StringType, \
    BooleanType, FloatType
from mvk.impl.python.datavalue import MappingValue, \
    LocationValue, StringValue, FloatValue, \
    IntegerValue, BooleanValue, InfiniteValue, Iterator
from mvk.impl.python.object import ClabjectReference, Clabject
from mvk.mvk import MvK

#import shell
#from shell import *

import re

from visitor import  Visitor
from position import Position
from hutnparser import Tree


class Constants: #TODO this whole class constant class must be put somewhere else and use by the mapping visitor ass well
    MODEL = 'Model'
    CLASS = 'Class'
    ASSOC = 'Association'
    REF = 'Reference'
    ATTR = 'Attribute'

class DTree(object):
    """
    Data Tree. a class to save our model data
    children are added in the order they are in the text.
    This makes it easier to find where we are in the given place
    """
    def __init__(self, **kwargs):
        self.parent = kwargs.pop('parent', None)
        self.type = kwargs.pop('type', None) #type will be : model, class attribute or reference
        self.attr_type = kwargs.pop('mvk_type', None) #attr type : in case of an attribute or reference: for example IntegerType
        self.mapping = kwargs.pop('mapping', '')
        self.value = kwargs.pop('value', None)
        self.start_pos = kwargs.pop('start_pos', None)
        self.end_pos = kwargs.pop('end_pos', None)
        self.children = []

    def addChild(self, child, sort = False):
        """
        when adding a child if that child is an attribute we dont need to sort
        but if it is a class and we add it to the model we do want it sorted in the order they appear in the text
        we do this because we explicitly visit them in order of class, and then assoc but we ant them kept in order
        of text. this is so that we can find things later
        :param child: the child to add
        :param sort: if True will sort them in the order they came in the text
        :return: nothing
        """
        l = len(self.children)
        if sort and l != 0:
            i = 0
            while (i < l) and child.start_pos >= self.children[i].end_pos:
                i += 1

            if i == l:
                self.children.append(child)
            else:
                temp2 = self.children[i:]
                temp1 = self.children[0:i]
                temp1.append(child)
                self.children = temp1 +temp2
        else:
            self.children.append(child)

    def __str__(self):
        #i realize that this almost literally the textbook case for polymorphism
        #but this is just for debugging/control purposes and not worth creating other classes over
        ret = self.type + ': '
        if self.type == Constants.MODEL:
            ret += self.value
        elif self.type == Constants.ASSOC or self.type == Constants.CLASS:
            ret += str(self.value) + ' (' + str(self.mapping) + ')'
        elif self.type == Constants.ATTR or self.type == Constants.REF:
            ret += self.mapping + ' = ' + str(self.value) + ' (' +str(self.attr_type) +')'
        return ret

    def __repr__(self):
        return "<" + str(self) + ">"

    def toStr(self, level = 0):
        ret = ''
        for i in range(0, level+1):
            ret += '\t'
        ret += str(self)
        if self.children:
            ret +=":\n"
            for child in self.children:
                ret += child.toStr(level+1)
        ret+= "\n"
        return ret



class ModelDataVisitor(Visitor):

    def __init__(self, map, mvkInstance):
        self.map = map
        self.__modelAddedToMVK = False #we can also use this visitor to create data without adding the model to the nvk
        self.__modelDataHasBeenAdded = False #the model has not been added to the data yet


        self.data = None
        self.dataIndexAssoc = []
        self.dataIndexClass = []

        self.oldData = None
        self.oldDataIndexAssoc = []
        self.oldDataIndexClass = []

        #return the keys containig mapping to the metamodel, normally 'there can be only one'
        #TODO should there really be only one ?  what about multiple metamodels ?
        form_key = self.__getKeysOfType(Constants.MODEL)[0]

        self.mvk = mvkInstance
        self.metamodelFull = self.map[ form_key ]["mapping"]  #the metamodel used packace.path.metamodel_name
        #before we import we check to see if a metmodel is not already loaded
        readLog = self.mvk.read(LocationValue(self.metamodelFull))
        if not readLog.is_success():
            try:
                #import the metamodel dynamically
                module = __import__(self.metamodelFull, fromlist=["Gen"])
                Gen = module.Gen
                modelVerse = Gen(self.mvk)
                modelVerse.instance() #this will update self.mvk to contain the Meta Model
            except Exception as e:
                err = "failed to import meta model. Details:\n" + str(e)
                print err



        dotIndex = self.metamodelFull.rfind('.') #rfind to find the last dot

        self.metamodelName = self.metamodelFull[dotIndex+1:] # just the name dot index of the metamodel (the metamodel_name part of self.metamodelFull)
        self.locationPrefix = self.metamodelFull[:dotIndex] #the location prefix is the package.path part of the full metamodel
        #self.location = "" # the location is package.path.instance_name (where instance name will be read later)

        self.attrKeys = self.__getKeysOfType(Constants.ATTR)
        self.classKeys = self.__getKeysOfType(Constants.CLASS)
        self.assocKeys = self.__getKeysOfType(Constants.ASSOC)
        self.refKeys = self.__getKeysOfType(Constants.REF)

        self.errorLog = []

        self.augmentMappingInfo()
        #print self.map

        #self.sh = Shell()
        #self.sh.setMvK(self.mvk)


    #return the grammar rule that is mapped to the model name
    def getModelNameGrammarRule(self):
        mappingName = self.metamodelName + '.name'
        keys = self.map.keys()
        for key in keys:
            if self.map[key]["mapping"] == mappingName:
                return key
        return ""

    def setAddingNewData(self): #maybe this is beter put on reset or update but i think you can call the visitor wihtout them this forces new data
        #we tell the visitor that this is new data getting added on the next visit
        self.__modelDataHasBeenAdded  = False



    ## main visitor procedures
    def visit(self, tree):
        self.errorLog = []
        #self.__setPaths(tree) MOVED TO PREPROSECCING
        self.__markAttributes(tree)

        self.__addTreeToData(tree)
        return self.data

    def updateModel(self):
        """
        Instead of doing update on the previous model we remove it
        Reason:
        take this use case:
        Assume Class A with field 'foo' , default value "foo" and field 'bar' default value 0

        Let us say that text first says:
        a = A()
        a.foo = "yipii"
        a.bar = 5

        the user changes the text to the following and than calls updateMethod:
        a = A()
        a.bar = 2

        the user expects this to mean:
        a = A()
        a.foo = "foo"
        a.bar = 2

        but because mvk.update simply updates values of attribute given and keeps teh rest
        what will actually happen is this:
        a = A()
        a.foo = "yipii"
        a.bar = 2

        this means we need to compare every attribute of every instance to perform update specifically
        (which would require the metamodel which we do not have nor should we need at this moment)
        it is simpler (at least for the current models) to simply remove everything correctly and rebuild
        """
        if self.data:
            self.__removeOldModel()
            if  self.__createModel():
                self.__createClasses()
                self.__createAssocs()
                self.__modelAddedToMVK = True
        return self.errorLog

    def clearModel(self):
        """
        removes the current model from the mvk
        :return:
        """
        if self.__modelAddedToMVK:
            if self.oldData:
                self.__removeOldModel()
            else: #we've added the model to the mvk but havent updated yet so we remove the current one
                self.__removeCurModel()


    def augmentMappingInfo(self):
        """
        Method that adds information to the mapping obtained via the Mvk
        :return:
        """
        #TODO refactor this: one for loop over every item with an if according to type
        #seems cleaner
        def getAttrName(k):
            name = ""
            mapping = self.map[k]["mapping"]
            #this check is needed because for metamodels attribute we would write the name of the metamodel twice otherwise
            if mapping.startswith(self.metamodelName) == False:
                name = self.metamodelFull + "." +  mapping
            else:
                name = self.locationPrefix + "." + mapping
                #locationPrefix contains the path the the metamodel without the metamodel name
                #the metamodel name is already contained in the mapping
            return name

        #for reference we add the following information: the type
        #the actual name of the gate , and what it refers to
        for key in self.refKeys:

            attrName = self.metamodelFull + "." +  self.map[key]["mapping"]
            readLog = self.mvk.read(LocationValue(attrName)) #we check if that attribute exists
            if (readLog.is_success()):
                self.map[key]["mvk_type"] = "LocationType"
                self.map[key]["mvk_mapping"] = self.map[key]["mapping"] #the mapping by which the mvk will find the reference keep this in case it is needed
                self.map[key]["mapping"] = str(readLog.get_item().value) #the mapping needed in this context to create the attribute

                ref = ""
                if attrName.endswith('from_port'):
                    #note we could also get .location  instead of .name for the full path which includes metamodel  name
                    # but this gives the same result as what the mapping expects
                    ref = readLog.get_item().parent.from_multiplicity.node.name
                elif attrName.endswith('to_port'):
                    ref = readLog.get_item().parent.to_multiplicity.node.name

                self.map[key]["refers_to"] = str(ref)
            else:
                err =  "Error while reading reference: " + str(readLog.get_status_message())
                print err
                self.__addToErrorLog(err, None)

        #for regular attributes we just want the type
        for key in self.attrKeys:

            attrName = getAttrName(key)
            readLog = self.mvk.read(LocationValue(attrName)) #we check if that attribute exists
            if (readLog.is_success()):
                self.map[key]["mvk_type"] = str(readLog.get_item().type)
            else:
                err =  "Error while reading attribute: " + str(readLog.get_status_message())
                print err
                self.__addToErrorLog(err, None)

        for key in self.assocKeys:
            attrName = getAttrName(key)
            readLog = self.mvk.read(LocationValue(attrName)) #we check if that attribute exists
            if (readLog.is_success()):
                self.map[key]["id_field"] = str(readLog.get_item().attributes.value[StringValue("Class.id_field")].value)
            else:
                err =  "Error while reading Association: " + str(readLog.get_status_message())

        for key in self.classKeys:
            attrName = getAttrName(key)
            readLog = self.mvk.read(LocationValue(attrName)) #we check if that attribute exists
            if (readLog.is_success()):
                self.map[key]["id_field"] = str(readLog.get_item().attributes.value[StringValue("Class.id_field")].value)
            else:
                err =  "Error while reading Class: " + str(readLog.get_status_message())

    def getAugmentedModelMap(self):
        return self.map

    def __addTreeToData(self,tree):
        if not self.__modelDataHasBeenAdded:
            self.__addModelToData(tree)
        self.__addClassesAndAssocToData(tree)

    def __addToErrorLog(self, error, data):
        log = { "error": error}
        if data and data.start_pos:
            start = { 'line': data.start_pos.line, 'column' : data.start_pos.column}
            end = { 'line': data.end_pos.line, 'column' :data.end_pos.column}
            log["error_position"] = {"startpos" : start, "endpos" :end }

        self.errorLog.append(log)

    def __getKeysOfType(self, string):
        """
         returns a list of keys for the map  whose type correspond to the given string
        like for example "Attribute", "Class", "metamodel" or "Association"
        """
        ret = []
        for key in self.map.keys():
            if self.map[key]["type"] == string:
                ret.append(key)
        return ret

    def __markAttributes(self, tree):
        """
        traverses the tree and marks any node corresponding to an element mapped as an attribute
        in the mapping datastructure.
        It fills in relevant information as well
        """
        def fillData(t, k , attr= True):
            if attr:
                setattr(t, "is_attribute", True)
            else:
                setattr(t, "is_reference", True)
                setattr(t, "mvk_mapping", self.map[k]['mvk_mapping'])
            setattr(t, "mapping", self.map[k]["mapping"])
            setattr(t, "value", self.getTokenValue(tree))
            setattr(t, "attr_type", self.map[k]["mvk_type"])

        if self.isTree(tree):
            found = False
            for key in self.attrKeys:
                if tree.path.endswith(key):
                    fillData(tree,key)
                    #print tree.head, tree.mapping
                    found = True
                    break
            #if not found as an attribute we try a reference
            if not found:
                for key in self.refKeys:
                    if tree.path.endswith(key):
                        fillData(tree,key,False)
                        found = True #wheter there is an error or not  we did find the attribute definition so we continue
                        break

            if not found: #if found there is no reason to search this branch further
                for elem in tree.tail:
                    self.__markAttributes(elem)

            if not found: #if found there is no reason to search this branch further
                for elem in tree.tail:
                   self.__markAttributes(elem)

    def __getEntityAttributes(self, tree, entityName):
        """
        given a entity name and a tree find any nodes in that tree who are mapped as attribute
        of that entity and return their information
        """
        ret = []
        if self.isTree(tree):
            if (( hasattr(tree, "is_attribute") and tree.mapping.startswith(entityName)) or
                ( hasattr(tree, "is_reference") and tree.mvk_mapping.startswith(entityName)) ):
                attr = DTree()
                attr.mapping = tree.mapping
                if hasattr(tree, "is_attribute"):
                    attr.type = Constants.ATTR
                    attr.value = tree.value
                else:
                    attr.type = Constants.REF
                    attr.value = self.location  + '.' + tree.value #the reference itself

                attr.attr_type = tree.attr_type
                if hasattr(tree, 'startpos'):
                    attr.start_pos  = Position(tree.startpos['line'] , tree.startpos['column'])
                    attr.end_pos = Position(tree.endpos['line'] , tree.endpos['column'])
                ret.append(attr)
                return ret
            else:
                for elem in tree.tail:
                    ret +=  self.__getEntityAttributes(elem, entityName)
        return ret

    def __createAttrDict(self, attr):
        """
        creates a dictionary of the attribute to be put in the mvk
        """
        #TODO suppurt for union and set etc...
        """
        ('VoidType', VoidType()),
                     ('AnyType', AnyType()),
                     ('FloatType', FloatType()),
                     ('StringType', StringType()),
                     ('BooleanType', BooleanType()),
                     ('IntegerType', IntegerType()),
                     ('TypeType', TypeType()),
                     ('SequenceType[FloatType]', SequenceType(basetype=FloatType())),
                     ('SetType[IntegerType]', SetType(basetype=IntegerType())),
                     ('MappingType(IntegerType: FloatType)', MappingType(keytype=IntegerType(), valuetype=FloatType())),
                     ('UnionType(BooleanType, StringType)', UnionType(types=SequenceValue(value=[BooleanType(), StringType()]))),
                     ('SequenceType[UnionType(SetType[IntegerType], MappingType(StringType: MappingType(IntegerType: FloatType)))]', SequenceType(basetype=UnionType(types=SequenceValue(value = [SetType(basetype=IntegerType()),
        """

        functions = {
            "IntegerType" : [ IntegerValue, int ],
            "BooleanType" : [ BooleanValue, bool ],
            "FloatType" : [ FloatValue, float ],
            "StringType" : [ StringValue, str ],
            "LocationType" : [ LocationValue, str ]
        }

        ret  = {}
        for a in attr:
            #print "mapping: ",  a["mapping"] , "of type" , str(a["attr_type"]),  " with value", a["value"], "of actual type" , type(a["value"])
            f = functions[str(a.attr_type)]
            constr= f[0]
            cast = f[1]
            #print "value cast = ", cast(a["value"])
            ret[StringValue(a.mapping)] = constr(cast(a.value))

        return ret

    def __createInstance(self,  type, location, attributes):
        """
        creates an instance of something in the mvk
        """
        attr = self.__createAttrDict(attributes)
        #TODO uncommnent print maybe this is interesting information
        #print "CREATING INSTANCE: type = '", type, "' location= '", location,"' attr= '", attributes, "'"
        cl = self.mvk.create(MappingValue({
            CreateConstants.TYPE_KEY: LocationValue(type),
            CreateConstants.LOCATION_KEY: LocationValue(location),
            CreateConstants.ATTRS_KEY: MappingValue( attr)
        }))
        return cl

    def __addModelToData(self, tree):
        """
        add the data of the model
        """
        start = Position(tree.startpos['line'] , tree.startpos['column'])
        end = Position(tree.endpos['line'] , tree.endpos['column'])
        self.data = DTree( parent = None, type = Constants.MODEL , start_pos = start, end_pos= end)

        i = self.metamodelFull.rfind('.')
        metamodelName = self.metamodelFull[i+1:]

        #set the attribute of the entity
        mappingName = metamodelName + '.name'
        instanceAttr = self.__getEntityAttributes(tree,  metamodelName)
        instanceName = ''

        for attr in instanceAttr:
            attr.parent = self.data
            self.data.addChild(attr)
            if attr.type == Constants.ATTR and attr.mapping == mappingName:
                instanceName = attr.value

        self.data.value = instanceName
        #IMPORTANT if the model has a reference  this will be a problem because __getEntityAtrributes
        #will need  self.location to set the value
        self.location = self.locationPrefix + "." + self.data.value #the value is the name of the model instance
        self.__modelDataHasBeenAdded = True

    def __fillData(self, kind,key, tree):
            start = Position(tree.startpos['line'] , tree.startpos['column'])
            end = Position(tree.endpos['line'] , tree.endpos['column'])

            instanceName = self.map[key]['mapping']
            #we look for attributes of that class only in the subtree of that declaration, can we just assume that ?
            instanceAttr = self.__getEntityAttributes(tree, instanceName)
            dataTree = DTree(type= kind, mapping= instanceName, start_pos= start, end_pos=end)

            idAttr = self.map[key]['id_field']
            for attr in instanceAttr:
                attr.parent = dataTree
                dataTree.addChild(attr)
                if attr.type == Constants.ATTR and attr.mapping == idAttr:
                    dataTree.value = attr.value

            dataTree.parent = self.data
            self.data.addChild(dataTree,True)
            if kind == Constants.CLASS:
                self.dataIndexClass.append(dataTree)
            else:
                self.dataIndexAssoc.append(dataTree)

    def __addClassesAndAssocToData(self, tree):
        if self.isTree(tree):
            found = False
            for key in self.classKeys:
                if tree.path.endswith(key):
                    self.__fillData(Constants.CLASS, key, tree)
                    found = True
                    break
            if not found:
                for key in self.assocKeys:
                    if tree.path.endswith(key):
                        self.__fillData(Constants.ASSOC, key, tree)
                        found = True
                        break
            if not found:
                for elem in tree.tail:
                   self.__addClassesAndAssocToData(elem)

    def  __isValidName(self, name):
        #a name must not consits only of whitespace characters
        return (name != None) and(name != "") and (re.match(r'^\s*$', name) == None)

    def __createModel(self):
        """
        creates a model where we are going to put the created attributes, associations and classes
        """
        #TODO uncommnent print maybe this is interesting information
        ret = False
        instanceAttr = []
        for item in self.data.children:
            if item.type == Constants.ATTR: #the model also has non attribute children
                instanceAttr.append(item)

        if self.__isValidName(self.data.value):
            cl = self.__createInstance(self.metamodelFull, self.locationPrefix, instanceAttr)
            if(cl.is_success()):
                ret = True
                #print "Created instance of model '" +  self.metamodelFull + "' called: " + self.data.value
            else:
                err =  "Error while creating model instance: " +  str(cl.get_status_message())
                #print err
                self.__addToErrorLog(err, self.data)
        else:
            pass
            #print "The Model wasn't created: the name was not valid"
            #Note this message is for information only and will not be displayed to the user, a syntax error probably took care of that"
        return ret

    def __createClasses(self):
            """
            travers the data and create instances of classes for elements who are mapped to them
            """
            #TODO uncommnent print maybe this is interesting information
            for item in self.dataIndexClass:
                if self.__isValidName(self.data.value):
                    fullClassName = self.metamodelFull + '.' + item.mapping
                    cl = self.__createInstance(fullClassName, self.location, item.children)
                    if cl.is_success():
                        #print "Created instance of Class: '" + fullClassName + "' with the following attr: ",  item.children
                        #self.sh.serialize(self.location, format_type='python')
                        self.__instanceConformsTo(item, self.location, self.metamodelFull)
                    else:
                        err = "Error while creating class instance: " +  str(cl.get_status_message())
                        #self.sh.serialize(self.location, format_type='python')
                        print err
                        self.__addToErrorLog(err, item)
                else:
                    pass
                    #print "An instance of Class" + item.mapping +" wasn't created: the name was not valid"
                    #nNote this message is for information only and will not be displayed to the user, a syntax error probably took care of that"

    def __createAssocs(self):
        """
        travers the data and create instances of associations for elements who are mapped to them
        """
        #TODO uncommnent print maybe this is interesting information
        for item in self.dataIndexAssoc:
            if self.__isValidName(self.data.value):
                fullAssocName = self.metamodelFull + '.' + item.mapping
                cl = self.__createInstance(fullAssocName, self.location, item.children)
                if cl.is_success():
                    #print "Created instance of Association: '" + fullAssocName + "' with the following attr: ",  item.children
                    #self.sh.serialize(self.location, format_type='python')
                    self.__instanceConformsTo(item, self.location, self.metamodelFull)
                else:
                    err = "Error while creating association instance: " +  str(cl.get_status_message())
                    #self.sh.serialize(self.location, format_type='python')
                    print err
                    self.__addToErrorLog(err, item)
            else:
                pass
                #print "An instance of Association" + item.mapping +" wasn't created: the name was not valid."
                #nNote this message is for information only and will not be displayed to the user, a syntax error probably took care of that"

    def __instanceConformsTo(self, data, instance, metamodel):
        #TODO uncommnent print maybe this is interesting information
        cl = self.mvk.conforms_to(LocationValue(instance), LocationValue(metamodel))
        if cl.get_result():
            pass
            #print "After creation of an instance the model still conforms to the meta-model"
        else:
            err =  "Meta-model conformance error: " +  str(cl.get_status_message())
            #print err
            self.__addToErrorLog(err, data)

    def resetData(self):
         if self.data:
            #we keep the old data so that we can remove it when we update the model
            self.oldData = self.data
            self.oldDataIndexClass = self.dataIndexClass
            self.oldDataIndexAssoc = self.dataIndexAssoc

            #the data fields are rest
            self.data = None
            self.dataIndexClass = []
            self.dataIndexAssoc = []

    def __removeOldModel(self):
        #TODO uncommnent print maybe this is interesting information
        if self.oldData and self.__modelAddedToMVK:
            #can't simply use self.location , the name of the model might have been changed
            prefix = self.locationPrefix + '.' + self.oldData.value
            #first we remove associations between classes
            for item in self.oldDataIndexAssoc:
                location = prefix + '.' + item.value
                dl = self.mvk.delete(LocationValue(location))
                #print dl
            #then we remove the classes
            for item in self.oldDataIndexClass:
                location = prefix + '.' + item.value
                dl = self.mvk.delete(LocationValue(location))
                #print dl
            #finally we remove themodel itself
            dl = self.mvk.delete(LocationValue(prefix))
            #print dl
            self.__modelAddedToMVK = False

    def __removeCurModel(self):
        """
        DIFF WITH  OLD MODEL: usage of self.data, self.dataIndexAssoc and self.dataIndexClass instead of old eauivalent
        :return:
        """
        #TODO uncommnent print maybe this is interesting information
        if self.data and self.__modelAddedToMVK:
            #can't simply use self.location , the name of the model might have been changed
            prefix = self.locationPrefix + '.' + self.data.value
            #first we remove associations between classes
            for item in self.dataIndexAssoc:
                location = prefix + '.' + item.value
                dl = self.mvk.delete(LocationValue(location))
                #print dl
            #then we remove the classes
            for item in self.dataIndexClass:
                location = prefix + '.' + item.value
                dl = self.mvk.delete(LocationValue(location))
                #print dl
            #finally we remove themodel itself
            dl = self.mvk.delete(LocationValue(prefix))
            #print dl
            self.__modelAddedToMVK = False