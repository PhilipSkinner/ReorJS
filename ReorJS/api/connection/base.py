import copy

class ConnectionBase():
  def __init__(self):
    print "Connection initialization requires overriding for correct instantiation"

  def checkObject(self, object):
    print "checkObject method requires overriding"

  def search(self, object, params={}, options={}):
    print "search method requires overriding"

  def update(self, object):
    print "update method requires overriding"

  def delete(self, object):    
    print "delete method requires overriding"
    
  def column(self, name, type, primary_key=False, null=False):
    return ColumnBase(name, type, primary_key=primary_key, null=null)
    
class ColumnBase():  
  def __init__(self, name, type, primary_key=False, null=False):
    self._value = None
    self.name = name
    self.type = type
    
    self.null = null
    self.primary_key = primary_key
    
    if self.null and self.primary_key:
      print "Column cannot be null and be primary key, fixing"
      self.null = False

  def __set__(self):
    print "__set__ method requires overriding"

    return None

  def __create__(self):
    print "__create__ method requires overriding"
  
    return None

  def value(self, val=None):
    if val == None:
      return self._value
    
    if not self.primary_key:
      self._value=val

  def __value__(self, val):
    self._value = val
