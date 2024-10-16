from sqlalchemy import select
from kilakochen.recipe import bp

from flask import render_template
from kilakochen.models import  Rezepte,Rezeptkategorien

from kilakochen import db

@bp.route('/')
@bp.route('/overview')
def overview():
    data = Rezepte.query.order_by(Rezepte.Titel).all()
    return render_template(
        'recipe_overview.html',
        page_title = "Übersicht der Rezepte",
        data=data
    )


@bp.route('/<int:id>/view')
def view_recipe(id):
    data = Rezepte.query.filter_by(ID=id).one_or_404()
    allergene = set()
    for zutat in data.rezepte_zutaten:
            for allergen in zutat.zutaten.zutaten_allergene:
                 allergene.add(allergen.allergene.Bezeichnung)

    return render_template(
        'recipe.html',
        page_title = "Rezept | " + data.Titel,
        rezept_name = data.Titel,
        data=data,
        allergene = ", ".join(allergene)
    )


@bp.route('/<int:id>/print')
def print(id):    
    data = Rezepte.query.filter_by(ID=id).one_or_404()
   
    filename="{}_{}.pdf".format("KiLaKochen",data.ID)

    html = render_template(
        'print_rezept.html',
        page_title = "Rezept - " + data.Titel,
        rezept_name = data.Titel,
        data=data
    )
    return html

@bp.route('/<int:id>/edit')
def edit(id):
    data = Rezepte.query.filter_by(ID=id).one_or_404()

    return render_template(
        'edit_recipe.html',
        page_title = "Rezept - " + data.Titel,
        data=data
    )

@bp.route('/new')
def new():
    data = Rezepte.query.filter_by(ID=37).one_or_404()

    return render_template(
        'edit_recipe.html',
        page_title = "Rezept - " + data.Titel,
        data=data
    )

