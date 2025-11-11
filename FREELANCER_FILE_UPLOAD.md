# 프리랜서 파일 업로드 및 분석 시스템

## 개요

프리랜서 등록 시 **이력서, 포트폴리오, 자격증** 등의 파일을 업로드하고, 자동으로 분석하여 **데이터베이스에 저장**하는 시스템입니다.

### 주요 기능

- ✅ **다중 파일 형식 지원** (.docx, .pdf, .xlsx, .txt, .md)
- ✅ **자동 텍스트 추출** - PDF, Word, Excel 파일에서 텍스트 추출
- ✅ **지능형 분석** - 이력서/포트폴리오 자동 분석 및 데이터 추출
- ✅ **원본 파일 보존** - 로컬 파일시스템에 원본 저장
- ✅ **구조화된 데이터** - JSON 형식으로 분석 결과 저장
- ✅ **재분석 기능** - 필요 시 문서 재분석 가능

---

## 데이터베이스 구조

### freelancer_document 테이블

```sql
CREATE TABLE freelancer_document (
  id VARCHAR(36) PRIMARY KEY,
  freelancer_id VARCHAR(36) NOT NULL,  -- FK: freelancer
  document_type VARCHAR(50),           -- resume, portfolio, certificate, etc
  original_filename VARCHAR(500),      -- 원본 파일명
  file_path VARCHAR(500),              -- 저장된 파일 경로
  file_size INTEGER,                   -- 파일 크기 (바이트)
  mime_type VARCHAR(100),              -- application/pdf, etc

  -- 분석 결과
  extracted_text LONGTEXT,             -- 추출된 원본 텍스트
  extracted_data JSON,                 -- 분석된 구조화 데이터
  is_analyzed BOOLEAN,                 -- 분석 여부
  analysis_error TEXT,                 -- 분석 중 오류 메시지

  created_at DATETIME,
  updated_at DATETIME
);
```

---

## API 엔드포인트

### 1. 문서 업로드 및 분석

**요청:**
```bash
POST /api/freelancers/{freelancer_id}/documents
Content-Type: multipart/form-data

Parameters:
- file: (FILE) 업로드할 파일
- documentType: (STRING) resume | portfolio | certificate | cover_letter | other
```

**cURL 예시:**
```bash
curl -X POST "http://localhost:8000/api/freelancers/freelancer-123/documents" \
  -F "file=@/path/to/resume.pdf" \
  -F "documentType=resume"
```

**응답 (201 Created):**
```json
{
  "success": true,
  "message": "문서 업로드 및 분석 완료",
  "data": {
    "id": "doc-uuid",
    "freelancerId": "freelancer-123",
    "documentType": "resume",
    "originalFilename": "resume.pdf",
    "fileSize": 245678,
    "mimeType": "application/pdf",
    "isAnalyzed": true,
    "analysisError": null,
    "extractedData": {
      "skills": ["Python", "JavaScript", "React"],
      "experience_years": 5,
      "education": ["Seoul National University"],
      "projects": ["E-commerce Platform", "Mobile App"],
      "languages": ["Korean", "English"],
      "certifications": ["AWS Solutions Architect"]
    },
    "createdAt": "2025-11-07T21:30:00",
    "updatedAt": "2025-11-07T21:30:00"
  }
}
```

### 2. 문서 목록 조회

**요청:**
```bash
GET /api/freelancers/{freelancer_id}/documents
  ?page=1
  &limit=20
  &documentType=resume
```

**응답 (200 OK):**
```json
{
  "success": true,
  "message": "문서 목록 조회 성공",
  "data": {
    "items": [
      { /* 문서 객체 */ }
    ],
    "total": 3,
    "page": 1,
    "limit": 20,
    "totalPages": 1
  }
}
```

### 3. 문서 상세 조회

**요청:**
```bash
GET /api/freelancers/documents/{document_id}
```

**응답 (200 OK):**
```json
{
  "success": true,
  "message": "문서 조회 성공",
  "data": {
    "id": "doc-uuid",
    "freelancerId": "freelancer-123",
    "documentType": "resume",
    "originalFilename": "resume.pdf",
    "fileSize": 245678,
    "mimeType": "application/pdf",
    "isAnalyzed": true,
    "extractedData": { /* ... */ },
    "extractedText": "전체 추출된 텍스트...",  // include_text=true일 때만
    "createdAt": "2025-11-07T21:30:00",
    "updatedAt": "2025-11-07T21:30:00"
  }
}
```

### 4. 문서 삭제

**요청:**
```bash
DELETE /api/freelancers/documents/{document_id}
```

**응답 (204 No Content):**
```json
{
  "success": true,
  "message": "문서 삭제 성공",
  "data": null
}
```

### 5. 문서 재분석

**요청:**
```bash
POST /api/freelancers/documents/{document_id}/re-analyze
```

**응답 (200 OK):**
```json
{
  "success": true,
  "message": "문서 재분석 완료",
  "data": {
    /* 업데이트된 문서 데이터 */
  }
}
```

---

## 문서 타입별 분석 결과

### 1. Resume (이력서)

```json
{
  "skills": ["Python", "React", "Node.js"],
  "experience_years": 5,
  "education": ["Seoul National University"],
  "projects": ["Project A", "Project B"],
  "languages": ["Korean", "English"],
  "certifications": ["AWS Solutions Architect"],
  "summary": "5년 경력의 풀스택 개발자입니다..."
}
```

**자동 추출 항목:**
- ✅ 기술 스택 (Python, Java, React 등)
- ✅ 경력 연수 ("5년", "경력 5년" 등)
- ✅ 학력 (대학교 이름)
- ✅ 프로젝트명
- ✅ 언어 능력
- ✅ 자격증

### 2. Portfolio (포트폴리오)

```json
{
  "projects": [
    {
      "title": "E-commerce Platform",
      "description": "React 기반 전자상거래 플랫폼",
      "url": "https://example.com"
    }
  ],
  "technologies": ["React", "Node.js", "MongoDB"],
  "links": ["https://github.com/example", "https://portfolio.com"]
}
```

**자동 추출 항목:**
- ✅ 프로젝트명 및 설명
- ✅ 사용 기술
- ✅ 포트폴리오 링크/URL

### 3. 기타 문서

```json
{
  "text": "문서의 처음 500자..."
}
```

---

## 파일 형식별 처리

| 형식 | 확장자 | 지원 | 추출 방식 |
|------|--------|------|---------|
| PDF | .pdf | ✅ | PyPDF2 라이브러리 |
| Word | .docx | ✅ | python-docx 라이브러리 |
| Excel | .xlsx | ✅ | openpyxl 라이브러리 |
| Text | .txt | ✅ | 기본 텍스트 읽기 |
| Markdown | .md | ✅ | 기본 텍스트 읽기 |

### 지원되는 MIME 타입

```
application/pdf
application/vnd.openxmlformats-officedocument.wordprocessingml.document (docx)
application/vnd.openxmlformats-officedocument.spreadsheetml.sheet (xlsx)
text/plain
text/markdown
```

---

## 설정

### config.py

```python
# File Upload Configuration
UPLOAD_FOLDER = 'uploads'              # 업로드 폴더 (기본값)
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 최대 파일 크기: 10MB
ALLOWED_EXTENSIONS = {
    'txt', 'pdf', 'docx', 'xlsx', 'md'
}
```

### 환경 변수 (.env)

```bash
UPLOAD_FOLDER=uploads/documents  # 커스텀 업로드 폴더
```

---

## 디렉토리 구조

```
uploads/
└── freelancer/
    ├── freelancer-123/
    │   ├── 20251107213000_resume.pdf
    │   ├── 20251107213015_portfolio.xlsx
    │   └── 20251107213030_certificate.pdf
    ├── freelancer-456/
    └── ...
```

**파일명 규칙:** `{timestamp}_{original_filename}`

---

## 오류 처리

### 가능한 오류 응답

#### 파일 없음
```json
{
  "success": false,
  "message": "파일이 없습니다",
  "data": null
}
```

#### 파일 크기 초과
```json
{
  "success": false,
  "message": "파일 크기는 10.0MB 이하여야 합니다",
  "data": null
}
```

#### 지원하지 않는 파일 형식
```json
{
  "success": false,
  "message": "허용된 파일 형식: txt, pdf, docx, xlsx, md",
  "data": null
}
```

#### 프리랜서 없음
```json
{
  "success": false,
  "message": "프리랜서를 찾을 수 없습니다",
  "data": null
}
```

#### 분석 실패
```json
{
  "success": true,
  "message": "문서 업로드 완료",
  "data": {
    "id": "doc-uuid",
    "isAnalyzed": false,
    "analysisError": "PDF 파일 읽기 오류: ..."
  }
}
```

---

## 사용 예시

### Python (requests 라이브러리)

```python
import requests

freelancer_id = "freelancer-123"
upload_url = f"http://localhost:8000/api/freelancers/{freelancer_id}/documents"

# 파일 업로드
with open('resume.pdf', 'rb') as f:
    files = {'file': f}
    data = {'documentType': 'resume'}
    response = requests.post(upload_url, files=files, data=data)

result = response.json()
print(f"문서 ID: {result['data']['id']}")
print(f"분석 여부: {result['data']['isAnalyzed']}")
print(f"추출된 스킬: {result['data']['extractedData']['skills']}")
```

### JavaScript (fetch API)

```javascript
const freelancerId = "freelancer-123";
const uploadUrl = `http://localhost:8000/api/freelancers/${freelancerId}/documents`;

const fileInput = document.getElementById('fileInput');
const file = fileInput.files[0];

const formData = new FormData();
formData.append('file', file);
formData.append('documentType', 'resume');

const response = await fetch(uploadUrl, {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log('Document ID:', result.data.id);
console.log('Skills:', result.data.extractedData.skills);
```

### cURL

```bash
# 이력서 업로드
curl -X POST \
  "http://localhost:8000/api/freelancers/freelancer-123/documents" \
  -F "file=@resume.pdf" \
  -F "documentType=resume"

# 포트폴리오 업로드
curl -X POST \
  "http://localhost:8000/api/freelancers/freelancer-123/documents" \
  -F "file=@portfolio.xlsx" \
  -F "documentType=portfolio"

# 문서 목록 조회
curl "http://localhost:8000/api/freelancers/freelancer-123/documents?page=1&limit=20"

# 문서 상세 조회
curl "http://localhost:8000/api/freelancers/documents/doc-uuid"

# 문서 삭제
curl -X DELETE "http://localhost:8000/api/freelancers/documents/doc-uuid"

# 문서 재분석
curl -X POST "http://localhost:8000/api/freelancers/documents/doc-uuid/re-analyze"
```

---

## 필요한 라이브러리

```bash
pip install python-docx PyPDF2 openpyxl
```

또는 requirements.txt에 추가:

```
python-docx==0.8.11
PyPDF2==3.15.0
openpyxl==3.10.10
```

---

## 프리랜서 등록 흐름

### 1단계: 기본 정보 등록

```bash
POST /api/freelancers
{
  "name": "김준호",
  "email": "junho@example.com",
  "phone": "010-1234-5678",
  "experience": 5,
  "hourlyRate": 50000,
  "skillIds": ["react", "python"]
}
```

### 2단계: 문서 업로드

```bash
POST /api/freelancers/{freelancer_id}/documents
- 이력서 업로드
- 포트폴리오 업로드
- 자격증 업로드
```

### 3단계: 자동 분석 완료

프리랜서의 `extractedData` 필드에서:
- 스킬 자동 추출
- 경력 연수 확인
- 프로젝트 정보 수집
- 언어 능력 파악

---

## 성능 고려사항

### 인덱싱

```sql
CREATE INDEX ix_freelancer_document_freelancer_id
  ON freelancer_document(freelancer_id);
CREATE INDEX ix_freelancer_document_is_analyzed
  ON freelancer_document(is_analyzed);
CREATE INDEX ix_freelancer_document_created_at
  ON freelancer_document(created_at);
```

### 파일 저장

- 원본 파일은 로컬 파일시스템에 저장
- 메타데이터와 분석 결과는 DB에 저장
- 클라우드 스토리지 연동 가능 (향후 확장)

### 문서 크기

- 단일 파일 최대 10MB
- 추출된 텍스트는 LONGTEXT로 저장 (최대 4GB)
- 분석 결과(JSON)는 적절한 크기로 유지

---

## 보안

### 파일 검증

✅ 파일 크기 확인 (10MB 이하)
✅ 파일 형식 확인 (확장자 기반)
✅ MIME 타입 검증
✅ 경로 탐색 공격 방지 (secure_filename)

### 접근 제어

- 프리랜서만 자신의 문서 접근 가능 (향후 권한 추가)
- 파일명 암호화 (타임스탬프 기반)

---

## 향후 개선 사항

- [ ] 클라우드 스토리지 통합 (AWS S3, GCS)
- [ ] 고급 NLP 분석 (스킬 자동 매칭)
- [ ] 문서 미리보기 기능
- [ ] 일괄 업로드 지원
- [ ] 문서 권한 관리
- [ ] 스캔 문서 OCR 지원
- [ ] 비용 추정 자동화

