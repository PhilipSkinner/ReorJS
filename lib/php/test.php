<?php
  require_once('reorjs.php');
  
  $reorjs = new ReorJS();
  
  $reorjs->setHost('localhost');
  $reorjs->setPort('9999');
  
  var_dump($reorjs->modifyApplication(1, "hello world", "everybody!"));
  var_dump($reorjs->listApplications());
?>