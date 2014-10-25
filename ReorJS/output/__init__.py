"""
	output/__init__.py
	ReorJSd Output Service
        
        --
	Provides the endpoints and handlers for the OutputService.
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
    if not self.checkCredentials(self.get_argument('key', None)):
      self.error('9001', 'Invalid API key')
      return

    #pong
    self.write('PONG')
    return
  
class StatusHandler(query.handlers.base.BaseHandler):
  def get(self):
    if not self.checkCredentials(self.get_argument('key', None)):
      self.error('9001', 'Invalid API key')
      return

    #get the status
    self.payload(stack.stacker.get_status())
    return

