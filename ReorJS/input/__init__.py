"""
	input/__init__py
	ReorJSd InputService
        
        --
	Provides the Task Receiving endpoint and handler for the HTTP service.
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
import traceback
import sys

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
    
    try:  
      stack.stacker.receive_result(cursor=cursor, result=result)
    except Exception, err:
      print traceback.format_exc()
      print sys.exc_info()
    
    self.status('200', 'Result received')
    return
