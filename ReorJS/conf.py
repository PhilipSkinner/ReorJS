import argparse
import socket

def configure():
	parser = argparse.ArgumentParser(description="ReorJS service daemon", fromfile_prefix_chars='@')
	parser.convert_arg_line_to_args = convert_arg_line_to_args

	#config file
	parser.add_argument('--config', default=None, help='Configuration file - see config format in docs')
	
	#debug settings
	parser.add_argument('--verbose', default=False, help='Verbose output enabled')
	parser.add_argument('--debug', default=False, help='Debug mode enabled')

	#registration of cluster args
	parser.add_argument('--reg-host', default=None, help='Registration hostname - any of your existing clusters hosts')
	parser.add_argument('--reg-port', default='9999', help='Registration port')

	#service details
	parser.add_argument('--port', default='9999', help='Port to run services on')
	parser.add_argument('--ip', default=socket.gethostbyname(socket.gethostname()), help='Local IP address (override if required)')
	parser.add_argument('--server', default='tornado', help='HTTP Server to use')

	#database type for API storage
	parser.add_argument('--db-type', default='redis', help='Database type for API temporary storage')

	#redis settings
	parser.add_argument('--redis-sock', default='/tmp/redis.sock', help='Local socket for redis server')
	parser.add_argument('--redis-host', default='localhost', help='Redis host')
	parser.add_argument('--redis-port', default='8989', help='Redis port')

	#mongo settings
	parser.add_argument('--mongo-name', default='reorjs', help='MongoDB API name')
	parser.add_argument('--mongo-host', default='localhost', help='MongoDB hostname')
	parser.add_argument('--mongo-port', default='27017', help='MongoDB port')
	parser.add_argument('--mongo-read', default='secondaryPreferred', help='MongoDB read preference')
	
	#mysql settings
	parser.add_argument('--mysql-name', default='reorjs', help='MySQL database name')
	parser.add_argument('--mysql-host', default='localhost', help='MySQL hostname')
	parser.add_argument('--mysql-port', default='3306', help='MySQL port')
	parser.add_argument('--mysql-user', default='reorjs', help='MySQL username')
	parser.add_argument('--mysql-password', default='reorjs', help='MySQL password')

	args = parser.parse_args()
	
	#do we have a conf file?
	if args.config != None:
		#read the config file
 		args = parser.parse_args(['@%s' % args.config])					

	return args

def convert_arg_line_to_args(arg_line):
        for arg in arg_line.split():
                if not arg.strip():
                        continue
                elif arg.strip() == '=':
                        continue
                        
                yield arg
