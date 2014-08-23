from base import *
import api

class APITaskHandler(BaseHandler):
  def get(self, id=None):
    if id == None:
      tasks = api.db.Task.search({})
      
      self.payload([t.to_serializable_object() for t in tasks])
      return
    else:
      task = api.db.Task.find({ 'id' : id })
      
      if task == None:
        self.error('3001', 'Task %s not found' % id)
        return
      
      self.payload(task.to_serializable_object())
      return
  
  def post(self, id=None):
    application = self.get_argument('application', None)
    dataset = self.get_argument('dataset', None)
    
    if application == None:
      self.error('3002', 'Application ID required')
      return
      
    if dataset == None:
      self.error('3003', 'Dataset ID required')
      return

    app = api.db.Application.find({ 'id' : application })
    
    if app == None:
      self.error('3004', 'No such application %s' % application)
      return
      
    data = api.db.Dataset.find({ 'id' : dataset })
    
    if data == None:
      self.error('3005', 'No such dataset %s' % dataset)
      return    
    
    if id == None:
      task = api.db.Task.create({ 'application_id' : application, 'dataset_id' : dataset, 'program' : app.program.value() })
      task.update()
      
      self.status('200', 'Task created')
      return
    else:
      self.error('3010', 'Task manipulation not yet supported')
      return
  
