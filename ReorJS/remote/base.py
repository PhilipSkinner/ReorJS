import simplejson as json
import logger

class RemoteConnection():
  def __init__(self, name=None, hostname=None, port=None, username=None, password=None, table=None):
    self.name = name
    self.hostname = hostname
    self.port = port
    self.username = username
    self.password = password
    self.table = table
    
    self.connection = None
    self.ready = self.connect()
    self.cursor = 1
    self.columns = []
    
    if self.ready:
      logger.LOG.log("Remote connection established")
    else:
      logger.LOG.log("Remote connection could not be established")

  def noEncode(self):
    return False

  def resetCursor(self):
    self.cursor = 1

  def connect(self):
    logger.LOG.log("Connect needs to be overridden")
    return False
    
  def query(self, rows=None):
    logger.LOG.log("Query needs to be overridden")
  
  def readColumns(self):
    logger.LOG.log("readColumns needs to be overridden")
  
  def fetch_data(self, rows=1000, cursor=None):
    if len(self.columns) == 0:
      self.readColumns()
    
    self.cursor = cursor
    if self.cursor == 0:
      self.cursor = 1
        
    data = self.query(rows=rows)
    
    if data == None:
      data = []
    
    if self.noEncode():
      return data
      
    return [{ 'data' : json.dumps(d['data']), 'cursor' : d['cursor'] } for d in data]

  def save_result(self, result=None, cursor=None):
    if result == None or cursor == None:
      return
    
    self.insert_data(result, cursor)
