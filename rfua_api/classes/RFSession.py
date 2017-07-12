#!/usr/bin/env python3
"""
Raiffaisen API is very unstable
Not every request is served correcty
That's why every request has for loop with retry count
"""
import requests
import json
from .. import config
from .. import credentials
from .. import validation


class RFSession:
    def __init__(self):
        self.authorize()
        self.refresh_cards()
        self.refreshHistory()
        self.refresh_holds()

    def do_request(self, type, url, cookies = None, params = None, data = json.dumps(credentials.string)):
        if type == 'post':
            result = requests.post(url, data, headers = config.Headers, cookies = cookies)
        elif type == 'get':
            result = requests.get(url, params, headers = config.Headers, cookies = cookies)
        else: result = None
        return result

    def authorize(self):
        for i in range(0, config.Timeout):
            self.Info = self.do_request('post', config.LoginUrl + "LogOn")
            if validation.CheckForVaidResponse(self.Info):
                self.cookies = self.Info.cookies.get_dict()
                return True
        raise Exception('LogIn Failed')

    def refresh_cards(self):
        for i in range(0, config.Timeout):
            self.Cards = self.do_request('get', config.Url + "CardAccountList", cookies = self.cookies)
            if validation.CheckForVaidResponse(self.Cards):
                self.params = {"uniqueKey": self.Cards.json()["Result"][0]['UniqueKey']}
                return True
        raise Exception('Cards Fetching Failed')

    def refresh_holds(self):
        for i in range(0, config.Timeout):
            self.Holds = self.do_request('get', config.Url + "HoldList", cookies = self.cookies,
                                         params = self.params)
            if validation.CheckForVaidResponse(self.Holds):
                return True
        raise Exception('Holds Fetching Failed')

    def refreshHistory(self):
        for i in range(0, config.Timeout):
            self.History = self.do_request('get', config.Url + "ExecutedCardOperationList",
                                           cookies = self.cookies, params = self.params)
            if validation.CheckForVaidResponse(self.History):
                return True
        raise Exception('History Fetching Failed')
