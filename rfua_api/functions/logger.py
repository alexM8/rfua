Log = []

def writeLog(request):
    LogEntry = request.json()
    LogEntry['TotalSeconds'] = request.elapsed.total_seconds()
    LogEntry['Destination'] = request.request.url
    Extrafields = 'Result', 'ShowAlert', 'AlertMessage'
    for field in Extrafields:
        try:
            del LogEntry[field]
        except:
            pass
    Log.append(LogEntry)

def getLog():
    return Log
