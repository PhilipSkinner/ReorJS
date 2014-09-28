"""
        api/connection/mongo.py
	ReorJSd API MongoDB Connector
        
        --
	Provides a basic set of commands for loading and saving data to/from
	a mongodb instance.
        --
        
        Author(s)       - Philip Skinner (philip@crowdca.lc)
        Last modified   - 2014-09-28
        
        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.
            
        This program is distributed in the hope that it will be useful,     
        but WITHOUT ANY WARRANTY; without even the implied warranty of      
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.
                 
        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>.
        
        Copyright (c) 2014, Crowdcalc B.V.
"""

import copy
import logger
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
    logger.LOG.log("Checking for existance of object %s in data source" % object.__tablename__)
      
    result = self.db[object.__tablename__]
      
    pk = None
      
    for attribute, value in object.__dict__.items():
      if isinstance(value, Column):
        if value.primary_key:
          pk = value
      
    if pk != None:            
      logger.LOG.log("Ensuring primary key index on collection %s" % object.__tablename__)
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
        try:
          new['_id'] = ObjectId(params[key])
        except:
          new['_id'] = params[key]
      else:
        new[key] = params[key]
        
    return new
  
  def search(self, object, params={}, options={}):
    if not object._checkParams(params):
      return []

    params = self.fixPK(object, params)    
      
    if object.__tablename__ == None:
      logger.LOG.log("%s Object table name needs to be set" % self)
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
      obj = copy.deepcopy(object)

      for column, value in result.iteritems():              
        for attribute, v in obj.__dict__.items():
          if isinstance(v, Column):
            if v.name == column:
              v.__value__(value)
      
      toReturn.append(obj)

    return toReturn              

  def update(self, object):
    #save our current objects attributes to our permanent store
    logger.LOG.log("Save in DB pls")
   
    doc = {}
    for attribute, value in object.__dict__.items():
      if isinstance(value, Column):
        if value.primary_key:
          pk = value
        else:
          doc[value.name] = value.value()
    
    if pk == None:
      logger.LOG.log("Issue calling update, no primary key given. Defaulting to insert only for %s" % object)
    else:    
      if self.db == None:
        self.db = self.connection().reorjs
        
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
      logger.LOG.log("Issue calling delete, no primary key given. Object will not be deleted")
      return False

    if self.db == None:
      self.db = self.connection().reorjs

    collection = self.db[object.__tablename__]
    collection.remove({ pk.name : ObjectId(pk.value()) })    

    logger.LOG.log("Object deleted")
    
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
