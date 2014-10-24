/*
 * Distributed messaging example v1.0.0
 * Author(s): Philip Skinner
 * Last modified: 2014-10-14
 *
 * --
 * 
 * Simple distributed messaging example between two nodes.
 *
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

function(id, data) {
  //its really simple, just fire the message over to the IP
  var ip = '127.0.0.1';
  var port = '8001';
  
  //taken from here http://stackoverflow.com/questions/9577611/http-get-request-in-node-js-express
  function getJSON(options, onResult) {
    var prot = options.port == 443 ? https : http;
    var req = prot.request(options, function(res) {
        var output = '';
        console.log(options.host + ':' + res.statusCode);
        res.setEncoding('utf8');

        res.on('data', function (chunk) {
            output += chunk;
        });

        res.on('end', function() {
            var obj = JSON.parse(output);
            onResult(res.statusCode, obj);
        });
    });

    req.on('error', function(err) { });

    req.end();
  };
  
  getJSON({
    host : ip,
    port : port,
    path : '/messager.php?message=' + data,
    method : 'GET',    
  }, function() {
    
  });

  return 1;
}
