def test_home_overview(client):
    response = client.get("/")
    assert "kila-kochen.de" in response.get_data(as_text=True)
    assert response.status_code == 200


def test_today_overview(client):
    response = client.get("/today")
    assert response.status_code == 200
    assert "Essensplan von heute" in response.get_data(as_text=True)


# Tests für die Rezepte
def test_recipe_overview(client):
    response = client.get("/recipe/overview")
    assert "Übersicht der Rezepte" in response.get_data(as_text=True)
    assert "Rezept" in response.get_data(as_text=True)
    assert response.status_code == 200


def test_recipe_view(client, auth):
    # Erst ein Rezept anlegen
    from kilakochen.models import Recipe, RecipeCategory
    from kilakochen import db
    cat = RecipeCategory(name='Hauptspeise', code='H')
    r = Recipe(name='Testrezept', description='Bla', category=cat, author='Junie', active=True)
    db.session.add(cat)
    db.session.add(r)
    db.session.commit()
    
    response = client.get(f"/recipe/view/{r.id}")
    assert response.status_code == 200
    assert "Testrezept" in response.get_data(as_text=True)


def test_ingredients_overview(client):
    response = client.get("/ingredient/overview")
    assert "Übersicht der Zutaten" in response.get_data(as_text=True)
    assert response.status_code == 200


def test_week_overview(client):
    response = client.get("/week/overview")
    assert "Auswahl KW" in response.get_data(as_text=True)
    assert response.status_code == 200
