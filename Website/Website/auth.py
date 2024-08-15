#auth.py
from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
# consider password hash
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password1")

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Logged in sucessfully', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
        else:
            flash('Account does not exist', category='error')

    return render_template("login.html", user = current_user)

@auth.route("/sign-up", methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        existing_email = User.query.filter_by(email=email).first()
        existing_user = User.query.filter_by(username=username).first()
        if existing_email:
            flash('The email already exists', category='error')
        elif existing_user:
            flash('The username is already taken', category='error')
        elif password1 != password2:
            flash('Please type your password correctly', category='error')
        elif len(username) < 2:
            flash('Username must be more than 2 characters', category='error')
        elif len(password1) < 4:
            flash('Password must be more than 4 digits', category='error')
        else:
            new_user = User(email=email, username=username, password = password1)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember='True')
            flash('Account Created')
            return redirect(url_for("views.home"))
        
    return render_template("signup.html", user = current_user)


        


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logged out sucessfully', category='success')
    return redirect(url_for("views.home"))