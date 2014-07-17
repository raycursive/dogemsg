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
                
postdata = {'action' : 'receive', 'from' : '123'}
request = GetRequest("http://msg.raycursive.com/api.php", postdata)
parsemsg(request)

