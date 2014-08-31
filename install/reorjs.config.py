import sys
import os

base = sys.argv[1]
conf = sys.argv[2]
log = sys.argv[3]
http = sys.argv[4]
db = sys.argv[5]

print "Ensuring config destination..."
#ensure our destination
parts = conf.split('/')
path = ''
for p in parts:
  if p != '':
    path = '%s/%s' % (path, p)
    if not os.path.isdir(path):
      #we need to make it
      print "Making directory %s" % path
      os.makedirs(path)

print "Copying over example configuration files..."
os.system('cp -rf %s/examples/* %s' % (base, conf))

print "Generating default conf"
f = open('%s/reorjsd.conf' % conf, 'w')
f.write('--port = 9999\n')
f.write('--ip = 127.0.0.1\n')
f.write('--db-type = %s\n' % db)
if db == 'mysql':
  f.write('--mysql-host = localhost\n')
  f.write('--mysql-port = 3306\n')
  f.write('--mysql-name = reorjs\n')
  f.write('--mysql-user = username\n')
  f.write('--mysql-password = password\n')
elif db == 'mongo':
  f.write('--mongo-host = localhost\n')
  f.write('--mongo-port = 27017\n')
f.write('--server = %s\n' % http)
f.close()

print "Generating system startup script"
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

print "Registering service"
os.system('chkconfig --add reorjsd')

print "Configuration setup and examples in place"
