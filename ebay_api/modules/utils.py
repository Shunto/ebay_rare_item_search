import urllib.request
from lxml import etree

APP_ID = 'ShuntoMi-onlinefl-PRD-5abc8ca47-74474a69'
DEV_ID = '0277c14f-c1ad-4d7d-914e-bc3258031457'
CERT_ID = 'PRD-abc8ca479332-c73b-479c-b33f-cb1a'
OAUTH_TOKEN = 'v^1.1#i^1#r^0#f^0#p^3#I^3#t^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'

def getEbayApiEndpointResponse(endpoint, operation_name, data, **headers):

    compatibility_level = 853
    category_site_id = 0
    
    http_headers = {
        "X-EBAY-API-COMPATIBILITY-LEVEL": compatibility_level,
        "X-EBAY-API-APP-NAME": APP_ID,
        "X-EBAY-API-DEV-NAME": DEV_ID,
        "X-EBAY-API-CERT-NAME": CERT_ID,
        "X-EBAY-API-CALL-NAME": operation_name,
        "X-EBAY-API-SITEID": category_site_id,
        "Content-Type": "text/xml"
    }

    http_headers.update(headers)
    
    req = urllib.request.Request(endpoint, data, http_headers)
    res = urllib.request.urlopen(req)
    return res.read()

def getEbayFindingApiResponse(operation_name, data, encoding, **headers):

    global_id = "EBAY-US"
    category_site_id = 0
    endpoint = "http://svcs.ebay.com/services/search/FindingService/v1"

    http_headers = {
        "X-EBAY-SOA-OPERATION-NAME": operation_name,
        "X-EBAY-SOA-SECURITY-APPNAME": APP_ID,
        "X-EBAY-SOA-GLOBAL-ID": global_id,
        "X-EBAY-SOA-RESPONSE-DATA-FORMAT": encoding
    }

    http_headers.update(headers)
    
    req = urllib.request.Request(endpoint, data, http_headers)
    res = urllib.request.urlopen(req)
    #return res
    return res.read()
