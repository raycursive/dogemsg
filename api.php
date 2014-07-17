<?php 
$db = connectdatabase();
mysql_select_db("database", $db);

if ($_POST["action"] == "send")
	sendmsg();

if ($_POST["action"] == "receive")
	if ($_POST["to"])
	receivemsg($_POST["to"], "keyto");
	else if ($_POST["from"])
	receivemsg($_POST["from"], "keyfrom");

if ($_POST["action"] == "delete")
	if ($_POST["to"])
	delmsgs($_POST["to"], "keyto");
	else if ($_POST["from"])
	delmsgs($_POST["from"], "keyfrom");

exit(json_encode(array("Status" => "Nothing")));
//Send message
function sendmsg(){
	mysql_query("INSERT INTO `messages` (keyfrom, keyto, time, message) VALUES ('". $_POST["from"]. "', '". $_POST["to"]. "', now(), '". $_POST["message"]. "')");
	exit(json_encode(array("Status" => "Added 1!")));
}


//Query data from database. ($des = "keyto" => receive, $des = "keyfrom" => get chat logs)
function receivemsg($key, $des){
	$returndata = array();
	$result = mysql_query("SELECT * FROM `messages` WHERE `". $des ."` = '". $key ."' ORDER BY time");
	while ($row = mysql_fetch_array($result)){
		$msg = array("from" => $row["keyfrom"], 
					 "to" => $row["keyto"], 
					 "time" => $row["time"],
					 "message" => $row["message"]);
		array_push($returndata, json_encode($msg));
	}
	exit(json_encode($returndata));

}

//Del msgs two days before
function delmsgs($key, $des){
	mysql_query("DELETE FROM messages WHERE `" . $des . "` = '" . $key . "' AND  period_diff(curdate(), date(time)) >= 2");
	exit(json_encode(array("Status" => "Ok!")));
}		

//Connect database
function connectdatabase(){
	$db = mysql_connect("localhost", "account", "password");
	if (!$db){
		die('could not connect: ' . mysql_error());
	}
	else
		return $db;
}

