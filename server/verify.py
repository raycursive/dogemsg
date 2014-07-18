import sys
from binascii import unhexlify
from pyelliptic.ecc import ECC


try:
    public_key = sys.argv[1]
    signature = sys.argv[2]
    msg = sys.argv[3]
    print(ECC(pubkey=unhexlify(public_key)).verify(
        unhexlify(signature), msg), end="")
except:
    print(False, end="")
