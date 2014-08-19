import copy
from base import ConnectionBase
from base import ColumnBase

class Connection(ConnectionBase):
  def __init__(self, connection):
    self.connection = connection

  def checkObject(self, object):
    #first check, does the table exist?
    print "Checking for existance of object %s in data source" % object.__tablename__

    result = None
      
    try:
      cursor = self.connection().cursor()
      cursor.execute('DESC %s' % object.__tablename__)
        
      result = cursor.fetchall()
      cursor.close()
    except:
      pass
      
    if result != None:
      print "Checking existing structure..."
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
        print "Structure is not correct, removing existing object..."
        result = None
          
        query = "DROP TABLE %s" % object.__tablename__
        cursor = self.connection().cursor()
        cursor.execute(query)
        cursor.close()
      else:
        print "Structure looks good!"

    if result == None:
      print "Object %s does not exist yet, creating..." % object.__tablename__
        
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
      cursor.close()
  
  def search(self, object, params={}, options={}):
    if not object._checkParams(params):
      return []
      
    if object.__tablename__ == None:
      print "%s Object table name needs to be set" % self
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

    cursor.close()
    return toReturn              

  def update(self, object):
    #save our current objects attributes to our permanent store
    print "Save in DB pls"
   
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
        print "Issue calling update, no primary key given. Defaulting to insert only for %s" % object
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
              values.append('"%s"' % value.value())
      
        query = "INSERT INTO %s (%s) VALUES (%s)" % (object.__tablename__, ",".join(columns), ",".join(values))
      
        cursor = self.connection().cursor()
        cursor.execute(query)
        self.connection().commit()
        cursor.close()
      
        print "Inserted %d rows" % cursor.rowcount
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
      print "Issue calling delete, no primary key given. Object will not be deleted"
      return False
    
    query = "DELETE FROM %s WHERE %s = %s" % (object.__tablename__, pk.name, pk.value())
    cursor = self.connection().cursor()
    cursor.execute(query)
    self.connection().commit()
    cursor.close()
    
    print "Object deleted"
    
    return False
  
  def column(self, name, type, primary_key=False, null=False):
    return Column(name, type, primary_key=primary_key, null=null)
    
class Column(ColumnBase):  
  def __set__(self):
    query = '%s = "%s"' % (self.name, self.value())
    
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
