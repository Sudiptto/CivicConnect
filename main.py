from flask import Flask, render_template, request, flash
from passwords import *
from allZipcode import * 

app = Flask(__name__)
app.config['SECRET_KEY'] = secret

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Access form data
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        zip_code = request.form['zipCode']
        state = request.form['state']
        city = request.form['city']
        #print(type(zip_code))
        if zip_code == '11218':
            print('test')
            flash('Incorrect Zipcode! Re-Type', category='error')
        print(first_name , last_name , zip_code , state , city)

    return render_template('home.html')


if __name__ == '__main__':
    #app.run(host=ip, port=5500) -> for local testing 
    app.run(debug=True)