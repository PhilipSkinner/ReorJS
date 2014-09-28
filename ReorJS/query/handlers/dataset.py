"""
        query/handlers/dataset.py
	ReorJSd API Dataset Handlers
          
        --
	Provides the handlers for the Dataset HTTP endpoints.
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

class APIDataSetHandler(BaseHandler):
  def get(self, id=None):  
    if id == None or id == '':
      results = api.db.Dataset.search({})
      
      self.payload([r.to_serializable_object() for r in results])
      return
    else:
      dataset = api.db.Dataset.find({ 'id' : id })
      
      if dataset == None:
        self.error('2001', 'Dataset %s not found' % id)
        return
      
      self.payload(dataset.to_serializable_object())
      return
  
  def post(self, id=None):
    name 		= self.get_argument('name', None)
    source_type 	= self.get_argument('source_type', None)
    source_name 	= self.get_argument('source_name', None)
    source_hostname 	= self.get_argument('source_hostname', None)
    source_username 	= self.get_argument('source_username', None)
    source_port 	= self.get_argument('source_port', None)
    source_table 	= self.get_argument('source_table', None)
    source_password	= self.get_argument('source_password', None)
    
    if name == None or name.replace(' ', '') == '':
      self.error('2002', 'Dataset requires a name')
      return
    
    if id == None or id == '':
      dataset = api.db.Dataset.create({ 'name' 			: name, 
                                        'source_type' 		: source_type, 
                                        'source_name' 		: source_name, 
                                        'source_hostname' 	: source_hostname, 
                                        'source_username' 	: source_username, 
                                        'source_password'	: source_password,
                                        'source_port' 		: source_port, 
                                        'source_table' 		: source_table })
      dataset.update()
      
      self.status('200', 'Dataset successfully created')
      return
    else:
      dataset = api.db.Dataset.find({ 'id' : id })
      
      if dataset == None:
        self.error('2001', 'Dataset %s not found' % id)
        return
      
      dataset.name.value(name)
      dataset.source_type.value(source_type)
      dataset.source_name.value(source_name)
      dataset.source_hostname.value(source_hostname)
      dataset.source_username.value(source_username)
      dataset.source_password.value(source_password)
      dataset.source_port.value(source_port)
      dataset.source_table.value(source_table)
      dataset.update()
      
      self.status('200', 'Dataset %s updated successfully' % id)
      return
  
  def put(self, id=None):
    self.post(id=id)
  
  def delete(self, id=None):
    if id == None or id == '':
      self.error('2003', 'Cannot delete dataset without a dataset id')
      return
    
    dataset = api.db.Dataset.find({ 'id' : id })
    
    if dataset == None:
      self.error('2001', 'Dataset %s not found' % id)
      return
    
    dataset.delete()
    
    self.status('200', 'Dataset %s deleted successfully' % id)
    return

class APIDataSetDataHandler(BaseHandler):
  def get(self, id=None):
    if id == None or id == '':
      self.error('2004', 'Dataset data fetching requires dataset id')
      return
    
    results = api.db.DatasetData.search({ 'dataset' : id })
    
    self.payload([r.to_serializable_object() for r in results])
    return
  
  def post(self, id=None):
    items = self.get_arguments('data', [])
    
    if len(items) == 0 or items == None:
      self.error('2005', 'Data must be provided for insertion')
      return
    
    dataset = api.db.Dataset.find({ 'id' : id })
    
    if dataset == None:
      self.error('2001', 'Dataset %s not found' % id)
      return
    
    count = 0;
    for point in items:
      temp = api.db.DatasetData.create({ 'dataset' : id, 'data' : point, 'custom_id' : '' })
      temp.update()
      count += 1
      
    self.status('200', '%d datapoints added to dataset %s' % (count, id))
    return

