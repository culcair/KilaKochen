from flask_login import current_user, login_required
from sqlalchemy import select
from kilakochen.main import bp    
from flask import abort, redirect, render_template, url_for
#from flask_weasyprint import HTML, render_pdf
from datetime import datetime,timedelta
from kilakochen.models import Allergene, Essensplan, Rezepte, Zutaten

from kilakochen.main.forms import EditHeuteForm, EditWocheForm
from kilakochen import db

@bp.route('/')
def index():
    return render_template('index.html', page_title = "Startseite")

def get_rezepte(kategorie):
    from pprint import pprint
    res = Rezepte.query.with_entities(Rezepte.ID,Rezepte.Titel).filter(Rezepte.rezeptkategorien.has(Kuerzel=kategorie)).order_by(Rezepte.Titel).all()
    
    
    choices = [(x.ID, x.Titel) for x in res]
    return choices

@login_required
@bp.route('/day/edit/<string:raw_date>', methods=['GET', 'POST'])
@bp.route('/today/edit', methods=['GET', 'POST'],defaults= {"raw_date" : datetime.today().date()})
def day_edit(raw_date):
    if type(raw_date) == str:
        given_date = datetime.fromisoformat(raw_date).date()
    else:
        given_date = raw_date
            
    plan = Essensplan.query.filter_by(Datum=given_date).one_or_none()
    
    form = EditHeuteForm()
    form.hauptgericht.choices = get_rezepte("H")
    form.beilage.choices = get_rezepte("B")
    form.dessert.choices = get_rezepte("D")
    if plan is not None:
        form.datum.data = plan.Datum
        if plan.Hauptgericht is not None:
            form.hauptgericht_old.data = plan.Hauptgericht.Titel
        if plan.Beilage is not None:
            form.beilage.default = [4] 
        if plan.Dessert is not None:
            form.dessert.default = (plan.Hauptgericht.ID,plan.Hauptgericht.Titel)
    else:
        form.datum.data = given_date

    if form.validate_on_submit():
        if plan is None:
            plan = Essensplan(
                Datum                   = given_date,
                HauptgerichtRezeptID    = form.hauptgericht.data,
                BeilageRezeptID         = form.beilage.data,
                DessertRezeptID         = form.dessert.data,
                Ausfall                 = form.ausfall.data,
                Anmerkung               = form.anmerkung.data
            )
        else:
            plan.HauptgerichtRezeptID  = form.hauptgericht.data
            plan.BeilageRezeptID       = form.beilage.data
            plan.DessertRezeptID       = form.dessert.data
            plan.Ausfall               = form.ausfall.data
            plan.Anmerkung             = form.anmerkung.data

        db.session.add(plan)
        db.session.commit()
        return redirect(url_for('main.day'))
    return render_template('edit_day.html', form=form)

@bp.route('/day/<string:raw_date>')
@bp.route('/today')
def day(raw_date = datetime.today().date()):
    if type(raw_date) == str:
        given_date = datetime.fromisoformat(raw_date).date()
    else:
        given_date = raw_date
 
    data = Essensplan.query.filter_by(Datum=given_date).one_or_none()

    if data is None and current_user.is_authenticated:
        data = Essensplan()
        return redirect(url_for('main.day_edit',raw_date=given_date))
    elif data is None:
        return abort(404)
    else:
        return render_template(
            'today.html',
            date = given_date,
            page_title = "Essensplan von heute",
            data=data
        )

@bp.route('/ingredients')
def ingredients():
    zutaten = Zutaten.query.all()
    allergene = Allergene.query.all()
    return render_template(
        'zutaten.html',
        page_title = "Übersicht aller Zutaten",
        data = zutaten,
        allergene = allergene
    )

@bp.route('/week/overview')
def week_overview():
    date = datetime.today().date()
    prefix = 3
    weeks = []
    for i in range(2-prefix,2+prefix):
        tmp = get_week(date,i)

        weeks.append(
            {
            "kw" : tmp[0].isocalendar().week ,
            "year" : tmp[0].isocalendar().year ,
            "first" : tmp[0],
            "last" : tmp[-1]
            }
        )
    kw = date.isocalendar().week
   
    return render_template(
        'week_overview.html',
        page_title = "Wochenplan",
        weeks = weeks,
        kw = kw
    )

@bp.route('/week/<string:raw_date>')
@bp.route('/week')
def week(raw_date = datetime.today().date()):
    if type(raw_date) == str:
        given_date = datetime.fromisoformat(raw_date).date()
    else:
        given_date = raw_date
    week = get_week(given_date)
    plaene = []
    for day in week:
        res = db.session.scalars(select(Essensplan).filter_by(Datum=day)).one_or_none()
        if res is None:
            plaene.append(Essensplan(Datum=day))
        else:
            plaene.append(res)

    return render_template(
        'week.html',
        page_title = "Wochenplan",
        plaene = plaene
    )

def get_week(given_date,given_offset=0):
    weekday = given_date.isoweekday()
    # The start of the week
    start = ( given_date - timedelta(days=weekday-1) ) + timedelta(weeks=given_offset)
    # build a simple range
    dates = [start + timedelta(days=d) for d in range(5)]
    return dates


@bp.route('/week/edit/<string:raw_date>')
@bp.route('/week/edit/', defaults = {'raw_date' : datetime.today().date()})
@login_required
def edit_week(raw_date):
    form = EditWocheForm()
    if type(raw_date) == str:
        given_date = datetime.fromisoformat(raw_date).date()
    else:
        given_date = raw_date

    dates = get_week(given_date)

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
        rezepte=rezepte,
        form = form
    )


@bp.route('/einkaufsliste')
def einkaufsliste():
    return render_template(
        'einkaufsliste.html',
        page_title = "Einkaufsliste"
    )