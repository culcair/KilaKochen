from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
)

from wtforms.validators import DataRequired, Optional
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField

from kilakochen.models import IngredientsGroup, Allergen


# Hilfsfunktionen, um Kategorien, Zutaten und Einheiten für SelectFields bereitzustellen
def get_categories():
    return IngredientsGroup.query.filter_by(active=True).all()


def get_allergens():
    return Allergen.query.filter_by(active=True).all()


class IngredientForm(FlaskForm):
    name = StringField("Bezeichnung", validators=[DataRequired()])
    group = QuerySelectField(
        "Kategorie",
        query_factory=get_categories,
        allow_blank=True,
        get_label="description",
        validators=[Optional()],
    )

    allergens = QuerySelectMultipleField(
        "Zutat",
        query_factory=get_allergens,
        allow_blank=False,
        get_label="name",
        validators=[DataRequired()],
    )

    submit = SubmitField("Zutat erstellen")
