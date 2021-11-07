from googlesearch import search

def googleSearch(query, country="us", num=20, stop=10, pause=2):
    links = []
    for j in search(query, country=country, num=num, stop=stop, pause=pause):
        links.append(j)
        
    #for link in links:
    #    print(link)

    return links

if __name__ == "__main__":

    googleSearch("TN014 TN-014 A3VV130 Genuine Konica Minolta Toner For Pro 1250 1052")
