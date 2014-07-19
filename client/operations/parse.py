import json
from contact import Contact
from operations import queryuser

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
	contact = getuserinfo(req['from'])
	keyfrom = contact['name']
	if 'alias' in contact:
		keyfrom += " (" + contact['alias'] + ")"
	return "====================================\n" + keyfrom + "\t" + time +"\n====================================\n\t" + message

#load userinfo from local file(if possible)(still implementing)
def getuserinfo(key):
        data = queryuser(key)   #it shoule be replaced to the method of friendlist
        return data
