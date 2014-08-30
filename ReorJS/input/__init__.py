import stack
import query.handlers.base

class InputService():
  def __init__(self):
    self.type = None
    
    self.ReceiveResultHandler = ReceiveResultHandler(None)

class ReceiveResultHandler(query.handlers.base.BaseHandler):
  def post(self):
    cursor = self.get_argument('cursor', None)
    result = self.get_argument('result', None)
    
    if cursor == None or cursor == '':
      self.error('5001', 'Missing cursor for result')
      return
    
    if result == None or result == '':
      self.error('5002', 'Missing result for cursor')
      return
      
    stack.stacker.receive_result(cursor=cursor, result=result)
    
    self.status('200', 'Result received')
    return
