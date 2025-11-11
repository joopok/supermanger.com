"""
Freelancer Service
비즈니스 로직 처리
"""
import uuid
from datetime import datetime
from sqlalchemy.orm import joinedload, selectinload
from app.db import db
from app.models import Freelancer, FreelancerProfile, Skill, FreelancerDocument
from app.models.freelancer import freelancer_skill
from app.utils import paginate
from app.services.file_service import FileService, ResumeAnalyzer, PortfolioAnalyzer


class FreelancerService:
    """프리랜서 서비스"""

    @staticmethod
    def get_list(page=1, limit=20, search=None, skills=None, availability=None,
                 min_rating=None, min_experience=None, max_hourly_rate=None,
                 sort_by='name', sort_order='asc'):
        """프리랜서 목록 조회 with 필터링, 정렬, 페이지네이션 (한 번의 쿼리로 모든 데이터 로드)"""
        # Eager Loading: 관계 데이터를 미리 로드하여 N+1 쿼리 문제 해결
        query = Freelancer.query.outerjoin(FreelancerProfile).options(
            joinedload(Freelancer.profile),  # 1:1 관계
            selectinload(Freelancer.skills),  # Many-to-Many 관계
            selectinload(Freelancer.portfolio_items),  # 1:Many 관계
            selectinload(Freelancer.reviews),  # 1:Many 관계
            selectinload(Freelancer.interview_evaluations),  # 1:Many 관계
            selectinload(Freelancer.documents),  # 1:Many 관계
        )

        # 필터링
        if search:
            query = query.filter(
                db.or_(
                    Freelancer.name.ilike(f'%{search}%'),
                    Freelancer.email.ilike(f'%{search}%'),
                    FreelancerProfile.bio.ilike(f'%{search}%')
                )
            )

        if skills and len(skills) > 0:
            query = query.join(Skill).filter(Skill.id.in_(skills)).distinct()

        if availability:
            query = query.filter(FreelancerProfile.availability == availability)

        if min_rating is not None:
            # 리뷰가 있을 때만 평점 필터링
            query = query.filter(
                db.or_(
                    Freelancer.reviews.any(db.func.avg(Freelancer.reviews.c.rating) >= min_rating),
                    ~Freelancer.reviews.any()  # 리뷰가 없는 경우도 포함
                )
            )

        if min_experience is not None:
            query = query.filter(FreelancerProfile.experience >= min_experience)

        if max_hourly_rate is not None:
            query = query.filter(FreelancerProfile.hourly_rate <= max_hourly_rate)

        # 정렬
        if sort_by == 'name':
            sort_column = Freelancer.name
        elif sort_by == 'experience':
            sort_column = FreelancerProfile.experience
        elif sort_by == 'hourlyRate':
            sort_column = FreelancerProfile.hourly_rate
        else:
            sort_column = Freelancer.created_at

        if sort_order.lower() == 'desc':
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())

        # 페이지네이션 (이미 모든 데이터가 로드됨)
        paginated = paginate(query, page, limit)

        # 응답 데이터 변환 (추가 쿼리 없음 - 메모리 캐시 사용)
        paginated['data'] = [item.to_dict() for item in paginated['data']]

        return paginated

    @staticmethod
    def get_by_id(freelancer_id):
        """프리랜서 상세 조회 (Eager Loading으로 한 번의 쿼리)"""
        # Eager Loading으로 모든 관계 데이터를 미리 로드
        freelancer = Freelancer.query.options(
            joinedload(Freelancer.profile),
            selectinload(Freelancer.skills),
            selectinload(Freelancer.portfolio_items),
            selectinload(Freelancer.reviews),
            selectinload(Freelancer.interview_evaluations),
            selectinload(Freelancer.documents),
        ).get(freelancer_id)

        if not freelancer:
            raise ValueError('프리랜서를 찾을 수 없습니다')
        return freelancer.to_dict()

    @staticmethod
    def create(data):
        """프리랜서 생성"""
        # 이메일 중복 확인
        if Freelancer.query.filter_by(email=data['email']).first():
            raise ValueError('이미 등록된 이메일입니다')

        # 스킬 검증
        skill_ids = data.get('skillIds', [])
        if not skill_ids:
            raise ValueError('최소 1개 이상의 스킬을 선택해주세요')

        # 새로운 프리랜서 생성 (기본 정보만)
        freelancer_id = str(uuid.uuid4())
        freelancer = Freelancer(
            id=freelancer_id,
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
        )

        # 프리랜서 프로필 생성 (경력, 요금, 상태 등)
        profile = FreelancerProfile(
            id=str(uuid.uuid4()),
            freelancer_id=freelancer_id,
            experience=data.get('experience', 0),
            hourly_rate=data.get('hourlyRate', 0),
            avatar=data.get('avatar'),
            bio=data.get('bio'),
            availability=data.get('availability', 'available'),
        )

        # 저장 (먼저 freelancer와 profile만)
        db.session.add(freelancer)
        db.session.add(profile)
        db.session.flush()  # ID 생성을 위해 flush

        # 스킬 연결 (직접 INSERT)
        for skill_id in skill_ids:
            skill = Skill.query.get(skill_id)
            if skill:
                # INSERT문으로 직접 추가 (association table 구조에 맞춤)
                db.session.execute(
                    db.insert(freelancer_skill).values(
                        freelancer_id=freelancer_id,
                        skill_id=skill_id
                    )
                )

        db.session.commit()

        return freelancer.to_dict()

    @staticmethod
    def update(freelancer_id, data):
        """프리랜서 정보 수정"""
        freelancer = Freelancer.query.get(freelancer_id)
        if not freelancer:
            raise ValueError('프리랜서를 찾을 수 없습니다')

        # 이메일 중복 확인 (다른 프리랜서)
        if 'email' in data:
            existing = Freelancer.query.filter_by(email=data['email']).first()
            if existing and existing.id != freelancer_id:
                raise ValueError('이미 등록된 이메일입니다')

        # 필드 업데이트
        for field, value in data.items():
            if field == 'skillIds':
                # 스킬 업데이트 (association table 수정)
                # 기존 스킬 제거
                db.session.execute(
                    db.delete(freelancer_skill).where(
                        freelancer_skill.c.freelancer_id == freelancer_id
                    )
                )
                # 새로운 스킬 추가
                for skill_id in value:
                    skill = Skill.query.get(skill_id)
                    if skill:
                        db.session.execute(
                            db.insert(freelancer_skill).values(
                                freelancer_id=freelancer_id,
                                skill_id=skill_id
                            )
                        )
            elif field == 'hourlyRate':
                setattr(freelancer, 'hourly_rate', value)
            else:
                if hasattr(freelancer, field):
                    setattr(freelancer, field, value)

        freelancer.updated_at = datetime.utcnow()
        db.session.commit()

        return freelancer.to_dict()

    @staticmethod
    def delete(freelancer_id):
        """프리랜서 삭제"""
        freelancer = Freelancer.query.get(freelancer_id)
        if not freelancer:
            raise ValueError('프리랜서를 찾을 수 없습니다')

        db.session.delete(freelancer)
        db.session.commit()

    @staticmethod
    def get_skills():
        """전체 스킬 목록 조회"""
        skills = Skill.query.all()
        return [skill.to_dict() for skill in skills]

    @staticmethod
    def get_or_create_skills(skill_ids):
        """스킬 ID로 스킬 객체 조회 또는 생성"""
        skills = []
        for skill_id in skill_ids:
            skill = Skill.query.get(skill_id)
            if not skill:
                # 기본 스킬 생성 (실제로는 프론트에서 전달된 스킬만 사용)
                skill = Skill(
                    id=skill_id,
                    name=skill_id,
                    category='other'
                )
                db.session.add(skill)
            skills.append(skill)

        db.session.commit()
        return skills


# ==================== Document Management ====================

class FreelancerDocumentService:
    """프리랜서 문서 관리 서비스"""

    @staticmethod
    def upload_document(freelancer_id: str, file, document_type: str, upload_dir: str):
        """문서 업로드 및 분석"""
        # 프리랜서 존재 확인
        freelancer = Freelancer.query.get(freelancer_id)
        if not freelancer:
            raise ValueError('프리랜서를 찾을 수 없습니다')

        # 파일 유효성 검사
        is_valid, message = FileService.validate_file(file)
        if not is_valid:
            raise ValueError(message)

        # 파일 저장
        success, saved_filename, file_path = FileService.save_file(file, upload_dir)
        if not success:
            raise ValueError(f'파일 저장 실패: {file_path}')

        # 파일 정보 추출
        file.seek(0, 2)
        file_size = file.tell()
        file.seek(0)

        mime_type = file.content_type or 'application/octet-stream'

        # 문서 객체 생성
        doc_id = str(uuid.uuid4())
        document = FreelancerDocument(
            id=doc_id,
            freelancer_id=freelancer_id,
            document_type=document_type,
            original_filename=file.filename,
            file_path=file_path,
            file_size=file_size,
            mime_type=mime_type,
        )

        db.session.add(document)
        db.session.flush()

        # 텍스트 추출 및 분석
        FreelancerDocumentService._analyze_document(document)

        db.session.commit()
        return document.to_dict()

    @staticmethod
    def _analyze_document(document: FreelancerDocument):
        """문서 분석 및 정보 추출"""
        try:
            # 텍스트 추출
            success, text = FileService.extract_text_from_file(document.file_path)

            if not success:
                document.is_analyzed = False
                document.analysis_error = text  # 오류 메시지
                return

            # 텍스트 저장
            document.extracted_text = text

            # 문서 타입에 따른 분석
            if document.document_type == 'resume':
                extracted_data = ResumeAnalyzer.analyze(text)
            elif document.document_type == 'portfolio':
                extracted_data = PortfolioAnalyzer.analyze(text)
            else:
                extracted_data = {'text': text[:500]}  # 기본: 처음 500자

            document.extracted_data = extracted_data
            document.is_analyzed = True

        except Exception as e:
            document.is_analyzed = False
            document.analysis_error = str(e)

    @staticmethod
    def get_documents(freelancer_id: str, page=1, limit=20, document_type=None):
        """프리랜서 문서 목록 조회"""
        query = FreelancerDocument.query.filter_by(freelancer_id=freelancer_id)

        if document_type:
            query = query.filter_by(document_type=document_type)

        query = query.order_by(FreelancerDocument.created_at.desc())

        return paginate(query, page, limit)

    @staticmethod
    def get_document(document_id: str):
        """문서 조회"""
        document = FreelancerDocument.query.get(document_id)
        if not document:
            raise ValueError('문서를 찾을 수 없습니다')
        return document.to_dict(include_text=True)

    @staticmethod
    def delete_document(document_id: str):
        """문서 삭제"""
        document = FreelancerDocument.query.get(document_id)
        if not document:
            raise ValueError('문서를 찾을 수 없습니다')

        # 파일 삭제
        import os
        try:
            if os.path.exists(document.file_path):
                os.remove(document.file_path)
        except Exception as e:
            print(f'파일 삭제 실패: {str(e)}')

        # DB에서 삭제
        db.session.delete(document)
        db.session.commit()

        return True

    @staticmethod
    def re_analyze_document(document_id: str):
        """문서 재분석"""
        document = FreelancerDocument.query.get(document_id)
        if not document:
            raise ValueError('문서를 찾을 수 없습니다')

        FreelancerDocumentService._analyze_document(document)
        db.session.commit()

        return document.to_dict()
