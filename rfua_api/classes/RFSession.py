#!/usr/bin/env python3
'''
Raiffaisen API is very unstable
Not every request is served correcty
That's why every request has for loop with retry count
'''
import requests, json
from .. import config, credentials
from ..functions import validation


class RFSession():
    def __init__(self):
        try:
            self.LogIn()
            self.refreshCards()
            self.refreshAccounts()
            self.refreshHistory()
            self.refreshHolds()
        except:
            print("Initialization failed")
            print(Exception)

    def Request(self, type, url, cookies = None, params = None, data = json.dumps(credentials.string)):
        if type == 'post':
            result = requests.post(url, data, headers = config.Headers, cookies = cookies)
        elif type == 'get':
            result = requests.get(url, params, headers = config.Headers, cookies = cookies)
        else: result = None
        return result

    def LogIn(self):
        for i in range(0, config.Timeout):
            self.Info = self.Request('post', config.LoginUrl + "LogOn")
            if validation.CheckForVaidResponse(self.Info):
                self.cookies = self.Info.cookies.get_dict()
                return True
        raise Exception('LogIn Failed')

    def refreshCards(self):
        for i in range(0, config.Timeout):
            self.Cards = self.Request('get', config.Url + "CardAccountList", cookies = self.cookies)
            if validation.CheckForVaidResponse(self.Cards):
                self.params = {"uniqueKey": self.Cards.json()["Result"][0]['UniqueKey']}
                return True
        raise Exception('Cards Fetching Failed')

    def refreshAccounts(self):
        for i in range(0, config.Timeout):
            self.Accounts = self.Request('get', config.Url + "DebitCardAccountData",
                                               cookies = self.cookies, params = self.params)
            if validation.CheckForVaidResponse(self.Accounts):
                return True
        raise Exception('Accounts Fetching Failed')

    def refreshHolds(self):
        for i in range(0, config.Timeout):
            self.Holds = self.Request('get', config.Url + "HoldList", cookies = self.cookies,
                                               params = self.params)
            if validation.CheckForVaidResponse(self.Holds):
                return True
        raise Exception('Holds Fetching Failed')

    def refreshHistory(self):
        for i in range(0, config.Timeout):
            self.History = self.Request('get', config.Url + "ExecutedCardOperationList",
                                              cookies = self.cookies, params = self.params)
            if validation.CheckForVaidResponse(self.History):
                return True
        raise Exception('History Fetching Failed')
