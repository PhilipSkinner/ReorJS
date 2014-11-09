"""
	reorjs.config.py
	Setup script for reorjsd conf files

	--
	Copies over the example config files and then builds the default conf
	file depending upon the configuration values generated by configure.py.
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

import sys
import os
import string
import random

base = sys.argv[1]
conf = sys.argv[2]
log = sys.argv[3]
http = sys.argv[4]
db = sys.argv[5]

print("Ensuring config destination...")
#ensure our destination
parts = conf.split('/')
path = ''
for p in parts:
	if p != '':
		path = '%s/%s' % (path, p)
		if not os.path.isdir(path):
			#we need to make it
			print("Making directory %s" % path)
			os.makedirs(path)

print("Copying over example configuration files...")
os.system('cp -rf %s/examples/* %s' % (base, conf))

print("Generating default conf")
f = open('%s/reorjsd.conf' % conf, 'w')
f.write('[Defaults]')
f.write('port=9999\n')
f.write('ip=127.0.0.1\n')
f.write('db-type=%s\n' % db)
if db == 'mysql':
	f.write('mysql-host=localhost\n')
	f.write('mysql-port=3306\n')
	f.write('mysql-name=reorjs\n')
	f.write('mysql-user=username\n')
	f.write('mysql-password=password\n')
elif db == 'mongo':
	f.write('mongo-host=localhost\n')
	f.write('mongo-port=27017\n')
f.write('server=%s\n' % http)
f.write('root-key=%s' % ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(24)))
f.close()

print("Generating system startup script")
r = open('reorjsd', 'r')
n = open('/etc/init.d/reorjsd', 'w')
for line in r.readlines():
	#strip it for sanity
	line = line.replace('\n', '').replace('\r', '')
	if line == "dir=''":
		n.write("dir='%s'\n" % base)
	else:
		n.write("%s\n" % line)

r.close()
n.close()

print("Setting permissions")
os.system('chmod 755 /etc/init.d/reorjsd')

print("Registering service")
os.system('chkconfig --add reorjsd')

print("Configuration setup and examples in place")
