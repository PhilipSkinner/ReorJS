"""
	installer.py
	Simple script to copy one directory to another.

	--
	Takes two arguments, the source directory and the destination.

	Ensures the destination exists and then copies the source over to it,
	overwriting anything that existed in the destination.
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

source = sys.argv[1]
destination = sys.argv[2]

print("Ensuring install destination...")
#ensure our destination
parts = destination.split('/')
path = ''
for p in parts:
	if p != '':
		path = '%s/%s' % (path, p)
		if not os.path.isdir(path):
			#we need to make it
			print("Making directory %s" % path)
			os.makedirs(path)

#now copy our package over
print("Copying package contents over")
os.system('cp -rf %s/* %s/' % (source, destination))

#debug - setting permissions, I messed them up in the repo
#os.system('chmod -R 777 %s' % (destination))

print("Installation complete")
