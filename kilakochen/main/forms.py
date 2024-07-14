from flask_wtf          import FlaskForm
from wtforms            import SelectField, SubmitField, TextAreaField


class EditHeuteForm(FlaskForm):
	hauptgericht    = SelectField  ('Hauptgericht')
	beilage			= SelectField('Beilage')
	dessert			= SelectField('Dessert')
	ausfall			= TextAreaField('Ausfall')
	anmerkung		= TextAreaField('Anmerkung')
	submit			= SubmitField('Speichern')


class EditHeuteForm(FlaskForm):
	hauptgericht    = SelectField  ('Hauptgericht')
	beilage			= SelectField('Beilage')
	dessert			= SelectField('Dessert')
	ausfall			= TextAreaField('Ausfall')
	anmerkung		= TextAreaField('Anmerkung')
	submit			= SubmitField('Speichern')