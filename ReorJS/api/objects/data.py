"""
	api/objects/data.py
	ReorJSd API Data Object
        
        --
	Provides a description of the Dataset and DatasetData API objects.
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

from base import ObjectBase

class Dataset(ObjectBase):
  __tablename__ = 'dataset'

  def __initattributes__(self):
    self.id 			= self.Column('id', int, primary_key=True)
    self.name 			= self.Column('name', str)
    self.source_type 		= self.Column('source_type', str)
    self.source_name 		= self.Column('source_name', str)
    self.source_hostname 	= self.Column('source_hostname', str)
    self.source_port 		= self.Column('source_port', str)
    self.source_username 	= self.Column('source_username', str)
    self.source_password 	= self.Column('source_password', str)
    self.source_table		= self.Column('source_table', str)
    self.created 		= self.Column('created', str, null=True)

  def __repr__(self):
    return "<Dataset('%s')>" % self.id
    
  def to_serializable_object(self):
    return {
      'id' 		: str(self.id.value()),
      'name' 		: self.name.value(),
      'source_type' 	: self.source_type.value(),
      'source_name' 	: self.source_name.value(),
      'source_hostname' : self.source_hostname.value(),
      'source_port' 	: self.source_port.value(),
      'source_username' : self.source_username.value(),
      'source_password' : self.source_password.value(),
      'source_table'	: self.source_table.value(),
      'created' 	: str(self.created.value()),
    }

class DatasetData(ObjectBase):
  __tablename__ = 'dataset_data'
  
  def __initattributes__(self):
    self.id 			= self.Column('id', int, primary_key=True)
    self.dataset_id 		= self.Column('dataset', int)
    self.custom_id 		= self.Column('custom_id', str)
    self.data 			= self.Column('data', str)
  
  def __repr__(self):
    return "<DatasetData('%s')>" % self.id

  def to_serializable_object(self):
    return {
      'id' 		: str(self.id.value()),
      'dataset' 	: self.dataset_id.value(),
      'custom_id' 	: self.custom_id.value(),
      'data' 		: self.data.value(),
    }
  
