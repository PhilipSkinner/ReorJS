<?php
  $dbh = mysqli_connect("127.0.0.1", "reorjs", "reorjs", "messager");
  $host = "http://127.0.0.1:9999/api/v1";
  $applicationId = 1;
  $resultId = 5;

  if ($_GET["action"]) {
    if ($_GET["action"] == 'poll') {
      //fetch any messages fragments from the mysql DB and delete
      $qry = "SELECT uid, content FROM received";
      $result = mysqli_query($dbh, $query);
      $ret = array();
      while ($row = mysqli_fetch_array($result)) {
        mysqli_query($dbh, "DELETE FROM received WHERE uid=" . $row['uid']);
        array_push($ret, $row['content']);
      }
      
      echo json_encode(array('results' => $ret));
    } else if ($_GET["action"] == 'receive') {
      //we got a message fragment!
      $content = mysqli_real_escape_string($dbh, $_GET["content"]);
      $qry = "INSERT INTO received (content) VALUES ('$content')";
      mysqli_query($dbh, $query);
      
      echo json_encode(array('result' => 1));
    } else if ($_GET["action"] == 'send') {
      //create a new table and insert the data
      $name = generateRandomString();
      $qry = "CREATE TABLE $name (uid int(11) not null auto_increment primary key, content text)";
      if (mysqli_query($dbh, $qry)) {      
        //register a data source with our local reorjs
        $url = $host . "/dataset";
        $data = array(
          'name' => $name,
          'source_type' => 'mysql',
          'source_hostname' => '127.0.0.1',
          'source_port' => '3306',
          'source_name' => 'messager',
          'source_table' => $name,
          'source_username' => 'reorjs',
          'source_password' => 'reorjs',
        );
        $options = array(
          'http' => array(
            'header' => 'Content-type: application/x-www-form-urlencoded\n',
            'method' => 'POST',
            'content' => http_build_query($data),
          ),
        );
        $context = stream_context_create($options);
        $result = file_get_contents($url, false, $context);
        
        $data = json_decode($result);
        
        if ($data['id']) {
          //create a task 
          $url = $host . "/tasks";
          $data = array(
            'application' => $applicationId,
            'dataset' => $data["id"],
            'result' => $resultId,
          );
          $options = array(
            'http' => array(
              'header' => 'Content-type: application/x-www-form-urlencoded\n',
              'method' => 'POST',
              'content' => http_build_query($data),
            ),
          );
          $context = stream_context_create($options);
          $result = file_get_contents($url, false, $context);
          
          echo json_encode(array('result' => 1));          
        }
      }
    }
  }

  echo json_encode(array('result' => 0));          

  //taken from http://stackoverflow.com/questions/4356289/php-random-string-generator  
  function generateRandomString($length = 10) {
    $characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
    $randomString = '';
    for ($i = 0; $i < $length; $i++) {
      $randomString .= $characters[rand(0, strlen($characters) - 1)];
    }
    return $randomString;
  }
?>
