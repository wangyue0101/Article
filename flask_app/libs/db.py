from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def patch_with_dialects(db_obj):
    import sqlalchemy.dialects
    from sqlalchemy.dialects import mysql  # noqa

    db_obj.dialects = sqlalchemy.dialects


def patch_sql(db):
    patch_with_dialects(db)


patch_sql(db)