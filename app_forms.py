from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Optional

from sql_controller import get_all_contacts_by_user

class LoginForm(FlaskForm):
    email = StringField("email", validators = [DataRequired(), Email()])
    password = PasswordField("password")
    remember = BooleanField("remember me?")
    submit = SubmitField("login")

class RegisterForm(FlaskForm):
    first_name = StringField("first name", validators = [DataRequired(), Length(min=1, max=25)])
    last_name = StringField("last name", validators = [DataRequired(), Length(min=1, max=25)])
    email = StringField("email", validators=[DataRequired(), Length(min=5, max=99), Email(message="Please type a proper email address.")])
    password = PasswordField("password", validators=[DataRequired(), Length(min=8, max=99)])
    confirm_password = PasswordField("confirm password", validators=[DataRequired(), Length(min=8, max=99), EqualTo("password")])
    submit = SubmitField("register")

class MeetingForm(FlaskForm):
    title = StringField("meeting title", validators=[Length(max=150), Optional()])
    contact = SelectField("contact", validators=[Optional()])
    method = StringField("method", validators=[Length(max=50), Optional()])
    place = StringField("place", validators=[Length(max=100), Optional()])
    submit = SubmitField("add meeting")

    def edit_contact_list(self, user_id):
        contacts = get_all_contacts_by_user(user_id, True)
        contacts_list = []
        contacts_list.append((None, "None"))

        for contact in contacts:
            tuple = (contact.contact_id, f"{contact.first_name} {contact.last_name}")
            contacts_list.append(tuple)

        self.contact.choices = contacts_list


class ContactAddress(FlaskForm):
    address_1 = StringField("address 1", validators=[Length(max=150)])
    address_2 = StringField("address 2", validators=[Length(max=150)])
    city = StringField("city", validators=[Length(max=50)])
    county = StringField("county", validators=[Length(max=50)])
    state = StringField("state", validators=[Length(max=50)])
    country = StringField("country", validators=[Length(max=50)])
    zip = StringField("zip", validators=[Length(max=9)])
    submit = SubmitField("add address")


class ContactSocial(FlaskForm):
    social_media = StringField("platform", validators=[Length(max=50)])
    social_media_address = StringField("address", validators=[Length(max=200)])
    submit = SubmitField("add social")

class MeetingNote(FlaskForm):
    note = TextAreaField("note",validators=[Length(max=5000)])
    submit = SubmitField("add note")
