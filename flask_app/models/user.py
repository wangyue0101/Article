from datetime import datetime

from flask_app.libs.db import db


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    article = db.relationship("Article", backref="user", lazy="dynamic")


class Article(db.Model):
    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DATETIME, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DATETIME, default=datetime.utcnow)
    content = db.Column(db.TEXT(255), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    comment = db.relationship("Comments", backref=db.backref("article"), lazy="dynamic")


class Comments(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    comment = db.Column(db.TEXT(255), nullable=False)
    created_at = db.Column(db.DATETIME, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DATETIME, default=datetime.utcnow)

    article_id = db.Column(db.Integer, db.ForeignKey("articles.id"))