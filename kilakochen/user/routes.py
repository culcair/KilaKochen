from datetime import datetime, timezone

from sqlalchemy.exc import SQLAlchemyError
from werkzeug import Response

from kilakochen import db
from kilakochen.user import bp
from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from kilakochen.models import User
from kilakochen.user.forms import CreateUserForm, EditUserForm


@bp.route("/overview", methods=["GET", "POST"])
@login_required
def overview():
    all_users = db.session.query(User).all()
    return render_template("user/overview.html", data=all_users)


def create_user(
    form : CreateUserForm
) -> dict:
    """
    Erzeugt einen neuen Benutzer.

    :param form: Benutzername
    """
    try:
        username = form.username.data
        if not db.session.query(
            User.query.filter_by(username=username).exists()
        ).scalar():
            new_user = User()
            form.populate_obj(new_user)
            db.session.add(new_user)
            new_user.set_password(form.password.data)
            db.session.commit()
            return {
                "message": f"Benutzer erfolgreich angelegt ({username})",
                "category": "success",
            }

        else:
            return {
                "message": f"Benutzername ist nicht eindeutig. Benutzer wurde nicht angelegt (Benutzername={username})",
                "category": "danger",
            }
    except Exception as e:
        db.session.rollback()
        return {
            "message": f"Fehler beim Erstellen des Benutzer: {str(e)}",
            "category": "warning",
        }


@bp.route("/edit:<int:user_id>", methods=["GET", "POST"])
@login_required
def edit(user_id: int) -> Response | str | tuple[str, int]:
    if current_user.is_authenticated:
        user = User.query.filter_by(id=user_id).first()
        form = EditUserForm(obj=user)
        if form.validate_on_submit():
            user.first_name = form.first_name.data
            user.given_name = form.given_name.data
            user.email = form.email.data
            user.username = form.username.data
            if form.password.data:
                user.set_password(form.password.data)
            user.level = form.access_level.data
            user.updated_at = datetime.now(timezone.utc)
            db.session.commit()
            return redirect(url_for("user.overview"))

        return render_template("user/edit.html", form=form)
    else:
        return render_template("errors/401.html"), 401


@bp.route("/delete:<int:user_id>", methods=["GET", "POST"])
@login_required
def status_change(user_id: int):
    if current_user.is_authenticated:
        if current_user.level >= User.ADMIN_LEVEL:
            try:
                user = User.query.filter_by(id=user_id).first()
                user.active = not user.active
                db.session.commit()
                if user.active:
                    flash(f"Benutzer {user.username} wurde aktviert!", "success")
                else:
                    flash(f"Benutzer {user.username} wurde deaktviert!", "danger")
            except SQLAlchemyError as e:
                print(e)
                db.session.rollback()

            return redirect(url_for("user.overview"))
        else:

            flash(f"Keine Berechtigung zum löschen!", "danger")
            return redirect(url_for("user.overview"))


@bp.route("/new", methods=["GET", "POST"])
@login_required
def new():
    if current_user.is_authenticated:
        form = CreateUserForm()
        if form.validate_on_submit():
            if current_user.level >= int(form.access_level.data):
                result = create_user(form)
                flash(result["message"], category=result["category"])
                return redirect(url_for("user.overview"))
        else:
            return render_template("user/new.html", form=form)
    else:
        return render_template("errors/401.html"), 401
