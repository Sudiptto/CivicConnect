from flask_sqlalchemy import SQLAlchemy
from app import app

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define your models
# Table 1: Track number of unique emails
class UniqueEmail(db.Model):
    __tablename__ = 'unique_email'
    id = db.Column(db.Integer, primary_key=True)
    hashed_email = db.Column(db.String(64), unique=True, nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)

# Table 2: Number of Occurrences
class Occurrence(db.Model):
    __tablename__ = 'occurrence'
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(100), nullable=False)
    occurrences = db.Column(db.Integer, nullable=False)

# Table 3: Data per Zipcode
class ZipcodeData(db.Model):
    __tablename__ = 'zipcode_data'
    zip_code = db.Column(db.String(10), primary_key=True)

    # Different prompts subject to add more in the future 
    Southern_Border = db.Column(db.Integer, nullable=False, default=0)
    Free_Palestine = db.Column(db.Integer, nullable=False, default=0)
    Affordable_Housing = db.Column(db.Integer, nullable=False, default=0)
    Abortion = db.Column(db.Integer, nullable=False, default=0)

    unique_emails = db.Column(db.Integer, nullable=False, default=0)
    total_emails_sent = db.Column(db.Integer, nullable=False, default=0)

# Table 4: Data per Representative
class RepresentativeData(db.Model):
    __tablename__ = 'representative_data'
    representative_name = db.Column(db.String(100), primary_key=True)

    # Different prompts subject to add more in the future 
    Southern_Border = db.Column(db.Integer, nullable=False, default=0)
    Free_Palestine = db.Column(db.Integer, nullable=False, default=0)
    Affordable_Housing = db.Column(db.Integer, nullable=False, default=0)
    Abortion = db.Column(db.Integer, nullable=False, default=0)


    total_emails_sent = db.Column(db.Integer, nullable=False, default=0)

# Create the database tables
with app.app_context():
    db.create_all()