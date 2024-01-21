from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Access form data
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        zip_code = request.form['zipCode']
        state = request.form['state']
        city = request.form['city']

        print(first_name , last_name , zip_code , state , city)

    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)