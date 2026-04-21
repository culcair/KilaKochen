from flask import session
from flask_login import current_user
from kilakochen.models import User
from kilakochen import db

def test_secret_route_unauthenticated(client):
    response = client.get('/user/overview')
    assert "/auth/login" in response.headers["Location"]

def test_login(client, auth):
    # User anlegen
    user = User(username='ch', active=True, level=10, first_name='Test', given_name='User')
    user.set_password('test')
    db.session.add(user)
    db.session.commit()

    assert client.get('/auth/login').status_code == 200
    response = auth.login('ch', 'test')
    assert response.status_code == 302