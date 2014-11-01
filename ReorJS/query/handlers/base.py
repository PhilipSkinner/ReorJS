"""
        query/handlers/base.py
	ReorJSd HTTP Handler Base	
          
        --
	Provides a framework for creating HTTP endpoint handlers.
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

import simplejson as json
import settings
import api

class BaseHandler():
  def __init__(self, server):
    self.server = server
    self.parent = None
  
  def setParent(self, parent):
    self.parent = parent

  def write(self, value):
    self.parent.write(value)

  def set_header(self, name, value):
    self.parent.set_header(name, value)

  def get_argument(self, name, default):
    return self.parent.get_argument(name, default)

  def json(self, obj):
    data = json.dumps(obj) if not isinstance(obj, basestring) else obj
    self.set_header('Content-Type', 'application/json')
    self.write(data)
    return
  
  def jsonp(self, obj):
    cb = self.get_argument('callback', None)
    
    if cb == None:
      self.json(obj)
      return
                                    
    data = json.dumps(obj) if not isinstance(obj, basestring) else obj
    self.set_header('Content-Type', 'text/javascript')
    self.write("%s(%s);" % (cb, data))
    return
  
  def payload(self, data, code='200'):
    self.jsonp({ 'meta' : { 'code' : code }, 'data' : data })
    return
  
  def error(self, code, message):
    self.jsonp({ 'meta' : { 'code' : code }, 'error' : { 'message' : message } })
    return
  
  def status(self, code, message, id=None):
    self.jsonp({ 'meta' : { 'code' : code}, 'status' : { 'message' : message }, 'id' : id })
    return
  
  def checkCredentials(self, key, rootOnly=False):
    if key == settings.ROOT_KEY:
      return True
    
    if rootOnly:
      return False
    
    #now we search for an applicable key
    target = api.db.Key.find({ 'access_key' : key })    
    if key != None:
      return True
    
    return False
                    
  def get(self):
    self.error('405', 'Unsupported method - GET')
    return
  
  def post(self):
    self.error('405', 'Unsupported method - POST')
    return
  
  def delete(self):
    self.error('405', 'Unsupported method - DELETE')
    return
                        
  def put(self):
    self.error('405', 'Unsupported method - PUT')
    return
    
  def options(self):
    self.error('405', 'Unsupported method - OPTION')
    return
