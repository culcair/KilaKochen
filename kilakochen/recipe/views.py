from sqlalchemy import select
from kilakochen.recipe import bp

from flask import render_template
from kilakochen.models import  Rezepte,Rezeptkategorien

from kilakochen import db

@bp.route('/')
@bp.route('/overview')
def overview():
    print("start")
    data = Rezepte.query.order_by(Rezepte.Titel).all()
    return render_template(
        'recipe_overview.html',
        page_title = "Übersicht der Rezepte",
        data=data
    )


@bp.route('/view/<int:id>')
def view_recipe(id):
    data = Rezepte.query.filter_by(ID=id).one_or_404()
    return render_template(
        'recipe.html',
        page_title = "Rezept - " + data.Titel,
        rezept_name = data.Titel,
        data=data
    )


@bp.route('/print/<int:id>')
def print_recipe(id):    
    data = Rezepte.query.filter_by(ID=id).one_or_404()
   
    filename="{}_{}.pdf".format("KiLaKochen",data.ID)

    html = render_template(
        'print_rezept.html',
        page_title = "Rezept - " + data.Titel,
        rezept_name = data.Titel,
        data=data
    )
    return html