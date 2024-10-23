from flask_wtf          import FlaskForm
from wtforms            import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError, AnyOf


def validate_login(form,field):
	message = 'Benutzername ist nicht alphanumerisch'
	if not field.data.isalnum():
		raise ValidationError(message)

def must_be_login(form, field):
	message = 'falscher Wert'
	if not field.data == "Login":
		raise ValidationError(message)

class LoginForm(FlaskForm):

	username    = StringField  ('Username'  , validators=[DataRequired(),validate_login])
	password    = PasswordField('Password'  , validators=[DataRequired()])
	login       = SubmitField('Login',		validators=[must_be_login])
