"""
        query/handlers/task.py
	ReorJS API Task Handlers
          
        --
	Provides handlers for the Task HTTP endpoints.
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
import settings

class APITaskHandler(BaseHandler):
  def get(self, id=None):
    if id == None or id == '':
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
    result = self.get_argument('result', None)
    
    if application == None:
      self.error('3002', 'Application ID required')
      return
      
    if dataset == None:
      self.error('3003', 'Dataset ID required')
      return
    
    if result == None:
      self.error('3004', 'Result ID required')
      return

    app = api.db.Application.find({ 'id' : application })
    
    if app == None:
      self.error('3005', 'No such application %s' % application)
      return
      
    data = api.db.Dataset.find({ 'id' : dataset })
    
    if data == None:
      self.error('3006', 'No such dataset %s' % dataset)
      return    
    
    resultSet = api.db.Dataset.find({ 'id' : result })
    
    if resultSet == None:
      self.error('3007', 'No such result dataset %s' % dataset)
      return
    
    if id == None or id == '':
      task = api.db.Task.create({ 'application_id' : application, 'dataset_id' : dataset, 'program' : app.program.value(), 'result_id' : result, 
                                  'status' : 'Pending', 'progress' : '0.00%', 'time_started' : 0, 'time_ended' : 0, 'block_size' : settings.BLOCKSIZE, 
                                  'read_cursor' : 0, 'completion_cursor' : 0 })
      task.update()
      
      self.status('200', 'Task created')
      return
    else:
      self.error('3010', 'Task manipulation not yet supported')
      return
  
