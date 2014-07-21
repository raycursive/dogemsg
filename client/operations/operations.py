import json
import urllib.request
import urllib.parse
from parse import parsemsg, msgdumps
from friendlist import add_contact_to_friend_list,
from randomstr import random_str
from hexparse import tohex, unhex

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


def receive(key, unread=1):
    '''key: ECC'''
    postdata = {'action': 'receive',
                'key': tohex(key.get_pubkey()),
                'unread': unread
                }
    request = GetRequest(server, postdata)
    result = []
    for i in unhex(json.loads(request)):
        i['message'] = key.decrypt(i['message'])
        if ECC(pubkey=i['from']).verify(i['signature'], i['message']):
            i['message'] = i['message'].decode()
            result.append(i)
        else:
            print("ERROR! Verify Failed!")
    for i in result:
        print(parsemsg(i))
    return result


def send(keyfrom, keyto, message):
    '''keyfrom : ECC keyto : hex address'''
    message = msgdumps(message)
    postdata = {'action': 'send',
                'from': tohex(keyfrom.get_pubkey()),
                'to': keyto,
                'signature': tohex(keyfrom.sign(message)),
                'message': tohex(keyfrom.encrypt(message, unhex(keyto)))
                }
    request = GetRequest(server, postdata)
    return json.loads(request)


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
    return json.loads(request)


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
    return json.loads(request)


def modifyuser(key, name='Anonymous', email=' '):
    msg = random_str()
    sign = tohex(key.sign(msg))
    postdata = {'action': 'modifyuser',
                'key': tohex(key.get_pubkey()),
                'name': name,
                'email': email,
                'signature': sign,
                'message': msg
                }
    request = GetRequest(server, postdata)
    return json.loads(request)


def queryuser(key):
    '''key: hex'''
    postdata = {'action': 'queryuser',
                'key': key
                }
    request = GetRequest(server, postdata)
    return json.loads(request)


def addfriend(friends_key, filename, alias=''):
    friend = queryuser(friends_key)
    add_contact_to_friend_list(friend, alias=alias, filename=filename)


def postfriendlist(key, filename):
    '''filename is the user filename'''
    pubkey = key.get_pubkey()
    encry_friendlist = key.encrypt(
        json.dumps(load_friend_list(filename)), pubkey)
    postdata = {'action': 'postfriendlist',
                'key': tohex(pubkey),
                'signature': key.sign(encry_friendlist),
                'message': encry_friendlist}
    request = GetRequest(server, postdata)
    return json.loads(request)


def fetchfriendlist(key, filename):
    '''return encrypted friendlist'''
    pubkey = key.get_pubkey()
    postdata = {'action': 'fetchfriendlist',
                'key': tohex(pubkey)}
    request = GetRequest(server, postdata)
    return json.loads(request)
