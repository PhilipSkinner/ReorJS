"""
	remote/local.py
	ReorJSd Local Data Connector

	--
	Provides a connection through to the local API database.
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

class MySQLRemote(RemoteConnection):
	def connect(self):

		return self.connection != None

	def readColumns(self):
		self.columns = [1]

	def query(self, rows=None):
		if rows == None:
			logger.LOG.log("Defaulting to 1000 rows")
			rows = 1000

		toReturn = []

		return toReturn
