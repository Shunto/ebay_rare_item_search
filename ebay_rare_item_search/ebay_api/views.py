from django.shortcuts import render
import requests
API_KEY = 'ShuntoMi-onlinefl-SBX-9abdb138a-8f290d89'

# Create your views here.

def home(request):
    url = 'https://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsByCategory&SERVICE-VERSION=1.0.0&SECURITY-APPNAME=[API_KEY]&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&categoryId=10181&paginationInput.entriesPerPage=2'
    response = requests.get(url)
    data = response.json()
    print(data)

    context = {
        'data' : data
    }

    return render(request, 'ebay_api/home.html', context)
