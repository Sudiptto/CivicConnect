from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
from app import *
from allZipcode import *
import secrets
from passwords import *
from analysis import *
from prompts import *
from emailsend import email_bp  # Import the blueprint from emailsend.py
from models import *  # Import the db and User model
import random

# Configure Flask-Mail settings
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
# mail username and password will change based on sending vs recieving email -> default recieving email
app.config["MAIL_USERNAME"] = sendEmail
app.config["MAIL_PASSWORD"] = sendPassword
app.config["MAIL_DEFAULT_SENDER"] = 'your_email@example.com'
mail.init_app(app)

# Register the email_bp Blueprint with the app
app.register_blueprint(email_bp)

# for re-captcha
RECAPTCHA_SECRET_KEY = privateCaptcha  

# start page
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # for captcha
        recaptcha_response = request.form.get('g-recaptcha-response')

        if not recaptcha_response:
            flash('Please complete the reCAPTCHA.', category='error')
            
        
        # Verify reCAPTCHA
        payload = {
            'secret': RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        recaptcha_verification = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
        result = recaptcha_verification.json()

        if not result.get('success'):
            flash('reCAPTCHA verification failed. Please try again.', category='error')
            return redirect(url_for('home'))
        

        # Access form data
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        zip_code = request.form['zipCode'] # turn to integer -> after we check if its numeric
        state = request.form['state']

        # VALIDATE IS ZIPCODE IS NUMERIC
        if zip_code.isnumeric() == False:
            flash("Please enter a valid 5 DIGIT INTEGER zipcode", category="error")


        # VALIDATE BOTH ZIP AND CITY DATA -> DONT USE THE API FOR NOW
        validateZipState = searchAndVerify(zipcodeData, zip_code, state)


        if validateZipState == 'Correct state!':
            #print('test')
            #flash('Correct Move on!', category='error')
            session['valid_zip_state'] = True

            # Encrypt -> First Name, Last Name and Email  -> use sha256
            session['first_name'] = first_name
            session['ZipCode'] = zip_code
            session['state'] = state

            return redirect(url_for('causes'))

        elif validateZipState == 'Invalid state and zip combo':
            session['valid_zip_state'] = False
            flash('Invalid state and zip combo', category='error')

        else:
            session['valid_zip_state'] = False
            flash('Incorrect zipcode', category='error')



    return render_template('home.html')


# this is the causes page
@app.route('/causes',  methods=['GET', 'POST'])
def causes():
    if not session.get('valid_zip_state'):
        errorMessage = 'Incomplete'
        return render_template('error.html', errorMessage=errorMessage)

    first_name = session.get('first_name')
    zipCode = session.get('ZipCode') #  integer
    state = session.get('state')

    allReps = allData(state, zipCode)
    nameList = list(allReps.values())
    emailList = list(allReps.keys())

    #print(emailList)
    # create new session for emailList and nameList
    session['allReps'] = allReps
    session['nameList'] = nameList
    session['emailList'] = emailList
    # NOTE WORKS -> REDIRECT TO AN EMAIL route (final route )
    if request.method == 'POST':

        cause = request.form['cause']
    
        # SESSION FOR EMAIL ROUTE
        session['validSubmit'] = True
        session['causeSubject'] = cause
        return redirect(url_for('email'))

    # check prompts.py for getAllPrompts()
    return render_template('causes.html', firstName = first_name, nameList = nameList, emailList = emailList, allPrompts = getAllPrompts(first_name))



# works
@app.route('/email', methods=['GET', 'POST'])
def email():
    if not session.get('valid_zip_state'):
        errorMessage = 'Incomplete'
        return render_template('error.html', errorMessage = errorMessage)

    if not session.get('validSubmit'):
        errorMessage = 'NoSubmit'
        return render_template('error.html', errorMessage = errorMessage)

    # grab all information:
    first_name = session.get('first_name')
    zipCode = session.get('ZipCode') #  integer
    state = session.get('state')
    # email and name
    emailList = session.get('emailList')
    nameList = session.get('nameList')

    # get back dictionary
    allReps = session.get('allReps')

    # subject and prompt
    subject = session.get('causeSubject')
    prompt = subjectPrompt(subject, first_name, nameList, str(zipCode))


    return render_template('email.html', emailList=emailList, firstName = first_name, subject=subject, prompt=prompt, allReps=allReps, zipCode=zipCode)


# email for verified email addresses
@app.route('/verifyEmailSuccess/<verified>')
def verifyEmailSuccess(verified):
    #print(verified)
    if verified == 'true':
        # ISSUE FROM HERE THIS IS WHERE LAG HAPPENS
        print('Email verified! -> valid!! ')
    else:
        print("REDIRECT")
        return redirect(url_for('home'))

    return render_template('emailVerified.html')

# get the email from the fetch request from the email page  (javascript) and print out the email
@app.route('/email_sent', methods=['POST'])
def email_sent():
    data = request.get_json()

    email = data['email']
    repEmails = data['repEmails']
    repNames = data['repNames']
    subject = data['subject']
    prompt = data['prompt']
    firstName = session.get("first_name")

    print("Email sent has been hit")
    # Generate a random 6-digit verification code
    verification_code = random.randint(100000, 999999)

    print("Verification code: ", verification_code)

    # Store the relevant data in the session (no need to use tokens anymore)
    session['verification_code'] = verification_code
    session['email'] = email
    session['repEmails'] = repEmails
    session['repNames'] = repNames
    session['subject'] = subject
    session['prompt'] = prompt
    session['firstName'] = firstName

    # make a session saying verification email has been sent
    session['verification_email_sent'] = True

    # Send the verification email
    send_verification_email(email, verification_code)

    # Return JSON indicating success
    return jsonify({'status': 'success', 'redirect_url': url_for('verifyEmail')})

# Verify email
@app.route('/verifyEmail', methods=['GET', 'POST'])
def verifyEmail():

    # verify if user filled out correct information
    if not session.get('valid_zip_state'):
        errorMessage = 'Incomplete'
        return render_template('error.html', errorMessage=errorMessage)

    if not session.get('validSubmit'):
        errorMessage = 'NoSubmit'
        return render_template('error.html', errorMessage=errorMessage)

    if not session.get('verification_email_sent'):
        errorMessage = 'NoSubmitEmail'
        return render_template('error.html', errorMessage=errorMessage)
    
    # grab session data
    verification_code = session.get('verification_code')
    email = session.get('email')
    repEmails = session.get('repEmails')
    repNames = session.get('repNames')
    subject = session.get('subject')
    prompt = session.get('prompt')
    firstName = session.get('firstName')

    # create session
    session['send_again'] = 0

    print("Verification code (verifyEmail): ", verification_code)

    if request.method == 'POST':
        # Gather user input from the form
        user_code = ''.join([request.form.get(f'digit{i}') for i in range(1, 7)])

        # Verify the code
        if user_code == str(verification_code):
            # Handle successful verification (e.g., send email, redirect)
            return "WORKED"  # Replace this with your success handling
        else:
            flash("TRY AGAIN, WRONG CODE")
            return redirect(url_for('verifyEmail'))  # Redirect to the same route to show the message

    # Render the verification page with the verification code
    return render_template('verification.html', verification_code=verification_code, email=email, repEmails=repEmails, repNames=repNames, subject=subject, prompt=prompt, firstName=firstName)


# Send the verification email again
@app.route('/send_again', methods=['POST'])
def send_again():
    data = request.get_json()
    email = data['email']

    # create session variable to track how many time send_again was used
    session['send_again'] = session.get('send_again') + 1
    print(session.get('send_again'))

    if session['send_again'] >= 3:
        print("LOL")
        # clear session
        session.clear()

        #make a session just for the emailMax
        session['valid_emailMax'] = True

        # Return a JSON response instructing the frontend to redirect
        return jsonify({'status': 'redirect', 'url': '/emailMax'})

    # Generate a new 6-digit verification code
    new_verification_code = random.randint(100000, 999999)

    # Update the session with the new verification code
    session['verification_code'] = new_verification_code

    # Send the verification email with the new code
    #send_verification_email(email, new_verification_code)

    # Return a JSON response indicating success
    return jsonify({'status': 'success'})

@app.route('/emailMax')
def emailMax():

    if not session.get('valid_emailMax'):
        errorMessage = 'Incomplete'
        return render_template('error.html', errorMessage=errorMessage)

    return render_template('emailMax.html')

# from the email page get the sent data from mailto (not as reliable as sending through civic connect) -> check email.html for the fetch api
@app.route('/email_sent_mailto', methods=['POST'])
def email_sent_mailto():

    data = request.get_json()

    return jsonify(data)

# EXIT ROUTE -> WORKS
@app.route('/exit', methods=['POST', 'GET'])
def exit():
    session.clear()
    return redirect(url_for('home'))


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
    msg = Message(subject, recipients=[email], html=body)
    mail.send(msg)


# INVALID URL
@app.errorhandler(404)
def page_not_found(e):
    return render_template('page_not_found.html'), 404

# INVALID SERVER ERROR
@app.errorhandler(500)
def page_not_found(e):
    return render_template('servererror.html'), 500

if __name__ == '__main__':
    #app.run(host=ip, port=5500, debug=True) #-> for local testing
    app.run(debug=True)