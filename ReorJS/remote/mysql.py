import base
import MySQLdb as mdb
import getpass

class MySQLRemote(base.RemoteConnection):
  def connect(self):
    if self.hostname == None:
      print "Hostname not given, defaulting to localhost"
      self.hostname = 'localhost'
    
    if self.username == None:
      print "Username not given, defaulting to current user"
      self.username = getpass.getuser()
    
    if self.name == None:
      print "Database name not given, cannot proceed"
      return False
      
    if self.table == None:
      print "No table given, cannot proceed"
      return False
  
    self.connection = mdb.connect(self.hostname, self.username, self.password, self.name)
    
    return self.connection != None

  def readColumns(self):
    c = self.connection.cursor()
    c.execute('DESC %s' % self.table)
    result = c.fetchall()
    c.close()
    
    self.columns = []
    
    if result == None:
      print "Cannot read columns from data source table"
    else:
      for column in result:
        self.columns.append(column[0])

  def query(self, rows=None):
    if rows == None:
      print "Defaulting to 1000 rows"
      rows = 1000
    
    toReturn = []        
    
    query = 'SELECT %s FROM %s LIMIT %d, %d' % (",".join(self.columns), self.table, self.cursor, rows)
    
    print query
    
    c = self.connection.cursor()
    c.execute(query)
    
    #increase our cursor
    self.cursor += c.rowcount
    
    for i in range(c.rowcount):
      row = c.fetchone()
      #turn it into a hash mapped by column
      temp = {}
      j = 0
      for col in self.columns:
        temp[col] = row[j]
        j += 1
        
      #and add it to our list
      toReturn.append(temp)
  
    return toReturn
