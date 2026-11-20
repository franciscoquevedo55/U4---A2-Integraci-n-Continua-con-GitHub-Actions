from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import User
from . import auth
from .forms import LoginForm

@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("juegos"))

    form = LoginForm()

    if form.validate_on_submit():
        usuario = User.query.filter_by(username=form.username.data).first()

        if usuario and usuario.verify_password(form.password.data):
            login_user(usuario, remember=form.remember_me.data)
            return redirect(url_for("juegos"))

        flash("Usuario o contraseña incorrectos")

    return render_template("login.html", form=form)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Has cerrado sesión correctamente")
    return redirect(url_for("auth.login"))
