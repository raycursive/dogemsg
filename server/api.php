<?php
$db = connectdatabase();
mysql_select_db("dogemsg", $db);

if ($_POST["action"] == "send") sendmsg();
if ($_POST["action"] == "receive") receivemsg();
if ($_POST["action"] == "delete") delmsgs();
if ($_POST["action"] == "adduser") adduser();
if ($_POST["action"] == "modifyuser") modifyuser();
if ($_POST["action"] == "queryuser") queryuser();


exit(json_encode(array("Status" => "Nothing")));

//Connect database
function connectdatabase() {
    $db = mysql_connect("localhost", "dogemsg", "dogeisgood");
    if (!$db) {
        die('could not connect: ' . mysql_error());
    } else return $db;
}

//Send message
function sendmsg() {
	$res = mysql_query("INSERT INTO `messages` (`keyfrom`, `keyto`, `time`, `message`, `signature`, `read`) VALUES ('" . $_POST["from"] . "', '" . $_POST["to"] . "', NOW(), '" . $_POST["message"] . "', '" . $_POST["signature"] . "', '0')");
	if(!$res){
		exit(error('send', mysql_error()));
	}
	else
		exit(json_encode(array("Status" => "Success!", "action" => "send")));
}

//Query data from database. 
function receivemsg() {
	$returndata = array();
	if($_POST['unread'] == 1)
		$result = mysql_query("SELECT * FROM `messages` WHERE `keyto` = '" . $_POST["key"] . "' AND `read` = FALSE ORDER BY time");
	else
		$result = mysql_query("SELECT * FROM `messages` WHERE `keyto` = '" . $_POST["key"] . "' ORDER BY time");
	if(!$result)
		exit(error('receive', mysql_error()));
	while ($row = mysql_fetch_array($result)) {
	    $msg = array("from" => $row["keyfrom"], "to" => $row["keyto"], "time" => $row["time"], "message" => $row["message"], "signature" => $row["signature"], "read" => $row["read"]);
	    array_push($returndata, json_encode($msg));
	}
	$res = mysql_query("UPDATE `messages` SET `read` = TRUE WHERE `keyto` = '" . $_POST["key"] . "' AND `read` = FALSE ");
	if (!$res)
		exit(error("receive", mysql_error()));
	else
		exit(json_encode($returndata));
}

//Del msgs two days before
function delmsgs() {
    if (authen($_POST["key"])) {
        $res = mysql_query("DELETE FROM `messages` WHERE `keyto` = '" . $_POST["key"] . "' AND  (period_diff(curdate(), date(time)) >= 2 or `read` = TRUE)");
        if (!$res)
        	exit(error("delete", mysql_error()));
        else
        	exit(json_encode(array("Status" => "Success!", "action" => "delete")));
    } else {
        exit(error("delete", "Verify Failed!"));
    }
}

//Authentication
//If message, signature == signed message
//If not message, signature == your signed pubkey
function authen($key) {
	if ($_POST["message"]){
        $param = $key . " " . $_POST["signature"] . " " . $_POST["message"];
    } else {
    	$param = $key . " " . $_POST["signature"] . " " . $key;
    }
    $res = shell_exec("python3 /home/wwwroot/dogemsg/verify.py " . $param);	
    return strcmp($res, "True") == 0;
}

//Error Notification
function error($action, $details) {
    return json_encode(array("Status" => "Error!", "action" => $action, "Details" => $details));
}

//Add new user to the database
function adduser() {
    if (authen($_POST["key"])) {
    	$res = mysql_query("INSERT INTO `users` (`key`, `name`, `email`, `friendlist`) VALUES ('" . $_POST["key"] . "', '" . $_POST["name"] . "', '" . $_POST["email"] . "', '0')");
    	if (!$res)
    		exit(error("adduser", mysql_error()));
    	else
    		exit(json_encode(array("Status" => "Success!","action" => "adduser" ,"key" => $_POST["key"], "name" => $_POST["name"], "email" => $_POST["email"])));
    } else {
    	exit(error("adduser", "Verify Failed!"));
    }
}

//Modify user name
function modifyuser() {
    if (authen($_POST["key"])) {
    	$res = mysql_query("UPDATE `users` SET `name`='" . $_POST["name"] . "', `email`='" . $_POST["email"] . "' WHERE `key`='" . $_POST["key"] . "'");
    	if (!$res)
    		exit(error("modifyuser", mysql_error()));
    	else
    		exit(json_encode(array("Status" => "Success", "action" => "modifyuser", "key" => $_POST["key"], "name" => $_POST["name"], "email" => $_POST["email"])));
    } else {
    	exit(error("modifyuser", "Verify Failed!"));
    }
}

function queryuser(){
    $result = mysql_query("SELECT * FROM `users` WHERE `key` = '" . $_POST["key"] . "'");
    if (!$result)
            exit(error("queryuser", mysql_error()));
        else
            $row = mysql_fetch_array($result);
            exit(json_encode(array("name" => $row["name"], "email" => $row["email"], "key" => $row["key"])));
}
