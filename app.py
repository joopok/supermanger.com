"""
Flask Application Entry Point
"""
import os
from app import create_app

# 애플리케이션 생성
app = create_app()

if __name__ == '__main__':
    # Flask 앱 실행
    port = int(os.getenv('API_PORT', 8000))
    host = os.getenv('API_HOST', '0.0.0.0')
    debug = os.getenv('FLASK_ENV') == 'development'

    print(f'🚀 Flask app starting on {host}:{port}')
    print(f'📊 Database: {os.getenv("DB_HOST")}:{os.getenv("DB_PORT")}/{os.getenv("DB_NAME")}')
    print(f'🌍 CORS Origins: {os.getenv("CORS_ORIGINS", "localhost")}')

    # use_reloader=False로 watchdog 호환성 문제 해결
    app.run(host=host, port=port, debug=debug, use_reloader=False)
