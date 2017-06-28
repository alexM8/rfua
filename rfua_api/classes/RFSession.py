#!/usr/bin/env python3
'''
Raiffaisen API is very unstable
Not every request is served correcty
That's why every request has for loop with retry count
'''
import requests, json
from .. import config, credentials


class RFSession():
    def __init__(self):
        self.log = []
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

    def Log(self, request):
        LogEntry = request.json()
        LogEntry['Destination'] = request.request.url
        LogEntry['HTTPResponseCode'] = request.status_code
        LogEntry['TotalSeconds'] = request.elapsed.total_seconds()
        Extrafields = 'Result', 'ShowAlert', 'AlertMessage'
        for field in Extrafields:
            del LogEntry[field]
        self.log.append(LogEntry)

    def CheckForVaidResponse(self, result):
        self.Log(result)
        if result.json()['ResponseCode'] == '000':
            return True
        else:
            return False

    def LogIn(self):
        for i in range(0, config.Timeout):
            self.Info = self.makeRFRequest('post', config.LoginUrl + "LogOn")
            if self.CheckForVaidResponse(self.Info):
                break
        self.cookies = self.Info.cookies.get_dict()

    def refreshCards(self):
        for i in range(0, config.Timeout):
            self.Cards = self.makeRFRequest('get', config.Url + "CardAccountList", cookies = self.cookies)
            if self.CheckForVaidResponse(self.Cards):
                break
            if self.Cards.json()["Result"] == None:
                self.LogIn()
        self.params = {"uniqueKey": self.Cards.json()["Result"][0]['UniqueKey']}

    def refreshAccounts(self):
        for i in range(0, config.Timeout):
            self.Accounts = self.makeRFRequest('get', config.Url + "DebitCardAccountData",
                                               cookies = self.cookies, params = self.params)
            if self.CheckForVaidResponse(self.Accounts):
                break

    def refreshHolds(self):
        for i in range(0, config.Timeout):
            self.Holds = self.makeRFRequest('get', config.Url + "HoldList", cookies = self.cookies,
                                               params = self.params)
            if self.CheckForVaidResponse(self.Holds):
                break

    def refreshHistory(self):
        for i in range(0, config.Timeout):
            self.History = self.makeRFRequest('get', config.Url + "ExecutedCardOperationList",
                                              cookies = self.cookies, params = self.params)
            if self.CheckForVaidResponse(self.History):
                break

    def __del__(self):
        for i in range(0, config.Timeout):
            self.LogOff = self.makeRFRequest('post', config.LoginUrl + "LogOff", cookies = self.cookies)
            if self.CheckForVaidResponse(self.LogOff):
                break