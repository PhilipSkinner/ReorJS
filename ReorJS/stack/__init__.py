import collections
import api
import random
import operator

SEQUENTIAL = 1
RANDOM = 2
SHARED = 3

stacker = None

def initStacker():
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
        ids.append(t.dataset_id.value())
      
      for i in ids:
        if i in self._datasets:
          #remove any that don't exist anymore in our task list
          del self._datasets[i]
        else:
          #fetch ones we don't have
          dataset = api.Dataset.find({ 'id' : i })
          if dataset != None:
            self._datasets[dataset.id.value()] = dataset
    
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
          print "Attempted to fetch task from system when no tasks have been defined"
          return None
        
        if len(self._datasets) == 0:
          print "Attempted to fetch task from system when no task datasets have been defined"
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
          toRead = random.choice(self._tasks.values())
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
        
        #foreach task, read in some data
        for task in toRead:
          dataset = self._datasets[task.dataset_id.value()]
        
          #do we have a connection for this dataset?
          if dataset.id.value() not in self._connections:
            #nope, we'd better make one
            
            #man I love this crappy list of crap
            
            if dataset.source_type.value() == 'local':
              #we're using the api database
              import remote.local
              
              self._connections[dataset.id.value()] = remote.local.LocalRemote(name			= dataset.source_name.value(), 
                                                                               hostname			= dataset.source_hostname.value(), 
                                                                               port			= dataset.source_port.value(),
                                                                               username			= dataset.source_username.value(), 
                                                                               password			= dataset.source_password.value(), 
                                                                               table			= dataset.source_table.value())
            elif dataset.source_type.value() == 'mysql':
              #its a mysql datasource
              import remote.mysql
              
              self._connections[dataset.id.value()] = remote.mysql.MySQLRemote(name			= dataset.source_name.value(), 
                                                                               hostname			= dataset.source_hostname.value(), 
                                                                               port			= dataset.source_port.value(),
                                                                               username			= dataset.source_username.value(),
                                                                               password			= dataset.source_password.value(),
                                                                               table			= dataset.source_table.value())
            elif dataset.source_type.value() == 'mongo':
              #its mongo
              import remote.mongo
              
              self._connections[dataset.id.value()] = remote.mongo.MongoRemote(name			= dataset.source_name.value(), 
                                                                               hostname			= dataset.source_hostname.value(), 
                                                                               port			= dataset.source_port.value(),
                                                                               username			= dataset.source_username.value(),
                                                                               password			= dataset.source_password.value(),
                                                                               table			= dataset.source_table.value())
            elif dataset.source_type.value() == 'hadoop':
              #hadoop connector
              import remote.hadoop
              
              self._connections[dataset.id.value()] = remote.hadoop.HadoopRemote(name			= dataset.source_name.value(), 
                                                                               hostname			= dataset.source_hostname.value(), 
                                                                               port			= dataset.source_port.value(),
                                                                               username			= dataset.source_username.value(),
                                                                               password			= dataset.source_password.value(),
                                                                               table			= dataset.source_table.value())
            elif dataset.source_type.value() == 'redis':
              #from redis
              import remote.redis
              
              self._connections[dataset.id.value()] = remote.redis.RedisRemote(name			= dataset.source_name.value(), 
                                                                               hostname			= dataset.source_hostname.value(), 
                                                                               port			= dataset.source_port.value(),
                                                                               username			= dataset.source_username.value(),
                                                                               password			= dataset.source_password.value(),
                                                                               table			= dataset.source_table.value())
            elif dataset.source_type.value() == 'memcached':
              #from memcached
              import remote.memcached
              
              self._connections[dataset.id.value()] = remote.memcached.MemcachedRemote(name			= dataset.source_name.value(), 
                                                                                       hostname			= dataset.source_hostname.value(), 
                                                                                       port			= dataset.source_port.value(),
                                                                                       username			= dataset.source_username.value(),
                                                                                       password			= dataset.source_password.value(),          
                                                                                       table			= dataset.source_table.value())
          
          #just to make sure
          if dataset.id.value() in self._connections:
            #we can fetch some data
            data = self._connections[dataset.id.value()].fetch_data(rows=10)
            
            for d in data:
              self.add_task(json.dumps({ 'script' : task.program.value(), 'data' : d })) 

      try:
        return self.stack.popleft()
      except:
        return None      

