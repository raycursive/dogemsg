import sys
from pyelliptic.ecc import ECC



try :
    public_key = sys.argv[1]
    signature = sys.argv[2]
    msg = sys.argv[3]
    print(ECC(pubkey = bytes.fromhex(public_key)).verify(bytes.fromhex(signature), msg), end = "")
except:
    print(False, end = "")


