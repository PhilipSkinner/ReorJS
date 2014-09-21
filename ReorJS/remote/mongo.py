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
