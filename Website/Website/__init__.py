## __init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'helloworld'
    # initialize database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # initialize jwt
    app.config["JWT_SECRET_KEY"] = "secret_key"
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    JWTManager(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix = "/")
    app.register_blueprint(auth, url_prefix = "/")

    from .models import Post

    with app.app_context():
        db.create_all()

    return app
