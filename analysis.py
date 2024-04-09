# note this is the final for analysing data and then posting it to the main python file 
import pandas as pd
from data import *
from allZipcode import *
from passwords import *
import time
# FUNCTIONS BELOW 
"""
Collect all zipcode data with state data
Put this data in a hashmap -> look ups will be O(1) complexity and will be used to verify that the data exists and that the state matches the zipcode provided for added credibility 
"""
# Data turned into a hashmap (dictionary)
"""zipcode_Data = {}

df = pd.read_csv('geo-data.csv')

for index, row in df.iterrows():
    zipcode = str(row['zipcode']).strip()

    # Check if the zipcode is numeric
    if zipcode.isnumeric():
        state = str(row['state_abbr']).strip()
        zipcode_Data[int(zipcode)] = state

print(zipcode_Data)"""


# As of 3/4 deleting the hashmap method to clean up space using the zipcode API 
# analyze the hashmap -> Note for 1/20 -> Further analyze the hashmap and check if the state value matches 
def searchAndVerify(zipData, zipCode, state):
    if zipCode in zipData:
        if zipData[zipCode] == state:
            return 'Correct state!'
        else:
            return 'Invalid state and zip combo'
    else:
        return 'Not Found'


# new search and verify using API 
"""def searchAndVerify(zipCode, state):
    # check if zipcode is valid first -> over/under 5 in length
    if len(zipCode) != 5:
        return 'Not Found'
    else:
        # implement the zipcode ai
        zipData = requests.get(f"https://api.zipcodestack.com/v1/search?codes={zipCode}&country=us&apikey={apiKey}")
        zipdata = zipData.json()
        # if no results than ZIPcode is invalid 
        resultTotal = len(zipdata['results'])

        if resultTotal == 0:
            return 'Not Found'
        
        else:
            # check if state and zipcode match 
            stateValue = zipdata['results'][zipCode][0]['state_code']
            if stateValue == state:
                return 'Correct state!'
            else:                
                return 'Invalid state and zip combo'
"""


     

# GRAB HOUSE AND THEN SENATE NAME
# key -> email, value - > name
def allData(state, zipcode):
    allRepData = {}

    # add the house rep  dictionary first 
    repData = represenativeNamesandEmails(zipcode)
    allRepData.update(repData)
    

    # add the senate data 
    #print(senatorData[state][0]) #
    # TWO SENATORS 
    allRepData[senatorData[state][0]] = senateNameEmail[senatorData[state][0]]
    allRepData[senatorData[state][1]] = senateNameEmail[senatorData[state][1]]

    return allRepData

#print(allData('NY', 11218))

#print(allData('NY', 11218))


