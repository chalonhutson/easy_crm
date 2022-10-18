# Easy CRM main server file

####### IMPORTS BEGIN #############

from os import environ
import os
from datetime import timedelta

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, url_for, abort, Response, make_response, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS, cross_origin

######### IMPORT END ###############


# Invokes the main Flask class and sets it to variable app.
app = Flask(__name__)
CORS(app)
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
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = environ["DATABASE_URI"]
# app.config["SQLALCHEMY_DATABASE_URI"] = environ["HEROKU_POSTGRESQL_JADE_URL2"]
# Secret key is needed for each session, and here is set in separate secrets.sh file, which is ignored by git.
app.secret_key = environ["SESSION_SECRET_KEY"]

app.jinja_env.undefined = StrictUndefined


db = SQLAlchemy(app)

Migrate(app, db)

##### CLOUDINARY



import src.controller as ctrl
import src.forms



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
    return ctrl.home()


@app.route("/login", methods = ["GET", "POST"])
def login():
    return ctrl.login(app)

@app.route("/logout")
@login_required
def logout():
    return ctrl.logout()
    
@app.route("/register", methods=["GET", "POST"])
def register():
    return ctrl.register(app)

@app.route("/contacts")
def contacts():
    return ctrl.contacts(app)

@app.route("/meetings")
def meetings():
    return ctrl.meetings(app)

@app.route("/individual-contact/<contact_id>")
def individual_contact(contact_id):
    return str(contact_id)

@app.route("/add-contact", methods=["GET", "POST"])
def add_contact():
    form = forms.ContactForm()
    print(form.first_name.data)
    return ctrl.add_contact(app, request, form)


@app.route("/delete-contact/<contact_id>")
def delete_contact(contact_id):
    return f"Delete {contact_id}"

@app.route("/add-meeting", methods=["GET", "POST"])
def add_meeting():
    return "add meeting"

@app.route("/individual-meeting/<meeting_id>")
def individual_meeting(meeting_id):
    return f"Meeting {meeting_id}"

@app.route("/delete-meeting/<meeting_id>")
def delete_meeting(meeting_id):
    return f"Delete meeting {meeting_id}"