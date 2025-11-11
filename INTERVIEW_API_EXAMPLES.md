# 면접평가 API 사용 예시

## 기본 설정

모든 요청에 `Content-Type: application/json` 헤더를 포함하세요.

```bash
BASE_URL="http://localhost:8000/api/interviews"
```

---

## 마스터 데이터 조회

### 1. 모든 카테고리 조회

```bash
curl -X GET "$BASE_URL/categories?page=1&limit=20&sortBy=order&sortOrder=asc"
```

**응답:**
```json
{
  "success": true,
  "message": "카테고리 목록 조회 성공",
  "data": {
    "items": [
      {
        "id": "cat-1",
        "name": "기술 역량 & 문제해결",
        "description": "최근 프로젝트에서 가장 어려웠던 기술 문제와 해결 과정",
        "weight": 20,
        "maxScore": 5.0,
        "order": 1
      },
      {
        "id": "cat-2",
        "name": "포트폴리오/기여 검증",
        "description": "포트폴리오에서 직접 구현한 부분과 기여도 검증",
        "weight": 20,
        "maxScore": 5.0,
        "order": 2
      }
    ],
    "total": 4,
    "page": 1,
    "limit": 20,
    "totalPages": 1
  }
}
```

### 2. 특정 카테고리의 체크포인트 조회

```bash
curl -X GET "$BASE_URL/categories/cat-1/checkpoints?page=1&limit=20"
```

**응답:**
```json
{
  "success": true,
  "message": "체크포인트 목록 조회 성공",
  "data": {
    "items": [
      {
        "id": "checkpoint-1",
        "categoryId": "cat-1",
        "checkpointText": "사용 스택의 선택 이유와 대안 설명",
        "order": 1
      },
      {
        "id": "checkpoint-2",
        "categoryId": "cat-1",
        "checkpointText": "설계·테스트·배포 흐름 이해",
        "order": 2
      },
      {
        "id": "checkpoint-3",
        "categoryId": "cat-1",
        "checkpointText": "성능/보안/확장성 고려",
        "order": 3
      }
    ],
    "total": 3,
    "page": 1,
    "limit": 20,
    "totalPages": 1
  }
}
```

### 3. 특정 카테고리의 레드플래그 조회

```bash
curl -X GET "$BASE_URL/categories/cat-1/red-flags?page=1&limit=20"
```

**응답:**
```json
{
  "success": true,
  "message": "레드플래그 목록 조회 성공",
  "data": {
    "items": [
      {
        "id": "flag-1",
        "categoryId": "cat-1",
        "flagText": "추상적 답변만 함",
        "severity": "high",
        "order": 1
      },
      {
        "id": "flag-2",
        "categoryId": "cat-1",
        "flagText": "테스트/모듈화 부재",
        "severity": "high",
        "order": 2
      }
    ],
    "total": 3,
    "page": 1,
    "limit": 20,
    "totalPages": 1
  }
}
```

---

## 면접 평가 CRUD

### 1. 면접 평가 생성

```bash
curl -X POST "$BASE_URL/evaluations" \
  -H "Content-Type: application/json" \
  -d '{
    "freelancerId": "freelancer-uuid-here",
    "interviewerName": "김평가",
    "projectName": "신한은행 슈퍼SOL",
    "notes": "전반적으로 우수한 기술 역량"
  }'
```

**응답:**
```json
{
  "success": true,
  "message": "평가 생성 성공",
  "data": {
    "id": "eval-uuid",
    "freelancerId": "freelancer-uuid-here",
    "interviewerName": "김평가",
    "projectName": "신한은행 슈퍼SOL",
    "totalScore": null,
    "recommendation": null,
    "notes": "전반적으로 우수한 기술 역량",
    "evaluatedAt": "2025-11-07T21:10:00",
    "createdAt": "2025-11-07T21:10:00",
    "updatedAt": "2025-11-07T21:10:00",
    "categoryScores": [],
    "checkpointResults": [],
    "redFlagFindings": []
  }
}
```

### 2. 평가 목록 조회

```bash
# 특정 프리랜서의 평가 조회
curl -X GET "$BASE_URL/evaluations?freelancerId=freelancer-uuid&page=1&limit=20&sortBy=evaluated_at&sortOrder=desc"

# 추천 대상만 조회
curl -X GET "$BASE_URL/evaluations?recommendation=recommend&minScore=65&page=1&limit=20"
```

**응답:**
```json
{
  "success": true,
  "message": "평가 목록 조회 성공",
  "data": {
    "items": [
      {
        "id": "eval-1",
        "freelancerId": "freelancer-1",
        "interviewerName": "김평가",
        "projectName": "신한은행",
        "totalScore": 78.5,
        "recommendation": "recommend",
        "notes": "우수함",
        "evaluatedAt": "2025-11-07T21:10:00",
        "createdAt": "2025-11-07T21:10:00",
        "updatedAt": "2025-11-07T21:15:00"
      }
    ],
    "total": 1,
    "page": 1,
    "limit": 20,
    "totalPages": 1
  }
}
```

### 3. 평가 상세 조회

```bash
curl -X GET "$BASE_URL/evaluations/eval-uuid"
```

**응답:**
```json
{
  "success": true,
  "message": "평가 조회 성공",
  "data": {
    "id": "eval-uuid",
    "freelancerId": "freelancer-uuid",
    "interviewerName": "김평가",
    "projectName": "신한은행 슈퍼SOL",
    "totalScore": 78.5,
    "recommendation": "recommend",
    "notes": "전반적으로 우수함",
    "evaluatedAt": "2025-11-07T21:10:00",
    "createdAt": "2025-11-07T21:10:00",
    "updatedAt": "2025-11-07T21:20:00",
    "categoryScores": [
      {
        "id": "score-1",
        "evaluationId": "eval-uuid",
        "categoryId": "cat-1",
        "categoryName": "기술 역량 & 문제해결",
        "score": 5.0,
        "scoreLabel": "상(5)",
        "checkedCount": 3
      }
    ],
    "checkpointResults": [
      {
        "id": "result-1",
        "evaluationId": "eval-uuid",
        "checkpointId": "checkpoint-1",
        "checkpointText": "사용 스택의 선택 이유와 대안 설명",
        "isChecked": true,
        "notes": "명확하게 설명함",
        "createdAt": "2025-11-07T21:12:00",
        "updatedAt": "2025-11-07T21:12:00"
      }
    ],
    "redFlagFindings": [
      {
        "id": "finding-1",
        "evaluationId": "eval-uuid",
        "redFlagId": "flag-1",
        "flagText": "추상적 답변만 함",
        "isFound": false,
        "severityActual": null,
        "evidence": "구체적으로 기술 스택과 아키텍처를 설명함",
        "createdAt": "2025-11-07T21:12:00",
        "updatedAt": "2025-11-07T21:12:00"
      }
    ]
  }
}
```

---

## 평가 점수 관리

### 1. 카테고리 점수 추가/수정

```bash
# 점수 추가
curl -X POST "$BASE_URL/evaluations/eval-uuid/category-scores/cat-1" \
  -H "Content-Type: application/json" \
  -d '{
    "categoryId": "cat-1",
    "score": 5.0,
    "scoreLabel": "상(5)",
    "checkedCount": 3
  }'

# 점수 수정
curl -X PUT "$BASE_URL/evaluations/eval-uuid/category-scores/cat-1" \
  -H "Content-Type: application/json" \
  -d '{
    "score": 3.0,
    "scoreLabel": "중(3)",
    "checkedCount": 2
  }'
```

**응답:**
```json
{
  "success": true,
  "message": "카테고리 점수 추가 성공",
  "data": {
    "id": "score-uuid",
    "evaluationId": "eval-uuid",
    "categoryId": "cat-1",
    "categoryName": "기술 역량 & 문제해결",
    "score": 5.0,
    "scoreLabel": "상(5)",
    "checkedCount": 3
  }
}
```

---

## 체크포인트 평가 결과

### 1. 체크포인트 결과 추가/수정

```bash
# 체크포인트 결과 추가
curl -X POST "$BASE_URL/evaluations/eval-uuid/checkpoint-results" \
  -H "Content-Type: application/json" \
  -d '{
    "checkpointId": "checkpoint-1",
    "isChecked": true,
    "notes": "사용 스택 선택 이유를 명확히 설명함"
  }'

# 체크포인트 결과 수정
curl -X PUT "$BASE_URL/evaluations/eval-uuid/checkpoint-results/checkpoint-1" \
  -H "Content-Type: application/json" \
  -d '{
    "isChecked": true,
    "notes": "업데이트된 평가 노트"
  }'
```

**응답:**
```json
{
  "success": true,
  "message": "체크포인트 결과 추가 성공",
  "data": {
    "id": "result-uuid",
    "evaluationId": "eval-uuid",
    "checkpointId": "checkpoint-1",
    "checkpointText": "사용 스택의 선택 이유와 대안 설명",
    "isChecked": true,
    "notes": "사용 스택 선택 이유를 명확히 설명함",
    "createdAt": "2025-11-07T21:12:00",
    "updatedAt": "2025-11-07T21:12:00"
  }
}
```

---

## 레드플래그 발견

### 1. 레드플래그 발견 추가/수정

```bash
# 레드플래그 발견 추가
curl -X POST "$BASE_URL/evaluations/eval-uuid/red-flag-findings" \
  -H "Content-Type: application/json" \
  -d '{
    "redFlagId": "flag-1",
    "isFound": false,
    "severityActual": null,
    "evidence": "추상적 답변이 아님 - 구체적으로 설명함"
  }'

# 레드플래그 발견 수정
curl -X PUT "$BASE_URL/evaluations/eval-uuid/red-flag-findings/flag-1" \
  -H "Content-Type: application/json" \
  -d '{
    "isFound": true,
    "severityActual": "high",
    "evidence": "일부 기술에 대해서만 추상적으로 답변함"
  }'
```

**응답:**
```json
{
  "success": true,
  "message": "레드플래그 발견 추가 성공",
  "data": {
    "id": "finding-uuid",
    "evaluationId": "eval-uuid",
    "redFlagId": "flag-1",
    "flagText": "추상적 답변만 함",
    "isFound": false,
    "severityActual": null,
    "evidence": "추상적 답변이 아님 - 구체적으로 설명함",
    "createdAt": "2025-11-07T21:12:00",
    "updatedAt": "2025-11-07T21:12:00"
  }
}
```

---

## 점수 계산 및 추천

### 1. 총점 자동 계산

```bash
curl -X POST "$BASE_URL/evaluations/eval-uuid/calculate-score" \
  -H "Content-Type: application/json"
```

**계산 방식:**
```
총점 = (각 카테고리 점수 합) / (카테고리 수) / 5.0 × 100
예: (5.0 + 5.0 + 3.0 + 5.0) / 4 / 5.0 × 100 = 85.0
```

**응답:**
```json
{
  "success": true,
  "message": "총점 계산 완료",
  "data": {
    "totalScore": 85.0
  }
}
```

### 2. 추천 여부 설정

```bash
curl -X POST "$BASE_URL/evaluations/eval-uuid/set-recommendation" \
  -H "Content-Type: application/json" \
  -d '{
    "recommendation": "recommend",
    "notes": "모든 카테고리에서 우수한 점수 획득. 신한은행 프로젝트에 적합"
  }'
```

**응답:**
```json
{
  "success": true,
  "message": "추천 상태 설정 완료",
  "data": {
    "id": "eval-uuid",
    "freelancerId": "freelancer-uuid",
    "interviewerName": "김평가",
    "projectName": "신한은행 슈퍼SOL",
    "totalScore": 85.0,
    "recommendation": "recommend",
    "notes": "모든 카테고리에서 우수한 점수 획득. 신한은행 프로젝트에 적합",
    "evaluatedAt": "2025-11-07T21:10:00",
    "createdAt": "2025-11-07T21:10:00",
    "updatedAt": "2025-11-07T21:22:00"
  }
}
```

---

## 전체 평가 흐름 예시

### Step 1: 평가 생성

```bash
EVAL_ID=$(curl -X POST "$BASE_URL/evaluations" \
  -H "Content-Type: application/json" \
  -d '{
    "freelancerId": "freelancer-123",
    "interviewerName": "홍길동",
    "projectName": "신한은행",
    "notes": "초기 평가"
  }' | jq -r '.data.id')
```

### Step 2: 각 카테고리 점수 추가

```bash
# 기술역량 점수 (상)
curl -X POST "$BASE_URL/evaluations/$EVAL_ID/category-scores/cat-1" \
  -H "Content-Type: application/json" \
  -d '{"categoryId": "cat-1", "score": 5.0, "scoreLabel": "상(5)", "checkedCount": 3}'

# 포트폴리오 점수 (상)
curl -X POST "$BASE_URL/evaluations/$EVAL_ID/category-scores/cat-2" \
  -H "Content-Type: application/json" \
  -d '{"categoryId": "cat-2", "score": 5.0, "scoreLabel": "상(5)", "checkedCount": 3}'

# 커뮤니케이션 점수 (중)
curl -X POST "$BASE_URL/evaluations/$EVAL_ID/category-scores/cat-3" \
  -H "Content-Type: application/json" \
  -d '{"categoryId": "cat-3", "score": 3.0, "scoreLabel": "중(3)", "checkedCount": 2}'

# 계약/업무 점수 (상)
curl -X POST "$BASE_URL/evaluations/$EVAL_ID/category-scores/cat-4" \
  -H "Content-Type: application/json" \
  -d '{"categoryId": "cat-4", "score": 5.0, "scoreLabel": "상(5)", "checkedCount": 4}'
```

### Step 3: 체크포인트 결과 추가

```bash
# 기술역량 체크포인트
curl -X POST "$BASE_URL/evaluations/$EVAL_ID/checkpoint-results" \
  -H "Content-Type: application/json" \
  -d '{"checkpointId": "checkpoint-1", "isChecked": true, "notes": "명확함"}'

# ... 더 많은 체크포인트 추가
```

### Step 4: 레드플래그 발견 기록

```bash
curl -X POST "$BASE_URL/evaluations/$EVAL_ID/red-flag-findings" \
  -H "Content-Type: application/json" \
  -d '{"redFlagId": "flag-1", "isFound": false, "evidence": "우수함"}'

# ... 더 많은 레드플래그 기록
```

### Step 5: 총점 계산

```bash
curl -X POST "$BASE_URL/evaluations/$EVAL_ID/calculate-score" \
  -H "Content-Type: application/json"
```

### Step 6: 추천 여부 결정

```bash
curl -X POST "$BASE_URL/evaluations/$EVAL_ID/set-recommendation" \
  -H "Content-Type: application/json" \
  -d '{"recommendation": "recommend", "notes": "우수 후보"}'
```

---

## 에러 응답 예시

### 잘못된 요청

```bash
curl -X POST "$BASE_URL/evaluations" \
  -H "Content-Type: application/json" \
  -d '{"interviewerName": "김평가"}'  # freelancerId 누락
```

**응답:**
```json
{
  "success": false,
  "message": "프리랜서 ID는 필수입니다",
  "data": null
}
```

### 존재하지 않는 리소스

```bash
curl -X GET "$BASE_URL/evaluations/invalid-id"
```

**응답:**
```json
{
  "success": false,
  "message": "평가를 찾을 수 없습니다: invalid-id",
  "data": null
}
```

---

## 권장 사항

### 데이터 입력 순서

1. **평가 생성** → 2. **카테고리 점수** → 3. **체크포인트 결과** → 4. **레드플래그** → 5. **점수 계산** → 6. **추천 설정**

### 성능 최적화

- 페이지네이션 활용 (page, limit)
- 필요한 필터만 사용
- 대량 데이터는 배치 처리

### 데이터 검증

- 점수는 1.0, 3.0, 5.0 중 하나
- 레드플래그 심각도는 low, medium, high, critical
- 추천 상태는 recommend, not_recommend, pending

