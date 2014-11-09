"""
	remote/memcached.py
	ReorJSd Remote Memcached Connector

	--
	Provides a remote connection to an external Memcached service.
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

from . import base
import logger

class MemcachedRemote(base.RemoteConnection):
	def connect(self):
		if self.host == None:
			logger.LOG.log("Hostname not given, defaulting to localhost")
			self.host = 'localhost'

		if self.name == None:
			logger.LOG.log("Database name not given, cannot proceed")
			return False

		if self.table == None:
			logger.LOG.log("No table given, cannot proceed")
			return False


		return self.connection != None

	def readColumns(self):
		self.columns = [1]

	def query(self, rows=None):
		if rows == None:
			logger.LOG.log("Defaulting to 1000 rows")
			rows = 1000

		toReturn = []

		return toReturn
