from base import *

class APIDataSetHandler(BaseHandler):
  def get(self, id=None):
    self.application.DataSetHandler.get()

class APIDataSetDataHandler(BaseHandler):
  def get(self, id=None):
    self.application.DataSetDataHandler.get()
