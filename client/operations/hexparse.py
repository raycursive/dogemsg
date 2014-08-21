from binascii import hexlify, unhexlify


def tohex(data):
    return hexlify(data).decode().upper()


def unhex(data):
    if type(data) == str:
        return unhexlify(data)
    elif type(data) == list:
        return [unhexlify(item) for item in data]
    elif type(data) == dict:
        return {key: unhexlify(data[key]) for key in data.keys()}
    else:
        raise TypeError('Input data must be a string, list or dictionary.')
