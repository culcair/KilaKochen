import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_babel import Babel, lazy_gettext as _l
from flask_bootstrap import Bootstrap5
from flask_talisman import Talisman
from sqlalchemy import MetaData
from config import Config
from flask_wtf import CSRFProtect

def get_locale():
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])


migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')
babel = Babel()
talisman = Talisman()
bootstrap = Bootstrap5()
csrf =CSRFProtect()

metadata = MetaData(
    naming_convention={
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
    }
)

db=SQLAlchemy(metadata=metadata)

def get_version() -> str :
    try:
        with open(".git/refs/heads/main","r") as git_file:
            app_version = git_file.readline()[:8]
    except FileNotFoundError as e :
        app_version = ""
    return app_version

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    print(app.config['SQLALCHEMY_DATABASE_URI'])
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    babel.init_app(app, locale_selector=get_locale)
    bootstrap.init_app(app)
    csrf.init_app(app)
    talisman.init_app(app)

    from kilakochen.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from kilakochen.user import bp as user_bp
    app.register_blueprint(user_bp, url_prefix='/user')

    from kilakochen.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from kilakochen.recipe import bp as bp
    app.register_blueprint(bp, url_prefix='/recipe')

    from kilakochen.main import bp as main_bp
    app.register_blueprint(main_bp)

    from kilakochen.cli import bp as cli_bp
    app.register_blueprint(cli_bp)

    if app.config['CONTENT_SECURITY_POLICY']:
        talisman.content_security_policy = app.config['CONTENT_SECURITY_POLICY']

    app.config["KILAKOCHEN_VERSION"] = get_version()

    if not app.debug and not app.testing:
        bootstrap.bootstrap_js_filename = app.config["BOOTSTRAP_JS_FILENAME"]

        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['ADMINS'], subject='KiLa Kochen Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/kilakochen.log',
                                           maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('kilakochen startup')

    return app


from kilakochen import models
