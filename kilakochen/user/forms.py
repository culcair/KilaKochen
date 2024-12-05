from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, EqualTo

from kilakochen.models import User


class CreateUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    first_name = StringField("First Name", validators=[DataRequired()])
    given_name = StringField("Given Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password_again = PasswordField(
        "Password (repeated)",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match"),
        ],
    )
    email = StringField("Email")
    level = SelectField("Access Level", choices=tuple(User.ACCESS_LEVEL.items()))
    submit = SubmitField("Create")


class EditUserForm(FlaskForm):
    id = StringField("ID", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    first_name = StringField("First Name", validators=[DataRequired()])
    given_name = StringField("Given Name", validators=[DataRequired()])
    password = PasswordField(
        "Password",
    )
    password_again = PasswordField(
        "Password (repeated)",
        validators=[EqualTo("password", message="Passwords must match")],
    )
    email = StringField("Email")
    level = SelectField("Access Level", choices=tuple(User.ACCESS_LEVEL.items()))
    submit = SubmitField("Edit")
