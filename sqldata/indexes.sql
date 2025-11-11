-- ==========================================
-- Additional Indexes for Performance
-- 성능 최적화를 위한 추가 인덱스
-- ==========================================

USE supermanager;

-- ==================== Composite Indexes ====================
-- 자주 함께 사용되는 컬럼들의 복합 인덱스

-- Freelancer 검색 최적화
ALTER TABLE freelancer ADD INDEX idx_name_email (name, email);
ALTER TABLE freelancer ADD INDEX idx_created_at_name (created_at, name);

-- FreelancerProfile 필터링 최적화
ALTER TABLE freelancer_profile ADD INDEX idx_availability_experience (availability, experience);
ALTER TABLE freelancer_profile ADD INDEX idx_hourly_rate_availability (hourly_rate, availability);

-- Portfolio 정렬 최적화
ALTER TABLE portfolio_item ADD INDEX idx_freelancer_created (freelancer_id, created_at DESC);

-- Review 평점 조회 최적화
ALTER TABLE review ADD INDEX idx_freelancer_rating (freelancer_id, rating DESC);
ALTER TABLE review ADD INDEX idx_rating_created (rating, created_at DESC);

-- Document 타입 필터링 최적화
ALTER TABLE freelancer_document ADD INDEX idx_freelancer_type (freelancer_id, document_type);
ALTER TABLE freelancer_document ADD INDEX idx_type_analyzed (document_type, is_analyzed);

-- Interview 평가 최적화
ALTER TABLE interview_evaluation ADD INDEX idx_freelancer_evaluated (freelancer_id, evaluated_at DESC);
ALTER TABLE interview_category_score ADD INDEX idx_evaluation_category (evaluation_id, category_id);

-- ==================== Partitioning (Optional) ====================
-- 매우 큰 테이블의 경우 파티셔닝 고려

-- 예: 평가 데이터를 월별로 파티셔닝
-- ALTER TABLE interview_evaluation
-- PARTITION BY RANGE (YEAR_MONTH(evaluated_at)) (
--     PARTITION p_2024_01 VALUES LESS THAN (202402),
--     PARTITION p_2024_02 VALUES LESS THAN (202403),
--     ...
--     PARTITION p_current VALUES LESS THAN (MAXVALUE)
-- );

-- ==================== Query Statistics ====================
-- MySQL 8.0+: 쿼리 통계 활성화
-- SET GLOBAL innodb_stats_auto_recalc = ON;
-- SET GLOBAL innodb_stats_on_metadata = OFF;

-- ==================== Performance Hints ====================
-- MyISAM 엔진에서 InnoDB로 변경
-- ALTER TABLE skill ENGINE=InnoDB;
-- (모든 테이블이 이미 InnoDB 사용)

-- ==================== Index Maintenance ====================

-- 인덱스 최적화 (정기적으로 실행)
-- OPTIMIZE TABLE freelancer;
-- OPTIMIZE TABLE freelancer_skill;
-- OPTIMIZE TABLE portfolio_item;
-- OPTIMIZE TABLE review;
-- OPTIMIZE TABLE interview_evaluation;

-- 인덱스 통계 업데이트
-- ANALYZE TABLE freelancer;
-- ANALYZE TABLE interview_evaluation;

-- 인덱스 재구성 (프래그멘테이션 제거)
-- ALTER TABLE freelancer ENGINE=InnoDB;

