from pyelliptic.ecc import ECC
from binascii import hexlify, unhexlify
import json


def tohex(key):
    return hexlify(key).decode().upper()


def generate_keypair(filename='defalut'):
    save_keypair(ECC(), filename)


def load_ECC(filename='default'):
    with open('keys/' + filename + '.key') as f:
        keypair = json.loads(f.read())
    return ECC(pubkey=unhexlify(keypair["public_key"]),
               privkey=unhexlify(keypair["private_key"]))


def save_keypair(key, filename):
    keypair = {'public_key': parsekey(key.get_pubkey()),
               'private_key': parsekey(key.get_privkey())
               }
    with open('keys/' + filename + '.key', 'w') as f:
        f.write(json.dumps(keypair))

