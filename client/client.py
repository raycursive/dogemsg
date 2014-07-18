from binascii import unhexlify
from pyelliptic.ecc import ECC
from key import load_keypair
from postrec import testsend

class user(object):
    """docstring for user"""
    def __init__(self, account):
        self.ecc, keypair = load_keypair(account)
        self.pubkey = keypair['public_key']
        self.privkey = keypair['private_key']
        #add more

    def send_message(self, keyto, message):
        encrypted_msg = self.ecc.encrypt(message, keyto) 
        signature = self.ecc.sign(message)
        testsend(self.pubkey, keyto, signature, encrypted_msg)

    def recieve_message(self, des, key):
        signature = self.ecc.sign(key)
        msg = testreceive(des, key, signature)


