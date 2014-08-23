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
  intro = bcolors.OKBLUE + 'Welcome to ReorJS!' + bcolors.ENDC + '\n\nTo initialize session please connect to reorjsd (see help connect)\n'
  
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
      self.api.createTask()
    elif details[0] == 'delete':
      self.api.deleteTask()
      
    return self.help_task()
    
  def help_task(self, task=None):
    self.bad("Usage: task ")
  
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
      self.api.createDataset()
    elif details[0] == 'modify':
      self.api.modifyDataset()
    elif details[0] == 'delete':
      self.api.deleteDataset()
    
    return self.help_dataset()
    
  def help_dataset(self, task=None):
    self.bad('Usage: dataset ')
  
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
      self.api.createApplication()
      return
    elif details[0] == 'modify':
      self.api.modifyApplication()
      return
    elif details[0] == 'delete':
      self.api.deleteApplication()
      return
    
    return self.help_application(task=task)
  
  def help_application(self, task=None):
    self.bad("Application help")
  
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
  
  def normal(self, line):
    print line
  
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
