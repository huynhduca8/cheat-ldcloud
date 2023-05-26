import requests
import time
import json
from threading import Thread
from login_controler import login 
from encrypt import get_mid
from multiprocessing.pool import ThreadPool
from file import read_file, write_file
class Cheat:
    def __init__(self, acc, is_account = False, is_renew = False):
        proxies = {
            'http': 'socks4://127.0.0.1:10808',
            'https': 'socks4://127.0.0.1:10808'
        }
        session = requests.Session()
        # session.proxies.update(proxies)
        self.session = session
        if is_account:
            result = login(session, acc['email'], acc['password'])
            if result:
                self.email = acc['email']
                self.uid = result['uid']
                self.token = result['token']
            else:
                print("USERNAME", acc['email'], "LOGIN FAILED")
                return
        else:
            self.uid = acc['uid']
            self.token = acc['token']
            self.email = acc['email']
        self.is_renew = is_renew
        self.mid = get_mid()
        self.time = int(time.time() * 1000)
        try:
            if self.uid:
                acc['uid'] = self.uid
                acc['token'] = self.token
                write_file('acc.json', accounts)
            self.main()
        except Exception as e:
            print('EMAIL', '%-30s' % self.email, 'SOMETHING WENT WRONG', e)
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
    def get_diamond(self):
        url = "https://ldq.ldcloud.net/api/en/wallet/my"
        params = {
            "uid": self.uid,
            "token": self.token
        }
        req = self.session.post(url, params=params).json()
        print(req)
        try:
            return req['data']['usableDiamond']
        except Exception as e:
            pass
        return 0
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
            "mid": self.mid,
            "ver": 1
        }
        req = self.session.post(url, params=params).json()
        try:
            if(req['code'] == 0):
                return self.get_money(package_name)
            raise Exception(req['msg']) 
        except Exception as e:
            print('EMAIL', '%-30s' % self.email, '%-25s' % "INSTALL FAILED", e)
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
                print('EMAIL', '%-30s' % self.email, '%-25s' % "INSTALL GAME SUCCESS", package_name, "DIAMON", req['data']['usableDiamond'])
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
            status = req['data']['status'] == 1
            if status:
                print('EMAIL', '%-30s' % self.email, 'RECEIVED 0.27$')
                return status
            raise Exception()
        except Exception as e:
            print('EMAIL', '%-30s' % self.email, 'CAN\'T RECEIVE 0.27$', req)
        return False
    
    def pre_buy_device(self):
        url = "https://ldq.ldcloud.net/api/en/cph/device/buy"
        params = {
            "uid": self.uid,
            "token": self.token,
            "priceId": 1961,
            "num": 1,
            "area": "tw"
        }
        req = self.session.post(url, params=params).json()
        try:
            return req['data']['id']
        except Exception as e:
            pass
        return False
    def buy_device(self):
        order_id = self.pre_buy_device()
        if not order_id:
            print('EMAIL', '%-30s' % self.email, 'CAN\'T BUY A DEVICE')
            return False
        url = "https://ldq.ldcloud.net/api/en/wallet/pay"
        params = {
            "uid": self.uid,
            "token": self.token,
            "orderId": order_id
        }
        req = self.session.post(url, params=params).json()
        try:
            status = req['code'] == 0
            if status:
                print('EMAIL', '%-30s' % self.email, 'BOUGHT A DEVICE')
            return status
        except Exception as e:
            print('EMAIL', '%-30s' % self.email, 'CAN\'T BUY A DEVICE', req)
        return False
    def get_coin(self):
        url = "https://ldq.ldcloud.net/api/en/reward/diamond/my"
        params = {
            "uid": self.uid,
            "token": self.token
        }
        req = self.session.post(url, params=params).json()
        try:
            print('EMAIL', '%-30s' % self.email,'COIN', req['data']['usableDiamond'])
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
            print('EMAIL', '%-30s' % self.email, 'DOESN\'T HAVE A DEVICE', e)
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
                print('EMAIL', '%-30s' % self.email, 'EXCHANGE SUCCESS')
            return req['code']
        except Exception as e:
            print('EMAIL', '%-30s' % self.email, 'EXCHANGE FAILED', e)
        return False
    def main(self):
        if not self.uid:
            return
        print('EMAIL', '%-30s' % self.email, 'STARTING')
        device_id = 0
        if self.is_renew:
            device_id = self.get_first_device()
            if(device_id == 0):
                if self.get_diamond() == 0:
                    self.get_dolar()
                self.buy_device()
                device_id = self.get_first_device()
        while True:
            games = self.get_list_games()
            if len(games) == 0:
                print('EMAIL', '%-30s' % self.email, "DOESN\'T HAVE ANY GAMES")
                break
            self.install_game(games[0])
            if(device_id > 0):
                while self.get_coin() >= 400:
                    self.exchange_20p(device_id)
                    time.sleep(1)
            time.sleep(1)
def run(acc):
    Cheat(acc, 'token' not in acc)

f_accounts = open('acc.json')
accounts = json.load(f_accounts)
if __name__ == '__main__':
    pool = ThreadPool(100)
    results = pool.map(run, accounts)