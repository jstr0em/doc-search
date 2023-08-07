from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    documents = db.relationship('Document')

    def has_doc(self):
        return len(self.documents) < 1


class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    path = db.Column(db.String(250))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
