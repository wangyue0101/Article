from flask import Blueprint

article_blue_api = Blueprint("article_blue_api", __name__)


from . import views  # noqa