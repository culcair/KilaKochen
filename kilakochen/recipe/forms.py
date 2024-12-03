from flask_wtf import FlaskForm
from wtforms import (
    Form,
    FormField,
    StringField,
    SubmitField,
    TextAreaField,
    FieldList,
    DecimalField,
)
from wtforms.fields.simple import BooleanField

from wtforms.validators import DataRequired, Optional
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import ValidationError

from kilakochen.models import Ingredient, RecipeCategory, Unit

# Optional: Benutzerdefinierte Validierung für Zutaten
def validate_zutaten(field):
    if len(field.entries) == 0:
        raise ValidationError("Mindestens eine Zutat muss hinzugefügt werden.")


# Hilfsfunktionen, um Kategorien, Zutaten und Einheiten für SelectFields bereitzustellen
def get_categories():
    return RecipeCategory.query.filter_by(active=True).all()


def get_ingredients():
    return Ingredient.query.filter_by(active=True).all()


def get_units():
    return Unit.query.filter_by(active=True).all()


class IngredientForm(Form):
    ingredient = QuerySelectField(
        "Zutat",
        query_factory=get_ingredients,
        allow_blank=False,
        get_label="name",
        validators=[DataRequired()],
    )
    amount = DecimalField("Menge", places=2)
    unit = QuerySelectField(
        "Einheit",
        query_factory=get_units,
        allow_blank=False,
        get_label="code",
        validators=[DataRequired()],
    )


class RecipeForm(FlaskForm):
    name = StringField("Titel", validators=[DataRequired()])
    description = TextAreaField("Zubereitung", validators=[DataRequired()])
    author = StringField("Autor", validators=[DataRequired()])
    category = QuerySelectField(
        "Kategorie",
        query_factory=get_categories,
        allow_blank=True,
        get_label="name",
        validators=[Optional()],
    )

    ingredients = FieldList(FormField(IngredientForm), min_entries=1, label="Zutaten")
    active = BooleanField("Aktiv?")
    submit = SubmitField("Rezept erstellen")
