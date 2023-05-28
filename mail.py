import requests
import re
def get_email():
    url = "https://www.1secmail.com/api/v1/"
    params = {
        "action": "genRandomMailbox",
        "count": 1
    }
    try:
        req = requests.get(url, params=params).json()
        return req[0]
    except:
        return None
def pre_get_message(email):
    url = "https://www.1secmail.com/api/v1/"
    params = {
        "action": "getMessages",
        "login": email.split('@')[0],
        "domain": email.split('@')[1]
    }
    try:
        req = requests.get(url, params=params).json()
        if req[0]['from'] == 'no-reply@email.ldcloud.net':
            return req[0]['id']
    except:
        return None
def get_message(email):
    while True:
        _id = pre_get_message(email)
        if _id:
            break
    url = "https://www.1secmail.com/api/v1/"
    params = {
        "action": "readMessage",
        "login": email.split('@')[0],
        "domain": email.split('@')[1],
        "id": _id
    }
    try:
        req = requests.get(url, params=params).json()
        html = req['htmlBody']
        return re.findall('\s(\d{6})\s', html)[0]
    except Exception as e:
        print('Except', e)
        return None