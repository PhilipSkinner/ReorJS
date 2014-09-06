import base
import logger

class HadoopRemote(base.RemoteConnection):
  def connect(self):
    if self.host == None:
      logger.LOG.log("Hostname not given, defaulting to localhost")
      self.host = 'localhost'
        
    if self.name == None:
      logger.LOG.log("Database name not given, cannot proceed")
      return False
      
    if self.table == None:
      logger.LOG.log("No table given, cannot proceed")
      return False
  
    return self.connection != None

  def readColumns(self):
    self.columns = [1]

  def query(self, rows=None):
    if rows == None:
      logger.LOG.log("Defaulting to 1000 rows")
      rows = 1000
    
    toReturn = []
    
    return toReturn
