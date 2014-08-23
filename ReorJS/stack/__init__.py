import collections
import api
import random
import operator

def SEQUENTIAL = 1
def RANDOM = 2
def SHARED = 3

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
            
    def get_task(self):
      if len(self.stack) == 0:
        #check if we need to read in more task and dataset data
        if len(self._tasks) == 0:
          self.refreshTasks():
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
            if dataset.source_type.value() == 'local':
              #we're using the api database
            elif dataset.source_type.value() == 'mysql':
              #its a mysql datasource
            elif dataset.source_type.value() == 'mongo':
              #its mongo
            elif dataset.source_type.value() == 'hadoop':
              #hadoop connector
            elif dataset.source_type.value() == 'redis':
              #from redis
            elif dataset.source_type.value() == 'memcached':
              #from memcached
          
      try:
        return self.stack.popleft()
      except:
        return None      

