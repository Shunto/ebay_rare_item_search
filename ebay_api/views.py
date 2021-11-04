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
    product_id = request.GET.get('product_id')

    if product_id:
        #operation_name = 'findItemsByCategory'
        operation_name = 'findItemsByProduct'
        variables = 'categoryId=10181&paginationInput.entriesPerPage=2'
        variables = 'paginationInput.entriesPerPage=3&productId.@type=ReferenceID&productId=' + product_id
        #variables = 'productId.@type=ReferenceID&productId={product_id}'

        url = f'https://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME={operation_name}&SERVICE-VERSION=1.0.0&SECURITY-APPNAME={API_KEY}&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&{variables}'

        response = requests.get(url)
        data = response.json()
        #data = json.loads(response.text())
        print(data)
        #test = "findItemsByProductResponse"
        #items = data[0][test]['searchResult']['item']
        #items = data.get(operation_name+'Response')[0].get('searchResult')[0].get('item')
        items = data[operation_name+'Response'][0]['searchResult'][0]['item']

        item_keys = items[0].keys()
        for item in items:
            for item_key in item_keys:
                item[item_key] = item[item_key][0]
        #for item_key in item_keys:
        #    items[0][item_key] = items[0][item_key][0]

        pagination_output = data[operation_name+'Response'][0]['paginationOutput'][0]
        
        context = {
            #'data' : data,
            'items' : items,
            'pagination_output' : pagination_output
        }

        return render(request, 'ebay_api/home.html', context)
    else:
        return render(request, 'ebay_api/home.html')

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
