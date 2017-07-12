from . import logger

def CheckForVaidResponse(result):
    logger.write_log(result)
    if result.json()['ResponseCode'] == '000':
        return True
    else:
        return False