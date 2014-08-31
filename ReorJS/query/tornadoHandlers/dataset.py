from base import *

class APIDataSetHandler(BaseHandler):
  def get(self, id=None):
    self.application.DataSetHandler.setParent(self)

    if id == '':
      id = None

    self.application.DataSetHandler.get(id=id)
  
  def post(self, id=None):
    self.application.DataSetHandler.setParent(self)

    if id == '':
      id = None

    self.application.DataSetHandler.post(id=id)
  
  def put(self, id=None):
    self.application.DataSetHandler.setParent(self)

    if id == '':
      id = None

    self.application.DataSetHandler.put(id=id)
    
  def delete(self, id=None):
    self.application.DataSetHandler.setParent(self)

    if id == '':
      id = None

    self.application.DataSetHandler.delete(id=id)

class APIDataSetDataHandler(BaseHandler):
  def get(self, id=None):
    self.application.DataSetDataHandler.setParent(self)

    if id == '':
      id = None

    self.application.DataSetDataHandler.get(id=id)
  
  def post(self, id=None):
    self.application.DataSetDataHandler.setParent(self)

    if id == '':
      id = None

    self.application.DataSetDataHandler.post(id=id)
