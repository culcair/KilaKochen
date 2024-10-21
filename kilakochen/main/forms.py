from flask_wtf          import FlaskForm
from wtforms            import BooleanField, DateField, FormField, SelectField, SubmitField, TextAreaField


class EditHeuteForm(FlaskForm):
	datum			= DateField('Datum',render_kw={"disabled" : True})
	hauptgericht    = SelectField  ('Hauptgericht')
	beilage			= SelectField('Beilage')
	dessert			= SelectField('Dessert')
	ausfall			= BooleanField('An diesem Tag keine Essen')
	anmerkung		= TextAreaField('Anmerkung')
	submit			= SubmitField('Speichern')


class EditWocheForm(FlaskForm):
	montag			= FormField(EditHeuteForm)
	dienstag		= FormField(EditHeuteForm)
	mittwoch		= FormField(EditHeuteForm)
	donnerstag		= FormField(EditHeuteForm)
	freitag			= FormField(EditHeuteForm)			
	submit			= SubmitField('Speichern')