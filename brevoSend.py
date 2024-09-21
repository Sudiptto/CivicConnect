from __future__ import print_function
import time
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from pprint import pprint
from passwords import *

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = brevoApiKey

api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))


# Variable types:
"""
sender = {"name":"Civic Connect", "email":"send@domain.net"} -> Dictionary 

subject = "Important Update from Our Team" -> String

html_content = "THIS IS FIRST EMAIL" -> String

to = [{"email":"example1@gmail.com","name":"Joe SShmo"}, {"email":"example2@gmail.com","name":"Jane Doe"}] -> List of Dictionaries

cc = [{"email":"example3@gmail.com","name":"Sudiptto Biswas"}] -> List of Dictionaries

reply_to = {"email":"civic@domain.net","name":"Civic Connect"} -> Dictionary

headers = {"Some-Custom-Name":"unique-id-1234"} -> headers

params = {"parameter":"My param value","subject":"New Subject"}

Note -> Can add BCC as well
"""


def sendEmailThroughBrevo(sender, subject, content, to, cc, reply_to):

    # send email through brevo
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, cc=cc, reply_to=reply_to, html_content=content, sender=sender, subject=subject)

    # error handling 
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)


# Function to turn turn a list of email addresses / names into a list of dictionaries
# Like this: [ {"email":"example3@gmail.com","name":"Sudiptto Biswas"}, {"email":"sud@gmail.com","name":"Sud"} ]

def createEmailList(emails, names):
    # create a list of dictionaries
    emailList = []
    for i in range(len(emails)):
        emailList.append({"email": emails[i], "name": names[i]})
    return emailList

# Test the function
#print(createEmailList(["biswassudiptto@gmail.com", "max@gmail.com", "mad@gmail.com"], ["Sudiptto Biswas", "Max", "Mad"])) # should return a list of dictionaries
