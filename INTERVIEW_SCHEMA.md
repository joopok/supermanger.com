# 면접평가 시스템 - 3NF 정규화 스키마

## 개요

면접평가표의 모든 데이터를 분석하여 **3NF(Third Normal Form) 정규화**를 기반으로 설계된 데이터베이스 스키마입니다.

### 정규화 목표

- **1NF (First Normal Form)**: 원자적 값만 저장 (JSON 제거 → 별도 테이블)
- **2NF (Second Normal Form)**: 부분 함수 종속성 제거 (비키 속성이 후보 키 전체에 종속)
- **3NF (Third Normal Form)**: 이행 함수 종속성 제거 (비키 속성이 다른 비키 속성에 종속되지 않음)

---

## 데이터베이스 스키마

### 마스터 데이터 테이블

#### 1. `interview_category` - 평가 카테고리 (마스터)
면접 평가의 주요 카테고리를 정의합니다.

```sql
CREATE TABLE interview_category (
  id VARCHAR(36) PRIMARY KEY,
  name VARCHAR(100) UNIQUE NOT NULL,           -- 기술역량, 포트폴리오, 커뮤니케이션, 업무방식
  description TEXT,
  weight INTEGER DEFAULT 1,                    -- 가중치
  max_score FLOAT DEFAULT 5.0,                 -- 최대 점수
  `order` INTEGER NOT NULL,                    -- 정렬 순서
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**포함된 카테고리:**
1. 기술 역량 & 문제해결 (weight=20)
2. 포트폴리오/기여 검증 (weight=20)
3. 커뮤니케이션 & 일정관리 (weight=20)
4. 계약/업무 방식 & 품질보증 (weight=20)

#### 2. `interview_question` - 핵심 질문 (1NF - 원자화)
각 카테고리에 대한 핵심 질문을 저장합니다.

```sql
CREATE TABLE interview_question (
  id VARCHAR(36) PRIMARY KEY,
  category_id VARCHAR(36) NOT NULL,
  question_text TEXT NOT NULL,
  `order` INTEGER NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (category_id) REFERENCES interview_category (id) ON DELETE CASCADE
);
```

#### 3. `interview_checkpoint` - 체크포인트 (1NF - 원자화, 3NF)
각 카테고리의 평가 항목들을 원자적 단위로 저장합니다.

```sql
CREATE TABLE interview_checkpoint (
  id VARCHAR(36) PRIMARY KEY,
  category_id VARCHAR(36) NOT NULL,
  checkpoint_text TEXT NOT NULL,              -- 예: "사용 스택의 선택 이유와 대안 설명"
  `order` INTEGER NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (category_id) REFERENCES interview_category (id) ON DELETE CASCADE,
  INDEX (category_id)
);
```

#### 4. `interview_red_flag` - 레드플래그 (1NF - 원자화, 3NF)
주의해야 할 항목들을 저장합니다.

```sql
CREATE TABLE interview_red_flag (
  id VARCHAR(36) PRIMARY KEY,
  category_id VARCHAR(36) NOT NULL,
  flag_text TEXT NOT NULL,                    -- 예: "추상적 답변만 함"
  severity VARCHAR(20),                       -- low, medium, high, critical
  `order` INTEGER NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (category_id) REFERENCES interview_category (id) ON DELETE CASCADE,
  INDEX (category_id)
);
```

### 거래 테이블 (Transaction Tables)

#### 5. `interview_evaluation` - 면접 평가 기록 (2NF)
각 프리랜서에 대한 면접 평가 기록입니다.

```sql
CREATE TABLE interview_evaluation (
  id VARCHAR(36) PRIMARY KEY,
  freelancer_id VARCHAR(36) NOT NULL,
  interviewer_name VARCHAR(100),              -- 평가자명
  project_name VARCHAR(200),                  -- 관련 프로젝트명
  total_score FLOAT,                          -- 총점 (0-100)
  recommendation VARCHAR(50),                 -- recommend, not_recommend, pending
  notes TEXT,
  evaluated_at DATETIME NOT NULL,             -- 평가 날짜
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (freelancer_id) REFERENCES freelancer (id) ON DELETE CASCADE,
  INDEX (freelancer_id),
  INDEX (evaluated_at)
);
```

#### 6. `interview_category_score` - 카테고리별 점수 (3NF)
각 평가에서 각 카테고리의 점수를 저장합니다.

```sql
CREATE TABLE interview_category_score (
  id VARCHAR(36) PRIMARY KEY,
  evaluation_id VARCHAR(36) NOT NULL,
  category_id VARCHAR(36) NOT NULL,
  score FLOAT NOT NULL,                       -- 1.0, 3.0, 5.0
  score_label VARCHAR(20) NOT NULL,           -- 하(1), 중(3), 상(5)
  checked_count INTEGER DEFAULT 0,            -- 체크된 항목 수
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (evaluation_id) REFERENCES interview_evaluation (id) ON DELETE CASCADE,
  FOREIGN KEY (category_id) REFERENCES interview_category (id) ON DELETE CASCADE,
  INDEX (evaluation_id),
  INDEX (category_id)
);
```

#### 7. `interview_evaluation_result` - 체크포인트 평가 결과 (3NF)
각 평가에서 체크포인트의 확인 여부를 저장합니다.

```sql
CREATE TABLE interview_evaluation_result (
  id VARCHAR(36) PRIMARY KEY,
  evaluation_id VARCHAR(36) NOT NULL,
  checkpoint_id VARCHAR(36) NOT NULL,
  is_checked BOOLEAN DEFAULT FALSE,
  notes TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (evaluation_id) REFERENCES interview_evaluation (id) ON DELETE CASCADE,
  FOREIGN KEY (checkpoint_id) REFERENCES interview_checkpoint (id) ON DELETE CASCADE,
  UNIQUE KEY uq_eval_checkpoint (evaluation_id, checkpoint_id)
);
```

#### 8. `interview_red_flag_finding` - 레드플래그 발견 (3NF)
각 평가에서 발견된 레드플래그를 저장합니다.

```sql
CREATE TABLE interview_red_flag_finding (
  id VARCHAR(36) PRIMARY KEY,
  evaluation_id VARCHAR(36) NOT NULL,
  red_flag_id VARCHAR(36) NOT NULL,
  is_found BOOLEAN DEFAULT FALSE,
  severity_actual VARCHAR(20),                -- 실제 심각도
  evidence TEXT,                              -- 근거/설명
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (evaluation_id) REFERENCES interview_evaluation (id) ON DELETE CASCADE,
  FOREIGN KEY (red_flag_id) REFERENCES interview_red_flag (id) ON DELETE CASCADE,
  UNIQUE KEY uq_eval_red_flag (evaluation_id, red_flag_id)
);
```

---

## API 엔드포인트

### 카테고리 관리

```
GET    /api/interviews/categories                    # 카테고리 목록
GET    /api/interviews/categories/<id>               # 카테고리 상세
POST   /api/interviews/categories                    # 카테고리 생성
PUT    /api/interviews/categories/<id>               # 카테고리 수정
DELETE /api/interviews/categories/<id>               # 카테고리 삭제
```

### 질문 관리

```
GET    /api/interviews/categories/<id>/questions     # 카테고리별 질문 조회
POST   /api/interviews/questions                     # 질문 생성
PUT    /api/interviews/questions/<id>                # 질문 수정
DELETE /api/interviews/questions/<id>                # 질문 삭제
```

### 체크포인트 관리

```
GET    /api/interviews/categories/<id>/checkpoints   # 카테고리별 체크포인트 조회
POST   /api/interviews/checkpoints                   # 체크포인트 생성
PUT    /api/interviews/checkpoints/<id>              # 체크포인트 수정
DELETE /api/interviews/checkpoints/<id>              # 체크포인트 삭제
```

### 레드플래그 관리

```
GET    /api/interviews/categories/<id>/red-flags     # 카테고리별 레드플래그 조회
POST   /api/interviews/red-flags                     # 레드플래그 생성
PUT    /api/interviews/red-flags/<id>                # 레드플래그 수정
DELETE /api/interviews/red-flags/<id>                # 레드플래그 삭제
```

### 면접 평가 CRUD

```
GET    /api/interviews/evaluations                   # 평가 목록 (필터 가능)
GET    /api/interviews/evaluations/<id>              # 평가 상세
POST   /api/interviews/evaluations                   # 평가 생성
PUT    /api/interviews/evaluations/<id>              # 평가 수정
DELETE /api/interviews/evaluations/<id>              # 평가 삭제
```

### 평가 점수 관리

```
POST   /api/interviews/evaluations/<id>/category-scores/<catId>        # 카테고리 점수 추가/수정
PUT    /api/interviews/evaluations/<id>/category-scores/<catId>        # 카테고리 점수 수정
```

### 체크포인트 결과

```
POST   /api/interviews/evaluations/<id>/checkpoint-results             # 체크포인트 결과 추가
PUT    /api/interviews/evaluations/<id>/checkpoint-results/<checkId>   # 체크포인트 결과 수정
```

### 레드플래그 발견

```
POST   /api/interviews/evaluations/<id>/red-flag-findings              # 레드플래그 발견 추가
PUT    /api/interviews/evaluations/<id>/red-flag-findings/<flagId>     # 레드플래그 발견 수정
```

### 스코어 계산 및 추천

```
POST   /api/interviews/evaluations/<id>/calculate-score               # 총점 계산
POST   /api/interviews/evaluations/<id>/set-recommendation            # 추천 여부 설정
```

---

## 사용 예시

### 1. 면접 평가 생성

```python
# 프리랜서에 대한 새로운 면접 평가 기록 생성
POST /api/interviews/evaluations
{
  "freelancerId": "freelancer-uuid",
  "interviewerName": "김평가",
  "projectName": "신한은행 프로젝트",
  "notes": "전반적으로 우수함"
}
```

### 2. 카테고리 점수 추가

```python
# 기술역량 카테고리에 "상(5)" 점수 추가
POST /api/interviews/evaluations/<eval-id>/category-scores/<cat-id>
{
  "categoryId": "tech-category-id",
  "score": 5.0,
  "scoreLabel": "상(5)",
  "checkedCount": 3
}
```

### 3. 체크포인트 결과 추가

```python
# 체크포인트 확인 여부 기록
POST /api/interviews/evaluations/<eval-id>/checkpoint-results
{
  "checkpointId": "checkpoint-id",
  "isChecked": true,
  "notes": "스택 선택 이유를 명확히 설명함"
}
```

### 4. 레드플래그 발견 추가

```python
# 레드플래그 발견 기록
POST /api/interviews/evaluations/<eval-id>/red-flag-findings
{
  "redFlagId": "red-flag-id",
  "isFound": false,
  "severityActual": null,
  "evidence": "테스트 코드가 잘 작성되어 있음"
}
```

### 5. 총점 계산 및 추천 설정

```python
# 총점 자동 계산 (모든 카테고리 점수 기반)
POST /api/interviews/evaluations/<eval-id>/calculate-score

# 추천 여부 설정
POST /api/interviews/evaluations/<eval-id>/set-recommendation
{
  "recommendation": "recommend",
  "notes": "모든 항목에서 우수한 점수 획득"
}
```

---

## 초기화 및 설정

### 마스터 데이터 초기화

```bash
python init_interview.py
```

실행 결과:
- 카테고리 4개 생성
- 질문 4개 생성
- 체크포인트 13개 생성
- 레드플래그 13개 생성

### 추천 기준

- **최소 65점 이상**: 자동 추천 대상
- **예외 사항**: 현재 프로젝트 특성을 잘 알고 있는 경우 예외로 처리 (문의 후 진행)

---

## 정규화 이점

### 1. 데이터 무결성
- 중복 제거로 인한 데이터 일관성 보장
- 이상 현상(anomaly) 제거

### 2. 유지보수성
- 각 테이블이 단일 책임을 가짐
- 변경 시 영향 범위 최소화

### 3. 쿼리 효율성
- 불필요한 JOIN 감소
- 인덱싱 최적화

### 4. 확장성
- 새로운 카테고리/체크포인트 추가 용이
- 평가 기준 변경 용이

---

## 관련 파일

### 모델 (Models)
- `app/models/freelancer.py` - 모든 모델 정의

### 서비스 (Services)
- `app/services/interview_service.py` - 모든 CRUD 로직

### 라우트 (Routes)
- `app/routes/interview_routes.py` - 모든 API 엔드포인트

### 초기화
- `init_interview.py` - 마스터 데이터 초기화 스크립트

---

## 신뢰성 특성 (Backend Reliability)

### 데이터 무결성
- Foreign Key Constraints with CASCADE delete
- Unique Constraints for preventing duplicates
- Transaction support for multi-step operations

### 에러 처리
- 명확한 예외 메시지
- HTTP 상태 코드 준수
- 유효성 검사 (Validation)

### 확장성
- UUID 기반 식별자로 분산 시스템 대응
- 마스터-상세 데이터 분리로 독립적 관리
- 평가 결과와 마스터 데이터 분리

---

## 성능 고려사항

### 인덱싱
```sql
CREATE INDEX ix_interview_category_score_evaluation_id ON interview_category_score(evaluation_id);
CREATE INDEX ix_interview_evaluation_freelancer_id ON interview_evaluation(freelancer_id);
CREATE INDEX ix_interview_evaluation_evaluated_at ON interview_evaluation(evaluated_at);
```

### 쿼리 최적화
- 페이지네이션 기본 지원 (limit, offset)
- 정렬 옵션 지원
- 필터링 옵션 지원

---

## 마이그레이션 전략 (기존 데이터 마이그레이션)

현재 JSON 형식의 포트폴리오 데이터가 있다면:

```python
# 기존 JSON 데이터를 PortfolioItem 테이블로 마이그레이션
for freelancer in Freelancer.query.all():
    for item in freelancer.portfolio:
        PortfolioItem.create(
            freelancer_id=freelancer.id,
            title=item['title'],
            description=item.get('description'),
            # ... 기타 필드
        )
```
