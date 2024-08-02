from flask_wtf          import FlaskForm
from wtforms            import BooleanField, DateField, FormField, RadioField, SelectField, StringField, SubmitField, TextAreaField


class EditHeuteForm(FlaskForm):
	datum			= DateField('Datum',render_kw={"disabled" : True})
	hauptgericht_old= StringField  ('Hauptgericht Alt',render_kw={"disabled" : True})	
	hauptgericht    = SelectField  ('Hauptgericht')
	beilage			= SelectField('Beilage')
	dessert			= SelectField('Dessert')
	ausfall			= BooleanField('An diesem Tag keine Essen')
	anmerkung		= TextAreaField('Anmerkung')
	submit			= SubmitField('Speichern')
