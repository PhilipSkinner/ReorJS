"""
	api/objects/stacker.py
	ReorJSd API Stacker Object
        
        --
	Provides a description of the Stacker API object.
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

class Stacker(ObjectBase):
  __tablename__ = 'stacker'

  def __initattributes__(self):  
    self.id 			= self.Column('id', int, primary_key=True)
    self.ip 			= self.Column('ip', str)
    self.port 			= self.Column('port', int)
    self.status 		= self.Column('status', int)
  
  def __repr__(self):
    return "<Stacker('%s')>" % self.id
  
  def to_serializable_object(self):
    return {
      'id' 		: str(self.id.value()),
      'ip' 		: self.ip.value(),
      'port' 		: self.port.value(),
      'status' 		: self.status.value(),
    }
