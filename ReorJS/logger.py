"""
	logger.py
	Logging for ReorJSd.

	--
	Provides logging access for ReorJSd.
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

import logging
import settings

class Logger():
	def __init__(self, logfile, level):
		logging.basicConfig(filename=logfile,level=level,format='%(asctime)-15s - [%(processName)s,%(process)d] - %(message)s')
		logging.info("Started logging")

	def critical(self, value):
		logging.error(value)

	def error(self, value):
		logging.error(value)

	def log(self, value):
		logging.warning(value)

	def info(self, value):
		logging.info(value)

	def debug(self, value):
		logging.debug(value)

LOG = None

def initLogger():
	global LOG
	level = logging.WARNING

	if settings.VERBOSE or settings.VERBOSE == "True":
		level = logging.INFO

	if settings.DEBUG or settings.DEBUG == "True":
		level = logging.DEBUG

	LOG = Logger('%s/reorjsd.log' % settings.LOG_LOCATION, level)
