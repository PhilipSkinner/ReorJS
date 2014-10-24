<?php

  class ReorJS {
    #default values
    var $host 	= 'localhost';
    var $port 	= '';
    var $key 	= '';
    
    function setHost($host) {
      $this->host = $host;
    }
    
    function setPort($port) {
      $this->port = $port;
    }
    
    function setKey($key) {
      $this->key = $key;
    }
    
    function connectionTest() {
      
    }
    
    function checkData($data) {
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
                error => $data['error'],
                code => $data['meta']['code']
              );
            }
          }
        }
      }
      
      return array();
    }
    
    function detailTask($id=null) {
      $req = new HTTP($this->_generateURL("/api/v1/task/" . $id), $this->port, "GET");
      $req->headers["Connection"] = "close";
      $req->send() or die("Couldn't send!");
      
      $raw = $req->getResponseBody();
      $data = json_decode($raw, true);

      return $this->checkData($data);              
    }
    
    function createTask($application=null, $dataset=null, $result=null) {
    
    }
    
    function listTasks() {
      $req = new HTTP($this->_generateURL("/api/v1/task"), $this->port, "GET");
      $req->headers["Connection"] = "close";
      $req->send() or die("Couldn't send!");
      
      $raw = $req->getResponseBody();
      $data = json_decode($raw, true);

      return $this->checkData($data);                
    }
    
    function createDataset($name=null, $source_type=null, $source_hostname=null, $source_port=null, $source_name=null, $source_table=null, $source_username=null, $source_password=null) {
    
    }
    
    function modifyDataset($id=null, $name=null, $source_type=null, $source_hostname=null, $source_port=null, $source_name=null, $source_table=null, $source_username=null, $source_password=null) {
    
    }
    
    function deleteDataset($id=null) {
      $req = new HTTP($this->_generateURL("/api/v1/dataset/" . $id), $this->port, "DELETE");
      $req->headers["Connection"] = "close";
      $req->send() or die("Couldn't send!");
      
      $raw = $req->getResponseBody();
      $data = json_decode($raw, true);

      return $this->checkData($data);            
    }
    
    function detailDataset($id=null) {
      $req = new HTTP($this->_generateURL("/api/v1/dataset/" . $id), $this->port, "GET");
      $req->headers["Connection"] = "close";
      $req->send() or die("Couldn't send!");
      
      $raw = $req->getResponseBody();
      $data = json_decode($raw, true);

      return $this->checkData($data);            
    }
    
    function listDatasets() {
      $req = new HTTP($this->_generateURL("/api/v1/dataset"), $this->port, "GET");
      $req->headers["Connection"] = "close";
      $req->send() or die("Couldn't send!");
      
      $raw = $req->getResponseBody();
      $data = json_decode($raw, true);

      return $this->checkData($data);            
    }
    
    function createApplication($name=null, $program=null) {
    
    }
    
    function modifyApplication($id=null, $name=null, $program=null) {
    
    }
    
    function deleteApplication($id=null) {
      $req = new HTTP($this->_generateURL("/api/v1/application/" . $id), $this->port, "DELETE");
      $req->headers["Connection"] = "close";
      $req->send() or die("Couldn't send!");
      
      $raw = $req->getResponseBody();
      $data = json_decode($raw, true);

      return $this->checkData($data);        
    }
    
    function detailApplication($id=null) {
      $req = new HTTP($this->_generateURL("/api/v1/application/" . $id), $this->port, "GET");
      $req->headers["Connection"] = "close";
      $req->send() or die("Couldn't send!");
      
      $raw = $req->getResponseBody();
      $data = json_decode($raw, true);

      return $this->checkData($data);    
    }
    
    function listApplications() {
      $req = new HTTP($this->_generateURL("/api/v1/application"), $this->port, "GET");
      $req->headers["Connection"] = "close";
      $req->send() or die("Couldn't send!");
      
      $raw = $req->getResponseBody();
      $data = json_decode($raw, true);

      return $this->checkData($data);
    }
    
    function _generateURL($endpoint) {
      return 'http://' . $this->host . ':' . $this->port . $endpoint;
    }
  }

  /* taken from https://gist.github.com/twslankard/989974 and customised */

  class HTTP { 
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
  }
 
  private function constructRequest() {
    $path = "/";
    if(isset($this->url_info['path']))
      $path = $this->url_info['path'];
 
    $req = "$this->method $path HTTP/1.1\r\n";
    foreach($this->headers as $header => $value) {
      $req .= "$header: $value\r\n";
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
