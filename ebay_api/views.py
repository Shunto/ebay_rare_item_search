from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
#import urllib2
import json
import hashlib
import sys
import os
#sys.path.append(".")
sys.path.append('/Users/shuntomizushima/programs/research/ebay_rare_item_search/ebay_api')
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ebay_rare_item_search.settings')
#sys.path.append('/ebay_rare_item_search/ebay_api')

from ebay_api_calls import findItemsByCategory

#API_KEY = 'ShuntoMi-onlinefl-SBX-9abdb138a-8f290d89'
API_KEY = 'ShuntoMi-onlinefl-PRD-5abc8ca47-74474a69'
EBAY_VERIFICATION_TOKEN = 'vCseeOgaClqLpLYJpUunocWXAJwactBSZNlAHHMVJhSlAQvoYM'

# Create your views here.

def home(request):
    category = request.GET.get('category')
    product_id = request.GET.get('product_id')
    best_offer_only = request.GET.get('best_offer_only')
    product_id_only = request.GET.get('product_id_only')
    sample_count = request.GET.get('sample_count')
    #best_offer_only = "true"
    #listing_type = 'BestOffer'
    condition = "3000"
    max_quantity = "1"
    min_quantity = "1"

    item_filter = [
        {
            "name": "BestOfferOnly",
            "value": best_offer_only
        }]
    '''{
            "name": "MaxQuantity",
            #"paramName":
            #"paramValue":
            "value": max_quantity
        },
        {
            "name": "MinQuantity",
            "paramName": "",
            "paramValue": "",
            "value": min_quantity
        }
    ]'''
    '''{
            "name": "Condition",
            "paramName": "",
            "paramValue": "",
            "value": condition
        }
    ]'''

    if category:
        category_id = category
        operation_name = 'findItemsByCategory'
        items = []
        item_keys = ["itemId", "title", "galleryURL", "viewItemURL"]
        page_number = "1"
        entries_per_page = "100"
        pagination_input = {
            "entriesPerPage": entries_per_page,
            "pageNumber"    : page_number
        }
        #pagination_output = {}
        pagination_output = []
        
        #variables = 'categoryId=' + category + '&paginationInput.entriesPerPage=100'
        #variables = 'paginationInput.entriesPerPage=3&productId.@type=ReferenceID&productId=' + product_id
        #variables = 'productId.@type=ReferenceID&productId={product_id}'
        #variables = variables + '&itemFilter.ListingType={item_fiter_variables[\'ListingType\']}'
        #variables = variables + f'&itemFilter.name=BestOfferOnly&itemFilter.value={item_filter_variables["BestOfferOnly"]}'
        #variables = variables + f'&itemFilter.name=BestOfferOnly.value={item_filter_variables["BestOfferOnly"]}'
        #variables = variables + f'&itemFilter.name=BestOfferOnly&itemFilter.value={best_offer_only}'
        #variables = variables + '&itemFilter.name=BestOfferOnly&itemFilter.value=true'
        # variables = variables + f'&itemFilter.name=MaxQuantity.value={item_filter_variables["MaxQuantity"]}'
        # variables = variables + f'&itemFilter.name=MinQuantity.value={item_filter_variables["MinQuantity"]}'
        # variables = variables + f'&itemFilter.name=Condition.value={item_filter_variables["Condition"]}'
        

        #url = f'https://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME={operation_name}&SERVICE-VERSION=1.0.0&SECURITY-APPNAME={API_KEY}&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&{variables}'

        #response = requests.get(url)
        #data = response.json()
        while len(items) < int(sample_count):
        #while int(page_number) < 3:
            response = findItemsByCategory(category_id, itemFilter=item_filter, paginationInput=pagination_input)
            data = json.loads(response.decode('utf-8'))
            
        #data = response
        #data = json.loads(response.text())
            print(data)
        #test = "findItemsByProductResponse"
        #items = data[0][test]['searchResult']['item']
        #items = data.get(operation_name+'Response')[0].get('searchResult')[0].get('item')
        
            #items = data[operation_name+'Response'][0]['searchResult'][0]['item']
            items = items + data[operation_name+'Response'][0]['searchResult'][0]['item']

            #item_keys = items[0].keys()
            #items = filter(lambda x: "productId" in x, items)
            # filtering out items with no product ids
            if product_id_only == "true":
                items = [item for item in items if "productId" in item]
            
            #pagination_output.update(data[operation_name+'Response'][0]['paginationOutput'][0])
            pagination_output.append(data[operation_name+'Response'][0]['paginationOutput'][0])
            page_number = str(int(page_number) + 1)
            pagination_input["pageNumber"] = page_number

        for item in items:
            for item_key in item_keys:
                item[item_key] = item[item_key][0]

        pagination_output = [pagination_output, page_number, len(items)]
        context = {
            'data': data,
            'items': items,
            'pagination_output': pagination_output
        }
        return render(request, 'ebay_api/home.html', context)
    elif product_id:
        #operation_name = 'findItemsByCategory'
        operation_name = 'findItemsByProduct'
        variables = 'categoryId=10181&paginationInput.entriesPerPage=10'
        variables = 'paginationInput.entriesPerPage=10&productId.@type=ReferenceID&productId=' + product_id
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

        #pagination_output = data[operation_name+'Response'][0]['paginationOutput'][0]
        pagination_output = data[operation_name+'Response'][0]['paginationOutput']
        
        context = {
            #'data': data,
            'items': items,
            'pagination_output': pagination_output
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
