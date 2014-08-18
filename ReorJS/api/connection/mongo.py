import copy
from base import ConnectionBase
from base import ColumnBase
from pymongo import ASCENDING, DESCENDING
from bson.objectid import ObjectId

class Connection(ConnectionBase):
  def __init__(self, connection):
    self.connection = connection
    self.db = self.connection().reorjs

  def checkObject(self, object):
    #first check, does the table exist?
    print "Checking for existance of object %s in data source" % object.__tablename__
      
    result = self.db[object.__tablename__]
      
    pk = None
      
    for attribute, value in object.__dict__.items():
      if isinstance(value, Column):
        if value.primary_key:
          pk = value
      
    if pk != None:            
      print "Ensuring primary key index on collection %s" % object.__tablename__
      result.create_index([(pk.name, ASCENDING)])      
  
  def fixPK(self, object, params):
    replace = None
    for attribute, value in object.__dict__.items():
      if isinstance(value, Column):
        if value.primary_key:
          replace = value.oldname
          
    new = {}
    for key, value in params.iteritems():
      if replace == key:
        new['_id'] = ObjectId(params[key])
      else:
        new[key] = params[key]
        
    return new
  
  def search(self, object, params={}, options={}):
    if not object._checkParams(params):
      return []

    params = self.fixPK(object, params)    
      
    if object.__tablename__ == None:
      print "%s Object table name needs to be set" % self
      return []
      
    pk = None
    for attribute, value in object.__dict__.items():
      if isinstance(value, Column):
        if value.primary_key:
          pk = value
        
    collection = self.db[object.__tablename__]    
    results = collection.find(params)
    
    toReturn = []    
    for result in results:
      #now create a copy of ourself with these values
      obj = copy.copy(object)
      
      for column, value in result.iteritems():      
        if column == '_id':        
          column = pk.oldname
          
        col = getattr(obj, column)
        col.__value__(value)
      
      toReturn.append(obj)

    return toReturn              

  def update(self, object):
    #save our current objects attributes to our permanent store
    print "Save in DB pls"
   
    doc = {}
    for attribute, value in object.__dict__.items():
      if isinstance(value, Column):
        if value.primary_key:
          pk = value
        else:
          doc[value.name] = value.value()
    
    if pk == None:
      print "Issue calling update, no primary key given. Defaulting to insert only for %s" % object
    else:    
      collection = self.db[object.__tablename__]
      
      if pk.value() == None:
        collection.insert(doc)
      else:
        collection.update({ pk.name : ObjectId(pk.value()) }, { '$set' : doc }, upsert=True, multi=False)      

  def delete(self, object):    
    #delete our objects from its permanent store
    pk = None
    for attribute, value in object.__dict__.items():
      if isinstance(value, Column):
        if value.primary_key:
          pk = value
    
    if pk == None:
      print "Issue calling delete, no primary key given. Object will not be deleted"
      return False

    collection = self.db[object.__tablename__]
    collection.remove({ pk.name : ObjectId(pk.value()) })    

    print "Object deleted"
    
    return False
  
  def column(self, name, type, primary_key=False, null=False):
    return Column(name, type, primary_key=primary_key, null=null)
    
class Column(ColumnBase):  
  def afterInit(self):
    self.oldname = ''
    if self.primary_key:
      self.oldname = '%s' % self.name
      self.name = '_id'

  def __set__(self):
    return None

  def __create__(self):
    return None
