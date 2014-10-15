"""
        query/handlers/application.py
	ReorJSd API Application Handler
          
        --
	Manages the handling of requests to the application endpoints.
        --
          
        Author(s)       - Philip Skinner (philip@crowdca.lc)
        Last modified   - 2014-09-28
        
        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or   
        (at your option) any later version.
            
        This program is distributed in the hope that it will be useful,     
        but WITHOUT ANY WARRANTY; without even the implied warranty of      
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.
                 
        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>.
        
        Copyright (c) 2014, Crowdcalc B.V.
"""

from base import *
import api

class APIApplicationHandler(BaseHandler):
  def get(self, id=None):
    if id == None or id == '':
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
    
    if id == None or id == '':
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
    if id == None or id == '':
      self.error('1004', 'Cannot delete application without an application id')
      return
    
    application = api.db.Application.find({ 'id' : id })
    
    if application == None:
      self.error('1001', 'Application %s not found' % id)
      return
    
    application.delete()
    
    self.status('200', 'Application %s deleted successfully' % id)
    return
  
