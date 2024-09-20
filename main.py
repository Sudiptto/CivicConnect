from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
from app import *
from allZipcode import *
import secrets
from passwords import *
from analysis import *
from prompts import *
from emailsend import email_bp  # Import the blueprint from emailsend.py
from models import *  # Import the db and User model


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

    reasoning = "sendOnBehalf"

    # Generate a unique token
    verification_token = secrets.token_hex(16)
    token_data[verification_token] = {
            'email': email,
            'repEmails': repEmails,
            'repNames': repNames,
            'subject': subject,
            'prompt': prompt,
            'firstName': firstName

    }

    return redirect(url_for('email_bp.send_verification_email_route', email=email, token=verification_token, reasoning=reasoning))


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