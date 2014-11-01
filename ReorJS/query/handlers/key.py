"""
        query/handlers/key.py
	ReorJSd API Key Handler
          
        --
	Manages the handling of requests to the key endpoints.
        --
          
        Author(s)       - Philip Skinner (philip@crowdca.lc)
        Last modified   - 2014-10-25
        
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
import string
import random

class APIKeyHandler(BaseHandler):
  def get(self, id=None):
    if not self.checkCredentials(self.get_argument('key', None), True):
      self.error('9001', 'Invalid API key')
      return
      
    if id == None or id == '':
      results = api.db.Key.search({})
      
      self.payload([r.to_serializable_object() for r in results])
      return
    else:   
      key = api.db.Key.find({ 'id' : id })
      
      if key == None:
        self.error('6001', 'Key %s not found' % id)
        return   
        
      self.payload(key.to_serializable_object())
      return

      
  def post(self, id=None):
    if not self.checkCredentials(self.get_argument('key', None), True):
      self.error('9001', 'Invalid API key')
      return
    
    key = api.db.Key.create({ 'access_key' : ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(24)) })
    key.update()

    self.status('200', 'Key successfully created')
    return                
  
  def delete(self, id=None):
    if not self.checkCredentials(self.get_argument('key', None), True):
      self.error('9001', 'Invalid API key')
      return

    if id == None or id == '':
      self.error('6002', 'Cannot delete key without a key id')
      return

    key = api.db.Key.find({ 'id' : id })

    if key == None:
      self.error('6001', 'Key %s not found' % id)
      return

    key.delete()

    self.status('200', 'Key %s deleted successfully' % id)
    return  
