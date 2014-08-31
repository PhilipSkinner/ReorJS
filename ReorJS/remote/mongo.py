import base
import pymongo
import getpass

class MongoRemote(base.RemoteConnection):
  def connect(self):
    if self.hostname == None:
      print "Hostname not given, defaulting to localhost"
      self.host = 'localhost'
    
    if self.port == None:
      print "Port not given, defaulting to 27017"
      self.port = 27017
    
    if self.name == None:
      print "Database name not given, cannot proceed"
      return False
      
    if self.table == None:
      print "No table given, cannot proceed"
      return False
  
    self.connection = pymongo.MongoClient(self.hostname, int(self.port))
    self.db = self.connection[self.name]

    return self.connection != None

  def readColumns(self):
    #not needed for mongo so just override
    self.columns = [1]

  def query(self, rows=None):
    if rows == None:
      print "Defaulting to 1000 rows"
      rows = 1000
    
    collection = self.db[self.table]
    
    results = collection.find({}).skip(self.cursor).limit(rows)
    
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
