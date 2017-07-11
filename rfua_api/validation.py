from . import logger

def CheckForVaidResponse(result):
    logger.writeLog(result)
    if result.json()['ResponseCode'] == '000':
        return True
    else:
        return False