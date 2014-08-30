import stack
import query.handlers.base

class OutputService():
  def __init__(self, type=None):
    self.type = None
    
    self.GetTaskHandler = GetTaskHandler(None)
    self.PingHandler = PingHandler(None)
    self.StatusHandler = StatusHandler(None)

class GetTaskHandler(query.handlers.base.BaseHandler):
  def get(self):
    #get a task from the stack
    task = stack.stacker.get_task()

    if task != None:
      self.payload(task)
      return
    
    self.error(404, 'No tasks waiting')
    return
    
class PingHandler(query.handlers.base.BaseHandler):
  def get(self):
    #pong
    self.write('PONG')
    return
  
class StatusHandler(query.handlers.base.BaseHandler):
  def get(self):
    #get the status
    self.payload(stack.stacker.get_status())
    return

