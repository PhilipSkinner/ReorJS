import conf
import settings
import api
import query
import stack
import output
import input
import logger

def main():
	config = conf.configure()
	
	#now configure our settings global
	set_setting('LOG_LOCATION',		config.log_location)
	set_setting('DEBUG', 			config.debug)
	set_setting('VERBOSE', 			config.verbose)
	set_setting('REGISTRATION_HOST', 	config.reg_host)
	set_setting('REGISTRATION_PORT', 	config.reg_port)
	set_setting('PORT', 			config.port)
	set_setting('IP', 			config.ip)
	set_setting('DB_TYPE', 			config.db_type)
	set_setting('REDIS_SOCKET', 		config.redis_sock)
	set_setting('REDIS_HOST', 		config.redis_host)
	set_setting('REDIS_PORT', 		config.redis_port)
	set_setting('MONGO_NAME',		config.mongo_name)
	set_setting('MONGO_HOST',		config.mongo_host)
	set_setting('MONGO_PORT',		config.mongo_port)
	set_setting('MONGO_READ',		config.mongo_read)
	set_setting('MYSQL_NAME',		config.mysql_name)
	set_setting('MYSQL_HOST',		config.mysql_host)
	set_setting('MYSQL_PORT',		config.mysql_port)
	set_setting('MYSQL_USER',		config.mysql_user)
	set_setting('MYSQL_PASSWORD',		config.mysql_password)
	set_setting('HTTP_SERVICE',		config.server)

	logger.LOG = logger.Logger()		
	logger.LOG.system.log('ReorJS service starting...')
	logger.LOG.system.log('Initializing API')
	
	#we need to configure our API database from settings
	if api.connect():	
		#and then our stacker		
		logger.LOG.system.log('Initializing stacker')
		stack.initStacker()
		
		#next we need to create our query service
		logger.LOG.system.log('Initializing query service')
		service = query.QueryService()
		
		#and run it
		logger.LOG.system.log('Running service...')
		service.run()		
	else:
		logger.LOG.api.log("Error connecting to API database, please check configuration.")
	

def set_setting(name, value):
	if settings.VERBOSE:
		logger.LOG.system.log('Setting system variable %s to value %s' % (name, value))
		
	setattr(settings, name, value)
	
def sigHandler(signal, frame):
	logger.LOG.system.log('ReorJS service exiting')	
	sys.exit(0)

if __name__ == '__main__':
	main()
