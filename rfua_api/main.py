#!/usr/bin/env python3
import traceback
from .classes.RFSession import RFSession

try:
    session = RFSession()

except Exception as e:
    print (session.log)
    traceback.print_exc()
