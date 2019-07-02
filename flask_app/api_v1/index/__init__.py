from flask import Blueprint


index_blue_api = Blueprint("index_blue_api", __name__)


from . import views     # noqa
