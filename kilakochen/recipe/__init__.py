from flask import Blueprint

bp = Blueprint('recipe', __name__)

from kilakochen.recipe import views