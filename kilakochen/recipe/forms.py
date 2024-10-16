from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateField,
    FormField,
    RadioField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)


class EditHeuteForm(FlaskForm):
    datum = DateField("Datum", render_kw={"disabled": True})
    hauptgericht_old = StringField("Hauptgericht Alt", render_kw={"disabled": True})
    hauptgericht = SelectField("Hauptgericht")
    beilage = SelectField("Beilage")
    dessert = SelectField("Dessert")
    ausfall = BooleanField("An diesem Tag keine Essen")
    anmerkung = TextAreaField("Anmerkung")
    submit = SubmitField("Speichern")


from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SelectField,
    FieldList,
    FormField,
    DecimalField,
    SubmitField,
)
from wtforms.validators import DataRequired, Optional
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms import ValidationError
from decimal import Decimal
from kilakochen.models import Rezeptkategorien, Zutaten, Einheiten


# Hilfsfunktionen, um Kategorien, Zutaten und Einheiten für SelectFields bereitzustellen
def get_kategorien():
    return Rezeptkategorien.query.all()


def get_zutaten():
    return Zutaten.query.filter_by(Aktiv=1).all()


def get_einheiten():
    return Einheiten.query.filter_by(Aktiv=1).all()


# Formular für einzelne Zutateneinträge
class ZutatenForm(FlaskForm):
    zutat = QuerySelectField(
        "Zutat",
        query_factory=get_zutaten,
        allow_blank=False,
        get_label="Bezeichnung",
        validators=[DataRequired()],
    )
    menge = DecimalField(
        "Menge", places=2, rounding=Decimal("0.01"), validators=[DataRequired()]
    )
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
    def validate_zutaten(self, field):
        if len(field.entries) == 0:
            raise ValidationError("Mindestens eine Zutat muss hinzugefügt werden.")
