import copy
import logger

class ConnectionBase():
  def __init__(self):
    logger.LOG.log("Connection initialization requires overriding for correct instantiation")

  def checkObject(self, object):
    logger.LOG.log("checkObject method requires overriding")

  def search(self, object, params={}, options={}):
    logger.LOG.log("search method requires overriding")

  def update(self, object):
    logger.LOG.log("update method requires overriding")

  def delete(self, object):    
    logger.LOG.log("delete method requires overriding")
    
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
      logger.LOG.log("Column cannot be null and be primary key, fixing")
      self.null = False
      
    self.afterInit()
  
  def afterInit(self):
    return self

  def __set__(self):
    logger.LOG.log("__set__ method requires overriding")

    return None

  def __create__(self):
    logget.LOG.log("__create__ method requires overriding")
  
    return None

  def value(self, val=None):
    if val == None:
      return self._value
    
    if not self.primary_key:
      self._value=val

  def __value__(self, val):
    self._value = val
