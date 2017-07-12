#!/usr/bin/env python3
import json, config
import flask as f
from rfua_api import logger, api
from table import FormTable

app = f.Flask(__name__)

# @app.route(config.location + "/")
# def header():
#     return '<a href="' + config.location + '/main' + '"></a>'

def header():
    return f.templating.render_template("header.html", location = config.location)

def footer():
    return f.templating.render_template("footer.html")

@app.route(config.location + "/")
def main():
    amount = api.session.Cards.json()['Result'][0]['AvailableBalance'] / 100
    return header() + f.templating.render_template("big.html", amount = '{:,.2f} UAH'.format(amount)) + footer()

@app.route(config.location + "/details")
def details():
    CardsDict = api.session.Cards.json()['Result']
    HoldsDict = api.session.Holds.json()['Result']['Items']
    HistoryDict = api.session.History.json()['Result']['Items']

    for x in range(0, len(HistoryDict)):
        HistoryDict[x]['OriginalAmount'] = '{:,.2f} UAH'.format(HistoryDict[x]['OriginalAmount'] / 100)
        Extrafields = "OperationUniqueKey", "ChannelType"
        for field in Extrafields:
            del HistoryDict[x][field]

    for x in range(0, len(HoldsDict)):
        HoldsDict[x]['Amount'] = '{:,.2f} UAH'.format(HoldsDict[x]['Amount'] / 100)
        del HoldsDict[x]["HoldUniqueKey"]

    for x in range(0, len(CardsDict)):
        CardsDict[x]['AvailableBalance'] = '{:,.2f} UAH'.format(CardsDict[x]['AvailableBalance'] / 100)
        Extrafields = "ProductAlias", "UniqueKey"
        for field in Extrafields:
            del CardsDict[x][field]

    return header() + \
        f.templating.render_template("body.html", table = FormTable(CardsDict, "success"), table_name = "Cards") + \
        f.templating.render_template("body.html", table = FormTable(HoldsDict, "success"), table_name = "Holds") + \
        f.templating.render_template("body.html", table = FormTable(HistoryDict, "success"), table_name = "History") + \
        footer()

@app.route(config.location + "/client")
def client():
    InfoDict = [api.session.Info.json()['Result']['clientData']]

    ExtraFields = "ResidentialStatus", "FunctionPackage", "ChannelStatus", \
                  "subscriptions", "AuthenticationToken", "Birthday",
    for fields in ExtraFields:
        del InfoDict[0][fields]

    return header() + \
             f.templating.render_template("body.html", table=FormTable(InfoDict, "success"), table_name="Client") + footer()

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