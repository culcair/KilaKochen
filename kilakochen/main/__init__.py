from flask import Blueprint

bp = Blueprint('main', __name__)

from kilakochen.main import views, filter