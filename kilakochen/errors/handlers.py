from flask import render_template
from kilakochen import db
from kilakochen.errors import bp


@bp.app_errorhandler(401)
def not_found_error(error):
    print(error)
    return render_template("errors/401.html"), 401


@bp.app_errorhandler(403)
def not_allowed(error):
    print(error)
    return render_template("errors/403.html"), 403


@bp.app_errorhandler(404)
def not_found_error(error):
    print(error)
    return render_template("errors/404.html"), 404


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    print(error)
    return render_template("errors/500.html"), 500
