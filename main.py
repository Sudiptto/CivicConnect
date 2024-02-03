from flask import Flask, render_template, request, flash, redirect, url_for, session 
from passwords import *
from allZipcode import * 
from analysis import * 
from prompts import *
app = Flask(__name__)
app.config['SECRET_KEY'] = secret

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

        zip_code = int(zip_code)

        # VALIDATE BOTH ZIP AND CITY DATA 
        validateZipState = searchAndVerify(zipcodeData, zip_code, state) 
        if validateZipState == 'Correct state!':
            #print('test')
            flash('Correct Move on!', category='error')
            session['valid_zip_state'] = True
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

    nameList = senateANDhouseNames(state, zipCode)
    emailList = senateAndhouseEmails(state, zipCode)

    # create new session for emailList

    session['emailList'] = emailList
    # NOTE WORKS -> REDIRECT TO AN EMAIL route (final route )
    if request.method == 'POST':
        
        cause = request.form['cause']
        causeSubject = ""
        # fill out the prompts -> check the prompts.py file 
        if cause == 'environmental-protection':
            causeSubject = 'Enviornmental Protection'

        if cause == 'free-palestine':
            causeSubject = 'Free Palestine'

        if cause == 'racial-redlining':
            causeSubject = 'Racial Redlining'

        if cause == 'poverty':
            causeSubject = 'Poverty'

        # SESSION FOR EMAIL ROUTE 
        session['validSubmit'] = True
        session['causeSubject'] = causeSubject
        return redirect(url_for('email'))

    return render_template('causes.html', firstName = first_name, nameList = nameList, emailList = emailList)


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
    emailList = session.get('emailList')
    subject = session.get('causeSubject')
    prompt =subjectPrompt(subject)


    return render_template('email.html', emailList=emailList, firstName = first_name, subject=subject, prompt=prompt)

# THIS PAGE -> Users can add / update their queries
@app.route('/queries')
def queries():
    if not session.get('valid_zip_state'):
        errorMessage = 'Incomplete'
        return render_template('error.html', errorMessage=errorMessage)

    first_name = session.get('first_name')
    return render_template('queries.html', firstName=first_name)



if __name__ == '__main__':
    #app.run(host=ip, port=5500, debug=True) #-> for local testing 
    app.run(debug=True)