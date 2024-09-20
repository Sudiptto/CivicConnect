from flask import Blueprint, request, flash, redirect, url_for, session
from app import *
from passwords import *
import secrets
from analysis import *
from addData import *
from brevoSend import *


# Create a Blueprint instance
email_bp = Blueprint('email_bp', __name__)

def send_verification_email(email, token, reasoning):



    if reasoning == "sendOnBehalf":
        # works -> send a verification email out to the user
        #print("Testing again for sendOnBehalf ", verification_data)
        verification_link = url_for('email_bp.verify_email', token=token, reasoning = reasoning, _external=True)

        body = f'''
            <div style="font-family:'Times New Roman', serif; padding:2rem; background-color:#f4f4f4;">
                <h1 style="text-align:center; color:#222; font-size:2rem; font-weight:bold; margin-bottom:2rem;">
                    Verify Email
                </h1>
                <p style="font-size:1.1rem; color:#333; line-height:1.8;">
                    Please click the following link to <strong>verify your email</strong>: 
                    <a href="{verification_link}" 
                    style="color:#003366; text-decoration:underline;"
                    onmouseover="this.style.color='#0056b3';" 
                    onmouseout="this.style.color='#003366';">
                        {verification_link}
                    </a>
                    <br>
                    Please stay on the page for a few seconds to ensure the email is processed and sent. Occasionally, emails may not be delivered due to budget constraints. 
                    If you do not receive an email within 5 minutes, kindly try again. We are working to improve email delivery times.
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
        subject = 'Verify Your Email!'
        msg = Message(subject, recipients=[email], html=body)
        mail.send(msg)



# VERIFY EMAIL
@email_bp.route('/generate_token_and_send_email', methods=['POST'])
def generate_token_and_send_email():
    if request.method == 'POST':
        # Access form data
        email = request.form['email']
        reasoning = request.form['reasoning']
        # Generate a unique token
        verification_token = secrets.token_hex(16)


        if reasoning == "sendOnBehalf":
            print("Send on behalf activated ")

        # Redirect to the route responsible for sending the email
        return redirect(url_for('send_verification_email_route', email=email, token=verification_token))


# send the email to the user
@email_bp.route('/send_verification_email/<email>/<token>/<reasoning>', methods=['GET'])
def send_verification_email_route(email, token, reasoning):
    if reasoning == 'sendOnBehalf':
        """repEmails = verification_data.get('repEmails')
        repNames = verification_data.get('repNames')
        subject = verification_data.get('subject')
        prompt = verification_data.get('prompt')"""

        send_verification_email(email, token, reasoning=reasoning)
        #print(verification_data)


        print('Send on behalf activated!!')

    return redirect(url_for('home'))





# route where email gets sent to me (civic connect email)
@email_bp.route('/verify_email/<token>/<reasoning>', methods=['GET'])
def verify_email(token, reasoning):
    # Check if the token is in the dictionary
    if token in token_data:
        # Retrieve data associated with the token
        data = token_data.pop(token)
        print("All data gotten: ", data)
        # Set a session variable to indicate email verification
        if reasoning == 'sendOnBehalf':
            # - > worked
            #print("Testing at this app route worked!")

            # change the repEmails to seperate emails (for testing -> not final product )
            # site for disposable emails - > https://temp-mail.org/en/

            print(data)

            userEmail = data['email']

            # send the email (use the emailName gmail) to the reps and cc the user email(the user who sent it and have the subject be the prompt)
            subject = data['subject']
            prompt = data['prompt']
            repEmails = data['repEmails']
            repNames = data['repNames']
            firstName = data['firstName']
            
            # firstName -> works 
            print("First name: ", firstName)
            
            print("DATA BELOW: ")

            print("repEmails: ", repEmails)
            print("repNames: ", repNames)

            # test createEmailList function
            print(createEmailList(repEmails, repNames))

            # send the email to the reps -> send one email and send it to all of the rep email addresses

            body = f'''
                <div style="background-color:#f9f9f9;padding:2rem;font-family:Arial,sans-serif;">
                    <div style="background-color:#fff;padding:2rem;border-radius:0.625rem;box-shadow:0 0.25rem 0.5rem rgba(0,0,0,0.1);">
                        <h1 style="text-align:center;color:#222;font-size:2.5rem;font-weight:bold;margin-bottom:1.5rem;text-decoration:underline;">
                            {subject}
                        </h1>
                        <p style="font-size:1rem;color:#555;"><strong>Email:</strong> {userEmail}</p>
                        <p style="font-size:1rem;color:#555;"><strong>Prompt:</strong></p>
                        <div style="padding-left:1.25rem;font-family:'Times New Roman', serif;font-size:1.2rem;line-height:2rem;color:#333;background-color:#f0f0f0;border-left:0.25rem solid #007bff;padding:1rem;">
                            {prompt[:-14]}
                        </div>
                        <p style="font-size:0.875rem;color:#777;margin-top:1.5rem;">
                            This email was sent via the CivicConnect email on behalf of <strong>{userEmail}</strong>.
                        </p>
                        <hr style="border:0;border-top:0.0625rem solid #e0e0e0;margin:1.5rem 0;">
                        <p style="text-align:center;font-size:1rem;color:#555;">
                            <a href="https://civicconnect.pythonanywhere.com/" style="background-color:#007bff;color:#fff;padding:0.5rem 1rem;border-radius:0.25rem;text-decoration:none;">
                                Use CivicConnect Here
                            </a>
                        </p>
                        <p style="text-align:center;font-size:1rem;color:#555;">
                            <a href="https://www.linkedin.com/company/civiccommunication" style="background-color:#007bff;color:#fff;padding:0.5rem 1rem;border-radius:0.25rem;text-decoration:none;">
                                Follow us on LinkedIn to see the journey
                            </a>
                        </p>
                    </div>
                </div>

            '''
            # sender info and cc email name information
            sender = {"name":"Civic Connect", "email":"send@civicconnect.net"}
            cc = [{"email": userEmail, "name": firstName}]

            # get back array of objects for repEmails
            repEmailObject = createEmailList(repEmails, repNames)

            # Reply to email
            reply_to = {"email":"civic@civicconnect.net","name":"Civic Connect"}

            # Old Flask mail -> USE BREVO instead
            #send_msg = Message(subject, sender=userEmail, recipients=repEmails, cc=[userEmail], html=body)

            #mail.send(send_msg)

            # BREVO email send
            sendEmailThroughBrevo(sender, subject, body, repEmailObject, cc, reply_to)

            # get the zipcode and the subject and send the data to the analytics file
            zipCode = int(prompt[-5:])

            #print("Check if zipCode exists: ", zipCode)
            print("User Email: ", userEmail)
            print("Subject: ", subject)
            print("ZipCode: ", zipCode)
            print("Representative Names: ", repNames) # this is an array
            
            # functions below are to add the data into the database
            add_unique_email(userEmail, zipCode)
            add_or_increment_topic(subject)
            update_zipcode_data(zipCode, subject)

            for rep in repNames:
                update_representative_data(rep, subject)

            


    # fix this part down here
    else:
        flash('Invalid or expired verification link.', category='error')
    session.clear()

    return redirect(url_for('verifyEmailSuccess', verified="true"))