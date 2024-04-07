from flask import Flask, render_template, request, flash, redirect, url_for, session, jsonify
from app import *
from flask_mail import Mail, Message
from emailTrack import *
from allZipcode import *
import secrets
from passwords import *
from analysis import *
from prompts import *
from emailsend import email_bp  # Import the blueprint from emailsend.py

mail = Mail(app)

# Configure Flask-Mail settings
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
# mail username and password will change based on sending vs recieving email -> default recieving email
app.config["MAIL_USERNAME"] = emailName
app.config["MAIL_PASSWORD"] = emailPassword
app.config["MAIL_DEFAULT_SENDER"] = 'your_email@example.com'
mail.init_app(app)

# Register the email_bp Blueprint with the app
app.register_blueprint(email_bp)

# start page
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # get client side IP (used to check if the state address matches the IP address) -> meant to prevent people from lying about their location
        # Note: THE IP ADDRESS works but for local testing it returns back the local host (However, when deployed it will return the correct IP address)!
        ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)

        # for local testing
        ip_address = ipAddress

        # get the ip_address look up and see what state its linked to and if it matches the state that the user inputted -> use IP address look up api
        # website - > https://ip-api.com/docs/api:json
        ipLookup = requests.get(f"http://ip-api.com/json/{ip_address}").json()
        ipState = ipLookup['region']


        # Access form data
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        zip_code = request.form['zipCode'] # turn to integer -> after we check if its numeric
        state = request.form['state']

        # VALIDATE IS ZIPCODE IS NUMERIC
        if zip_code.isnumeric() == False:
            flash("Please enter a valid 5 DIGIT INTEGER zipcode", category="error")

        #zip_code = int(zip_code)

        # VALIDATE BOTH ZIP AND CITY DATA -> DONT USE THE API FOR NOW
        validateZipState = searchAndVerify(zipcodeData, zip_code, state)


        if validateZipState == 'Correct state!' and state==ipState:
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

        # works
        elif state != ipState:
            session['valid_zip_state'] = False
            flash('Please enter the current state and zipcode you are in!', category='error')

        else:
            session['valid_zip_state'] = False
            flash('Incorrect zipcode', category='error')



    return render_template('home.html')

#add another route that red

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
        causeSubject = ""
        # fill out the prompts -> check the prompts.py file
        if cause == 'southern-border':
            causeSubject = 'Southern Border'

        if cause == 'free-palestine':
            causeSubject = 'Free Palestine'

        if cause == 'affordable-housing':
            causeSubject = 'Affordable Housing'

        if cause == 'poverty':
            causeSubject = 'Poverty'

        # SESSION FOR EMAIL ROUTE
        session['validSubmit'] = True
        session['causeSubject'] = causeSubject
        return redirect(url_for('email'))

    # check prompts.py for getAllPrompts()
    return render_template('causes.html', firstName = first_name, nameList = nameList, emailList = emailList, allPrompts = getAllPrompts(first_name, nameList))


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

# THIS PAGE -> Users can add / update their queries
@app.route('/queries', methods=['POST', 'GET'])
def queries():
    if not session.get('valid_zip_state'):
        errorMessage = 'Incomplete'
        return render_template('error.html', errorMessage=errorMessage)

    if request.method == 'POST':
        selectOption = request.form['emailReason']
        email = request.form['email']
        promptCritique = request.form['critique']


        # verify if the email address is valid
        # Generate a unique token
        verification_token = secrets.token_hex(16)

        # Store the token and associated data in the dictionary
        token_data[verification_token] = {
            'email': email,
            'selectOption': selectOption,
            'promptCritique': promptCritique
        }

        reasoning = "queries"
        #session['reasoning'] = reasoning

        # Redirect to the route responsible for sending the email
        return redirect(url_for('email_bp.send_verification_email_route', email=email, token=verification_token, reasoning=reasoning))


    first_name = session.get('first_name')
    return render_template('queries.html', firstName=first_name)


# get the email from the fetch request from the email page  (javascript) and print out the email
@app.route('/email_sent', methods=['POST'])
def email_sent():
    data = request.get_json()

    email = data['email']
    repEmails = data['repEmails']
    repNames = data['repNames']
    subject = data['subject']
    prompt = data['prompt']

    reasoning = "sendOnBehalf"

    # Generate a unique token
    verification_token = secrets.token_hex(16)
    token_data[verification_token] = {
            'email': email,
            'repEmails': repEmails,
            'repNames': repNames,
            'subject': subject,
            'prompt': prompt
    }

    return redirect(url_for('email_bp.send_verification_email_route', email=email, token=verification_token, reasoning=reasoning))


# from the email page get the sent data from mailto (not as reliable as sending through civic connect) -> check email.html for the fetch api
@app.route('/email_sent_mailto', methods=['POST'])
def email_sent_mailto():

    data = request.get_json()

    subject = data['subject']
    zipCode = int(data['zipCode'])
    route = data['route']

    # send this data over to analytics.csv to be tracked
    # verified -> works
    trackData(zipCode, subject, route)

    return jsonify(data)

# EXIT ROUTE -> WORKS
@app.route('/exit', methods=['POST', 'GET'])
def exit():
    session.clear()
    return redirect(url_for('home'))


if __name__ == '__main__':
    #app.run(host=ip, port=5500, debug=True) #-> for local testing
    app.run(debug=True)