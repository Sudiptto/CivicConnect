from flask import Flask
from passwords import secret

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = secret
# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

token_data = {}
reasoning = ""
