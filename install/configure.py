"""
        configure.py
        Automated config generator for ReorJS packages
        
        --
        Scans the system to ensure all requirements are met for installing
        the ReorJS server, ReorJS CLI and ReorJS Node packages.                
        --
        
        Author(s)       - Philip Skinner (philip@crowdca.lc)
        Last modified   - 2014-08-31
        
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

import os
import sys

def configure():
  header('Welcome to the ReorJS Configuration Tool')
  print "This tool will now proceed to read your systems configuration and generate the relevant installation scripts.\n"

  #check we are running as sudo
  question('Running with correct permissions')
  answer('Yes', 'No', checkPermissions())
  
  configuration = {
    'reorjs' : {
      'home' : '',
      'logs' : '',
      'config' : '',
      'http' : '',
      'db' : '',
      'tornado' : False,
      'fapws' : False,
      'mysql' : False,
      'mongo' : False,
      'proceed' : False,
      'issues' : [],
    },
    'cli' : {
      'home' : '',
      'proceed' : False,
      'issues' : [],      
    },
    'node' : {
      'home' : '',
      'proceed' : False,
      'issues' : [],
    },
  }
  
  header('ReorJS Daemon Requirements')
  #gather package information
  exists = requiredPackages([
    {
      'name' : 'ArgParse',
      'libname' : 'argparse',
    },
    {
      'name' : 'socket',
      'libname' : 'socket',
    },
    {
      'name' : 'MySQL',
      'libname' : 'MySQLdb',
    },
    {
      'name' : 'Mongo',
      'libname' : 'pymongo',
    },
    {
      'name' : 'bson',
      'libname' : 'bson',
    },
    {
      'name' : 'copy',
      'libname' : 'copy',      
    },
    {
      'name' : 're',
      'libname' : 're',
    },
    {
      'name' : 'Tornado',
      'libname' : 'tornado',
    },
    {
      'name' : 'fapws',
      'libname' : 'fapws',
    },
    {
      'name' : 'simplejson',
      'libname' : 'simplejson',
    },
    {
      'name' : 'collections',
      'libname' : 'collections',
    },
    {
      'name' : 'random',
      'libname' : 'random',
    },
    {
      'name' : 'operator',
      'libname' : 'operator',
    },
    {
      'name' : 'getpass',
      'libname' : 'getpass',
    },
    {
      'name' : 'redis',
      'libname' : 'redis',
    },
  ]) 
  
  #now ensure we have everything we need and atleast one of the optional group packages
  configuration['reorjs']['proceed'] = True
  if 'tornado' not in exists and 'fapws' not in exists:
    configuration['reorjs']['proceed'] = False
    configuration['reorjs']['issues'].append('Missing either tornado or fapws requirements')
  else:
    configuration['reorjs']['tornado'] = True
    configuration['reorjs']['fapws'] = True
  
  if 'MySQLdb' not in exists and ('pymongo' not in exists or 'bson' not in exists):
    configuration['reorjs']['proceed'] = False
    configuration['reorjs']['issues'].append('Missing either MySQLdb or pymongo and bson requirements')
  else:
    configuration['reorjs']['mongo'] = True
    configuration['reorjs']['mysql'] = True  
    
  all = ['getpass', 'random', 'operator', 'collections', 'simplejson', 're', 'copy', 'socket', 'argparse']
  for a in all:
    if a not in exists:
      configuration['reorjs']['issues'].append('Missing requirement %s' % a)
      configuration['reorjs']['proceed'] = False
  
  header('ReorJS CLI Requirements')
  exists = requiredPackages([
    {
      'name' : 'cmd',
      'libname' : 'cmd',      
    },
    {
      'name' : 'shlex',
      'libname' : 'shlex',
    },
    {
      'name' : 'PrettyTable',
      'libname' : 'prettytable',
    },
    {
      'name' : 'urllib',
      'libname' : 'urllib',
    },
    {
      'name' : 'urllib2',
      'libname' : 'urllib2',
    },
    {
      'name' : 'httplib2',
      'libname' : 'httplib2',
    },
    {
      'name' : 'simplejson',
      'libname' : 'simplejson',
    },
  ])

  configuration['cli']['proceed'] = True
  all = ['cmd', 'shlex', 'prettytable', 'urllib', 'urllib2', 'httplib2', 'simplejson']
  for a in all:
    if a not in exists:
      configuration['cli']['issues'].append('Missing requirement %s' % a)
      configuration['cli']['proceed'] = False
  
  header('ReorJS Node Client Requirements')
  warning('No requirements needed')
  configuration['node']['proceed'] = True
  
  header('Checking default locations')
  question('Checking conf directory')
  if answer('/etc', 'Not found', checkDir('/etc')):
    #set our config directory values
    configuration['reorjs']['config'] = '/etc/reorjs'
  else:
    #no conf directory found
    configuration['reorjs']['proceed'] = False
    configuration['reorjs']['issues'].append('Could not establish default configuration file location')
    
  question('Checking install directory')
  if answer('/usr/local', 'Not found', checkDir('/usr/local')):
    #set our install directories
    configuration['reorjs']['home'] = '/usr/local/reorjs/reorjsd'
    configuration['cli']['home'] = '/usr/local/reorjs/cli'
    configuration['node']['home'] = '/usr/local/reorjs/nodes'
  else:
    configuration['reorjs']['proceed'] = False
    configuration['reorjs']['issues'].append('Could not establish default installation location')

    configuration['cli']['proceed'] = False
    configuration['cli']['issues'].append('Could not establish default installation location')

    configuration['node']['proceed'] = False
    configuration['node']['issues'].append('Could not establish default installation location')      
  
  question('Checking log directory')
  if answer('/var/log', 'Not found', checkDir('/var/log')):
    configuration['reorjs']['logs'] = '/var/log/reorjs'
  else:
    configuration['reorjs']['proceed'] = False
    configuration['reorjs']['issues'].append('Could not establish default logging location')
  
  header('Final configuration')
  print "Installation will be configured as follows:\n"
  
  warning('ReorJS Server\n')
  report('Will install', ('Yes' if configuration['reorjs']['proceed'] else 'No'))
  if configuration['reorjs']['proceed']:
    report('Installation directory', configuration['reorjs']['home'])
    report('Config directory', configuration['reorjs']['config'])
    report('Logs directory', configuration['reorjs']['logs'])
    report('Default HTTP server', ('Tornado' if configuration['reorjs']['tornado'] else 'fapws'))
    configuration['reorjs']['http'] = 'tornado' if configuration['reorjs']['tornado'] else 'fapws'
    supported = []
    if configuration['reorjs']['tornado']:
      supported.append('Tornado')
    if configuration['reorjs']['fapws']:
      supported.append('fapws')
    report('Supported HTTP servers', ", ".join(supported))
    report('Default API DB', ('MongoDB' if configuration['reorjs']['mongo'] else 'MySQL'))
    configuration['reorjs']['db'] = 'mongo' if configuration['reorjs']['mongo'] else 'mysql'
    supported = []
    if configuration['reorjs']['mongo']:
      supported.append('MongoDB')
    if configuration['reorjs']['mysql']:
      supported.append('MySQL')
    report('Supported DB servers', ", ".join(supported))    
  else:
    print "\nInstallation will not proceed due to these issues:"  
    if len(configuration['reorjs']['issues']) == 0:
      bad('Unknown issues')
    else:
      for i in configuration['reorjs']['issues']:
        bad(i)
  
  warning('\nReorJS CLI\n')
  report('Will install', ('Yes' if configuration['cli']['proceed'] else 'No'))
  if configuration['cli']['proceed']:  
    report('Installation directory', configuration['cli']['home'])
  else:
    print "\nInstallation will not proceed due to these issues:"
    if len(configuration['cli']['issues']) == 0:
      bad('Unknown issues')
    else:
      for i in configuration['cli']['issues']:
        bad(i)
  
  warning('\nReorJS Node Client\n')
  report('Will install', ('Yes' if configuration['node']['proceed'] else 'No'))
  if configuration['node']['proceed']:
    report('Installation directory', configuration['node']['home'])
  else:
    print "\nInstallation will not proceed due to these issues:"
    if len(configuration['node']['issues']) == 0:
      bad('Unknown issues')
    else:
      for i in configuration['node']['issues']:
        bad(i)
  
  yes_no = None
  while yes_no != 'N' and yes_no != 'Y':
    yes_no = raw_input('Continue and create installation scripts? (Y,N) ').upper()
  
  if yes_no == 'Y':
    if configuration['reorjs']['proceed']:
      print "Writing ReorJS Server installation script..."    
      f = open('reorjsd.sh', 'w')
      f.write('python installer.py ReorJS "%s"\n' % configuration['reorjs']['home'])
      f.write('python reorjs.config.py "%s" "%s" "%s" "%s" "%s"\n' % (configuration['reorjs']['home'], configuration['reorjs']['config'], configuration['reorjs']['logs'], configuration['reorjs']['http'], configuration['reorjs']['db']))
      f.close()
    
    if configuration['cli']['proceed']:
      print "Writing CLI installation script..."
      f = open('cli.sh', 'w')
      f.write('python installer.py CLI "%s"\n' % configuration['cli']['home'])
      f.close()    
  
    if configuration['node']['proceed']:  
      print "Writing node client installation script..."
      f = open('node.sh', 'w')
      f.write('python installer.py node "%s"\n' % configuration['node']['home'])
      f.close()
    
    print "Writing installation script"
    f = open('install.sh', 'w')
    if configuration['reorjs']['proceed']:
      f.write('sh reorjsd.sh\n')
    if configuration['cli']['proceed']:
      f.write('sh cli.sh\n')
    if configuration['node']['proceed']:
      f.write('sh node.sh\n')
    f.close()
    
    good('\nInstallation scripts created, run "sh install.sh" to complete installation\n')
  else:
    warning("Quitting configuration")

  info('Bye!')

def clean():
  header('Welcome to the ReorJS Configuration Tool')
  print "We are now performing a clean of any auto-generated install scripts.\n"

  files = ['reorjsd.sh', 'cli.sh', 'node.sh', 'install.sh']

  for f in files:    
    question('Removing %s' % f)
    os.system('rm -rf %s' % f)
    good('Removed')
    
  print "\nAll clean, just run 'python configure.py' again to generate your install scripts"

# helpers

class bcolors:
  HEADER = '\033[95m'
  OKBLUE = '\033[94m'
  OKGREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'

def checkDir(dir):
  return os.path.isdir(dir)

def requiredPackages(packages):
  exists = []
  for p in packages:  
    question('Checking for %s' % p['name'])
    if answer('Yes', 'No', checkPackage(p['libname'])):
      exists.append(p['libname'])
    
  return exists

def report(name, val):
  question(name)
  warning(val)

def question(text):
  maxLen = 60 - len(text) - 2
  numTabs = 0
  tabLength = 8
  
  #whatever
  while maxLen > tabLength:
    numTabs += 1
    maxLen -= tabLength
  
  if maxLen > (tabLength / 2):
    numTabs += 1
  
  sys.stdout.write('%s: %s' % (text, "\t" * numTabs))

def answer(yes, no, check):
  if check:
    good(yes)
    return True
  else:
    bad(no)
    return False

def good(text):
  sys.stdout.write('%s%s%s\n' % (bcolors.OKGREEN, text, bcolors.ENDC))

def info(text):
  sys.stdout.write('%s%s%s\n' % (bcolors.OKBLUE, text, bcolors.ENDC))
  
def bad(text):
  sys.stdout.write('%s%s%s\n' % (bcolors.FAIL, text, bcolors.ENDC))

def warning(text):
  sys.stdout.write('%s%s%s\n' % (bcolors.WARNING, text, bcolors.ENDC))

def header(text):
  sys.stdout.write('\n%s%s%s\n%s\n\n' % (bcolors.HEADER, text, bcolors.ENDC, '=' * len(text)))

def checkPermissions():
  return os.getuid() == 0

def checkPackage(name, version=None):
  try:
    package = __import__(name)
    
    if version:
      myV = None
      try:
        myV = package.__version__
      except:
        pass
      
      if myV == None:
        try:
          myV = package.version
        except:
          pass
      
      if myV == None:
        try:
          myV = package.VERSION
        except:
          pass
      
      if myV != None and myV != version:
        return False
    
    return True
  except ImportError:
    return False

if len(sys.argv) == 2:
  if sys.argv[1] == 'clean':
    clean()
    sys.exit(0)

configure()
