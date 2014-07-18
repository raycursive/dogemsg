<?php
$db = connectdatabase();
mysql_select_db("dogemsg", $db);

if ($_POST["action"] == "send") sendmsg($_POST["from"]);

if ($_POST["action"] == "receive") if ($_POST["to"]) receivemsg($_POST["to"], "keyto");
else if ($_POST["from"]) receivemsg($_POST["from"], "keyfrom");

if ($_POST["action"] == "delete") if ($_POST["to"]) delmsgs($_POST["to"], "keyto");
else if ($_POST["from"]) delmsgs($_POST["from"], "keyfrom");

exit(json_encode(array("Status" => "Nothing")));

//Connect database
function connectdatabase() {
    $db = mysql_connect("localhost", "dogemsg", "dogeisgood");
    if (!$db) {
        die('could not connect: ' . mysql_error());
    } else return $db;
}

//Send message
function sendmsg($key) {
	if (authen($key)) {
	    mysql_query("INSERT INTO `messages` (keyfrom, keyto, time, message, signature, read) VALUES ('" . $key . "', '" . $_POST["to"] . "', now(), '" . $_POST["message"] . "', '" . $_POST["signature"] . "', FALSE)");
	    exit(json_encode(array("Status" => "Added 1!", "action" => "send")));
	} else {
		exit(error('send'));
	}
}

//Query data from database. ($des = "keyto" => receive, $des = "keyfrom" => get chat logs)
function receivemsg($key, $des) {
	if (authen($key)) {
	    $returndata = array();
	    $result = mysql_query("SELECT * FROM `messages` WHERE `" . $des . "` = '" . $key . "' AND `read` = FALSE ORDER BY time");
	    mysql_query("UPDATE 'messages' SET 'read' = TRUE WHERE `" . $des . "` = '" . $key . "' AND `read` = FALSE ");
	    while ($row = mysql_fetch_array($result)) {
	        $msg = array("from" => $row["keyfrom"], "to" => $row["keyto"], "time" => $row["time"], "message" => $row["message"], "signature" => $row["signature"]);
	        array_push($returndata, json_encode($msg));
	    }
	    exit(json_encode($returndata));
	} else {
		exit(error('receive'))
	}
    
}

//Del msgs two days before
function delmsgs($key, $des) {
    if (authen($key)) {
        mysql_query("DELETE FROM messages WHERE `" . $des . "` = '" . $key . "' AND  period_diff(curdate(), date(time)) >= 2");
        exit(json_encode(array("Status" => "Success!", "action" => "delete")));
    } else {
        exit(error('delete'));
    }
}

//Authentication
//If message, signature == signed message
//If not message, signature == your signed pubkey
function authen($key, $message) {
	if ($_POST["message"]){
        $param = $key . " " . $_POST["signature"] . " " . $_POST["message"];
    } else {
    	$param = $key . " " . $_POST["signature"] . " " . $key;
    }
    $res = shell_exec("python3 /home/wwwroot/dogemsg/verify.py " . $param);	
    return strcmp($res, "True") == 0;
}

//Error Notification
function error($action) {
    return json_encode(array("Status" => "Error!", "action" => $action, "Error" => "Verify failed!"));
}

//Add new user to the database
function adduser($key, $name, $email) {
    if (authen($key)) {
    	mysql_query("INSERT INTO 'users' (key, name, email, friendlist) VALUES ('" . $key . "', '" . $name . "', '" . $email . "', 'FALSE'");
    	exit(json_encode(array("Status" => "user added", "key" => $key, "name" => $name, "email" => $email)));
    } else {
    	exit(error('adduser'))
    }
}

//Modify user name
function modifyuser($key, $name, $email) {
    if (authen($key)) {
    	mysql_query("UPDATE 'users' SET 'name'='" . $name . "', 'email'='" . $email . "' WHERE 'key'='" . $key . "'");
    	exit(json_encode(array("Status" => "user modified", "key" => $key, "name" => $name, "email" => $email)));
    } else {
    	exit(error('modifyuser'))
    }
}
