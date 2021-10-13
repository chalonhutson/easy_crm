# Easy CRM main server file

####### IMPORTS BEGIN #############
from os import environ
from datetime import timedelta

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, url_for, abort
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

from model import connect_to_db

import sql_controller
import app_forms

######### IMPORT END ###############

# Invokes the main Flask class and sets it to variable app.
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "home"
login_manager.login_message = "Please login to continue."
login_manager.login_message_category = "danger"

# This line prevents (or allows if set to True) Flask from taking you to a separate screen during debug mode, when you are redirected.
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
app.config["REMEMBER_COOKIE_DURATION"] = timedelta(hours=24)

# Secret key is needed for each session, and here is set in separate secrets.sh file, which is ignored by git.
app.secret_key = environ["SESSION_SECRET_KEY"]

app.jinja_env.undefined = StrictUndefined

@login_manager.user_loader
def load_user(user_id):
    return sql_controller.get_user_by_id(user_id)


# Endpoint functions

@app.errorhandler(404)
def page_not_found(e):
    return render_template('page_not_found.html', page_title = "404 Error"), 404

@app.route("/home")
@app.route("/")
def home():
    if current_user.is_authenticated:
        c_count = sql_controller.return_count_contacts(current_user.id)
        m_count = sql_controller.return_count_meetings(current_user.id)
        return render_template("home.html", page_title = "Overview", first_name = current_user.first_name, last_name = current_user.last_name, contacts_count = c_count, meetings_count = m_count)
    else:
        login = app_forms.LoginForm()
        register = app_forms.RegisterForm()
        user_dict = {"first_name": "My name is Jeff"}
        return render_template("index.html", page_title = "Home", login=login, register=register)

@app.route("/login", methods = ["GET", "POST"])
def login():
    login = app_forms.LoginForm()
    if login.validate_on_submit():
        user = sql_controller.attempt_login(login.email.data, login.password.data)
        
        if user:
            login_user(user, remember=login.remember.data)
            flash("You are logged in.", "success")
            return redirect(url_for("contacts"))
        else:
            flash("Login failed. Please double check your email/password combo.", "danger")
            return redirect(url_for("home"))

    else:
        flash("Something went wrong. Please double check the your username/password and try again.", "danger")
        return redirect(url_for("home"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You are logged out.", "success")
    return redirect(url_for("home"))    
    
@app.route("/register", methods = ["GET", "POST"])
def register():
    register = app_forms.RegisterForm()
    if register.validate_on_submit():
        first_name = register.first_name.data
        last_name = register.last_name.data
        email = register.email.data
        password = register.password.data
        if not sql_controller.get_user_by_email(email):
            registeration = sql_controller.attempt_registration(first_name, last_name, email, password)
            if registeration:
                login_user(registeration)
                flash("You have successfully registered and are now logged in.", "success")
            else:
                flash("You were not able to register.", "danger")
        else:
            flash("This email already has an account registered to it.", "danger")
        return redirect("home")
    else:
        flash("Something went wrong. Please double check the registration specifications and try again.", "danger")
        return redirect(url_for("home"))


@app.route("/contacts")
@login_required
def contacts():
    contacts = sql_controller.get_all_contacts_page(current_user.id, 25, 0)
    return render_template("contacts.html", page_title = "Contacts", contacts = contacts)

@app.route("/meetings")
@login_required
def meetings():
    meetings = sql_controller.get_all_meetings_page(current_user.id, 25, 0)
    return render_template("meetings.html", page_title = "Meetings", meetings = meetings)

@app.route("/add-meeting")
@login_required
def add_meeting():
    return "working on it"

@app.route("/meetings/<meeting_id>")
@login_required
def individual_meeting(meeting_id):
    return "working on it"

@app.route("/contacts/<contact_id>")
@login_required
def individual_contact(contact_id):
    contact = sql_controller.get_contact_by_id(contact_id)
    contact_phones = sql_controller.get_phones_for_contact(contact_id)
    contact_phones = sql_controller.get_phones_as_list(contact_phones)
    contact_emails = sql_controller.get_emails_for_contact(contact_id)
    contact_emails = sql_controller.get_emails_as_list(contact_emails)

    return render_template("individual-contact.html", page_title = f"{contact.first_name} {contact.last_name}", contact = contact, phones = contact_phones, emails = contact_emails)

@app.route("/add_contact", methods = ["GET", "POST"])
@login_required
def add_contact():
    if request.method == "POST":
        print(request.form)
        fname = request.form["fname"]
        lname = request.form["lname"]
        title = request.form["title"]
        company = request.form["company"]
        bio = request.form["bio"]

        post_result = sql_controller.add_contact(current_user.id, fname, lname, title, company, bio)

        if post_result == True:
            flash("Contact created successfully.", "success")
        else:
            flash("Something went wrong, please check your contact meets the requirements.", "error")
            
        return render_template("add-contact.html", page_title = "Add Contact")


    else:
        return render_template("add-contact.html", page_title = "Add Contact")


@app.route("/add-email/<contact_id>", methods = ["GET", "POST"])
@login_required
def add_email(contact_id):
    contact = sql_controller.get_contact_by_id(contact_id)

    if request.method == "POST":
        print(request.form)
        new_email = request.form["new_email"]
        if sql_controller.add_email(current_user.id, contact_id, new_email):
            flash("Email added to contact.", "success")
        else:
            flash("Something went wrong. Ensure you are meeting the email requirements.", "danger")
        return render_template("add-email.html", page_title = "Add Email", contact = contact)
    else:
        return render_template("add-email.html", page_title = "Add Email", contact = contact)


@app.route("/add-phone/<contact_id>", methods = ["GET", "POST"])
@login_required
def add_phone(contact_id):
    contact = sql_controller.get_contact_by_id(contact_id)

    if request.method == "POST":
        print(request.form)
        new_phone = request.form["new_phone"]
        if sql_controller.add_phone(current_user.id, contact_id, new_phone):
            flash("Phone number added to contact.", "success")
        else:
            flash("Something went wrong. Ensure you are meeting the phone number requirements.", "danger")
        return render_template("add-phone.html", page_title = "Add Phone", contact = contact)
    else:
        return render_template("add-phone.html", page_title = "Add Phone", contact = contact)







# Main run script
if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host="0.0.0.0")
