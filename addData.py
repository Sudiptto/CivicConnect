import hashlib
from models import *
from app import app

# FUNCTION BELOW IS USED TO ADD UNIQUE EMAILS TO THE DATABASE AND HASHED
def hash_email(email):
    return hashlib.sha256(email.encode()).hexdigest()

# Function to format the topic to the correct format
def format_topic(topic):
    # add a - when there is a space, replace the space with a -
    return topic.replace(" ", "_")


def add_unique_email(email, zip_code):
    with app.app_context():
        # Hash the email
        hashed_email = hash_email(email)

        # Check if the hashed email already exists in the database
        existing_email = UniqueEmail.query.filter_by(hashed_email=hashed_email).first()
        if existing_email:
            print("Email already exists.")
            return

        # If the email doesn't exist, add it to the database
        new_email = UniqueEmail(hashed_email=hashed_email, zip_code=zip_code)
        db.session.add(new_email)
        db.session.commit()
        print("New unique email added.")

# Counts the number of occurences of a topic in the database
def add_or_increment_topic(topic):
    with app.app_context():
        # Check if the topic already exists in the database
        existing_topic = Occurrence.query.filter_by(topic=topic).first()

        if existing_topic:
            # Topic exists, increment the occurrence count
            existing_topic.occurrences += 1
            print(f"Incremented occurrences for topic '{topic}' to {existing_topic.occurrences}.")
        else:
            # Topic doesn't exist, add it with occurrences starting at 1
            new_topic = Occurrence(topic=topic, occurrences=1)
            db.session.add(new_topic)
            print(f"Added new topic '{topic}' with occurrences starting at 1.")

        # Commit the session to save changes
        db.session.commit()

def update_zipcode_data(zip_code, topic):
    topic = format_topic(topic)
    with app.app_context():
        # Check if the zip code already exists in the ZipcodeData table
        zipcode_data = ZipcodeData.query.filter_by(zip_code=zip_code).first()

        if not zipcode_data:
            # If zip code doesn't exist, create a new entry with all counts set to 0
            zipcode_data = ZipcodeData(zip_code=zip_code)
            db.session.add(zipcode_data)

        # Check if the topic column exists in the model
        if hasattr(zipcode_data, topic):
            # Get the current value of the topic, defaulting to 0 if it's None
            current_value = getattr(zipcode_data, topic) or 0
            # Increment the count for the specified topic
            setattr(zipcode_data, topic, current_value + 1)
        else:
            print(f"topic '{topic}' is not a valid field.")
            return

        # Update unique_emails count
        unique_email_count = UniqueEmail.query.filter_by(zip_code=zip_code).count()
        zipcode_data.unique_emails = unique_email_count

        # Increment the total_emails_sent count
        zipcode_data.total_emails_sent += 1

        # Commit the changes to the database
        db.session.commit()

        #print(f"Updated data for zip code '{zip_code}' - {topic}: {getattr(zipcode_data, topic)}")
        #print(f"Unique emails for zip code '{zip_code}': {zipcode_data.unique_emails}")
        #print(f"Total emails sent for zip code '{zip_code}': {zipcode_data.total_emails_sent}")

def update_representative_data(representative_name, topic):
    topic = format_topic(topic)
    with app.app_context():
        # Check if the representative already exists in the RepresentativeData table
        representative_data = RepresentativeData.query.filter_by(representative_name=representative_name).first()

        if not representative_data:
            # If the representative doesn't exist, create a new entry with all counts set to 0
            representative_data = RepresentativeData(representative_name=representative_name)
            db.session.add(representative_data)
            db.session.commit()  # Ensure the entry is saved with initial values

        # Check if the topic column exists in the model
        if hasattr(representative_data, topic):
            # Get the current value of the topic, defaulting to 0 if it's None
            current_value = getattr(representative_data, topic) or 0
            # Increment the count for the specified topic
            setattr(representative_data, topic, current_value + 1)
        else:
            print(f"topic '{topic}' is not a valid field.")
            return

        # Ensure total_emails_sent is not None, default to 0 if necessary
        total_emails_sent = representative_data.total_emails_sent or 0
        representative_data.total_emails_sent = total_emails_sent + 1

        # Commit the changes to the database
        db.session.commit()

        #print(f"Updated data for representative '{representative_name}' - {prompt}: {getattr(representative_data, prompt)}")
        #print(f"Total emails sent for representative '{representative_name}': {representative_data.total_emails_sent}")

