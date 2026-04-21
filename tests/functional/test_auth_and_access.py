from kilakochen.models import User, Recipe, RecipeCategory
from kilakochen import db

def test_login_logout(client, auth):
    # User anlegen
    user = User(username='testuser', active=True, level=10, first_name='Test', given_name='User')
    user.set_password('testpass')
    db.session.add(user)
    db.session.commit()

    # Login
    response = auth.login('testuser', 'testpass')
    assert response.status_code == 302
    
    response = client.get('/', follow_redirects=True)
    assert "logout" in response.get_data(as_text=True)
    assert "testuser" in response.get_data(as_text=True)

    # Logout
    response = auth.logout()
    assert response.status_code == 302
    response = client.get('/', follow_redirects=True)
    assert "login" in response.get_data(as_text=True)

def test_unauthorized_access(client):
    # Routen die login_required haben
    protected_routes = [
        '/recipe/new',
        '/ingredient/new',
        '/user/overview',
        '/today/edit'
    ]
    for route in protected_routes:
        response = client.get(route)
        assert response.status_code == 302
        assert '/auth/login' in response.headers['Location']

def test_admin_only_access(client, auth):
    # User mit niedrigem Level
    user = User(username='cook', active=True, level=5, first_name='Cook', given_name='User')
    user.set_password('pass')
    db.session.add(user)
    db.session.commit()

    auth.login('cook', 'pass')
    
    # User bearbeiten (anderer User) sollte fehlschlagen/umleiten
    admin = User(username='admin', active=True, level=15, first_name='Admin', given_name='User')
    admin.set_password('adminpass')
    db.session.add(admin)
    db.session.commit()
    
    response = client.get(f'/user/edit:{admin.id}', follow_redirects=True)
    assert "Keine Berechtigung" in response.get_data(as_text=True)
