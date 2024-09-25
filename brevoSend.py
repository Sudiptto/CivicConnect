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

# send email verification email through brevo
def sendEmailVerificationEmail(sender, subject, content, to):
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, html_content=content, sender=sender, subject=subject)

    # error handling 
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)

def createEmailList(emails, names):
    # create a list of dictionaries
    emailList = []
    for i in range(len(emails)):
        emailList.append({"email": emails[i], "name": names[i]})
    return emailList

# Test the function
#print(createEmailList(["biswassudiptto@gmail.com", "max@gmail.com", "mad@gmail.com"], ["Sudiptto Biswas", "Max", "Mad"])) # should return a list of dictionaries

# function for sending email
def send_verification_email(email, randomNumber):
    # works -> send a verification email out to the user
    #print("Testing again for sendOnBehalf ", verification_data)
    
    body = f'''
        <div style="font-family:'Times New Roman', serif; padding:2rem; background-color:#f4f4f4;">
            <h1 style="text-align:center; color:#222; font-size:2rem; font-weight:bold; margin-bottom:2rem;">
                Verify Your Email
            </h1>
            <p style="font-size:1.1rem; color:#333; line-height:1.8;">
                Here is your 6-digit verification code: 
                <strong style="font-size:1.5rem; color:#003366;">{randomNumber}</strong>
                <br><br>
                Please enter this code on the verification page to confirm your email. If you do not receive the code within 5 minutes, kindly try again. We are working to improve email delivery times.
            </p>

            <hr style="border:0; border-top:1px solid #e0e0e0; margin:2rem 0;">
            <div style="text-align:center; font-size:1rem; color:#555; line-height:1.8;">
                <p style="margin-bottom:1.5rem;">
                    <a href="https://civicconnect.pythonanywhere.com/" 
                    style="color:#003366; text-decoration:underline;"
                    onmouseover="this.style.color='#0056b3';" 
                    onmouseout="this.style.color='#003366';">
                        Use CivicConnect
                    </a>
                </p>
                <p>
                    <a href="https://www.linkedin.com/company/civiccommunication" 
                    style="color:#003366; text-decoration:underline;"
                    onmouseover="this.style.color='#0056b3';" 
                    onmouseout="this.style.color='#003366';">
                        Follow us on LinkedIn
                    </a>
                </p>
            </div>
        </div>
    '''
    subject = 'Verify Your Email with a 6-Digit Code!'

    # send through BREVO:
    sender = {"name":"Civic Connect", "email":"send@civicconnect.net"}

    to = [{"email": email, "name": "User"}]

    # Brevo function
    sendEmailVerificationEmail(sender, subject, body, to)


# function to see account data
def getAccountData():
    api_instance = sib_api_v3_sdk.AccountApi(sib_api_v3_sdk.ApiClient(configuration))
    api_response = None
    try:
        api_response = api_instance.get_account()
        #pprint(api_response)
        
    except ApiException as e:
        print("Exception when calling AccountApi->get_account: %s\n" % e)

    return api_response

def getEmailRemaining():

    userData = getAccountData()
    emailsRemaining = userData.plan[0].credits
    emailsRemaining = int(emailsRemaining)

    return emailsRemaining

# if there are emails left
def didEmailRanOut(emailsLeft):
    if getEmailRemaining() <= emailsLeft:
        return True
    else:
        return False

#print(getAccountData())
#print(getEmailRemaining())