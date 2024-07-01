import os

from flask_bootstrap import Bootstrap5
from flask import Flask, render_template
from datetime import datetime

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='devUESTRA',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        SQLALCHEMY_DATABASE_URI = 'sqlite:///phonebook.db',
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
        BOOTSTRAP_BOOTSWATCH_THEME = "minty",
        BOOTSTRAP_SERVE_LOCAL = True

    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    bootstrap = Bootstrap5(app)

    @app.route('/')
    def index():
        return render_template('index.html', page_title = "Startseite")
    
    @app.route('/heute')
    def heute():
        date = datetime.now()
        return render_template(
            'heute.html',
            date = date,
            page_title = "Essensplan von heute"
        )
    
    @app.route('/rezepte')
    def rezepte():
        return render_template('rezepte.html', page_title = "Übersicht der Rezepte")

    @app.route('/zutaten')
    def zutaten():
        return render_template('zutaten.html', page_title = "Übersicht aller Zutaten")

    @app.route('/wochenplan')
    def wochenplan():
        return render_template('wochenplan.html', page_title = "Wochenplan")
    
    @app.route('/einkaufsliste')
    def einkaufsliste():
        return render_template('einkaufsliste.html', page_title = "Einkaufsliste")    

    return app    


