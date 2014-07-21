from pyelliptic.ecc import ECC
from hexparse import unhex
import json
import os
import sys

os.chdir(os.path.join(os.path.dirname(sys.argv[0]), os.pardir))


def load_friend_list(filename='default'):
    with open('accounts/' + filename + '/friendlist.dat') as f:
        friendlist = json.loads(f.read())
    return friendlist


def add_contact_to_friend_list(contact, alias='', filename='default'):
    with open('accounts/' + filename + '/friendlist.dat', 'r+') as f:
        friendlist = json.loads(f.read())
        friendlist[contact['key']] = {'name': contact['name'],
                                      'email': contact['email'],
                                      'alias': alias}
        f.write(json.dumps(friendlist))


def modify_friend():
    pass