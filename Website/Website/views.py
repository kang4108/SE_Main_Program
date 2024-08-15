#views.py
from flask import Blueprint, render_template, flash, request, redirect, url_for, jsonify
from flask_login import current_user, login_required
from .models import Post, User
from . import db
import requests
from datetime import datetime

views = Blueprint('views', __name__)

MS_PN_URL = 'http://localhost:5002/notification'
MS_GR_URL = 'http://localhost:5003/greetAPI'

@views.route("/")
@views.route("/home")
def home():
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
    return render_template("home.html", user=current_user, posts=posts)

# post upload
@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():

    if request.method == "POST":
        text = request.form.get('text')

        if not text:
            flash('Text entry is empty', category='error')
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            # notification microservice
            notify_request(current_user.username, 'created')
            flash('Post created!', category='success')
            return redirect(url_for("views.home"))

    return render_template("create_post.html", user=current_user)

# post upload-2
@views.route("/create-post-2", methods=['GET', 'POST'])
@login_required
def create_post_2():

    if request.method == "POST":
        text = request.form.get('text')

        if not text:
            flash('Text entry is empty', category='error')
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            # notification microservice
            notify_request(current_user.username, 'created')
            flash('Post created!', category='success')
            return redirect(url_for("views.home"))

    return render_template("create_post.html", user=current_user)

# user post list
@views.route("/posts/<username>")
def posts(username):
    user = User.query.filter_by(username=username).first()
    posts = Post.query.filter_by(author=user.id).all()
    return render_template("user_posts.html", user=current_user, posts=posts, username=username)

# post delete
@views.route("/delete/<id>")
@login_required
def delete_post(id):
    post = Post.query.filter_by(id=id).first()
    db.session.delete(post)
    db.session.commit()
    # notification microservice
    notify_request(current_user.username, 'deleted')
    flash('Post deleted.', category='success')
    return redirect(url_for('views.home'))

def notify_request(user, action):
    try:
        response = requests.post(MS_PN_URL, json={'user': user, 'action': action})
        if response.status_code != 200:
            flash('Notification failed', category='error')
    except Exception as e:
        flash(f'Notification failed: {e}', category='error')

