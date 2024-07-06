from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = "users"
    
    id            = db.Column(db.Integer, primary_key=True)
    login         = db.Column(db.String(80), nullable=False)
    password_hash = db.Column(db.String(50))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash,password)
    


def init_db():
    db.create_all()
    # Einfügen von Beispieldaten

if __name__ == '__main__':
    with current_app.app_context():
        init_db()
