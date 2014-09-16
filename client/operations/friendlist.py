import json
import os
import sys
from hexparse import tohex, unhex
os.chdir(os.path.join(os.path.dirname(sys.argv[0]), os.pardir))

class Friendlist():
    def __init__(self, filename = 'default'):
        self.filename = filename
        with open('accounts/' + filename + '/friendlist.dat') as f:
            self.data = json.loads(f.read())

    def __repr__(self):
        return json.dumps(self.data)

    def saveto(self, filename):
        with open('accounts/' + filename + '/friendlist.dat','w') as f:
            f.write(json.dumps(self.data))
        self.filename = filename

    def save(self):
        self.saveto(self.filename)

    def addcontact(self, contact, alias=''):
        self.data[contact['key']] = {'name': contact['name'],
                                     'email': contact['email'],
                                     'alias': alias}
        self.save()

    def modifyalias(self, key, alias = ''):
        friendlist[key]['alias'] = alias

    def deletecontact(self, key):
        del self.data[key]

    def getcontact(self, key):
        if key in self.data:
            return self.data[key]
        else:
            return {'name':key, 'alias':'', 'email':''}


##def load_friend_list(filename='default'):
##    with open('accounts/' + filename + '/friendlist.dat') as f:
##        friendlist = json.loads(f.read())
##    return friendlist
##
##def save_friend_list(friendlist,filename='default'):
##    with open('accounts/' + filename + '/friendlist.dat','w') as f:
##        f.write(json.dumps(friendlist))
##
##def add_contact_to_friend_list(contact, friendlist, alias=''):
##    friendlist[contact['key']] = {'name': contact['name'],
##                                  'email': contact['email'],
##                                  'alias': alias}
##    save_friend_list(friendlist)
##
##
##def modify_alias(key, friendlist, name = '', email = '', alias = ''):
##    friendlist['key'] = {'name': name,
##                         'email': email,
##                         'alias': alias}
##    save_friend_list(friendlist)
def addfriend(friendlist, friends_key, alias=''):
    from operations import queryuser
    friendlist.addcontact(queryuser(friends_key),alias)

def updatefriend(friendlist, friends_key):
    from operations import queryuser
    addfriend(friendlist, friends_key, friendlist.getcontact(friends_key)['alias'])

def updatefromserver(friendlist):
    from operations import fetchfriendlist
    from keymanage import load_ECC
    fetched = fetchfriendlist(load_ECC(friendlist.filename))
    for key in fetched:
        friendlist.data[key].update(fetched[key])





