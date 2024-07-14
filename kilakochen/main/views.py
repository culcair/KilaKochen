from flask_login import current_user, login_required
from kilakochen.main import bp    
from flask import redirect, render_template, url_for
#from flask_weasyprint import HTML, render_pdf
from datetime import datetime,timedelta
from kilakochen.models import Allergene, Essensplan, Rezepte, Zutaten

from kilakochen.main.forms import EditHeuteForm
from kilakochen import db

@bp.route('/')
def index():
    return render_template('index.html', page_title = "Startseite")

@login_required
@bp.route('/heute/edit', methods=['GET', 'POST'])
def heute_edit():
    form = EditHeuteForm()

    result = Rezepte.query.with_entities(Rezepte.ID,Rezepte.Titel).filter(Rezepte.rezeptkategorien.has(Kuerzel="H")).all()
    form.hauptgericht.choices = [(x.ID, x.Titel) for x in result]
    result = Rezepte.query.with_entities(Rezepte.ID,Rezepte.Titel).filter(Rezepte.rezeptkategorien.has(Kuerzel="B")).all()
    form.beilage.choices = [(x.ID, x.Titel) for x in result]
    result = Rezepte.query.with_entities(Rezepte.ID,Rezepte.Titel).filter(Rezepte.rezeptkategorien.has(Kuerzel="D")).all()
    form.dessert.choices = [(x.ID, x.Titel) for x in result]
    if form.validate_on_submit():
        heute = Essensplan(
            Datum = datetime.now(),
            HauptgerichtRezeptID = form.hauptgericht.data[0],
            BeilageRezeptID = form.beilage.data[0],
            DessertRezeptID = form.dessert.data[0],
            Ausfall = form.ausfall.data,
            Anmerkung = form.anmerkung.data
        )
        db.session.add(heute)
        db.session.commit()
        return redirect(url_for('main.heute'))
    return render_template('edit_heute.html', form=form)

@bp.route('/heute')
def heute():
    date = datetime.now()
    data = Essensplan.query.filter_by(
        Datum=date.date()).one_or_none()

    print(data)
    if data is None and current_user.is_authenticated:
        data = Essensplan()
        return redirect(url_for('main.heute_edit'))
    else:
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

@bp.route('/rezept/<int:id>/print')
def print_rezept(id):    
    data = Rezepte.query.filter_by(ID=id).one_or_404()
    
    filename="{}_{}.pdf".format("KiLaKochen",data.ID)

    html = render_template(
        'print_rezept.html',
        page_title = "Rezept - " + data.Titel,
        rezept_name = data.Titel,
        data=data
    )

    return html
#    return render_pdf(
#        HTML(string=html),
#        download_filename=filename
#        )

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

@bp.route('/wochenplan/edit/<string:raw_date>')
@bp.route('/wochenplan/edit/', defaults = {'raw_date' : datetime.now()})
@login_required
def edit_wochenplan(raw_date):
    if type(raw_date) == str:
        given_date = datetime.fromisoformat(raw_date)
    else:
        given_date = raw_date

    weekday = given_date.isoweekday()
    # The start of the week
    start = given_date - timedelta(days=weekday-1)
    # build a simple range
    dates = [start + timedelta(days=d) for d in range(5)]

    plaene = []
    for week_date in dates:
        tmp = None
        res = Essensplan.query.filter_by(Datum=week_date).one_or_none()
        if  res is None:
            tmp = Essensplan(Datum=week_date)
        else:
            tmp = res
        plaene.append(tmp)

    rezepte = Rezepte.query.all() 

    return render_template(
        'edit_wochenplan.html',
        page_title = "Wochenplan",
        data=dates,
        plaene=plaene,
        rezepte=rezepte
    )


@bp.route('/einkaufsliste')
def einkaufsliste():
    return render_template(
        'einkaufsliste.html',
        page_title = "Einkaufsliste"
    )