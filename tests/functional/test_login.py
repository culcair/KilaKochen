from flask import session, g
from flask_login import current_user


def test_secret_route_unauthenticated(client):
    # passes
    response = client.get('/user/overview')
    assert response.headers["Location"] == "/auth/login?next=%2Fuser%2Foverview"

def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/"

    client.get('/')
    assert session['user_id'] == 1
    assert g.user['username'] == 'ch'