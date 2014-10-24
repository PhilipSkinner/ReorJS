/*
 * ReorJS Browser Node v1.0.0
 * Author(s): Philip Skinner
 * Last modified: 2014-09-28
 *
 * --
 * Browser based compute node for ReorJS.
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

var _compute = {
  //specify the domain and port your ReorJSd service is running on
  _domain	: 'http://yourwebsite.com:9999',
  //specify the timeout between tasks being executed - important for ensuring you do not overly affect a users computer
  _timeout 	: 500,
  //specify the maximum number of errors to allow before we stop processing tasks
  _maxError	: 10,
  _uid		: window.__cc_uid || 0,
  _timeStart	: 0,
  _data 	: null,
  _func 	: null,
  _results 	: {},
  _tasks 	: 0,
  _fetching	: false,
  _errors	: 0,

  _request	: function(options) {
    xhr = null;
    try {
      xhr = new XMLHttpRequest();
    } catch(e) {}
    try {
      xhr = new ActiveXObject('MSXML2.XMLHTTP');
    } catch(e) {}
    try {
      xhr = new ActiveXObject('Microsoft.XMLHTTP');
    } catch(e) {}

    var dataString = '';
    for (var i in options.data) {
      dataString += i + '=' + escape(options.data[i]) + '&';
    }    
    
    var method = 'GET';
    if (options.method) {
      method = options.method;
    }    
    if (method == 'GET') {    
      options.url += '?' + dataString;    
    }

    xhr.open(method, options.url, true, null, null);
    xhr.setRequestHeader('Accept', 'text/javascript, text/html, application/xml, text/xml, */*');

    if (method == 'POST') {
      xhr.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    }

    xhr.onreadystatechange = _compute._requestChange;
    xhr._execOnFinish = options.onComplete;    
    if (method == 'GET') {
      xhr.send(null);
    } else {
      xhr.send(dataString);
    }
  },
  
  _requestChange: function() {    
    if (this.readyState == 4) {
      //bingo
      if (this.response) {
        _compute._fetching = false;
        var script = document.createElement('script');
        script.setAttribute('type', 'text/javascript');
        script.text = '_compute.d = ' + this.response + ';';
        document.head.appendChild(script);
        document.head.removeChild(script);
      
        xhr._execOnFinish(_compute.d);
      } else {
        _compute._errors++;
        if (_compute._fetching && _compute._errors < _compute._maxError) {
          //do it again
          setTimeout('_compute._computeInit();', _compute._timeout);
        }      
      }
    }
  },

  _computeInit	: function() {
        _compute._fetching = true;
	_compute._timeStart = Date.now();
	
	_compute._request({
	  url : this._domain + '/output/v1/task', data: {},
	  onComplete: function(data) {
	    _compute._computeStart(data);
	  }
	});
  },
		
  _computeStart	: function(data) {  
	if (data && data.data && data.data.script && data.data.cursor) {
		_compute._data = data;
		_compute._results = {};
		_compute._func = function() {
        	        try {
        	          _compute._data.data.script = _compute._data.data.script.replace('\\n', '\n').replace('\\r', '\n').replace('\\t', '\r');
                          
                          var result = eval('(' + _compute._data.data.script + ')')(_compute._data.data.cursor, _compute._data.data.data);						
                          _compute._results['result'] = JSON.stringify(result);
                          _compute._results['cursor'] = _compute._data.data.cursor;
                          _compute._tasks--;
                                  
                          _compute._checkTasks();
                        } catch(e) { console.log(e); }                                                                
		};
			
		_compute._tasks = 1;
		setTimeout('_compute._func();', _compute._timeout);
	}		
  },
		
  _checkTasks	: function() {
	if (_compute._tasks > 0) {
		return;
	}
			
	_compute._sendResults(Date.now() - _compute._timeStart);
  },
	
  _sendResults	: function(taken) {
	_compute._request({
		url : this._domain + '/input/v1/result',
		data : _compute._results,
		method : 'POST',
		onComplete: function(data) {
		  //lets run again
		  _compute._computeInit();
		},				
	});
  }
}		

_compute._computeInit();
