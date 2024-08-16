#auth.py
from flask import Blueprint, render_template, redirect, url_for, request, flash, make_response
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    create_access_token,
    set_access_cookies,
    unset_jwt_cookies,
)
import requests
# consider password hash
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint('auth', __name__)

AUTH_SERVICE_URL = "http://127.0.0.1:5009"

@auth.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        response = requests.post(
            f"{AUTH_SERVICE_URL}/login",
            json={"username": username, "password": password},
        )
        if response.status_code == 200:
            token = response.json().get("access_token")
            resp = make_response(redirect(url_for("views.home")))
            set_access_cookies(resp, token)
            return resp
        else:
            flash("Invalid username or password", category="error")
            return redirect(url_for("auth.login"))

    return render_template("login.html")


@auth.route("/sign-up", methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if password1 != password2:
            flash('Please type your password correctly', category='error')
        elif len(username) < 2:
            flash('Username must be more than 2 characters', category='error')
        elif len(password1) < 4:
            flash('Password must be more than 4 digits', category='error')
        else:
            response = requests.post(
                f"{AUTH_SERVICE_URL}/register",
                json={
                    "username": username,
                    "email": email,
                    "password": password1,
                },
            )
            if response.status_code == 201:
                flash("Congratulations, you are now a registered user!", category="success")
                return redirect(url_for("views.home"))
            else:
                flash("Error registering user.", category="error")
                return redirect(url_for("signup"))

    return render_template("signup.html")

@auth.route("/logout")
def logout():
    resp = make_response(redirect(url_for("views.home")))
    unset_jwt_cookies(resp)
    flash("Logout successful", category="success")
    return resp