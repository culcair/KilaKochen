from flask import render_template, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from sqlalchemy.exc import SQLAlchemyError
from werkzeug import Response

from kilakochen import db
from kilakochen.models import User
from kilakochen.user import bp
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



@bp.route("/edit:<int:user_id>", methods=["GET", "POST"])
@login_required
def edit(user_id: int) -> Response | str | tuple[str, int]:
    if current_user.level < User.ADMIN_LEVEL and current_user.id != user_id:
        flash("Keine Berechtigung zum Bearbeiten dieses Benutzers.", "danger")
        return redirect(url_for("user.overview"))

    user = User.query.filter_by(id=user_id).first()
    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        form.populate_obj(user)
        if form.password.data:
            user.set_password(form.password.data)
        try:
            db.session.commit()
            flash(f"Benutzer {user.username} wurde aktualisiert.", "success")
        except SQLAlchemyError as e:
            db.session.rollback()
            flash("Fehler beim Aktualisieren des Benutzers.", "danger")
        return redirect(url_for("user.overview"))

    return render_template("user/edit.html", form=form)


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
                    flash(f"Benutzer {user.username} wurde aktiviert!", "success")
                else:
                    flash(f"Benutzer {user.username} wurde deaktiviert!", "danger")
            except SQLAlchemyError as e:
                current_app.logger.error(f"Fehler beim Deaktivieren des Benutzers: {e}")
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
            if current_user.level >= int(form.level.data):
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
                        flash(f"Benutzer erfolgreich angelegt ({username})", category="success")

                    else:
                        flash(
                            f"Benutzername ist nicht eindeutig. Benutzer wurde nicht angelegt (Benutzername={username})",
                            category="danger")
                        return render_template("user/new.html", form=form)
                except Exception as e:
                    db.session.rollback()
                    flash(f"Fehler beim Erstellen des Benutzer: {str(e)}", category="warning")
                return redirect(url_for("user.overview"))
        else:
            return render_template("user/new.html", form=form)
    else:
        return render_template("errors/401.html"), 401
