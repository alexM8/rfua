#!/usr/bin/env python3
'''
Raiffaisen API is very unstable
Not every request is served correcty
That's why every request has for loop with retry count
'''
import requests, json
from .. import config, credentials
from ..functions import logger


class RFSession():
    def __init__(self):
        self.LogIn()
        self.refreshCards()
        self.refreshAccounts()
        self.refreshHistory()
        self.refreshHolds()

    def makeRFRequest(self, type, url, cookies = None, params = None, data = json.dumps(credentials.string)):
        if type == 'post':
            result = requests.post(url, data, headers = config.Headers, cookies = cookies)
        elif type == 'get':
            result = requests.get(url, params, headers = config.Headers, cookies = cookies)
        else: result = None
        return result

    def CheckForVaidResponse(self, result):
        logger.writeLog(result)
        if result.json()['ResponseCode'] == '000':
            return True
        else:
            return False

    def LogIn(self):
        for i in range(0, config.Timeout):
            self.Info = self.makeRFRequest('post', config.LoginUrl + "LogOn")
            if self.CheckForVaidResponse(self.Info):
                self.cookies = self.Info.cookies.get_dict()
                break
        raise Exception('LogIn Failed')

    def refreshCards(self):
        for i in range(0, config.Timeout):
            self.Cards = self.makeRFRequest('get', config.Url + "CardAccountList", cookies = self.cookies)
            if self.CheckForVaidResponse(self.Cards):
                self.params = {"uniqueKey": self.Cards.json()["Result"][0]['UniqueKey']}
                break
        raise Exception('Cards Fetching Failed')

    def refreshAccounts(self):
        for i in range(0, config.Timeout):
            self.Accounts = self.makeRFRequest('get', config.Url + "DebitCardAccountData",
                                               cookies = self.cookies, params = self.params)
            if self.CheckForVaidResponse(self.Accounts):
                break
        raise Exception('Accounts Fetching Failed')

    def refreshHolds(self):
        for i in range(0, config.Timeout):
            self.Holds = self.makeRFRequest('get', config.Url + "HoldList", cookies = self.cookies,
                                               params = self.params)
            if self.CheckForVaidResponse(self.Holds):
                break
        raise Exception('Holds Fetching Failed')

    def refreshHistory(self):
        for i in range(0, config.Timeout):
            self.History = self.makeRFRequest('get', config.Url + "ExecutedCardOperationList",
                                              cookies = self.cookies, params = self.params)
            if self.CheckForVaidResponse(self.History):
                break
        raise Exception('History Fetching Failed')