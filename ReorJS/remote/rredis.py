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
    
    toReturn = []

    #gotta love redis
    try:
      toReturn = self.connection.lrange(self.table, self.cursor, (self.cursor + rows - 1))
    except:
      print "Issue fetching data from redis"
    
    #the data inside redis should be ready to use already, it won't be changed hugely

    return toReturn
