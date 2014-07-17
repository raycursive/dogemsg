import json
import urllib.request, urllib.parse

def GetRequest(des, postdata):
	params = urllib.parse.urlencode(postdata).encode('utf-8')
	header = {'User-Agent':'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'}
	req = urllib.request.Request(
		url = des,
		data = params,
		headers = header
		)
	return urllib.request.urlopen(req).read().decode("UTF8")

def parsemsg(req):
        for i in map(json.loads, json.loads(req)):
                print(i)

def testreceive(des, key):
        postdata = {'action' : 'receive', des : key}
        request = GetRequest("http://msg.raycursive.com/api.php", postdata)
        parsemsg(request)

def testsend(keyfrom, keyto, message):
        postdata = {'action' : 'send', 'from' : keyfrom, 'to' : keyto, 'message': message}
        request = GetRequest("http://msg.raycursive.com/api.php", postdata)
        print(request)

def testdelete(key, des, signature, message):
        postdata = {'action' : 'delete', des : key, 'signature' : signature, 'message': message}
        request = GetRequest("http://msg.raycursive.com/api.php", postdata)
        print(postdata)
        print(request)
