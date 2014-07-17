from pyelliptic.ecc import ECC
import json

def parsekey(key):
    return ''.join(['%02x' % i for i in key ]).upper()
    
def generate_keypair(filename = 'account'):
	key = ECC()
	keypair = {'public_key' : parsekey(key.get_pubkey()),
                   'private_key' : parsekey(key.get_privkey())
                   }
	with open('keys/' + filename + '.key', 'w') as f:
		f.write(json.dumps(keypair))

def load_keypair(filename = 'account'):
    with open('keys/' + filename + '.key') as f:
        keypair = json.loads(f.read())
    return ECC(pubkey = bytes.fromhex(keypair["public_key"]),
               privkey = bytes.fromhex(keypair["private_key"]))

