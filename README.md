# SuperManager Backend (Python Flask)

프리랜서 관리 시스템의 백엔드 API 서버입니다.

## 🏗️ 프로젝트 구조

```
app/
├── __init__.py           # Flask 애플리케이션 팩토리
├── db.py                 # SQLAlchemy 초기화
├── utils.py              # 유틸리티 함수
├── models/               # 데이터베이스 모델
│   ├── __init__.py
│   └── freelancer.py     # Freelancer, Skill 모델
├── schemas/              # Marshmallow 스키마
│   ├── __init__.py
│   └── freelancer_schema.py
├── services/             # 비즈니스 로직
│   ├── __init__.py
│   └── freelancer_service.py
└── routes/               # API 라우트
    ├── __init__.py
    └── freelancer_routes.py

app.py                     # 애플리케이션 진입점
config.py                  # Flask 설정
requirements.txt           # Python 의존성
.env                       # 환경변수
init_skills.py            # 초기 스킬 데이터 생성
```

## 📋 설치 및 실행

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 환경변수 설정

`.env` 파일에서 데이터베이스 연결정보 확인:

```
DB_HOST=192.168.0.109
DB_PORT=3306
DB_USER=joopok
DB_PASSWORD=~Asy10131227
DB_NAME=supermanager
```

### 3. 데이터베이스 생성

```bash
# MySQL에서 데이터베이스 생성
mysql -h 192.168.0.109 -u joopok -p
> CREATE DATABASE supermanager CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. 초기 스킬 데이터 생성

```bash
python init_skills.py
```

### 5. 서버 실행

```bash
python app.py
```

서버가 실행되면:
- 🚀 API: http://localhost:8000
- 📊 Database: 192.168.0.109:3306/supermanager

## 📚 API 엔드포인트

### Freelancer Management

#### 목록 조회
```
GET /api/freelancers
Query Parameters:
  - page: 페이지 번호 (기본값: 1)
  - limit: 페이지당 항목 수 (기본값: 20)
  - search: 검색어 (이름, 이메일, 소개)
  - skills: 스킬 ID 배열 (예: skills=react&skills=nodejs)
  - availability: available | busy | unavailable
  - minRating: 최소 평점 (0-5)
  - minExperience: 최소 경력 (년)
  - maxHourlyRate: 최대 시급 (원)
  - sortBy: name | rating | experience | hourlyRate | createdAt (기본값: name)
  - sortOrder: asc | desc (기본값: asc)

Response:
{
  "success": true,
  "message": "프리랜서 목록 조회 성공",
  "data": {
    "data": [...],
    "total": 100,
    "page": 1,
    "limit": 20,
    "totalPages": 5
  }
}
```

#### 상세 조회
```
GET /api/freelancers/{freelancer_id}

Response:
{
  "success": true,
  "message": "프리랜서 조회 성공",
  "data": {
    "id": "...",
    "name": "...",
    "email": "...",
    ...
  }
}
```

#### 생성
```
POST /api/freelancers
Content-Type: application/json

Request Body:
{
  "name": "홍길동",
  "email": "hong@example.com",
  "phone": "010-1234-5678",
  "experience": 5,
  "hourlyRate": 50000,
  "availability": "available",
  "bio": "경력 5년의 React 개발자입니다",
  "avatar": "https://...",
  "skillIds": ["react", "nodejs", "typescript"]
}

Response:
{
  "success": true,
  "message": "프리랜서 등록 성공",
  "data": {...}
}
```

#### 수정
```
PUT /api/freelancers/{freelancer_id}
Content-Type: application/json

Request Body:
{
  "name": "홍길동",
  "experience": 6,
  "hourlyRate": 60000,
  "skillIds": ["react", "nodejs", "typescript", "python"]
}

Response:
{
  "success": true,
  "message": "프리랜서 정보 수정 성공",
  "data": {...}
}
```

#### 삭제
```
DELETE /api/freelancers/{freelancer_id}

Response:
{
  "success": true,
  "message": "프리랜서 삭제 성공"
}
```

### Skills

#### 스킬 목록 조회
```
GET /api/freelancers/skills

Response:
{
  "success": true,
  "message": "스킬 목록 조회 성공",
  "data": [
    {
      "id": "react",
      "name": "React",
      "category": "frontend"
    },
    ...
  ]
}
```

## 🛠️ 기술 스택

- **Framework**: Flask 3.0.0
- **ORM**: SQLAlchemy 3.1.1
- **Validation**: Marshmallow 3.20.1
- **Database**: MySQL/MariaDB
- **Python**: 3.9+

## 📝 데이터 모델

### Freelancer
```python
{
  "id": "uuid",
  "name": "이름",
  "email": "이메일",
  "phone": "전화번호",
  "experience": 5,  # 경력 년수
  "hourlyRate": 50000,  # 시급
  "avatar": "프로필 이미지 URL",
  "bio": "소개",
  "availability": "available|busy|unavailable",
  "rating": 4.5,
  "reviewCount": 10,
  "portfolio": [],
  "skills": [
    {
      "id": "react",
      "name": "React",
      "level": "advanced",
      "category": "frontend"
    }
  ],
  "createdAt": "2024-11-07T...",
  "updatedAt": "2024-11-07T..."
}
```

### Skill
```python
{
  "id": "skill-id",
  "name": "스킬명",
  "category": "frontend|backend|devops|design|other"
}
```

## 🔄 프론트엔드 연동

프론트엔드에서 다음과 같이 API를 호출합니다:

```typescript
// src/services/freelancerService.ts
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api'
});

export const freelancerService = {
  getList: (params) => api.get('/freelancers', { params }),
  getById: (id) => api.get(`/freelancers/${id}`),
  create: (data) => api.post('/freelancers', data),
  update: (id, data) => api.put(`/freelancers/${id}`, data),
  delete: (id) => api.delete(`/freelancers/${id}`),
  getSkills: () => api.get('/freelancers/skills'),
};
```

## 🧪 테스트

```bash
# 헬스 체크
curl http://localhost:8000/api/freelancers/health

# 프리랜서 목록 조회
curl "http://localhost:8000/api/freelancers?page=1&limit=20"

# 스킬 목록 조회
curl "http://localhost:8000/api/freelancers/skills"
```

## 📖 개발 가이드

### 새로운 엔드포인트 추가

1. `app/models/freelancer.py`에서 모델 정의
2. `app/schemas/freelancer_schema.py`에서 스키마 정의
3. `app/services/freelancer_service.py`에서 비즈니스 로직 구현
4. `app/routes/freelancer_routes.py`에서 라우트 정의

### 에러 처리

```python
from app.utils import handle_success, handle_error

# 성공
return handle_success(data, '메시지', 200)

# 실패
return handle_error('에러 메시지', 400)
```

## 🚀 배포

### Docker를 사용한 배포

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

```bash
docker build -t supermanager-backend .
docker run -p 8000:8000 --env-file .env supermanager-backend
```

## 📝 라이선스

이 프로젝트는 내부용입니다.
# supermanger.com
