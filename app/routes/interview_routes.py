"""
Interview Evaluation API Routes
면접 평가 API 엔드포인트
"""
from flask import Blueprint, request
from app.services import (
    InterviewCategoryService, InterviewQuestionService,
    InterviewCheckpointService, InterviewRedFlagService,
    InterviewEvaluationService
)
from app.utils import handle_error, handle_success
import uuid

bp = Blueprint('interview', __name__, url_prefix='/api/interviews')


# ==================== Interview Category Endpoints ====================

@bp.route('/categories', methods=['GET'])
def get_categories():
    """면접 카테고리 목록 조회"""
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        search = request.args.get('search', None)
        sort_by = request.args.get('sortBy', 'order')
        sort_order = request.args.get('sortOrder', 'asc')

        result = InterviewCategoryService.get_list(
            page=page, limit=limit, search=search,
            sort_by=sort_by, sort_order=sort_order
        )
        return handle_success(result, '카테고리 목록 조회 성공', 200)
    except Exception as e:
        return handle_error(str(e), 400)


@bp.route('/categories/<category_id>', methods=['GET'])
def get_category(category_id):
    """카테고리 조회"""
    try:
        category = InterviewCategoryService.get_by_id(category_id)
        return handle_success(category.to_dict(), '카테고리 조회 성공', 200)
    except ValueError as e:
        return handle_error(str(e), 404)
    except Exception as e:
        return handle_error(str(e), 400)


@bp.route('/categories', methods=['POST'])
def create_category():
    """카테고리 생성"""
    try:
        data = request.get_json()
        if not data or 'name' not in data:
            return handle_error('카테고리 이름은 필수입니다', 400)

        category = InterviewCategoryService.create(
            name=data['name'],
            description=data.get('description'),
            weight=data.get('weight', 1),
            max_score=data.get('maxScore', 5.0),
            order=data.get('order', 0)
        )
        return handle_success(category.to_dict(), '카테고리 생성 성공', 201)
    except ValueError as e:
        return handle_error(str(e), 400)
    except Exception as e:
        return handle_error(str(e), 400)


@bp.route('/categories/<category_id>', methods=['PUT'])
def update_category(category_id):
    """카테고리 수정"""
    try:
        data = request.get_json()
        category = InterviewCategoryService.update(category_id, **data)
        return handle_success(category.to_dict(), '카테고리 수정 성공', 200)
    except ValueError as e:
        return handle_error(str(e), 404)
    except Exception as e:
        return handle_error(str(e), 400)


@bp.route('/categories/<category_id>', methods=['DELETE'])
def delete_category(category_id):
    """카테고리 삭제"""
    try:
        InterviewCategoryService.delete(category_id)
        return handle_success(None, '카테고리 삭제 성공', 204)
    except ValueError as e:
        return handle_error(str(e), 404)
    except Exception as e:
        return handle_error(str(e), 400)


# ==================== Interview Question Endpoints ====================

@bp.route('/categories/<category_id>/questions', methods=['GET'])
def get_questions(category_id):
    """카테고리별 질문 조회"""
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)

        result = InterviewQuestionService.get_by_category(category_id, page, limit)
        return handle_success(result, '질문 목록 조회 성공', 200)
    except ValueError as e:
        return handle_error(str(e), 404)
    except Exception as e:
        return handle_error(str(e), 400)


@bp.route('/questions', methods=['POST'])
def create_question():
    """질문 생성"""
    try:
        data = request.get_json()
        if not data or 'categoryId' not in data or 'questionText' not in data:
            return handle_error('카테고리 ID와 질문 텍스트는 필수입니다', 400)

        question = InterviewQuestionService.create(
            category_id=data['categoryId'],
            question_text=data['questionText'],
            order=data.get('order', 0)
        )
        return handle_success(question.to_dict(), '질문 생성 성공', 201)
    except ValueError as e:
        return handle_error(str(e), 400)
    except Exception as e:
        return handle_error(str(e), 400)


@bp.route('/questions/<question_id>', methods=['PUT'])
def update_question(question_id):
    """질문 수정"""
    try:
        data = request.get_json()
        question = InterviewQuestionService.update(question_id, **data)
        return handle_success(question.to_dict(), '질문 수정 성공', 200)
    except ValueError as e:
        return handle_error(str(e), 404)
    except Exception as e:
        return handle_error(str(e), 400)


@bp.route('/questions/<question_id>', methods=['DELETE'])
def delete_question(question_id):
    """질문 삭제"""
    try:
        InterviewQuestionService.delete(question_id)
        return handle_success(None, '질문 삭제 성공', 204)
    except ValueError as e:
        return handle_error(str(e), 404)
    except Exception as e:
        return handle_error(str(e), 400)


# ==================== Interview Checkpoint Endpoints ====================

@bp.route('/categories/<category_id>/checkpoints', methods=['GET'])
def get_checkpoints(category_id):
    """카테고리별 체크포인트 조회"""
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)

        result = InterviewCheckpointService.get_by_category(category_id, page, limit)
        return handle_success(result, '체크포인트 목록 조회 성공', 200)
    except ValueError as e:
        return handle_error(str(e), 404)
    except Exception as e:
        return handle_error(str(e), 400)


@bp.route('/checkpoints', methods=['POST'])
def create_checkpoint():
    """체크포인트 생성"""
    try:
        data = request.get_json()
        if not data or 'categoryId' not in data or 'checkpointText' not in data:
            return handle_error('카테고리 ID와 체크포인트 텍스트는 필수입니다', 400)

        checkpoint = InterviewCheckpointService.create(
            category_id=data['categoryId'],
            checkpoint_text=data['checkpointText'],
            order=data.get('order', 0)
        )
        return handle_success(checkpoint.to_dict(), '체크포인트 생성 성공', 201)
    except ValueError as e:
        return handle_error(str(e), 400)
    except Exception as e:
        return handle_error(str(e), 400)


@bp.route('/checkpoints/<checkpoint_id>', methods=['PUT'])
def update_checkpoint(checkpoint_id):
    """체크포인트 수정"""
    try:
        data = request.get_json()
        checkpoint = InterviewCheckpointService.update(checkpoint_id, **data)
        return handle_success(checkpoint.to_dict(), '체크포인트 수정 성공', 200)
    except ValueError as e:
        return handle_error(str(e), 404)
    except Exception as e:
        return handle_error(str(e), 400)


@bp.route('/checkpoints/<checkpoint_id>', methods=['DELETE'])
def delete_checkpoint(checkpoint_id):
    """체크포인트 삭제"""
    try:
        InterviewCheckpointService.delete(checkpoint_id)
        return handle_success(None, '체크포인트 삭제 성공', 204)
    except ValueError as e:
        return handle_error(str(e), 404)
    except Exception as e:
        return handle_error(str(e), 400)


# ==================== Interview Red Flag Endpoints ====================

@bp.route('/categories/<category_id>/red-flags', methods=['GET'])
def get_red_flags(category_id):
    """카테고리별 레드플래그 조회"""
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)

        result = InterviewRedFlagService.get_by_category(category_id, page, limit)
        return handle_success(result, '레드플래그 목록 조회 성공', 200)
    except ValueError as e:
        return handle_error(str(e), 404)
    except Exception as e:
        return handle_error(str(e), 400)


@bp.route('/red-flags', methods=['POST'])
def create_red_flag():
    """레드플래그 생성"""
    try:
        data = request.get_json()
        if not data or 'categoryId' not in data or 'flagText' not in data:
            return handle_error('카테고리 ID와 레드플래그 텍스트는 필수입니다', 400)

        red_flag = InterviewRedFlagService.create(
            category_id=data['categoryId'],
            flag_text=data['flagText'],
            severity=data.get('severity', 'medium'),
            order=data.get('order', 0)
        )
        return handle_success(red_flag.to_dict(), '레드플래그 생성 성공', 201)
    except ValueError as e:
        return handle_error(str(e), 400)
    except Exception as e:
        return handle_error(str(e), 400)


@bp.route('/red-flags/<red_flag_id>', methods=['PUT'])
def update_red_flag(red_flag_id):
    """레드플래그 수정"""
    try:
        data = request.get_json()
        red_flag = InterviewRedFlagService.update(red_flag_id, **data)
        return handle_success(red_flag.to_dict(), '레드플래그 수정 성공', 200)
    except ValueError as e:
        return handle_error(str(e), 404)
    except Exception as e:
        return handle_error(str(e), 400)


@bp.route('/red-flags/<red_flag_id>', methods=['DELETE'])
def delete_red_flag(red_flag_id):
    """레드플래그 삭제"""
    try:
        InterviewRedFlagService.delete(red_flag_id)
        return handle_success(None, '레드플래그 삭제 성공', 204)
    except ValueError as e:
        return handle_error(str(e), 404)
    except Exception as e:
        return handle_error(str(e), 400)


# ==================== Interview Evaluation Endpoints ====================

@bp.route('/evaluations', methods=['GET'])
def get_evaluations():
    """평가 목록 조회"""
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        freelancer_id = request.args.get('freelancerId', None)
        recommendation = request.args.get('recommendation', None)
        min_score = request.args.get('minScore', None, type=float)
        sort_by = request.args.get('sortBy', 'evaluated_at')
        sort_order = request.args.get('sortOrder', 'desc')

        result = InterviewEvaluationService.get_list(
            page=page, limit=limit, freelancer_id=freelancer_id,
            recommendation=recommendation, min_score=min_score,
            sort_by=sort_by, sort_order=sort_order
        )
        return handle_success(result, '평가 목록 조회 성공', 200)
    except Exception as e:
        return handle_error(str(e), 400)


@bp.route('/evaluations/<evaluation_id>', methods=['GET'])
def get_evaluation(evaluation_id):
    """평가 조회"""
    try:
        evaluation = InterviewEvaluationService.get_by_id(evaluation_id)
        return handle_success(evaluation.to_dict(), '평가 조회 성공', 200)
    except ValueError as e:
        return handle_error(str(e), 404)
    except Exception as e:
        return handle_error(str(e), 400)


@bp.route('/evaluations', methods=['POST'])
def create_evaluation():
    """평가 생성"""
    try:
        data = request.get_json()
        if not data or 'freelancerId' not in data:
            return handle_error('프리랜서 ID는 필수입니다', 400)

        evaluation = InterviewEvaluationService.create(
            freelancer_id=data['freelancerId'],
            interviewer_name=data.get('interviewerName'),
            project_name=data.get('projectName'),
            evaluated_at=None,  # 현재 시간
            notes=data.get('notes')
        )
        return handle_success(evaluation.to_dict(), '평가 생성 성공', 201)
    except ValueError as e:
        return handle_error(str(e), 400)
    except Exception as e:
        return handle_error(str(e), 400)


@bp.route('/evaluations/<evaluation_id>', methods=['PUT'])
def update_evaluation(evaluation_id):
    """평가 수정"""
    try:
        data = request.get_json()
        evaluation = InterviewEvaluationService.update(evaluation_id, **data)
        return handle_success(evaluation.to_dict(), '평가 수정 성공', 200)
    except ValueError as e:
        return handle_error(str(e), 404)
    except Exception as e:
        return handle_error(str(e), 400)


@bp.route('/evaluations/<evaluation_id>', methods=['DELETE'])
def delete_evaluation(evaluation_id):
    """평가 삭제"""
    try:
        InterviewEvaluationService.delete(evaluation_id)
        return handle_success(None, '평가 삭제 성공', 204)
    except ValueError as e:
        return handle_error(str(e), 404)
    except Exception as e:
        return handle_error(str(e), 400)


# ==================== Category Score Endpoints ====================

@bp.route('/evaluations/<evaluation_id>/category-scores', methods=['POST'])
def add_category_score(evaluation_id):
    """카테고리 점수 추가"""
    try:
        data = request.get_json()
        if not data or 'categoryId' not in data or 'score' not in data:
            return handle_error('카테고리 ID와 점수는 필수입니다', 400)

        category_score = InterviewEvaluationService.add_category_score(
            evaluation_id=evaluation_id,
            category_id=data['categoryId'],
            score=float(data['score']),
            score_label=data.get('scoreLabel', ''),
            checked_count=data.get('checkedCount', 0)
        )
        return handle_success(category_score.to_dict(), '카테고리 점수 추가 성공', 201)
    except ValueError as e:
        return handle_error(str(e), 400)
    except Exception as e:
        return handle_error(str(e), 400)


@bp.route('/evaluations/<evaluation_id>/category-scores/<category_id>', methods=['PUT'])
def update_category_score(evaluation_id, category_id):
    """카테고리 점수 수정"""
    try:
        data = request.get_json()
        if not data or 'score' not in data:
            return handle_error('점수는 필수입니다', 400)

        category_score = InterviewEvaluationService.update_category_score(
            evaluation_id=evaluation_id,
            category_id=category_id,
            score=float(data['score']),
            score_label=data.get('scoreLabel', ''),
            checked_count=data.get('checkedCount', 0)
        )
        return handle_success(category_score.to_dict(), '카테고리 점수 수정 성공', 200)
    except ValueError as e:
        return handle_error(str(e), 400)
    except Exception as e:
        return handle_error(str(e), 400)


# ==================== Checkpoint Result Endpoints ====================

@bp.route('/evaluations/<evaluation_id>/checkpoint-results', methods=['POST'])
def add_checkpoint_result(evaluation_id):
    """체크포인트 결과 추가"""
    try:
        data = request.get_json()
        if not data or 'checkpointId' not in data:
            return handle_error('체크포인트 ID는 필수입니다', 400)

        result = InterviewEvaluationService.add_checkpoint_result(
            evaluation_id=evaluation_id,
            checkpoint_id=data['checkpointId'],
            is_checked=data.get('isChecked', False),
            notes=data.get('notes')
        )
        return handle_success(result.to_dict(), '체크포인트 결과 추가 성공', 201)
    except ValueError as e:
        return handle_error(str(e), 400)
    except Exception as e:
        return handle_error(str(e), 400)


@bp.route('/evaluations/<evaluation_id>/checkpoint-results/<checkpoint_id>', methods=['PUT'])
def update_checkpoint_result(evaluation_id, checkpoint_id):
    """체크포인트 결과 수정"""
    try:
        data = request.get_json()
        result = InterviewEvaluationService.update_checkpoint_result(
            evaluation_id=evaluation_id,
            checkpoint_id=checkpoint_id,
            is_checked=data.get('isChecked'),
            notes=data.get('notes')
        )
        return handle_success(result.to_dict(), '체크포인트 결과 수정 성공', 200)
    except ValueError as e:
        return handle_error(str(e), 400)
    except Exception as e:
        return handle_error(str(e), 400)


# ==================== Red Flag Finding Endpoints ====================

@bp.route('/evaluations/<evaluation_id>/red-flag-findings', methods=['POST'])
def add_red_flag_finding(evaluation_id):
    """레드플래그 발견 추가"""
    try:
        data = request.get_json()
        if not data or 'redFlagId' not in data:
            return handle_error('레드플래그 ID는 필수입니다', 400)

        finding = InterviewEvaluationService.add_red_flag_finding(
            evaluation_id=evaluation_id,
            red_flag_id=data['redFlagId'],
            is_found=data.get('isFound', False),
            severity_actual=data.get('severityActual'),
            evidence=data.get('evidence')
        )
        return handle_success(finding.to_dict(), '레드플래그 발견 추가 성공', 201)
    except ValueError as e:
        return handle_error(str(e), 400)
    except Exception as e:
        return handle_error(str(e), 400)


@bp.route('/evaluations/<evaluation_id>/red-flag-findings/<red_flag_id>', methods=['PUT'])
def update_red_flag_finding(evaluation_id, red_flag_id):
    """레드플래그 발견 수정"""
    try:
        data = request.get_json()
        finding = InterviewEvaluationService.update_red_flag_finding(
            evaluation_id=evaluation_id,
            red_flag_id=red_flag_id,
            is_found=data.get('isFound'),
            severity_actual=data.get('severityActual'),
            evidence=data.get('evidence')
        )
        return handle_success(finding.to_dict(), '레드플래그 발견 수정 성공', 200)
    except ValueError as e:
        return handle_error(str(e), 400)
    except Exception as e:
        return handle_error(str(e), 400)


# ==================== Score Calculation Endpoints ====================

@bp.route('/evaluations/<evaluation_id>/calculate-score', methods=['POST'])
def calculate_total_score(evaluation_id):
    """총점 계산 및 저장"""
    try:
        total_score = InterviewEvaluationService.calculate_total_score(evaluation_id)
        return handle_success(
            {'totalScore': total_score},
            '총점 계산 완료',
            200
        )
    except ValueError as e:
        return handle_error(str(e), 404)
    except Exception as e:
        return handle_error(str(e), 400)


@bp.route('/evaluations/<evaluation_id>/set-recommendation', methods=['POST'])
def set_recommendation(evaluation_id):
    """추천 여부 설정"""
    try:
        data = request.get_json()
        if not data or 'recommendation' not in data:
            return handle_error('추천 상태는 필수입니다', 400)

        evaluation = InterviewEvaluationService.set_recommendation(
            evaluation_id=evaluation_id,
            recommendation=data['recommendation'],
            notes=data.get('notes')
        )
        return handle_success(evaluation.to_dict(), '추천 상태 설정 완료', 200)
    except ValueError as e:
        return handle_error(str(e), 400)
    except Exception as e:
        return handle_error(str(e), 400)
