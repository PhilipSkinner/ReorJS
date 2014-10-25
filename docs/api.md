ReorJS API
==========

The ReorJS API is a restful HTTP interface that allows you to manage your ReorJS service.

Please note, if you want to control your service manually you may want to look into using the ReorJS CLI instead. The API requires programming to be used correctly.

Formats & Access
----------------

The API runs on the same port as the main service, and is accessible through the following url format:

/api/v[version]

This document covers version 1 of the API. For older or newer documentation please find the relevant document in this release.

All data sent from the API is JSON and follows this format:

{
  'meta' : {
    'code' : [status code],
  },
  'error' : {
    'message' : [error message],
  },
  'status' : {
    'message' : [status message],
  },
  'data' : [encoded object],
}

Not all sections will be present. If there is an error then only the meta and error sections will be present in the data. If you committed a change operation on the API, the status and meta sections will be present. If you requested data from the api then the data and meta sections will be present.

Applications
------------

Endpoint: /api/v1/application
Method: GET
Description: Fetch a list of applications from the API.
Arguments:
  key			=> A valid API key

Endpoint: /api/v1/application
Method: POST
Description: Create a new application.
Arguments:
  key			=> A valid API key
  name 		=> The name of the program
  program 	=> The Javascript program

Endpoint: /api/v1/application/[application id]
Method: GET
Description: Gets the details of the application
Arguments:
  key			=> A valid API key

Endpoint: /api/v1/application/[application id]
Method: POST
Description: Modifies the application
Arguments:
  key			=> A valid API key
  name		=> The name of the program
  program	=> The Javascript program

Endpoint: /api/v1/application/[application id]
Method: DELETE
Description: Deletes the application
Arguments:
  key			=> A valid API key

Datasets
--------

Endpoint: /api/v1/dataset
Method: GET
Description: Fetch a list of datasets from the API.
Arguments:
  key			=> A valid API key

Endpoint: /api/v1/dataset
Method: POST
Description: Create a new dataset
Arguments:
  key			=> A valid API key
  name			=> The name of the dataset
  source_type		=> The type of source (mysql, redis, mongo)
  source_hostname 	=> The hostname of the source
  source_port		=> The port of the source
  source_name		=> The name of the source database
  source_table		=> The name of the source table
  source_username	=> The username for connecting to the source
  source_password	=> The password for connecting to the source

Endpoint: /api/v1/dataset/[dataset id]
Method: GET
Description: Gets the details of the dataset
Arguments:
  key			=> A valid API key

Endpoint: /api/v1/dataset/[dataset id]
Method: POST
Description: Updates the datasets details.
Arguments:
  key			=> A valid API key
  name			=> The name of the dataset
  source_type		=> The type of source (mysql, redis, mongo)
  source_hostname 	=> The hostname of the source
  source_port		=> The port of the source
  source_name		=> The name of the source database
  source_table		=> The name of the source table
  source_username	=> The username for connecting to the source
  source_password	=> The password for connecting to the source

Endpoint: /api/v1/dataset/[dataset id]
Method: DELETE
Description: Deletes the dataset
Arguments:
  key			=> A valid API key

Tasks
-----

Endpoint: /api/v1/tasks
Method: GET
Description: Fetch a list of tasks from the API
Arguments:
  key			=> A valid API key

Endpoint: /api/v1/tasks
Method: POST
Description: Creates a task
Arguments:
  key			=> A valid API key
  application		=> The ID of the application to run
  dataset		=> The ID of the dataset to use as source data
  result		=> The ID of the dataset to store the result in

Endpoint: /api/v1/tasks/[task id]
Method: GET
Description: Gets the details of the task
Arguments:
  key			=> A valid API key

Supplemental
------------

Endpoint: /output/v1/ping
Method: GET
Description: Pings the output service
Arguments: 
  key			=> A valid API key

Endpoint: /output/v1/status
Method: GET
Description: Fetches the status of the input/output stacker
Arguments:
  key			=> A valid API key

== Error Codes ==

Generally any errors returned by the system will be accompanied by an descriptive error message to assist you with the debugging of the problem.

Here is a list of the standard errors that are returned by the system and what they mean:

1001 => Application <id> not found
The application referenced by the ID passed to the system was not found in the API database.

1002 => Application requires a name
The name parameter for the application referenced in the request is either missing or not an acceptable value. Check the arguments you are passing.

1003 => Application requires a program
The program parameter for the application referenes in the request is either missing of not an acceptable value. Check the arguments you are passing.

1004 => Cannot delete application without an application id
An attempt was made to delete an application without providing the application id that the operation was to be carried out on.

405 => Unsupported method - <method>
A request using the method <method> was sent to the endpoint in question, but that method is not supported. For a full list of supported methods check the API documentation.

2001 => Dataset <id> not found
The dataset referenced by the ID passed to the system was not found in the API database.

2002 => Dataset requires a name
The name parameter for the dataset referenced in the request is either missing or not an acceptable value. Check the arguments you are passing.

2003 => Cannot delete dataset without a dataset id
An attempt was made to delete a dataset without providing the dataset id that the operation was to be carried out on.

2004 => Dataset data fetching requires dataset id
An attempt was made to fetch data from a dataset without providing the dataset id that the operation was to be carried out on.

2005 => Data must be provided for insertion
In order to insert data into a dataset, the data must be provided in the request. Any attempt to insert null or blank datapoints into a dataset will result in this error.

3001 => Task <id> not found
The task references by the ID passed to the system was not found in the API database.

3002 => Application ID required
The application id parameter for the task was not provided. Check the arguments you are passing.

3003 => Dataset ID required
The source dataset id parameter for the task was not provided. Check the arguments you are passing.

3004 => Result ID required
The result dataset id parameter for the task was not provided. Check the arguments you are passing.

3005 => No such application <id>
An application id was provided to the request that does not reference an application that could be found in the API database.

3006 => No such dataset <id>
A dataset id for the source dataset was provided to the request that does not reference a dataset that could be found in the API database.

3007 => No such result dataset <id
A dataset id for the result dataset was provided to the request that does not reference a dataset that could be found in the API database.

3010 => Task manipulation not yet supported
Modifying a task once it is in the system is not yet supported. Please install a newer release or consider updating to the latest master version from our repo.

404 => No tasks waiting
No tasks are currently waiting to be processed and as such no workunits are available for processing.

5001 => Missing cursor for result
The special cursor value for the result was missing from the result. Please ensure that your compute client is returning data in the correct manner. Check the client best practices document to ensure your client is compatible with the system.

5002 => Missing result for cursor
The result for this cursor was missing. Make sure that your application code is returning a correct result for every possible input value. Check the application development best practices document to ensure your application is as compatible as possible with the system.

9001 => Invalid API Key
An invalid api key was sent for authentication. This error will also occur if no API key is sent.

9002 => Could not reach output service
An attempt was made to ping the server and an invalid response was returned
