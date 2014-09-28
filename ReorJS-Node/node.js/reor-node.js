/*
 * ReorJS Node.js Node v1.0.0
 * Author(s): Philip Skinner
 * Last modified: 2014-09-28
 *
 * --
 * ReorJS node.js compute node with network discovery.
 *
 * This program includes a number of third party modules.
 *
 * These modules have been chosen to ensure that this code will run
 * correctly on multiple platforms.
 *
 * You can delete the scan directory and attempt to install these
 * modules manually, but we recommend to just copy the directory
 * along with this module.
 * --
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,     
 * but WITHOUT ANY WARRANTY; without even the implied warranty of      
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Copyright (c) 2014, Crowdcalc B.V.                                                                                                                      
*/

var SETTINGS = {
	version		: '0.0.1',
	port		: '9999',
	scan		: 15000,
	distributor	: null,
};

var http = require('http')
var querystring = require('querystring')

var inqueue = [];
var outqueue = [];

//woot

doScan();

function readQueue() {
	var item = inqueue.shift();
	var valid = false;

	if (item) {
		var _compute = {};

		_compute.results = {};
		_compute.parsed = JSON.parse(item);
		
		if (_compute.parsed) {
			//do we have some work?
			if (_compute.parsed.data && _compute.parsed.data.cursor && _compute.parsed.data.data && _compute.parsed.data.script) {
				//fix our script
				try {
					if (_compute.parsed.data.script) {
						_compute.parsed.data.script = _compute.parsed.data.script.replace("\\n", "\n").replace('\\r', '\n').replace('\\t', '\r');
					}
					
					_compute.result = eval('(' + _compute.parsed.data.script + ')')(_compute.parsed.data.cursor, _compute.parsed.data.data);
				} catch(e) {
					console.log("Error in script", _compute.parsed.data.script);
					console.log(e);
					_compute.result = { 'id' : 'ERR' };
				}

				_compute.id = _compute.parsed.data.cursor;
				
				console.log(_compute.result);
				
				outqueue.push({ result: JSON.stringify(_compute.result), id: _compute.id });
				valid = true;

				// we got some data, so we try and do some more right way
				//		readQueue();
				setTimeout(readQueue, 5000);
			}
		}
	}
	
	if (!valid) {
		// nothing in the queue, check again in a second
		console.log('Read queue is empty')
		setTimeout(readQueue, 5000);
	}
}


function sendMessage() {
	var item = outqueue.shift();

	if (item) {
		var post_data = querystring.stringify({
			cursor : item.id,
			result : item.result,
		});
		
		var post_options = {
			host: SETTINGS.distributor,
			port: SETTINGS.port,
			path: '/input/v1/result',
			method: 'POST',
			headers: {
				'Content-Type': 'application/x-www-form-urlencoded',
				'Content-Length': post_data.length
			}
		};

		var post_req = http.request(post_options, function(res) {
			res.setEncoding('utf8');
			res.on('data', function (chunk) {

			});
		});

		// post the data
		post_req.write(post_data);
		post_req.end();
		setTimeout(sendMessage, 1);
	} else {
		setTimeout(sendMessage, 10);
	}
}

getTimeout = 100;
getCounter = 0;

var _getHandler = function(res) {
	var str = '';

	res.on('data', function(chunk) {
		str += chunk;
	});

	//the whole response has been received, so we just print it out here
	res.on('end', function () {
		if (str.length) {
			inqueue.push(str);
			getTimeout = 1;
		} else {
			getTimeout = 10;
		}

		getCounter--;
	});
}

var _getFailHandler = function() {
	getCounter--;
}

function main() {
	if (getCounter < 1000) {
		var req = http.get('http://' + SETTINGS.distributor + ':' +  SETTINGS.port + '/output/v1/task', _getHandler);
		req.on('error', _getFailHandler);
		getCounter++;
	} else {
		getTimeout = 10;
	}

	setTimeout(main, getTimeout);
}

function doScan() {
	if (SETTINGS.distributor != null) {
		return;
	}

	console.log("Scanning for service discovery");

	var scan = require('./scan/main');
	var os = require('os');

	var range = []; 
	var ifaces = os.networkInterfaces();
	for (var dev in ifaces) {
		var alias=0;
		ifaces[dev].forEach(function(details) {
			if (details.family == 'IPv4') {
				var address = details.address;
				if (address != '127.0.0.1') {
					machineIP = address;
					for (var i = 0; i < 255; i++) {
						range.push(details.address.split('.').splice(0,3).join('.') + '.' + i);
					} 
				}
			}
		});
	}

	console.log("Scanning IP range", range[0], range[range.length - 1]);

	var options = {
		ips : range,
		ports: [SETTINGS.port],
		status: 'O',
		timeout: 100,
		banner : false,
		bannerlen : 0,
		showOpen : true,
	};

	var scanner = new scan(options);
	scanner.on('result', function(data) {
		if (data && data.status && data.status == 'open') {
			console.log("Found potential service", data.ip);
			SETTINGS.distributor = data.ip;

			main();
			readQueue();
			sendMessage();		
		}
	});
	scanner.on('done', function() {
		if (SETTINGS.distributor == null) {
			console.log("No service found, pausing and retrying");
			setTimeout(doScan, SETTINGS.scan);
		}
	});

	scanner.run();
}
