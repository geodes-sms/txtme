"""
 Idea two possibilities:
 1) one God Kernel interface:
    God entity idea is bad software engineering , but MvK works like this you create a model the same way you create an attribute just a different type
 
 2) or three interface kernel + model + entity + assocs
    Kernel can create a model 
    Model can create entityes and attributes and associations
    Entityes can create attributes (subentityes)
    Assocs can create attributes (a reference is an attribute)
    All entityes should make changes to the same instance of the kernel
    
 we need to be able to do two general things
 1) crud on instances of everything
 2) query meta information.
 we need to be able to create an instance of a of Entity A but also query the type of the attributes of A.

 What follows is just an idea of the interfaces we would need. I am not claiming it is the best solution or even a good solution but the methods declared here must be present in some shape or form at the very least to be compatible with the current prototype.

 Notice that the constructor is never included in the interface so that it can be constructed with whatever information is necessary
 
 SAVE IS MISSING (the MvK as i have it cant save a model but we can save the text and use it to create the model on the spot
 it might be a good idea to assume that others do save but for the moment there is no place in the code where saving the model is done so save is useless for the moment
 )
 LOAD MODEL IS MISSING FOR SAME REASON
 
 NO UPDATE: update is the same as doing delete, create again or simply setting a new value for an attribute
"""

#TODO foresee exceptions and such in case of failure ?

class KernelInterface(object):
	"""
	The main interface entity
	"""
	
	def start(): 
		"""
		should start  the actual Kernel
		:return maybe some status code like success or failure or nothing
		"""
		raise NotImplementedError()
	
	def isModelLoaded( modelName ):
		"""
		returns true if the (meta) model is already loaded inside the kernel
		:param modelName : String the name/path of the (meta) model
		:return Boolean
		"""
		raise NotImplementedError()
	
	def LoadMetaModel( metaModelName ):
		"""
		loads the meta model into the kernel
		:param metaModelName : String the name/path of the meta model
		:return Boolean (True for success and False for fail)
		"""
		raise NotImplementedError()
	
	def getMetaModel( metaModelName  ):
		"""
		return a MetaModelInterface for the requested model
		:param metaModelName : String the name/path of the meta model
		:return MetaModelModelInterface
		"""
		raise NotImplementedError()
		
class MetaModelInterface (object):
	"""
	used for all meta information queries
	and to create instances of a Model Interface
	This is separate from the model instance because this is information that will be queried before there is a model instance
	"""
		
	def createModel( modelName ):
		"""
		creates a model and returns the interface for it
		:param modelName : String the name/path of the model
		:return ModelInstanceInterface
		"""
		raise NotImplementedError()
	
	
	#def loadModel( modelName ):
	#	"""
	#	Loads a modelalready created
	#	:param modelName : String the name/path of the model
	#	:return ModelInstanceInterface
	#	"""
	#	raise NotImplementedError()
	#	NOTE: for use with multiple editor where the first one has already used the create method.
	#	a better way would be to do this via the kernel interface and load both model and the meta-model interface at the same time
	
	
	def modelHasEntity( entityName ):
		"""
		returns whether the meta model has an entity (more or less the concept of class diagram class) with the given name
		:param entityName : String
		:return Boolean
		"""
		raise NotImplementedError()
	
	def modelHasAttr( attrName ):
		"""
		returns whether the meta model has an attribute with given name
		:param attrName : String
		:return Boolean
		"""
		raise NotImplementedError()
	
	def modelHasAssoc( assocName ):
		"""
		returns whether the meta model has an association with given name
		:param assocName : String
		:return Boolean
		"""
		raise NotImplementedError()
	
	def modelHasEntity( entityName ):
		"""
		returns whether the meta model has an entity (attribute, entity or association) with the given name, no matter what it is
		:param entityName : String
		:return Boolean
		"""
		raise NotImplementedError()
	
	def entityHasAttr( entityName, attrName ):
		"""
		returns whether the given entity has the given attribute
		:param entityName : String
		:param attrName : String
		:return Boolean
		"""
		raise NotImplementedError()
	
	def assocHasAttr( assocName, attrName ):
		"""
		returns whether the given association has the given attribute
		:param assocName : String
		:param attrName : String
		:return Boolean
		"""
		raise NotImplementedError()
		
	def entityHasAttr( enityName, attrName ):
		"""
		returns whether the given entity has the given attribute
		:param entityName : String
		:param attrName : String
		:return Boolean
		"""
		raise NotImplementedError()
	
	def getModelAttrType( attrName ):
		"""
		get the type from a model attribute
		:param attrName : String
		:return String
		"""
		raise NotImplementedError()
	
	def getEntityAttrType( entityName, attrName ):
		"""
		get the type from a model attribute
		:param attrName : String
		:return String
		"""
		raise NotImplementedError()
	
	def getAssocAttrType( assocName, attrName ):
		"""
		get the type from an association attribute
		:param assocName : String
		:return String
		"""
		raise NotImplementedError()
	
	def getEntityIdAttr( entityName ):
		"""
		get the name of the attribute that is used to identify the given entity (usually something like 'name' or 'id')
		use getEntityAttrType() for the given entityName and the result of this method to get the type of that attribute
		:param entityName : String
		:return String
		"""
		raise NotImplementedError()
		
	def getAssocIdAttr( assocName ):
		"""
		get the name of the attribute that is used to identify the given association (usually something like 'name' or 'id')
		use getAssocAttrType() for the given entityName and the result of this method to get the type of that attribute
		:param assocName : String
		:return String
		"""
		raise NotImplementedError()
		
	def getAssocFromEntity( assocName ):
		"""
		get the entity name of the entity the given association starts from
		for example an association going from entity A to entity B will return 'A'
		:param assocName : String
		:return String
		"""
		raise NotImplementedError()
	
	def getAssocToEntity( assocName ):
		"""
		get the entity name of the entity the given association goes to
		for example an association going from entity A to entity B will return 'B'
		:param assocName : String
		:return String
		"""
		raise NotImplementedError()

class ModelInstanceInterface(object):
	"""
	The model instance interface is the interface for a single instance of a model
	It should never be created separately , only returned from the MetaModelInterface methods
	"""
	
	def getName():
		"""
		returns the model name for which this interface was created
		:return String
		"""
		raise NotImplementedError()
	
	def addEntity( entityName, entityId ):
		"""
		adds an instance entityId of a entity entityName to the model
		:param entityName : String , the name of the entity (A in: instance a of entity A) 
		:param entityId : an id of the entity  (a in: instance a of entity A)<br>
		the type of this should be the same as the type returned by MetaModelInterface::getEntityIdAttr(entityName)
		:return EntityInstanceInterface
		"""
		raise NotImplementedError()
	
	def getEntity( entityId ):
		"""
		returns an EntityInterface for the requested Id 
		:param entityId : the identifying name of the entity in the model
		:return EntityInstanceInterface
		"""
		raise NotImplementedError()
	
	def delEntity( entityId ):
		"""
		deletes the instance with the give id from the model.
		How this cascades with associations and such connected to it is depended on the Modeling Kernel used
		:return None
		"""
		raise NotImplementedError()
	
	def addAssociation( assocName, assocId ):
		"""
		adds an instance assocId of an  association assocName to the model
		:param assocName : String , the name of the association (A in: instance a of Assoc A) 
		:param assocId : an id of the entity  (a in: instance a of Assoc A)<br>
		the type of this should be the same as or castable to the type returned by MetaModelInterface::getAssocIdAttr(assocName)
		:return AssocInstanceInterface
		"""
		raise NotImplementedError()
	
	def getAssoc( assocId ):
		"""
		returns an AssocInstanceInterface for the requested Id 
		:param assocId : the identifying name of the entity in the model
		:return AssocInstanceInterface
		"""
		raise NotImplementedError()
		
	def delAssociation( assocName ):
		"""
		deletes the instance with the give id from the model.
		:return None
		"""
		raise NotImplementedError()
	
	def setAttr( attrName , attrValue ):
		"""
		gives attrName the value of attrValue
		:param attrName : String
		:param attrValue : Should be of same (or castable to) the type returned by MetaModelInterface::getModelAttrType(attrName)
		"""
		raise NotImplementedError()
	
	def getAttrValue( attrName ):
		"""
		returns the value of the given attribute
		:param attrName : String
		:return the value of that attribute , the type should be the Python equivalent cast of the type returned by MetaModelInterface::getModelAttrType(attrName)
		"""
		raise NotImplementedError()
	
	"""
	Note no delete attribute because an attibute isnt an instance bu part of the model. To 'delete' an attribute simple change its value to whetver null value the type has
	"""
	def checkConformance():
		"""
		Checks whether the model conforms to the meta model
		:return A tupple (boolean, message) : (True, "") if the model conforms  or (False, <error message>) if the model doesnt conform
		"""
		raise NotImplementedError()

class EntityInstanceInterface(object):
	"""
	The interface for a single instance of a entity
	It should never be created separately , only returned from the ModelInstanceInterface methods
	"""
	
	def getName():
		"""
		returns the name of the entity
		:return String
		"""
		raise NotImplementedError()
		
	def getInstanceId():
		"""
		returns the id of the current instance, the name or id used to identify this instance in the model
		:return the id, the type will be the Python equivalent of the type returned by 
		MetaModelInterface::getEntityAttrType(getEntityName(), MetaModelInterface::getEntityIdAttr(getEntityName()))
		"""
		raise NotImplementedError()
		
	def setAttr( attrName , attrValue ):
		"""
		gives attrName the value of attrValue
		:param attrName : String
		:param attrValue : Should be of same (or castable to) the type returned by MetaModelInterface::getEntityAttrType(getEntityName(), attrName)
		"""
		raise NotImplementedError()
	
	def getAttrValue( attrName ):
		"""
		returns the value of the given attribute
		:param attrName : String
		:return the value of that attribute , the type should be the Python equivalent cast of the type returned by MetaModelInterface::getEntityAttrType(getEntityName(), attrName)
		"""
		raise NotImplementedError()

class AssociationInstanceInterface(object):
	"""
	The interface for a single instance of an association
	It should never be created separately , only returned from the ModelInstanceInterface methods
	"""
	
	def getName():
		"""
		returns the name of the association
		:return String
		"""
		raise NotImplementedError()
		
	def getInstanceId():
		"""
		returns the id of the current instance, the name or id used to identify this instance in the model
		:return the id, the type will be the Python equivalent of the type returned by 
		MetaModelInterface::getAssocAttrType(getAssocName(), MetaModelInterface::getAssocIdAttr(getAssocName()))
		"""
		raise NotImplementedError()
		
	def setAttr( attrName , attrValue ):
		"""
		gives attrName the value of attrValue
		:param attrName : String
		:param attrValue : Should be of same (or castable to) the type returned by MetaModelInterface::getEntityAttrType(getEntityName(), attrName)
		"""
		raise NotImplementedError()
	
	def getAttrValue( attrName ):
		"""
		returns the value of the given attribute
		:param attrName : String
		:return the value of that attribute , the type should be the Python equivalent cast of the type returned by MetaModelInterface::getEntityAttrType(getEntityName(), attrName)
		"""
		raise NotImplementedError()
	
	def setFrom( entityId ):
		"""
		set where this association starts from
		:param entityId : an id of a entity. That entity should be of the type accepted by the association and the id should be of the same type as the identifing attribute of that entity
		:return None
		"""
		raise NotImplementedError()
	
	def setTo( entityId ):
		"""
		set where this association goes to
		:param entityId : an id of a entity. That entity should be of the type accepted by the association and the id should be of the same type as the identifing attribute of that entity
		:return None
		"""
		raise NotImplementedError()
	
"""
Note stuff like getname getInstance , get and set attribute can all go in a base interface but they will al have to be implemnted anyway and this at least makes it clear template and this way nothing will be forgotten
"""	