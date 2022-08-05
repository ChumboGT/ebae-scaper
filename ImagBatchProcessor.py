import numpy as np
import pandas as pd

#Read the Data into a Pandas Data Frame (Only Item Number and Image URL)
listings_df = pd.read_csv ('C:\_github\python\eBayScraper-listings.csv')#,usecols= ['Item Number','Image URL'])
listings_df.reset_index() 

#For Each of the image links, we will need to:
### 1 -> Send the Jpg to the Azue Vision API
### 2 -> Take the Extracted Information, store in Pipe-Delimited Format, tagged with the Item Number.
### 3 -> Make sure there is an open/close of the file so we don't lose progress, could be long-running!

for index, row in listings_df.iterrows():
    print(index, row['Item Number'], row['Image URL'])