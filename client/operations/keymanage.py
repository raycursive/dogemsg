from pyelliptic.ecc import ECC
from hexparse import unhex, tohex
import json
import os
import sys

os.chdir(os.path.join(os.path.dirname(sys.argv[0]), os.pardir))


def generate_keypair(filename='defalut'):
    save_keypair(ECC(), filename)


def load_ECC(filename='default'):
    with open('accounts/' + filename + '/key.dat') as f:
        keypair = json.loads(f.read())
    return ECC(pubkey=unhex(keypair["public_key"]),
               privkey=unhex(keypair["private_key"]))


def save_keypair(key, filename):
    keypair = {'public_key': tohex(key.get_pubkey()),
               'private_key': tohex(key.get_privkey())
               }
    if not os.path.exists('accounts/'+filename):
        os.mkdir('accounts/'+filename)
    with open('accounts/' + filename + '/key.dat', 'w') as f:
        f.write(json.dumps(keypair))
    with open('config.json') as g:
        config = json.loads(g.read())
        config['saved_path'].append(filename)
    with open('config.json', 'w') as g:
        g.write(json.dumps(config))
    #need to reload settings
