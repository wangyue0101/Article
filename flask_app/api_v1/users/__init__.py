from flask import Blueprint

user_blue_api = Blueprint("user_blue_api", __name__)

from . import views    # noqa
