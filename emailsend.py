from flask import Blueprint, request, flash, redirect, url_for, session
from flask_mail import Mail, Message
from app import *
from passwords import *
import secrets
from analysis import *
from addData import *


# Create a Blueprint instance
email_bp = Blueprint('email_bp', __name__)

# Initialize Flask-Mail
mail = Mail(app)

def send_verification_email(email, token, reasoning):
    # to send the verification email use a different email address (for sending)
    app.config["MAIL_USERNAME"] = verifyCivicEmail
    app.config["MAIL_PASSWORD"] = verifyCivicAppPass

    # create new mail object
    verify_mail = Mail(app)

    verification_data = token_data.get(token, {})

    if reasoning == 'queries':

        optionChosen = verification_data.get('selectOption')
        promptCritique = verification_data.get('promptCritique')
        subject = 'Verify Your Email for Query'
        verification_link = url_for('email_bp.verify_email', token=token, reasoning = reasoning, _external=True)

        body = f'Click the following link to verify your email: {verification_link} <br> <b>Here is your inputs:</b> <br> <p>Option chosen: {optionChosen} <br> {promptCritique} '

        msg = Message(subject, recipients=[email], html=body)
        verify_mail.send(msg)

    elif reasoning == "sendOnBehalf":
        # works -> send a verification email out to the user
        #print("Testing again for sendOnBehalf ", verification_data)
        verification_link = url_for('email_bp.verify_email', token=token, reasoning = reasoning, _external=True)
        body = f'Click the following link to verify your email: {verification_link} <br>'
        subject = 'Verify Your Email!'
        msg = Message(subject, recipients=[email], html=body)
        verify_mail.send(msg)

        app.config["MAIL_USERNAME"] = emailName
        app.config["MAIL_PASSWORD"] = emailPassword


# VERIFY EMAIL
@email_bp.route('/generate_token_and_send_email', methods=['POST'])
def generate_token_and_send_email():
    if request.method == 'POST':
        # Access form data
        email = request.form['email']
        selectOption = request.form['emailReason']
        promptCritique = request.form['critique']
        reasoning = request.form['reasoning']
        # Generate a unique token
        verification_token = secrets.token_hex(16)

        if reasoning == 'queries':
        # Store the token and associated data in the dictionary
            token_data[verification_token] = {
                'email': email,
                'selectOption': selectOption,
                'promptCritique': promptCritique
            }

        elif reasoning == "sendOnBehalf":
            print("Send on behalf activated ")

        # Redirect to the route responsible for sending the email
        return redirect(url_for('send_verification_email_route', email=email, token=verification_token))


# send the email to the user
@email_bp.route('/send_verification_email/<email>/<token>/<reasoning>', methods=['GET'])
def send_verification_email_route(email, token, reasoning):
    if reasoning == 'queries':
        send_verification_email(email, token, reasoning=reasoning)
        flash('Verification link sent to your email. Reasoning: ' + reasoning, category='info')

    elif reasoning == 'sendOnBehalf':
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
        if reasoning == 'queries':
            session['email_verified'] = True
            session['email'] = data['email']

            promptCritique = data['promptCritique']
            optionChosen = data['selectOption']
            email = data['email']

            flash('Email verified.', category='success')


            # send the prompt email to us -> only after verification
            subject = f'User Prompt: {optionChosen}'
            body = f'<div style="background-color:#f2f2f2;padding:20px;"><h2 style="color:#333;">User Prompt Details</h2><p><strong>Email:</strong> {email}</p><p><strong>Option chosen:</strong> {optionChosen}</p><p><strong>Prompt Critique:</strong></p><div style="padding-left:20px;">{promptCritique}</div></div>'
            msg2 = Message(subject, sender=data['email'], recipients=[emailName], cc = [email], html=body)
            mail.send(msg2)
            flash('Email sent successfully! Check inbox for more', category='error')

        elif reasoning == 'sendOnBehalf':
            # - > worked
            #print("Testing at this app route worked!")

            # change the repEmails to seperate emails (for testing -> not final product )
            # site for disposable emails - > https://temp-mail.org/en/
            repEmailFake = ["fejime7164@ekposta.com", "test@gmail.com"]
            repNames = ["Testing1", "Testing2"]
            data['repEmails'] = repEmailFake
            data["repNames"] = repNames

            print(data)

            userEmail = data['email']

            # send the email (use the emailName gmail) to the reps and cc the user email(the user who sent it and have the subject be the prompt)
            subject = data['subject']
            prompt = data['prompt']
            repEmails = data['repEmails']
            repNames = data['repNames']

            # send through the sendcivic gmail (not verifycivic gmail)
            app.config["MAIL_USERNAME"] = sendEmail
            app.config["MAIL_PASSWORD"] = sendPassword
            
            # create new mail object
            send_mail = Mail(app)
            

            # send the email to the reps -> send one email and send it to all of the rep email addresses

            body = f'<div style="background-color:#f2f2f2;padding:20px;"><h2 style="color:#333;">{subject}</h2><p><strong>Email:</strong> {userEmail}</p><p><strong>Subject:</strong> {subject}</p><p><strong>Prompt:</strong></p><div style="padding-left:20px;">{prompt[:-14]}</div><p>This email was sent via the CivicConnect email on behalf of {userEmail}.</p></div>'
            send_msg = Message(subject, sender=userEmail, recipients=repEmails, cc=[userEmail], html=body)

            send_mail.send(send_msg)

            # get the zipcode and the subject and send the data to the analytics file
            zipCode = int(prompt[-5:])

            #print("Check if zipCode exists: ", zipCode)
            print("User Email: ", userEmail)
            print("Subject: ", subject)
            print("ZipCode: ", zipCode)
            print("Representative Names: ", repNames) # this is an array

            #print("Final place before email is sent: ")
            
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