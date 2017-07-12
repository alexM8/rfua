Log = []


def write_log(request):
    log_entry = request.json()
    log_entry['TotalSeconds'] = request.elapsed.total_seconds()
    log_entry['Destination'] = request.request.url
    extra_fields = 'Result', 'ShowAlert', 'AlertMessage'
    for field in extra_fields:
        try:
            del log_entry[field]
        except:
            pass
    Log.append(log_entry)

def get_log():
    return Log
