#models.py
from . import db
from sqlalchemy.sql import func

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.Text, nullable = False)
    date_created = db.Column(db.DateTime(timezone = True), default = func.now())
    author_name = db.Column(db.String(100))
    author_id = db.Column(db.Integer, nullable=False)
