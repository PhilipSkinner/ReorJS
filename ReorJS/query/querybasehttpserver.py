"""
	query/querybasehttpserver.py
	ReorJSd Base HTTP Service

	--
	Uses the BaseHTTPServer class to create and handle all HTTP requests
	to the ReorJSd services.
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

from .base import BaseQueryService
import settings
import logger
try:
	from urllib.parse import urlparse # python 3
except:
	from urlparse import urlparse # python2

import re
import cgi
from . import handlers

try:
	from http.server import BaseHTTPRequestHandler, HTTPServer # python 3
except:
	from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer # python 2


class QueryBaseHTTPServer(BaseQueryService):
	def __init__(self, output=None, input=None):
		logger.LOG.log("Setting up QueryBaseHTTPServer")

		self.DataSetDataHandler = handlers.APIDataSetDataHandler(self)
		self.DataSetHandler = handlers.APIDataSetHandler(self)
		self.TaskHandler = handlers.APITaskHandler(self)
		self.ApplicationHandler = handlers.APIApplicationHandler(self)
		self.KeyHandler = handlers.APIKeyHandler(self)

		self.output = output
		self.input = input

		self.server = HTTPServer((settings.IP, int(settings.PORT)), HTTPHandler)
		self.server.parent = self
		self.server.serve_forever()

class HTTPHandler(BaseHTTPRequestHandler):
	def determine_operation(self, method='GET', url=''):
		#reset
		self._headers = [
			('Access-Control-Allow-Origin', '*'),
			('Access-Control-Allow-Headers', 'X-Request, X-Requested-With'),
			('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, DELETE, PUT'),
			('Access-Control-Max-Age', '1728000')
		]
		self._response = ''
		self.parsed_path = urlparse.urlparse(self.path)
		self.args = urlparse.parse_qs(self.parsed_path.query)
		self.form = {}
		if method == 'POST':
			self.form = cgi.FieldStorage(
				fp = self.rfile,
				headers = self.headers,
				environ = {'REQUEST_METHOD' : 'POST', 'CONTENT_TYPE' : self.headers['Content-Type']})

		urls = [
			('/api/v1/dataset/(.*)/data', self.data_set_data_handler),
			('/api/v1/dataset/(.*)', self.data_set_handler),
			('/api/v1/dataset/', self.data_set_handler),
			('/api/v1/dataset', self.data_set_handler),
			('/api/v1/task/(.*)', self.task_handler),
			('/api/v1/task/', self.task_handler),
			('/api/v1/task', self.task_handler),
			('/api/v1/application/(.*)', self.application_handler),
			('/api/v1/application/',self.application_handler),
			('/api/v1/application',	self.application_handler),
			('/api/v1/key/(.*)', self.key_handler),
			('/api/v1/key/', self.key_handler),
			('/api/v1/key', self.key_handler),
		]

		if self.server.parent.output != None:
			urls.append(('/output/v1/task', self.get_task_handler))
			urls.append(('/output/v1/ping', self.ping_handler))
			urls.append(('/output/v1/status', self.status_handler))

		if self.server.parent.input != None:
			urls.append(('/input/v1/result', self.receive_result_handler))

		for u in urls:
			m = re.match('^%s(\?)?.*?$' % u[0], url)

			if m != None:
				#we have our match
				return u[1](method, url, m)

	##
	# output handlers
	##

	def get_task_handler(self, method, urls, matches):
		self.server.parent.output.GetTaskHandler.setParent(self)

		if method == 'GET':
			self.server.parent.output.GetTaskHandler.get()
		elif method == 'POST':
			self.server.parent.output.GetTaskHandler.post()
		elif method == 'DELETE':
			self.server.parent.output.GetTaskHandler.delete()
		elif method == 'PUT':
			self.server.parent.output.GetTaskHandler.put()

		self.complete_request()
		return

	def ping_handler(self, method, urls, matches):
		self.server.parent.output.PingHandler.setParent(self)

		if method == 'GET':
			self.server.parent.output.PingHandler.get()
		elif method == 'POST':
			self.server.parent.output.PingHandler.post()
		elif method == 'DELETE':
			self.server.parent.output.PingHandler.delete()
		elif method == 'PUT':
			self.server.parent.output.PingHandler.put()

		self.complete_request()
		return

	def status_handler(self, method, urls, matches):
		self.server.parent.output.StatusHandler.setParent(self)

		if method == 'GET':
			self.server.parent.output.StatusHandler.get()
		elif method == 'POST':
			self.server.parent.output.StatusHandler.post()
		elif method == 'DELETE':
			self.server.parent.output.StatusHandler.delete()
		elif method == 'PUT':
			self.server.parent.output.StatusHandler.put()

		self.complete_request()
		return

	##
	# input handlers
	##

	def receive_result_handler(self, method, urls, matches):
		self.server.parent.input.ReceiveResultHandler.setParent(self)

		if method == 'GET':
			self.server.parent.input.ReceiveResultHandler.get()
		elif method == 'POST':
			self.server.parent.input.ReceiveResultHandler.post()
		elif method == 'DELETE':
			self.server.parent.input.ReceiveResultHandler.delete()
		elif method == 'PUT':
			self.server.parent.input.ReceiveResultHandler.put()

		self.complete_request()
		return

	##
	# api handlers
	##

	def data_set_data_handler(self, method, url, matches):
		parts = matches.groups()
		id = None

		if len(parts) > 0:
			id = parts[0]

		self.server.parent.DataSetDataHandler.setParent(self)

		if method == 'GET':
			self.server.parent.DataSetDataHandler.get(id=id)
		elif method == 'POST':
			self.server.parent.DataSetDataHandler.post(id=id)
		elif method == 'DELETE':
			self.server.parent.DataSetDataHandler.delete(id=id)
		elif method == 'PUT':
			self.server.parent.DataSetDataHandler.put(id=id)

		self.complete_request()
		return

	def data_set_handler(self, method, url, matches):
		parts = matches.groups()
		id = None

		if len(parts) > 0:
			id = parts[0]

		self.server.parent.DataSetHandler.setParent(self)

		if method == 'GET':
			self.server.parent.DataSetHandler.get(id=id)
		elif method == 'POST':
			self.server.parent.DataSetHandler.post(id=id)
		elif method == 'DELETE':
			self.server.parent.DataSetHandler.delete(id=id)
		elif method == 'PUT':
			self.server.parent.DataSetHandler.put(id=id)

		self.complete_request()
		return

	def task_handler(self, method, url, matches):
		parts = matches.groups()
		id = None

		if len(parts) > 0:
			id = parts[0]

		self.server.parent.TaskHandler.setParent(self)

		if method == 'GET':
			self.server.parent.TaskHandler.get(id=id)
		elif method == 'POST':
			self.server.parent.TaskHandler.post(id=id)
		elif method == 'DELETE':
			self.server.parent.TaskHandler.delete(id=id)
		elif method == 'PUT':
			self.server.parent.TaskHandler.put(id=id)

		self.complete_request()
		return

	def key_handler(self, method, url, matches):
		parts = matches.groups()
		id = None

		if len(parts) > 0:
			id = parts[0]

		self.server.parent.KeyHandler.setParent(self)

		if method == 'GET':
			self.server.parent.KeyHandler.get(id=id)
		elif method == 'POST':
			self.server.parent.KeyHandler.post(id=id)
		elif method == 'DELETE':
			self.server.parent.KeyHandler.delete(id=id)
		elif method == 'PUT':
			self.server.parent.KeyHandler.put(id=id)

		self.complete_request()
		return

	def application_handler(self, method, url, matches):
		parts = matches.groups()
		id = None

		if len(parts) > 0:
			id = parts[0]

		self.server.parent.ApplicationHandler.setParent(self)

		if method == 'GET':
			self.server.parent.ApplicationHandler.get(id=id)
		elif method == 'POST':
			self.server.parent.ApplicationHandler.post(id=id)
		elif method == 'DELETE':
			self.server.parent.ApplicationHandler.delete(id=id)
		elif method == 'PUT':
			self.server.parent.ApplicationHandler.put(id=id)

		self.complete_request()
		return

	def do_POST(self):
		self.determine_operation('POST', self.path)
		return

	def do_DELETE(self):
		self.determine_operation('DELETE', self.path)
		return

	def do_PUT(self):
		self.determine_operation('PUT', self.path)
		return

	def do_OPTIONS(self):
		self.determine_operation('OPTIONS', self.path)
		return

	def do_GET(self):
		self.determine_operation('GET', self.path)
		return

	def complete_request(self):
		self.do_headers()
		self.wfile.write(self._response)
		return

	#standard data return methods
	def do_headers(self):
		self.send_response(200)
		for h in self._headers:
			self.send_header(h[0], h[1])
		self.end_headers()

	def get_argument(self, name, default):
		if name in list(self.args.keys()):
			return str(self.args[name][0])

		if name in list(self.form.keys()):
			return str(self.form[name].value)

		return default

	def set_header(self, name, value):
		self._headers.append((name, value))

	def write(self, value):
		self._response = "%s%s" % (self._response, value)
