from kilakochen.main import bp    
from flask import render_template

from datetime import datetime

@bp.route('/')
def index():
    return render_template('index.html', page_title = "Startseite")
    
@bp.route('/heute')
def heute():
    date = datetime.now()
    return render_template(
        'heute.html',
        date = date,
        page_title = "Essensplan von heute"
    )

@bp.route('/rezepte')
def rezepte():
    return render_template(
        'rezepte.html',
        page_title = "Übersicht der Rezepte"
        )

@bp.route('/zutaten')
def zutaten():
    return render_template(
        'zutaten.html',
        page_title = "Übersicht aller Zutaten"
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