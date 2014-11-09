"""
	remote/redis.py
	ReorJSd Remote Redis Connector

	--
	Provides a remote connection to a Redis service.
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
import redis
import logger

class RedisRemote(base.RemoteConnection):
	def connect(self):
		if self.hostname == None:
			logger.LOG.log("Hostname not given, defaulting to localhost")
			self.hostname = 'localhost'

		if self.port == None:
			logger.LOG.log("Port not given, defaulting to 6379")
			self.port = 6379

		if self.name == None:
			logger.LOG.log("Database name not given, cannot proceed")
			return False

		if self.table == None:
			logger.LOG.log("No table given, cannot proceed")
			return False

		self.connection = redis.Redis(host=self.hostname, port=int(self.port))

		return self.connection != None

	def noEncode(self):
		return True

	def readColumns(self):
		#not needed
		self.columns = [1]

	def query(self, rows=None):
		if rows == None:
			logger.LOG.log("Defaulting to 1000 rows")
			rows = 1000

		results = []
		toReturn = []

		#gotta love redis
		try:
			results = self.connection.lrange(self.table, (self.cursor - 1), (self.cursor + rows - 1))
		except:
			logger.LOG.log("Issue fetching data from redis")

		#setup the cursors
		for d in results:
			toReturn.append({ 'data' : d, 'cursor' : self.cursor })
			self.cursor += 1

		return toReturn
