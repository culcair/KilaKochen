from flask import Blueprint

bp = Blueprint('errors', __name__)

from kilakochen.errors import handlers