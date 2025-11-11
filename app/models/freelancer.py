"""
Freelancer Model - 3NF Normalized Structure with Interview Evaluation
정규화 원칙:
- 1NF: 원자적 값만 저장 (JSON 제거)
- 2NF: 부분 함수 종속성 제거
- 3NF: 이행 함수 종속성 제거
"""
from datetime import datetime
from app.db import db

# ==================== Association Tables ====================

# Many-to-many: Freelancer ↔ Skill
freelancer_skill = db.Table(
    'freelancer_skill',
    db.Column('freelancer_id', db.String(36), db.ForeignKey('freelancer.id', ondelete='CASCADE'), primary_key=True),
    db.Column('skill_id', db.String(36), db.ForeignKey('skill.id', ondelete='CASCADE'), primary_key=True),
)

# ==================== Master Data ====================

class Skill(db.Model):
    """스킬 마스터 - 상수 데이터 (3NF 준수)"""
    __tablename__ = 'skill'

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    category = db.Column(db.String(50), nullable=False)  # frontend, backend, devops, design, etc
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    freelancers = db.relationship('Freelancer', secondary=freelancer_skill, backref='skills')

    def __repr__(self):
        return f'<Skill {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
        }


class InterviewCategory(db.Model):
    """면접 평가 카테고리 - 마스터 데이터 (3NF)"""
    __tablename__ = 'interview_category'

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)  # 기술역량, 포트폴리오, 커뮤니케이션, 업무방식
    description = db.Column(db.Text, nullable=True)
    weight = db.Column(db.Integer, default=1)  # 가중치 (예: 20점만점 중 몇 점)
    max_score = db.Column(db.Float, default=5.0)  # 최대 점수
    order = db.Column(db.Integer, nullable=False)

    # Relationships
    checkpoints = db.relationship('InterviewCheckpoint', back_populates='category', cascade='all, delete-orphan')
    red_flags = db.relationship('InterviewRedFlag', back_populates='category', cascade='all, delete-orphan')
    questions = db.relationship('InterviewQuestion', back_populates='category', cascade='all, delete-orphan')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<InterviewCategory {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'weight': self.weight,
            'maxScore': self.max_score,
            'order': self.order,
        }


class InterviewQuestion(db.Model):
    """면접 카테고리별 핵심 질문 (1NF - 원자화)"""
    __tablename__ = 'interview_question'

    id = db.Column(db.String(36), primary_key=True)
    category_id = db.Column(db.String(36), db.ForeignKey('interview_category.id', ondelete='CASCADE'), nullable=False, index=True)
    question_text = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer, nullable=False)

    # Relationships
    category = db.relationship('InterviewCategory', back_populates='questions')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<InterviewQuestion {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'categoryId': self.category_id,
            'questionText': self.question_text,
            'order': self.order,
        }


class InterviewCheckpoint(db.Model):
    """면접 체크포인트 - 평가 항목 (1NF - 원자화, 3NF - 카테고리에만 종속)"""
    __tablename__ = 'interview_checkpoint'

    id = db.Column(db.String(36), primary_key=True)
    category_id = db.Column(db.String(36), db.ForeignKey('interview_category.id', ondelete='CASCADE'), nullable=False, index=True)
    checkpoint_text = db.Column(db.Text, nullable=False)  # [ ] 사용 스택 선택 이유와 대안 설명
    order = db.Column(db.Integer, nullable=False)

    # Relationships
    category = db.relationship('InterviewCategory', back_populates='checkpoints')
    evaluation_results = db.relationship('InterviewEvaluationResult', back_populates='checkpoint', cascade='all, delete-orphan')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<InterviewCheckpoint {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'categoryId': self.category_id,
            'checkpointText': self.checkpoint_text,
            'order': self.order,
        }


class InterviewRedFlag(db.Model):
    """면접 레드플래그 - 주의 항목 (1NF - 원자화, 3NF)"""
    __tablename__ = 'interview_red_flag'

    id = db.Column(db.String(36), primary_key=True)
    category_id = db.Column(db.String(36), db.ForeignKey('interview_category.id', ondelete='CASCADE'), nullable=False, index=True)
    flag_text = db.Column(db.Text, nullable=False)  # 추상적 답변만 함 · 테스트/모듈화 부재
    severity = db.Column(db.String(20), default='medium')  # low, medium, high, critical
    order = db.Column(db.Integer, nullable=False)

    # Relationships
    category = db.relationship('InterviewCategory', back_populates='red_flags')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<InterviewRedFlag {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'categoryId': self.category_id,
            'flagText': self.flag_text,
            'severity': self.severity,
            'order': self.order,
        }


# ==================== Core Models ====================

class Freelancer(db.Model):
    """프리랜서 - 기본 개인정보 (1NF)"""
    __tablename__ = 'freelancer'

    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=False)

    # Relationships
    profile = db.relationship('FreelancerProfile', uselist=False, back_populates='freelancer', cascade='all, delete-orphan')
    portfolio_items = db.relationship('PortfolioItem', back_populates='freelancer', cascade='all, delete-orphan')
    reviews = db.relationship('Review', back_populates='freelancer', cascade='all, delete-orphan')
    interview_evaluations = db.relationship('InterviewEvaluation', back_populates='freelancer', cascade='all, delete-orphan')

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Freelancer {self.name}>'

    def to_dict(self, include_skills=True, include_portfolio=True, include_reviews=True, include_evaluations=False):
        """모델을 딕셔너리로 변환"""
        data = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'createdAt': self.created_at.isoformat(),
            'updatedAt': self.updated_at.isoformat(),
        }

        # Profile 정보 추가
        if self.profile:
            data.update({
                'experience': self.profile.experience,
                'hourlyRate': self.profile.hourly_rate,
                'avatar': self.profile.avatar,
                'bio': self.profile.bio,
                'availability': self.profile.availability,
            })

        # Skills 추가
        if include_skills:
            data['skills'] = [
                {
                    'id': skill.id,
                    'name': skill.name,
                    'category': skill.category,
                    'level': 'intermediate'  # 기본값
                }
                for skill in self.skills
            ]

        # Portfolio 추가
        if include_portfolio:
            data['portfolio'] = [item.to_dict() for item in self.portfolio_items]

        # Reviews 및 평점 추가
        if include_reviews and self.reviews:
            data['reviews'] = [review.to_dict() for review in self.reviews]
            # 평균 평점 계산
            avg_rating = sum(r.rating for r in self.reviews) / len(self.reviews) if self.reviews else 0
            data['rating'] = round(avg_rating, 2)
            data['reviewCount'] = len(self.reviews)

        # Interview Evaluations 추가
        if include_evaluations and self.interview_evaluations:
            data['interviewEvaluations'] = [ev.to_dict() for ev in self.interview_evaluations]

        return data


class FreelancerProfile(db.Model):
    """프리랜서 프로필 - 경력 및 요금 정보 (2NF)"""
    __tablename__ = 'freelancer_profile'

    id = db.Column(db.String(36), primary_key=True)
    freelancer_id = db.Column(db.String(36), db.ForeignKey('freelancer.id', ondelete='CASCADE'), nullable=False, unique=True, index=True)

    # 경력 및 요금
    experience = db.Column(db.Integer, default=0)  # 경력 년수
    hourly_rate = db.Column(db.Integer, default=0)  # 시급 (원)

    # 프로필
    avatar = db.Column(db.String(500), nullable=True)
    bio = db.Column(db.Text, nullable=True)

    # 상태
    availability = db.Column(db.String(20), default='available', index=True)  # available, busy, unavailable

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    freelancer = db.relationship('Freelancer', back_populates='profile')

    def __repr__(self):
        return f'<FreelancerProfile {self.freelancer_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'freelancerId': self.freelancer_id,
            'experience': self.experience,
            'hourlyRate': self.hourly_rate,
            'avatar': self.avatar,
            'bio': self.bio,
            'availability': self.availability,
            'createdAt': self.created_at.isoformat(),
            'updatedAt': self.updated_at.isoformat(),
        }


class PortfolioItem(db.Model):
    """포트폴리오 항목 - 원자화된 데이터 (1NF)"""
    __tablename__ = 'portfolio_item'

    id = db.Column(db.String(36), primary_key=True)
    freelancer_id = db.Column(db.String(36), db.ForeignKey('freelancer.id', ondelete='CASCADE'), nullable=False, index=True)

    # 포트폴리오 항목 정보
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    url = db.Column(db.String(500), nullable=True)
    image_url = db.Column(db.String(500), nullable=True)

    # 프로젝트 상세
    technologies = db.Column(db.JSON, default=list)  # List of tech stack
    duration_months = db.Column(db.Integer, nullable=True)  # 프로젝트 기간 (개월)
    role = db.Column(db.String(100), nullable=True)  # 담당 역할
    company = db.Column(db.String(200), nullable=True)  # 회사명

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    freelancer = db.relationship('Freelancer', back_populates='portfolio_items')

    def __repr__(self):
        return f'<PortfolioItem {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'freelancerId': self.freelancer_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'imageUrl': self.image_url,
            'technologies': self.technologies or [],
            'durationMonths': self.duration_months,
            'role': self.role,
            'company': self.company,
            'createdAt': self.created_at.isoformat(),
            'updatedAt': self.updated_at.isoformat(),
        }


class Review(db.Model):
    """리뷰 및 평점 (2NF)"""
    __tablename__ = 'review'

    id = db.Column(db.String(36), primary_key=True)
    freelancer_id = db.Column(db.String(36), db.ForeignKey('freelancer.id', ondelete='CASCADE'), nullable=False, index=True)

    # 리뷰 정보
    rating = db.Column(db.Float, nullable=False)  # 1.0 ~ 5.0
    comment = db.Column(db.Text, nullable=True)
    project_name = db.Column(db.String(200), nullable=True)  # 프로젝트명
    reviewer_name = db.Column(db.String(100), nullable=True)  # 리뷰어 이름

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    freelancer = db.relationship('Freelancer', back_populates='reviews')

    def __repr__(self):
        return f'<Review {self.freelancer_id} - {self.rating}>'

    def to_dict(self):
        return {
            'id': self.id,
            'freelancerId': self.freelancer_id,
            'rating': self.rating,
            'comment': self.comment,
            'projectName': self.project_name,
            'reviewerName': self.reviewer_name,
            'createdAt': self.created_at.isoformat(),
            'updatedAt': self.updated_at.isoformat(),
        }


# ==================== Interview Evaluation Models ====================

class InterviewEvaluation(db.Model):
    """면접 평가 기록 (2NF - 각 평가가 freelancer에 종속)"""
    __tablename__ = 'interview_evaluation'

    id = db.Column(db.String(36), primary_key=True)
    freelancer_id = db.Column(db.String(36), db.ForeignKey('freelancer.id', ondelete='CASCADE'), nullable=False, index=True)

    # 평가자/평가 정보
    interviewer_name = db.Column(db.String(100), nullable=True)  # 평가자명
    project_name = db.Column(db.String(200), nullable=True)  # 관련 프로젝트명
    total_score = db.Column(db.Float, nullable=True)  # 총점수 (0-100)
    recommendation = db.Column(db.String(50), nullable=True)  # recommend, not_recommend, pending
    notes = db.Column(db.Text, nullable=True)  # 추가 메모

    # Timestamps
    evaluated_at = db.Column(db.DateTime, nullable=False, index=True)  # 평가 날짜
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    freelancer = db.relationship('Freelancer', back_populates='interview_evaluations')
    category_scores = db.relationship('InterviewCategoryScore', back_populates='evaluation', cascade='all, delete-orphan')
    results = db.relationship('InterviewEvaluationResult', back_populates='evaluation', cascade='all, delete-orphan')
    red_flag_findings = db.relationship('InterviewRedFlagFinding', back_populates='evaluation', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<InterviewEvaluation {self.freelancer_id} - {self.evaluated_at}>'

    def to_dict(self, include_details=True):
        data = {
            'id': self.id,
            'freelancerId': self.freelancer_id,
            'interviewerName': self.interviewer_name,
            'projectName': self.project_name,
            'totalScore': self.total_score,
            'recommendation': self.recommendation,
            'notes': self.notes,
            'evaluatedAt': self.evaluated_at.isoformat(),
            'createdAt': self.created_at.isoformat(),
            'updatedAt': self.updated_at.isoformat(),
        }

        if include_details:
            data['categoryScores'] = [cs.to_dict() for cs in self.category_scores]
            data['checkpointResults'] = [r.to_dict() for r in self.results]
            data['redFlagFindings'] = [rff.to_dict() for rff in self.red_flag_findings]

        return data


class InterviewCategoryScore(db.Model):
    """면접 카테고리별 점수 (3NF - evaluation에만 종속)"""
    __tablename__ = 'interview_category_score'

    id = db.Column(db.String(36), primary_key=True)
    evaluation_id = db.Column(db.String(36), db.ForeignKey('interview_evaluation.id', ondelete='CASCADE'), nullable=False, index=True)
    category_id = db.Column(db.String(36), db.ForeignKey('interview_category.id', ondelete='CASCADE'), nullable=False, index=True)

    # 점수 정보
    score = db.Column(db.Float, nullable=False)  # 1.0, 3.0, 5.0
    score_label = db.Column(db.String(20), nullable=False)  # 하(1), 중(3), 상(5)
    checked_count = db.Column(db.Integer, default=0)  # 체크된 항목 수

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    evaluation = db.relationship('InterviewEvaluation', back_populates='category_scores')
    category = db.relationship('InterviewCategory')

    def __repr__(self):
        return f'<InterviewCategoryScore {self.category_id}={self.score}>'

    def to_dict(self):
        return {
            'id': self.id,
            'evaluationId': self.evaluation_id,
            'categoryId': self.category_id,
            'categoryName': self.category.name if self.category else None,
            'score': self.score,
            'scoreLabel': self.score_label,
            'checkedCount': self.checked_count,
        }


class InterviewEvaluationResult(db.Model):
    """면접 평가 결과 - 체크포인트 확인 여부 (3NF - evaluation과 checkpoint에만 종속)"""
    __tablename__ = 'interview_evaluation_result'

    id = db.Column(db.String(36), primary_key=True)
    evaluation_id = db.Column(db.String(36), db.ForeignKey('interview_evaluation.id', ondelete='CASCADE'), nullable=False, index=True)
    checkpoint_id = db.Column(db.String(36), db.ForeignKey('interview_checkpoint.id', ondelete='CASCADE'), nullable=False, index=True)

    # 결과
    is_checked = db.Column(db.Boolean, default=False)  # 체크 여부
    notes = db.Column(db.Text, nullable=True)  # 평가 노트

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    evaluation = db.relationship('InterviewEvaluation', back_populates='results')
    checkpoint = db.relationship('InterviewCheckpoint', back_populates='evaluation_results')

    __table_args__ = (
        db.UniqueConstraint('evaluation_id', 'checkpoint_id', name='uq_eval_checkpoint'),
    )

    def __repr__(self):
        return f'<InterviewEvaluationResult {self.evaluation_id} - {self.checkpoint_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'evaluationId': self.evaluation_id,
            'checkpointId': self.checkpoint_id,
            'checkpointText': self.checkpoint.checkpoint_text if self.checkpoint else None,
            'isChecked': self.is_checked,
            'notes': self.notes,
            'createdAt': self.created_at.isoformat(),
            'updatedAt': self.updated_at.isoformat(),
        }


class InterviewRedFlagFinding(db.Model):
    """면접 평가 중 발견된 레드플래그 (3NF - evaluation과 red_flag에만 종속)"""
    __tablename__ = 'interview_red_flag_finding'

    id = db.Column(db.String(36), primary_key=True)
    evaluation_id = db.Column(db.String(36), db.ForeignKey('interview_evaluation.id', ondelete='CASCADE'), nullable=False, index=True)
    red_flag_id = db.Column(db.String(36), db.ForeignKey('interview_red_flag.id', ondelete='CASCADE'), nullable=False, index=True)

    # 발견 여부
    is_found = db.Column(db.Boolean, default=False)  # 이 레드플래그가 발견되었는가?
    severity_actual = db.Column(db.String(20), nullable=True)  # 실제 심각도 (low, medium, high, critical)
    evidence = db.Column(db.Text, nullable=True)  # 근거/설명

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    evaluation = db.relationship('InterviewEvaluation', back_populates='red_flag_findings')
    red_flag = db.relationship('InterviewRedFlag')

    __table_args__ = (
        db.UniqueConstraint('evaluation_id', 'red_flag_id', name='uq_eval_red_flag'),
    )

    def __repr__(self):
        return f'<InterviewRedFlagFinding {self.evaluation_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'evaluationId': self.evaluation_id,
            'redFlagId': self.red_flag_id,
            'flagText': self.red_flag.flag_text if self.red_flag else None,
            'isFound': self.is_found,
            'severityActual': self.severity_actual,
            'evidence': self.evidence,
            'createdAt': self.created_at.isoformat(),
            'updatedAt': self.updated_at.isoformat(),
        }


# ==================== File Management ====================

class FreelancerDocument(db.Model):
    """프리랜서 문서 및 파일 관리 (3NF)"""
    __tablename__ = 'freelancer_document'

    id = db.Column(db.String(36), primary_key=True)
    freelancer_id = db.Column(db.String(36), db.ForeignKey('freelancer.id', ondelete='CASCADE'), nullable=False, index=True)

    # 문서 정보
    document_type = db.Column(db.String(50), nullable=False)  # resume, portfolio, certificate, cover_letter, etc
    original_filename = db.Column(db.String(500), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)  # 상대 경로
    file_size = db.Column(db.Integer, nullable=False)  # 바이트
    mime_type = db.Column(db.String(100), nullable=False)  # application/pdf, etc

    # 분석 결과
    extracted_text = db.Column(db.Text, nullable=True)  # 추출된 텍스트
    extracted_data = db.Column(db.JSON, nullable=True)  # 분석된 구조화 데이터
    # 예시:
    # {
    #   "skills": ["Python", "React"],
    #   "experience_years": 5,
    #   "education": ["서울대학교"],
    #   "projects": ["프로젝트1", "프로젝트2"]
    # }

    # 메타데이터
    is_analyzed = db.Column(db.Boolean, default=False, index=True)
    analysis_error = db.Column(db.Text, nullable=True)  # 분석 중 발생한 오류

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    freelancer = db.relationship('Freelancer', backref='documents')

    def __repr__(self):
        return f'<FreelancerDocument {self.id} - {self.document_type}>'

    def to_dict(self, include_text=False):
        data = {
            'id': self.id,
            'freelancerId': self.freelancer_id,
            'documentType': self.document_type,
            'originalFilename': self.original_filename,
            'fileSize': self.file_size,
            'mimeType': self.mime_type,
            'isAnalyzed': self.is_analyzed,
            'analysisError': self.analysis_error,
            'extractedData': self.extracted_data,
            'createdAt': self.created_at.isoformat(),
            'updatedAt': self.updated_at.isoformat(),
        }

        if include_text:
            data['extractedText'] = self.extracted_text

        return data
