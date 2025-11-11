"""
Interview Evaluation Service - 면접 평가 비즈니스 로직
3NF 정규화된 구조로 신뢰성 있는 CRUD 작업 수행
"""
import uuid
from datetime import datetime
from app.db import db
from app.models import (
    InterviewEvaluation, InterviewCategory, InterviewQuestion,
    InterviewCheckpoint, InterviewRedFlag,
    InterviewCategoryScore, InterviewEvaluationResult, InterviewRedFlagFinding,
    Freelancer
)
from app.utils import paginate


class InterviewCategoryService:
    """면접 평가 카테고리 서비스 (마스터 데이터)"""

    @staticmethod
    def get_list(page=1, limit=20, search=None, sort_by='order', sort_order='asc'):
        """카테고리 목록 조회"""
        query = InterviewCategory.query

        if search:
            query = query.filter(
                db.or_(
                    InterviewCategory.name.ilike(f'%{search}%'),
                    InterviewCategory.description.ilike(f'%{search}%')
                )
            )

        # 정렬
        sort_column = getattr(InterviewCategory, sort_by, InterviewCategory.order)
        if sort_order.lower() == 'desc':
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column)

        return paginate(query, page, limit)

    @staticmethod
    def get_by_id(category_id):
        """카테고리 조회"""
        category = InterviewCategory.query.get(category_id)
        if not category:
            raise ValueError(f'카테고리를 찾을 수 없습니다: {category_id}')
        return category

    @staticmethod
    def create(name, description=None, weight=1, max_score=5.0, order=0):
        """카테고리 생성"""
        # 중복 확인
        existing = InterviewCategory.query.filter_by(name=name).first()
        if existing:
            raise ValueError(f'이미 존재하는 카테고리: {name}')

        category = InterviewCategory(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            weight=weight,
            max_score=max_score,
            order=order
        )
        db.session.add(category)
        db.session.commit()
        return category

    @staticmethod
    def update(category_id, **kwargs):
        """카테고리 수정"""
        category = InterviewCategoryService.get_by_id(category_id)

        # 이름 중복 확인
        if 'name' in kwargs and kwargs['name'] != category.name:
            existing = InterviewCategory.query.filter_by(name=kwargs['name']).first()
            if existing:
                raise ValueError(f'이미 존재하는 카테고리: {kwargs["name"]}')

        for key, value in kwargs.items():
            if hasattr(category, key) and value is not None:
                setattr(category, key, value)

        db.session.commit()
        return category

    @staticmethod
    def delete(category_id):
        """카테고리 삭제 (관련 데이터도 CASCADE)"""
        category = InterviewCategoryService.get_by_id(category_id)
        db.session.delete(category)
        db.session.commit()
        return True


class InterviewQuestionService:
    """면접 질문 서비스"""

    @staticmethod
    def get_by_category(category_id, page=1, limit=20):
        """카테고리별 질문 조회"""
        query = InterviewQuestion.query.filter_by(category_id=category_id).order_by(InterviewQuestion.order)
        return paginate(query, page, limit)

    @staticmethod
    def get_by_id(question_id):
        """질문 조회"""
        question = InterviewQuestion.query.get(question_id)
        if not question:
            raise ValueError(f'질문을 찾을 수 없습니다: {question_id}')
        return question

    @staticmethod
    def create(category_id, question_text, order=0):
        """질문 생성"""
        # 카테고리 존재 확인
        InterviewCategoryService.get_by_id(category_id)

        question = InterviewQuestion(
            id=str(uuid.uuid4()),
            category_id=category_id,
            question_text=question_text,
            order=order
        )
        db.session.add(question)
        db.session.commit()
        return question

    @staticmethod
    def update(question_id, **kwargs):
        """질문 수정"""
        question = InterviewQuestionService.get_by_id(question_id)

        for key, value in kwargs.items():
            if hasattr(question, key) and value is not None:
                setattr(question, key, value)

        db.session.commit()
        return question

    @staticmethod
    def delete(question_id):
        """질문 삭제"""
        question = InterviewQuestionService.get_by_id(question_id)
        db.session.delete(question)
        db.session.commit()
        return True


class InterviewCheckpointService:
    """면접 체크포인트 서비스"""

    @staticmethod
    def get_by_category(category_id, page=1, limit=20):
        """카테고리별 체크포인트 조회"""
        query = InterviewCheckpoint.query.filter_by(category_id=category_id).order_by(InterviewCheckpoint.order)
        return paginate(query, page, limit)

    @staticmethod
    def get_by_id(checkpoint_id):
        """체크포인트 조회"""
        checkpoint = InterviewCheckpoint.query.get(checkpoint_id)
        if not checkpoint:
            raise ValueError(f'체크포인트를 찾을 수 없습니다: {checkpoint_id}')
        return checkpoint

    @staticmethod
    def create(category_id, checkpoint_text, order=0):
        """체크포인트 생성"""
        # 카테고리 존재 확인
        InterviewCategoryService.get_by_id(category_id)

        checkpoint = InterviewCheckpoint(
            id=str(uuid.uuid4()),
            category_id=category_id,
            checkpoint_text=checkpoint_text,
            order=order
        )
        db.session.add(checkpoint)
        db.session.commit()
        return checkpoint

    @staticmethod
    def update(checkpoint_id, **kwargs):
        """체크포인트 수정"""
        checkpoint = InterviewCheckpointService.get_by_id(checkpoint_id)

        for key, value in kwargs.items():
            if hasattr(checkpoint, key) and value is not None:
                setattr(checkpoint, key, value)

        db.session.commit()
        return checkpoint

    @staticmethod
    def delete(checkpoint_id):
        """체크포인트 삭제"""
        checkpoint = InterviewCheckpointService.get_by_id(checkpoint_id)
        db.session.delete(checkpoint)
        db.session.commit()
        return True


class InterviewRedFlagService:
    """면접 레드플래그 서비스"""

    @staticmethod
    def get_by_category(category_id, page=1, limit=20):
        """카테고리별 레드플래그 조회"""
        query = InterviewRedFlag.query.filter_by(category_id=category_id).order_by(InterviewRedFlag.order)
        return paginate(query, page, limit)

    @staticmethod
    def get_by_id(red_flag_id):
        """레드플래그 조회"""
        red_flag = InterviewRedFlag.query.get(red_flag_id)
        if not red_flag:
            raise ValueError(f'레드플래그를 찾을 수 없습니다: {red_flag_id}')
        return red_flag

    @staticmethod
    def create(category_id, flag_text, severity='medium', order=0):
        """레드플래그 생성"""
        # 카테고리 존재 확인
        InterviewCategoryService.get_by_id(category_id)

        if severity not in ['low', 'medium', 'high', 'critical']:
            raise ValueError(f'잘못된 심각도: {severity}')

        red_flag = InterviewRedFlag(
            id=str(uuid.uuid4()),
            category_id=category_id,
            flag_text=flag_text,
            severity=severity,
            order=order
        )
        db.session.add(red_flag)
        db.session.commit()
        return red_flag

    @staticmethod
    def update(red_flag_id, **kwargs):
        """레드플래그 수정"""
        red_flag = InterviewRedFlagService.get_by_id(red_flag_id)

        if 'severity' in kwargs and kwargs['severity'] not in ['low', 'medium', 'high', 'critical']:
            raise ValueError(f'잘못된 심각도: {kwargs["severity"]}')

        for key, value in kwargs.items():
            if hasattr(red_flag, key) and value is not None:
                setattr(red_flag, key, value)

        db.session.commit()
        return red_flag

    @staticmethod
    def delete(red_flag_id):
        """레드플래그 삭제"""
        red_flag = InterviewRedFlagService.get_by_id(red_flag_id)
        db.session.delete(red_flag)
        db.session.commit()
        return True


class InterviewEvaluationService:
    """면접 평가 서비스 - 핵심 CRUD"""

    @staticmethod
    def get_list(page=1, limit=20, freelancer_id=None, recommendation=None, min_score=None,
                 sort_by='evaluated_at', sort_order='desc'):
        """평가 목록 조회"""
        query = InterviewEvaluation.query

        if freelancer_id:
            query = query.filter_by(freelancer_id=freelancer_id)

        if recommendation:
            query = query.filter_by(recommendation=recommendation)

        if min_score is not None:
            query = query.filter(InterviewEvaluation.total_score >= min_score)

        # 정렬
        sort_column = getattr(InterviewEvaluation, sort_by, InterviewEvaluation.evaluated_at)
        if sort_order.lower() == 'asc':
            query = query.order_by(sort_column)
        else:
            query = query.order_by(sort_column.desc())

        return paginate(query, page, limit)

    @staticmethod
    def get_by_id(evaluation_id):
        """평가 조회"""
        evaluation = InterviewEvaluation.query.get(evaluation_id)
        if not evaluation:
            raise ValueError(f'평가를 찾을 수 없습니다: {evaluation_id}')
        return evaluation

    @staticmethod
    def create(freelancer_id, interviewer_name=None, project_name=None,
               evaluated_at=None, notes=None):
        """평가 생성"""
        # 프리랜서 존재 확인
        freelancer = Freelancer.query.get(freelancer_id)
        if not freelancer:
            raise ValueError(f'프리랜서를 찾을 수 없습니다: {freelancer_id}')

        if evaluated_at is None:
            evaluated_at = datetime.utcnow()

        evaluation = InterviewEvaluation(
            id=str(uuid.uuid4()),
            freelancer_id=freelancer_id,
            interviewer_name=interviewer_name,
            project_name=project_name,
            evaluated_at=evaluated_at,
            notes=notes
        )
        db.session.add(evaluation)
        db.session.commit()
        return evaluation

    @staticmethod
    def update(evaluation_id, **kwargs):
        """평가 수정"""
        evaluation = InterviewEvaluationService.get_by_id(evaluation_id)

        if 'recommendation' in kwargs and kwargs['recommendation'] not in [None, 'recommend', 'not_recommend', 'pending']:
            raise ValueError(f'잘못된 추천 상태: {kwargs["recommendation"]}')

        for key, value in kwargs.items():
            if hasattr(evaluation, key) and value is not None:
                setattr(evaluation, key, value)

        db.session.commit()
        return evaluation

    @staticmethod
    def delete(evaluation_id):
        """평가 삭제"""
        evaluation = InterviewEvaluationService.get_by_id(evaluation_id)
        db.session.delete(evaluation)
        db.session.commit()
        return True

    @staticmethod
    def add_category_score(evaluation_id, category_id, score, score_label, checked_count=0):
        """카테고리 점수 추가"""
        # 평가 존재 확인
        evaluation = InterviewEvaluationService.get_by_id(evaluation_id)
        # 카테고리 존재 확인
        InterviewCategoryService.get_by_id(category_id)

        if score not in [1.0, 3.0, 5.0]:
            raise ValueError(f'잘못된 점수: {score}. 1.0, 3.0, 5.0만 가능합니다')

        if score_label not in ['하(1)', '중(3)', '상(5)']:
            raise ValueError(f'잘못된 점수 라벨: {score_label}')

        category_score = InterviewCategoryScore(
            id=str(uuid.uuid4()),
            evaluation_id=evaluation_id,
            category_id=category_id,
            score=score,
            score_label=score_label,
            checked_count=checked_count
        )
        db.session.add(category_score)
        db.session.commit()
        return category_score

    @staticmethod
    def update_category_score(evaluation_id, category_id, score, score_label, checked_count=0):
        """카테고리 점수 수정 또는 생성"""
        category_score = InterviewCategoryScore.query.filter_by(
            evaluation_id=evaluation_id,
            category_id=category_id
        ).first()

        if not category_score:
            return InterviewEvaluationService.add_category_score(
                evaluation_id, category_id, score, score_label, checked_count
            )

        if score not in [1.0, 3.0, 5.0]:
            raise ValueError(f'잘못된 점수: {score}. 1.0, 3.0, 5.0만 가능합니다')

        category_score.score = score
        category_score.score_label = score_label
        category_score.checked_count = checked_count
        db.session.commit()
        return category_score

    @staticmethod
    def add_checkpoint_result(evaluation_id, checkpoint_id, is_checked=False, notes=None):
        """체크포인트 결과 추가"""
        # 평가 존재 확인
        evaluation = InterviewEvaluationService.get_by_id(evaluation_id)
        # 체크포인트 존재 확인
        InterviewCheckpointService.get_by_id(checkpoint_id)

        # 중복 확인
        existing = InterviewEvaluationResult.query.filter_by(
            evaluation_id=evaluation_id,
            checkpoint_id=checkpoint_id
        ).first()
        if existing:
            raise ValueError(f'이미 존재하는 결과: {evaluation_id} - {checkpoint_id}')

        result = InterviewEvaluationResult(
            id=str(uuid.uuid4()),
            evaluation_id=evaluation_id,
            checkpoint_id=checkpoint_id,
            is_checked=is_checked,
            notes=notes
        )
        db.session.add(result)
        db.session.commit()
        return result

    @staticmethod
    def update_checkpoint_result(evaluation_id, checkpoint_id, is_checked=None, notes=None):
        """체크포인트 결과 수정"""
        result = InterviewEvaluationResult.query.filter_by(
            evaluation_id=evaluation_id,
            checkpoint_id=checkpoint_id
        ).first()

        if not result:
            return InterviewEvaluationService.add_checkpoint_result(
                evaluation_id, checkpoint_id, is_checked or False, notes
            )

        if is_checked is not None:
            result.is_checked = is_checked
        if notes is not None:
            result.notes = notes

        db.session.commit()
        return result

    @staticmethod
    def add_red_flag_finding(evaluation_id, red_flag_id, is_found=False, severity_actual=None, evidence=None):
        """레드플래그 발견 추가"""
        # 평가 존재 확인
        evaluation = InterviewEvaluationService.get_by_id(evaluation_id)
        # 레드플래그 존재 확인
        InterviewRedFlagService.get_by_id(red_flag_id)

        if severity_actual and severity_actual not in ['low', 'medium', 'high', 'critical']:
            raise ValueError(f'잘못된 심각도: {severity_actual}')

        # 중복 확인
        existing = InterviewRedFlagFinding.query.filter_by(
            evaluation_id=evaluation_id,
            red_flag_id=red_flag_id
        ).first()
        if existing:
            raise ValueError(f'이미 존재하는 발견: {evaluation_id} - {red_flag_id}')

        finding = InterviewRedFlagFinding(
            id=str(uuid.uuid4()),
            evaluation_id=evaluation_id,
            red_flag_id=red_flag_id,
            is_found=is_found,
            severity_actual=severity_actual,
            evidence=evidence
        )
        db.session.add(finding)
        db.session.commit()
        return finding

    @staticmethod
    def update_red_flag_finding(evaluation_id, red_flag_id, is_found=None,
                               severity_actual=None, evidence=None):
        """레드플래그 발견 수정"""
        finding = InterviewRedFlagFinding.query.filter_by(
            evaluation_id=evaluation_id,
            red_flag_id=red_flag_id
        ).first()

        if not finding:
            return InterviewEvaluationService.add_red_flag_finding(
                evaluation_id, red_flag_id, is_found or False, severity_actual, evidence
            )

        if is_found is not None:
            finding.is_found = is_found
        if severity_actual is not None:
            finding.severity_actual = severity_actual
        if evidence is not None:
            finding.evidence = evidence

        db.session.commit()
        return finding

    @staticmethod
    def calculate_total_score(evaluation_id):
        """총점 계산 및 저장"""
        evaluation = InterviewEvaluationService.get_by_id(evaluation_id)

        # 모든 카테고리 점수 조회
        category_scores = InterviewCategoryScore.query.filter_by(
            evaluation_id=evaluation_id
        ).all()

        if not category_scores:
            evaluation.total_score = 0
        else:
            # 총점 = (각 카테고리 점수 합) / (카테고리 수) × 20 = (각 카테고리 점수 합) × (20 / 카테고리 수)
            # 또는 간단히 (각 카테고리 점수 합 / 5) × 100 = (점수 합) × 20
            total_points = sum(cs.score for cs in category_scores)
            category_count = len(category_scores)
            # 정규화: 최대 5점씩 여러 카테고리의 평균을 100점 만점으로 변환
            evaluation.total_score = (total_points / category_count / 5.0) * 100

        db.session.commit()
        return evaluation.total_score

    @staticmethod
    def set_recommendation(evaluation_id, recommendation, notes=None):
        """추천 여부 설정"""
        evaluation = InterviewEvaluationService.get_by_id(evaluation_id)

        if recommendation not in ['recommend', 'not_recommend', 'pending']:
            raise ValueError(f'잘못된 추천 상태: {recommendation}')

        evaluation.recommendation = recommendation
        if notes is not None:
            evaluation.notes = notes

        db.session.commit()
        return evaluation
