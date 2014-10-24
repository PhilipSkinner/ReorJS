"""
	remote/mongo.py
	ReorJSd Remote MongoDB Connector
        
        --
	Provides a remote connection to a MongoDB service.
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

import base
import pymongo
import getpass
import logger

class MongoRemote(base.RemoteConnection):
  def connect(self):
    if self.hostname == None:
      logger.LOG.log("Hostname not given, defaulting to localhost")
      self.host = 'localhost'
    
    if self.port == None:
      logger.LOG.log("Port not given, defaulting to 27017")
      self.port = 27017
    
    if self.name == None:
      logger.LOG.log("Database name not given, cannot proceed")
      return False
      
    if self.table == None:
      logger.LOG.log("No table given, cannot proceed")
      return False
  
    self.connection = pymongo.MongoClient(self.hostname, int(self.port))
    self.db = self.connection[self.name]

    return self.connection != None

  def readColumns(self):
    #not needed for mongo so just override
    self.columns = [1]

  def query(self, rows=None):
    if rows == None:
      logger.LOG.log("Defaulting to 1000 rows")
      rows = 1000
    
    collection = self.db[self.table]
    
    results = collection.find({}).skip(self.cursor - 1).limit(rows)
    
    toReturn = []
    
    for r in results:
      r['_id'] = str(r['_id'])
      toReturn.append({ 'data' : r, 'cursor' : self.cursor })
      self.cursor += 1

    return toReturn

  def insert_data(self, data, id):
    collection = self.db[self.table]   
     
    doc = { 'result' : data, 'id' : id }
    
    collection.insert(doc)
