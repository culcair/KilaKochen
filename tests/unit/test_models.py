from kilakochen.models import User, Recipe, Ingredient, RecipeCategory

def test_new_user():
    u = User(username='test', given_name='Test', first_name='User', level=5)
    u.set_password('cat')
    assert u.username == 'test'
    assert u.check_password('cat')
    assert not u.check_password('dog')
    assert u.level == 5

def test_recipe_model(client):
    cat = RecipeCategory(name='Hauptspeise', code='H')
    r = Recipe(name='Nudeln', description='Kochen', category=cat, author='Junie')
    assert r.name == 'Nudeln'
    assert r.category.code == 'H'
    assert r.author == 'Junie'

def test_ingredient_model(client):
    i = Ingredient(name='Salz', active=True)
    assert i.name == 'Salz'
    assert i.active is True
