"""
Freelancer Routes (CRUD API)
"""
import os
from flask import Blueprint, request, jsonify, current_app
from marshmallow import ValidationError
from app.services import FreelancerService, FreelancerDocumentService
from app.schemas import (
    FreelancerSchema,
    FreelancerCreateSchema,
    FreelancerUpdateSchema,
    SkillSchema,
)
from app.utils import handle_success, handle_error

# Blueprint 생성
bp = Blueprint('freelancer', __name__, url_prefix='/api/freelancers')

# Schema 인스턴스
freelancer_schema = FreelancerSchema()
freelancers_schema = FreelancerSchema(many=True)
freelancer_create_schema = FreelancerCreateSchema()
freelancer_update_schema = FreelancerUpdateSchema(partial=True)
skill_schema = SkillSchema()
skills_schema = SkillSchema(many=True)


@bp.route('', methods=['GET'])
def list_freelancers():
    """프리랜서 목록 조회"""
    try:
        # 쿼리 파라미터 추출
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        search = request.args.get('search')
        availability = request.args.get('availability')
        min_rating = request.args.get('minRating', type=float)
        min_experience = request.args.get('minExperience', type=int)
        max_hourly_rate = request.args.get('maxHourlyRate', type=int)
        sort_by = request.args.get('sortBy', 'name')
        sort_order = request.args.get('sortOrder', 'asc')

        # 스킬 필터 (배열로 올 수 있음)
        skills = request.args.getlist('skills')

        # 유효성 검사
        if page < 1:
            page = 1
        if limit < 1 or limit > 100:
            limit = 20

        # 서비스 호출
        result = FreelancerService.get_list(
            page=page,
            limit=limit,
            search=search,
            skills=skills,
            availability=availability,
            min_rating=min_rating,
            min_experience=min_experience,
            max_hourly_rate=max_hourly_rate,
            sort_by=sort_by,
            sort_order=sort_order
        )

        return handle_success(result, '프리랜서 목록 조회 성공', 200)

    except Exception as e:
        return handle_error(str(e), 400)


@bp.route('/<freelancer_id>', methods=['GET'])
def get_freelancer(freelancer_id):
    """프리랜서 상세 조회"""
    try:
        freelancer = FreelancerService.get_by_id(freelancer_id)
        return handle_success(freelancer, '프리랜서 조회 성공', 200)

    except ValueError as e:
        return handle_error(str(e), 404)
    except Exception as e:
        return handle_error(str(e), 400)


@bp.route('', methods=['POST'])
def create_freelancer():
    """프리랜서 생성"""
    try:
        # 요청 데이터 유효성 검사
        data = freelancer_create_schema.load(request.get_json())

        # 서비스 호출
        freelancer = FreelancerService.create(data)

        return handle_success(freelancer, '프리랜서 등록 성공', 201)

    except ValidationError as e:
        return handle_error('유효하지 않은 데이터입니다', 400, e.messages)
    except ValueError as e:
        return handle_error(str(e), 400)
    except Exception as e:
        return handle_error(f'서버 오류: {str(e)}', 500)


@bp.route('/<freelancer_id>', methods=['PUT'])
def update_freelancer(freelancer_id):
    """프리랜서 정보 수정"""
    try:
        # 요청 데이터 유효성 검사
        data = freelancer_update_schema.load(request.get_json())

        # 서비스 호출
        freelancer = FreelancerService.update(freelancer_id, data)

        return handle_success(freelancer, '프리랜서 정보 수정 성공', 200)

    except ValidationError as e:
        return handle_error('유효하지 않은 데이터입니다', 400, e.messages)
    except ValueError as e:
        return handle_error(str(e), 404 if '찾을 수 없습니다' in str(e) else 400)
    except Exception as e:
        return handle_error(f'서버 오류: {str(e)}', 500)


@bp.route('/<freelancer_id>', methods=['DELETE'])
def delete_freelancer(freelancer_id):
    """프리랜서 삭제"""
    try:
        FreelancerService.delete(freelancer_id)
        return handle_success(None, '프리랜서 삭제 성공', 200)

    except ValueError as e:
        return handle_error(str(e), 404)
    except Exception as e:
        return handle_error(f'서버 오류: {str(e)}', 500)


@bp.route('/skills', methods=['GET'])
def get_skills():
    """전체 스킬 목록 조회"""
    try:
        skills = FreelancerService.get_skills()
        return handle_success(skills, '스킬 목록 조회 성공', 200)

    except Exception as e:
        return handle_error(str(e), 400)


# ==================== Document Upload Routes ====================

@bp.route('/<freelancer_id>/documents', methods=['POST'])
def upload_document(freelancer_id):
    """프리랜서 문서 업로드 및 분석"""
    try:
        # 파일 확인
        if 'file' not in request.files:
            return handle_error('파일이 없습니다', 400)

        file = request.files['file']
        document_type = request.form.get('documentType', 'other')

        if not document_type:
            return handle_error('문서 타입은 필수입니다', 400)

        # 업로드 디렉토리 생성
        upload_dir = os.path.join(
            current_app.config['UPLOAD_FOLDER'],
            'freelancer',
            freelancer_id
        )

        # 문서 업로드 및 분석
        result = FreelancerDocumentService.upload_document(
            freelancer_id=freelancer_id,
            file=file,
            document_type=document_type,
            upload_dir=upload_dir
        )

        return handle_success(result, '문서 업로드 및 분석 완료', 201)

    except ValueError as e:
        return handle_error(str(e), 400)
    except Exception as e:
        return handle_error(f'서버 오류: {str(e)}', 500)


@bp.route('/<freelancer_id>/documents', methods=['GET'])
def get_documents(freelancer_id):
    """프리랜서 문서 목록 조회"""
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        document_type = request.args.get('documentType', None)

        result = FreelancerDocumentService.get_documents(
            freelancer_id=freelancer_id,
            page=page,
            limit=limit,
            document_type=document_type
        )

        return handle_success(result, '문서 목록 조회 성공', 200)

    except Exception as e:
        return handle_error(f'서버 오류: {str(e)}', 500)


@bp.route('/documents/<document_id>', methods=['GET'])
def get_document(document_id):
    """문서 상세 조회"""
    try:
        result = FreelancerDocumentService.get_document(document_id)
        return handle_success(result, '문서 조회 성공', 200)

    except ValueError as e:
        return handle_error(str(e), 404)
    except Exception as e:
        return handle_error(f'서버 오류: {str(e)}', 500)


@bp.route('/documents/<document_id>', methods=['DELETE'])
def delete_document(document_id):
    """문서 삭제"""
    try:
        FreelancerDocumentService.delete_document(document_id)
        return handle_success(None, '문서 삭제 성공', 204)

    except ValueError as e:
        return handle_error(str(e), 404)
    except Exception as e:
        return handle_error(f'서버 오류: {str(e)}', 500)


@bp.route('/documents/<document_id>/re-analyze', methods=['POST'])
def re_analyze_document(document_id):
    """문서 재분석"""
    try:
        result = FreelancerDocumentService.re_analyze_document(document_id)
        return handle_success(result, '문서 재분석 완료', 200)

    except ValueError as e:
        return handle_error(str(e), 404)
    except Exception as e:
        return handle_error(f'서버 오류: {str(e)}', 500)


# Health check endpoint
@bp.route('/health', methods=['GET'])
def health():
    """헬스 체크"""
    return jsonify({'status': 'ok', 'message': 'Freelancer API is running'}), 200
