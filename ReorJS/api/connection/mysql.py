"""
	api/connection/mysql.py
	ReorJSd API MySQL Connector
	        
        --
	Provides methods for loading and saving data to and from a MySQL
	database instance.
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

import copy
import logger
from base import ConnectionBase
from base import ColumnBase

class Connection(ConnectionBase):
  def __init__(self, connection):
    self.connection = connection

  def checkObject(self, object):
    #first check, does the table exist?
    logger.LOG.log("Checking for existance of object %s in data source" % object.__tablename__)

    result = None
      
    try:
      cursor = self.connection().cursor()
      cursor.execute('DESC %s' % object.__tablename__)
        
      result = cursor.fetchall()
      cursor.close()
    except:
      pass
      
    if result != None:
      logger.LOG.log("Checking existing structure...")
      #convert result into usable dict
      current = {}
        
      for column in result:
        current[column[0]] = {
          'type' : column[1],
          'null' : column[2],
          'key'  : column[3],
        }
      
      correct = True
      #check all attributes of the object to see if they match
      for attribute, value in object.__dict__.items():
        if isinstance(value, Column):
          #check it out
          if value.name in current:
            if current[value.name]['type'] == 'text':
              if value.type != str:
                correct = False
            elif current[value.name]['type'] == 'int(11)':
              if value.type != int:
                correct = False
              
            if current[value.name]['null'] == 'YES':
              if value.null == False:
                correct = False
            else:
              if value.null == True:
                correct = False
              
            if current[value.name]['key'] == 'PRI':
              if value.primary_key == False:
                correct = False
            else:
              if value.primary_key == True:
                correct = False
          else:
            correct = False
        
      if not correct:
        logger.LOG.log("Structure is not correct, removing existing object...")
        result = None
          
        query = "DROP TABLE %s" % object.__tablename__
        cursor = self.connection().cursor()
        cursor.execute(query)
        self.connection().commit()
        cursor.close()
      else:
        logger.LOG.log("Structure looks good!")

    if result == None:
      logger.LOG.log("Object %s does not exist yet, creating..." % object.__tablename__)
        
      query = "CREATE TABLE %s (" % object.__tablename__
      cols = []
      #get a list of all attributed and their types then create them
      for attribute, value in object.__dict__.items():
        if isinstance(value, Column):
          #good to go
          cols.append(value.__create__())
        
      query += '%s)' % ','.join(cols)
                                
      cursor = self.connection().cursor()
      cursor.execute(query)
      self.connection().commit()
      cursor.close()
  
  def search(self, object, params={}, options={}):
    if not object._checkParams(params):
      return []
      
    if object.__tablename__ == None:
      logger.LOG.log("%s Object table name needs to be set" % self)
      return []
      
    columns = []
    for attribute, value in object.__dict__.items():
      if isinstance(value, Column):
        columns.append(value.name)
    
    query = 'SELECT %s FROM %s WHERE 1=1 ' % (",".join(columns), object.__tablename__)
    
    for column, value in params.iteritems():
      query += ' AND %s = "%s" ' % (column, value)
    
    if 'limit' in options:
      query += ' LIMIT %s ' % options['limit']
      
    cursor = self.connection().cursor()
    cursor.execute(query)
    
    results = cursor.fetchall()
    
    toReturn = []    
    for result in results:
      #create a temporary dict
      temp = {}
      
      i = 0
      for c in columns:
        temp[c] = result[i]
        i += 1
      
      #now create a copy of ourself with these values
      obj = copy.deepcopy(object)
      
      for column, value in temp.iteritems():
        col = getattr(obj, column)
        col.__value__(value)
      
      toReturn.append(obj)

    self.connection().commit()
    cursor.close()
    return toReturn              

  def update(self, object):
    #save our current objects attributes to our permanent store
    logger.LOG.log("Save in DB pls")
   
    result = False
    #attempt an update and then fail over to an insert
    try:
      query = "UPDATE %s SET " % object.__tablename__
      set = []
      pk = None
      for attribute, value in object.__dict__.items():
        if isinstance(value, Column):
          if value.primary_key:
            pk = value
          else:
            set.append(value.__set__())
    
      if pk == None:
        logger.LOG.log("Issue calling update, no primary key given. Defaulting to insert only for %s" % object)
      else:    
        query += '%s WHERE %s = %s' % (','.join(set), pk.name, pk.value())
        
        cursor = self.connection().cursor()
        cursor.execute(query)
        self.connection().commit()
        cursor.close()
        
        if cursor.rowcount > 0:
          result = True
    except:
      pass
      
    if result == False:
      try:
        #now do an insert please      
        columns = []
        values = []
        for attribute, value in object.__dict__.items():
          if isinstance(value, Column):
            columns.append(value.name)
            if value.value() == None:
              values.append('NULL')
            else:
              values.append('"%s"' % value.value().replace('"', '\\"').replace(';', '\\;'))                      
      
        query = "INSERT INTO %s (%s) VALUES (%s)" % (object.__tablename__, ",".join(columns), ",".join(values))
        
        cursor = self.connection().cursor()
        cursor.execute(query)
        self.connection().commit()
        cursor.close()
      
        logger.LOG.log("Inserted %d rows" % cursor.rowcount)
      except:
        pass

  def delete(self, object):    
    #delete our objects from its permanent store
    pk = None
    for attribute, value in object.__dict__.items():
      if isinstance(value, Column):
        if value.primary_key:
          pk = value
    
    if pk == None:
      logger.LOG.log("Issue calling delete, no primary key given. Object will not be deleted")
      return False
    
    query = "DELETE FROM %s WHERE %s = %s" % (object.__tablename__, pk.name, pk.value())
    cursor = self.connection().cursor()
    cursor.execute(query)
    self.connection().commit()
    cursor.close()
    
    logger.LOG.log("Object deleted")
    
    return False
  
  def column(self, name, type, primary_key=False, null=False):
    return Column(name, type, primary_key=primary_key, null=null)
    
class Column(ColumnBase):  
  def __set__(self):
    query = '%s = "%s"' % (self.name, self.value().replace('"', '\\"'))
    
    return query

  def __create__(self):
    query = '%s ' % self.name
    if self.type == int:
      query += ' int(11) '
    elif self.type == str:
      query += ' text '
    
    if self.null:
      query += ' NULL '
    else:
      query += ' NOT NULL '
    
    if self.primary_key:
      query += ' PRIMARY KEY AUTO_INCREMENT '
    
    return query
