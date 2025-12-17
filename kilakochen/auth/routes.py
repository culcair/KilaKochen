from datetime import datetime, timezone
from urllib.parse import urlsplit

from kilakochen import db
from kilakochen.auth import bp
from flask import flash, redirect, render_template, url_for, request
from flask_login import current_user, login_user, logout_user

from kilakochen.auth.forms import LoginForm
from kilakochen.models import User


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("overview"))

    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data) or not user.active:
            flash("Falscher Benutzername oder falsches Passwort", category="danger")
            return redirect(url_for("auth.login"))

        login_user(user, remember=form.remember_me.data)
        flash("Login erfolgreich.", category="success")
        user.last_seen = datetime.now(timezone.utc)
        db.session.commit()
        next_page = request.args.get("next","")
        next_page = next_page.replace("\\","")
        parsed_url = urlsplit(next_page)
        if (
            not next_page or
            parsed_url.netloc or
            parsed_url.scheme or
            not next_page.startswith("/") or
            next_page.startswith("//")
        ):
            next_page = url_for("main.index")

        return redirect(next_page)

    return render_template("login.html", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    flash("Logout erfolgreich.", category="success")
    return redirect(url_for("main.index"))
