from flask_login import current_user, login_required
from flask_wtf import FlaskForm
from sqlalchemy import select
from kilakochen.main import bp    
from flask import redirect, render_template, url_for
from flask_weasyprint import HTML, render_pdf
from datetime import datetime,timedelta
from kilakochen.models import Allergene, Essensplan, Rezepte, Zutaten

from kilakochen.main.forms import EditHeuteForm, EditWocheForm
from kilakochen import db

@bp.route('/')
def index():
    return render_template('index.html', page_title = "Startseite")

def get_rezepte(kategorie):
    res = Rezepte.query.with_entities(Rezepte.ID,Rezepte.Titel).filter(Rezepte.rezeptkategorien.has(Kuerzel=kategorie)).order_by(Rezepte.Titel).all()
    
    choices = [(None,"")] + [(x.ID, x.Titel) for x in res]
    return choices


@bp.route('/day/<string:raw_date>/edit', methods=['GET', 'POST'])
@bp.route('/today/edit', methods=['GET', 'POST'],defaults= {"raw_date" : datetime.today().date()})
@login_required
def day_edit(raw_date :str) :
    if type(raw_date) == str:
        given_date = datetime.fromisoformat(raw_date).date()
    else:
        given_date = raw_date
            
    plan : Essensplan = Essensplan.query.filter_by(Datum=given_date).one_or_none()
    form : EditHeuteForm = EditHeuteForm()
    
    if plan is not None:
        form.datum.data = plan.Datum
        if plan.Hauptgericht is not None:
            form.hauptgericht.choices = [(plan.Hauptgericht.ID,plan.Hauptgericht.Titel)] + get_rezepte("H")
        else:
            form.hauptgericht.choices = get_rezepte("H")

        if plan.Beilage is not None:
            form.beilage.choices = [(plan.Beilage.ID,plan.Beilage.Titel)] + get_rezepte("B")
        else:
            form.beilage.choices = get_rezepte("B")
        if plan.Dessert is not None:
            form.dessert.choices = [(plan.Dessert.ID,plan.Dessert.Titel)] +  get_rezepte("D")
        else:
            form.dessert.choices = get_rezepte("D")
    else:
        form.hauptgericht.choices = get_rezepte("H")
        form.beilage.choices = get_rezepte("B")
        form.dessert.choices = get_rezepte("D")
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
        return redirect(url_for('main.week',raw_date=given_date))
    
    return render_template('edit_day.html', form=form)

@bp.route('/day/<string:raw_date>')
@bp.route('/today')
def day(raw_date = None):
    if raw_date is None:
        given_date = datetime.today().date()
    else:
        given_date = datetime.fromisoformat(raw_date).date()
 
    data = Essensplan.query.filter_by(Datum=given_date).one_or_none()

    if data is None:
        data = Essensplan(Datum=given_date)
        
    db.session.add(data)
    db.session.commit()
    if current_user.is_authenticated:
        return redirect(url_for('main.day_edit',raw_date=given_date))
    else:
        return render_template(
            'today.html',
            date = given_date,
            page_title = "Essensplan von heute",
            plan=data
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



@bp.route('/week/<string:raw_date>/print')
@bp.route('/week/print')
def print_week(raw_date = None):
    if raw_date is None:
        given_date = datetime.today().date()
    else:
        given_date = datetime.fromisoformat(raw_date).date()

    given_week = get_week(given_date)
    kw = given_date.isocalendar().week
    plaene = []
    for given_day in given_week:
        res = db.session.scalars(select(Essensplan).filter_by(Datum=given_day)).one_or_none()
        if res is None:
            plaene.append(Essensplan(Datum=given_day))
        else:
            plaene.append(res)

    html_string = render_template(
        'print_week.html',
        page_title = "Wochenplan",
        plaene = plaene,
        kw = kw
    )
    tmp = HTML(string=html_string)
#    return html_string
    download_filename = "Wochenplan-KW{}.pdf".format(kw)
    return render_pdf(tmp,automatic_download=True,download_filename=download_filename)

@bp.route('/week/<string:raw_date>')
@bp.route('/week')
def week(raw_date = None):
    if raw_date is None:
        given_date = datetime.today().date()
    else:
        given_date = datetime.fromisoformat(raw_date).date()
    given_week = get_week(given_date)
    kw = given_date.isocalendar().week
    previous_week = given_week[0] + timedelta(weeks=-1)
    next_week = given_week[0] + timedelta(weeks=1)

    plaene = []
    for given_day in given_week:
        res = db.session.scalars(select(Essensplan).filter_by(Datum=given_day)).one_or_none()
        if res is None:
            plaene.append(Essensplan(Datum=given_day))
        else:
            plaene.append(res)

    return render_template(
        'week.html',
        page_title = "Wochenplan",
        plaene = plaene,
        kw = kw,
        previous = previous_week,
        next = next_week
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
        res = Essensplan.query.filter_by(Datum=week_date).one_or_none()
        if res is None:
            tmp = Essensplan(Datum=week_date)
        else:
            tmp = res
        plaene.append(tmp)

    rezepte = Rezepte.query.all() 

    return render_template(
        'edit_week.html',
        page_title = "Wochenplan",
        data=dates,
        plaene=plaene,
        rezepte=rezepte,
        form = form
    )

@bp.route('/forbidden')
def forbidden():
    return render_template('errors/403.html'), 403

@bp.route('/einkaufsliste')
def einkaufsliste():
    return render_template(
        'einkaufsliste.html',
        page_title = "Einkaufsliste"
    )

