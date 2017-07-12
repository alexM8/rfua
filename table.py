import config
from dateutil.parser import parse


def form_table(data, header_colour="active", result=''):
    for card in range(0, len(data)):
        for element in data[0].items():
            result += "<th class = \"" + header_colour + "\">" + str(element[0]) + "</th>"
        break
    result += "</tr><tr class = \"active\">"
    for card in range(0, len(data)):
        for element in data[card].items():
            test = element[1]
            if element[0] in config.DataFields:
                test = parse(test).date().isoformat()
            result += "<td class = \"active\">" + str(test) + "</td>"
        result += "</tr><tr class = \"active\">"
    result = "<table class = \"table table-bordered\"><tr class = \"" + header_colour + "\">" + result + "</tr></table>"
    return result
