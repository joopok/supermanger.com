#!/usr/bin/env python
"""
면접평가표 초기화 스크립트
Interview Evaluation Master Data Initialization
"""
import uuid
from app import create_app
from app.db import db
from app.models import InterviewCategory, InterviewQuestion, InterviewCheckpoint, InterviewRedFlag


def init_interview_data():
    """면접평가 마스터 데이터 초기화"""
    app = create_app()

    with app.app_context():
        # 기존 데이터 확인
        existing_count = InterviewCategory.query.count()
        if existing_count > 0:
            print(f'⚠️  이미 {existing_count}개의 카테고리가 존재합니다')
            response = input('계속하시겠습니까? (y/n): ')
            if response.lower() != 'y':
                print('취소됨')
                return

        print('📋 면접평가 카테고리 초기화 중...')

        # ==================== 1. 기술역량 & 문제해결 ====================
        tech_skills = InterviewCategory(
            id=str(uuid.uuid4()),
            name='기술 역량 & 문제해결',
            description='최근 프로젝트에서 가장 어려웠던 기술 문제와 해결 과정',
            weight=20,
            max_score=5.0,
            order=1
        )
        db.session.add(tech_skills)
        db.session.flush()

        tech_questions = [
            InterviewQuestion(
                id=str(uuid.uuid4()),
                category_id=tech_skills.id,
                question_text='최근 프로젝트에서 가장 어려웠던 기술 문제와 해결 과정은?',
                order=1
            )
        ]
        db.session.add_all(tech_questions)

        tech_checkpoints = [
            InterviewCheckpoint(
                id=str(uuid.uuid4()),
                category_id=tech_skills.id,
                checkpoint_text='사용 스택의 선택 이유와 대안 설명',
                order=1
            ),
            InterviewCheckpoint(
                id=str(uuid.uuid4()),
                category_id=tech_skills.id,
                checkpoint_text='설계·테스트·배포 흐름 이해',
                order=2
            ),
            InterviewCheckpoint(
                id=str(uuid.uuid4()),
                category_id=tech_skills.id,
                checkpoint_text='성능/보안/확장성 고려',
                order=3
            ),
        ]
        db.session.add_all(tech_checkpoints)

        tech_red_flags = [
            InterviewRedFlag(
                id=str(uuid.uuid4()),
                category_id=tech_skills.id,
                flag_text='추상적 답변만 함',
                severity='high',
                order=1
            ),
            InterviewRedFlag(
                id=str(uuid.uuid4()),
                category_id=tech_skills.id,
                flag_text='테스트/모듈화 부재',
                severity='high',
                order=2
            ),
            InterviewRedFlag(
                id=str(uuid.uuid4()),
                category_id=tech_skills.id,
                flag_text='도구/버전 이해 부족',
                severity='medium',
                order=3
            ),
        ]
        db.session.add_all(tech_red_flags)

        # ==================== 2. 포트폴리오/기여 검증 ====================
        portfolio = InterviewCategory(
            id=str(uuid.uuid4()),
            name='포트폴리오/기여 검증',
            description='포트폴리오에서 직접 구현한 부분과 기여도 검증',
            weight=20,
            max_score=5.0,
            order=2
        )
        db.session.add(portfolio)
        db.session.flush()

        portfolio_questions = [
            InterviewQuestion(
                id=str(uuid.uuid4()),
                category_id=portfolio.id,
                question_text='이 포트폴리오에서 직접 구현한 부분과 기여도(%)는?',
                order=1
            )
        ]
        db.session.add_all(portfolio_questions)

        portfolio_checkpoints = [
            InterviewCheckpoint(
                id=str(uuid.uuid4()),
                category_id=portfolio.id,
                checkpoint_text='코드/리포지터리/커밋 증빙',
                order=1
            ),
            InterviewCheckpoint(
                id=str(uuid.uuid4()),
                category_id=portfolio.id,
                checkpoint_text='데모 또는 산출물 제공',
                order=2
            ),
            InterviewCheckpoint(
                id=str(uuid.uuid4()),
                category_id=portfolio.id,
                checkpoint_text='재사용 가능한 구조/문서화',
                order=3
            ),
        ]
        db.session.add_all(portfolio_checkpoints)

        portfolio_red_flags = [
            InterviewRedFlag(
                id=str(uuid.uuid4()),
                category_id=portfolio.id,
                flag_text='기여 범위 모호',
                severity='critical',
                order=1
            ),
            InterviewRedFlag(
                id=str(uuid.uuid4()),
                category_id=portfolio.id,
                flag_text='NDA만으로 모든 증빙 거부',
                severity='critical',
                order=2
            ),
            InterviewRedFlag(
                id=str(uuid.uuid4()),
                category_id=portfolio.id,
                flag_text='데모 미제공',
                severity='high',
                order=3
            ),
        ]
        db.session.add_all(portfolio_red_flags)

        # ==================== 3. 커뮤니케이션 & 일정관리 ====================
        communication = InterviewCategory(
            id=str(uuid.uuid4()),
            name='커뮤니케이션 & 일정관리',
            description='불명확한 요구사항 명확화와 일정 공유 능력',
            weight=20,
            max_score=5.0,
            order=3
        )
        db.session.add(communication)
        db.session.flush()

        comm_questions = [
            InterviewQuestion(
                id=str(uuid.uuid4()),
                category_id=communication.id,
                question_text='불명확한 요구를 어떻게 명확화하나요? 지연 시 어떻게 공유하나요?',
                order=1
            )
        ]
        db.session.add_all(comm_questions)

        comm_checkpoints = [
            InterviewCheckpoint(
                id=str(uuid.uuid4()),
                category_id=communication.id,
                checkpoint_text='요구사항 정리 습관(메모/PRD)',
                order=1
            ),
            InterviewCheckpoint(
                id=str(uuid.uuid4()),
                category_id=communication.id,
                checkpoint_text='리스크 조기 공유 주기 합의',
                order=2
            ),
            InterviewCheckpoint(
                id=str(uuid.uuid4()),
                category_id=communication.id,
                checkpoint_text='이슈트래커/문서 도구 활용',
                order=3
            ),
        ]
        db.session.add_all(comm_checkpoints)

        comm_red_flags = [
            InterviewRedFlag(
                id=str(uuid.uuid4()),
                category_id=communication.id,
                flag_text='과도한 낙관 일정',
                severity='high',
                order=1
            ),
            InterviewRedFlag(
                id=str(uuid.uuid4()),
                category_id=communication.id,
                flag_text='피드백 방어적',
                severity='medium',
                order=2
            ),
            InterviewRedFlag(
                id=str(uuid.uuid4()),
                category_id=communication.id,
                flag_text='기록/회의록 회피',
                severity='medium',
                order=3
            ),
        ]
        db.session.add_all(comm_red_flags)

        # ==================== 4. 계약/업무 방식 & 품질보증 ====================
        contract = InterviewCategory(
            id=str(uuid.uuid4()),
            name='계약/업무 방식 & 품질보증',
            description='범위/마일스톤/소유권/보안/하자보수 합의 능력',
            weight=20,
            max_score=5.0,
            order=4
        )
        db.session.add(contract)
        db.session.flush()

        contract_questions = [
            InterviewQuestion(
                id=str(uuid.uuid4()),
                category_id=contract.id,
                question_text='범위/마일스톤/소유권/보안/하자보수는 어떻게 합의하나요?',
                order=1
            )
        ]
        db.session.add_all(contract_questions)

        contract_checkpoints = [
            InterviewCheckpoint(
                id=str(uuid.uuid4()),
                category_id=contract.id,
                checkpoint_text='명확한 SOW(범위·산출물)',
                order=1
            ),
            InterviewCheckpoint(
                id=str(uuid.uuid4()),
                category_id=contract.id,
                checkpoint_text='마일스톤-지불 연동',
                order=2
            ),
            InterviewCheckpoint(
                id=str(uuid.uuid4()),
                category_id=contract.id,
                checkpoint_text='테스트/리뷰/문서 기준',
                order=3
            ),
            InterviewCheckpoint(
                id=str(uuid.uuid4()),
                category_id=contract.id,
                checkpoint_text='IP/보안·SLA 합의',
                order=4
            ),
        ]
        db.session.add_all(contract_checkpoints)

        contract_red_flags = [
            InterviewRedFlag(
                id=str(uuid.uuid4()),
                category_id=contract.id,
                flag_text='선지급 과다 요구',
                severity='high',
                order=1
            ),
            InterviewRedFlag(
                id=str(uuid.uuid4()),
                category_id=contract.id,
                flag_text='소스코드 전달/소유권 거부',
                severity='critical',
                order=2
            ),
            InterviewRedFlag(
                id=str(uuid.uuid4()),
                category_id=contract.id,
                flag_text='유지보수 불가',
                severity='critical',
                order=3
            ),
            InterviewRedFlag(
                id=str(uuid.uuid4()),
                category_id=contract.id,
                flag_text='SLA 부재',
                severity='high',
                order=4
            ),
        ]
        db.session.add_all(contract_red_flags)

        # 데이터베이스에 저장
        db.session.commit()

        print('✅ 면접평가 마스터 데이터 초기화 완료')
        print(f'   - 카테고리: 4개')
        print(f'   - 질문: {len(tech_questions) + len(portfolio_questions) + len(comm_questions) + len(contract_questions)}개')
        print(f'   - 체크포인트: {len(tech_checkpoints) + len(portfolio_checkpoints) + len(comm_checkpoints) + len(contract_checkpoints)}개')
        print(f'   - 레드플래그: {len(tech_red_flags) + len(portfolio_red_flags) + len(comm_red_flags) + len(contract_red_flags)}개')

        # 추천 기준 정보 출력
        print('\n📌 인력 추천 기준:')
        print('   - 최소 65점 이상인 경우만 추천')
        print('   - 현재 프로젝트 특성을 많이 알고 있는 경우 예외로 문의 후 진행')


if __name__ == '__main__':
    init_interview_data()
