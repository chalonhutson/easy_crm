#Model.py is the file that organizes the SQL database with the help of SQLAlchemy

#Import OS environ to read environment variables.
from os import environ

#Import SQLAlchemy to build out database.
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


#Model definition of tables for Easy CRM database.

class User_info(db.Model):

    __tablename__ = 'user_info'

    user_info_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    first_name = db.Column(db.String(25), nullable = False)
    last_name = db.Column(db.String(25), nullable = False)
    email = db.Column(db.String(9), nullable = False)

class Rating(db.Model):

    __tablename__ = 'contacts'

    contact_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    user_info_id = db.Column(db.Integer, db.ForeignKey("user_info.user_info_id"))
    first_name = db.Column(db.String(25), nullable = True)
    last_name = db.Column(db.String(25), nullable = True)
    job_title = db.Column(db.String(50), nullable = True)
    company = db.Column(db.String(50), nullable = True)
    bio = db.Column(db.String(2000), nullable = True)

class Contacts_phone_numbers(db.Model):

    __tablename__ = 'contact_phone_numbers'

    contact_phone_number_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contacts.contact_id"))
    phone_number = db.Column(db.String(10), nullable = False)

class Contacts_social_medias(db.Model):

    __tablename__ = 'contacts_social_medias'

    contact_social_media_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contacts.contact_id"))
    social_media = db.Column(db.String(50), nullable = False)
    social_media_address = db.Column(db.String(200), nullable = False)

class Contacts_addresses(db.Model):

    __tablename__ = 'contacts_social_medias'

    contact_address_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contacts.contact_id"))
    street_address_1 = db.Column(db.String(150), nullable = True)
    street_address_2 = db.Column(db.String(150), nullable = True)
    city = db.Column(db.String(50), nullable = True)
    county = db.Column(db.String(50), nullable = True)
    state = db.Column(db.String(50), nullable = True)
    country = db.Column(db.String(50), nullable = True)
    zip = db.Column(db.String(9), nullable = True)

class Contacts_notes(db.Model):

    __tablename__ = 'contacts_notes'

    contact_note_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contacts.contact_id"))
    note = db.Column(db.String(5000), nullable = False)

class Meetings(db.Model):

    __tablename__ = "meetings"

    meeting_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    user_info_id = db.Column(db.Integer, db.ForeignKey("user_info.user_info_id"), nullable = False)
    contact_id = db.Column(db.Integer, db.ForeignKey("contacts.contact_id"), nullable = True)
    meeting_title = db.Column(db.String(150), nullable = True)
    meeting_method = db.Column(db.String(50), nullable = True)
    meeting_place = db.Column(db.String(100), nullable = True)
    meeting_datetime = db.Column(db.DateTime, nullable = True)

class Meetings_notes(db.Model):

    __tablename__ = "meetings_notes"

    meeting_note_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    meeting_id = db.Column(db.Integer, db.ForeignKey("meetings.meeting_id"), nullable = False)
    note = db.Column(db.String(5000), nullable = False)