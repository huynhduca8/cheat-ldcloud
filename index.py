import requests
import time
import json
from threading import Thread
from login_register import login 
from encrypt import get_mid
from multiprocessing.pool import ThreadPool
class Cheat:
    def __init__(self, p1, p2, is_account = False):
        proxies = {
            'http': 'socks4://127.0.0.1:10808',
            'https': 'socks4://127.0.0.1:10808'
        }
        session = requests.Session()
        # session.proxies.update(proxies)
        self.session = session
        if is_account:
            result = login(session, p1, p2)
            if result:
                self.uid = result['uid']
                self.token = result['token']
            else:
                print("USERNAME", p1, "LOGIN FAILED")
                return
        else:
            self.uid = p1
            self.token = p2
        self.mid = get_mid()
        self.time = int(time.time() * 1000)
        self.main()
    def get_time(self):
        self.time = int(self.time + 1e5)
        return self.time
    def handle_games(self, games, installed_games):
        games_result = []
        for game in games:
            if(game['packageName'] not in installed_games):
                games_result.append(game)
                installed_games.append(game['packageName'])
        return games_result
    def get_list_games(self):
        url = "https://ldq.ldcloud.net/api/en/user/reward/download/ext"
        params = {
            "uid": self.uid,
            "token": self.token
        }
        req = self.session.post(url, params=params).json()
        try:
            return self.handle_games(req['data']['specify'], req['data']['packageLogs'] or [])
        except Exception as e:
            print('get_list_games', e)
        return []
    def remove_duplicate_game(self, games):
        gameTemps = []
        gameTemp = ''
        for game in games:
            gameTemp = game['']
    def install_game(self, game):
        package_name = game['packageName']
        partner = game['partner']
        region_code = game['regionCode']
        url = "https://ldq.ldcloud.net/api/en/user/reward/download"
        params = {
            "uid": self.uid,
            "token": self.token,
            "nonce": 0,
            "partner": partner,
            "regionCode": region_code,
            "packageName": package_name,
            "mid": 0,
            "ver": 1
        }
        req = self.session.post(url, params=params).json()
        try:
            if(req['code'] == 0):
                return self.get_money(package_name)
            raise Exception(req['msg']) 
        except Exception as e:
            print("UID", self.uid, "INSTALL FAILED", e)
        return False
    def get_money(self, package_name):
        url = "https://ldq.ldcloud.net/api/en/reward/diamond/my"
        params = {
            "uid": self.uid,
            "token": self.token
        }
        req = self.session.post(url, params=params).json()
        try:
            is_success = req['code'] == 0
            if is_success:
                print("UID", self.uid, "INSTALL GAME SUCCESS", package_name, "DIAMON", req['data']['usableDiamond'])
            return is_success
        except Exception as e:
            print('get_money', e)
        return False
    def get_dolar(self):
        url = "https://ldq.ldcloud.net/api/en/user/reward/regist"
        params = {
            "uid": self.uid,
            "token": self.token,
            "mid": self.mid
        }
        req = self.session.post(url, params=params).json()
        try:
            return req['code'] == 0
        except Exception as e:
            print('get_dolar', e)
        return False
    def buy_device(self):
        url = "https://ldq.ldcloud.net/api/en/cph/device/buy"
        params = {
            "uid": self.uid,
            "token": self.token,
            "priceId": 1781,
            "num": 1,
            "area": "sg"
        }
        req = self.session.post(url, params=params).json()
        try:
            print(req)
            return req['data']['id']
        except Exception as e:
            print('buy_device', e)
        return False
    def get_coin(self):
        url = "https://ldq.ldcloud.net/api/en/reward/diamond/my"
        params = {
            "uid": self.uid,
            "token": self.token
        }
        req = self.session.post(url, params=params).json()
        try:
            print('UID', self.uid,'COIN', req['data']['usableDiamond'])
            return req['data']['usableDiamond']
        except Exception as e:
            print('get_coin', e)
        return 0
    def get_first_device(self):
        url = "https://ldq.ldcloud.net/api/en/cph/device/my-device"
        params = {
            "uid": self.uid,
            "token": self.token,
            "size": 1000,
            "current" : 1,
            "cardType" : 0,
            "groupId" : -1,
            "orderby" : 2
        }
        req = self.session.post(url, params=params).json()
        try:
            return req['data']['records'][0]['deviceId']
        except Exception as e:
            print("UID", self.uid, 'DOESN\'T HAVE A DEVICE', e)
        return 0
    def exchange_20p(self, device_d):
        url = "https://ldq.ldcloud.net/api/en/reward/diamond/exchange"
        params = {
            "uid": self.uid,
            "token": self.token,
            'prizeId': 2,
            'deviceId': device_d
        }
        req = self.session.post(url, params=params).json()
        try:
            if req['code'] == 0:
                print("UID", self.uid, 'EXCHANGE SUCCESS')
            return req['code']
        except Exception as e:
            print("UID", self.uid, 'EXCHANGE FAILED', e)
        return False
    def main(self):
        if not self.uid:
            return
        print('START', self.uid)
        games = self.get_list_games()
        if len(games) == 0:
            print("UID", self.uid, "DOESN\'T HAVE ANY GAMES")
            return
        device_id = self.get_first_device()
        if(len(games)):
            for game in games:
                self.install_game(game)
                if(device_id > 0):
                    while self.get_coin() >= 400:
                        self.exchange_20p(device_id)
                        time.sleep(1)
                time.sleep(660)
def run(acc):
    if 'uid' in acc:
        Cheat(acc['uid'], acc['token'])
    elif 'email' in acc:
        Cheat(acc['email'], acc['password'], True)
if __name__ == '__main__':
    f_accounts = open('accounts.json')
    accounts = json.load(f_accounts)
    pool = ThreadPool(8)
    results = pool.map(run, accounts)