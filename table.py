import config
from dateutil.parser import parse

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