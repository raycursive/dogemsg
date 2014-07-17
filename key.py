from pyelliptic.ecc import ECC

def parsekey(key):
    return "".join([hex(i)[2:] for i in key]).upper()
    
