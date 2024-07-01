from flask import current_app, g
import click
from flask_sqlalchemy import SQLAlchemy
import os

import csv

db = SQLAlchemy()

class Phonebook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vorname = db.Column(db.String(80), nullable=False)
    nachname = db.Column(db.String(80), nullable=False)
    mobiltelefon = db.Column(db.String(30), nullable=False)
    standort = db.Column(db.String(30), nullable=False)

def init_db():
    db.create_all()
    # Einfügen von Beispieldaten
    if not Phonebook.query.first():
        with open('phonebook/examples/data.csv') as data:
            data_reader = csv.DictReader(data,delimiter=";")
            for row in data_reader:
                entry = Phonebook(**row)
                db.session.add(entry)
        db.session.commit()

if __name__ == '__main__':
    with current_app.app_context():
        init_db()
