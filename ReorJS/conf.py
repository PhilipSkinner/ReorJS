"""
	conf.py
	Configuration manager for ReorJSd

	--
	Provides options for conf file and command line configuration
	parameter passing.
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

import argparse
try:
	import ConfigParser as configparser
except:
	import configparser
import socket

def configure():
	conf_parser = argparse.ArgumentParser(description="ReorJS service daemon", fromfile_prefix_chars='@',add_help=False)
	conf_parser.convert_arg_line_to_args = convert_arg_line_to_args

	conf_parser.add_argument('--config', default='/etc/reorjs/reorjsd.conf', help='Configuration file - see config format in docs')
	args, remaining_argv = conf_parser.parse_known_args()
	defaults = {
		'log-location' 	: '/var/log/reorjs',
		'verbose' 	: False,
		'debug' 		: False,
		'reg-host' 	: None,
		'reg-port' 	: '9999',
		'port' 		: '9999',
		'ip' 		: socket.gethostbyname(socket.gethostname()),
		'server' 	: 'tornado',
		'db-type' 	: 'redis',
		'redis-sock' 	: '/tmp/redis.sock',
		'redis-host' 	: 'localhost',
		'redis-port' 	: '8989',
		'mongo-name' 	: 'reorjs',
		'mongo-host' 	: 'localhost',
		'mongo-port' 	: '27017',
		'mongo-read' 	: 'secondaryPreferred',
		'mysql-name' 	: 'reorjs',
		'mysql-host' 	: 'localhost',
		'mysql-port' 	: '3306',
		'mysql-user' 	: 'reorjs',
		'mysql-password' : 'reorjs',
		'blocksize' 	: '100',
		'tasklimit' 	: '15',
		'readmethod' 	: '1',
		'root-key'	: None,
	}

	#do we have a conf file?
	if args.config != None:
		#read the config file
		config = configparser.SafeConfigParser()
		config.read([args.config])
		newDefaults = dict(config.items("Defaults"))
		for k, v in newDefaults.items():
			defaults[k] = v

	parser = argparse.ArgumentParser(parents=[conf_parser])

	#logging
	parser.add_argument('--log-location', default=defaults['log-location'], help='Log file directory')

	#debug settings
	parser.add_argument('--verbose', default=defaults['verbose'], help='Verbose output enabled')
	parser.add_argument('--debug', default=defaults['debug'], help='Debug mode enabled')

	#registration of cluster args
	parser.add_argument('--reg-host', default=defaults['reg-host'], help='Registration hostname - any of your existing clusters hosts')
	parser.add_argument('--reg-port', default=defaults['reg-port'], help='Registration port')

	#service details
	parser.add_argument('--port', default=defaults['port'], help='Port to run services on')
	parser.add_argument('--ip', default=defaults['ip'], help='Local IP address (override if required)')
	parser.add_argument('--server', default=defaults['server'], help='HTTP Server to use')

	#database type for API storage
	parser.add_argument('--db-type', default=defaults['db-type'], help='Database type for API temporary storage')

	#redis settings
	parser.add_argument('--redis-sock', default=defaults['redis-sock'], help='Local socket for redis server')
	parser.add_argument('--redis-host', default=defaults['redis-host'], help='Redis host')
	parser.add_argument('--redis-port', default=defaults['redis-port'], help='Redis port')

	#mongo settings
	parser.add_argument('--mongo-name', default=defaults['mongo-name'], help='MongoDB API name')
	parser.add_argument('--mongo-host', default=defaults['mongo-host'], help='MongoDB hostname')
	parser.add_argument('--mongo-port', default=defaults['mongo-port'], help='MongoDB port')
	parser.add_argument('--mongo-read', default=defaults['mongo-read'], help='MongoDB read preference')

	#mysql settings
	parser.add_argument('--mysql-name', default=defaults['mysql-name'], help='MySQL database name')
	parser.add_argument('--mysql-host', default=defaults['mysql-host'], help='MySQL hostname')
	parser.add_argument('--mysql-port', default=defaults['mysql-port'], help='MySQL port')
	parser.add_argument('--mysql-user', default=defaults['mysql-user'], help='MySQL username')
	parser.add_argument('--mysql-password', default=defaults['mysql-password'], help='MySQL password')

	#system settings
	parser.add_argument('--blocksize', default=defaults['blocksize'], help='Default processing block size')
	parser.add_argument('--tasklimit', default=defaults['tasklimit'], help='Number of tasks to process at the same time')
	parser.add_argument('--readmethod', default=defaults['readmethod'], help='Read method for stacker tasks')

	#authentication settings
	parser.add_argument('--root-key', default=defaults['root-key'], help="Define the root API key")

	args = parser.parse_args(remaining_argv)

	return args

def convert_arg_line_to_args(arg_line):
	for arg in arg_line.split():
		if not arg.strip():
			continue
		elif arg.strip() == '=':
			continue

		yield arg
