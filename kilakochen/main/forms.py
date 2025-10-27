from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateField,
    FormField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import Optional
from wtforms_sqlalchemy.fields import QuerySelectField

from kilakochen.models import Recipe, RecipeCategory


# Hilfsfunktionen, um Kategorien, Zutaten und Einheiten für SelectFields bereitzustellen
def get_recipes(category: str):
    cat = RecipeCategory.query.filter_by(code=category).first()
    if not cat:
        return []  # Rückgabe einer leeren Liste, falls keine Kategorie gefunden wurde
    return Recipe.query.filter_by(active=True, category_id=cat.id).order_by(Recipe.name).all()


class EditDayForm(FlaskForm):
    date = DateField("Datum", render_kw={"disabled": True})
    main_dish = QuerySelectField(
        "Hauptgericht",
        query_factory=lambda: get_recipes("H"),
        allow_blank=True,
        get_label="name",
        validators=[Optional()],
    )
    side_dish = QuerySelectField(
        "Beilage",
        query_factory=lambda: get_recipes("B"),
        allow_blank=True,
        get_label="name",
        validators=[Optional()],
    )
    dessert = QuerySelectField(
        "Dessert",
        query_factory=lambda: get_recipes("D"),
        allow_blank=True,
        get_label="name",
        validators=[Optional()],
    )

    outage = BooleanField("An diesem Tag keine Essen")
    comment = TextAreaField("Anmerkung")
    submit = SubmitField("Speichern")

class EditWeekForm(FlaskForm):
    montag = FormField(EditDayForm)
    dienstag = FormField(EditDayForm)
    mittwoch = FormField(EditDayForm)
    donnerstag = FormField(EditDayForm)
    freitag = FormField(EditDayForm)
    submit = SubmitField("Speichern")