import simplejson as json

class BaseHandler():
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
                    
  def get(self):
    print "Get needs to be overridden"
  
  def post(self):
    print "Post needs to be overridden"
  
  def delete(self):
    print "Delete needs to be overridden"
                        
  def put(self):
    print "Put needs to be overridden"
    
  def options(self):
    print "Options needs to be overridden"
