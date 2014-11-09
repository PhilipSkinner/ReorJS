"""
	configure.py
	Automated config generator for ReorJS packages

	--
	Scans the system to ensure all requirements are met for installing
	the ReorJS CLI package
	--

	Author(s)       - Philip Skinner (philip@crowdca.lc)
	Last modified   - 2014-10-24

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
	print("This tool will now proceed to read your systems configuration and generate the relevant installation scripts.\n")

	#check we are running as sudo
	question('Running with correct permissions')
	answer('Yes', 'No', checkPermissions())

	configuration = {
		'cli' : {
			'home' : '',
			'proceed' : False,
			'issues' : [],
		},
		'documentation' : {
			'home' : '',
			'proceed' : True,
		},
	}

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

	header('Checking default locations')

	question('Checking install directory')
	if answer('/usr/local', 'Not found', checkDir('/usr/local')):
		#set our install directories
		configuration['cli']['home'] = '/usr/local/reorjs/cli'
		configuration['documentation']['home'] = '/usr/local/reorjs/docs'
	else:
		configuration['cli']['proceed'] = False
		configuration['cli']['issues'].append('Could not establish default installation location')

	header('Final configuration')
	print("Installation will be configured as follows:\n")

	warning('\nReorJS CLI\n')
	report('Will install', ('Yes' if configuration['cli']['proceed'] else 'No'))
	if configuration['cli']['proceed']:
		report('Installation directory', configuration['cli']['home'])
	else:
		print("\nInstallation will not proceed due to these issues:")
		if len(configuration['cli']['issues']) == 0:
			bad('Unknown issues')
		else:
			for i in configuration['cli']['issues']:
				bad(i)

	warning('\nReorJS Documentation\n')
	report('Will install', 'Yes')
	report('Installation directory', configuration['documentation']['home'])

	yes_no = None
	while yes_no != 'N' and yes_no != 'Y':
		yes_no = input('Continue and create installation scripts? (Y,N) ').upper()

	if yes_no == 'Y':
		if configuration['cli']['proceed']:
			print("Writing CLI installation script...")
			f = open('cli.sh', 'w')
			f.write('python installer.py CLI "%s"\n' % configuration['cli']['home'])
			f.write('python cli.config.py "%s"\n' % configuration['cli']['home'])
			f.close()

		if configuration['documentation']['proceed']:
			print("Writing documentation installation script...")
			f = open('docs.sh', 'w')
			f.write('python installer.py docs "%s"\n' % configuration['documentation']['home'])
			f.close()

		print("Writing installation script")
		f = open('install.sh', 'w')
		if configuration['cli']['proceed']:
			f.write('sh cli.sh\n')
		if configuration['documentation']['proceed']:
			f.write('sh docs.sh\n')
		f.close()

		good('\nInstallation scripts created, run "sh install.sh" to complete installation\n')
	else:
		warning("Quitting configuration")

	info('Bye!')

def clean():
	header('Welcome to the ReorJS Configuration Tool')
	print("We are now performing a clean of any auto-generated install scripts.\n")

	files = ['reorjsd.sh', 'cli.sh', 'node.sh', 'install.sh']

	for f in files:
		question('Removing %s' % f)
		os.system('rm -rf %s' % f)
		good('Removed')

	print("\nAll clean, just run 'python configure.py' again to generate your install scripts")

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
