import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['webmaster@kinderladen-jakobistrasse.de']
    LANGUAGES = ['en', 'de']
    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    BOOTSTRAP_BOOTSWATCH_THEME = "minty"
    BOOTSTRAP_SERVE_LOCAL = True
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE') or True
    REMEMBER_COOKIE_SECURE = os.environ.get('REMEMBER_COOKIE_SECURE') or True
