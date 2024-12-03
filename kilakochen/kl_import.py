from kilakochen.models import Ingredient, RecipeIngredient, Unit, Recipe, RecipeCategory




def get_ingredient(old_rezept: Rezepte, recipe_id: int) -> list[RecipeIngredient]:
    result = []
    for zutat in old_rezept.rezepte_zutaten:
        try:
            ingredient = Ingredient.query.filter_by(
                name=zutat.zutaten.Bezeichnung
            ).one_or_none()
            unit = Unit.query.filter_by(name=zutat.einheiten.Bezeichnung).one_or_none()
            if ingredient is not None:
                tmp = RecipeIngredient(
                    recipe_id=recipe_id,
                    ingredient=ingredient,
                    amount=zutat.Menge,
                    unit=unit,
                )
                result.append(tmp)
        except AttributeError as e:
            print(e)
            print(
                f"Rezept: {old_rezept.Titel} Zutaten: {old_rezept.rezepte_zutaten} zutat:{zutat}"
            )

    return result


def get_recipe_category_id(bezeichnung: str | None) -> int | None:
    if bezeichnung is None:
        return None
    else:
        tmp = RecipeCategory.query.filter_by(name=bezeichnung).one_or_none()
        return tmp.id if tmp is not None else None


def migrate_recipes(db):
    rezepte = Rezepte.query.count()
    for rezept in Rezepte.query.all():
        print(rezept.Titel)
        if rezept.rezeptkategorien is not None:
            cat_id = get_recipe_category_id(rezept.rezeptkategorien.BezeichnungSingular)
        else:
            cat_id = 4
        new_recipe = None
        new_recipe = Recipe(
            name=rezept.Titel,
            description=rezept.Zubereitung,
            author="system",
            active=True,
            category_id=cat_id,
        )
        db.session.add(new_recipe)
        db.session.commit()
        new_recipe.ingredients = get_ingredient(rezept, new_recipe.id)
        db.session.commit()

    recipes = Recipe.query.count()

    print(f"Anzahl alter Rezepte:{rezepte} Anzahl neuer Rezepte:{recipes}")
