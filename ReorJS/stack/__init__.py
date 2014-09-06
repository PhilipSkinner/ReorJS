import collections
import api
import logger
import random
import operator
import simplejson as json

SEQUENTIAL = 1
RANDOM = 2
SHARED = 3

stacker = None

def initStacker():
    global stacker
    stacker = StackManager(4096, method=RANDOM)
    return True

class StackManager(object):
    def __init__(self, memory, method=SEQUENTIAL):
      self.stack = collections.deque()
      self.memorylimit = memory
      
      self.method = method
      self.readLimit = 3
      
      if self.method == SHARED:
        #we need to store the read times to ensure its done equally
        self._readfrom = {}
      
      self._datasets = {}
      self._tasks = {}
      self._connections = {}
      
      self.refreshTasks()
      self.refreshDatasets()
          
    def refreshDatasets(self):
      #get the datasets for the tasks we have, quickgen an id list
      ids = []
      for i,t in self._tasks.iteritems():
        ids.append(str(t.dataset_id.value()))
        
      for i in ids:
        if i in self._datasets:
          #remove any that don't exist anymore in our task list
          #del self._datasets[i]
          a=1
        else:
          #fetch ones we don't have
          dataset = api.db.Dataset.find({ 'id' : i })
          if dataset != None:
            self._datasets[str(dataset.id.value())] = dataset
    
    def refreshTasks(self):
      #check our existing tasks still exist
      for id, t in self._tasks.iteritems():
        temp = api.db.Task.find({ 'id' : id })
        if temp == None:
          del self._tasks[id] 
    
      #get a list of tasks from the database
      tasks = api.db.Task.search({ },{ 'limit' : 15 })
      
      for t in tasks:
        if t.id.value() not in self._tasks:
          self._tasks[t.id.value()] = t
    
    def get_connection(self, dataset):
      #do we have a connection for this dataset?
      if dataset.id.value() not in self._connections:
        #nope, we'd better make one
             
        #man I love this crappy list of crap
            
        if dataset.source_type.value() == 'local':
          #we're using the api database
          import remote.local
              
          self._connections[dataset.id.value()] = remote.local.LocalRemote(name			= dataset.source_name.value(), 
                                                                           hostname		= dataset.source_hostname.value(), 
                                                                           port			= dataset.source_port.value(),
                                                                           username		= dataset.source_username.value(), 
                                                                           password		= dataset.source_password.value(), 
                                                                           table		= dataset.source_table.value())
        elif dataset.source_type.value() == 'mysql':
          #its a mysql datasource
          import remote.mysql
              
          self._connections[dataset.id.value()] = remote.mysql.MySQLRemote(name			= dataset.source_name.value(), 
                                                                           hostname		= dataset.source_hostname.value(), 
                                                                           port			= dataset.source_port.value(),
                                                                           username		= dataset.source_username.value(),
                                                                           password		= dataset.source_password.value(),
                                                                           table		= dataset.source_table.value())
        elif dataset.source_type.value() == 'mongo':
          #its mongo
          import remote.mongo
              
          self._connections[dataset.id.value()] = remote.mongo.MongoRemote(name			= dataset.source_name.value(), 
                                                                           hostname		= dataset.source_hostname.value(), 
                                                                           port			= dataset.source_port.value(),
                                                                           username		= dataset.source_username.value(),
                                                                           password		= dataset.source_password.value(),
                                                                           table		= dataset.source_table.value())
        elif dataset.source_type.value() == 'hadoop':
          #hadoop connector
          import remote.hadoop
              
          self._connections[dataset.id.value()] = remote.hadoop.HadoopRemote(name		= dataset.source_name.value(), 
                                                                             hostname		= dataset.source_hostname.value(), 
                                                                             port		= dataset.source_port.value(),
                                                                             username		= dataset.source_username.value(),
                                                                             password		= dataset.source_password.value(),
                                                                             table		= dataset.source_table.value())
        elif dataset.source_type.value() == 'redis':
          #from redis
          import remote.redis
              
          self._connections[dataset.id.value()] = remote.redis.RedisRemote(name			= dataset.source_name.value(), 
                                                                           hostname		= dataset.source_hostname.value(), 
                                                                           port			= dataset.source_port.value(),
                                                                           username		= dataset.source_username.value(),
                                                                           password		= dataset.source_password.value(),
                                                                           table		= dataset.source_table.value())
        elif dataset.source_type.value() == 'memcached':
          #from memcached
          import remote.memcached
              
          self._connections[dataset.id.value()] = remote.memcached.MemcachedRemote(name			= dataset.source_name.value(), 
                                                                                   hostname		= dataset.source_hostname.value(), 
                                                                                   port			= dataset.source_port.value(),
                                                                                   username		= dataset.source_username.value(),
                                                                                   password		= dataset.source_password.value(),          
                                                                                   table		= dataset.source_table.value())
          
    
      #just to make sure
      if dataset.id.value() in self._connections:
        #hoorah
        return self._connections[dataset.id.value()]
      
      return None    
    
    def add_task(self, task):
      self.stack.append(task)
    
    def get_status(self):
      usedmemory = sum([len(x) for x in self.stack])
      
      return {
        'stacksize' : usedmemory,
        'required' : max(0, self.memorylimit - usedmemory),
        'max' : self.memorylimit,
        'method' : self.method,        
      }
            
    def get_task(self):
      if len(self.stack) == 0:
        #check if we need to read in more task and dataset data
        if len(self._tasks) == 0:
          self.refreshTasks()
        if len(self._datasets) == 0:
          self.refreshDatasets()
        
        #did we actually get anything?
        if len(self._tasks) == 0:
          logger.LOG.log("Attempted to fetch task from system when no tasks have been defined")
          return None
        
        if len(self._datasets) == 0:
          logger.LOG.log("Attempted to fetch task from system when no task datasets have been defined")
          return None
      
        #we need to fetch some more tasks
        toRead = []
        if self.method == SEQUENTIAL:
          #just grab the first          
          for i, t in self._tasks.iteritems():
            toRead.append(t)
            break
        elif self.method == RANDOM:
          #grab a random one
          toRead.append(random.choice(self._tasks.values()))
        elif self.method == SHARED:
          #check each one in the list and compare it to its read value
          m = max(self._readfrom, key=lambda x: self._readyfrom[x[0]])          
          count = 0
          for i, t in self._tasks.iteritems():
            #if its under the max include it
            if count < self.readLimit:
              if i in self._readyfrom:
                #quick comparison
                if self._readyfrom[i] < m:
                  toRead.append(t)
              else:
                #never used before, use it!
                toRead.append(t)

        if len(toRead) == 0:
          return None        
          
        #foreach task, read in some data
        for task in toRead:
          if str(task.dataset_id.value()) in self._datasets:
            dataset = self._datasets[str(task.dataset_id.value())]
            
            connection = self.get_connection(dataset)        
            if connection != None:
              #we can fetch some data
              data = self._connections[dataset.id.value()].fetch_data(rows=10)
            
              for d in data:
                #cursor is result dataset along with the cursor position in the data read
                self.add_task({ 'script' : task.program.value(), 'data' : d['data'], 'cursor' : '%s-%s' % (task.result_id.value(), d['cursor']) }) 
      try:
        return self.stack.popleft()
      except:
        return None      

    def receive_result(self, cursor=None, result=None):
     if cursor == None or cursor == '' or result == None or result == '':
      return False
     
     #lets see if we can find the dataset for this
     tmp = cursor.split('-')
     datasetId = tmp[0]
     cursorId = tmp[1]

     #get our dataset
     dataset = None
     if datasetId not in self._datasets:
       dataset = api.db.Dataset.find({ 'id' : datasetId })
       if dataset != None:
         self._datasets[str(dataset.id.value())] = dataset
     
     if datasetId not in self._datasets:
       #we had some sort of serious issue here
       return False
              
     dataset = self._datasets[datasetId]
     
     #get our connection
     connection = self.get_connection(dataset)     
     
     if connection != None:
       connection.save_result(result=result, cursor=cursorId)
     
     return True     
      
          
