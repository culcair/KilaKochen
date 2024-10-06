from flask import Blueprint

bp = Blueprint('user', __name__)

from kilakochen.user import forms, routes