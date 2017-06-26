#!/usr/bin/python3.4
from flask import Flask, current_app
from flask.templating import render_template
from rfua_api_client.main import session
import json

app = Flask(__name__)
location = ""

@app.route(location + "/favicon.ico")
def favicon():
    return current_app.send_static_file("favicon.ico")

@app.route(location + "/")
def root():
    return header()

def header():
    return render_template("header.html", location = location)

def FormTable(dict, header_colour = "active"):
    result = "<tr class = \"" + header_colour + "\">"
    for card in range(0, len(dict)):
        for element in dict[0].items():
            result += "<th class = \"" + header_colour + "\">" + str(element[0]) + "</th>"
        break
    result += "</tr><tr class = \"active\">"
    for card in range(0, len(dict)):
        for element in dict[card].items():
            result += "<td class = \"active\">" + str(element[1]) + "</td>"
        result += "</tr><tr class = \"active\">"
    result += "</tr>"
    result = "<table class = \"table table-bordered\"" + result + "</table>"
    return result

@app.route(location + "/accounts")
def accounts():
    AccountsDict = session.Accounts.json()['Result']

    AccountsDict['UAHBalance'] /= 100
    AccountsDict['Balance'] /= 100
    AccountsDict['AvailableBalance'] /= 100

    Extrafields = "ProductName", "ProductAlias", "UniqueKey", "AccountDescription", "NonReducableBalance"
    for field in Extrafields:
        del AccountsDict[field]

    accounts = []
    accounts.append(AccountsDict)
    result = header() + render_template("body.html", dict = FormTable(accounts, "success"))
    return result

@app.route(location + "/cards")
def cards():
    CardsDict = session.Cards.json()['Result']

    for x in range(0, len(CardsDict)):
        CardsDict[x]['AvailableBalance'] /= float(100)
        Extrafields = "ProductAlias", "UniqueKey"
        for field in Extrafields:
            del CardsDict[x][field]

    return header() + render_template("body.html", dict = FormTable(CardsDict, "success"))

@app.route(location + "/holds")
def holds():
    HoldsDict = session.Holds.json()['Result']['Items']

    for x in range(0, len(HoldsDict)):
        HoldsDict[x]['Amount'] /= float(100)
        del HoldsDict[x]["HoldUniqueKey"]

    return header() + render_template("body.html", dict = FormTable(HoldsDict, "success"))

@app.route(location + "/history")
def history():
    HistoryDict = session.History.json()['Result']['Items']

    for x in range(0, len(HistoryDict)):
        HistoryDict[x]['OriginalAmount'] /= float(100)
        Extrafields = "OperationUniqueKey", "ChannelType"
        for field in Extrafields:
            del HistoryDict[x][field]

    return header() + render_template("body.html", dict = FormTable(HistoryDict, "success"))

@app.route(location + "/refresh")
def refresh():
    session.refreshHistory()
    session.refreshHolds()
    session.refreshCards()
    session.refreshAccounts()
    return "<script> window.history.back(); </script>"

@app.route(location + "/log")
def log():
    session.log = json.loads(json.dumps(session.log, sort_keys = True))
    return header() + render_template("body.html", dict = FormTable(session.log, "danger"))

@app.route(location + "/devices")
def devices():
    DevicesDict = session.Info.json()['Result']['clientData']['subscriptions']

    return header() + render_template("body.html", dict=FormTable(DevicesDict, "success"))

@app.route(location + "/info")
def info():
    InfoDict = session.Info.json()['Result']['clientData']

    ExtraFields = "ResidentialStatus", "FunctionPackage", "ChannelStatus", "subscriptions"
    for fields in ExtraFields:
        del InfoDict[fields]

    info = []
    info.append(InfoDict)

    return header() + render_template("body.html", dict=FormTable(info, "success"))
