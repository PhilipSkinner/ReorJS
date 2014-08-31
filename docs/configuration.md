Configuration
=============

Configuration files should be stored in /etc/reorjs.

Example configurations are provided to give you a starting point for configuring your ReorJS service.

Format
------

The format of the configuration file is as below:

--variable-name = value

Comments can be placed by entering a single hash (#) before the start of a line:

# this is a comment

Format of examples
------------------

Configuration examples in this document are formatted:

--variable-name = [Value1|Value2|Value3]

Where Value1, Value2 and Value3 are valid values for the configuration option variable-name.

For variables where a custom string value is to be entered, an example value will be provided:

--variable-name = [127.0.0.1]

Options
-------

The following options are available for configuration:

--debug = [True|False]
  Enables or disabled debugging, default value is False

--verbose = [True|False]
  Turns on/off verbose output, default value if False

--reg-host = [127.0.0.1]
  Sets the cluster control registration host, default is null

--reg-port = [9999]
  Sets the cluster control registration port, default is 9999

--port = [9999]
  Sets the servers port, default is 9999

--ip = [127.0.0.1]
  Sets the IP address to bind on, default is 127.0.0.1

--db-type = [mysql|mongo]
  Configures the API database type

--redis-socket = [/tmp/redis.sock]
  Optional, configures the redis socket on the local file system

--redis-host = [127.0.0.1]
  Optional, configures the redis host for networking

--redis-port = [8989]
  Optional, configures the redis port for networking

--mongo-name = [reorjs]
  Optional, configures the database name for mongo

--mongo-host = [127.0.0.1]
  Optional, configures the host for mongo

--mongo-port = [27017]
  Optional, configures the port for mongo

--mongo-read = [Primary]
  Optional, configures the read method for mongo

--mysql-name = [reorjs]
  Optional, configures the mysql database name

--mysql-host = [127.0.0.1]
  Optional, configures the mysql hostname

--mysql-port = [3306]
  Optional, configures the mysql port

--mysql-user = [username]
  Optional, configures the user for accessing mysql

--mysql-password = [password]
  Optional, configures the password for accessing mysql

--server = [tornado|fapws]
  Configures which HTTP service will be used for dealing with requests.
