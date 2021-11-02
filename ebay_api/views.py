from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
#import urllib2
import json
import hashlib

#API_KEY = 'ShuntoMi-onlinefl-SBX-9abdb138a-8f290d89'
API_KEY = 'ShuntoMi-onlinefl-PRD-5abc8ca47-74474a69'
EBAY_VERIFICATION_TOKEN = 'vCseeOgaClqLpLYJpUunocWXAJwactBSZNlAHHMVJhSlAQvoYM'

# Create your views here.

def home(request):
    url = 'https://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsByCategory&SERVICE-VERSION=1.0.0&SECURITY-APPNAME=' + API_KEY + '&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&categoryId=10181&paginationInput.entriesPerPage=2'
    response = requests.get(url)
    data = response.json()
    print(data)

    context = {
        'data' : data
    }

    return render(request, 'ebay_api/home.html', context)

@csrf_exempt
def ebay_challenge_and_response_verification(request):

    if request.method == 'POST': # If the form has been submitted...
        #form = ContactForm(request.POST) # A form bound to the POST data
        #if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
        return HttpResponse(status=200)
        
    challenge_code = request.GET.get('challenge_code')
    verificationToken = EBAY_VERIFICATION_TOKEN
    #verificationToken = '9jf@31i7jx9phr0w210#tt@4973iqcdg9b-(9+3pb-zl#qm3^-'
    endpoint = 'https://ebayrareitemsearch.herokuapp.com/ebay-challenge-and-response-verification'
    #endpoint = str(request)
    #request = urllib2.urlopen(request)
    #test = request.GET.url
    #test = str(request.read())
    #test = str(request.info().keys())

    #print(challenge_code)
    #print(endpoint)
    #str(string_to_hash).encode('utf-8')
    m = hashlib.sha256(str(challenge_code+verificationToken+endpoint).encode('utf-8')).hexdigest();
    #print(m);
    response = {}
    #response['status'] = 200
    #response['response'] = 'SUCCESS'
    response['challengeResponse'] = m
    #response['test'] = test

    return HttpResponse(json.dumps(response), status=200, content_type="application/json")
    #return JsonResponse(response)
    #return JsonResponse({'status':200, 'response':'SUCCESS'})
