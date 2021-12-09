from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, RadioField, SubmitField, StringField, EmailField, PasswordField, \
    BooleanField
from wtforms.validators import DataRequired, InputRequired
from datetime import datetime


def set_years():
    now = datetime.now().year
    years = [x for x in range(now, now - 51, -1)]
    return years


class inputForm(FlaskForm):
    year = SelectField("Year", choices=[], validators=[DataRequired()])
    odometer = IntegerField("Odometer", validators=[DataRequired()])
    make = SelectField("Make", choices=[], validators=[DataRequired()])
    model = SelectField("Model", choices=[], validators=[DataRequired()])
    transmission = RadioField("Transmission", choices=['Automatic', 'Manual'], validators=[DataRequired()])
    submit = SubmitField("Submit")


class RegisterForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    register = SubmitField("Sign up")


class LoginForm(FlaskForm):
    username = StringField('User Name', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    login = SubmitField("Log in")
