from flask import Blueprint, render_template, flash, request, redirect, url_for
from flask_login import current_user, login_required
from .models import Post, User
from . import db
import requests

views = Blueprint('views', __name__)

url = 'http://localhost:5000/notify'

@views.route("/")
@views.route("/home")
def home():
    posts = Post.query.all()
    return render_template("home.html", user = current_user, posts = posts)

# post upload
@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get('text')

        if not text:
            flash('Text entry is empty', category='error')
        else:
            post = Post(text = text, author = current_user.id)
            db.session.add(post)
            db.session.commit()
            # notification
            flash('Post created!', category='success')
            return redirect(url_for("views.home"))

    return render_template("create_post.html", user = current_user)

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
     # notification
     flash('Post deleted.', category='success')
     return redirect(url_for('views.home'))