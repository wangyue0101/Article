import os
import redis


class BaseConfig:
    SECRET_KEY = '1230'
    CSRF_ENABLED = True

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://aiohttp:lyaiohttp.@192.168.0.108:3306/python?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_ECHO = True

    SESSION_TYPE = "redis"
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.StrictRedis(host="192.168.0.108", port=6379)
    SESSION_KEY_PREFIX = "flask_pro:session:"
    PERMANENT_SESSION_LIFETIME = 3000

    flask_app_name = os.environ.get("FLASK_APP")


class DevelopmentConfig(BaseConfig):
    ENV = "development"
    DEBUG = True
    SECRET_KEY = "dev_secret_key"


class TestingConfig(BaseConfig):
    ENV = "testing"
    TESTING = True


class ProductionConfig(BaseConfig):
    ENV = "production"

    SECRET_KEY = os.urandom(24)


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}