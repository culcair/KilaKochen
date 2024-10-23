from flask_wtf          import FlaskForm
from wtforms            import StringField, PasswordField, SubmitField
<<<<<<< HEAD
from wtforms.validators import DataRequired, ValidationError, AnyOf


def validate_login(form,field):
	message = 'Benutzername ist nicht alphanumerisch'
	if not field.data.isalnum():
		raise ValidationError(message)

def must_be_login(form, field):
	message = 'falscher Wert'
	if not field.data == "login":
		raise ValidationError(message)
=======
from wtforms.validators import DataRequired
>>>>>>> parent of b3cde4f (* Schutz gegen SQL Injection)

class LoginForm(FlaskForm):
	username    = StringField  ('Username'  , validators=[DataRequired()])
	password    = PasswordField('Password'  , validators=[DataRequired()])
<<<<<<< HEAD
	login       = SubmitField('Login',		validators=[must_be_login])
=======
	login       = SubmitField('Login')
>>>>>>> parent of b3cde4f (* Schutz gegen SQL Injection)
