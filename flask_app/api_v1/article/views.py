from flask import render_template, redirect, url_for, flash, session, request

from flask_app.models.user import User, Article, Comments
from flask_app.libs.db import db
from . import article_blue_api
from flask_app.api_v1.form_validata import ArticleComments


@article_blue_api.route("/get_user_article/<user_id>")
def get_user_article(user_id):
    if user_id:
        user = db.session.query(User).get(user_id)
        user_article = user.article.all()

        if user_article:
            article = user_article
        else:
            article = []

        return render_template("user_article.html", article=article)


@article_blue_api.route("/get_article_list")
def get_article_list():
    page = request.args.get("page", 1)
    pagination = Article.query.order_by(Article.created_at.desc()).paginate(page=int(page), per_page=10, error_out=False)
    article_content = pagination.items
    return render_template("article_list.html", pagination=pagination, article_content=article_content)


@article_blue_api.route("/delete_article/<article_id>")
def delete_article(article_id):
    article = Article.query.get(article_id)

    if not article_id:
        flash("参数错误，没有这篇文章")
        return redirect(url_for("index"))

    try:
        db.session.delete(article)
        db.session.commit()
    except:
        flash("删除失败")
        db.session.rollback()
    else:
        flash("文章删除成功")

    return render_template("index.html")


@article_blue_api.route("/posts/<article_id>", methods=['GET', 'POST'])
def posts(article_id):
    article = Article.query.get(article_id)
    if request.method == 'POST':
        user = session.get("user", None)
        if not user:
            flash("未登录用户无法评论")
            return redirect(url_for("index"))

        if not article:
            flash("文章未找到")
            return redirect(url_for("index"))

        comment = Comments(
            title=request.form.get("title"),
            comment=request.form.get("comment"),
            article=article
        )

        try:
            db.session.add(comment)
            db.session.commit()
        except:
            flash("数据提交失败")
            db.session.rollback()
        else:
            flash("评论提交成功")
            return redirect(url_for(".get_article_list"))

    return render_template("comments.html", article=article)


@article_blue_api.route("/update_article/<article_id>", methods=['GET', 'POST'])
def update_article(article_id):
    article = Article.query.get(article_id)
    if request.method == 'POST':
        if not article:
            flash("文章未找到")
            return redirect(url_for("index"))

        content = request.form.get("content")

        if not content:
            flash("参数错误")
            return redirect(url_for("index"))

        article.content = content
        try:
            db.session.add(article)
            db.session.commit()
        except:
            flash("内容保存出错")
            return redirect(url_for("index"))
        else:
            flash("保存成功")
            return redirect(url_for(".get_article_list"))

    return render_template("update_article_content.html", article=article.title)


@article_blue_api.route("/search")
def search():
    article = Article.query.get(16)
    print(article.comment.all())
    return "None"