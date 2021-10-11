# Easy CRM main server file

####### IMPORTS BEGIN #############
from os import environ

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, url_for
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db
# User_info, Contacts, Contacts_phone_numbers, Contacts_emails, Contacts_social_medias, Contacts_addresses, Contacts_notes, Meetings, Meetings_notes
from controller import add_contact, find_contact_by_fname, get_all_contacts_page

######### IMPORT END ###############

# Invokes the main Flask class and sets it to variable app.
app = Flask(__name__)

# This line prevents (or allows if set to True) Flask from taking you to a separate screen during debug mode, when you are redirected.
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

# Secret key is needed for each session, and here is set in separate secrets.sh file, which is ignored by git.
app.secret_key = environ["SESSION_SECRET_KEY"]

app.jinja_env.undefined = StrictUndefined


# Endpoint functions

@app.route("/")
@app.route("/home")
def home():
    user_dict = {"first_name": "My name is Jeff"}
    return render_template("index.html", page_title = "Home")

@app.route("/contacts")
def contacts():
    contacts = get_all_contacts_page(1, 25, 0)
    return render_template("contacts.html", page_title = "Contacts", contacts = contacts)

@app.route("/add_contact")
def add_contact():
    return render_template("add-contact.html", page_title = "Add Contact")

@app.route("/meetings")
def meetings():
    return render_template("meetings.html", page_title = "Meetings")


# Main run script
if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host="0.0.0.0")
