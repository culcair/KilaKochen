from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateField,
    FormField,
    SelectField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import Optional

from wtforms_sqlalchemy.fields import QuerySelectField

from kilakochen.models import Recipe, RecipeCategory


class EditHeuteForm(FlaskForm):
    datum = DateField("Datum", render_kw={"disabled": True})
    hauptgericht = SelectField("Hauptgericht")
    beilage = SelectField("Beilage")
    dessert = SelectField("Dessert")
    ausfall = BooleanField("An diesem Tag keine Essen")
    anmerkung = TextAreaField("Anmerkung")
    submit = SubmitField("Speichern")


class EditWocheForm(FlaskForm):
    montag = FormField(EditHeuteForm)
    dienstag = FormField(EditHeuteForm)
    mittwoch = FormField(EditHeuteForm)
    donnerstag = FormField(EditHeuteForm)
    freitag = FormField(EditHeuteForm)
    submit = SubmitField("Speichern")

# Hilfsfunktionen, um Kategorien, Zutaten und Einheiten für SelectFields bereitzustellen
def get_recipes():
#    cat_id = RecipeCategory.query.filter_by(name=category).first().id
    return Recipe.query.filter_by(active=True).all()


class EditDayForm(FlaskForm):
    date = DateField("Datum", render_kw={"disabled": True})
    main_dish = QuerySelectField(
        "Hauptgericht",
        query_factory=get_recipes,
        allow_blank=True,
        get_label="name",
        validators=[Optional()],
    )
    side_dish = QuerySelectField(
        "Beilage",
        query_factory=get_recipes,
        allow_blank=True,
        get_label="name",
        validators=[Optional()],
    )
    dessert = QuerySelectField(
        "Dessert",
        query_factory=get_recipes,
        allow_blank=True,
        get_label="name",
        validators=[Optional()],
    )

    outage = BooleanField("An diesem Tag keine Essen")
    comment = TextAreaField("Anmerkung")
    submit = SubmitField("Speichern")

class EditWocheForm(FlaskForm):
    montag = FormField(EditHeuteForm)
    dienstag = FormField(EditHeuteForm)
    mittwoch = FormField(EditHeuteForm)
    donnerstag = FormField(EditHeuteForm)
    freitag = FormField(EditHeuteForm)
    submit = SubmitField("Speichern")