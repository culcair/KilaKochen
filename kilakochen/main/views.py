from kilakochen.main import bp    
from flask import render_template
from flask_weasyprint import HTML, render_pdf
from datetime import datetime
from kilakochen.models import Allergene, Essensplan, Rezepte, Zutaten

from kilakochen import db

@bp.route('/')
def index():
    return render_template('index.html', page_title = "Startseite")
    
@bp.route('/heute')
def heute():
    date = datetime.now()
    data = Essensplan.query.filter_by(
        Datum=date.date()).one_or_404()

    return render_template(
        'heute.html',
        date = date,
        page_title = "Essensplan von heute",
        data=data
    )


@bp.route('/rezepte')
def rezepte():
    data = Rezepte.query.order_by(Rezepte.Titel).all()
    return render_template(
        'rezepte.html',
        page_title = "Übersicht der Rezepte",
        data=data
    )

@bp.route('/rezept/<int:id>')
def rezept(id):
    data = Rezepte.query.filter_by(ID=id).one_or_404()
    
    return render_template(
        'rezept.html',
        page_title = "Rezept - " + data.Titel,
        rezept_name = data.Titel,
        data=data
    )

@bp.route('/rezept/print/<int:id>')
def rezepte(id):    
    data = Rezepte.query.filter_by(ID=id).one_or_404()
    
    html = render_template(
        'print_base.html',
        page_title = "Rezept - " + data.Titel,
        rezept_name = data.Titel,
        data=data
    )

    return render_pdf(HTML(string=html))




@bp.route('/zutaten')
def zutaten():
    zutaten = Zutaten.query.all()
    allergene = Allergene.query.all()
    return render_template(
        'zutaten.html',
        page_title = "Übersicht aller Zutaten",
        data = zutaten,
        allergene = allergene
    )

@bp.route('/wochenplan')
def wochenplan():
    return render_template(
        'wochenplan.html',
        page_title = "Wochenplan"
    )

@bp.route('/einkaufsliste')
def einkaufsliste():
    return render_template(
        'einkaufsliste.html',
        page_title = "Einkaufsliste"
    )