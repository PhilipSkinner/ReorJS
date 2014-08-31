import sys
import os

source = sys.argv[1]
destination = sys.argv[2]

print "Ensuring install destination..."
#ensure our destination
parts = destination.split('/')
path = ''
for p in parts:
  if p != '':  
    path = '%s/%s' % (path, p)
    if not os.path.isdir(path):
      #we need to make it
      print "Making directory %s" % path
      os.makedirs(path)

#now copy our package over
print "Copying package contents over"
os.system('cp -rf %s/* %s/' % (source, destination))

#debug - setting permissions, I messed them up in the repo
#os.system('chmod -R 777 %s' % (destination))

print "Installation complete"
