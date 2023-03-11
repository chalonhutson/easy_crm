#Model.py is the file that organizes the SQL database with the help of SQLAlchemy

#Import OS environ to read environment variables.
from os import environ, system

#Import SQLAlchemy to build out database.
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_login import LoginManager, UserMixin, login_user
from werkzeug.security import generate_password_hash, check_password_hash

if __name__ == "__main__":
    db = SQLAlchemy()
else:
    from src import db




#Model definition of tables for Easy CRM database.

class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    first_name = db.Column(db.String(25), nullable = False)
    last_name = db.Column(db.String(25), nullable = False)
    email = db.Column(db.String(99), nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)

    contacts = db.relationship("Contact", backref="user", lazy=False)
    meetings = db.relationship("Meeting", backref="user", lazy=False)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name} e={self.email}>"




class Contact(db.Model):

    __tablename__ = "contacts"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    first_name = db.Column(db.String(25), nullable = True)
    last_name = db.Column(db.String(25), nullable = True)
    job_title = db.Column(db.String(50), nullable = True)
    company = db.Column(db.String(50), nullable = True)
    bio = db.Column(db.String(2000), nullable = True)

    phone_numbers = db.relationship("ContactPhoneNumber", backref="contact", lazy=False)
    emails = db.relationship("ContactEmail", backref="contact", lazy=False)
    social_medias = db.relationship("ContactSocialMedia", backref="contact", lazy=False)
    addresses = db.relationship("ContactAddress", backref="contact", lazy=False)
    notes = db.relationship("ContactNote", backref="contact", lazy=False)

    def __init__(self, user_id, first_name, last_name, job_title, company, bio):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.job_title = job_title
        self.company = company
        self.bio = bio

    def __repr__(self):
        return f"<Contact {self.first_name} {self.last_name}>"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


class ContactPhoneNumber(db.Model):

    __tablename__ = "contacts_phone_numbers"

    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contacts.id"))
    phone_number = db.Column(db.String(10), nullable = False)

    def __init__(self, contact_id, phone_number):
        self.contact_id = contact_id
        self.phone_number = phone_number

    def __repr__(self):
        return f"<Contact Phone Number {self.phone_number}>"

    def get_readable_number(self):
        return f"({self.phone_number[0:3]}) {self.phone_number[3:6]}-{self.phone_number[7:]}"


class ContactEmail(db.Model):

    __tablename__ = "contacts_emails"

    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contacts.id"))
    email = db.Column(db.String(99), nullable = False)

    def __init__(self, contact_id, email):
        self.contact_id = contact_id
        self.email = email
    
    def __repr__(self):
        return f"<Contact Email {self.email}>"


class ContactSocialMedia(db.Model):

    __tablename__ = "contacts_social_medias"

    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contacts.id"))
    social_media = db.Column(db.String(50), nullable = False)
    social_media_address = db.Column(db.String(200), nullable = False)

    def __init__(self, contact_id, social_media, social_media_address):
        self.contact_id = contact_id
        self.social_media = social_media
        self.social_media_address = social_media_address

    def __repr__(self):
        return f"<Contact Social Media {self.social_media_address}>"


class ContactAddress(db.Model):

    __tablename__ = "contacts_addresses"

    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contacts.id"))
    street_address_1 = db.Column(db.String(150), nullable = True)
    street_address_2 = db.Column(db.String(150), nullable = True)
    city = db.Column(db.String(50), nullable = True)
    county = db.Column(db.String(50), nullable = True)
    state = db.Column(db.String(50), nullable = True)
    country = db.Column(db.String(50), nullable = True)
    zipcode = db.Column(db.String(9), nullable = True)

    def __init__(self, contact_id, street_address_1, street_address_2, city, county, state, country, zipcode):
        self.contact_id = contact_id
        self.street_address_1 = street_address_1
        self.street_address_2 = street_address_2
        self.city = city
        self.county = county
        self.state = state
        self.country = country
        self.zipcode = zipcode

    def __repr__(self):
        return f"Contact Address Row || id={self.contact_address_id}, contact_id={self.contact_id}, street1={self.street_address_1}, street2={self.street_address_2}, city={self.city}, county={self.county}, state={self.state}, country={self.country}, zip={self.zip}"


class ContactNote(db.Model):

    __tablename__ = "contacts_notes"

    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contacts.id"))
    note = db.Column(db.String(5000), nullable = False)

    def __init__(self, contact_id, note):
        self.contact_id = contact_id
        self.note = note

    def __repr__(self):
        return f"<Contact Note {self.id}>"


class Meeting(db.Model):

    __tablename__ = "meetings"

    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)
    contact_id = db.Column(db.Integer, db.ForeignKey("contacts.id"), nullable = True)
    title = db.Column(db.String(150), nullable = True)
    method = db.Column(db.String(50), nullable = True)
    place = db.Column(db.String(100), nullable = True)
    datetime = db.Column(db.DateTime, nullable = True)

    contact = db.relationship("Contact", backref="meetings", lazy=False)

    notes = db.relationship("MeetingNote", backref="meeting", lazy=False)

    def __init__(self, user_id, contact_id, title, method, place, datetime):
        self.user_id = user_id
        self.contact_id = contact_id
        self.title = title
        self.method = method
        self.place = place
        self.datetime = datetime

    def __repr__(self):
        return f"<Meeting {self.title}>"


class MeetingNote(db.Model):

    __tablename__ = "meetings_notes"

    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    meeting_id = db.Column(db.Integer, db.ForeignKey("meetings.id"), nullable = False)
    note = db.Column(db.String(5000), nullable = False)

    def __init__(self, meeting_id, note):
        self.meeting_id = meeting_id
        self.note = note

    def __repr__(self):
        return f"<Meeting Note {self.id}>"

def seed_database(app):
    system("dropdb easy-crm")
    system("createdb easy-crm")

    with app.app_context():
        db.create_all()

    frodo = User("Frodo", "Baggins", "myburden@email.com", "password")
    samwise = User("Samwise", "Gamgee", "icancarryyou@email.com", "password")
    
    with app.app_context():
        db.session.add_all([frodo, samwise])
        db.session.commit()

    samwise = Contact(1, "Samwise", "Gamgee", "Gardener", "The Fellowship", "He really likes potatoes.")
    frodo = Contact(2, "Frodo", "Baggins", "Ringbearer", "The Fellowship", "He likes hearing about great stories.")

    with app.app_context():
        db.session.add_all([samwise, frodo])
        db.session.commit()

if __name__ == "__main__":
    from flask import Flask
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = environ["DATABASE_URI"]
    db.app = app
    db.init_app(app)
    seed_database(app)