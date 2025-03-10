from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['GET', 'POST'])
@auth.route("/login.html", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.homefeed'))
            else:
                flash('Password is incorrect.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html")


@auth.route("/signup", methods=['GET', 'POST'])
@auth.route("/signup.html", methods=['GET', 'POST'])

def sign_up():
    if request.method == 'POST':
        email = request.form.get("email")
        name = request.form.get("name")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_exists = User.query.filter_by(email=email).first()
        name_exists = User.query.filter_by(name=name).first()

        if email_exists:
            flash('Email is already in use.', category='error')
         
        elif password1 != password2:
            flash('Password don\'t match!', category='error')

        elif "iiti.ac.in" not in email:
            flash("Please sign up with institute id", category='error')
         
        else:
            new_user = User(email=email, name=name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Successfully signed up!')
            return redirect(url_for('views.homefeed'))

    return render_template("signup.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.homefeed"))


