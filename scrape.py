import requests
from bs4 import BeautifulSoup
# PLEASE NOTE: THIS IS FOR ONE TIME DATA USE FOLLOW THE COMMENTS !
# STATE ABBREVIATIONS DATA WILL BE USED LATER
state_abbreviations = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

# Wikipedia URL with the table
url = 'https://en.wikipedia.org/wiki/List_of_current_United_States_senators'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')


# Two lists- One all states, second is a matrix (2D array) of all senator names per state (use the state abbreviation to get the abbreviation data ) -> then make dictionary at END (note not that efficient but data is for ONE TIME USE )
stateData = []
senatorNames = []
# note as of jan 2024 this is the 5th table on wikipedia
senator_table = soup.find_all('table', {'class': 'wikitable'})[4]

# STATE DATA -> ABBREVIATION
for row in senator_table.find_all('tr')[1:]:  # Skipping the header row
    columns = row.find_all(['th', 'td'])  # Include both th and td

    # Extract relevant data
    state = columns[0].get_text(strip=True)

    # Check if state is not an empty string
    if state:
        stateData.append(state_abbreviations[state])


# senator data 
# Iterate through each row in the table
for row in senator_table.find_all('tr')[1:]:
    # Extract text content of each cell in the row
    row_content = [col.get_text(strip=True) for col in row.find_all(['th', 'td'])]
    senatorNames.extend([row_content[1], row_content[2]]) # either one can be the senator 

# remove all the empty '' characters
finalSenateData = []
for i in range(len(senatorNames)):
    if senatorNames[i] != '':
        finalSenateData.append(senatorNames[i])

# NOW ALL THE SENATOR NAMES ARE THERE IN ORDER
#print(finalSenateData) # print
#print(len(finalSenateData)) # print
        
# Logic -> each state has two senators in order so use a dictionary to store
# Example: {stateAbr: [senator1, senator2]}
        
stateSenator = {}

# two pointer

senator1 = 0
senator2 = 1
states = 0

while senator2 < len(finalSenateData):
    senatorByState = []
    senatorByState.append(finalSenateData[senator1])
    senatorByState.append(finalSenateData[senator2])

    stateSenator[stateData[states]] = senatorByState

    states += 1
    senator1 += 2
    senator2 += 2

#print(stateSenator)    
#print(len(stateSenator)) # print
# DATA FOR 2024 JANUARY

currentSenateData = {'AL': ['Tommy Tuberville', 'Katie Britt'], 'AK': ['Lisa Murkowski', 'Dan Sullivan'], 'AZ': ['Kyrsten Sinema', 'Mark Kelly'], 'AR': ['John Boozman', 'Tom Cotton'], 'CA': ['Alex Padilla', 'Laphonza Butler'], 'CO': ['Michael Bennet', 'John Hickenlooper'], 'CT': ['Richard Blumenthal', 'Chris Murphy'], 'DE': ['Tom Carper', 'Chris Coons'], 'FL': ['Marco Rubio', 'Rick Scott'], 'GA': ['Jon Ossoff', 'Raphael Warnock'], 'HI': ['Brian Schatz', 'Mazie Hirono'], 'ID': ['Mike Crapo', 'Jim Risch'], 'IL': ['Dick Durbin', 'Tammy Duckworth'], 'IN': ['Todd Young', 'Mike Braun'], 'IA': ['Chuck Grassley', 'Joni Ernst'], 'KS': ['Jerry Moran', 'Roger Marshall'], 'KY': ['Mitch McConnell', 'Rand Paul'], 'LA': ['Bill Cassidy', 'John Kennedy'], 'ME': ['Susan Collins', 'Angus King'], 'MD': ['Ben Cardin', 'Chris Van Hollen'], 'MA': ['Elizabeth Warren', 'Ed Markey'], 'MI': ['Debbie Stabenow', 'Gary Peters'], 'MN': ['Amy Klobuchar', 'Tina Smith'], 'MS': ['Roger Wicker', 'Cindy Hyde-Smith'], 'MO': ['Josh Hawley', 'Eric Schmitt'], 'MT': ['Jon Tester', 'Steve Daines'], 'NE': ['Deb Fischer', 'Pete Ricketts'], 'NV': ['Catherine Cortez Masto', 'Jacky Rosen'], 'NH': ['Jeanne Shaheen', 'Maggie Hassan'], 'NJ': ['Bob Menendez', 'Cory Booker'], 'NM': ['Martin Heinrich', 'Ben Ray Luján'], 'NY': ['Chuck Schumer', 'Kirsten Gillibrand'], 'NC': ['Thom Tillis', 'Ted Budd'], 'ND': ['John Hoeven', 'Kevin Cramer'], 'OH': ['Sherrod Brown', 'J. D. Vance'], 'OK': ['James Lankford', 'Markwayne Mullin'], 'OR': ['Ron Wyden', 'Jeff Merkley'], 'PA': ['Bob Casey Jr.', 'John Fetterman'], 'RI': ['Jack Reed', 'Sheldon Whitehouse'], 'SC': ['Lindsey Graham', 'Tim Scott'], 'SD': ['John Thune', 'Mike Rounds'], 'TN': ['Marsha Blackburn', 'Bill Hagerty'], 'TX': ['John Cornyn', 'Ted Cruz'], 'UT': ['Mike Lee', 'Mitt Romney'], 'VT': ['Bernie Sanders', 'Peter Welch'], 'VA': ['Mark Warner', 'Tim Kaine'], 'WA': ['Patty Murray', 'Maria Cantwell'], 'WV': ['Joe Manchin', 'Shelley Moore Capito'], 'WI': ['Ron Johnson', 'Tammy Baldwin'], 'WY': ['John Barrasso', 'Cynthia Lummis']}

