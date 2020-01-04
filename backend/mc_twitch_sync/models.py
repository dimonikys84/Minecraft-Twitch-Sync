# coding=utf-8
import functools
# import enum
import datetime
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()


def db_atomic(db_session):
    """
    Декоратор для автоматического коммита сессии после выполнения ф-ции
    :param db_session: sqlalchemy db session
    :return: function result
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                res = func(*args, **kwargs)
                db_session.commit()
                return res
            except Exception:
                db_session.rollback()
                raise
        return wrapper
    return decorator


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    twitch_nickname = db.Column(db.String(255), nullable=False, unique=True)
    twitch_id = db.Column(db.Integer, unique=True, nullable=True)
    is_member = db.Column(db.Boolean, default=False)
    expire_date = db.Column(db.Date, default=datetime.datetime.min)
    minecraft_nickname = db.Column(db.String(255), nullable=True)
    minecraft_uuid = db.Column(db.String(255), nullable=True)
    is_banned = db.Column(db.Boolean, default=False)
