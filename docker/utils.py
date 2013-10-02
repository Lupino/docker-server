import hashlib

def md5sum(*args):
    h = hashlib.md5()
    args = map(lambda x: bytes(x, 'utf-8'), args)
    for arg in args:
        h.update(arg)
    key = h.hexdigest()
    return key

