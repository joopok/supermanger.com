"""
테스트 데이터 생성 스크립트 - 3NF 정규화 구조
"""
import uuid
from datetime import datetime, timedelta
from app import create_app
from app.db import db
from app.models import Freelancer, FreelancerProfile, Skill, PortfolioItem, Review

# 테스트 프리랜서 데이터
TEST_FREELANCERS = [
    {
        'name': '김준호',
        'email': 'junho.kim@example.com',
        'phone': '010-1234-5678',
        'experience': 5,
        'hourly_rate': 50000,
        'bio': '경력 5년의 React 개발자입니다. UI/UX에 관심이 많습니다.',
        'availability': 'available',
        'skills': ['react', 'typescript', 'nodejs', 'javascript'],
        'portfolio': [
            {
                'title': '전자상거래 플랫폼',
                'description': 'React와 Node.js로 구축한 풀스택 전자상거래 플랫폼',
                'technologies': ['react', 'nodejs', 'mongodb', 'stripe'],
                'role': '프론트엔드 리드',
                'company': '테크스타트업',
                'duration_months': 12,
                'url': 'https://example-ecommerce.com'
            },
            {
                'title': '모바일 앱 개발',
                'description': 'React Native로 개발한 건강관리 모바일 앱',
                'technologies': ['react-native', 'typescript', 'firebase'],
                'role': '풀스택 개발자',
                'company': '헬스테크 스타트업',
                'duration_months': 8,
                'url': 'https://example-mobile-app.com'
            }
        ],
        'reviews': [
            {'rating': 4.8, 'comment': '우수한 기술력과 의사소통 능력', 'project': '전자상거래 프로젝트'},
            {'rating': 4.5, 'comment': '일정 관리가 탁월함', 'project': '모바일 앱 프로젝트'},
            {'rating': 4.9, 'comment': '코드 품질이 매우 높음', 'project': '추가 프로젝트'}
        ]
    },
    {
        'name': '이수영',
        'email': 'suyoung.lee@example.com',
        'phone': '010-2345-6789',
        'experience': 7,
        'hourly_rate': 60000,
        'bio': '풀스택 개발자로 백엔드와 프론트엔드 모두 경험이 있습니다.',
        'availability': 'available',
        'skills': ['python', 'django', 'react', 'postgresql'],
        'portfolio': [
            {
                'title': 'SaaS 플랫폼',
                'description': 'Django와 React로 구축한 SaaS 플랫폼',
                'technologies': ['django', 'react', 'postgresql', 'docker'],
                'role': '풀스택 개발자',
                'company': '엔터프라이즈 소프트웨어',
                'duration_months': 18,
                'url': 'https://example-saas.com'
            }
        ],
        'reviews': [
            {'rating': 4.7, 'comment': '데이터베이스 설계가 뛰어남', 'project': 'SaaS 플랫폼'},
            {'rating': 4.6, 'comment': '성능 최적화를 잘함', 'project': '추가 프로젝트'}
        ]
    },
    {
        'name': '박민준',
        'email': 'minjun.park@example.com',
        'phone': '010-3456-7890',
        'experience': 3,
        'hourly_rate': 35000,
        'bio': '신입 개발자지만 열정적으로 배우고 있습니다.',
        'availability': 'busy',
        'skills': ['javascript', 'react', 'css3', 'html5'],
        'portfolio': [
            {
                'title': '개인 포트폴리오 사이트',
                'description': 'React로 구축한 반응형 포트폴리오 웹사이트',
                'technologies': ['react', 'tailwind-css', 'javascript'],
                'role': '개발자',
                'company': '개인 프로젝트',
                'duration_months': 3,
                'url': 'https://example-portfolio.com'
            }
        ],
        'reviews': [
            {'rating': 4.2, 'comment': '배우는 속도가 빠름', 'project': '포트폴리오 사이트'},
        ]
    },
    {
        'name': '최지은',
        'email': 'jieun.choi@example.com',
        'phone': '010-4567-8901',
        'experience': 6,
        'hourly_rate': 55000,
        'bio': '데이터베이스 설계 및 최적화 전문가입니다.',
        'availability': 'available',
        'skills': ['mysql', 'postgresql', 'mongodb', 'redis'],
        'portfolio': [
            {
                'title': '대규모 데이터베이스 최적화',
                'description': '100만 사용자 규모 서비스의 데이터베이스 최적화',
                'technologies': ['postgresql', 'redis', 'elasticsearch'],
                'role': '데이터베이스 아키텍트',
                'company': '대형 기술 회사',
                'duration_months': 12,
                'url': 'https://example-case-study.com'
            }
        ],
        'reviews': [
            {'rating': 4.9, 'comment': '데이터베이스 최적화 전문가', 'project': '대규모 최적화'},
            {'rating': 4.8, 'comment': '성능 향상 눈에 띔', 'project': '추가 프로젝트'}
        ]
    },
    {
        'name': '정호준',
        'email': 'hojun.jung@example.com',
        'phone': '010-5678-9012',
        'experience': 8,
        'hourly_rate': 70000,
        'bio': 'DevOps 엔지니어로 클라우드 인프라 구축을 전담합니다.',
        'availability': 'available',
        'skills': ['docker', 'kubernetes', 'aws', 'jenkins'],
        'portfolio': [
            {
                'title': '마이크로서비스 인프라 구축',
                'description': 'AWS 기반 Kubernetes 클러스터로 마이크로서비스 아키텍처 구축',
                'technologies': ['kubernetes', 'aws', 'docker', 'terraform'],
                'role': 'DevOps 리드',
                'company': '클라우드 네이티브 스타트업',
                'duration_months': 20,
                'url': 'https://example-devops.com'
            }
        ],
        'reviews': [
            {'rating': 4.9, 'comment': '인프라 구축 능력이 뛰어남', 'project': '마이크로서비스'},
            {'rating': 4.7, 'comment': '자동화를 잘함', 'project': 'CI/CD 구축'}
        ]
    },
    {
        'name': '유명희',
        'email': 'myunghee.yu@example.com',
        'phone': '010-6789-0123',
        'experience': 4,
        'hourly_rate': 45000,
        'bio': 'UI/UX 디자이너로 사용자 경험을 중시합니다.',
        'availability': 'available',
        'skills': ['figma', 'ui-ux', 'photoshop', 'illustrator'],
        'portfolio': [
            {
                'title': 'B2B SaaS UI/UX 디자인',
                'description': 'B2B SaaS 플랫폼의 전체 UI/UX 디자인 및 구현',
                'technologies': ['figma', 'design-systems'],
                'role': 'UI/UX 디자이너',
                'company': 'B2B 소프트웨어 회사',
                'duration_months': 10,
                'url': 'https://example-design.com'
            }
        ],
        'reviews': [
            {'rating': 4.8, 'comment': '디자인 감각이 우수함', 'project': 'SaaS UI/UX'},
            {'rating': 4.6, 'comment': '사용자 피드백 반영이 잘됨', 'project': '추가 프로젝트'}
        ]
    },
    {
        'name': '한성호',
        'email': 'sungho.han@example.com',
        'phone': '010-7890-1234',
        'experience': 9,
        'hourly_rate': 75000,
        'bio': '대규모 프로젝트 리드 경험이 풍부합니다.',
        'availability': 'busy',
        'skills': ['java', 'spring', 'mysql', 'docker'],
        'portfolio': [
            {
                'title': '금융 시스템 구축',
                'description': 'Spring Boot 기반 대규모 금융 거래 시스템',
                'technologies': ['spring-boot', 'mysql', 'redis', 'kafka'],
                'role': '기술 리드',
                'company': '금융 회사',
                'duration_months': 24,
                'url': 'https://example-fintech.com'
            }
        ],
        'reviews': [
            {'rating': 4.9, 'comment': '리더십이 뛰어남', 'project': '금융 시스템'},
            {'rating': 4.8, 'comment': '복잡한 요구사항을 잘 처리함', 'project': '추가 프로젝트'},
            {'rating': 4.7, 'comment': '팀 매니지먼트 능력이 뛰어남', 'project': '또 다른 프로젝트'}
        ]
    },
    {
        'name': '윤지수',
        'email': 'jisu.yoon@example.com',
        'phone': '010-8901-2345',
        'experience': 2,
        'hourly_rate': 30000,
        'bio': '최신 웹 기술을 배우고 있는 개발자입니다.',
        'availability': 'available',
        'skills': ['vue', 'typescript', 'tailwind'],
        'portfolio': [
            {
                'title': '블로그 플랫폼',
                'description': 'Vue 3와 TypeScript로 구축한 블로그 플랫폼',
                'technologies': ['vue', 'typescript', 'tailwind'],
                'role': '개발자',
                'company': 'Web3 스타트업',
                'duration_months': 5,
                'url': 'https://example-blog.com'
            }
        ],
        'reviews': [
            {'rating': 4.3, 'comment': '기술 습득이 빠름', 'project': '블로그 플랫폼'},
        ]
    },
]


def init_data():
    """테스트 데이터 생성 - 3NF 정규화 구조"""
    app = create_app()

    with app.app_context():
        # 프리랜서 추가
        for freelancer_data in TEST_FREELANCERS:
            # 이미 존재하는지 확인
            existing = Freelancer.query.filter_by(email=freelancer_data['email']).first()
            if existing:
                print(f'⏭️  프리랜서 이미 존재: {freelancer_data["name"]}')
                continue

            # 1. Freelancer 생성 (기본 정보만)
            freelancer = Freelancer(
                id=str(uuid.uuid4()),
                name=freelancer_data['name'],
                email=freelancer_data['email'],
                phone=freelancer_data['phone'],
            )
            db.session.add(freelancer)
            db.session.flush()

            # 2. FreelancerProfile 생성 (경력/요금 정보)
            profile = FreelancerProfile(
                id=str(uuid.uuid4()),
                freelancer_id=freelancer.id,
                experience=freelancer_data.get('experience', 0),
                hourly_rate=freelancer_data.get('hourly_rate', 0),
                bio=freelancer_data.get('bio'),
                availability=freelancer_data.get('availability', 'available'),
            )
            db.session.add(profile)
            db.session.flush()

            # 3. 스킬 연결
            for skill_id in freelancer_data.get('skills', []):
                skill = Skill.query.filter_by(id=skill_id).first()
                if skill:
                    freelancer.skills.append(skill)

            # 4. PortfolioItem 생성
            for portfolio_item in freelancer_data.get('portfolio', []):
                item = PortfolioItem(
                    id=str(uuid.uuid4()),
                    freelancer_id=freelancer.id,
                    title=portfolio_item['title'],
                    description=portfolio_item.get('description'),
                    url=portfolio_item.get('url'),
                    technologies=portfolio_item.get('technologies', []),
                    duration_months=portfolio_item.get('duration_months'),
                    role=portfolio_item.get('role'),
                    company=portfolio_item.get('company'),
                )
                db.session.add(item)
            db.session.flush()

            # 5. Review 생성
            for idx, review_data in enumerate(freelancer_data.get('reviews', [])):
                review = Review(
                    id=str(uuid.uuid4()),
                    freelancer_id=freelancer.id,
                    rating=review_data.get('rating', 4.0),
                    comment=review_data.get('comment'),
                    project_name=review_data.get('project'),
                    reviewer_name=f"클라이언트_{idx + 1}",
                    created_at=datetime.utcnow() - timedelta(days=30 - idx * 10),
                )
                db.session.add(review)

            db.session.commit()
            print(f'✅ 프리랜서 추가: {freelancer_data["name"]}')
            print(f'   - 프로필: {profile.experience}년 경력, ₩{profile.hourly_rate:,}/시간')
            print(f'   - 스킬: {len(freelancer.skills)}개')
            print(f'   - 포트폴리오: {len(freelancer.portfolio_items)}개')
            print(f'   - 리뷰: {len(freelancer.reviews)}개\n')

        print(f'✨ 총 {len(TEST_FREELANCERS)}개의 테스트 프리랜서가 생성되었습니다!')


if __name__ == '__main__':
    print('📋 필수 스크립트 실행 순서:')
    print('1️⃣  python init_skills.py          (스킬 마스터 생성)')
    print('2️⃣  python init_interview.py       (면접평가 마스터 생성)')
    print('3️⃣  python init_data.py            (프리랜서 테스트 데이터 생성)\n')

    init_data()
