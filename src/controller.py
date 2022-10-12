from os import environ

from flask_login import login_user, logout_user, current_user
from flask import render_template

import cloudinary
import cloudinary.api
import cloudinary.uploader

from src.model import Contact

cloudinary.config( 
  cloud_name = environ["CLOUD_NAME"], 
  api_key = environ["CLOUD_API_KEY"], 
  api_secret = environ["CLOUD_API_SECRET_KEY"] 
)



def home():
    if current_user.is_authenticated:
        contacts_count = len(current_user.contacts)
        meetings_count = len(current_user.meetings)
        return render_template("home.html", page_title = "Overview", first_name = current_user.first_name, last_name = current_user.last_name, contacts_count = contacts_count, meetings_count = meetings_count)
    else:
        login = forms.LoginForm()
        register = forms.RegisterForm()
        return render_template("index.html", page_title = "Home", login=login, register=register)