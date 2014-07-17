<?php 
$db = connectdatabase();
mysql_select_db("dogemsg", $db);

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

//Connect database
function connectdatabase(){
	$db = mysql_connect("localhost", "dogemsg", "dogeisgood");
	if (!$db){
		die('could not connect: ' . mysql_error());
	}
	else
		return $db;
}


//Send message
function sendmsg(){
	mysql_query("INSERT INTO `messages` (keyfrom, keyto, time, message, signature, read) VALUES ('". $_POST["from"] . "', '" . $_POST["to"] . "', now(), '" . $_POST["message"] . "', '" . $_POST["signature"] . "', 0)");
	exit(json_encode(array("Status" => "Added 1!", "action" => "send")));
}


//Query data from database. ($des = "keyto" => receive, $des = "keyfrom" => get chat logs)
function receivemsg($key, $des){
	$returndata = array();
	$result = mysql_query("SELECT * FROM `messages` WHERE `". $des ."` = '". $key ."' AND `read` = FALSE ORDER BY time");
	while ($row = mysql_fetch_array($result)){
		$msg = array("from" => $row["keyfrom"], 
					 "to" => $row["keyto"], 
					 "time" => $row["time"],
					 "message" => $row["message"],
					 "signature" => $row["signature"]);
		array_push($returndata, json_encode($msg));
	}
	exit(json_encode($returndata));

}

//Del msgs two days before
function delmsgs($key, $des){
	$param = $key . " " . $_POST["signature"] . " " . $_POST["message"];
	$res = shell_exec("python3 /home/wwwroot/dogemsg/verify.py ". $param);
	 if(strcmp($res, "True") == 0){
		mysql_query("DELETE FROM messages WHERE `" . $des . "` = '" . $key . "' AND  period_diff(curdate(), date(time)) >= 2");
		exit(json_encode(array("Status" => "Success!", "action" => "delete")));
	}
	else{
		exit(json_encode(array("Status" => "Error!", "action" => "delete","Error" => "Verify failed!")));
	}
}

