#Model.py is the file that organizes the SQL database with the help of SQLAlchemy

#Import OS environ to read environment variables.
from os import environ

#Import SQLAlchemy to build out database.
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

db = SQLAlchemy()


#Model definition of tables for Easy CRM database.

class User_info(db.Model):

    __tablename__ = "user_info"
    __table_args__ = {"extend_existing": True}

    user_info_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    first_name = db.Column(db.String(25), nullable = False)
    last_name = db.Column(db.String(25), nullable = False)
    email = db.Column(db.String(99), nullable = False, unique = True)
    password = db.Column(db.String, nullable = False)

    def __repr__(self):
        return f"User Info Row || user_info_aid={self.user_info_id}, fname={self.first_name}, lname={self.last_name}, email={self.email}"


class Contacts(db.Model):

    __tablename__ = "contacts"
    __table_args__ = {"extend_existing": True}

    contact_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    user_info_id = db.Column(db.Integer, db.ForeignKey("user_info.user_info_id"))
    first_name = db.Column(db.String(25), nullable = True)
    last_name = db.Column(db.String(25), nullable = True)
    job_title = db.Column(db.String(50), nullable = True)
    company = db.Column(db.String(50), nullable = True)
    bio = db.Column(db.String(2000), nullable = True)

    def __repr__(self):
        return f"Contact Row || contact_id={self.contact_id}, user_info_id={self.user_info_id}, fname={self.first_name}, lname={self.last_name}"

class Contacts_phone_numbers(db.Model):

    __tablename__ = "contacts_phone_numbers"
    __table_args__ = {"extend_existing": True}

    contact_phone_number_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contacts.contact_id"))
    phone_number = db.Column(db.String(10), nullable = False)

    def __repr__(self):
        return f"Contact Phone # Row || phone_id={self.contact_phone_number_id}, contact_id={self.contact_id}, phone={self.phone_number}"

class Contacts_emails(db.Model):

    __tablename__ = "contacts_emails"
    __table_args__ = {"extend_existing": True}

    contact_email_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contacts.contact_id"))
    email = db.Column(db.String(99), nullable = False)

class Contacts_social_medias(db.Model):

    __tablename__ = "contacts_social_medias"
    __table_args__ = {"extend_existing": True}

    contact_social_media_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contacts.contact_id"))
    social_media = db.Column(db.String(50), nullable = False)
    social_media_address = db.Column(db.String(200), nullable = False)

    def __repr__(self):
        return f"Contact Social Media Row || id={self.contact_social_media_id}, contact_id={self.contact_id}, social_media={self.social_media}, social_media_address={self.social_media_address}"

class Contacts_addresses(db.Model):

    __tablename__ = "contacts_addresses"
    __table_args__ = {"extend_existing": True}

    contact_address_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contacts.contact_id"))
    street_address_1 = db.Column(db.String(150), nullable = True)
    street_address_2 = db.Column(db.String(150), nullable = True)
    city = db.Column(db.String(50), nullable = True)
    county = db.Column(db.String(50), nullable = True)
    state = db.Column(db.String(50), nullable = True)
    country = db.Column(db.String(50), nullable = True)
    zip = db.Column(db.String(9), nullable = True)

    def __repr__(self):
        return f"Contact Address Row || id={self.contact_address_id}, contact_id={self.contact_id}, street1={self.street_address_1}, street2={self.street_address_2}, city={self.city}, county={self.county}, state={self.state}, country={self.country}, zip={self.zip}"

class Contacts_notes(db.Model):

    __tablename__ = "contacts_notes"
    __table_args__ = {"extend_existing": True}

    contact_note_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contacts.contact_id"))
    note = db.Column(db.String(5000), nullable = False)

    def __repr__(self):
        return f"Contact Note Row || id={self.contact_note_id}, contact_id={self.contact_id}, note={self.note}"

class Meetings(db.Model):

    __tablename__ = "meetings"
    __table_args__ = {"extend_existing": True}

    meeting_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    user_info_id = db.Column(db.Integer, db.ForeignKey("user_info.user_info_id"), nullable = False)
    contact_id = db.Column(db.Integer, db.ForeignKey("contacts.contact_id"), nullable = True)
    meeting_title = db.Column(db.String(150), nullable = True)
    meeting_method = db.Column(db.String(50), nullable = True)
    meeting_place = db.Column(db.String(100), nullable = True)
    meeting_datetime = db.Column(db.DateTime, nullable = True)

    def __repr__(self):
        return f"Meetings Row || id={self.meeting_id}, user_id={self.user_info_id}, contact_id={self.contact_id}, title={self.meeting_title}, method={self.meeting_method}, place={self.meeting_place}, datetime={self.meeting_datetime}"


class Meetings_notes(db.Model):

    __tablename__ = "meetings_notes"
    __table_args__ = {"extend_existing": True}

    meeting_note_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    meeting_id = db.Column(db.Integer, db.ForeignKey("meetings.meeting_id"), nullable = False)
    note = db.Column(db.String(5000), nullable = False)

    def __repr__(self):
        return f"Meeting Note Row || id={self.meeting_note_id}, meeting_id={self.meeting_id}, note={self.note}"


# def add_contact(user_id, fname, lname, title, company, bio):
#     new_c = Contacts(first_name = fname, last_name = lname, job_title = title, company = company, bio = bio)
#     db.session.add(new_c)
#     db.session.commit()

# def find_contact_by_fname(user_id, name):
#     name = name.lower()
#     q = Contacts.query.filter(func.lower(Contacts.first_name) == name)
#     qcount = q.count()

#     if qcount == 0:
#         return "No results."
#     if qcount == 1:
#         qresult = q.first()
#         full_name = f"{qr.first_name} {qr.last_name}"
#         return full_name
#     if qcount > 1:
#         qresult = q.all()
#         return qresult

# def get_all_contacts_page(user_id, per_page, page_offset):
#     page_offset = page_offset * per_page
#     query = Contacts.query.filter(Contacts.user_info_id == user_id).limit(per_page).offset(page_offset)

#     if query.count() >= per_page:
#         for i in query:
#             print(i.first_name)
#     elif query.count() > 0:
#         for i in query:
#             print(i.first_name)
#             print("End of contacts.")
#     else:
#         print("No more contacts.")
    


# Helper functions

def connect_to_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = environ["POSTGRES_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


# Allows us to run code interactively and work with the database directly.
if __name__ == "__main__":
    from server import app
    connect_to_db(app)
    print("Connected to Easy CRM database.")