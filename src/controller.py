from os import environ

from flask_login import login_user, logout_user, current_user
from flask import render_template, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

import cloudinary
import cloudinary.api
import cloudinary.uploader

from src.model import User, Contact
import src.forms as forms

cloudinary.config( 
  cloud_name = environ["CLOUD_NAME"], 
  api_key = environ["CLOUD_API_KEY"], 
  api_secret = environ["CLOUD_API_SECRET_KEY"] 
)

def get_user_by_id(user_id):
  return User.query.get(user_id)

def attempt_registration(app, first_name, last_name, email, pass_hash):
  try:
    with app.app_context():
      new_user = User(first_name, last_name, email, pass_hash)
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

def register(app):
    register = forms.RegisterForm()
    if register.validate_on_submit():
        first_name = register.first_name.data
        last_name = register.last_name.data
        email = register.email.data
        password = register.password.data
        with app.app_context():
          user = User.query.filter_by(email=email).first()
          # return str(user)
        if not user:
            pass_hash = generate_password_hash(password)
            new_user = attempt_registration(app, first_name, last_name, email, pass_hash)
            if new_user:
                user = attempt_login(email, password)
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