from flask import render_template, flash, redirect, url_for, g, session, make_response

from flask_app.models.user import User, Article
from flask_app.libs.db import db
from flask_app.utils.get_datetime import get_midnight_today_to_utc
from flask_app.utils.auth import md5_key
from . import user_blue_api
from ..form_validata import UserRegisterForm, AddArticleForm, UserLoginForm

LOCAL_TIME = get_midnight_today_to_utc()


@user_blue_api.route("/register_user", methods=['GET', 'POST'])
def register_user():
    form = UserRegisterForm()

    if form.validate_on_submit():
        pwd_to_md5 = md5_key(form.password.data)
        user = User(
            name=form.username.data, email=form.email.data,
            password=pwd_to_md5
        )
        try:
            db.session.add(user)
            db.session.commit()
        except:
            db.session.rollback()
            flash("注册失败")
        else:
            flash("注册成功")
            return redirect(url_for(".login"))

    return render_template("user_register.html", title="注册", form=form)


@user_blue_api.route("/login", methods=['GET', 'POST'])
def login():
    form = UserLoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        try:
            user = User.query.filter_by(name=username).first()
        except:
            flash("数据库查询失败")
            return render_template("login.html", form=form)

        if not user:
            flash("用户不存在，请注册")
            return render_template("login.html", form=form)

        md5_pass = md5_key(password)

        if md5_pass != user.password:
            flash("用户密码不正确，请重新输入")
            return render_template("login.html", form=form)

        flash("登录成功")
        session["user"] = user
        g.user = user
        response = make_response(render_template("index.html"))
        response.set_cookie("username", user.name, max_age=30)
        return response

    return render_template("login.html", form=form)


@user_blue_api.route("/login_out")
def login_out():
    session.pop("user", None)
    return redirect(url_for("index"))


@user_blue_api.route("/add_article", methods=['GET', 'POST'])
def add_article():
    form = AddArticleForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        if not user:
            flash("用户未注册，请注册再添加文章")
            return redirect(url_for(".register_user"))

        article = Article(
            title=form.title.data, content=form.content.data,
            created_at=LOCAL_TIME, updated_at=LOCAL_TIME,
            user=user
        )
        try:
            db.session.add(article)
            db.session.commit()
        except:
            db.session.rollback()
            flash("添加失败")
        else:
            flash("添加成功")
    return render_template("add_article.html", form=form)


@user_blue_api.route("/get_user_list")
def get_user_list():
    users = db.session.query(User).all()
    return render_template("users.html", users=users)


@user_blue_api.route("/delete_user/<user_id>")
def delete_user(user_id):
    user = User.query.get(user_id)

    if user:
        try:
            Article.query.filter_by(author_id=user_id).delete()
            db.session.delete(user)
            db.session.commit()
        except:
            db.session.rollback()
            flash("删除失败")
        else:
            flash("删除成功")
            if session.get("user"):
                if session["user"].id == user.id:
                    session.pop("user")

    return render_template("index.html")
