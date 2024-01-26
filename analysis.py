import pandas as pd
from allZipcode import *
import time
# FUNCTIONS BELOW 
"""
Collect all zipcode data with state data
Put this data in a hashmap -> look ups will be O(1) complexity and will be used to verify that the data exists and that the state matches the zipcode provided for added credibility 
"""
# Data turned into a hashmap 
"""zipcode_Data = {}

df = pd.read_csv('geo-data.csv')

for index, row in df.iterrows():
    zipcode = str(row['zipcode']).strip()

    # Check if the zipcode is numeric
    if zipcode.isnumeric():
        state = str(row['state_abbr']).strip()
        zipcode_Data[int(zipcode)] = state

print(zipcode_Data)"""

# analyze the hashmap -> Note for 1/20 -> Further analyze the hashmap and check if the state value matches 
def searchAndVerify(zipData, zipCode, state):
    if zipCode in zipData:
        if zipData[zipCode] == state:
            return 'Correct state!'
        else:
            return 'Invalid state and zip combo'
    else:
        return 'Not Found'
    
print(searchAndVerify(zipcodeData, 11218, 'NY'))
print(searchAndVerify(zipcodeData, 11218, 'WY'))
print(searchAndVerify(zipcodeData, 11200, 'NY'))


# Note for future: analysis on the length of zipcode, only consider the zipcodes whos lengths are 5 to be eligible and the zipcodes whos lengths are 4 or not 5 to uneligible 