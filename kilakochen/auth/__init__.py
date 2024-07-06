from flask import Blueprint

bp = Blueprint('auth', __name__)

from kilakochen.auth import forms, routes