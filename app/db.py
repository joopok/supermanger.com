"""
Database initialization and setup
"""
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy instance
db = SQLAlchemy()


def init_db(app):
    """데이터베이스 초기화"""
    db.init_app(app)
    with app.app_context():
        db.create_all()
