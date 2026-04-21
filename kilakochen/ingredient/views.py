import sqlalchemy
from flask import flash, redirect, render_template, url_for, request
from flask_login import login_required
from sqlalchemy import select
from sqlalchemy.orm import load_only
from werkzeug.exceptions import NotFound

from kilakochen import db
from kilakochen.ingredient import bp
from kilakochen.ingredient.forms import IngredientForm
from kilakochen.models import Ingredient, Allergen


@bp.route("/")
@bp.route("/overview")
def overview():
    data = Ingredient.query.filter_by(active=True).order_by(Ingredient.name).all()
#    data = Ingredient.query.order_by(Ingredient.name).all()
    stmt = select(Allergen).options(load_only(Allergen.name, Allergen.code)).order_by(Allergen.name)
    allergens = db.session.execute(stmt).scalars().all()
    allergen_str = ", ".join(f"{allergen.code}= {allergen.name}" for allergen in allergens)

    return render_template(
        "ingredient/overview.html", page_title="Übersicht der Zutaten", data=data,allergens=allergen_str
    )


@bp.route("/view/<int:ingredient_id>/")
def view(ingredient_id):

    if request.referrer:
        back_ref_url = request.referrer
    else:
        back_ref_url = ""
    ingredient: Ingredient = Ingredient.query.filter_by(id=ingredient_id).one_or_404()
    return render_template(
        "ingredient/view.html",
        page_title="Zutat | " + ingredient.name,
        ingredient=ingredient,
        back_ref_url=back_ref_url,
    )


def edit_or_new_ingredient(form: IngredientForm, modus: str):
    name = form.name.data
    try:
        if modus == "new" and not db.session.query(
            Ingredient.query.filter_by(name=name).exists()
        ).scalar():
            new_ingredient = Ingredient()
            form.populate_obj(new_ingredient)
            db.session.add(new_ingredient)
            db.session.commit()
            flash(f"Zutat {new_ingredient.name} angelegt.",category="success")
        elif modus == "edit":
            ingredient = Ingredient.query.filter_by(name=name).first()
            form.populate_obj(ingredient)
            db.session.add(ingredient)
            db.session.commit()
            flash(f"Zutat {ingredient.name} angepasst.", category="success")
        else:
            flash(f"Zutat mit dem Namen {name} ist schon vorhanden.",category="warning")

    except sqlalchemy.exc.IntegrityError as e:
        db.session.rollback()
        flash(f"Fehler beim Anlegen: {e}",category="danger")


@bp.route("/new", methods=["GET", "POST"])
@login_required
def new():
    form = IngredientForm()
    if form.validate_on_submit():
        edit_or_new_ingredient(form, "new")
        return redirect(url_for("ingredient.overview"))

    return render_template("ingredient/new.html", form=form)


@bp.route("/edit/<int:ingredient_id>", methods=["GET", "POST"])
@login_required
def edit(ingredient_id):
    if db.session.query(
            Ingredient.query.filter_by(id=ingredient_id).exists()
    ).scalar():
        ingredient = Ingredient.query.filter_by(id=ingredient_id).one_or_none()
        form = IngredientForm(obj=ingredient)
        form.submit.label.text = f"Änderung speichern"
        if form.validate_on_submit():
            edit_or_new_ingredient(form, "edit")
            return redirect(url_for("ingredient.overview"))

        return render_template("ingredient/edit.html",
                               form=form,
                               data=ingredient
                               )

    else:
        raise NotFound