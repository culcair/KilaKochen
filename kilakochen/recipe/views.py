import logging

from flask import flash, redirect, render_template, url_for, request
from flask_login import login_required, current_user
from flask_weasyprint import HTML, render_pdf
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError

from kilakochen import db
from kilakochen.models import Recipe, RecipeCategory, RecipeIngredient
from kilakochen.recipe import bp
from kilakochen.recipe.forms import RecipeForm, IngredientForm
from sqlalchemy import func, select
from typing import Dict, Any

logger = logging.getLogger("recipe")

def create_new_recipe(form: RecipeForm) -> str:
    """
    Erstellt ein neues Rezept und fügt die Zutaten hinzu.
    Returns: Erfolgsmeldung oder Fehlermeldung
    """
    if db.session.query(
            Recipe.query.filter_by(name=form.name.data).exists()
    ).scalar():
        return f"Fehler: Ein Rezept mit dem Namen '{form.name.data}' existiert bereits."
    else:
        new_recipe = Recipe(
            name=form.name.data,
            description=form.description.data,
            category=form.category.data,
            author=form.author.data,
            active=True
        )
        db.session.add(new_recipe)

        for entry in form.ingredients.entries:
            data = entry.data
            new_ingredient = RecipeIngredient(
                ingredient=data["ingredient"],
                amount=data["amount"],
                unit=data["unit"],
                recipe=new_recipe
            )
            db.session.add(new_ingredient)
    try:
        db.session.commit()
        return f"Neues Rezept ({new_recipe.name}) wurde angelegt."
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Fehler beim Erstellen des Rezepts: {e}")
        return "Fehler beim Erstellen des Rezepts. Bitte versuchen Sie es erneut."

def get_recipe_counts_by_category(
    *,
    only_active: bool = True,
) -> Dict[str, Any]:
    """
    Liefert die Anzahl der Rezepte pro Kategorie sowie die Gesamtanzahl.

    Rückgabeformat:
    {
        "total": int,
        "categories": [
            {"id": int, "name": str, "count": int},
            ...
        ]
    }
    """
    recipe_join_condition = Recipe.category_id == RecipeCategory.id
    if only_active:
        recipe_join_condition &= Recipe.active.is_(True)

    stmt = (
        select(
            RecipeCategory.id,
            RecipeCategory.name,
            func.count(Recipe.id).label("count"),
        )
        .outerjoin(Recipe, recipe_join_condition)
        .where(
            RecipeCategory.active.is_(True)
            if only_active
            else True
        )
        .group_by(RecipeCategory.id, RecipeCategory.name)
        .order_by(RecipeCategory.name)
    )

    rows = db.session.execute(stmt).all()

    total = sum(row.count for row in rows)

    return {
        "total": total,
        "categories": [
            {
                "id": row.id,
                "name": row.name,
                "count": row.count,
            }
            for row in rows
        ],
    }



@bp.route("/")
@bp.route("/overview")
def overview():
    category = request.args.get("category_id")
    
    query = Recipe.query.order_by(Recipe.name)
    if category:
        query = query.filter(Recipe.category_id == category)

    if current_user.is_authenticated:
        data = query.all()
    else:
        data = query.filter_by(active=True).all()

    logger.info(get_recipe_counts_by_category())

    return render_template(
        "recipe/overview.html",
        page_title="Übersicht der Rezepte",
        data=data,
        categories=get_recipe_counts_by_category()
    )

@bp.route("/view/<int:recipe_id>")
def view(recipe_id):
    if request.referrer:
        back_ref_url = request.referrer
    else:
        back_ref_url = ""

    data : Recipe = Recipe.query.filter_by(id=recipe_id).one_or_404()

    return render_template(
        "recipe/view.html",
        page_title="Rezept | " + data.name,
        rezept_name=data.name,
        data=data,
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
        page_orientation="portrait",
    )

    tmp = HTML(string=html_string)

    download_filename = "{}_{}.pdf".format("KiLaKochen", data.id)
    return render_pdf(tmp, automatic_download=True, download_filename=download_filename)


@bp.route("/new", methods=["GET", "POST"])
@login_required
def new():
    form = RecipeForm()
    template_form = IngredientForm(prefix="ingredients-_-")
    if form.validate_on_submit():
        result = create_new_recipe(form)
        if "Fehler" in result:
            flash(result, category="danger")
        else:
            flash(result, category="success")
        return redirect(url_for("recipe.overview"))

    return render_template("recipe/new.html", form=form, _template=template_form)


@bp.route("/edit/<int:recipe_id>", methods=["GET", "POST"])
@login_required
def edit(recipe_id):
    recipe = Recipe.query.filter_by(id=recipe_id).one_or_404()
    form = RecipeForm(obj=recipe)
    template_form = IngredientForm(prefix="ingredients-_-")

    if form.validate_on_submit():
        recipe.name = form.name.data
        recipe.description = form.description.data
        recipe.author = form.author.data
        recipe.category = form.category.data
        recipe.active = form.active.data
        
        # Zutaten synchronisieren
        recipe.ingredients.clear()
        for i_form in form.ingredients:
            ri = RecipeIngredient(
                ingredient=i_form.ingredient.data,
                amount=i_form.amount.data,
                unit=i_form.unit.data
            )
            recipe.ingredients.append(ri)

        try:
            db.session.commit()
            url_recipe = url_for("recipe.view",recipe_id=recipe.id)
            flash(f'Das Rezept <a href="{url_recipe}">{recipe.name}</a> wurde aktualisiert',category="success")
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Fehler beim Aktualisieren des Rezepts {recipe.id}: {e}")
            flash("Fehler beim Aktualisieren des Rezepts.", category="danger")
        return redirect(url_for("recipe.overview"))

    return render_template("recipe/edit.html", form=form, _template=template_form,recipe=recipe)

