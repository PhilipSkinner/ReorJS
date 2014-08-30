import base
import redis

class RedisRemote(base.RemoteConnection):
  def connect(self):
    if self.hostname == None:
      print "Hostname not given, defaulting to localhost"
      self.hostname = 'localhost'
      
    if self.port == None:
      print "Port not given, defaulting to 6379"
      self.port = 6379
    
    if self.name == None:
      print "Database name not given, cannot proceed"
      return False
      
    if self.table == None:
      print "No table given, cannot proceed"
      return False
  
    self.connection = redis.Redis(host=self.hostname, port=int(self.port))
  
    return self.connection != None
  
  def noEncode(self):
    return True

  def readColumns(self):
    #not needed
    self.columns = [1]

  def query(self, rows=None):
    if rows == None:
      print "Defaulting to 1000 rows"
      rows = 1000
    
    results = []
    toReturn = []

    #gotta love redis
    try:
      results = self.connection.lrange(self.table, self.cursor, (self.cursor + rows - 1))
    except:
      print "Issue fetching data from redis"
    
    #setup the cursors
    for d in results:
      toReturn.append({ 'data' : d, 'cursor' : self.cursor })
      self.cursor += 1      

    return toReturn
