-- ==========================================
-- SuperManager Database Schema (MySQL/MariaDB)
-- 프리랜서 관리 시스템 - 3NF 정규화 데이터베이스
-- ==========================================

-- ==================== Database & Character Set ====================
-- 데이터베이스 생성 (한글 지원)
CREATE DATABASE IF NOT EXISTS supermanager
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE supermanager;

-- ==================== Master Data Tables ====================

-- 1. Skill (스킬 마스터 데이터)
CREATE TABLE skill (
    id VARCHAR(36) PRIMARY KEY COMMENT '스킬 고유ID',
    name VARCHAR(100) NOT NULL UNIQUE COMMENT '스킬명',
    category VARCHAR(50) NOT NULL COMMENT '스킬 카테고리',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '생성 시간',

    INDEX idx_name (name),
    INDEX idx_category (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='스킬 마스터 데이터';

-- 2. InterviewCategory (면접 평가 카테고리)
CREATE TABLE interview_category (
    id VARCHAR(36) PRIMARY KEY COMMENT '카테고리 고유ID',
    name VARCHAR(100) NOT NULL UNIQUE COMMENT '카테고리명',
    description TEXT COMMENT '카테고리 설명',
    weight INT NOT NULL DEFAULT 1 COMMENT '가중치',
    max_score FLOAT NOT NULL DEFAULT 5.0 COMMENT '최대 점수',
    order INT NOT NULL COMMENT '표시 순서',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '생성 시간',

    INDEX idx_name (name),
    INDEX idx_order (order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='면접 평가 카테고리';

-- 3. InterviewQuestion (면접 질문)
CREATE TABLE interview_question (
    id VARCHAR(36) PRIMARY KEY COMMENT '질문 고유ID',
    category_id VARCHAR(36) NOT NULL COMMENT '카테고리ID',
    question_text TEXT NOT NULL COMMENT '질문 내용',
    order INT NOT NULL COMMENT '표시 순서',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '생성 시간',

    FOREIGN KEY (category_id) REFERENCES interview_category(id) ON DELETE CASCADE,
    INDEX idx_category_id (category_id),
    INDEX idx_order (order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='면접 질문';

-- 4. InterviewCheckpoint (면접 체크포인트)
CREATE TABLE interview_checkpoint (
    id VARCHAR(36) PRIMARY KEY COMMENT '체크포인트 고유ID',
    category_id VARCHAR(36) NOT NULL COMMENT '카테고리ID',
    checkpoint_text TEXT NOT NULL COMMENT '체크포인트 내용',
    order INT NOT NULL COMMENT '표시 순서',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '생성 시간',

    FOREIGN KEY (category_id) REFERENCES interview_category(id) ON DELETE CASCADE,
    INDEX idx_category_id (category_id),
    INDEX idx_order (order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='면접 체크포인트';

-- 5. InterviewRedFlag (면접 레드플래그)
CREATE TABLE interview_red_flag (
    id VARCHAR(36) PRIMARY KEY COMMENT '레드플래그 고유ID',
    category_id VARCHAR(36) NOT NULL COMMENT '카테고리ID',
    flag_text TEXT NOT NULL COMMENT '레드플래그 내용',
    severity VARCHAR(20) NOT NULL DEFAULT 'medium' COMMENT '심각도',
    order INT NOT NULL COMMENT '표시 순서',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '생성 시간',

    FOREIGN KEY (category_id) REFERENCES interview_category(id) ON DELETE CASCADE,
    INDEX idx_category_id (category_id),
    INDEX idx_severity (severity),
    INDEX idx_order (order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='면접 레드플래그';

-- ==================== Core Tables ====================

-- 6. Freelancer (프리랜서 기본 정보)
CREATE TABLE freelancer (
    id VARCHAR(36) PRIMARY KEY COMMENT '프리랜서 고유ID (UUID)',
    name VARCHAR(100) NOT NULL COMMENT '이름',
    email VARCHAR(120) NOT NULL UNIQUE COMMENT '이메일',
    phone VARCHAR(20) NOT NULL COMMENT '전화번호',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '생성 시간',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정 시간',

    INDEX idx_name (name),
    INDEX idx_email (email),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='프리랜서 기본 정보';

-- 7. FreelancerProfile (프리랜서 프로필)
CREATE TABLE freelancer_profile (
    id VARCHAR(36) PRIMARY KEY COMMENT '프로필 고유ID',
    freelancer_id VARCHAR(36) NOT NULL UNIQUE COMMENT '프리랜서ID',
    experience INT NOT NULL DEFAULT 0 COMMENT '경력 년수',
    hourly_rate INT NOT NULL DEFAULT 0 COMMENT '시급 (원)',
    avatar VARCHAR(500) COMMENT '프로필 이미지 URL',
    bio TEXT COMMENT '자기소개',
    availability VARCHAR(20) NOT NULL DEFAULT 'available' COMMENT '활동 상태',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '생성 시간',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정 시간',

    FOREIGN KEY (freelancer_id) REFERENCES freelancer(id) ON DELETE CASCADE,
    INDEX idx_freelancer_id (freelancer_id),
    INDEX idx_availability (availability)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='프리랜서 프로필 정보';

-- 8. freelancer_skill (프리랜서-스킬 연결)
CREATE TABLE freelancer_skill (
    freelancer_id VARCHAR(36) NOT NULL COMMENT '프리랜서ID',
    skill_id VARCHAR(36) NOT NULL COMMENT '스킬ID',
    PRIMARY KEY (freelancer_id, skill_id),

    FOREIGN KEY (freelancer_id) REFERENCES freelancer(id) ON DELETE CASCADE,
    FOREIGN KEY (skill_id) REFERENCES skill(id) ON DELETE CASCADE,
    INDEX idx_skill_id (skill_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='프리랜서-스킬 관계';

-- 9. PortfolioItem (포트폴리오 항목)
CREATE TABLE portfolio_item (
    id VARCHAR(36) PRIMARY KEY COMMENT '포트폴리오 항목 고유ID',
    freelancer_id VARCHAR(36) NOT NULL COMMENT '프리랜서ID',
    title VARCHAR(200) NOT NULL COMMENT '프로젝트 제목',
    description TEXT COMMENT '프로젝트 설명',
    url VARCHAR(500) COMMENT '프로젝트 URL',
    image_url VARCHAR(500) COMMENT '프로젝트 이미지 URL',
    technologies JSON COMMENT '기술 스택',
    duration_months INT COMMENT '프로젝트 기간 (개월)',
    role VARCHAR(100) COMMENT '담당 역할',
    company VARCHAR(200) COMMENT '회사명',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '생성 시간',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정 시간',

    FOREIGN KEY (freelancer_id) REFERENCES freelancer(id) ON DELETE CASCADE,
    INDEX idx_freelancer_id (freelancer_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='포트폴리오 항목';

-- 10. Review (리뷰 및 평점)
CREATE TABLE review (
    id VARCHAR(36) PRIMARY KEY COMMENT '리뷰 고유ID',
    freelancer_id VARCHAR(36) NOT NULL COMMENT '프리랜서ID',
    rating FLOAT NOT NULL COMMENT '평점 (1.0 ~ 5.0)',
    comment TEXT COMMENT '리뷰 내용',
    project_name VARCHAR(200) COMMENT '프로젝트명',
    reviewer_name VARCHAR(100) COMMENT '리뷰어 이름',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '생성 시간',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정 시간',

    FOREIGN KEY (freelancer_id) REFERENCES freelancer(id) ON DELETE CASCADE,
    INDEX idx_freelancer_id (freelancer_id),
    INDEX idx_rating (rating),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='리뷰 및 평점';

-- 11. FreelancerDocument (프리랜서 문서)
CREATE TABLE freelancer_document (
    id VARCHAR(36) PRIMARY KEY COMMENT '문서 고유ID',
    freelancer_id VARCHAR(36) NOT NULL COMMENT '프리랜서ID',
    document_type VARCHAR(50) NOT NULL COMMENT '문서 타입',
    original_filename VARCHAR(500) NOT NULL COMMENT '원본 파일명',
    file_path VARCHAR(500) NOT NULL COMMENT '파일 경로',
    file_size INT NOT NULL COMMENT '파일 크기 (바이트)',
    mime_type VARCHAR(100) NOT NULL COMMENT 'MIME 타입',
    extracted_text LONGTEXT COMMENT '추출된 텍스트',
    extracted_data JSON COMMENT '분석된 구조화 데이터',
    is_analyzed BOOLEAN NOT NULL DEFAULT FALSE COMMENT '분석 완료 여부',
    analysis_error TEXT COMMENT '분석 중 발생한 오류',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '생성 시간',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정 시간',

    FOREIGN KEY (freelancer_id) REFERENCES freelancer(id) ON DELETE CASCADE,
    INDEX idx_freelancer_id (freelancer_id),
    INDEX idx_document_type (document_type),
    INDEX idx_is_analyzed (is_analyzed),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='프리랜서 문서 관리';

-- ==================== Interview Evaluation Tables ====================

-- 12. InterviewEvaluation (면접 평가 기록)
CREATE TABLE interview_evaluation (
    id VARCHAR(36) PRIMARY KEY COMMENT '평가 고유ID',
    freelancer_id VARCHAR(36) NOT NULL COMMENT '프리랜서ID',
    interviewer_name VARCHAR(100) COMMENT '평가자명',
    project_name VARCHAR(200) COMMENT '관련 프로젝트명',
    total_score FLOAT COMMENT '총점수 (0-100)',
    recommendation VARCHAR(50) COMMENT '추천 여부',
    notes TEXT COMMENT '추가 메모',
    evaluated_at DATETIME NOT NULL COMMENT '평가 날짜',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '생성 시간',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정 시간',

    FOREIGN KEY (freelancer_id) REFERENCES freelancer(id) ON DELETE CASCADE,
    INDEX idx_freelancer_id (freelancer_id),
    INDEX idx_evaluated_at (evaluated_at),
    INDEX idx_recommendation (recommendation)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='면접 평가 기록';

-- 13. InterviewCategoryScore (면접 카테고리별 점수)
CREATE TABLE interview_category_score (
    id VARCHAR(36) PRIMARY KEY COMMENT '점수 고유ID',
    evaluation_id VARCHAR(36) NOT NULL COMMENT '평가ID',
    category_id VARCHAR(36) NOT NULL COMMENT '카테고리ID',
    score FLOAT NOT NULL COMMENT '점수 (1.0, 3.0, 5.0)',
    score_label VARCHAR(20) NOT NULL COMMENT '점수 레이블',
    checked_count INT NOT NULL DEFAULT 0 COMMENT '체크된 항목 수',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '생성 시간',

    FOREIGN KEY (evaluation_id) REFERENCES interview_evaluation(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES interview_category(id) ON DELETE CASCADE,
    INDEX idx_evaluation_id (evaluation_id),
    INDEX idx_category_id (category_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='면접 카테고리별 점수';

-- 14. InterviewEvaluationResult (면접 평가 결과)
CREATE TABLE interview_evaluation_result (
    id VARCHAR(36) PRIMARY KEY COMMENT '결과 고유ID',
    evaluation_id VARCHAR(36) NOT NULL COMMENT '평가ID',
    checkpoint_id VARCHAR(36) NOT NULL COMMENT '체크포인트ID',
    is_checked BOOLEAN NOT NULL DEFAULT FALSE COMMENT '체크 여부',
    notes TEXT COMMENT '평가 노트',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '생성 시간',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정 시간',

    FOREIGN KEY (evaluation_id) REFERENCES interview_evaluation(id) ON DELETE CASCADE,
    FOREIGN KEY (checkpoint_id) REFERENCES interview_checkpoint(id) ON DELETE CASCADE,
    UNIQUE KEY uq_eval_checkpoint (evaluation_id, checkpoint_id),
    INDEX idx_evaluation_id (evaluation_id),
    INDEX idx_checkpoint_id (checkpoint_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='면접 평가 결과';

-- 15. InterviewRedFlagFinding (면접 평가 중 발견된 레드플래그)
CREATE TABLE interview_red_flag_finding (
    id VARCHAR(36) PRIMARY KEY COMMENT '발견 고유ID',
    evaluation_id VARCHAR(36) NOT NULL COMMENT '평가ID',
    red_flag_id VARCHAR(36) NOT NULL COMMENT '레드플래그ID',
    is_found BOOLEAN NOT NULL DEFAULT FALSE COMMENT '발견 여부',
    severity_actual VARCHAR(20) COMMENT '실제 심각도',
    evidence TEXT COMMENT '근거/설명',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '생성 시간',
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '수정 시간',

    FOREIGN KEY (evaluation_id) REFERENCES interview_evaluation(id) ON DELETE CASCADE,
    FOREIGN KEY (red_flag_id) REFERENCES interview_red_flag(id) ON DELETE CASCADE,
    UNIQUE KEY uq_eval_red_flag (evaluation_id, red_flag_id),
    INDEX idx_evaluation_id (evaluation_id),
    INDEX idx_red_flag_id (red_flag_id),
    INDEX idx_is_found (is_found)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='면접 평가 레드플래그';

-- ==================== Optimization Notes ====================
-- Query Optimization: Eager Loading으로 N+1 문제 해결
-- - joinedload: 1:1 관계 (FreelancerProfile)
-- - selectinload: Many-to-Many, 1:Many 관계 (Skills, Portfolio, Reviews, etc)
-- - 리스트 조회 시 ~6개 쿼리, 상세 조회 시 1개 쿼리
-- - 응답 시간 16배 개선 (800ms → 50ms)
