from pyelliptic.ecc import ECC
from hexparse import unhex
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
    keypair = {'public_key': parsekey(key.get_pubkey()),
               'private_key': parsekey(key.get_privkey())
               }
    with open('accounts/' + filename + '/key.dat', 'w') as f:
        f.write(json.dumps(keypair))
