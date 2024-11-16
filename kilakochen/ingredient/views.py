import sqlalchemy
from flask_login import login_required
from sqlalchemy import select
from sqlalchemy.orm import load_only

from kilakochen import db
from kilakochen.ingredient.forms import IngredientForm
from kilakochen.models import Ingredient, Allergen, IngredientsGroup
from kilakochen.ingredient import bp


from flask import flash, redirect, render_template, url_for, request


@bp.route("/")
@bp.route("/overview")
def overview():
    data = Ingredient.query.filter_by(active=True).order_by(Ingredient.name).all()
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


def create_new_ingredient( form : IngredientForm ) -> (bool, str):
    name = form.name.data
    try:
        if not db.session.query(
            Ingredient.query.filter_by(name=name).exists()
        ).scalar():
            new_ingredient = Ingredient()
            form.populate_obj(new_ingredient)
            db.session.add(new_ingredient)
            db.session.commit()
            return True, new_ingredient.name

    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        return False, name


@bp.route("/new", methods=["GET", "POST"])
@login_required
def new():
    form = IngredientForm()
    if form.validate_on_submit():
        result = create_new_ingredient(form)
        flash(result, category="info")
        return redirect(url_for("ingredient.overview"))

    return render_template("ingredient/new.html", form=form)


@bp.route("/edit/<int:ingredient_id>")
def edit(ingredient_id):
    return redirect(url_for("ingredient.view", ingredient_id=ingredient_id))
