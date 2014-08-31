from base import *

class ReceiveResult(BaseHandler):
  def post(self):
    self.application.input.ReceiveResultHandler.setParent(self)
    
    self.application.input.ReceiveResultHandler.post()
