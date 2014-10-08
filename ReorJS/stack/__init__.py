"""
	stack/__init__.py
	ReorJSd Simple Stacking Mechanism
        
        --
	Provides the task and result stacking mechanisms for the service.
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

import collections
import api
import logger
import random
import operator
import simplejson as json
import time
import settings

SEQUENTIAL = 1
RANDOM = 2
SHARED = 3

stacker = None

def initStacker():
    global stacker
    stacker = StackManager(4096, method=settings.READMETHOD)
    return True

class StackManager(object):
    def __init__(self, memory, method=settings.READMETHOD):
      self.stack = collections.deque()
      self.pending = collections.deque()
      self.memorylimit = memory
      
      self.method = method
      self.readLimit = 3
      
      if self.method == SHARED:
        #we need to store the read times to ensure its done equally
        self._readfrom = {}
      
      self._datasets = {}
      self._tasks = {}
      self._taskResultCursors = {}
      self._connections = {}
      self._reqCounter = 0
      
      self.refreshTasks(initial=True)
      self.refreshDatasets()
          
    def refreshDatasets(self, initial=False):
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
      
    
    def refreshTasks(self, initial=False):
      #check our existing tasks still exist
      newT = {}
      logger.LOG.debug("Checking tasks")
      for id, t in self._tasks.iteritems():
        temp = api.db.Task.find({ 'id' : id })
        logger.LOG.debug("Checking task %s" % id)
        if (temp != None and temp.time_ended.value() == 0):
          logger.LOG.debug("Task is good")
          newT[id] = t

      self._tasks = newT
      logger.LOG.debug("Our tasks have been set")
    
      #get a list of tasks from the database
      logger.LOG.debug("Searching for new tasks")
      tasks = api.db.Task.search({ 'time_ended' : 0 },{ 'limit' : settings.TASKLIMIT })
      
      for t in tasks:      
        logger.LOG.debug("Checking task %s" % t.id.value())
        if t.id.value() not in self._tasks:
          logger.LOG.debug("Its a new task!")
          t.status.value('Stacking')          
          t.read_cursor.value(t.completion_cursor.value())
          t.update()
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
      self.pending.append(task)
      
    def release_tasks(self):
      try:
        while len(self.pending) > 0:
          self.stack.append(self.pending.popleft())
      except:
        pass
    
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
        self._reqCounter += 1
        #check if we need to read in more task and dataset data
        if len(self._tasks) == 0 or self._reqCounter > 100:
          self._reqCounter = 0
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
            if t.status.value() in ['Stacking', 'Pending']:
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
            if task.status.value() == 'Pending':
              task.time_started.value(int(round(time.time() * 1000)))
              task.status.value('Stacking')
              task.update()
          
            dataset = self._datasets[str(task.dataset_id.value())]
            
            connection = self.get_connection(dataset)        
            if connection != None:
              #we can fetch some data
              data = self._connections[dataset.id.value()].fetch_data(rows=task.block_size.value(), cursor=task.read_cursor.value())
              finished = False
              
              if len(data) > 0:
                for d in data:
                  #cursor is result dataset along with the cursor position in the data read
                  self.add_task({ 'script' : task.program.value(), 'data' : d['data'], 'cursor' : '%s-%s-%s' % (task.id.value(), task.result_id.value(), d['cursor']) })
                  task.read_cursor.value(d['cursor'])
                               
                task.read_cursor.value(task.read_cursor.value() + 1)
                task.update()
                self.release_tasks()
                
                if len(data) < task.block_size.value():
                  finished = True
              else:
                finished = True
              
              if finished:
                #no more data
                if task.status.value() == 'Stacking':
                  task.status.value('All data stacked')
                  task.update()
            else:
              task.status.value('Unable to connect to data source')
              task.time_ended.value(int(round(time.time() * 1000)))
              task.update()
          else:
            task.status.value('Invalid dataset provided')
            task.time_ended.value(int(round(time.time() * 1000)))
            task.update()
      try:
        return self.stack.popleft()
      except:
        return None      

    def receive_result(self, cursor=None, result=None):
     if cursor == None or cursor == '' or result == None or result == '':
      return False
      
     #lets see if we can find the dataset for this
     tmp = cursor.split('-')
     taskId = tmp[0]
     datasetId = tmp[1]
     cursorId = tmp[2]
     
     #get our task
     task = None
     if taskId not in self._tasks:
       task = api.db.Task.find({ 'id' : taskId })
       if task != None:
        self._tasks[str(task.id.value())] = task
      
     if taskId not in self._tasks:
       #a serious issue
       return False
     else:
       task = self._tasks[taskId]

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
       
       #record this cursorId locally
       if task.id.value() not in self._taskResultCursors:       
         #we record a blockmap, the target blockmap size and the started time so we can re-stack any missing blocks
         self._taskResultCursors[task.id.value()] = {
           'size' : task.block_size.value(),
           'block_map' : {},
         }
       
       #we calculate the block number from the cursor ID divided by the target block size
       block = (int(cursorId) - 1) / self._taskResultCursors[task.id.value()]['size'] #corrected as we start at zero folks :)
       logger.LOG.debug("Cursor %s is in block %s" % (cursorId, block))
       
       #if the block is not within the blockmap then we need to create the value
       if block not in self._taskResultCursors[task.id.value()]['block_map']:
         self._taskResultCursors[task.id.value()]['block_map'][block] = { 'completed' : 0, 'started' : time.time() }
       
       #record a completed task within the blockmap
       #when we reach a blockmap size for the completed value, the block is finished
       self._taskResultCursors[task.id.value()]['block_map'][block]['completed'] += 1
       
       max = 0
       maxBlock = -1
       #now check every block map and update the completion cursor as required
       for k, v in self._taskResultCursors[task.id.value()]['block_map'].iteritems():
         #determine the maxblock we have seen so far
         if k > maxBlock:
           maxBlock = k
          
         #if the number of completed items equals the blockmaps size         
         if v['completed'] == self._taskResultCursors[task.id.value()]['size'] and k == maxBlock:
           #we advance the cursor
           completedTo = (k + 1) * v['completed']
           logger.LOG.debug("We have completed %s so far" % completedTo)
       
           #and if the cursor is greater than our max we increase it
           if completedTo > max:
            max = completedTo

       logger.LOG.debug(self._taskResultCursors[task.id.value()]['block_map'])
       #we save our completion cursor for the task
       task.completion_cursor.value(max)
       #and calculate the % if applicable

       #special case when all data is stacked on the last block     
       if task.status.value() == 'All data stacked':       
         logger.LOG.debug("Checking last target of %s against %s" % ((task.read_cursor.value() - 1), self._taskResultCursors[task.id.value()]['block_map'][block]['completed']))
         if (task.read_cursor.value() - 1) == (self._taskResultCursors[task.id.value()]['block_map'][block]['completed'] + (block * self._taskResultCursors[task.id.value()]['size'])):
           #we set the completion cursor for the task
           task.completion_cursor.value(task.read_cursor.value() - 1)
           #reset the max
           max = task.read_cursor.value() - 1
         
         #and is it finished?
         if max == (task.read_cursor.value() - 1):
           #our task is completed
           task.status.value('Complete')
           task.read_cursor.value(task.completion_cursor.value())
           task.time_ended.value(int(round(time.time() * 1000)))      
           self.refreshTasks()

       logger.LOG.debug("Setting task progress to %.2f%%" % (float(100) / float((task.read_cursor.value() - 1)) * float(task.completion_cursor.value())))
       task.progress.value('%.2f%%' % (float(100) / float(task.read_cursor.value() - 1) * float(task.completion_cursor.value())))                

       task.update()       
     else:
       task.status('Unable to save result to remote data source')
       task.time_ended(int(round(time.time() * 1000)))
       task.update()
       return False     
     
     return True
