from flask import Flask, render_template, request, flash, redirect, url_for, session 
from flask_mail import Mail, Message
from allZipcode import *
import secrets
from passwords import *
from analysis import * 
from prompts import *
from jinja2 import Environment # will be used for custon jinja functions 


# initilize everything
app = Flask(__name__)
app.config['SECRET_KEY'] = secret
mail = Mail(app)

# Configure Flask-Mail settings
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = emailName
app.config["MAIL_PASSWORD"] = emailPassword
app.config["MAIL_DEFAULT_SENDER"] = 'your_email@example.com'
mail.init_app(app)
token_data = {}

# Jinja Function to append
def append_item(lst, item):
    lst.append(item)
    return lst

env = Environment()
env.filters['append'] = append_item

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
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
    prompt = subjectPrompt(subject,first_name,nameList)


    return render_template('email.html', emailList=emailList, firstName = first_name, subject=subject, prompt=prompt, allReps=allReps)

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

        # Redirect to the route responsible for sending the email
        return redirect(url_for('send_verification_email_route', email=email, token=verification_token))
    

    first_name = session.get('first_name')
    return render_template('queries.html', firstName=first_name)




# EXIT ROUTE -> WORKS
@app.route('/exit', methods=['POST'])
def exit():
    if request.method == 'POST':
        session.clear()
        return redirect(url_for('home'))
    return redirect(url_for('home'))


# VERIFY EMAIL
@app.route('/generate_token_and_send_email', methods=['POST'])
def generate_token_and_send_email():
    if request.method == 'POST':
        # Access form data
        email = request.form['email']
        selectOption = request.form['emailReason']
        promptCritique = request.form['critique']
        # Generate a unique token
        verification_token = secrets.token_hex(16)

        # Store the token and associated data in the dictionary
        token_data[verification_token] = {
            'email': email,
            'selectOption': selectOption,
            'promptCritique': promptCritique
        }

        # Redirect to the route responsible for sending the email
        return redirect(url_for('send_verification_email_route', email=email, token=verification_token))


@app.route('/send_verification_email/<email>/<token>', methods=['GET'])
def send_verification_email_route(email, token):
    verification_data = token_data.get(token, {})
    optionChosen = verification_data.get('selectOption')
    promptCritique = verification_data.get('promptCritique')
    send_verification_email(email, token, optionChosen, promptCritique)
    flash('Verification link sent to your email.', category='info')

    return redirect(url_for('home'))


# NOTE ADD THE USER PROMPTS HERE (ALSO APPEARS IN MY SENT BOX)
def send_verification_email(email, token, optionChosen, promptCritique):
    # to send the verification email 
    subject = 'Verify Your Email for Query'
    verification_link = url_for('verify_email', token=token, _external=True)

    body = f'Click the following link to verify your email: {verification_link} <br> <b>Here is your inputs:</b> <br> <p>Option chosen: {optionChosen} <br> {promptCritique} '

    msg = Message(subject, recipients=[email], html=body)
    mail.send(msg)
    

# route where email gets sent to me 
@app.route('/verify_email/<token>', methods=['GET'])
def verify_email(token):
    # Check if the token is in the dictionary
    if token in token_data:
        # Retrieve data associated with the token
        data = token_data.pop(token)
        #print(data)
        # Set a session variable to indicate email verification
        session['email_verified'] = True
        session['email'] = data['email']

        promptCritique = data['promptCritique']
        optionChosen = data['selectOption']
        email = data['email']

        flash('Email verified.', category='success')
        # send the prompt email to us -> only after verification
        subject = f'User Prompt: {optionChosen}'
        body = f'<div style="background-color:#f2f2f2;padding:20px;"><h2 style="color:#333;">User Prompt Details</h2><p><strong>Email:</strong> {email}</p><p><strong>Option chosen:</strong> {optionChosen}</p><p><strong>Prompt Critique:</strong></p><div style="padding-left:20px;">{promptCritique}</div></div>'
        msg2 = Message(subject, sender=data['email'], recipients=[emailName], html=body)
        mail.send(msg2)
        #flash('Email sent successfully! Check inbox for more', category='error')
    # fix this part down here 
    else:
        flash('Invalid or expired verification link.', category='error')
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    #app.run(host=ip, port=5500, debug=True) #-> for local testing 
    app.run(debug=True)