import urllib.request
from lxml import etree
from utils import getEbayApiEndpointResponse, getEbayFindingApiResponse, getEbayProductApiResponse


OAUTH_TOKEN = 'v^1.1#i^1#f^0#p^3#I^3#r^0#t^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'

def getCategories(detailLevel="ReturnAll", levelLimit=1, categorySiteId=0):

    operation_name = "GetCategories"
    endpoint = "https://api.ebay.com/ws/api.dll"
    
    root = etree.Element("GetCategoriesRequest", xmlns="urn:ebay:apis:eBLBaseComponents")

    credentials_elem = etree.SubElement(root, "RequesterCredentials")
    token_elem = etree.SubElement(credentials_elem, "eBayAuthToken")
    token_elem.text = OAUTH_TOKEN

    CategorySiteID_elem = etree.SubElement(root, "CategorySiteID")
    CategorySiteID_elem.text = str(categorySiteId)
    
    detailLevel_elem = etree.SubElement(root, "DetailLevel")
    detailLevel_elem.text = detailLevel
    
    levelLimit_elem = etree.SubElement(root, "LevelLimit")
    levelLimit_elem.text = str(levelLimit)

    request_xml = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="utf-8")
    #print("request_xml: {}".format(request_xml))
    
    data = request_xml

    response = getEbayApiResponse(endpoint, operation_name, data)
    #print("response: {}".format(response))
    
    return response


def findItemsAdvanced(keywords, categoryId=None, descriptionSearch=None, itemFilter=None, paginationInput=None, outputSelector=None, encoding="JSON"):

    operation_name = "findItemsAdvanced"
    
    root = etree.Element("findItemsAdvanced", xmlns="http://www.ebay.com/marketplace/search/v1/services")

    keywords_elem = etree.SubElement(root, "keywords")
    keywords_elem.text = keywords

    if categoryId:
        categoryId_elem = etree.SubElement(root, "categoryId")
        categoryId_elem.text = categoryId

    if descriptionSearch:
        descriptionSearch_elem = etree.SubElement(root, "descriptionSearch")
        descriptionSearch_elem.text = descriptionSearch
    
    if itemFilter:
        for item in itemFilter:
            itemFilter_elem = etree.SubElement(root, "itemFilter")
            for key in item:
                key_elem = etree.SubElement(itemFilter_elem, key)
                key_elem.text = item[key]
 
    if paginationInput:
        paginationInput_elem = etree.SubElement(root, "paginationInput")
        for key in paginationInput:
            key_elem = etree.SubElement(paginationInput_elem, key)
            key_elem.text = paginationInput[key]

    if outputSelector:
        for item in outputSelector:
            outputSelector_elem = etree.SubElement(root, "outputSelector")
            outputSelector_elem.text = item

    #request_xml = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="utf-8")
    request_xml = etree.tostring(root, pretty_print=True)
    #print("request_xml: {}".format(request_xml))
    
    data = request_xml

    response = getEbayFindingApiResponse(operation_name, data, encoding)
    print("response: {}".format(response))
    
    return response

        
def findItemsByCategory(categoryId, itemFilter=None, paginationInput=None, outputSelector=None, encoding="JSON"):

    operation_name = "findItemsByCategory"
    
    root = etree.Element(operation_name, xmlns="http://www.ebay.com/marketplace/search/v1/services")
    
    categoryId_elem = etree.SubElement(root, "categoryId")
    categoryId_elem.text = categoryId

    if categoryId:
        categoryId_elem = etree.SubElement(root, "categoryId")
        categoryId_elem.text = categoryId
    
    if itemFilter:
        for item in itemFilter:
            itemFilter_elem = etree.SubElement(root, "itemFilter")
            for key in item:
                key_elem = etree.SubElement(itemFilter_elem, key)
                key_elem.text = item[key]
 
    if paginationInput:
        paginationInput_elem = etree.SubElement(root, "paginationInput")
        for key in paginationInput:
            key_elem = etree.SubElement(paginationInput_elem, key)
            key_elem.text = paginationInput[key]

    if outputSelector:
        for item in outputSelector:
            outputSelector_elem = etree.SubElement(root, "outputSelector")
            outputSelector_elem.text = item

    #request_xml = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="utf-8")
    request_xml = etree.tostring(root, pretty_print=True)
    #print("request_xml: {}".format(request_xml))
    
    data = request_xml

    response = getEbayFindingApiResponse(operation_name, data, encoding)
    #print("response: {}".format(response))
    
    return response


def findItemsByProduct(productId, itemFilter=None, paginationInput=None, outputSelector=None, encoding="JSON"):

    operation_name = "findItemsByProduct"
    
    root = etree.Element(operation_name, xmlns="http://www.ebay.com/marketplace/search/v1/services")

    productId_elem = etree.SubElement(root, "productId", type="ReferenceID")
    productId_elem.text = productId
          
    if itemFilter:
        for item in itemFilter:
            itemFilter_elem = etree.SubElement(root, "itemFilter")
            for key in item:
                key_elem = etree.SubElement(itemFilter_elem, key)
                key_elem.text = item[key]
 
    if paginationInput:
        paginationInput_elem = etree.SubElement(root, "paginationInput")
        for key in paginationInput:
            key_elem = etree.SubElement(paginationInput_elem, key)
            key_elem.text = paginationInput[key]

    if outputSelector:
        for item in outputSelector:
            outputSelector_elem = etree.SubElement(root, "outputSelector")
            outputSelector_elem.text = item

    #request_xml = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="utf-8")
    request_xml = etree.tostring(root, pretty_print=True)
    #print("request_xml: {}".format(request_xml))
    
    data = request_xml

    response = getEbayFindingApiResponse(operation_name, data, encoding)
    #print("response: {}".format(response))
    
    return response


def findProducts(QueryKeywords=None, MaxEntries=None, AvailableItemsOnly="true", PageNumber=None, ProductIDType="Reference", ProductSort=None, SortOrder=None, encoding="JSON"):

    operation_name = "findProductsRequest"
    
    #root = etree.Element(operation_name, xmlns="urn:ebay:apis:eBLBaseComponents")
    root = etree.Element("findProductsRequest", xmlns="http://www.ebay.com/marketplace/marketplacecatalog/v1/services")


    if QueryKeywords:
        QueryKeywords_elem = etree.SubElement(root, "QueryKeywords")
        QueryKeywords_elem.text = QueryKeywords
    
    if MaxEntries:
        MaxEntries_elem = etree.SubElement(root, "MaxEntries")
        MaxEntries_elem.text = MaxEntries

    ProductIDType_elem = etree.SubElement(root, "ProductID", type="ProductIDCodeType")
    ProductIDType_elem.text = ProductIDType

    if PageNumber:
        PageNumber_elem = etree.SubElement(root, "PageNumber")
        PageNumber_elem.text = PageNumber

    if ProductSort:
        ProductSort_elem = etree.SubElement(root, "ProductSortn")
        ProductSort_elem.text = ProductSort

    if SortOrder:
        SortOrder_elem = etree.SubElement(root, "SortOrder")
        SortOrder_elem.text = SortOrder
 
    #request_xml = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="utf-8")
    request_xml = etree.tostring(root, pretty_print=True)
    #print("request_xml: {}".format(request_xml))
    
    data = request_xml

    response = getEbayProductApiResponse(operation_name, data, encoding)
    print("response: {}".format(response))
    
    return response
    
if __name__ == "__main__":
    #getCategories()
    #findItemsByCategory("58058")
    findItemsAdvanced("macbook", categoryId="")
    #findItemsAdvanced("")
    #findProducts(MaxEntries="5")
