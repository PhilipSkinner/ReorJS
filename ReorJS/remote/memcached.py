import base

class MemcachedRemote(base.RemoteConnection):
  def connect(self):
    if self.host == None:
      print "Hostname not given, defaulting to localhost"
      self.host = 'localhost'
    
    if self.name == None:
      print "Database name not given, cannot proceed"
      return False
      
    if self.table == None:
      print "No table given, cannot proceed"
      return False
  
    
    return self.connection != None

  def readColumns(self):
    self.columns = [1]

  def query(self, rows=None):
    if rows == None:
      print "Defaulting to 1000 rows"
      rows = 1000
    
    toReturn = []
    
    return toReturn
