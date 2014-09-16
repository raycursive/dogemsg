from keymanage import *
from operations import *
from friendlist import *
from msglog import *

os.chdir(os.path.join(os.path.dirname(sys.argv[0]), os.pardir))

def load_settings():
    with open("config.json") as f:
        settings = json.loads(f.read())
    return settings


class user(object):

    """docstring for user"""

    def __init__(self, account):
        self.ecc = load_ecc(account)


if __name__ == '__main__':
    settings = load_settings()
    key = load_ECC(settings['current_path'])
    friendlist = Friendlist(settings['current_path'])
    msglog = Msglog(settings['current_path'])
    
