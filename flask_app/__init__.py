from config import config

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_nav.elements import Navbar, View
from flask_app.libs.redis import redis
from flask_app.libs.session import session

from flask_app.libs.db import db


def create_app(env_config):
    app = Flask(__name__)
    app.config.from_object(config[env_config])

    bootstrap = Bootstrap()
    nav = Nav()

    nav.register_element("navbar", Navbar("Falsk入门",
                                            View("首页", "index"),
                                            View("文章添加", "user_blue_api.add_article"),
                                            View("文章查看", "article_blue_api.get_article_list"),
                                            View("读者列表", "user_blue_api.get_user_list"),
                                            View("用户注册", "user_blue_api.register_user"),
                                            )
    )
    from flask_app.api_v1.index.views import init_views

    nav.init_app(app)
    db.init_app(app)
    bootstrap.init_app(app)
    init_views(app)
    register_route(app)
    session.init_app(app)

    return app


def register_route(app):
    from flask_app.api_v1.article import article_blue_api
    from flask_app.api_v1.users import user_blue_api

    app.register_blueprint(article_blue_api, url_prefix="/api/v1/article")
    app.register_blueprint(user_blue_api, url_prefix="/api/v1/user")


