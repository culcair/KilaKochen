from kilakochen.main import bp    
from flask import render_template

from datetime import datetime
from kilakochen.models import Essensplan, Rezepte, Zutaten,ZutatenProRezept,Mengenangabe, Zutatengruppe

from kilakochen import db

@bp.route('/')
def index():
    return render_template('index.html', page_title = "Startseite")
    
@bp.route('/heute')
def heute():
    date = datetime.now()

    res = Essensplan.query.filter_by(
        wplan_kw=date.isocalendar().week,
        wplan_wtag=date.isocalendar().weekday,
        wplan_jahr=date.isocalendar().year
        ).one_or_404()
    
    hgericht = Rezepte.query.filter_by(rezept_id=res.wplan_hgericht).first().rezept_name
    beilage =  Rezepte.query.filter_by(rezept_id=res.wplan_beilage).first().rezept_name
    dessert =  Rezepte.query.filter_by(rezept_id=res.wplan_dessert).first().rezept_name
    data = [hgericht, beilage, dessert]    
    return render_template(
        'heute.html',
        date = date,
        page_title = "Essensplan von heute",
        data=data
    )

@bp.route('/rezepte/<int:id>')
@bp.route('/rezepte', defaults={'id' : 0})
def rezepte(id):
    if id > 0:
        data = {}
        data["rezept"] = Rezepte.query.filter_by(rezept_id=id).first()
        rezept_name = data["rezept"].rezept_name
        res_zutaten = ZutatenProRezept.query.filter_by(Rezept_ID=id).all()
        data["zutaten_header"] = ["Menge", "Einheit", "Zutat"]
        data["zutaten"] = []
        for zutat in res_zutaten:
            zutat_data = []
            tmp = Zutaten.query.filter_by(zutat_id=zutat.Zutat_ID).one()
            mengen_einheit = Mengenangabe.query.filter_by(angaben_id=zutat.Einheit).one()
            zutat_data.append(zutat.Menge)
            zutat_data.append(mengen_einheit.angaben_abkz)
            zutat_data.append(tmp.zutat_name)
            data["zutaten"].append(zutat_data)
        return render_template(
            'rezept.html',
            page_title = "Rezept - " + rezept_name,
            rezept_name = rezept_name,
            data=data
        )
    else:
        data = Rezepte.query.order_by(Rezepte.rezept_name).all()
        return render_template(
            'rezepte.html',
            page_title = "Übersicht der Rezepte",
            data=data
        )
    

@bp.route('/zutaten')
def zutaten():
    data = Zutaten.query.all()
#    data = Zutaten.query.order_by("zutat_name").all()
    return render_template(
        'zutaten.html',
        page_title = "Übersicht aller Zutaten",
        data = data
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