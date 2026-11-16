from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def commit_or_rollback():

    try:
        db.session.commit()

    except Exception:
        db.session.rollback()
        raise