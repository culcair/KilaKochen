from decimal import Decimal
from typing import List, Optional
from sqlalchemy import select
from kilakochen.recipe import bp
from datetime import datetime

from flask import flash, redirect, render_template, url_for
from kilakochen.models import Rezepte, RezepteZutaten, Rezeptkategorien

from kilakochen import db
from kilakochen.recipe.forms import RezeptForm


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
        print(neues_rezept)
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
        "recipe_overview.html", page_title="Übersicht der Rezepte", data=data
    )


@bp.route("/<int:id>/view")
def view_recipe(id):
    data = Rezepte.query.filter_by(ID=id).one_or_404()
    allergene = set()
    for zutat in data.rezepte_zutaten:
        for allergen in zutat.zutaten.zutaten_allergene:
            allergene.add(allergen.allergene.Bezeichnung)

    return render_template(
        "recipe.html",
        page_title="Rezept | " + data.Titel,
        rezept_name=data.Titel,
        data=data,
        allergene=", ".join(allergene),
    )


@bp.route("/<int:id>/print")
def print(id):
    data = Rezepte.query.filter_by(ID=id).one_or_404()

    filename = "{}_{}.pdf".format("KiLaKochen", data.ID)

    html = render_template(
        "print_rezept.html",
        page_title="Rezept - " + data.Titel,
        rezept_name=data.Titel,
        data=data,
    )
    return html


@bp.route("/new", methods=['GET', 'POST'])
def new_recipe():
    form = RezeptForm()
    if form.validate_on_submit():
        # Verarbeite das Formular, um das Rezept und die Zutaten zu speichern
        zutaten_liste = []
        for zutat_form in form.zutaten.entries:
            print(zutat_form)
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
        print(result)
        flash(result)
        return redirect(url_for("recipe_overview"))

    return render_template("new_recipe.html", form=form)


@bp.route("/<int:id>/edit")
def edit(id):
    data = Rezepte.query.filter_by(ID=37).one_or_404()

    return render_template(
        "edit_recipe.html", page_title="Rezept - " + data.Titel, data=data
    )
