"""
Flask Configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    # Database - SQLite (로컬) 또는 MySQL (원격)
    db_type = os.getenv('DB_TYPE', 'sqlite')

    if db_type == 'mysql':
        # MySQL 연결 설정
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
            f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        )
    else:
        # SQLite 연결 설정 (기본값)
        db_name = os.getenv('DB_NAME', 'supermanager')
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_name}.db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True  # SQL 로그 출력

    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    JSON_SORT_KEYS = False

    # API
    JSON_AS_ASCII = False  # 한글 지원
    JSONIFY_PRETTYPRINT_REGULAR = True

    # File Upload
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'xlsx', 'md'}


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


# Configuration 선택
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """환경에 따른 설정 반환"""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])
