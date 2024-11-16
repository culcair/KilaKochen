from flask import Blueprint

bp = Blueprint("ingredient", __name__)

from kilakochen.ingredient import views
