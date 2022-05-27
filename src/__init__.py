# Easy CRM main server file

####### IMPORTS BEGIN #############

from os import environ
import os
from datetime import timedelta

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, url_for, abort, Response, make_response
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

######### IMPORT END ###############



# Invokes the main Flask class and sets it to variable app.
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "home"
login_manager.login_message = "Please login to continue."
login_manager.login_message_category = "danger"

basedir = os.path.abspath(os.path.dirname(__file__))
# This line prevents (or allows if set to True) Flask from taking you to a separate screen during debug mode, when you are redirected.
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
#Replacing the "remember me" time from one day to thirty days.
# app.config["REMEMBER_COOKIE_DURATION"] = timedelta(hours=24)
app.config["REMEMBER_COOKIE_DURATION"] = timedelta(days=30)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = environ["POSTGRES_URI"]
# app.config["SQLALCHEMY_DATABASE_URI"] = environ["HEROKU_POSTGRESQL_JADE_URL2"]
# Secret key is needed for each session, and here is set in separate secrets.sh file, which is ignored by git.
app.secret_key = environ["SESSION_SECRET_KEY"]

app.jinja_env.undefined = StrictUndefined


db = SQLAlchemy(app)

Migrate(app, db)




import src.sql_controller as ctrl
import src.app_forms



@login_manager.user_loader
def load_user(user_id):
    return ctrl.get_user_by_id(user_id)


# Endpoint functions

@app.errorhandler(404)
def page_not_found(e):
    return render_template('page_not_found.html', page_title = "404 Error"), 404

@app.route("/home")
@app.route("/")
def home():
    if current_user.is_authenticated:
        c_count = ctrl.return_count_contacts(current_user.id)
        m_count = ctrl.return_count_meetings(current_user.id)
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
        user = ctrl.attempt_login(login.email.data, login.password.data)
        
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
        if not ctrl.get_user_by_email(email):
            pass_hash = generate_password_hash(password)
            registeration = ctrl.attempt_registration(first_name, last_name, email, pass_hash)
            if registeration:
                login = ctrl.attempt_login(email, password)
                if login:
                    login_user(registeration)
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


@app.route("/contacts")
@login_required
def contacts():
    contacts = ctrl.get_all_contacts_page(current_user.id, 25, 0)
    return render_template("contacts.html", page_title = "Contacts", contacts = contacts)

@app.route("/meetings")
@login_required
def meetings():
    meetings = ctrl.get_all_meetings_page(current_user.id, 25, 0)
    return render_template("meetings.html", page_title = "Meetings", meetings = meetings)

@app.route("/add-meeting", methods = ["GET", "POST"])
@login_required
def add_meeting():
    if request.method == "POST":
        if ctrl.add_meeting(current_user.id, request.form):
            flash("Meeting added successfully.","success")
        else:
            flash("Something went wrong with adding your meeting, please try again.", "danger")
        return redirect(url_for("add_meeting"))

    else:
        form = app_forms.MeetingForm()
        form.edit_contact_list(current_user.id)
        return render_template("add-meeting.html", page_title="Add Meeting", form = form)

@app.route("/add-note-meeting/<meeting_id>", methods = ["GET", "POST"])
@login_required
def add_note_meeting(meeting_id):
    meeting = ctrl.get_meeting_by_id(meeting_id)
    contact = ctrl.get_contact_by_id(meeting_id)
    if request.method == "POST":
        new_note = request.form
        if ctrl.add_note_meeting(current_user.id, meeting_id, new_note):
            flash("Note added to meeting.", "success")
        else:
            flash("Something went wrong. Ensure you are meeting the note requirements.", "danger")
        return redirect(url_for("add_note_meeting", meeting_id = meeting_id))
    else:
        form = app_forms.MeetingNote()
        return render_template("add-note-meeting.html", page_title = f"Add Note to {meeting.meeting_title}", meeting = meeting, form = form)


@app.route("/add-note-contact/<contact_id>", methods = ["GET", "POST"])
@login_required
def add_note_contact(contact_id):
    contact = ctrl.get_contact_by_id(contact_id)
    contact = ctrl.get_contact_by_id(contact_id)
    if request.method == "POST":
        new_note = request.form
        if ctrl.add_note_contact(current_user.id, contact_id, new_note):
            flash("Note added to contact.", "success")
        else:
            flash("Something went wrong. Ensure you are contact the note requirements.", "danger")
        return redirect(url_for("add_note_contact", contact_id = contact_id))
    else:
        form = app_forms.ContactNote()
        return render_template("add-note-contact.html", page_title = f"Add Note for {contact.first_name} {contact.last_name}", contact = contact, form = form)








@app.route("/meetings/<meeting_id>")
@login_required
def individual_meeting(meeting_id):
    meeting = ctrl.get_meeting_by_id(meeting_id)
    notes = ctrl.get_all_notes_meeting(meeting_id)
    if meeting.meeting_datetime:
        date, time = ctrl.get_readable_date_time(meeting.meeting_datetime)
    else:
        date, time = None, None
    contact = ctrl.get_contact_by_id(meeting.contact_id)
    if contact:
        contact = contact
    else:
        contact = None
    return render_template("individual-meeting.html", page_title = meeting.meeting_title, meeting = meeting, contact = contact, date = date, time = time, notes = notes)

@app.route("/contacts/<contact_id>")
@login_required
def individual_contact(contact_id):
    contact, phones, emails, addresses, socials, notes = ctrl.get_all_for_contact(contact_id)
    return render_template("individual-contact.html", page_title = f"{contact.first_name} {contact.last_name}", contact = contact, phones = phones, emails = emails, addresses = addresses, socials = socials, notes = notes, ynumber = 0, thing = "thing", do = "do")

@app.route("/add_contact", methods = ["GET", "POST"])
@login_required
def add_contact():
    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        title = request.form["title"]
        company = request.form["company"]
        bio = request.form["bio"]

        post_result = ctrl.add_contact(current_user.id, fname, lname, title, company, bio)

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
    contact = ctrl.get_contact_by_id(contact_id)
    form = app_forms.ContactEmail()

    if request.method == "POST":
        new_email = request.form["email"]
        if ctrl.add_email(current_user.id, contact_id, new_email):
            flash("Email added to contact.", "success")
        else:
            flash("Something went wrong. Ensure you are meeting the email requirements.", "danger")
        return render_template("add-email.html", page_title = "Add Email", form = form, contact = contact)
    else:
        return render_template("add-email.html", page_title = "Add Email", form = form, contact = contact)


@app.route("/add-phone/<contact_id>", methods = ["GET", "POST"])
@login_required
def add_phone(contact_id):
    contact = ctrl.get_contact_by_id(contact_id)
    form = app_forms.ContactPhone()

    if request.method == "POST":
    # Validate on submit not working, investigate further.
    # if form.validate_on_submit():
        phone = form.phone.data
        phone_formatted = ctrl.format_phone(phone)
        if phone_formatted:
            if ctrl.add_phone(current_user.id, contact_id, phone_formatted):
                flash("Phone number added to contact.", "success")
            else:
                flash("Something went wrong. Ensure you are meeting the phone number requirements.", "danger")
        else:
            flash("Something went wrong. Ensure you are meeting the phone number requirements.", "danger")
        return render_template("add-phone.html", page_title = "Add Phone", form = form, contact = contact)
    else:
        return render_template("add-phone.html", page_title = "Add Phone", form = form, contact = contact)

@app.route("/add-address/<contact_id>", methods = ["GET", "POST"])
@login_required
def add_address(contact_id):
    contact = ctrl.get_contact_by_id(contact_id)

    if request.method == "POST":
        new_address = request.form
        if ctrl.add_address(current_user.id, contact_id, new_address):
            flash("Address added to contact.", "success")
        else:
            flash("Something went wrong. Ensure you are meeting the address requirements.", "danger")
        return redirect(url_for("add_address", contact_id = contact_id))
    else:
        form = app_forms.ContactAddress()
        return render_template("add-address.html", page_title = "Add Address", contact = contact, form=form)

@app.route("/add-social/<contact_id>", methods = ["GET", "POST"])
@login_required
def add_social(contact_id):
    contact = ctrl.get_contact_by_id(contact_id)

    if request.method == "POST":
        new_social = request.form
        if ctrl.add_social(current_user.id, contact_id, new_social):
            flash("Social added to contact.", "success")
        else:
            flash("Something went wrong. Ensure you are meeting the social requirements.", "danger")
        return redirect(url_for("add_social", contact_id = contact_id))
    else:
        form = app_forms.ContactSocial()
        return render_template("add-social.html", page_title = "Add Social", contact = contact, form=form)


@app.route("/delete_address", methods=["POST"])
@login_required
def delete_address():
    if request.method == "POST":
        address_id = request.form["delete_address"]
        contact_id = ctrl.get_contact_by_address(address_id)
        if ctrl.delete_address(current_user.id, address_id):
            flash("Address deleted from contact.", "success")  
            if contact_id:
                return redirect(url_for("individual_contact", contact_id = contact_id))
            flash("Something went wrong. Please try again.", "danger")
            return redirect(url_for("contacts"))
    else:
        abort(404)

@app.route("/delete_social", methods=["POST"])
@login_required
def delete_social():
    if request.method == "POST":
        social_id = request.form["delete_social"]
        contact_id = ctrl.get_contact_by_social(social_id)
        if ctrl.delete_social(current_user.id, social_id):
            flash("Social deleted from contact.", "success")  
            if contact_id:
                return redirect(url_for("individual_contact", contact_id = contact_id))
        else:
            flash("Something went wrong. Please try again.", "danger")
        return redirect(url_for("contacts"))
    else:
        abort(404)


@app.route("/delete-phone", methods=["POST"])
@login_required
def delete_phone():
    if request.method == "POST":
        phone_id = request.form["delete_phone"]
        contact_id = ctrl.get_contact_by_phone(phone_id)
        if ctrl.delete_phone(current_user.id, phone_id):
            flash("phone deleted from contact.", "success")  
            if contact_id:
                return redirect(url_for("individual_contact", contact_id = contact_id))
        else:
            flash("Something went wrong. Please try again.", "danger")
        return redirect(url_for("contacts"))
    else:
        abort(404)


@app.route("/delete-email", methods=["POST"])
@login_required
def delete_email():
    if request.method == "POST":
        email_id = request.form["delete_email"]
        contact_id = ctrl.get_contact_by_email(email_id)
        if ctrl.delete_email(current_user.id, email_id):
            flash("email deleted from contact.", "success")  
            if contact_id:
                return redirect(url_for("individual_contact", contact_id = contact_id))
        else:
            flash("Something went wrong. Please try again.", "danger")
        return redirect(url_for("contacts"))
    else:
        abort(404)


@app.route("/delete-note-meeting", methods = ["GET", "POST"])
@login_required
def delete_note_meeting():
    if request.method == "POST":
        note_id = request.form["delete_note_meeting"]
        note = ctrl.get_note_meeting_by_id(note_id)
        if ctrl.delete_note_meeting(current_user.id, note_id):
            flash("note deleted from meeting.", "success")
            if note:
                return redirect(url_for("individual_meeting", meeting_id = note.meeting_id))
        else:
            flash("Something went wrong.", "danger")
        return redirect(url_for("meetings"))
    else:
        abort(404)


@app.route("/delete-note-contact", methods = ["GET", "POST"])
@login_required
def delete_note_contact():
    if request.method == "POST":
        note_id = request.form["delete_note_contact"]
        note = ctrl.get_note_contact_by_id(note_id)
        if ctrl.delete_note_contact(current_user.id, note_id):
            flash("note deleted from contact", "success")
            if note:
                return redirect(url_for("individual_contact", contact_id = note.contact_id))
        else:
            flash("Something went wrong.", "danger")
        return redirect(url_for("contact"))
    else:
        abort(404)

@app.route("/delete-meeting/<meeting_id>", methods = ["GET", "POST"])
@login_required
def delete_meeting(meeting_id):
    meeting = ctrl.get_meeting_by_id(meeting_id)
    if not meeting:
        return abort(404)
    if request.method == "POST":
        if ctrl.delete_meeting(current_user.id, meeting_id):
            flash("Meeting successfully deleted.", "success")
        else:
            flash("Something went wrong.", "danger")
        return redirect(url_for("meetings"))
    else:
        return render_template("delete-meeting.html", page_title = f"Delete {meeting.meeting_title}?", meeting = meeting)


@app.route("/delete-contact/<contact_id>", methods = ["GET", "POST"])
@login_required
def delete_contact(contact_id):
    contact = ctrl.get_contact_by_id(contact_id)
    if not contact:
        return abort(404)
    if request.method == "POST":
        if ctrl.delete_contact(current_user.id, contact_id):
            flash("contact successfully deleted.", "success")
        else:
            flash("Something went wrong.", "danger")
        return redirect(url_for("contacts"))
    else:
        return render_template("delete-contact.html", page_title = f"Delete {contact.first_name} {contact.last_name}?", contact = contact)


@app.route("/update-meeting/", methods = ["POST", "GET"])
@login_required
def update_meeting():
    if request.method == "POST":
        meeting = ctrl.get_meeting_by_id(request.form["meeting_id"])
        form = request.form
        if form["_method"] == "PUT":
            if ctrl.update_meeting(current_user.id, form):
                flash("Meeting updated successfully.", "success")
            else:
                flash("Something went wrong.", "danger")
            return redirect(url_for("individual_meeting", meeting_id = meeting.meeting_id))
        else:
            form = app_forms.MeetingForm()
            info = request.form["info"]
            if meeting.meeting_datetime is not None:
                date, time = ctrl.get_readable_date_time(meeting.meeting_datetime)
            else:
                date, time = None, None
            if request.form["info"] == "contact":
                form.edit_contact_list(current_user.id)                
            return render_template("update-meeting.html", page_title = f"Update {meeting.meeting_title}'s {info}", meeting = meeting, date = date, time = time, info = info, form = form)
    flash("Something went wrong.", "danger")
    return redirect(url_for("meetings"))


@app.route("/update-contact", methods = ["POST", "GET"])
@login_required
def update_contact():
    if request.method == "POST":
        form = request.form
        info = request.form["info"]
        contact = ctrl.get_contact_by_id(form["contact_id"])
        if len(contact.first_name) > 0 or len(contact.last_name) > 0:
            contact_full_name = f"{contact.first_name} {contact.last_name}"
        else:
            contact_full_name = "contact"
        if form["_method"] == "PUT":
            if ctrl.update_contact(current_user.id, form):
                flash("Contact updated successfully", "success")
                return redirect(url_for("individual_contact", contact_id = contact.contact_id))
            else:
                flash("Something went wrong.", "danger")
        else:
            app_form = app_forms.ContactForm()
            return render_template("update-contact.html", page_title = f"Update {contact_full_name}'s {info}", contact_full_name = contact_full_name, contact = contact, info = info, form = app_form)
    flash("Something went wrong.", "danger")
    return redirect(url_for("contacts"))


@app.route("/update-contact-phone", methods = ["POST"])
@login_required
def update_contact_phone():
    phone_id = request.form["phone_id"]
    new_phone_number = request.form["new_phone_number"]

    print(phone_id)
    print(new_phone_number)

    return "Cool story bro."




# connect_to_db(app)

# Main run script
# if __name__ == "__main__":
#     # app.debug = False
#     # app.jinja_env.auto_reload = app.debug


#     # DebugToolbarExtension(app)

#     app.run()
