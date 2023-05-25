import requests
import time
uid = "2500230505221557"
token = "321db0cee2353f3d826222c914c971db"
class Cheat:
    def __init__(self, uid, token):
        self.uid = uid
        self.token = token
        self.time = int(time.time() * 1000 + 2e9)
    def getTime(self):
        self.time = int(self.time + 1e9)
        return self.time
    def getListGames(self):
        url = "https://ldq.ldcloud.net/api/en/user/reward/download/ext"
        params = {
            "uid": self.uid,
            "token": self.token
        }
        req = requests.post(url, params=params).json()
        try:
            return req['data']['specify']
        except:
            return []
    def installGame(self, packageName, partner, regionCode):
        url = "https://ldq.ldcloud.net/api/en/user/reward/download"
        params = {
            "uid": self.uid,
            "token": self.token,
            "nonce": self.getTime(),
            "partner": partner,
            "regionCode": regionCode,
            "packageName": packageName,
            "mid": "999985bd600c610",
            "ver": 1
        }
        print params['nonce']
        req = requests.post(url, params=params).json()
        try:
            print req
            if(req['code'] == 0):
                return self.getMoney()
        finally:
            return False
    def getMoney(self):
        url = "https://ldq.ldcloud.net/api/en/reward/diamond/my"
        params = {
            "uid": self.uid,
            "token": self.token
        }
        req = requests.post(url, params=params).json()
        try:
            print req
            return req['code'] == 0
        finally:
            return False
    def getDolar(self):
        url = "https://ldq.ldcloud.net/api/en/reward/diamond/my"
        params = {
            "uid": self.uid,
            "token": self.token
        }
        req = requests.post(url, params=params).json()
        try:
            print req
            return req['code'] == 0
        finally:
            return False
    def main(self):
        games = self.getListGames()
        if(len(games)):
            for game in games[:3]:
                print game['packageName']
                self.installGame(game['packageName'], game['partner'], game['regionCode'])
import time

cheat = Cheat(uid, token)
cheat.main()