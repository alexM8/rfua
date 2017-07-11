#!/usr/bin/env python3
import json
import flask as f
from rfua_api import logger, api
from . import config
from table import FormTable

app = f.Flask(__name__)

@app.route(config.location + "/")
def header():
    return f.templating.render_template("header.html", location = config.location)

def footer():
    return f.templating.render_template("footer.html")

@app.route(config.location + "/main")
def main():
    return header() + \
        f.templating.render_template("big.html", amount = api.session.Cards.json()['Result'][0]['AvailableBalance'] / 100) +\
        footer()

@app.route(config.location + "/details")
def details():
    CardsDict = api.session.Cards.json()['Result']
    HoldsDict = api.session.Holds.json()['Result']['Items']
    HistoryDict = api.session.History.json()['Result']['Items']

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
        f.templating.render_template("body.html", table = FormTable(CardsDict, "success"), table_name = "Cards") + \
        f.templating.render_template("body.html", table = FormTable(HoldsDict, "success"), table_name = "Holds") + \
        f.templating.render_template("body.html", table = FormTable(HistoryDict, "success"), table_name = "History") + \
        footer()
    return result

@app.route(config.location + "/client")
def client():
    InfoDict = api.session.Info.json()['Result']['clientData']

    ExtraFields = "ResidentialStatus", "FunctionPackage", "ChannelStatus", \
                  "subscriptions", "AuthenticationToken", "Birthday",
    for fields in ExtraFields:
        del InfoDict[fields]

    info = []
    info.append(InfoDict)

    result = header() + \
             f.templating.render_template("body.html", table=FormTable(info, "success"), table_name="Client") + footer()
    return result

@app.route(config.location + "/refresh")
def refresh():
    try:
        api.session.refreshHistory()
        api.session.refreshHolds()
        api.session.refreshCards()
        return "<script> window.history.back(); </script>"
    except:
        api.session.__init__()
        return "<script> window.history.back(); </script>"

@app.route(config.location + "/log")
def log():
    Log = json.loads(json.dumps(logger.getLog(), sort_keys = True))
    return header() + f.templating.render_template("body.html", table = FormTable(Log, "danger")) + footer()

@app.route(config.location + "/devices")
def devices():
    DevicesDict = api.session.Info.json()['Result']['clientData']['subscriptions']
    return header() + f.templating.render_template("body.html", table = FormTable(DevicesDict, "success")) + footer()