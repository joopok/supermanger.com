# 🚀 SuperManager 빠른 시작 가이드

인력목록/인력등록 시스템의 완전한 CRUD 기능이 준비되었습니다!

## 📋 시스템 구성

```
프론트엔드 (React)          백엔드 (Flask)            데이터베이스 (MariaDB)
├─ FreelancerListPage      ├─ /api/freelancers      ├─ freelancer (테이블)
├─ FreelancerFormPage      ├─ /api/freelancers/{id} ├─ skill (테이블)
└─ ApiTestPage             └─ DB 초기화 스크립트     └─ supermanager (DB)
```

## 🔐 서버 정보

```
마리아DB 서버 정보:
├─ Host: 192.168.0.109
├─ Port: 3306
├─ User: joopok
├─ Password: ~Asy10131227
└─ Database: supermanager
```

---

## ⚡ Step 1: 백엔드 초기 설정

### 1-1. Python 의존성 설치

```bash
cd /Users/doseunghyeon/developerApp/python/www.supermanger.com
pip install -r requirements.txt
```

**설치될 패키지:**
- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- Flask-CORS 4.0.0
- PyMySQL 1.1.0
- Marshmallow 3.20.1

### 1-2. 데이터베이스 초기화

```bash
# 방법 1: 자동 초기화 (권장)
python setup.py

# 방법 2: 수동 초기화
# MySQL에서 다음 명령 실행
mysql -h 192.168.0.109 -u joopok -p
> CREATE DATABASE supermanager CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
> exit
```

**초기화 결과:**
```
✨ 초기화 완료!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 테이블 생성: freelancer, skill, freelancer_skill
📊 스킬 데이터: 30개 생성
👥 프리랜서 데이터: 8명 생성
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🚀 Step 2: 백엔드 서버 시작

### 방법 A: 자동 실행 스크립트 (권장)

```bash
chmod +x run_server.sh
./run_server.sh
```

### 방법 B: 수동 실행

```bash
python app.py
```

**출력 예시:**
```
╔════════════════════════════════════════════════════════╗
║     🚀 SuperManager 백엔드 서버 시작                    ║
╚════════════════════════════════════════════════════════╝

1️⃣ 의존성 확인 중...
   ✅ Flask 설치됨

2️⃣ 데이터베이스 초기화 중...
   ✅ 테이블 생성 완료
   ✅ 30개의 스킬이 준비되었습니다!
   ✅ 8명의 프리랜서가 생성되었습니다!

3️⃣ Flask 서버 시작 중...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✨ 서버가 시작되었습니다!

   🌐 API 주소: http://192.168.0.109:8000/api
   📊 DB 주소: 192.168.0.109:3306

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**서버가 실행 중임을 확인:**
```bash
# 다른 터미널에서 실행
curl http://192.168.0.109:8000/api/freelancers
```

---

## 🌐 Step 3: 프론트엔드 시작

**새 터미널 창에서:**

```bash
cd /Users/doseunghyeon/developerApp/react/www.supermanger.com

# 의존성 설치 (첫 실행시만)
npm install

# 개발 서버 시작
npm run dev
```

**출력 예시:**
```
VITE v7.0.0  ready in XXX ms

➜  Local:   http://localhost:3000
➜  press h to show help
```

---

## ✅ Step 4: API 테스트

### 프론트엔드에서 API 테스트

브라우저에서 열기:
```
http://localhost:3000/api-test
```

**표시되는 정보:**
- ✅ 총 프리랜서 수
- ✅ 가용 상태별 분류
- ✅ 프리랜서 카드 목록
- ✅ 스킬, 경력, 시급 정보

---

## 📚 API 엔드포인트

### 목록 조회

```bash
curl "http://192.168.0.109:8000/api/freelancers?page=1&limit=20"

응답:
{
  "success": true,
  "message": "프리랜서 목록 조회 성공",
  "data": {
    "data": [...],
    "total": 8,
    "page": 1,
    "limit": 20,
    "totalPages": 1
  }
}
```

### 상세 조회

```bash
curl "http://192.168.0.109:8000/api/freelancers/{freelancer_id}"

응답:
{
  "success": true,
  "message": "프리랜서 조회 성공",
  "data": {
    "id": "...",
    "name": "김준호",
    "email": "junho.kim@example.com",
    "experience": 5,
    "hourlyRate": 50000,
    "skills": [...]
  }
}
```

### 생성

```bash
curl -X POST http://192.168.0.109:8000/api/freelancers \
  -H "Content-Type: application/json" \
  -d '{
    "name": "홍길동",
    "email": "hong@example.com",
    "phone": "010-1234-5678",
    "experience": 5,
    "hourlyRate": 50000,
    "availability": "available",
    "bio": "React 개발자입니다",
    "skillIds": ["react", "nodejs", "typescript"]
  }'
```

### 수정

```bash
curl -X PUT http://192.168.0.109:8000/api/freelancers/{id} \
  -H "Content-Type: application/json" \
  -d '{
    "experience": 6,
    "hourlyRate": 60000
  }'
```

### 삭제

```bash
curl -X DELETE http://192.168.0.109:8000/api/freelancers/{id}
```

### 스킬 목록

```bash
curl "http://192.168.0.109:8000/api/freelancers/skills"
```

---

## 🧪 테스트 데이터

### 생성된 스킬 (30개)

**Frontend** (8개)
- React, Vue, Angular, TypeScript, JavaScript, HTML5, CSS3, Tailwind CSS

**Backend** (7개)
- Node.js, Python, Java, .NET, PHP, Go, Rust

**Database** (4개)
- MySQL, PostgreSQL, MongoDB, Redis

**DevOps** (7개)
- Docker, Kubernetes, AWS, Google Cloud, Azure, Jenkins, GitLab CI/CD

**Design** (4개)
- Figma, UI/UX Design, Photoshop, Illustrator

### 생성된 프리랜서 (8명)

| 이름 | 경력 | 시급 | 상태 | 스킬 |
|------|------|------|------|------|
| 김준호 | 5년 | ₩50,000 | 가능 | React, TypeScript, Node.js |
| 이수영 | 7년 | ₩60,000 | 가능 | Python, Node.js, React |
| 박민준 | 3년 | ₩35,000 | 바쁨 | JavaScript, React, CSS3 |
| 최지은 | 6년 | ₩55,000 | 가능 | MySQL, PostgreSQL, MongoDB |
| 정호준 | 8년 | ₩70,000 | 가능 | Docker, Kubernetes, AWS |
| 유명희 | 4년 | ₩45,000 | 가능 | Figma, UI/UX, Photoshop |
| 한성호 | 9년 | ₩75,000 | 바쁨 | Java, Node.js, MySQL |
| 윤지수 | 2년 | ₩30,000 | 가능 | Vue, TypeScript, Tailwind |

---

## 🎯 주요 기능 확인

### 1️⃣ 인력목록 페이지

```
URL: http://localhost:3000/freelancers
기능:
├─ 프리랜서 카드/테이블 뷰 전환
├─ 검색 (이름, 이메일, 스킬)
├─ 필터링 (스킬, 가용상태, 경력, 시급)
├─ 정렬 (이름, 경력, 시급, 평점)
└─ 페이지네이션
```

### 2️⃣ 인력등록 페이지

```
URL: http://localhost:3000/freelancers/new
기능:
├─ 기본 정보 (이름, 이메일, 전화)
├─ 프로필 (프로필 사진, 소개)
├─ 경력 정보 (경력년수, 시급)
├─ 스킬 선택 (복수 선택)
└─ 가용상태 설정
```

### 3️⃣ API 테스트 페이지

```
URL: http://localhost:3000/api-test
기능:
├─ 실시간 API 호출 테스트
├─ 프리랜서 목록 표시
├─ 통계 정보 표시
└─ 서버 연결 상태 확인
```

---

## ⚙️ 환경 설정

### 프론트엔드 (.env.local)

```env
VITE_API_BASE_URL=http://192.168.0.109:8000/api
VITE_APP_NAME=SuperManager
VITE_APP_VERSION=0.1.0
VITE_ENV=development
VITE_DEBUG=true
VITE_DEFAULT_LOCALE=ko
```

### 백엔드 (.env)

```env
DB_HOST=192.168.0.109
DB_PORT=3306
DB_USER=joopok
DB_PASSWORD=~Asy10131227
DB_NAME=supermanager

FLASK_ENV=development
FLASK_DEBUG=True
API_PORT=8000
API_HOST=0.0.0.0
```

---

## 🐛 트러블슈팅

### 문제: "데이터베이스 연결 실패"

```
❌ pymysql.err.OperationalError: (1045, "Access denied for user 'joopok'@'192.168.0.109'")
```

**해결 방법:**
```bash
# 1. MariaDB 연결 테스트
mysql -h 192.168.0.109 -u joopok -p'~Asy10131227'

# 2. .env 파일의 DB 정보 확인
cat .env | grep DB_

# 3. MySQL 서버 상태 확인
# Windows: services.msc에서 MySQL 재시작
# macOS: brew services restart mariadb
```

### 문제: "CORS 오류"

```
❌ Access to XMLHttpRequest at 'http://192.168.0.109:8000/api/freelancers'
   from origin 'http://localhost:3000' has been blocked by CORS policy
```

**해결 방법:**
```bash
# 1. Flask에서 CORS 활성화 확인 (이미 적용됨)
# 2. 프론트엔드 .env.local에서 API_BASE_URL 확인
VITE_API_BASE_URL=http://192.168.0.109:8000/api

# 3. 브라우저 개발자 도구에서 실제 요청 URL 확인
```

### 문제: "포트 8000 사용 중"

```
❌ Address already in use
```

**해결 방법:**
```bash
# 1. 포트 8000을 사용 중인 프로세스 찾기
lsof -i :8000

# 2. 프로세스 종료
kill -9 <PID>

# 3. 다른 포트 사용 (선택사항)
API_PORT=8001 python app.py
```

---

## 📊 데이터베이스 스키마

### Freelancer 테이블

```sql
CREATE TABLE freelancer (
  id VARCHAR(36) PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(120) UNIQUE NOT NULL,
  phone VARCHAR(20) NOT NULL,
  experience INTEGER DEFAULT 0,
  hourly_rate INTEGER DEFAULT 0,
  avatar VARCHAR(500),
  bio TEXT,
  availability VARCHAR(20) DEFAULT 'available',
  rating FLOAT DEFAULT 0.0,
  review_count INTEGER DEFAULT 0,
  portfolio JSON,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX (email),
  INDEX (name)
);
```

### Skill 테이블

```sql
CREATE TABLE skill (
  id VARCHAR(36) PRIMARY KEY,
  name VARCHAR(100) UNIQUE NOT NULL,
  category VARCHAR(50) NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Freelancer-Skill 관계 테이블

```sql
CREATE TABLE freelancer_skill (
  freelancer_id VARCHAR(36) NOT NULL,
  skill_id VARCHAR(36) NOT NULL,
  PRIMARY KEY (freelancer_id, skill_id),
  FOREIGN KEY (freelancer_id) REFERENCES freelancer(id),
  FOREIGN KEY (skill_id) REFERENCES skill(id)
);
```

---

## 🔗 파일 구조

```
Frontend: /Users/doseunghyeon/developerApp/react/www.supermanger.com/
├─ src/
│  ├─ pages/freelancers/
│  │  ├─ FreelancerListPage.tsx       # 목록 페이지
│  │  ├─ FreelancerFormPage.tsx       # 등록/수정 페이지
│  │  └─ FreelancerDetailPage.tsx     # 상세 페이지
│  ├─ components/
│  │  ├─ freelancer/
│  │  │  ├─ FreelancerCard.tsx
│  │  │  ├─ FreelancerTable.tsx
│  │  │  └─ SkillSelector.tsx
│  │  └─ api-test/
│  │     └─ ApiTestPage.tsx           # API 테스트 페이지
│  ├─ services/
│  │  └─ freelancerService.ts         # API 호출 서비스
│  ├─ store/
│  │  └─ freelancerStore.ts           # Zustand 상태 관리
│  └─ types/
│     └─ freelancer.ts                # 타입 정의
└─ .env.local                          # 환경변수

Backend: /Users/doseunghyeon/developerApp/python/www.supermanger.com/
├─ app/
│  ├─ models/
│  │  └─ freelancer.py                # DB 모델
│  ├─ schemas/
│  │  └─ freelancer_schema.py         # 검증 스키마
│  ├─ services/
│  │  └─ freelancer_service.py        # 비즈니스 로직
│  ├─ routes/
│  │  └─ freelancer_routes.py         # API 라우트
│  ├─ __init__.py
│  ├─ db.py
│  └─ utils.py
├─ config.py                           # Flask 설정
├─ app.py                              # 진입점
├─ setup.py                            # 초기화 스크립트
├─ run_server.sh                       # 실행 스크립트
├─ requirements.txt                    # 의존성
├─ .env                                # 환경변수
└─ README.md                           # 상세 문서
```

---

## 📝 다음 단계

### 진행 상황
- ✅ 인력목록 화면 (CRUD 완료)
- ✅ 인력등록 화면 (CRUD 완료)
- ✅ API 테스트 페이지
- ✅ 데이터베이스 초기화
- ✅ 테스트 데이터 생성

### 앞으로 할 일
- 🔄 인력상세 페이지 완성
- 🔄 리뷰/평점 기능
- 🔄 포트폴리오 관리
- 🔄 다른 모듈 구현 (프로젝트, 장비, 업무 등)

---

## 💡 팁

### 빠른 테스트

```bash
# 1. 백엔드만 테스트 (API)
curl "http://192.168.0.109:8000/api/freelancers"

# 2. 데이터베이스 확인
mysql -h 192.168.0.109 -u joopok -p'~Asy10131227' supermanager
> SELECT COUNT(*) FROM freelancer;
> SELECT * FROM freelancer LIMIT 1;

# 3. 프론트엔드 콘솔 로그 확인
# 브라우저 개발자 도구 → Console 탭
```

### 로그 확인

```bash
# Flask 서버 로그 (실시간)
# 터미널에서 직접 확인

# 프론트엔드 콘솔 로그
# 브라우저 개발자 도구 → Console 탭

# API 응답 검사
# 브라우저 개발자 도구 → Network 탭
```

---

## 🎉 축하합니다!

이제 완전한 인력관리 CRUD 시스템이 준비되었습니다!

**문의 사항이 있으시면:**
- 📖 README.md 참고
- 🔍 CLAUDE.md에서 환경 설정 확인
- 💻 프론트엔드: http://localhost:3000
- 🌐 백엔드: http://192.168.0.109:8000/api
