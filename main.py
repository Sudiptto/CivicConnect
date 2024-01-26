from flask import Flask, render_template, request, flash, redirect, url_for, session 
from passwords import *
from allZipcode import * 
from analysis import * 
app = Flask(__name__)
app.config['SECRET_KEY'] = secret

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Access form data
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        zip_code = int(request.form['zipCode']) # turn to integer
        state = request.form['state']
        # VALIDATE BOTH ZIP AND CITY DATA 
        validateZipState = searchAndVerify(zipcodeData, zip_code, state) 
        if validateZipState == 'Correct state!':
            #print('test')
            flash('Correct Move on!', category='error')
            session['valid_zip_state'] = True
            session['first_name'] = first_name  
            return redirect(url_for('causes'))
        
        elif validateZipState == 'Invalid state and zip combo':
            session['valid_zip_state'] = False
            flash('Invalid state and zip combo', category='error')
        else:
            session['valid_zip_state'] = False
            flash('Incorrect zipcode', category='error')

        

    return render_template('home.html')

@app.route('/causes')
def causes():
    if not session.get('valid_zip_state'):
        #print('activated')
        return render_template('error.html')
    first_name = session.get('first_name')
    return render_template('causes.html', firstName = first_name)

if __name__ == '__main__':
    #app.run(host=ip, port=5500) #-> for local testing 
    app.run(debug=True)