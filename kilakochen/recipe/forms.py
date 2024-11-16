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
from kilakochen.old_models import Rezeptkategorien, Zutaten, Einheiten


# Hilfsfunktionen, um Kategorien, Zutaten und Einheiten für SelectFields bereitzustellen
def get_kategorien():
    return Rezeptkategorien.query.all()


def get_zutaten():
    return Zutaten.query.filter_by(Aktiv=1).all()


def get_einheiten():
    return Einheiten.query.filter_by(Aktiv=1).all()


# Formular für einzelne Zutateneinträge
class ZutatenForm(Form):
    zutat = QuerySelectField(
        "Zutat",
        query_factory=get_zutaten,
        allow_blank=False,
        get_label="Bezeichnung",
        validators=[DataRequired()],
    )
    menge = DecimalField("Menge", places=2, validators=[DataRequired()])
    einheit = QuerySelectField(
        "Einheit",
        query_factory=get_einheiten,
        allow_blank=False,
        get_label="Kuerzel",
        validators=[DataRequired()],
    )


# Hauptformular für das Rezept
class RezeptForm(FlaskForm):
    titel = StringField("Titel", validators=[DataRequired()])
    zubereitung = TextAreaField("Zubereitung", validators=[DataRequired()])
    author = StringField("Autor", validators=[DataRequired()])
    kategorie = QuerySelectField(
        "Kategorie",
        query_factory=get_kategorien,
        allow_blank=True,
        get_label="BezeichnungSingular",
        validators=[Optional()],
    )

    zutaten = FieldList(FormField(ZutatenForm), min_entries=1, label="Zutaten")

    submit = SubmitField("Rezept erstellen")


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
