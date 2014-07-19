import json
from contact import Contact

def msgdumps(string):
	result = {"type" : "message",
			  "message" : string
	}
	return json.dumps(result)

def msgloads(string):
	result = json.loads(string)
	return result['message']

def parsemsg(req):
	time = req['time']
	message = msgloads(req['message'])
	contact = getuserinfo(queryuser(req['from']))
	keyfrom = contact.name
	if contact.alias != "":
		keyfrom += " (" + contact.alias + ")"
	return "====================================\n" + keyfrom + "\t" + time +"\n====================================\n\t" + message

#load userinfo from local file(if possible)(still implementing)
def getuserinfo(string):
	result = json.loads(string)
	return Contact(result["key"], name = result["name"], alias = "", email = result["email"])
