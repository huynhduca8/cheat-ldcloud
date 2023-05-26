from encrypt import md5
from datetime import datetime
from encrypt import get_mid, get_uuid
from file import read_file, write_file
import time
import requests
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
def pre_login(session, username, password):
    url = "https://usersdk.ldmnq.com/user/login"
    data = {
        "appId": "8889",
        "auth": md5(password),
        "email": username,
        "loginMode": "USERNAME",
        "mainChannelId": "0",
        "mid": get_mid(),
        "phoneBrand": "0",
        "phoneModel": "0",
        "subChannelId": "0",
        "time": get_current_time()
    }
    data['sign'] = md5(data).upper()
    req = session.post(url, json = data).json()
    try:
        uid = req['data']['uid']
        token = req['data']['token']
        return {
            "uid": uid,
            "token": token
        }
    except Exception as e:
        # if req and req['code'] == 60001:
        time.sleep(3)
        print("EMAIL", username, "REPRELOGINING")
        return pre_login(session, username, password)
    return False
def login(session, username, password):
    result_pre_login = pre_login(session, username, password)
    if not result_pre_login:
        print(username, "Login failed")
        return
    uid = result_pre_login['uid']
    token = result_pre_login['token']
    url = "https://poly.ldcloud.net/api/user/login"
    data = {
        "pltType": 5,
        "appId": 8888,
        "channelId": 10400,
        "pchannelId": 10401,
        "accessToken": token,
        "locale": "en_US",
        "pltUid": int(uid),
        "uuid": get_uuid()
    }
    req = session.post(url, data = data).json()
    try:
        uid = req['data']['uid']
        token = req['data']['token']
        return {
            "uid": uid,
            "token": token
        }
    except Exception as e:
        if req and req['code'] == 60001:
            time.sleep(1.5)
            print("EMAIL", username, "RELOGINING")
            return pre_login(session, username, password)
        else:
            print(username, 'Login error', e, req)
    return False
def send_email(session, email):
    url = "https://usersdk.ldmnq.com/user/sendEmail"
    data = {
        "appId":"8889",
        "email": email,
        "pwd":"d41d8cd98f00b204e9800998ecf8427e",
        "sendType":"reg",
    }
    data['sign'] = md5(data).upper()
    req = session.post(url, json = data).json()
    try:
        print(email, 'Send message success')
        return req['code'] == 200
    except Exception as e:
        print(email, 'Send message error', e)
    return False
def verify_register(session, email, password, otp):
    url = "https://usersdk.ldmnq.com/user/login"
    data = {
        "appId":"8889",
        "auth": otp,
        "email": email,
        "loginMode": "EMAIL",
        "mainChannelId": "0",
        "mid": get_mid(),
        "phoneBrand": "0",
        "phoneModel": "0",
        "pwd": md5(password),
        "subChannelId": "0",
        "time": get_current_time()
    }
    data['sign'] = md5(data).upper()
    req = session.post(url, json = data).json()
    try:
        result = {
            "uid": req['data']['uid'],
            "token": req['data']['token']
        }
        print(email, 'Verify success')
        return result
    except Exception as e:
        print(email, 'Verify error', e)
    return False