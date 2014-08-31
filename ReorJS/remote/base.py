import simplejson as json

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
    self.cursor = 0
    self.columns = []
    
    if self.ready:
      print "Remote connection established"
    else:
      print "Remote connection could not be established"

  def noEncode(self):
    return False

  def resetCursor(self):
    self.cursor = 0

  def connect(self):
    print "Connect needs to be overridden"
    return False
    
  def query(self, rows=None):
    print "Query needs to be overridden"
  
  def readColumns(self):
    print "readColumns needs to be overridden"    
  
  def fetch_data(self, rows=1000):
    if len(self.columns) == 0:
      self.readColumns()
  
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
