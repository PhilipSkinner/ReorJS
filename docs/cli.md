ReorJS Command Line Interface
=============================

The ReorJS CLI gives you quick and easy access to the API provided by the ReorJS service.

To run the ReorJS CLI run the following command:

reorjs-cli

If you cannot find the reorjs-cli command on your machine, ensure that the configuration and installation mechanism could install it correctly. Its requirements are different to those of the server and node clients.

Getting Help
------------

To get help while using the CLI, enter the help command.

All other commands have documented help aswell, to access it you can do:

[command] help

If you require help with a subcommand you may also run:

[command] help [subcommand]

An example of this is the application list command:

application help list

Commands
--------

*help*

Displays a list of supported commands.

*connect*

Usage: connect http://[host]:[port] [apikey]

*application*

Usage: application [command] [options...]

Applications are javascript functions that can be run against data within the system.

Supported Commands

* list 
  Usage: application list
* detail 
  Usage: application detail [application id]
* create 
  Usage: application create [name] [program]
* modify 
  Usage: application modify [id] [name] [program]
* delete
  Usage: application delete [id]

*dataset*

Usage: dataset [command] [options...]

Datasets are sources of information. Currently supported sources are mysql, mongo, redis, memcached, hadoop and the local API

Supported Commands: 

* list 
  Usage: dataset list
* detail 
  Usage: dataset detail [id]
* create 
  Usage: dataset create [name] [type] *hostname* *port* *dbname* *tablename* *username* *password*
* modify 
  Usage: dataset modify [id] [name] [type] *hostname* *port* *dbname* *tablename* *username* *password*
* delete
  Usage: dataset delete [id]

*task*

Usage: task [command] [options...]

Tasks map an application to a set of data and starts the computation on the connected ReorJS Javascript clients.

Supported Commands: 

* list 
  Usage: task list
* detail 
  Usage: task detail [id]
* create
  Usage: task create [application id] [dataset id] [result dataset id]

