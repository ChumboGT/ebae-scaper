import numpy as np
import pandas as pd

#From Azure Example#
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time
#End Example Imports

sub_key = '2e4572e51b80421a96daf2fcfe9fe700'
sub_sub_key = '2fdee91697114319b9506503d66a3549'
comp_vision_endpoint = 'https://arepotech-cv.cognitiveservices.azure.com/'

#Read the Data into a Pandas Data Frame (Only Item Number and Image URL)
listings_df = pd.read_csv ('C:\_github\python\eBayScraper-listings.csv')#,usecols= ['Item Number','Image URL'])
listings_df.reset_index() 

computervision_client = ComputerVisionClient(comp_vision_endpoint, CognitiveServicesCredentials(sub_key))

### EXAMPLE CODE BEGINS!!!#

for row in listings_df.head(5).itertuples():
    item_number = int(row[6])
    img_url = str(row[7])

    print(item_number, str(img_url))

    print("===== Read File - remote =====")
    # Get an image with text
    read_image_url = img_url

    # Call API with URL and raw response (allows you to get the operation location)
    read_response = computervision_client.read(read_image_url,  raw=True)

    # Get the operation location (URL with an ID at the end) from the response
    read_operation_location = read_response.headers["Operation-Location"]
    # Grab the ID from the URL
    operation_id = read_operation_location.split("/")[-1]

    # Call the "GET" API and wait for it to retrieve the results 
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status not in ['notStarted', 'running']:
            break
        time.sleep(1)

    # Print the detected text, line by line
    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                print(line.text)
                print(line.bounding_box)
    print()
    '''
    END - Read File - remote
    '''

    print("End of Computer Vision quickstart.")
### END EXAMPLE CODE! ###


#For Each of the image links, we will need to:
### 1 -> Send the Jpg to the Azue Vision API
### 2 -> Take the Extracted Information, store in Pipe-Delimited Format, tagged with the Item Number.
### 3 -> Make sure there is an open/close of the file so we don't lose progress, could be long-running!

# -> Old, may not need ->> for index, row in listings_df.iterrows():


#for row in listings_df.head(5).itertuples():
#    item_number = int(row[6])
#    img_url = str(row[7])

#    print(item_number, str(img_url))