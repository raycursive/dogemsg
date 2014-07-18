import json
import urllib.request
import urllib.parse
import parsemsg
from randomstr import *
from key import *
from binascii import hexlify, unhexlify

server = "http://msg.raycursive.com/api.php"

def GetRequest(des, postdata):
    params = urllib.parse.urlencode(postdata).encode('utf-8')
    header = {
        'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'}
    req = urllib.request.Request(
        url=des,
        data=params,
        headers=header
    )
    return urllib.request.urlopen(req).read().decode("UTF8")




def receive(key, unread = 1):
    '''key: ECC'''
    postdata = {'action': 'receive',
                'key': tohex(key.get_pubkey()),
                'unread' : unread
                }
    request = GetRequest(server, postdata)
    result = []
    for i in map(json.loads, json.loads(request)):
        i['message'] = key.decrypt(unhexlify(i['message']))
        if ECC(pubkey = unhexlify(i['from'])).verify(unhexlify(i['signature']),i['message']):
            i['message'] = i['message'].decode()
            result.append(i)
        else:
            print("ERROR! Verify Failed!")
    return result



def send(keyfrom, keyto, message):
    '''keyfrom : ECC keyto : hex address'''
    postdata = {'action': 'send',
                'from': tohex(keyfrom.get_pubkey()),
                'to': keyto,
                'signature': tohex(keyfrom.sign(message)),
                'message': tohex(keyfrom.encrypt(message, unhexlify(keyto)))
                }
    request = GetRequest(server, postdata)
    print(request)


def delete(key):
    ''' key : ECC'''
    msg = random_str()
    sign = tohex(key.sign(msg))
    postdata = {'action': 'delete',
                'key': tohex(key.get_pubkey()),
                'signature': sign,
                'message': msg
                }
    request = GetRequest(server, postdata)
    print(request)


def adduser(key, name='Anonymous', email=''):
    ''' key : ECC '''
    msg = random_str()
    sign = tohex(key.sign(msg))    
    postdata = {'action': 'adduser',
                'key': tohex(key.get_pubkey()),
                'name': name,
                'email': email,
                'signature': sign,
                'message': msg
                }
    request = GetRequest(server, postdata)
    print(request)

def modifyuser(key, name='Anonymous', email=' '):
    msg = random_str()
    sign = tohex(key.sign(msg))
    postdata = {'action': 'modifyuser',
                'key': tohex(key.get_pubkey()),
                'name':name,
                'email': email,
                'signature': sign,
                'message':msg
                }
    request = GetRequest(server, postdata)
    print(request)

def queryuser(key):
    '''key: hex'''
    postdata = {'action': 'queryuser',
                'key': key
                }
    request = GetRequest(server, postdata)
    print(request)
