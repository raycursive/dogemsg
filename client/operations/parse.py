import json
from hexparse import unhex


def msgdumps(string):
    result = {"type": "message",
              "message": string
              }
    return json.dumps(result)


def msgloads(string):
    result = json.loads(string)
    return result['message']

def parsemsg(data):
    proc = ['message', 'signature']
    for info in data:
        for meta in proc:
            info[meta] = unhex(info[meta])
    return data


# def parsemsg(req):
#     time = req['time']
#     message = msgloads(req['message'])
#     contact = friendlist.getcontact(req['from'])
#     contact_name = contact['name']
#     if 'alias' in contact:
#         contact_name += " (" + contact['alias'] + ")"
#     return "====================================\n" +\
#         contact_name + "\t" + time + \
#         "\n====================================\n\t" +\
#         message

# load userinfo from local file(if possible)(still implementing)

##
##def getuserinfo(key):
##    data = queryuser(key)  # it shoule be replaced to the method of friendlist
##    return data
