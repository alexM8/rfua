#!/usr/bin/env python3
from .classes.RFSession import RFSession

try:
    session = RFSession()

except Exception as e:
    print(e)
