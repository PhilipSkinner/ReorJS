import copy

class ObjectBase():
  __tablename__ = None

  def __init__(self, parent=None, init=False):
    self.__attributes__ = False
  
    if parent == None:
      print "Error attempting object passthrough instantiation, no parent object given."

      return None
      
    #init objects attributed
    self.connection = parent.connection
    self.__initattributes__()  
    
    if init:
      self.connection().checkObject(self)

  def __initattributes__(self):
    return self      
  
  def __repr__(self):
    return "<ObjectBase>"
    
  def _checkParams(self, params):
    #check params

    #make sure our attributes are good
    if not self.__attributes__:
      self.__initattributes__()
    
    if not type(params) is dict:
      print "Parameters passed must be of type dict, not %s" % type(params)
      return False
    
    for column, value in params.iteritems():
      if not type(column) is str:
        print "Passed parameter column names must be of type str, not %s" % type(column)
        return False
        
      if not hasattr(self, column):
        print "%s has no such attribute %s" % (self, column)
        return False
    
    return True
  
  def search(self, params={}, options={}):
    return self.connection().search(self, params, options)

  def find(self, params):
    #run a search and return the first item
    results = self.search(params=params, options={ 'limit' : 1 })
    
    if results != None and len(results) > 0:
      return results[0]
    
    return None

  def create(self, params):
    #match the params against our configured parameters
    if not self._checkParams(params):
      return False
    
    #set our attributes
    for column, value in params.iteritems():
      col = getattr(self, column)
      col.value(value)
    
    return self
          
  def update(self):
    self.connection().update(self)

  def delete(self):    
    self.connection().delete(self)
  
  def Column(self, name, type, primary_key=False, null=False):
    return self.connection().column(name, type, primary_key=primary_key, null=null)
