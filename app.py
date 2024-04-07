from flask import Flask
from passwords import secret

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = secret

token_data = {}
reasoning = ""
