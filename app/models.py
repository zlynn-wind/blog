from datetime import datetime
from flask import current_app
from flask_login import UserMixin, unicode
from flask_sqlalchemy import BaseQuery
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash

from app.init import db,login_manager


class Permission:
    USER = 0
    ADMIN = 1

class BaseModel(db.Model):

    __abstract__ = True

    @classmethod
    def create(cls, _commit=True, **kwargs):
        obj = cls(**kwargs)
        obj.save(_commit)
        return obj

    @classmethod
    def get(cls, id_):
        query = cls.query
        return query.filter_by(id=id_).first()

    def delete(self, _hard=False, _commit=True):
        if hasattr(self, "deleted_at") and _hard is False:
            self.deleted_at = datetime.utcnow()
            db.session.add(self)
        else:
            db.session.delete(self)
        if _commit:
            db.session.commit()


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    user_permisson = db.Column(db.String(64))

    def __init__(self, id=None,
                 username=None, password_hash=None,
                 user_permisson=None):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.user_permisson = user_permisson
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def get_user_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def get_user_by_username(cls,username):
        return cls.query.filter_by(username=username).first()

    def checkout_username(cls, username):
        user = cls.query.filter_by(username=username).first()
        if user is None:
            return True

    def update_password(cls, new_password):
        cls.password_hash = generate_password_hash(new_password)
        db.session.add(cls)
        db.commit()


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @classmethod
    def create(cls, username=None,
               password=None, user_permisson=None,
               _commit=True):
        obj = cls(
            username=username,
            password_hash=generate_password_hash(password),
            user_permisson=user_permisson,
        )
        db.session.add(obj)
        if _commit is True:
            db.session.commit()
        return obj


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id}).decode('utf-8')

    @staticmethod
    def update_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password_hash = generate_password_hash(new_password)
        db.session.add(user)
        return True


class Post(db.Model):
    __tablename__ = 'Post'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    text = db.Column(db.Text)

    def __init__(self, id=None,
                 user_id=None, text=None):
        self.id = id
        self.user_id = user_id
        self.text = text


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64))
    text = db.Column(db.Text)

    def __init__(self, id=None,
                 nickname=None, text=None):
        self.id = id
        self.nickname = nickname
        self.text = text
