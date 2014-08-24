import cmd
import shlex
import api
from prettytable import PrettyTable

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

class ReorJSCLI(cmd.Cmd):
  """ReorJS Client"""
  api = api.API()
  
  prompt = bcolors.HEADER + '[reorjs]: ' + bcolors.ENDC
  intro = bcolors.OKBLUE + '\nWelcome to ReorJS!' + bcolors.ENDC + '\n\nTo initialize session please connect to reorjsd (see help connect)\n'
  
  ##
  # connect: allows user to specify API details for client
  ##
  
  def do_connect(self, details):
    if details == None or details == '':
      return self.help_connect()
    
    details = shlex.split(details)
    
    if details[0] == 'test':
      if self.api.connectionTest():
        self.good("API server responded correctly!")
      else:
        self.error("ERROR: Could not connect to the API server")
    else:   
      if len(details) == 1:
        return self.help_connect()        
       
      self.api.setHost(details[0])
      self.api.setKey(details[1])

      print "API configured. To test connection type connect test."
  
  def help_connect(self):
    self.bad("Usage: connect http://[host]:[port] [apikey]")
  
  ##
  # connect: end
  ##
  
  ##
  # task: allows user to manipulate tasks through the api
  ##
  
  def do_task(self, task):
    if task == None or task == '':
      return self.help_task()

    details = shlex.split(task)

    if details[0] == 'list':
      tasks = self.api.listTasks()
      
      self.doTable(tasks)
      
      return
    elif details[0] == 'detail':
      if len(details) == 1:
        return self.help_task(task=details[0])
  
      task = self.api.detailTask(id=details[1])  
      
      self.doRecord(task)      
      
      return
    elif details[0] == 'create':
      if len(details) < 3:
        return self.help_task(task=details[0])
      
      application = details[1]
      dataset = details[2]
      
      status = self.api.createTask(application=application, dataset=dataset)      
      self.doStatus(status)
      
      return
    elif details[0] == 'help' and len(details) == 2:
      return self.help_task(task=details[0], specific=details[1])
      
    return self.help_task()
    
  def help_task(self, task=None, specific=None, name=None):
    if specific == None:
      specific = task
      task = 'help'
    
    if task == 'help':
      if specific == 'list':
        self.bad('Usage: task list')
        self.normal('Lists all of the current tasks')
        return
      elif specific == 'detail':
        self.bad('Usage: task detail [id]')
        self.normal('Shows the specifics for task [i]')
        return
      elif specific == 'create':
        self.bad('Usage: task create [application id] [dataset id]')
        self.normal('Creates a task by combining application [application id] and dataset [dataset id]')
        return

    #if we got this far we need to show the default
    self.header('\nTasks')
    self.header('------------')
    self.normal('Tasks map an application to a set of data and starts the computation on the connected ReorJS Javascript clients.\n')
    self.bad('Usage: task [command] [options...]')    
    self.info('Commands: list detail create\n')
    self.normal('See task help [command] for more information\n')
    return
  
  ##
  # task: end
  ##
  
  ##
  # dataset: allows user to manipulate datasets through the api
  ##  
  
  def do_dataset(self, task):
    if task == None or task == '':
      return self.help_dataset()
    
    details = shlex.split(task)
    
    if details[0] == 'list':
      datasets = self.api.listDatasets()

      self.doTable(datasets)
      
      return    
    elif details[0] == 'detail':
      if len(details) == 1:
        return self.help_dataset(task=details[0])
  
      dataset = self.api.detailDataset(id=details[1])  
      
      self.doRecord(dataset)      
      
      return
    elif details[0] == 'create':
      #we need a minimum of 2 values
      if len(details) < 3:
        return self.help_dataset(task=details[0])
      
      #fill up the other entries
      while len(details) < 9:
        details.append(None)
                
      name 		= details[1]
      source_type 	= str(details[2]).lower()
      source_hostname 	= details[3]
      source_port 	= details[4]
      source_name 	= details[5]
      source_table 	= details[6]
      source_username 	= details[7]
      source_password 	= details[8]
    
      #check our type to be a supported type
      if source_type not in ['mysql', 'redis', 'mongo', 'hadoop', 'memcached', 'local']:
        return self.help_dataset(task=details[0], specific='type', name=source_type)
    
      status = self.api.createDataset(name		= name,
                                      source_type 	= source_type,
                                      source_hostname 	= source_hostname,
                                      source_port 	= source_port,
                                      source_name 	= source_name,
                                      source_table 	= source_table,
                                      source_username 	= source_username,
                                      source_password 	= source_password)
      self.doStatus(status)
      return      
    elif details[0] == 'modify':
      #need atleast id, name and type
      if len(details) < 4:
        return self.help_dataset(task=details[0])

      #fill up the other entries
      while len(details) < 10:
        details.append(None)
        
      id 		= details[1]
      name		= details[2]
      source_type	= details[3]
      source_hostname	= details[4]
      source_port	= details[5]
      source_name	= details[6]
      source_table	= details[7]
      source_username	= details[8]
      source_password	= details[9]
      
      #check our type to be a supported type
      if source_type not in ['mysql', 'redis', 'mongo', 'hadoop', 'memcached', 'local']:
        return self.help_dataset(task=details[0], specific='type', name=source_type)
      
      status = self.api.modifyDataset(id		= id,
                                      name		= name,
                                      source_type	= source_type,
                                      source_hostname	= source_hostname,
                                      source_port	= source_port,
                                      source_name	= source_name,
                                      source_table	= source_table,
                                      source_username	= source_username,
                                      source_password	= source_password)
      self.doStatus(status)
      return
    elif details[0] == 'delete':
      if len(details) < 2:
        return self.help_dataset(task=details[0])

      status = self.api.deleteDataset(id=details[1])
      self.doStatus(status)
            
      return
    elif details[0] == 'help' and len(details) == 2:
      return self.help_dataset(task=details[0], specific=details[1])
    
    return self.help_dataset()
    
  def help_dataset(self, task=None, specific=None, name=None):
    if specific == None:
      specific = task
      task = 'help'
    
    if task == 'help':
      if specific == 'list':
        self.bad('Usage: dataset list')
        self.normal('List all datasets currently available')      
        return
      elif specific == 'detail':
        self.bad('Usage: dataset detail [id]')
        self.normal('Shows the specific details for the dataset referenced by id [id]')
        return
      elif specific == 'create':
        self.bad('Usage: dataset create [name] [type] *hostname* *port* *dbname* *tablename* *username* *password*')
        self.normal('Creates a dataset of [type] using the given options. Please make sure to pass all options that are required for your dataset. Skip any unrequired options by entering a single 1')
        return
      elif specific == 'modify':
        self.bad('Usage: dataset modify [id] [name] [type] *hostname* *port* *dbname* *tablename* *username* *password*')
        self.normal('Modifies the dataset referenced by [id] using the given options. Please make sure to pass all options that are required for your dataset. Skip any unrequired options by entering a single 1')
        return
      elif specific == 'delete':
        self.bad('Usage: dataset delete [id]')
        self.normal('Removes the dataset [id]')
        return

    #if we got this far we need to show the default
    self.header('\nDatasets')
    self.header('------------')
    self.normal('Datasets are sources of information. Currently supported sources are mysql, mongo, redis, memcached, hadoop and the local API\n')
    self.bad('Usage: dataset [command] [options...]')    
    self.info('Commands: list detail create modify delete\n')
    self.normal('See dataset help [command] for more information\n')
    return
  
  ##
  # dataset: end
  ##
  
  ##
  # application: allows user to manipulate applications through the api
  ##
  
  def do_application(self, task):
    if task == None or task == '':
      return self.help_application()

    details = shlex.split(task)
    
    if details[0] == 'list':
      applications = self.api.listApplications()
      
      self.doTable(applications)
      
      return
    elif details[0] == 'detail':
      if len(details) == 1:
        return self.help_application(task=details[0])
    
      application = self.api.detailApplication(id=details[1])

      self.doRecord(application)      
      
      return
    elif details[0] == 'create':
      if len(details) < 3:
        return self.help_application(task=details[0])
      
      name 	= details[1]
      program 	= details[2]
      
      status = self.api.createApplication(name = name, program = program)
      self.doStatus(status)
      return
    elif details[0] == 'modify':
      if len(details) < 4:
        return self.help_application(task=details[0])
      
      id 	= details[1]
      name	= details[2]
      program	= details[3]
      
      status = self.api.modifyApplication(id = id, name = name, program = program)
      self.doStatus(status)
      return
    elif details[0] == 'delete':
      if len(details) < 2:
        return self.help_application(task=details[0])
      
      status = self.api.deleteApplication(id=details[1])
      self.doStatus(status)
      return
    elif details[0] == 'help' and len(details) == 2:
      return self.help_application(task=details[0], specific=details[1])
    
    return self.help_application(task=task)
  
  def help_application(self, task=None, specific=None, name=None):
    #convert stuff
    if specific == None:
      specific = task
      task = 'help'
      
    if task == 'help':
      if specific == 'list':
        self.bad('Usage: application list')
        self.normal('List all applications currently available')
        return
      elif specific == 'detail':
        self.bad('Usage: application detail [application id]')
        self.normal('Shows the specific details for an application by id')
        return
      elif specific == 'create':
        self.bad('Usage: application create [name] [program]')
        self.normal('Creates an application named [name] with the Javascript program [program]')
        return
      elif specific == 'modify':
        self.bad('Usage: application modify [id] [name] [program]')
        self.normal('Updates the application referenced by [id] to have name [name] and Javascript program [program]')
        return
      elif specific == 'delete':
        self.bad('Usage: application delete [id]')
        self.normal('Removes application [id]')
        return

    #if we got this far we need to show the default
    self.header('\nApplications')
    self.header('------------')
    self.normal('Applications are javascript functions that can be run against data within the system.\n')
    self.bad('Usage: application [command] [options...]')    
    self.info('Commands: list detail create modify delete\n')
    self.normal('See application help [command] for more information\n')
    return
      
  ##
  # application: end
  ##
  
  def do_quit(self, line):
    return self.do_EOF(line)
    
  def do_EOF(self, line):
    self.info('Bye!')
    return True
  
  ##
  # print functions
  ##

  def doRecord(self, hash):
    for k, v in hash.iteritems():
      print bcolors.HEADER + k + bcolors.ENDC + '\t\t: ' + str(v)
  
  def doTable(self, hash):
    table = None
      
    for rec in hash:
      if table == None:
        cols = rec.keys()
        cols = [bcolors.HEADER + c + bcolors.ENDC for c in cols]
        table = PrettyTable(cols)

      table.add_row(rec.values())
      
    print table    
    
  def doStatus(self, status):
    code = '9999'
    
    if status != None:
      if 'code' in status:
        code = status['code']      
      
      if 'meta' in status:
        if 'code' in status['meta']:
          code = status['meta']['code']
  
      if 'error' in status:
        if 'message' in status['error']:
          self.error('%s : %s' % (code, status['error']['message']))
          return
      
      if 'status' in status:
        if 'message' in status['status']:
          self.good('%s : %s' % (code, status['status']['message']))
          return
    
    self.error('%s : An unknown error occured' % code)
    return
  
  def normal(self, line):
    print line
  
  def header(self, line):
    print bcolors.HEADER + line + bcolors.ENDC
  
  def bad(self, line):
    print bcolors.WARNING + line + bcolors.ENDC
  
  def error(self, line):
    print bcolors.FAIL + line + bcolors.ENDC
  
  def good(self, line):
    print bcolors.OKGREEN + line + bcolors.ENDC
  
  def info(self, line):
    print bcolors.OKBLUE + line + bcolors.ENDC

if __name__ == '__main__':  
  ReorJSCLI().cmdloop()
