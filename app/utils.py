"""
Utility functions
"""
from flask import jsonify
from datetime import datetime


def handle_success(data=None, message='성공', status_code=200):
    """성공 응답"""
    response = {
        'success': True,
        'message': message,
    }
    if data is not None:
        response['data'] = data
    return jsonify(response), status_code


def handle_error(message='오류가 발생했습니다', status_code=400, errors=None):
    """에러 응답"""
    response = {
        'success': False,
        'message': message,
    }
    if errors:
        response['errors'] = errors
    return jsonify(response), status_code


def serialize_datetime(dt):
    """datetime을 ISO format 문자열로 변환"""
    if isinstance(dt, datetime):
        return dt.isoformat()
    return dt


def paginate(query, page=1, limit=20):
    """쿼리 결과를 페이지네이션"""
    paginated = query.paginate(page=page, per_page=limit, error_out=False)
    return {
        'data': [item for item in paginated.items],
        'total': paginated.total,
        'page': page,
        'limit': limit,
        'totalPages': paginated.pages
    }
