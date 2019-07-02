from .user import User, Article
from flask_app.libs.db import db


__all__ = [
    "User",
    "Article"
]


def create_tables(app):
    db.create_all(app=app)


def drop_tables(app):
    db.drop_all(app=app)
