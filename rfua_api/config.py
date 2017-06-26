#!/usr/bin/env python3
import uuid, json

ClientDetails = {'ApplicationVersion': 'Version 291',
                 'CallId': str(uuid.uuid4()), # Random value in uuid format
                 'ClientIP': '192.168.0.1',
                 'ClientIMEI': '7F2CA69D-9730-48DE-8E78-8F564356DB07',
                 'ClientMAC': '',
                 'RootJailbreak': 'false',
                 'OSIdentifier': '10.3.2'}
Headers = {'Host': 'phoenix.aval.ua',
           'Content-Type': 'application/json',
           'Request-Context': json.dumps(ClientDetails),
           'Accept': '*/*',
           'User-Agent': 'Apache-HttpClient/4.1.1 (java 1.5)',
           'Accept-Language': 'en-us',
           'Connection': 'keep-alive'
           }
Url = 'https://online.aval.ua:444/iphone/en/Account/'
LoginUrl = 'https://online.aval.ua:444/iphone/en/Security/'
Timeout = 8
