"""
SuperManager 초기화 스크립트
- 데이터베이스 테이블 생성
- 초기 스킬 데이터 생성
- 테스트 프리랜서 데이터 생성
"""
import sys
import os

def check_database_connection():
    """데이터베이스 연결 확인"""
    from dotenv import load_dotenv

    load_dotenv()

    db_type = os.getenv('DB_TYPE', 'sqlite')

    # SQLite는 항상 연결 가능 (로컬 파일)
    if db_type != 'mysql':
        print("📁 SQLite 데이터베이스 사용 (로컬)")
        return True

    # MySQL 연결 확인
    try:
        import pymysql
        connection = pymysql.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            connect_timeout=3
        )
        connection.close()
        return True
    except Exception:
        return False


def init_database():
    """데이터베이스 초기화"""
    print("\n" + "="*60)
    print("🔄 데이터베이스 초기화 시작...")
    print("="*60)

    # 연결 확인
    print("\n📡 데이터베이스 연결 확인 중...")
    if not check_database_connection():
        print("❌ 데이터베이스 서버에 연결할 수 없습니다!")
        print(f"   Host: {os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}")
        print(f"   User: {os.getenv('DB_USER')}")
        print("\n💡 해결 방법:")
        print("   1. 데이터베이스 서버가 실행 중인지 확인하세요")
        print("   2. .env 파일의 DB_HOST, DB_PORT를 확인하세요")
        print("   3. 네트워크 연결을 확인하세요")
        return False

    print("✅ 데이터베이스 서버 연결 확인됨")

    from app import create_app
    from app.db import db

    try:
        app = create_app()

        with app.app_context():
            print("\n📋 테이블 생성 중...")
            db.create_all()
            print("✅ 테이블 생성 완료")

            # 연결 테스트
            try:
                from app.models import Freelancer
                count = Freelancer.query.count()
                print(f"✅ 데이터베이스 연결 성공 (현재 프리랜서: {count}명)")
            except Exception as e:
                print(f"⚠️  데이터베이스 쿼리 실패: {str(e)}")
                return False

        return True
    except Exception as e:
        print(f"❌ 데이터베이스 초기화 실패: {str(e)}")
        return False


def init_skills():
    """초기 스킬 데이터 생성"""
    print("\n" + "="*60)
    print("🎯 초기 스킬 데이터 생성 중...")
    print("="*60)

    from app import create_app
    from app.db import db
    from app.models import Skill

    INITIAL_SKILLS = [
        # Frontend
        {'id': 'react', 'name': 'React', 'category': 'frontend'},
        {'id': 'vue', 'name': 'Vue', 'category': 'frontend'},
        {'id': 'angular', 'name': 'Angular', 'category': 'frontend'},
        {'id': 'typescript', 'name': 'TypeScript', 'category': 'frontend'},
        {'id': 'javascript', 'name': 'JavaScript', 'category': 'frontend'},
        {'id': 'html5', 'name': 'HTML5', 'category': 'frontend'},
        {'id': 'css3', 'name': 'CSS3', 'category': 'frontend'},
        {'id': 'tailwind', 'name': 'Tailwind CSS', 'category': 'frontend'},

        # Backend
        {'id': 'nodejs', 'name': 'Node.js', 'category': 'backend'},
        {'id': 'python', 'name': 'Python', 'category': 'backend'},
        {'id': 'java', 'name': 'Java', 'category': 'backend'},
        {'id': 'dotnet', 'name': '.NET', 'category': 'backend'},
        {'id': 'php', 'name': 'PHP', 'category': 'backend'},
        {'id': 'golang', 'name': 'Go', 'category': 'backend'},
        {'id': 'rust', 'name': 'Rust', 'category': 'backend'},

        # Database
        {'id': 'mysql', 'name': 'MySQL', 'category': 'backend'},
        {'id': 'postgresql', 'name': 'PostgreSQL', 'category': 'backend'},
        {'id': 'mongodb', 'name': 'MongoDB', 'category': 'backend'},
        {'id': 'redis', 'name': 'Redis', 'category': 'backend'},

        # DevOps
        {'id': 'docker', 'name': 'Docker', 'category': 'devops'},
        {'id': 'kubernetes', 'name': 'Kubernetes', 'category': 'devops'},
        {'id': 'aws', 'name': 'AWS', 'category': 'devops'},
        {'id': 'gcp', 'name': 'Google Cloud', 'category': 'devops'},
        {'id': 'azure', 'name': 'Azure', 'category': 'devops'},
        {'id': 'jenkins', 'name': 'Jenkins', 'category': 'devops'},
        {'id': 'gitlab-ci', 'name': 'GitLab CI/CD', 'category': 'devops'},

        # Design
        {'id': 'figma', 'name': 'Figma', 'category': 'design'},
        {'id': 'ui-ux', 'name': 'UI/UX Design', 'category': 'design'},
        {'id': 'photoshop', 'name': 'Photoshop', 'category': 'design'},
        {'id': 'illustrator', 'name': 'Illustrator', 'category': 'design'},
    ]

    app = create_app()

    with app.app_context():
        created_count = 0
        skipped_count = 0

        for skill_data in INITIAL_SKILLS:
            existing = Skill.query.filter_by(id=skill_data['id']).first()
            if not existing:
                skill = Skill(
                    id=skill_data['id'],
                    name=skill_data['name'],
                    category=skill_data['category']
                )
                db.session.add(skill)
                created_count += 1
                print(f"  ✅ {skill_data['name']} ({skill_data['category']})")
            else:
                skipped_count += 1

        db.session.commit()
        print(f"\n📊 스킬 생성 완료: {created_count}개 생성, {skipped_count}개 스킵")

    return True


def init_freelancers():
    """테스트 프리랜서 데이터 생성"""
    print("\n" + "="*60)
    print("👥 테스트 프리랜서 데이터 생성 중...")
    print("="*60)

    import uuid
    from app import create_app
    from app.db import db
    from app.models import Freelancer, Skill

    TEST_FREELANCERS = [
        {
            'name': '김준호',
            'email': 'junho.kim@example.com',
            'phone': '010-1234-5678',
            'experience': 5,
            'hourly_rate': 50000,
            'bio': '경력 5년의 React 개발자입니다. UI/UX에 관심이 많습니다.',
            'skills': ['react', 'typescript', 'nodejs', 'javascript'],
            'availability': 'available',
        },
        {
            'name': '이수영',
            'email': 'suyoung.lee@example.com',
            'phone': '010-2345-6789',
            'experience': 7,
            'hourly_rate': 60000,
            'bio': '풀스택 개발자로 백엔드와 프론트엔드 모두 경험이 있습니다.',
            'skills': ['python', 'nodejs', 'react', 'postgresql'],
            'availability': 'available',
        },
        {
            'name': '박민준',
            'email': 'minjun.park@example.com',
            'phone': '010-3456-7890',
            'experience': 3,
            'hourly_rate': 35000,
            'bio': '신입 개발자지만 열정적으로 배우고 있습니다.',
            'skills': ['javascript', 'react', 'css3', 'html5'],
            'availability': 'busy',
        },
        {
            'name': '최지은',
            'email': 'jieun.choi@example.com',
            'phone': '010-4567-8901',
            'experience': 6,
            'hourly_rate': 55000,
            'bio': '데이터베이스 설계 및 최적화 전문가입니다.',
            'skills': ['mysql', 'postgresql', 'mongodb', 'redis'],
            'availability': 'available',
        },
        {
            'name': '정호준',
            'email': 'hojun.jung@example.com',
            'phone': '010-5678-9012',
            'experience': 8,
            'hourly_rate': 70000,
            'bio': 'DevOps 엔지니어로 클라우드 인프라 구축을 전담합니다.',
            'skills': ['docker', 'kubernetes', 'aws', 'jenkins'],
            'availability': 'available',
        },
        {
            'name': '유명희',
            'email': 'myunghee.yu@example.com',
            'phone': '010-6789-0123',
            'experience': 4,
            'hourly_rate': 45000,
            'bio': 'UI/UX 디자이너로 사용자 경험을 중시합니다.',
            'skills': ['figma', 'ui-ux', 'photoshop', 'illustrator'],
            'availability': 'available',
        },
        {
            'name': '한성호',
            'email': 'sungho.han@example.com',
            'phone': '010-7890-1234',
            'experience': 9,
            'hourly_rate': 75000,
            'bio': '대규모 프로젝트 리드 경험이 풍부합니다.',
            'skills': ['java', 'nodejs', 'mysql', 'docker'],
            'availability': 'busy',
        },
        {
            'name': '윤지수',
            'email': 'jisu.yoon@example.com',
            'phone': '010-8901-2345',
            'experience': 2,
            'hourly_rate': 30000,
            'bio': '최신 웹 기술을 배우고 있는 개발자입니다.',
            'skills': ['vue', 'typescript', 'tailwind'],
            'availability': 'available',
        },
    ]

    app = create_app()

    with app.app_context():
        created_count = 0
        skipped_count = 0

        for freelancer_data in TEST_FREELANCERS:
            existing = Freelancer.query.filter_by(email=freelancer_data['email']).first()
            if existing:
                skipped_count += 1
                continue

            freelancer = Freelancer(
                id=str(uuid.uuid4()),
                name=freelancer_data['name'],
                email=freelancer_data['email'],
                phone=freelancer_data['phone'],
                experience=freelancer_data.get('experience', 0),
                hourly_rate=freelancer_data.get('hourly_rate', 0),
                bio=freelancer_data.get('bio'),
                availability=freelancer_data.get('availability', 'available'),
                rating=round(3.5 + (hash(freelancer_data['email']) % 20) / 10, 1),
                review_count=int(hash(freelancer_data['email']) % 50),
            )

            for skill_id in freelancer_data.get('skills', []):
                skill = Skill.query.filter_by(id=skill_id).first()
                if skill:
                    freelancer.skills.append(skill)

            db.session.add(freelancer)
            created_count += 1
            print(f"  ✅ {freelancer_data['name']} ({freelancer_data['email']})")

        db.session.commit()
        print(f"\n📊 프리랜서 생성 완료: {created_count}명 생성, {skipped_count}명 스킵")

    return True


def main():
    """메인 초기화 함수"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "   🚀 SuperManager 백엔드 초기화 스크립트".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")

    try:
        # 1. 데이터베이스 초기화
        if not init_database():
            print("\n❌ 데이터베이스 초기화 실패")
            return False

        # 2. 스킬 데이터 생성
        if not init_skills():
            print("\n❌ 스킬 데이터 생성 실패")
            return False

        # 3. 프리랜서 데이터 생성
        if not init_freelancers():
            print("\n❌ 프리랜서 데이터 생성 실패")
            return False

        print("\n" + "="*60)
        print("✨ 초기화 완료!")
        print("="*60)
        print("\n📝 다음 단계:")
        print("  1. Flask 백엔드 시작: python app.py")
        print("  2. 프론트엔드 시작: npm run dev")
        print("\n🌐 API Endpoint: http://192.168.0.109:8000/api")
        print("="*60 + "\n")

        return True

    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
