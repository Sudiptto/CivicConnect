from flask import Flask
from passwords import secret
from flask_mail import Mail, Message



# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = secret
# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# for mailing
mail = Mail(app)

token_data = {}
reasoning = ""
