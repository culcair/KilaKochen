from unicodedata import category

from flask_login import login_required, current_user
from flask_weasyprint import HTML, render_pdf
from sqlalchemy import func

from kilakochen.models import Recipe, RecipeCategory
from kilakochen.recipe import bp

from flask import flash, redirect, render_template, url_for, request

from kilakochen import db
from kilakochen.recipe.forms import RecipeForm, IngredientForm


def create_new_recipe( form : RecipeForm ) -> str:
    """
    Erstellt ein neues Rezept und fügt die Zutaten hinzu.

    """
    try:
        if db.session.query(
            Recipe.query.filter_by(name=form.name.data).exists()
        ).scalar():
            return f"Fehler"
        else:
            return "Alles gut"
    except Exception as e:
        return f"Fehler"


def get_count():
    return (
        db.session.query(
            RecipeCategory.name,  # Name der Kategorie
            func.count(Recipe.id).label("recipe_count")  # Anzahl der Rezepte
        )
        .join(Recipe, Recipe.category_id == RecipeCategory.id)  # Join zwischen Recipe und RecipeCategory
        .group_by(RecipeCategory.name)  # Gruppieren nach Kategorie
        .all()
    )

@bp.route("/")
@bp.route("/overview")
def overview():
    if current_user.is_authenticated:
        data = Recipe.query.order_by(Recipe.name).all()
    else:
        data = Recipe.query.filter_by(active=True).order_by(Recipe.name).all()
    return render_template(
        "recipe/overview.html", page_title="Übersicht der Rezepte", data=data,categories=get_count()
    )



@bp.route("/view/<int:recipe_id>")
def view(recipe_id):
    if request.referrer:
        back_ref_url = request.referrer
    else:
        back_ref_url = ""
    data = Recipe.query.filter_by(id=recipe_id).one_or_404()
    allergens = set()
    for recipe_ingredient in data.ingredients:
        for allergen in recipe_ingredient.ingredient.allergens:
            allergens.add(allergen.name)


    return render_template(
        "recipe/view.html",
        page_title="Rezept | " + data.name,
        rezept_name=data.name,
        data=data,
        allergens=' , '.join(allergens),
        back_ref_url=back_ref_url,
    )


@bp.route("/print/<int:recipe_id>")
def recipe_print(recipe_id):
    data = Recipe.query.filter_by(id=recipe_id).one_or_404()

    html_string = render_template(
        "recipe/print.html",
        page_title="Rezept - " + data.name,
        rezept_name=data.name,
        data=data,
    )

    tmp = HTML(string=html_string)

    download_filename = "{}_{}.pdf".format("KiLaKochen", data.id)
    return render_pdf(tmp, automatic_download=True, download_filename=download_filename)


@bp.route("/new", methods=["GET", "POST"])
@login_required
def new():
    form = RecipeForm()
    template_form = IngredientForm(prefix="ingredient-_-")
    if form.validate_on_submit():
        result = create_new_recipe(form)
        flash(result, category="info")
        return redirect(url_for("recipe.overview"))

    return render_template("recipe/new.html", form=form, _template=template_form)


@bp.route("/edit/<int:recipe_id>", methods=["GET", "POST"])
def edit(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).one_or_404()
    form = RecipeForm(obj=recipe)
    template_form = IngredientForm(prefix="ingredient-_-")

    if form.validate_on_submit():
        form.populate_obj(recipe)
        db.session.commit()
        url_recipe = url_for("recipe.view",recipe_id=recipe.id)
        flash(f'Das Rezept <a href="{url_recipe}">{recipe.name}</a> wurde aktualisiert',category="success")
        return redirect(url_for("recipe.overview"))

    return render_template("recipe/edit.html", form=form, _template=template_form,recipe=recipe)

