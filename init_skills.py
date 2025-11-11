"""
초기 스킬 데이터 생성 스크립트
"""
from app import create_app
from app.db import db
from app.models import Skill

# 초기 스킬 데이터
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


def init_skills():
    """초기 스킬 데이터 생성"""
    app = create_app()

    with app.app_context():
        # 기존 스킬 데이터 삭제 (선택사항)
        # db.session.query(Skill).delete()

        # 스킬 추가
        for skill_data in INITIAL_SKILLS:
            # 이미 존재하는지 확인
            existing = Skill.query.filter_by(id=skill_data['id']).first()
            if not existing:
                skill = Skill(
                    id=skill_data['id'],
                    name=skill_data['name'],
                    category=skill_data['category']
                )
                db.session.add(skill)
                print(f'✅ 스킬 추가: {skill_data["name"]}')
            else:
                print(f'⏭️  스킬 이미 존재: {skill_data["name"]}')

        db.session.commit()
        print(f'\n✨ 총 {len(INITIAL_SKILLS)}개의 스킬이 준비되었습니다!')


if __name__ == '__main__':
    init_skills()
