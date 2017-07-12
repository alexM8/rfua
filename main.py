#!/usr/bin/env python3
import json
import config
import flask as f
from rfua_api import logger
from rfua_api import api
from table import form_table

app = f.Flask(__name__)


def header():
    return f.templating.render_template("header.html", location=config.location)


def footer():
    return f.templating.render_template("footer.html")


@app.route(config.location + "/")
def main():
    amount = api.session.Cards.json()['Result'][0]['AvailableBalance'] / 100
    return header() + f.templating.render_template("big.html", amount='{:,.2f} UAH'.format(amount)) + footer()


@app.route(config.location + "/details")
def details():
    cards_dict = api.session.Cards.json()['Result']
    holds_dict = api.session.Holds.json()['Result']['Items']
    history_dict = api.session.History.json()['Result']['Items']

    for x in range(0, len(history_dict)):
        history_dict[x]['OriginalAmount'] = '{:,.2f} UAH'.format(history_dict[x]['OriginalAmount'] / 100)
        extra_fields = "OperationUniqueKey", "ChannelType"
        for field in extra_fields:
            del history_dict[x][field]

    for x in range(0, len(holds_dict)):
        holds_dict[x]['Amount'] = '{:,.2f} UAH'.format(holds_dict[x]['Amount'] / 100)
        del holds_dict[x]["HoldUniqueKey"]

    for x in range(0, len(cards_dict)):
        cards_dict[x]['AvailableBalance'] = '{:,.2f} UAH'.format(cards_dict[x]['AvailableBalance'] / 100)
        extra_fields = "ProductAlias", "UniqueKey"
        for field in extra_fields:
            del cards_dict[x][field]

    return header() + \
        f.templating.render_template("body.html", table=form_table(cards_dict, "success"), table_name="Cards") + \
           f.templating.render_template("body.html", table=form_table(holds_dict, "success"), table_name="Holds") + \
           f.templating.render_template("body.html", table=form_table(history_dict, "success"), table_name="History") + \
           footer()


@app.route(config.location + "/client")
def client():
    info_dict = [api.session.Info.json()['Result']['clientData']]

    extra_fields = "ResidentialStatus", "FunctionPackage", "ChannelStatus", \
                   "subscriptions", "AuthenticationToken", "Birthday"
    for fields in extra_fields:
        del info_dict[0][fields]

    return header() + \
        f.templating.render_template("body.html", table=form_table(info_dict, "success"), table_name="Client") + \
           footer()


@app.route(config.location + "/refresh")
def refresh():
    try:
        api.session.refreshHistory()
        api.session.refresh_holds()
        api.session.refresh_cards()
        return "<script> window.history.back(); </script>"
    except Exception as e:
        print(e)
        api.session.__init__()
        return "<script> window.history.back(); </script>"


@app.route(config.location + "/log")
def logfile():
    log = json.loads(json.dumps(logger.get_log(), sort_keys=True))
    return header() + f.templating.render_template("body.html", table=form_table(log, "danger")) + footer()
