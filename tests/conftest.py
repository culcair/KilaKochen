import pytest
import os
# Mock SECRET_KEY for testing
os.environ['SECRET_KEY'] = 'test-secret-key'

from kilakochen import create_app, db

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['DEBUG'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='ch', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)