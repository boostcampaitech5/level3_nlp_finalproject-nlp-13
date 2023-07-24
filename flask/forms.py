from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class SignInForm(FlaskForm):
    ID = StringField("ID")
    PW = PasswordField("PW")
    submit = SubmitField("Sign in")