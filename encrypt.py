import hashlib
import json
import random
import string
import uuid
def md5( data):
    return hashlib.md5(json.dumps(data, separators=(',', ':')).encode('utf-8')).hexdigest()
def get_mid():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
def get_uuid():
    return uuid.uuid1().hex.upper()