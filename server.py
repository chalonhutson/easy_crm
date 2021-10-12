# Easy CRM main server file

####### IMPORTS BEGIN #############
from os import environ

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, url_for, abort
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db

import controller

######### IMPORT END ###############

# Invokes the main Flask class and sets it to variable app.
app = Flask(__name__)

# This line prevents (or allows if set to True) Flask from taking you to a separate screen during debug mode, when you are redirected.
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

# Secret key is needed for each session, and here is set in separate secrets.sh file, which is ignored by git.
app.secret_key = environ["SESSION_SECRET_KEY"]

app.jinja_env.undefined = StrictUndefined


# Endpoint functions

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@app.route("/")
@app.route("/home")
def home():
    user_dict = {"first_name": "My name is Jeff"}
    return render_template("index.html", page_title = "Home")

@app.route("/contacts")
def contacts():
    contacts = controller.get_all_contacts_page(1, 25, 0)
    return render_template("contacts.html", page_title = "Contacts", contacts = contacts)

@app.route("/contacts/<contact_id>")
def individual_contact(contact_id):
    contact = controller.get_contact_by_id(contact_id)
    contact_phones = controller.get_phones_for_contact(contact_id)
    contact_phones = controller.get_phones_as_list(contact_phones)
    contact_emails = controller.get_emails_for_contact(contact_id)
    contact_emails = controller.get_emails_as_list(contact_emails)

    return render_template("individual-contact.html", page_title = f"{contact.first_name} {contact.last_name}", contact = contact, phones = contact_phones, emails = contact_emails)

@app.route("/add_contact", methods = ["GET", "POST"])
def add_contact():
    if request.method == "POST":
        print(request.form)
        fname = request.form["fname"]
        lname = request.form["lname"]
        title = request.form["title"]
        company = request.form["company"]
        bio = request.form["bio"]

        post_result = controller.add_contact(1, fname, lname, title, company, bio)

        if post_result == True:
            flash("Contact created successfully.", "success")
        else:
            flash("Something went wrong, please check your contact meets the requirements.", "error")
            
        return render_template("add-contact.html", page_title = "Add Contact")


    else:
        return render_template("add-contact.html", page_title = "Add Contact")


@app.route("/add-email/<contact_id>", methods = ["GET", "POST"])
def add_email(contact_id):
    contact = controller.get_contact_by_id(contact_id)

    if request.method == "POST":
        print(request.form)
        new_email = request.form["new_email"]
        if controller.add_email(1, contact_id, new_email):
            flash("Email added to contact.")
        else:
            flash("Something went wrong. Ensure you are meeting the email requirements.")
        return render_template("add-email.html", page_title = "Add Email", contact = contact)
    else:
        return render_template("add-email.html", page_title = "Add Email", contact = contact)


@app.route("/add-phone/<contact_id>", methods = ["GET", "POST"])
def add_phone(contact_id):
    contact = controller.get_contact_by_id(contact_id)

    if request.method == "POST":
        print(request.form)
        new_phone = request.form["new_phone"]
        if controller.add_phone(1, contact_id, new_phone):
            flash("Phone number added to contact.")
        else:
            flash("Something went wrong. Ensure you are meeting the phone number requirements.")
        return render_template("add-phone.html", page_title = "Add Phone", contact = contact)
    else:
        return render_template("add-phone.html", page_title = "Add Phone", contact = contact)




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
