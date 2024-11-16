def test_home_overview(client):
    response = client.get("/")
    assert b"Symbolbild" in response.data
    assert response.status_code == 200


def test_today_overview(client):
    response = client.get("/today")
    assert response.status_code == 200
    assert b"Heute ist" in response.data


# Tests für die Rezepte
def test_recipe_overview(client):
    response = client.get("/recipe/overview")
    assert b"Anzahl aller Rezepte" in response.data
    assert b"Rezeptname" in response.data
    assert response.status_code == 200


def test_recipe_view(client):
    recipe_range = range(1, 11)
    for i in recipe_range:
        response = client.get(f"/recipe/view/{i}")
        assert response.status_code == 200


def test_ingredients_overview(client):
    response = client.get("/ingredient/overview")
    assert b"Anzahl aller Zutaten" in response.data
    assert b"Zutaten Gruppe" in response.data
    assert response.status_code == 200


def test_week_overview(client):
    response = client.get("/week/overview")
    assert b"Auswahl KW" in response.data
    assert response.status_code == 200
