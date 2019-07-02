import os
import random

from flask import current_app
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
import forgery_py

from flask_app import create_app
from flask_app.models import create_tables, drop_tables
from flask_app.libs.db import db
from flask_app.models.user import User, Article, Comments

env_config = os.getenv('FLASK_CONFIG', "development")

app = create_app(env_config)

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command("runserver", Server(use_debugger=True))
manager.add_command("db", MigrateCommand)


@app.cli.command("make")
def make_db():
    create_tables(app)


@app.cli.command("drop")
def drop_db_table():
    drop_tables(app)


@app.cli.command("config")
def get_config():
    print(current_app.config)

@app.cli.command("forger_data")
def forger_data():

    def generate_user():
        return User(
            name=forgery_py.internet.user_name(),
            password=forgery_py.basic.password(),
            email=forgery_py.internet.email_address()
        )

    def generate_article(func_author):
        return Article(
            title=forgery_py.lorem_ipsum.title(),
            content=forgery_py.lorem_ipsum.words(),
            user=func_author()
        )

    def generate_comments(func_article):
        return Comments(
            title=forgery_py.lorem_ipsum.title(),
            comment=forgery_py.lorem_ipsum.words(),
            article=func_article()
        )

    users = [generate_user() for i in range(5)]
    db.session.add_all(users)

    random_user = lambda: users[random.randint(0, 4)]

    articles = [generate_article(random_user) for i in range(0, 50)]
    db.session.add_all(articles)

    random_article = lambda: articles[random.randint(0, len(articles)-1)]

    comments = [generate_comments(random_article) for i in range(30)]
    db.session.add_all(comments)

    try:
        db.session.commit()
    except:
        print("数据存储失败")
        db.session.rollback()

@app.cli.command("test")
def test():
    import unittest
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == '__main__':
    manager.run()
