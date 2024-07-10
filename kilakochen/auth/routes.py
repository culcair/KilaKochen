from kilakochen.auth import bp    
from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user

from kilakochen.auth.forms import LoginForm
from kilakochen.models import User

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('overview'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Falscher Benutzername oder falsches Passwort")
            return redirect(url_for('auth.login'))
            
        login_user(user, remember=form.remember_me.data)
        print(current_user)
        flash('Logged in successfully.')

        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))