from base import *
import api

class APIApplicationHandler(BaseHandler):
  def get(self, id=None):
    if id == None:
      results = api.db.Application.search({})
      
      self.payload([r.to_serializable_object() for r in results])
      return
    else:
      application = api.db.Application.find({ 'id' : id })
      
      if application == None:
        self.error('1001', 'Application %s not found' % id)
        return
        
      self.payload(application.to_serializable_object())
      return
    
  def post(self, id=None):
    name = self.get_argument('name', None)
    program = self.get_argument('program', None)
    
    if name == None or name.replace(' ', '') == '':
      self.error('1002', 'Application requires a name')
      return
    
    if program == None or program.replace(' ', '') == '':
      self.error('1003', 'Application requires a program')      
      return            
    
    if id == None:
      application = api.db.Application.create({ 'name' : name, 'program' : program })
      application.update()
      
      self.status('200', 'Application successfully created')
      return
    else:
      application = api.db.Application.find({ 'id' : id })
      
      if application == None:
        self.error('1001', 'Application %s not found' % id)
        return

      application.name.value(name)
      application.program.value(program)
      application.update()
      
      self.status('200', 'Application %s updated successfully' % id)
      return
  
  def delete(self, id=None):
    if id == None:
      self.error('1004', 'Cannot delete application without an application id')
      return
    
    application = api.db.Application.find({ 'id' : id })
    
    if application == None:
      self.error('1001', 'Application %s not found' % id)
      return
    
    application.delete()
    
    self.status('200', 'Application %s deleted successfully' % id)
    return
  
