from flask_sqlalchemy import SQLAlchemy
import hashlib
import jwt
import datetime
from db import db


class User(db.Model):
    rowid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __repr__(self):
        return '<User %r>' % self.username

    @staticmethod
    def hash_password(password):
        return hashlib.md5(password.encode('utf-8')).hexdigest()

    @staticmethod
    def create_user(username, password, **kwargs):
        user = User(username=username, password=User.hash_password(password), **kwargs)
        db.session.add(user)
        db.session.commit()

    @staticmethod
    def get_user(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def from_token(token):
        try:
            payload = jwt.decode(token, db.app.config.get('SECRET_KEY'))
            return User.get_user(payload['sub'])
        except:
            return None

    @staticmethod
    def authenticate_user(username, password):
        user = User.get_user(username)
        if user and user.password == User.hash_password(password):
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': user.username
            }
            return jwt.encode(
                payload,
                db.app.config.get('SECRET_KEY'),
                algorithm='HS256'
            ).decode()
        return None

    @staticmethod
    def delete_user(username):
        db.session.delete(User.get_user(username))
        db.session.commit()

    def change_password(self, password):
        self.password = User.hash_password(password)
        db.session.commit()
