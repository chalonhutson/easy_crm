from os import environ

from flask_login import login_user, logout_user, current_user
from flask import render_template, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

import cloudinary
import cloudinary.api
import cloudinary.uploader

from src.model import User, Contact, ContactPhoneNumber, ContactEmail, ContactAddress, ContactSocialMedia, ContactNote, Meeting, MeetingNote
import src.forms as forms

cloudinary.config( 
  cloud_name = environ["CLOUD_NAME"], 
  api_key = environ["CLOUD_API_KEY"], 
  api_secret = environ["CLOUD_API_SECRET_KEY"] 
)

def get_user_by_id(user_id):
  return User.query.get(user_id)

def attempt_registration(app, db, first_name, last_name, email, password):
  try:
    with app.app_context():
      new_user = User(first_name, last_name, email, password)
      print("attempted")
      db.session.add(new_user)
      print("here")
      db.session.commit()
      return new_user
  except:
    print("Failed to register new user.")
    return None

def attempt_login(app, email, password):
  with app.app_context():
    user = User.query.filter_by(email=email).first()
    if user:
      if check_password_hash(user.password, password):
        return user
    print("Failed to login user.")
    return False


def home():
    if current_user.is_authenticated:
        contacts_count = len(current_user.contacts)
        meetings_count = len(current_user.meetings)
        return render_template("home.html", page_title = "Overview", first_name = current_user.first_name, last_name = current_user.last_name, contacts_count = contacts_count, meetings_count = meetings_count)
    else:
        login = forms.LoginForm()
        register = forms.RegisterForm()
        return render_template("index.html", page_title = "Home", login=login, register=register)

def login(app):
    login = forms.LoginForm()
    if login.validate_on_submit():
        user = attempt_login(app, login.email.data, login.password.data)
        
        if user:
            login_user(user, remember=login.remember.data)
            print(f"User {user.first_name} {user.last_name} logged in with email = {user.email}.")
            if user.email == "test@email.com":
                print(user.email)
                flash("You have logged in with a test account. Please don't post any private information using this email.", "success")
            else:
                flash("You are logged in.", "success")
            return redirect(url_for("home"))
        else:
            flash("Login failed. Please double check your email/password combo.", "danger")
            return redirect(url_for("home"))

    else:
        flash("Something went wrong. Please double check the your username/password and try again.", "danger")
        return redirect(url_for("home"))

def logout():
    logout_user()
    flash("You are logged out.", "success")
    return redirect(url_for("home"))  

def register(app, db):
    register_form = forms.RegisterForm()
    if register_form.validate_on_submit():
        first_name = register_form.first_name.data
        last_name = register_form.last_name.data
        email = register_form.email.data
        password = register_form.password.data
        with app.app_context():
          user = User.query.filter_by(email=email).first()
          # return str(user)
        if not user:
            # pass_hash = generate_password_hash(password)
            new_user = attempt_registration(app, db, first_name, last_name, email, password)
            if new_user:
                user = attempt_login(app, email, password)
                if login:
                    login_user(user)
                    flash("You have successfully registered and are now logged in.", "success")
                else:
                    flash("You have registered, please try and log in.", "success")
            else:
                flash("You were not able to register.", "danger")
        else:
            flash("This email already has an account registered to it.", "danger")
        return redirect("home")
    else:
        flash("Something went wrong. Please double check the registration specifications and try again.", "danger")
        return redirect(url_for("home"))


def individual_contact(contact_id):
  contact = Contact.query.get(contact_id)
  return render_template("individual-contact.html", page_title=contact.get_full_name(), contact=contact)

def contacts(app):
  contacts = Contact.query.filter_by(user_id=current_user.id).all()
  return render_template("contacts.html", page_title="Contacts", contacts=contacts)


def add_contact(app, db, request):
  form = forms.ContactForm()
  if request.method == "GET":
    return render_template("add-contact.html", page_title="Add Contact", form=form)
  else:
    first_name = form.first_name.data
    last_name = form.last_name.data
    job_title = form.job_title.data
    company = form.company.data
    bio = form.bio.data
    new_contact = Contact(current_user.id, first_name, last_name, job_title, company, bio)
    db.session.add(new_contact)
    db.session.commit()
    flash("Contact added.")
    return redirect(url_for("contacts"))

def add_phone(app, db, contact_id, request):
  form = forms.ContactPhone()

  if form.validate_on_submit():
    phone_number = form.phone.data
    new_phone = ContactPhoneNumber(contact_id, phone_number)
    db.session.add(new_phone)
    db.session.commit()
    return redirect(url_for("individual_contact", contact_id=contact_id))
  else:
    contact = Contact.query.get(contact_id)
    return render_template("add-phone.html", form=form, contact=contact, page_title=f"Add Phone")

def add_email(app, db, contact_id, request):
  form = forms.ContactEmail()

  if form.validate_on_submit():
    email = form.email.data
    new_email = ContactEmail(contact_id, email)
    db.session.add(new_email)
    db.session.commit()
    return redirect(url_for("individual_contact", contact_id=contact_id))
  else:
    contact = Contact.query.get(contact_id)
    return render_template("add-email.html", form=form, contact=contact, page_title=f"Add Email")


def add_address(app, db, contact_id, request):
  form = forms.ContactAddress()

  if form.validate_on_submit():
    address_1 = form.address_1.data
    address_2 = form.address_2.data
    city = form.city.data
    county = form.county.data
    state = form.state.data
    country = form.country.data
    zipcode = form.zipcode.data
    new_address = ContactAddress(contact_id, address_1, address_2, city, county, state, country, zipcode)
    db.session.add(new_address)
    db.session.commit()
    return redirect(url_for("individual_contact", contact_id=contact_id))
  else:
    contact = Contact.query.get(contact_id)
    return render_template("add-address.html", form=form, contact=contact, page_title=f"Add Address")

def add_social(app, db, contact_id, request):
  form = forms.ContactSocial()

  if form.validate_on_submit():
    social_media = form.social_media.data
    social_media_address = form.social_media_address.data
    new_social = ContactSocialMedia(contact_id, social_media, social_media_address)
    db.session.add(new_social)
    db.session.commit()
    return redirect(url_for("individual_contact", contact_id=contact_id))
  else:
    contact = Contact.query.get(contact_id)
    return render_template("add-social.html", form=form, contact=contact, page_title=f"Add Social")

def add_note_contact(app, db, contact_id, request):
  form = forms.ContactNote()

  if form.validate_on_submit():
    note = form.note.data
    new_note = ContactNote(contact_id, note)
    db.session.add(new_note)
    db.session.commit()
    return redirect(url_for("individual_contact", contact_id=contact_id))
  else:
    contact = Contact.query.get(contact_id)
    return render_template("add-note-contact.html", form=form, contact=contact, page_title=f"Add Note")


# Contact delete functions

def delete_contact(app, db, contact_id):

  contact = Contact.query.get(contact_id)
    
  try:
    for phone in contact.phone_numbers:
      db.session.delete(phone)
      db.session.commit()
    
    for email in contact.emails:
      db.session.delete(email)
      db.session.commit()

    for social in contact.social_medias:
      db.session.delete(social)
      db.session.commit()

    for address in contact.addresses:
      db.session.delete(address)
      db.session.commit()

    for note in contact.notes:
      db.session.delete(note)
      db.session.commit()

    for meeting in contact.meetings:
      for note in meeting.notes:
        db.session.delete(note)
        db.session.commit()
      db.session.delete(meeting)

    db.session.delete(contact)
    db.session.commit()
    flash("Contact deleted.", "success")
  except:
    flash("Something went wrong with the deletion of the contact.", "danger")

  return redirect(url_for("contacts"))


def delete_phone(app, db, phone_id):
  phone = ContactPhoneNumber.query.get(phone_id)
  contact_id = phone.contact.id
  db.session.delete(phone)
  db.session.commit()
  flash("Phone number deleted", "success")
  return redirect(url_for("individual_contact", contact_id=contact_id))

def delete_email(app, db, email_id):
  email = ContactEmail.query.get(email_id)
  contact_id = email.contact.id
  db.session.delete(email)
  db.session.commit()
  flash("Email deleted", "success")
  return redirect(url_for("individual_contact", contact_id=contact_id))

def delete_address(app, db, address_id):
  address = ContactAddress.query.get(address_id)
  contact_id = address.contact.id
  db.session.delete(address)
  db.session.commit()
  flash("Address deleted", "success")
  return redirect(url_for("individual_contact", contact_id=contact_id))

def delete_social(app, db, social_id):
  social = ContactSocialMedia.query.get(social_id)
  contact_id = social.contact.id
  db.session.delete(social)
  db.session.commit()
  flash("Social deleted", "success")
  return redirect(url_for("individual_contact", contact_id=contact_id))

def delete_note_contact(app, db, note_id):
  note = ContactNote.query.get(note_id)
  contact_id = note.contact.id
  db.session.delete(note)
  db.session.commit()
  flash("Note deleted", "success")
  return redirect(url_for("individual_contact", contact_id=contact_id))







# Meetings

def meetings(app):
  return render_template("meetings.html", page_title="Meetings")

def add_meeting(app, db, request):
  form = forms.MeetingForm()
  form.update_contact_list(current_user.contacts)

  if form.validate_on_submit():
    title = form.title.data
    contact_id = form.contact.data
    method = form.method.data
    place = form.place.data
    datetime = form.datetime.data

    new_meeting = Meeting(current_user.id, contact_id, title, method, place, datetime)
    db.session.add(new_meeting)
    db.session.commit()
    return redirect(url_for("meetings"))

  else:
    return render_template("add-meeting.html", page_title="Add Meeting", form=form)

def delete_meeting(app, db, meeting_id):
  meeting = Meeting.query.get(meeting_id)

  for note in meeting.notes:
    db.session.delete(note)
    db.session.commit()

  db.session.delete(meeting)
  db.session.commit()

  return redirect(url_for("meetings"))

def add_note_meeting(app, db, request, meeting_id):
  form = forms.MeetingNote()

  if form.validate_on_submit():
    note = form.note.data
    new_meeting_note = MeetingNote(meeting_id, note)
    db.session.add(new_meeting_note)
    db.session.commit()
    return redirect(url_for("individual_meeting", meeting_id=meeting_id))
  else:
    meeting = Meeting.query.get(meeting_id)
    return render_template("add-note-meeting.html", page_title="Add Meeting Note", meeting=meeting, form=form)

def delete_note_meeting(app, db, meeting_note_id):
  meeting_note = MeetingNote.query.get(meeting_note_id)
  meeting_id = meeting_note.meeting.id
  print(meeting_note)
  db.session.delete(meeting_note)
  db.session.commit()
  flash("Message deleted.", "success")
  return redirect(url_for("individual_meeting", meeting_id=meeting_id))

def individual_meeting(meeting_id):
  meeting = Meeting.query.get(meeting_id)
  return render_template("individual-meeting.html", page_title="Meeting", meeting=meeting)
