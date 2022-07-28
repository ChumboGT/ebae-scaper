import requests
from bs4 import BeautifulSoup

item_names = []
item_prices = []

ebay_store_url = 'https://www.ebay.com/sch/1920-29/37832/m.html?_ssn=the-ad-store'
response = requests.get(ebay_store_url)
data=response.text

soup = BeautifulSoup(data, "html.parser")

listings = soup.find_all('li', attrs={'class': 'sresult'})

for listing in listings:
    prod_name=" "
    prod_price = " "
    
    h3_lvtitle = listing.find('h3', attrs={'class':"lvtitle"})

    if (h3_lvtitle.a.title!="Nothing"):
        title = str(h3_lvtitle.a.contents[0]).replace("\r","").replace("\n","").replace("\t","")

        if (prod_name==" "):
            prod_name=f"{title}"
            item_names.append(title);
        #else:
            #prod_name=f"{prod_name},{title}"

    #If products are found, find the prices
    if(prod_name!=" "):
        li_lvprice = listing.find('li', attrs={'class':"lvprice"})
        price = str(li_lvprice.find('span', attrs={'class':"bold"}).contents[0]).removeprefix("\n\t\t\t\t\t")

        if (prod_price==" "):
            prod_price=f"{price}"
            item_prices.append(prod_price);
        #else:
            #prod_price=f"{prod_price},{price}"


from scipy import stats
import numpy as np
import pandas as pd

df = pd.DataFrame({"Name":item_names, "Prices": item_prices})
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