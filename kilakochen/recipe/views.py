from decimal import Decimal
from typing import List, Optional

from flask_login import login_required
from flask_weasyprint import HTML, render_pdf
from kilakochen.recipe import bp
from datetime import datetime

from flask import flash, redirect, render_template, url_for, request
from kilakochen.models import Rezepte, RezepteZutaten

from kilakochen import db
from kilakochen.recipe.forms import RezeptForm, ZutatenForm


def create_new_recipe(
    titel: str,
    zubereitung: str,
    author: str,
    kategorie_id: Optional[int],
    zutaten: List[dict],
):
    """
    Erstellt ein neues Rezept und fügt die Zutaten hinzu.

    :param titel: Titel des Rezepts
    :param zubereitung: Zubereitungsbeschreibung
    :param author: Autor des Rezepts
    :param kategorie_id: ID der Rezeptkategorie (optional)
    :param zutaten: Liste der Zutaten mit Menge und Einheit. Beispiel:
                    [{'zutat_id': 1, 'menge': Decimal('100'), 'einheit_id': 1}, ...]
    """
    try:
        # Erstelle neues Rezept
        neues_rezept = Rezepte(
            Titel=titel,
            Zubereitung=zubereitung,
            author=author,
            created_at=datetime.now().date(),
            KategorieID=kategorie_id,
            updated_at=datetime.now(),
        )
        db.session.add(neues_rezept)
        db.session.commit()

        # Füge die Zutaten zum Rezept hinzu
        for zutat in zutaten:
            neue_zutat = RezepteZutaten(
                RezeptID=neues_rezept.ID,
                ZutatID=zutat["zutat_id"],
                Menge=Decimal(zutat["menge"]),
                EinheitID=zutat["einheit_id"],
                Stand=datetime.now(),
            )
            db.session.add(neue_zutat)

        db.session.commit()
        return f"Rezept '{titel}' wurde erfolgreich erstellt!"

    except Exception as e:
        db.session.rollback()
        return f"Fehler beim Erstellen des Rezepts: {str(e)}"


@bp.route("/")
@bp.route("/overview")
def overview():
    data = Rezepte.query.order_by(Rezepte.Titel).all()
    return render_template(
        "recipe/overview.html", page_title="Übersicht der Rezepte", data=data
    )


@bp.route("/<int:recipe_id>/view")
def view(recipe_id):
    if request.referrer:
        back_ref_url = request.referrer
    else:
        back_ref_url=""
    data = Rezepte.query.filter_by(ID=recipe_id).one_or_404()
    allergene = set()
    for zutat in data.rezepte_zutaten:
        for allergen in zutat.zutaten.allergene:
            allergene.add(allergen.Bezeichnung)

    return render_template(
        "recipe/view.html",
        page_title="Rezept | " + data.Titel,
        rezept_name=data.Titel,
        data=data,
        allergene=", ".join(allergene),
        back_ref_url=back_ref_url
    )


@bp.route("/<int:recipe_id>/print")
def recipe_print(recipe_id):
    data = Rezepte.query.filter_by(ID=recipe_id).one_or_404()

    html_string = render_template(
        "recipe/print.html",
        page_title="Rezept - " + data.Titel,
        rezept_name=data.Titel,
        data=data,
    )

    tmp = HTML(string=html_string)

    download_filename = "{}_{}.pdf".format("KiLaKochen", data.ID)
    return render_pdf(tmp,automatic_download=True,download_filename=download_filename)


@bp.route("/new", methods=["GET", "POST"])
@login_required
def new():
    form = RezeptForm()
    template_form = ZutatenForm(prefix='zutaten-_-')
    if form.validate_on_submit():
        # Verarbeite das Formular, um das Rezept und die Zutaten zu speichern
        zutaten_liste = []
        for zutat_form in form.zutaten.entries:
            zutaten_liste.append(
                {
                    "zutat_id": zutat_form.zutat.data.ID,
                    "menge": zutat_form.menge.data,
                    "einheit_id": zutat_form.einheit.data.ID,
                }
            )
        # Verwende die oben definierte create_new_recipe-Funktion
        result = create_new_recipe(
            titel=form.titel.data,
            zubereitung=form.zubereitung.data,
            author=form.author.data,
            kategorie_id=form.kategorie.data.ID if form.kategorie.data else None,
            zutaten=zutaten_liste,
            
        )
        flash(result,category="info")
        return redirect(url_for("recipe.overview"))

    return render_template("recipe/new.html", form=form,_template=template_form)

def populate_recipe_form(recipe: Rezepte) -> RezeptForm:
    form : RezeptForm = RezeptForm()
    form.author.data = recipe.author
    form.kategorie.data = recipe.rezeptkategorien
    form.zubereitung.data = recipe.Zubereitung
    # Leere die Zutatenliste, bevor sie neu befüllt wird
    form.zutaten.entries = []

    # Füge die vorhandenen Zutaten des Rezeptes hinzu
    for rezept_zutat in recipe.rezepte_zutaten:
        # Erstelle ein neues Zutatenformular
        zutat_form = ZutatenForm()

        # Befülle die Felder des Zutatenformulars
        zutat_form.zutat.data = rezept_zutat.zutaten  # QuerySelectField für Zutat
        zutat_form.menge.data = rezept_zutat.Menge  # DecimalField für Menge
        zutat_form.einheit.data = rezept_zutat.einheiten  # QuerySelectField für Einheit

        # Füge das befüllte Zutatenformular der FieldList hinzu
        form.zutaten.append_entry(zutat_form)

    return form

@bp.route("/<int:recipe_id>/edit")
def edit(recipe_id):
    return redirect(url_for("recipe.view", recipe_id=recipe_id))
