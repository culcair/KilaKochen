from flask_login import current_user, login_required
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from kilakochen.main import bp
from flask import redirect, render_template, url_for, flash
from flask_weasyprint import HTML, render_pdf
from datetime import datetime, timedelta, date

from kilakochen.models import MealPlan, Recipe

from kilakochen.main.forms import EditDayForm
from kilakochen import db


@bp.route("/")
def index():
    return render_template("index.html", page_title="Startseite")

def get_rezepte(kategorie):
    res = (
        Recipe.query.with_entities(Recipe.ID, Recipe.Titel)
        .filter(Recipe.category.has(code=kategorie))
        .order_by(Recipe.name)
        .all()
    )

    choices = [(None, "")] + [(x.ID, x.Titel) for x in res]
    return choices

@bp.route("/stats")
def stats():
    meals  = {}
    for meal_plan in MealPlan.query.all():
        if meal_plan.main_dish is not None:


            if meal_plan.main_dish_id in meals:
                meals[meal_plan.main_dish_id]["count"] += 1
            else:
                meals[meal_plan.main_dish_id] = {
                    "count":1,
                    "name" : meal_plan.main_dish.name
                }
    return render_template(
        "stats.html",
        meals=meals
    )

def populate_editheuteform(plan : MealPlan, form : EditDayForm, given_date):
    if plan is not None:
        form.date.data = plan.date
        if plan.main_dish is not None:
            form.main_dish.choices = [
                (plan.main_dish.id, plan.main_dish.name)
            ] + get_rezepte("H")
        else:
            form.main_dish.choices = get_rezepte("H")

        if plan.side_dish is not None:
            form.side_dish.choices = [
                (plan.side_dish.id, plan.side_dish.name)
            ] + get_rezepte("B")
        else:
            form.side_dish.choices = get_rezepte("B")
        if plan.dessert is not None:
            form.dessert.choices = [
                (plan.dessert.id, plan.dessert.name)
            ] + get_rezepte("D")
        else:
            form.dessert.choices = get_rezepte("D")
    else:
        plan = MealPlan(date=given_date)
        form.main_dish.choices = get_rezepte("H")
        form.side_dish.choices = get_rezepte("B")
        form.dessert.choices = get_rezepte("D")
        form.date.data = given_date

    return plan, form


def get_date( raw_date : date | str) -> date :
    """
    :param raw_date:
    :return: given_date
    """
    if type(raw_date) == str:
        given_date = datetime.fromisoformat(raw_date).date()
    else:
        given_date = raw_date
    return given_date


@bp.route("/day/<string:raw_date>/edit", methods=["GET", "POST"])
@bp.route(
    "/today/edit",
    methods=["GET", "POST"],
    defaults={"raw_date": datetime.today().date()},
)
@login_required
def day_edit(raw_date: str):
    given_date = get_date(raw_date)
    plan: MealPlan = MealPlan.query.filter_by(date=given_date).one_or_none()
    if plan is None:
        plan = MealPlan(date=given_date)

    form: EditDayForm = EditDayForm(obj=plan)

    if form.validate_on_submit():
        form.populate_obj(plan)
        try:
            db.session.add(plan)
            db.session.commit()
            flash(f"Speiseplan vom {plan.date} wurde aktualisiert.", "success")
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"Es trat eine Fehler bei der Aktualisierung vom Speiseplan {plan.date} auf. {e}", "danger")

        return redirect(url_for("main.week", raw_date=given_date))

    return render_template("edit_day.html", form=form)

@bp.get("/day/<string:raw_date>")
@bp.get("/today",defaults={"raw_date": datetime.today().date()})
def day(raw_date):
    given_date = get_date(raw_date)

    data = MealPlan.query.filter_by(date=given_date).one_or_none()

    if current_user.is_authenticated and data is None:
        return redirect(url_for("main.day_edit", raw_date=given_date))
    else:
        return render_template(
            "today.html",
            date=given_date,
            page_title="Essensplan von heute",
            plan=data,
        )


@bp.route("/week/overview")
def week_overview():
    given_date = datetime.today().date()
    prefix = 3
    weeks = []
    for i in range(2 - prefix, 2 + prefix):
        tmp = get_week(given_date, i)

        weeks.append(
            {
                "kw": tmp[0].isocalendar().week,
                "year": tmp[0].isocalendar().year,
                "first": tmp[0],
                "last": tmp[-1],
            }
        )
    kw = given_date.isocalendar().week

    return render_template(
        "week_overview.html", page_title="Wochenplan", weeks=weeks, kw=kw
    )


@bp.route("/week/print/<string:raw_date>")
@bp.route("/week/print")
def print_week(raw_date=None):
    given_date = get_date(raw_date)
    given_week = get_week(given_date)
    kw = given_date.isocalendar().week
    plaene = []
    for given_day in given_week:
        res = db.session.scalars(
            select(MealPlan).filter_by(date=given_day)
        ).one_or_none()
        if res is None:
            plaene.append(MealPlan(date=given_day))
        else:
            plaene.append(res)

    html_string = render_template(
        "print_week.html", page_title="Wochenplan", plaene=plaene, kw=kw
    )
    tmp = HTML(string=html_string)
    #    return html_string
    download_filename = "Wochenplan-KW{}.pdf".format(kw)
    return render_pdf(tmp, automatic_download=True, download_filename=download_filename)


@bp.route("/week/<string:raw_date>")
@bp.route("/week")
def week(raw_date=None):
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
        plan = db.session.scalars(
            select(MealPlan).filter_by(date=given_day)
        ).one_or_none()
        if plan is None:
            plaene.append(MealPlan(date=given_day))
        else:
            plaene.append(plan)


    return render_template(
        "week.html",
        page_title="Wochenplan",
        plaene=plaene,
        kw=kw,
        previous=previous_week,
        next=next_week,
    )


def get_week(given_date, given_offset=0):
    weekday = given_date.isoweekday()
    # The start of the week
    start = (given_date - timedelta(days=weekday - 1)) + timedelta(weeks=given_offset)
    # build a simple range
    dates = [start + timedelta(days=d) for d in range(5)]
    return dates


@bp.route("/week/edit/<string:raw_date>", methods=["GET", "POST"])
@bp.route(
    "/week/edit",
    methods=["GET", "POST"],
    defaults={"raw_date": datetime.today().date()},
)
@login_required
def edit_week(raw_date):
    given_date = get_date(raw_date)
    given_week = get_week(given_date)
    kw = given_date.isocalendar().week
    previous_week = given_week[0] + timedelta(weeks=-1)
    next_week = given_week[0] + timedelta(weeks=1)

    plaene = []
    day_forms = []
    for given_day in given_week:
        plan = db.session.scalars(select(MealPlan).filter_by(date=given_day)).one_or_none()
        if plan is None:
            plan = MealPlan(date=given_day)
        form = EditDayForm(prefix=f"plan_{given_day}",obj=plan)
        day_forms.append(form)
        plaene.append(plan)

    for day_form in day_forms:
        if day_form.submit.data:
            if day_form.validate_on_submit():
                edit_plan = None
                for find_plan in plaene:
                    if find_plan.date == day_form.date.data:
                        edit_plan = find_plan
                day_form.populate_obj(edit_plan)
                db.session.add(edit_plan)
                db.session.commit()

    return render_template(
        "edit_week.html",
        page_title="Wochenplan",
        plaene=plaene,
        forms=day_forms,
        kw=kw,
        previous=previous_week,
        next=next_week,
    )


@bp.route("/forbidden")
def forbidden():
    return render_template("errors/403.html"), 403


@bp.route("/einkaufsliste")
def einkaufsliste():
    return render_template("einkaufsliste.html", page_title="Einkaufsliste")
