"""
	query/__init__.py
	ReorJSd Query Service

	--
	Initializes the selected query service for the system.
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

import settings
import logger
from .queryfapws import QueryFAPWS
from .querytornado import QueryTornado
from .querybasehttpserver import QueryBaseHTTPServer

import output
import input

class QueryService():
	def __init__(self):
		self.tornado = None
		self.fapws = None
		self.base = None

		self.output = output.OutputService()
		self.input = input.InputService()

		if settings.HTTP_SERVICE == 'tornado':
			logger.LOG.log("Setting up Tornado")

			self.tornado = QueryTornado(output=self.output, input=self.input)
		elif settings.HTTP_SERVICE == 'fapws':
			logger.LOG.log("Setting up fapws")

			self.fapws = QueryFAPWS(output=self.output, input=self.input)
		elif settings.HTTP_SERVICE == 'base':
			logger.LOG.log("Setting up BaseHTTPServer")

			self.base = QueryBaseHTTPServer(output=self.output, input=self.input)

	def run(self):
		if self.tornado != None:
			logger.LOG.log("Running tornado service")

			self.tornado.start()
		elif self.fapws != None:
			logger.LOG.log("Running fapws service")

			self.fapws.start()
		elif self.base != None:
			logger.LOG.log("Running BaseHTTPServer service")

			self.base.start()
