#!/usr/bin/env python3
import traceback
from . import config
from .classes.RFSession import RFSession

try:
    session = RFSession(config)

except Exception as e:
    print (session.log)
    traceback.print_exc()
