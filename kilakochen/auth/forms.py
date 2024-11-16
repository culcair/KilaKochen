from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.simple import BooleanField
from wtforms.validators import DataRequired, ValidationError



def validate_login(form,field):
    message = "Benutzername ist nicht alphanumerisch"
    if not field.data.isalnum():
        raise ValidationError(message)


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), validate_login])
    password = PasswordField("Password", validators=[DataRequired()])
    login = SubmitField("Login")
    remember_me = BooleanField("Remember Me")
