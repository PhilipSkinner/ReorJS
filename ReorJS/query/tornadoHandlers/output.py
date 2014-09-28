"""
        query/tornadoHandlers/output.py
        ReorJSd Output Tornado Handlers
          
        --
        Tornado handlers for Output endpoints.
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

class GetTask(BaseHandler):
  def get(self):
    self.application.output.GetTaskHandler.setParent(self)
    
    self.application.output.GetTaskHandler.get()

class Ping(BaseHandler):
  def get(self):
    self.application.output.PingHandler.setParent(self)
    
    self.application.output.PingHandler.get()
    
class Status(BaseHandler):
  def get(self):
    self.application.output.StatusHandler.setParent(self)
    
    self.application.output.StatusHandler.get()
