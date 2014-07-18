import json

def msgdumps(string):
	result = {"type" : "message",
			  "message" : string.encode()
	}
	return json.dumps(result)

def msgloads(string):
	result = json.loads(string)
	return result['message'].decode()

def parsemsg(req):
	time = req['time']
	message = msgloads(req['message'])
	keyfrom = get_user_info(req['from'])
	return "====================================\n" + keyfrom + "\t" + time +"\n====================================\n" + message
