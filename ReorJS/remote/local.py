import base

class MySQLRemote(RemoteConnection):
  def connect(self):

    return self.connection != None

  def readColumns(self):
    self.columns = [1]

  def query(self, rows=None):
    if rows == None:
      print "Defaulting to 1000 rows"
      rows = 1000
    
    toReturn = []
    
    return toReturn
