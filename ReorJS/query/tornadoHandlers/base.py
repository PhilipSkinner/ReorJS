"""
	query/tornadoHandlers/application.py
	ReorJSd Base Tornado Handler

	--
	Framework for creating Tornado handlers.
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

import tornado.web
import simplejson as json
import logger

class BaseHandler(tornado.web.RequestHandler):
	def prepare(self):
		self.set_header('Access-Control-Allow-Origin', '*')
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE, PUT')
		self.set_header('Access-Control-Allow-Headers', 'X-Request, X-Requested-With')
		self.set_header('Access-Control-Max-Age', '1728000')

	def get(self):
		logger.LOG.log("Tornado get needs to be overridden")

	def post(self):
		logger.LOG.log("Tornado post needs to be overridden")

	def delete(self):
		logger.LOG.log("Tornado delete needs to be overridden")

	def put(self):
		logger.LOG.log("Tornado put needs to be overridden")

	def options(self):
		logger.LOG.log("Tornado options needs to be overridden")
