"""
Flask Application Factory
"""
from flask import Flask
from flask_cors import CORS
from config import get_config
from app.db import db, init_db
from app.models import freelancer


def create_app():
    """애플리케이션 팩토리"""
    # Flask 앱 생성
    app = Flask(__name__)

    # 설정 로드
    config = get_config()
    app.config.from_object(config)

    # 데이터베이스 초기화
    db.init_app(app)

    # CORS 설정
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config.get('CORS_ORIGINS', '*').split(','),
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })

    # 라우트 등록
    register_routes(app)

    # 에러 핸들러
    register_error_handlers(app)

    # 데이터베이스 초기화 (실패해도 앱은 시작됨)
    with app.app_context():
        try:
            db.create_all()
            print('✅ 데이터베이스 테이블 생성/확인 완료')
        except Exception as e:
            print(f'⚠️  데이터베이스 연결 실패: {str(e)}')
            print('📝 setup.py를 실행하거나 데이터베이스 서버를 확인하세요')

    return app


def register_routes(app):
    """라우트 등록"""
    from app.routes import freelancer_routes, interview_routes

    app.register_blueprint(freelancer_routes.bp)
    app.register_blueprint(interview_routes.bp)


def register_error_handlers(app):
    """에러 핸들러 등록"""
    from app.utils import handle_error

    @app.errorhandler(400)
    def bad_request(error):
        return handle_error('잘못된 요청입니다', 400), 400

    @app.errorhandler(404)
    def not_found(error):
        return handle_error('요청한 리소스를 찾을 수 없습니다', 404), 404

    @app.errorhandler(500)
    def internal_error(error):
        return handle_error('서버 오류가 발생했습니다', 500), 500
