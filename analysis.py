import pandas as pd
from allZipcode import *
import time
# Strategy
"""
Collect all zipcode data, put it in a seperate list and sort it
After sorting it we can use binary search to verify the zipcode info (log(n) complexity )
"""
# As of 1/20/2024 -> Data has been extracted and all the zipcode data is sorted least to greatest in the allZipcode.py folder -> Please refer to that for any zipcode checking 
#data = pd.read_csv('geo-data.csv')
#print(data['zipcode'])
#zipcode = list(data['zipcode'])
#print(zipcode)

# BINARY SEARCH FOR THE ZIPCODE
#zipcode = zipcode
#start_time = time.time()
def binaryZipSearch(zipcode, target):
    l = 0
    u = len(zipcode) - l
    while l <= u:
        medium = (l + u) // 2
        if zipcode[medium] == target:
            return 'FOUND'
        else:
            if zipcode[medium] < target:
                l = medium + 1
            else:
                u = medium - 1
    return 'None'

# WORKS 
print(binaryZipSearch(zipcode, 99950))
print(binaryZipSearch(zipcode, 11100)) 

# Around 1 ms
"""end_time = time.time()
execution_time = (end_time - start_time) * 1000
# 1.001 -> Milliseconds 
print(f"Execution Time: {execution_time} millisecondss")"""

