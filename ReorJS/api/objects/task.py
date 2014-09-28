"""
	api/objects/task.py
	ReorJSd API Task Object
        
        --
	Provides a description of the Task API object.
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

class Task(ObjectBase):
  __tablename__ = 'task'

  def __initattributes__(self):  
    self.id 			= self.Column('id', int, primary_key=True)
    self.owner 			= self.Column('owner', int, null=True)
    self.dataset_id 		= self.Column('dataset_id', int)    
    self.result_id 		= self.Column('result_id', int)
    self.application_id 	= self.Column('application_id', int)
    self.program 		= self.Column('program', str)
    self.status			= self.Column('status', str)
    self.progress		= self.Column('progress', str)
    self.time_started		= self.Column('time_started', int)
    self.time_ended		= self.Column('time_ended', int)
    self.block_size		= self.Column('block_size', int)
    self.read_cursor		= self.Column('read_cursor', int)
    self.completion_cursor	= self.Column('completion_cursor', int)
  
  def __repr__(self):
    return "<Task('%s')>" % self.id
  
  def to_serializable_object(self):
    return {
      'id' 			: str(self.id.value()),
      'owner' 			: self.owner.value(),
      'dataset' 		: self.dataset_id.value(),
      'result' 			: self.result_id.value(),
      'application' 		: self.application_id.value(),
      'program' 		: self.program.value(),
      'status'			: self.status.value(),
      'progress'		: self.progress.value(),
      'time_started'		: self.time_started.value(),
      'time_ended'		: self.time_ended.value(),
      'block_size'		: self.block_size.value(),
      'read_cursor'		: self.read_cursor.value(),
      'completion_cursor' 	: self.completion_cursor.value(),      
    }
