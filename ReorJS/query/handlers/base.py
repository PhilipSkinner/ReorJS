import simplejson as json

class BaseHandler():
  def __init__(self, server):
    self.server = server
    self.parent = None
  
  def setParent(self, parent):
    self.parent = parent

  def write(self, value):
    self.parent.write(value)

  def set_header(self, name, value):
    self.parent.set_header(name, value)

  def get_argument(self, name, default):
    return self.parent.get_argument(name, default)

  def json(self, obj):
    data = json.dumps(obj) if not isinstance(obj, basestring) else obj
    self.set_header('Content-Type', 'application/json')
    self.write(data)
    return
  
  def jsonp(self, obj):
    cb = self.get_argument('callback', None)
    
    if cb == None:
      self.json(obj)
      return
                                    
    data = json.dumps(obj) if not isinstance(obj, basestring) else obj
    self.set_header('Content-Type', 'text/javascript')
    self.write("%s(%s);" % (cb, data))
    return
  
  def payload(self, data, code='200'):
    self.jsonp({ 'meta' : { 'code' : code }, 'data' : data })
    return
  
  def error(self, code, message):
    self.jsonp({ 'meta' : { 'code' : code }, 'error' : { 'message' : message } })
    return
  
  def status(self, code, message):
    self.jsonp({ 'meta' : { 'code' : code}, 'status' : { 'message' : message } })
    return
                    
  def get(self):
    self.error('405', 'Unsupported method - GET')
    return
  
  def post(self):
    self.error('405', 'Unsupported method - POST')
    return
  
  def delete(self):
    self.error('405', 'Unsupported method - DELETE')
    return
                        
  def put(self):
    self.error('405', 'Unsupported method - PUT')
    return
    
  def options(self):
    self.error('405', 'Unsupported method - OPTION')
    return
