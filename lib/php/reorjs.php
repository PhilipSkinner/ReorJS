<?php
  /**
   * reorjs.php
   * Simple ReorJS API connector
   *      
   * --
   * Provides simple programmatic access to the ReorJS server API calls for managing
   * ReorJS application, dataset and task objects
   * --
   *     
   * Author(s)       - Philip Skinner (philip@crowdca.lc)
   * Last modified   - 2014-11-01
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
   *
   * <code>
   * require_once('reorjs.php');
   * $reorjs = new ReorJS();
   * $reorjs->setHost('localhost');
   * $reorjs->setPort('9999');
   * $reorjs->setKey('temporary_key');
   * $reorjs->createApplication("hello", "world");
   * </code>
   */

  class ReorJS {
    var $host 	= 'localhost';
    var $port 	= '';
    var $key 	= '';

    /**
     * Function name: setHost
     * 
     * Overview: sets the reorjsd host to be used for requests
     *
     * Parameters: $host
     */    
    function setHost($host) {
      $this->host = $host;
    }
    
    /**
     * Function name: setPort
     *
     * Overview: sets the port to be used for communication
     *
     * Parameters: $port
     */    
    function setPort($port) {
      $this->port = $port;
    }
    
    /**
     * Function name: setKey
     *
     * Overview: sets the access key to be used for authentication
     *
     * Parameters: $key
     */    
    function setKey($key) {
      $this->key = $key;
    }

    /****************/
    /* TASK METHODS */
    /****************/
    
    /**
     * Function name: detailTask
     *
     * Overview: returns details for a particular task in the system
     *
     * Parameters: $id
     */    
    function detailTask($id=null) {
      $req = new _HTTP($this->_generateURL("/api/v1/task/" . $id . "?key=" . $this->key), $this->port, "GET");
      $req->send() or die("Couldn't send!");
      
      $raw = $req->getResponseBody();
      $data = json_decode($raw, true);

      return $this->_checkData($data);              
    }
    
    /**
     * Function name: createTask
     *
     * Overview: creates a task in the system
     *
     * Parameters: $application, $dataset, $result
     */    
    function createTask($application=null, $dataset=null, $result=null) {
      $req = new _HTTP($this->_generateURL("/api/v1/task"), $this->port, "POST");
      $req->headers["Content-Type"] = "application/x-www-form-urlencoded";
      $req->body = [
        "key"			=> $this->key,
        "application"		=> $application,
        "dataset"		=> $dataset,
        "result"		=> $result,
      ];      
      $req->send() or die("Couldn't send!");
      
      $raw = $req->getResponseBody();
      $data = json_decode($raw, true);

      return $this->_checkData($data);                        
    }
    
    /**
     * Function name: listTasks
     *
     * Overview: lists all of the tasks currently in the system
     *
     * Parameters: None
     */    
    function listTasks() {
      $req = new _HTTP($this->_generateURL("/api/v1/task?key=" . $this->key), $this->port, "GET");
      $req->send() or die("Couldn't send!");
      
      $raw = $req->getResponseBody();
      $data = json_decode($raw, true);

      return $this->_checkData($data);                
    }
    
    /*******************/
    /* DATASET METHODS */
    /*******************/
    
    /**
     * Function name: createDataset
     *
     * Overview: creates a new dataset (or source) in the system
     *
     * Parameters: $name, $source_type, $source_hostname, $source_port, $source_name, $source_table, $source_username, $source_password
     */    
    function createDataset($name=null, $source_type=null, $source_hostname=null, $source_port=null, $source_name=null, $source_table=null, $source_username=null, $source_password=null) {
      $req = new _HTTP($this->_generateURL("/api/v1/dataset"), $this->port, "POST");
      $req->headers["Content-Type"] = "application/x-www-form-urlencoded";
      $req->body = [
        "key"			=> $this->key,    
        "name" 			=> $name,
        "source_type" 		=> $source_type,
        "source_hostname" 	=> $source_hostname,
        "source_port" 		=> $source_port,
        "source_name" 		=> $source_name,
        "source_table" 		=> $source_table,
        "source_username" 	=> $source_username,
        "source_password" 	=> $source_password,
      ];      
      $req->send() or die("Couldn't send!");
      
      $raw = $req->getResponseBody();
      $data = json_decode($raw, true);

      return $this->_checkData($data);                  
    }
    
    /**
     * Function name: modifyDataset
     *
     * Overview: modifies an existing dataset
     *
     * Parameters: $id, $name, $source_type, $source_hostname, $source_port, $source_name, $source_table, $source_username, $source_password
     */    
    function modifyDataset($id=null, $name=null, $source_type=null, $source_hostname=null, $source_port=null, $source_name=null, $source_table=null, $source_username=null, $source_password=null) {
      $req = new _HTTP($this->_generateURL("/api/v1/dataset/" . $id), $this->port, "POST");
      $req->headers["Content-Type"] = "application/x-www-form-urlencoded";
      $req->body = [
        "key"			=> $this->key,
        "name" 			=> $name,
        "source_type" 		=> $source_type,
        "source_hostname" 	=> $source_hostname,
        "source_port" 		=> $source_port,
        "source_name" 		=> $source_name,
        "source_table" 		=> $source_table,
        "source_username" 	=> $source_username,
        "source_password" 	=> $source_password,
      ];      
      $req->send() or die("Couldn't send!");
      
      $raw = $req->getResponseBody();
      $data = json_decode($raw, true);

      return $this->_checkData($data);                  
    }
    
    /**
     * Function name: deleteDataset
     *
     * Overview: deletes a dataset
     *
     * Parameters: $id
     */    
    function deleteDataset($id=null) {
      $req = new _HTTP($this->_generateURL("/api/v1/dataset/" . $id . "?key=" . $this->key), $this->port, "DELETE");
      $req->send() or die("Couldn't send!");
      
      $raw = $req->getResponseBody();
      $data = json_decode($raw, true);

      return $this->_checkData($data);            
    }
    
    /**
     * Function name: detailDataset
     *
     * Overview: returns the details for a dataset
     *
     * Parameters: $id
     */    
    function detailDataset($id=null) {
      $req = new _HTTP($this->_generateURL("/api/v1/dataset/" . $id . "?key=" . $this->key), $this->port, "GET");
      $req->send() or die("Couldn't send!");
      
      $raw = $req->getResponseBody();
      $data = json_decode($raw, true);

      return $this->_checkData($data);            
    }
    
    /**
     * Function name: listDatasets
     *
     * Overview: returns a list of datasets in the system
     *
     * Parameters: None
     */    
    function listDatasets() {
      $req = new _HTTP($this->_generateURL("/api/v1/dataset?key=" . $this->key), $this->port, "GET");
      $req->send() or die("Couldn't send!");
      
      $raw = $req->getResponseBody();
      $data = json_decode($raw, true);

      return $this->_checkData($data);            
    }
    
    /*************************/
    /* APPLICATION ENDPOINTS */
    /*************************/
    
    /**
     * Function name: createApplication
     *
     * Overview: creates a new application
     *
     * Parameters: $name, $program
     */    
    function createApplication($name=null, $program=null) {
      $req = new _HTTP($this->_generateURL("/api/v1/application"), $this->port, "POST");
      $req->headers["Content-Type"] = "application/x-www-form-urlencoded";
      $req->body = [
        "key" 		=> $this->key,
        "name" 		=> $name,
        "program" 	=> $program,
      ];      
      $req->send() or die("Couldn't send!");
      
      $raw = $req->getResponseBody();
      $data = json_decode($raw, true);

      return $this->_checkData($data);              
    }
    
    /**
     * Function name: modifyAppliction
     *
     * Overview: modifies an application
     *
     * Parameters: $id, $name, $program
     */    
    function modifyApplication($id=null, $name=null, $program=null) {
      $req = new _HTTP($this->_generateURL("/api/v1/application/" . $id), $this->port, "POST");
      $req->headers["Content-Type"] = "application/x-www-form-urlencoded";
      $req->body = [
        "key"		=> $this->key,
        "name" 		=> $name,
        "program" 	=> $program,
      ];      
      $req->send() or die("Couldn't send!");
      
      $raw = $req->getResponseBody();
      $data = json_decode($raw, true);

      return $this->_checkData($data);      
    }
    
    /**
     * Function name: deleteApplication
     *
     * Overview: deletes an application
     *
     * Parameters: $id
     */    
    function deleteApplication($id=null) {
      $req = new _HTTP($this->_generateURL("/api/v1/application/" . $id . "?key=" . $this->key), $this->port, "DELETE");
      $req->send() or die("Couldn't send!");
      
      $raw = $req->getResponseBody();
      $data = json_decode($raw, true);

      return $this->_checkData($data);        
    }
    
    /**
     * Function name: detailApplication
     *
     * Overview: returns the details for an application
     *
     * Parameters: $id
     */    
    function detailApplication($id=null) {
      $req = new _HTTP($this->_generateURL("/api/v1/application/" . $id . "?key=" . $this->key), $this->port, "GET");
      $req->send() or die("Couldn't send!");
      
      $raw = $req->getResponseBody();
      $data = json_decode($raw, true);

      return $this->_checkData($data);    
    }
    
    /**
     * Function name: listApplications
     *
     * Overview: lists all of the applications
     *
     * Parameters: None
     */    
    function listApplications() {
      $req = new _HTTP($this->_generateURL("/api/v1/application?key=" . $this->key), $this->port, "GET");
      $req->send() or die("Couldn't send!");
      
      $raw = $req->getResponseBody();
      $data = json_decode($raw, true);

      return $this->_checkData($data);
    }

    /*
     * Private internal methods.
     */
    
    #checks return data and normalises some stuff    
    function _checkData($data) {
      if (isset($data['meta'])) {
        if (isset($data['meta']['code'])) {
          if ((string)$data['meta']['code'] === '200') {
            if (isset($data['data'])) {
              return $data['data'];
            } else if (isset($data['status'])) {
              return $data;
            }
          } else {
            if (isset($data['error'])) {
              return array(
                "error" => $data['error'],
                "code" => $data['meta']['code']
              );
            }
          }
        }
      }
      
      return array();
    }
    
    #generates a url from the host, port and endpoint
    function _generateURL($endpoint) {
      return 'http://' . $this->host . ':' . $this->port . $endpoint;
    }
  }

  /*
   * @access private
   * Simple HTTP class
   *
   * Based on https://gist.github.com/twslankard/989974
   */
  class _HTTP { 
    public $url 		= null;
    public $method 		= 'GET';
    public $body 		= null;
    public $headers 		= Array();
 
    var $url_info 		= null;
    var $host_name		= null;
    var $host_ip		= null;
    var $response_body 		= null;
    var $response_headers 	= Array();
    var $response_code 		= null;
    var $response_message 	= null;
 
    public function __construct($url, $port, $method) { 
      $this->url = $url;
      $this->method = $method;
 
      $this->url_info = parse_url($url);
      $this->host_name = $this->url_info['host'];
      $this->host_ip = gethostbyname($this->host_name); 
      $this->port = $port; 
      
      $this->headers["Host"] = $this->host_name;
      if ($this->port) {
        $this->headers["Host"] .= ':' . $this->port;
      }
      $this->headers["Cache-Control"] = "no-cache";
      $this->headers["Connection"] = "close";
  }
 
  private function constructRequest() {
    $path = "/";
    if(isset($this->url_info['path'])) {
      $path = $this->url_info['path'];
    }
    if (isset($this->url_info['query'])) {
      $path .= '?' . $this->url_info['query'];
    }

    $body = '';
    if ($this->body != null) {
      foreach($this->body as $key => $value) {
        $body .= $key . '=' . urlencode($value) . '&';
      }
      $this->headers["Content-Length"] = strlen($body);      
    }  
 
    $req = "$this->method $path HTTP/1.1\r\n";
    foreach($this->headers as $header => $value) {
      $req .= "$header: $value\r\n";
    }

    if ($body != '') {
      $req .= "\r\n";
      $req .= $body;
      $req .= "\r\n";
    }
    
    return "$req\r\n";
  }
 
  function readLine($fp) {
    $line = "";
 
    while (!feof($fp)) {
      $line .= fgets($fp, 2048);
      if (substr($line, -1) == "\n") {
        return rtrim($line, "\r\n");
      }
    }
    return $line;
  }
 
  public function send() { 
    $fp = fsockopen($this->host_ip, $this->port); 
    $request = $this->constructRequest();    
    fwrite($fp, $request);
    $line = $this->readline($fp);
    $status = explode(" ", $line);

    if(!isset($status[0]) || !preg_match("/^HTTP\/\d+\.?\d*/", $status[0])) {
      die("Couldn't get HTTP version from response.");
    }
    
    if(!isset($status[1])) {
      die("Couldn't get HTTP response code from response.");
    } else {
      $this->response_code = $status[1];
    }
    
    if(!isset($status[2])) {
      die("Couldn't get HTTP response reason from response.");
    } else {
      $this->response_reason = $status[2];
    }

    do {
      $line = $this->readLine($fp);
      if($line != "") { 
        $header = split(":", $line); 
        $this->response_headers[$header[0]] = ltrim($header[1]);
      }
    } while(!feof($fp) && $line != "");
    
    $this->response_body = "";
    do {
      $line = $this->readLine($fp);
      if ($line) {
        $this->response_body .= "$line\n";
      }
    } while(!feof($fp));
 
    fclose($fp); 
    return TRUE;
  }
 
  public function getStatus() {
    return $this->response_code;
  }
 
  public function getHeaders() {
    return $this->response_headers;
  }
 
  public function getResponseBody() {
    return $this->response_body;
  } 
}

?>
