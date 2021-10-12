from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

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