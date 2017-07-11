#!/usr/bin/env python3
from flask import Flask, current_app
from flask.templating import render_template
from rfua_api.main import *
from rfua_api.functions import logger
import config
from dateutil.parser import parse
import json

app = Flask(__name__)

@app.route(config.location + "/favicon.ico")
def favicon():
    return current_app.send_static_file("favicon.ico")

@app.route(config.location + "/")
def header():
    return render_template("header.html", location = config.location)

def footer():
    return render_template("footer.html")

@app.route(config.location + "/main")
def main():
    return header() +\
           render_template("big.html", amount = session.Cards.json()['Result'][0]['AvailableBalance'] / 100) +\
           footer()

def FormTable(dict, header_colour = "active", result = ''):
    for card in range(0, len(dict)):
        for element in dict[0].items():
            result += "<th class = \"" + header_colour + "\">" + str(element[0]) + "</th>"
        break
    result += "</tr><tr class = \"active\">"
    for card in range(0, len(dict)):
        for element in dict[card].items():
            test = element[1]
            if element[0] in config.DataFields:
                test = parse(test).date().isoformat()
            result += "<td class = \"active\">" + str(test) + "</td>"
        result += "</tr><tr class = \"active\">"
    result = "<table class = \"table table-bordered\"><tr class = \"" + header_colour + "\">" + result + "</tr></table>"
    return result

@app.route(config.location + "/details")
def details():
    CardsDict = session.Cards.json()['Result']
    HoldsDict = session.Holds.json()['Result']['Items']
    HistoryDict = session.History.json()['Result']['Items']

    for x in range(0, len(HistoryDict)):
        HistoryDict[x]['OriginalAmount'] /= 100
        Extrafields = "OperationUniqueKey", "ChannelType"
        for field in Extrafields:
            del HistoryDict[x][field]

    for x in range(0, len(HoldsDict)):
        HoldsDict[x]['Amount'] /= 100
        del HoldsDict[x]["HoldUniqueKey"]

    for x in range(0, len(CardsDict)):
        CardsDict[x]['AvailableBalance'] /= 100
        Extrafields = "ProductAlias", "UniqueKey"
        for field in Extrafields:
            del CardsDict[x][field]

    result = header() + \
             render_template("body.html", table = FormTable(CardsDict, "success"), table_name = "Cards") + \
             render_template("body.html", table = FormTable(HoldsDict, "success"), table_name = "Holds") + \
             render_template("body.html", table = FormTable(HistoryDict, "success"), table_name = "History") + \
             footer()
    return result

@app.route(config.location + "/client")
def client():
    InfoDict = session.Info.json()['Result']['clientData']

    ExtraFields = "ResidentialStatus", "FunctionPackage", "ChannelStatus", \
                  "subscriptions", "AuthenticationToken", "Birthday",
    for fields in ExtraFields:
        del InfoDict[fields]

    info = []
    info.append(InfoDict)

    result = header() + \
             render_template("body.html", table=FormTable(info, "success"), table_name="Information") + footer()
    return result

@app.route(config.location + "/refresh")
def refresh():
    try:
        session.refreshHistory()
        session.refreshHolds()
        session.refreshCards()
        return "<script> window.history.back(); </script>"
    except:
        session.__init__()
        return "<script> window.history.back(); </script>"

@app.route(config.location + "/log")
def log():
    Log = json.loads(json.dumps(logger.getLog(), sort_keys = True))
    return header() + render_template("body.html", table = FormTable(Log, "danger")) + footer()

@app.route(config.location + "/devices")
def devices():
    DevicesDict = session.Info.json()['Result']['clientData']['subscriptions']
    return header() + render_template("body.html", table = FormTable(DevicesDict, "success")) + footer()