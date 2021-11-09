from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json
import hashlib
import random
import sys
import os
from ebay_rare_item_search.settings import BASE_DIR
sys.path.append(os.path.join(BASE_DIR, 'ebay_api/modules'))
from ebay_api_calls import findItemsByCategory
from item_filters import uniqueItemFilterByTitle, uniqueItemFilterByProductId
from google_search import googleSearch

#API_KEY = 'ShuntoMi-onlinefl-SBX-9abdb138a-8f290d89'
API_KEY = 'ShuntoMi-onlinefl-PRD-5abc8ca47-74474a69'
EBAY_VERIFICATION_TOKEN = 'vCseeOgaClqLpLYJpUunocWXAJwactBSZNlAHHMVJhSlAQvoYM'

# Create your views here.

def home(request):
    category = request.GET.get('category')
    title = request.GET.get('title')
    product_id = request.GET.get('product_id')
    best_offer_only = request.GET.get('best_offer_only')
    title_search = request.GET.get('title_search')
    product_id_only = request.GET.get('product_id_only')
    condition = request.GET.get('condition')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sample_count = request.GET.get('sample_count')
    
    #best_offer_only = "true"
    #listing_type = 'BestOffer'
    #condition = "3000"
    max_quantity = "1"
    min_quantity = "1"
    item_keys = ["itemId", "title", "condition", "primaryCategory", "galleryURL", "viewItemURL"]

    item_filter = [
        {
            "name": "BestOfferOnly",
            "value": best_offer_only
        },
        {
            "name": "MaxQuantity",
            "value": max_quantity
        },
        {
            "name": "MinQuantity",
            "value": min_quantity
        },
        {
            "name": "MinPrice",
            #"paramName": "Currency",
            #"paramValue": "USD",
            "value": min_price
        },
        {
            "name": "MaxPrice",
            #"paramName": "Currency",
            #"paramValue": "USD",
            "value": max_price
        }
    ]

    if condition:
        item_filter.append({
            "name": "Condition",
            "value": condition
        })

    if category:
        category_id = category
        operation_name = 'findItemsByCategory'
        items = []
        rare_items = []

        response = findItemsByCategory(category_id, itemFilter=item_filter)
        data = json.loads(response.decode('utf-8'))
        total_pages = data[operation_name+'Response'][0]['paginationOutput'][0]["totalPages"][0]
        total_entries = data[operation_name+'Response'][0]['paginationOutput'][0]["totalEntries"][0]

        page_count = 0
        if int(total_pages) <= 100:
            page_numbers = list(range(1, int(total_pages)+1))
        else:
            #page_numbers = list(range(1, 101)) # max allowed page number = 100
            page_numbers = list(range(1, 30)) # any page number greater than or equal to 30 doesn't work so far somehow
        random.shuffle(page_numbers)
        randomized_page_numbers = page_numbers
        entries_per_page = "10" # Min: 0, Max: 100
        total_searched_item_count = 0
        pagination_input = {
            "entriesPerPage": entries_per_page,
            "pageNumber": str(randomized_page_numbers[page_count])
            #"pageNumber": "30"
        }
        #pagination_output = {}
        pagination_output = []
        missed_page_numbers = []
        
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
            if "item" in data[operation_name+'Response'][0]['searchResult'][0]:
                items = data[operation_name+'Response'][0]['searchResult'][0]['item']

            #item_keys = items[0].keys()
                #items = filter(lambda x: "productId" in x, items)
                # filtering out items with no product ids
                if product_id_only == "true":
                    items = [item for item in items if "productId" in item]
                elif product_id_only == "false":
                    items = [item for item in items if "productId" not in item]
                # filtering out items when other items with the same product ids exist
                if title_search == "true":
                    items = uniqueItemFilterByTitle(items)
                else:
                    items = uniqueItemFilterByProductId(items)

                rare_items = rare_items + items
            else:
                missed_page_numbers.append(data[operation_name+'Response'][0]['paginationOutput'][0]['pageNumber'][0])
            
            #pagination_output.update(data[operation_name+'Response'][0]['paginationOutput'][0])
            pagination_output.append(data[operation_name+'Response'][0]['paginationOutput'][0])

            page_count += 1
            searched_item_count = data[operation_name+'Response'][0]['paginationOutput'][0]['entriesPerPage'][0]
            total_searched_item_count += int(searched_item_count)

            if page_count == len(randomized_page_numbers):
                break
            if page_count == total_pages:
                break
            #page_number = str(int(page_number) + 1)
            pagination_input["pageNumber"] = str(randomized_page_numbers[page_count])

        for item in rare_items:
            for item_key in item_keys:
                item[item_key] = item[item_key][0]
                if "conditionDisplayName" in item[item_key]:
                    item[item_key]["conditionDisplayName"] = item[item_key]["conditionDisplayName"][0]
                if "categoryName" in item[item_key]:
                    item[item_key]["categoryName"] = item[item_key]["categoryName"][0]
                if (title_search == "false") and ("productId" in item):
                    item["product_id"] = item["productId"][0]["__value__"]

        pagination_output = [pagination_output, page_count+1, len(items), missed_page_numbers]
        total_rare_item_count = len(rare_items)
        random.shuffle(rare_items)
        if int(sample_count) <= total_rare_item_count:
            rare_items[0:int(sample_count)]

        output_info = {
            "sampled_rare_item_count": len(rare_items),
            "total_rare_item_count": total_rare_item_count,
            "total_searched_item_count": total_searched_item_count,
            "total_searched_page_count": page_count,
            "page_numbers": page_numbers[0:5],
            "total_entries": total_entries,
            "searched_category": category
        }
        
        context = {
            'data': data,
            'items': rare_items,
            'pagination_output': pagination_output,
            'output_info': output_info
        }
        return render(request, 'ebay_api/home.html', context)
    elif title:
        operation_name = 'findItemsAdvanced'
        variables = 'keywords=' + title
        items = []

        print(title)

        url = f'https://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME={operation_name}&SERVICE-VERSION=1.0.0&SECURITY-APPNAME={API_KEY}&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&{variables}'

        response = requests.get(url)
        data = response.json()
        print(data)
        data["search keywords"] = title
        if "item" in data[operation_name+'Response'][0]['searchResult'][0]:
            items = data[operation_name+'Response'][0]['searchResult'][0]['item']

            for item in items:
                for item_key in item_keys:
                    item[item_key] = item[item_key][0]
                
        pagination_output = data[operation_name+'Response'][0]['paginationOutput']
        
        context = {
            'data': data,
            'items': items,
            'pagination_output': pagination_output
        }

        return render(request, 'ebay_api/home.html', context)
    elif product_id:
        #operation_name = 'findItemsByCategory'
        operation_name = 'findItemsByProduct'
        #variables = 'categoryId=10181&paginationInput.entriesPerPage=10'
        variables = 'paginationInput.entriesPerPage=10&productId.@type=ReferenceID&productId=' + product_id
        #variables = 'productId.@type=ReferenceID&productId={product_id}'

        url = f'https://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME={operation_name}&SERVICE-VERSION=1.0.0&SECURITY-APPNAME={API_KEY}&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&{variables}'

        response = requests.get(url)
        data = response.json()
        print(data)
        #test = "findItemsByProductResponse"
        #items = data[0][test]['searchResult']['item']
        #items = data.get(operation_name+'Response')[0].get('searchResult')[0].get('item')
        items = data[operation_name+'Response'][0]['searchResult'][0]['item']

        #item_keys = items[0].keys()
        for item in items:
            for item_key in item_keys:
                item[item_key] = item[item_key][0]
                if "productId" in item:
                    #item["productId"] = item["productId"][0]
                    #item["productId"][0]["value"] = item["productId"][0]["__value__"]
                    #item["productId"] = item["productId"][0]
                    item["product_id"] = item["productId"][0]["__value__"]

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

    
def google_search_results(request):
    
    query = request.GET.get('query')

    links =  googleSearch(query)
    
    results = {
        "query": query,
        "links": links
    }
    
    return render(request, 'ebay_api/google_search_results.html', results)


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
