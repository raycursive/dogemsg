import json
import os
import sys
from parse import parsemsg
from friendlist import Friendlist
from functools import reduce

#just for test
#implimenting loading Friendlist from path of global config
friendlist = Friendlist()

os.chdir(os.path.join(os.path.dirname(sys.argv[0]), os.pardir))

class Msglog():

    def __init__(self, filename = 'default'):
        self.filename = filename
        with open('accounts/' + filename + '/msglog.dat') as f:
            self.data = json.loads(f.read())

    def getlog(self, key):
        logs = self.data[key]
        contact = friendlist.getcontact(key)
        if contact['alias'] != '':
            contact['name'] += " (" + contact['alias'] + ")"
        header = "====================================\n" + \
                  contact['name'] + "\t" + contact['email'] + \
                  "\n====================================\n"
        messages = "".join((msg['time']+'\n'+msg['message']+'\n\n' for msg in logs))
        return header + messages

    def addlog(self, key, time, message):
        if not key in self.data:
            self.data[key] = []
        self.data[key].append({'time' : time,
                               'message' : message})


    def addlogfrommeta(self, array):
        for dic in array:
            self.addlog(dic['from'], dic['time'], dic['message'])

    def __repr__(self):
        return reduce(lambda a,b: a+b, (self.getlog(key) for key in self.data),"")


