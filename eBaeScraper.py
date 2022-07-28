import math

def round_up(n, int=0):
    multiplier = 10 ** int
    return math.ceil(n * multiplier) / multiplier

import requests
from bs4 import BeautifulSoup

def get_request_data(url):
    response = requests.get(url)
    return response.text

def get_ebay_url(page_num) :
    return 'https://www.ebay.com/sch/1920-29/37832/i.html?_ssn=the-ad-store&_fosrp=1&_pgn=' + str(page_num)

item_names = []
item_prices = []
new_item_bool = []
item_urls = []
item_ebay_numbers = []
#incomplete_ebay_url = 'https://www.ebay.com/sch/1920-29/37832/i.html?_ssn=the-ad-store&_fosrp=1&_pgn='
incomplete_ebay_url = 'https://www.ebay.com/sch/m.html?_trkparms=folent%3Abestbid_01%7Cfolenttp%3A1&_ssn=bestbid_01&_pgn='
data=get_request_data(incomplete_ebay_url + "1")

soup = BeautifulSoup(data, "html.parser")
item_num_lis = soup.find_all(text='			Item:')
#<li>			Item: 155093865935</li>
record_count = int(soup.find('span', attrs={'class': 'rcnt'}).contents[0].replace(',',''))
total_pages = int(round_up(record_count/60))
print(type(total_pages))


for page_num in range(1,total_pages):
    pagedata = get_request_data(get_ebay_url(page_num))
    listing_page = soup.find_all('li', attrs={'class': 'sresult'})
    for listing in listing_page:
        prod_name=" "
        prod_price = " "
        new_prod = 0
        
        h3_lvtitle = listing.find('h3', attrs={'class':"lvtitle"})

        if (h3_lvtitle.a.title!="Nothing"):
            title = str(h3_lvtitle.a.contents[0]).replace("\r","").replace("\n","").replace("\t","")
            ref_link = str(h3_lvtitle.a['href'])

            if ("New listing" in title):
                title = str(h3_lvtitle.a.contents[1]).replace("\r","").replace("\n","").replace("\t","")
                new_prod = 1
            
            item_names.append(title)
            new_item_bool.append(new_prod)
            item_urls.append(ref_link)

        #If products are found, find the prices
            li_lvprice = listing.find('li', attrs={'class':"lvprice"})
            price = str(li_lvprice.find('span', attrs={'class':"bold"}).contents[0]).removeprefix("\n\t\t\t\t\t")

            if (prod_price==" "):
                prod_price=f"{price}"
                item_prices.append(prod_price)


#Get the Item Numbers form the URLs
for item_url in item_urls:
    item_ebay_numbers.append(item_url.removeprefix("https://www.ebay.com/itm/").split('?', 1)[0])

from scipy import stats
import numpy as np
import pandas as pd

df = pd.DataFrame({"New Listing":new_item_bool,"Name":item_names, "Price": item_prices, "Url": item_urls, "Item Number": item_ebay_numbers})
df.to_csv('C:\_git\python\eBayScraperthe-ad-store-listings.csv')
#data_note_8 = data_note_8.ilociloc[np.abs(stats.zscore(data_note_8["Prices"])) lt; 3,]
#print(response)
#print(soup)

# ToDo:
# 1) Pull the URLs for the Items!
#    - e.g. https://www.ebay.com/sch/the-ad-store/m.html
#    - Loop through all the items returned, scraping their individual links
#    - Make sure to go through all Pages of Items Available
# 2) Loop through the Item URLs!
#    - for each item, pull info including image, description, category, ect!