# This python file is responsible for tracking the number of emails (using CSV)

# what the columns will consist of
# ZipCode, #Email Sent: Southern Border (mailto), #Email Sent: Free Palestine (mailto), #Email Sent: Affordable Housing (mailto), #Email Sent: Affordable Housing(mailto), #Email Sent: Southern Border (Through CivicConnect), #Email Sent: Free Palestine (Through CivicConnect), #Email Sent: Affordable Housing (Through CivicConnect), #Email Sent: Affordable Housing (Through CivicConnect), #Total Emails (mailto), #Total Emails (Through CivicConnect), #Total Emails

import pandas as pd

# read data 
df = pd.read_csv('analytics.csv')
#print(df)

# add zipcode first thing
def add_zipcode(zipcode):
    zipcode = int(zipcode)
    # Define the column headers
    headers = ["ZipCode",
               "#Email Sent: Southern Border (mailto)",
               "#Email Sent: Free Palestine (mailto)",
               "#Email Sent: Affordable Housing (mailto)",
               "#Email Sent: Abortion (mailto)",

               "#Email Sent: Southern Border (Through CivicConnect)",
               "#Email Sent: Free Palestine (Through CivicConnect)",
               "#Email Sent: Affordable Housing (Through CivicConnect)",
               "#Email Sent: Abortion (Through CivicConnect)",
               "#Total Emails (mailto)",

               "#Total Emails (Through CivicConnect)",
               "#Total Emails"]

    # Check if the zipcode doesn't exist
    if zipcode not in df['ZipCode'].values:
        num_rows = len(df.index)

        # Create a new row with the zipcode and all other columns set to 0
        new_row = [zipcode] + [0] * (len(headers) - 1)

        # Add the new row to the DataFrame at the end
        df.loc[num_rows] = new_row

    # if zipcode already exists
    else:
        print(f"Zipcode {zipcode} already exists in the DataFrame.")
        return df

    # Write the updated data back to the CSV file
    df.to_csv('analytics.csv', index=False)
    return df

# dictionary with subject and column name (for the emails through CivicConnect)
civic_dict = {
    "Southern Border": "Southern Border (Through CivicConnect)",
    "Free Palestine": "Free Palestine (Through CivicConnect)",
    "Affordable Housing": "Affordable Housing (Through CivicConnect)",
    "Abortion": "Abortion (Through CivicConnect)"}

# dictionary with subject and column name (for the emails through mailto)
mailto_dict = {
    "Southern Border": "Southern Border (mailto)",
    "Free Palestine": "Free Palestine (mailto)",
    "Affordable Housing": "Affordable Housing (mailto)",
    "Abortion": "Abortion (mailto)"
}

def trackData(zipcode, subject, route):
    # check if zipcode exists
    zipcode = int(zipcode)
    df = add_zipcode(zipcode)

    # check between the two routes
    if route == "CivicConnectEmail":
        # get column name based on subject
        columnName = civic_dict[subject]
        updateColumn = "Total Emails (Through CivicConnect)"

    elif route == "MailTo":
        columnName = mailto_dict[subject]
        updateColumn = "Total Emails (mailto)"

    # locate row index (same as zipcode) and increment the value by 1 (on the corresponding rows)
    row_index = df.index[df['ZipCode'] == zipcode]

    # incremenent to the subject, Total Emails (Through CivicConnect) and Total Emails
    df.loc[row_index, columnName] += 1
    df.loc[row_index, updateColumn] += 1
    df.loc[row_index, "Total Emails"] += 1

    df.to_csv('analytics.csv', index=False)

"""trackData(11215, "Free Palestine", "CivicConnectEmail")
trackData(11218, "Southern Border", "CivicConnectEmail")
trackData(11216, "Southern Border", "CivicConnectEmail")
trackData(30321, "Southern Border", "CivicConnectEmail")
trackData(11218, "Southern Border", "CivicConnectEmail")
trackData(11218, "Southern Border", "CivicConnectEmail")
trackData(11215, "Poverty", "CivicConnectEmail")
trackData(11218, "Affordable Housing", "CivicConnectEmail")
trackData(11218, "Southern Border", "CivicConnectEmail")"""

#trackData(11218, "Southern Border", "CivicConnectEmail")
# Create an empty DataFrame


# USE THESE BELOW TO CLEAR THE DATA IN THE CSV FILE


"""df = pd.DataFrame()
column_names = ['ZipCode', 'Southern Border (mailto)', 'Free Palestine (mailto)', 'Affordable Housing (mailto)', 'Abortion (mailto)', 'Southern Border (Through CivicConnect)', 'Free Palestine (Through CivicConnect)', 'Affordable Housing (Through CivicConnect)', 'Abortion (Through CivicConnect)', 'Total Emails (mailto)', 'Total Emails (Through CivicConnect)', 'Total Emails']


df = pd.DataFrame(columns=column_names)


df.to_csv('analytics.csv', index=False)"""