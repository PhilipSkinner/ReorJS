"""
        cli.config.py
        Setup script for CLI scripts
        
        --
        Generates a custom cli startup script and puts it into the /usr/local/bin
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

base = sys.argv[1]

print "Generating cli startup script"
r = open('reorjs-cli', 'r')
n = open('/usr/local/bin/reorjs-cli', 'w')
for line in r.readlines():  
  #strip it for sanity
  line = line.replace('\n', '').replace('\r', '')
  if line == "dir=''":
    n.write("dir='%s'\n" % base)
  else:
    n.write("%s\n" % line)
    
r.close()
n.close()

print "Setting permissions"
os.system('chmod 755 /usr/local/bin/reorjs-cli')

print "CLI startup script configured"
