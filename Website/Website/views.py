#views.py
from flask import Blueprint, render_template, flash, request, redirect, url_for, jsonify
from .models import Post
from . import db
import requests
from datetime import datetime
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    create_access_token,
    set_access_cookies,
    unset_jwt_cookies,
    verify_jwt_in_request,
)

views = Blueprint('views', __name__)

MS_PN_URL = 'http://localhost:5002/notification'
MS_GR_URL = 'http://localhost:5003/greetAPI'

@views.route("/")
@views.route("/home")
@jwt_required(optional=True, locations=["cookies"])
def home():
    user = get_jwt_identity()
    '''response = requests.get(MS_GR_URL)
    greeting_response = response.json()'''
    try:
        response = requests.get(MS_GR_URL)
        if response.status_code != 200:
            flash('Notification failed', category='error')
        else:
            greeting_response = response.json() 
            flash(greeting_response, category='info')
    except Exception as e:
        flash(f'Notification failed: {e}', category='error')
    posts = Post.query.all()
    return render_template("home.html", user=user, posts=posts)

# post upload
@jwt_required(locations=["cookies"])
@views.route("/create-post", methods=['GET', 'POST'])
def create_post():
    verify_jwt_in_request()
    user = get_jwt_identity()
    if request.method == "POST":
        text = request.form.get('text')

        if not text:
            flash('Text entry is empty', category='error')
        else:
            post = Post(text=text, author_name=user["username"], author_id=user["id"])
            db.session.add(post)
            db.session.commit()
            # notification microservice
            notify_request(user["username"], 'created')
            flash('Post created!', category='success')
            return redirect(url_for("views.home"))

    return render_template("create_post.html", user=user)

# post upload-2
@jwt_required(locations=["cookies"])
@views.route("/create-post-2", methods=['GET', 'POST'])
def create_post_2():
    verify_jwt_in_request()
    user = get_jwt_identity()
    if request.method == "POST":
        text = request.form.get('text')

        if not text:
            flash('Text entry is empty', category='error')
        else:
            post = Post(text=text, author_name=user["username"], author_id=user["id"])
            db.session.add(post)
            db.session.commit()
            # notification microservice
            notify_request(user["username"], 'created')
            flash('Post created!', category='success')
            return redirect(url_for("views.home"))

    return render_template("create_post.html", user=user)

# user post list
@jwt_required(locations=["cookies"])
@views.route("/posts/<username>")
def posts(username):
    verify_jwt_in_request()
    user = get_jwt_identity()
    posts = Post.query.filter_by(author_id=user["id"]).all()
    return render_template("user_posts.html", user=user, posts=posts, username=username)

# post delete
@jwt_required(locations=["cookies"])
@views.route("/delete/<id>")
def delete_post(id):
    verify_jwt_in_request()
    user = get_jwt_identity()
    post = Post.query.filter_by(id=id).first()
    db.session.delete(post)
    db.session.commit()
    # notification microservice
    notify_request(user["username"], 'deleted')
    flash('Post deleted.', category='success')
    return redirect(url_for('views.home'))

@jwt_required(locations=["cookies"])
def notify_request(user, action):
    verify_jwt_in_request()
    try:
        response = requests.post(MS_PN_URL, json={'user': user, 'action': action})
        if response.status_code != 200:
            flash('Notification failed', category='error')
    except Exception as e:
        flash(f'Notification failed: {e}', category='error')

