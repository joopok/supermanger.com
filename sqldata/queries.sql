-- ==================== 유용한 쿼리 모음 ====================
-- SuperManager 시스템용 주요 조회 및 분석 쿼리

USE supermanager;

-- ==================== 1. 프리랜서 조회 쿼리 ====================

-- 1.1 모든 프리랜서 (기본 정보 + 프로필)
SELECT
  f.id,
  f.name,
  f.email,
  f.phone,
  fp.experience,
  fp.hourly_rate,
  fp.availability,
  f.created_at
FROM freelancer f
LEFT JOIN freelancer_profile fp ON f.id = fp.freelancer_id
ORDER BY f.created_at DESC;

-- 1.2 프리랜서 (완전한 정보 - 뷰 사용)
SELECT * FROM v_freelancer_complete
ORDER BY created_at DESC;

-- 1.3 특정 경력 이상의 프리랜서
SELECT
  f.name,
  f.email,
  fp.experience,
  fp.hourly_rate,
  COUNT(fs.skill_id) as skill_count,
  AVG(r.rating) as avg_rating
FROM freelancer f
LEFT JOIN freelancer_profile fp ON f.id = fp.freelancer_id
LEFT JOIN freelancer_skill fs ON f.id = fs.freelancer_id
LEFT JOIN review r ON f.id = r.freelancer_id
WHERE fp.experience >= 5
GROUP BY f.id
ORDER BY fp.experience DESC;

-- 1.4 시급이 저렴한 순서로 정렬
SELECT
  f.name,
  f.email,
  fp.hourly_rate,
  fp.experience,
  fp.availability
FROM freelancer f
LEFT JOIN freelancer_profile fp ON f.id = fp.freelancer_id
WHERE fp.availability = 'available'
ORDER BY fp.hourly_rate ASC;

-- 1.5 가용 중인 프리랜서
SELECT
  f.name,
  f.email,
  fp.hourly_rate,
  COUNT(fs.skill_id) as skill_count
FROM freelancer f
LEFT JOIN freelancer_profile fp ON f.id = fp.freelancer_id
LEFT JOIN freelancer_skill fs ON f.id = fs.freelancer_id
WHERE fp.availability = 'available'
GROUP BY f.id;

-- ==================== 2. 스킬 관련 쿼리 ====================

-- 2.1 프리랜서별 스킬 목록
SELECT
  f.name as freelancer_name,
  GROUP_CONCAT(CONCAT(s.name, ' (', fs.proficiency_level, ')') SEPARATOR ', ') as skills
FROM freelancer f
LEFT JOIN freelancer_skill fs ON f.id = fs.freelancer_id
LEFT JOIN skill s ON fs.skill_id = s.id
GROUP BY f.id
ORDER BY f.name;

-- 2.2 특정 스킬을 보유한 프리랜서
SELECT
  f.name,
  f.email,
  fs.proficiency_level,
  fp.experience,
  fp.hourly_rate
FROM freelancer f
LEFT JOIN freelancer_skill fs ON f.id = fs.freelancer_id
LEFT JOIN freelancer_profile fp ON f.id = fp.freelancer_id
LEFT JOIN skill s ON fs.skill_id = s.id
WHERE s.name = 'React'
ORDER BY fs.proficiency_level DESC;

-- 2.3 가장 많은 프리랜서가 보유한 스킬
SELECT
  s.name as skill_name,
  s.category,
  COUNT(fs.freelancer_id) as freelancer_count
FROM skill s
LEFT JOIN freelancer_skill fs ON s.id = fs.skill_id
GROUP BY s.id
ORDER BY freelancer_count DESC
LIMIT 20;

-- 2.4 카테고리별 스킬 분포
SELECT
  s.category,
  COUNT(*) as skill_count,
  COUNT(DISTINCT fs.freelancer_id) as freelancer_count
FROM skill s
LEFT JOIN freelancer_skill fs ON s.id = fs.skill_id
GROUP BY s.category
ORDER BY skill_count DESC;

-- ==================== 3. 포트폴리오 관련 쿼리 ====================

-- 3.1 프리랜서별 포트폴리오
SELECT
  f.name as freelancer_name,
  COUNT(pi.id) as project_count,
  GROUP_CONCAT(pi.title SEPARATOR ', ') as projects
FROM freelancer f
LEFT JOIN portfolio_item pi ON f.id = pi.freelancer_id
GROUP BY f.id;

-- 3.2 특정 기술을 사용한 포트폴리오
SELECT
  f.name as freelancer_name,
  pi.title as project_title,
  pi.company,
  pi.duration_months,
  pi.role
FROM freelancer f
JOIN portfolio_item pi ON f.id = pi.freelancer_id
WHERE pi.technologies LIKE '%React%'
ORDER BY pi.created_at DESC;

-- 3.3 포트폴리오가 있는 프리랜서 통계
SELECT
  f.name,
  COUNT(pi.id) as portfolio_count,
  SUM(pi.duration_months) as total_project_duration
FROM freelancer f
LEFT JOIN portfolio_item pi ON f.id = pi.freelancer_id
GROUP BY f.id
HAVING COUNT(pi.id) > 0
ORDER BY portfolio_count DESC;

-- ==================== 4. 리뷰 및 평점 관련 쿼리 ====================

-- 4.1 프리랜서별 평가 통계
SELECT
  f.name,
  COUNT(r.id) as review_count,
  ROUND(AVG(r.rating), 2) as avg_rating,
  MIN(r.rating) as min_rating,
  MAX(r.rating) as max_rating
FROM freelancer f
LEFT JOIN review r ON f.id = r.freelancer_id
GROUP BY f.id
ORDER BY avg_rating DESC;

-- 4.2 평점이 높은 프리랜서
SELECT
  f.name,
  f.email,
  fp.hourly_rate,
  COUNT(r.id) as review_count,
  ROUND(AVG(r.rating), 2) as avg_rating
FROM freelancer f
LEFT JOIN freelancer_profile fp ON f.id = fp.freelancer_id
LEFT JOIN review r ON f.id = r.freelancer_id
GROUP BY f.id
HAVING COUNT(r.id) > 0 AND AVG(r.rating) >= 4.5
ORDER BY avg_rating DESC;

-- 4.3 최근 리뷰
SELECT
  f.name as freelancer_name,
  r.rating,
  r.comment,
  r.project_name,
  r.created_at
FROM review r
JOIN freelancer f ON r.freelancer_id = f.id
ORDER BY r.created_at DESC
LIMIT 10;

-- ==================== 5. 면접 평가 쿼리 ====================

-- 5.1 모든 면접 평가 (완전한 정보)
SELECT * FROM v_interview_evaluation_summary
ORDER BY evaluated_at DESC;

-- 5.2 추천 대상 (65점 이상)
SELECT
  f.name as freelancer_name,
  ie.interviewer_name,
  ie.project_name,
  ie.total_score,
  ie.recommendation,
  ie.evaluated_at
FROM interview_evaluation ie
JOIN freelancer f ON ie.freelancer_id = f.id
WHERE ie.total_score >= 65 AND ie.recommendation = 'recommend'
ORDER BY ie.total_score DESC;

-- 5.3 특정 프리랜서의 모든 평가
SELECT
  ie.id,
  ie.interviewer_name,
  ie.project_name,
  ie.total_score,
  ie.recommendation,
  COUNT(DISTINCT ics.category_id) as evaluated_categories,
  ie.evaluated_at
FROM interview_evaluation ie
LEFT JOIN interview_category_score ics ON ie.id = ics.evaluation_id
WHERE ie.freelancer_id = 'freelancer-001'
GROUP BY ie.id
ORDER BY ie.evaluated_at DESC;

-- 5.4 카테고리별 점수 분석
SELECT
  f.name as freelancer_name,
  ic.name as category_name,
  ics.score,
  ics.score_label,
  ics.checked_count
FROM interview_category_score ics
JOIN interview_evaluation ie ON ics.evaluation_id = ie.id
JOIN freelancer f ON ie.freelancer_id = f.id
JOIN interview_category ic ON ics.category_id = ic.id
ORDER BY f.name, ic.`order`;

-- 5.5 가장 많이 발견되는 레드플래그
SELECT
  irf.flag_text,
  irf.severity,
  COUNT(irff.id) as found_count
FROM interview_red_flag irf
LEFT JOIN interview_red_flag_finding irff ON irf.id = irff.red_flag_id
GROUP BY irf.id
ORDER BY found_count DESC;

-- ==================== 6. 문서 관리 쿼리 ====================

-- 6.1 프리랜서별 업로드된 문서
SELECT
  f.name as freelancer_name,
  fd.document_type,
  fd.original_filename,
  fd.file_size,
  fd.is_analyzed,
  fd.created_at
FROM freelancer_document fd
JOIN freelancer f ON fd.freelancer_id = f.id
ORDER BY f.name, fd.created_at DESC;

-- 6.2 분석되지 않은 문서
SELECT
  f.name as freelancer_name,
  fd.document_type,
  fd.original_filename,
  fd.analysis_error,
  fd.created_at
FROM freelancer_document fd
JOIN freelancer f ON fd.freelancer_id = f.id
WHERE fd.is_analyzed = FALSE
ORDER BY fd.created_at DESC;

-- 6.3 이력서 분석 결과
SELECT
  f.name as freelancer_name,
  fd.original_filename,
  JSON_EXTRACT(fd.extracted_data, '$.skills') as extracted_skills,
  JSON_EXTRACT(fd.extracted_data, '$.experience_years') as experience_years
FROM freelancer_document fd
JOIN freelancer f ON fd.freelancer_id = f.id
WHERE fd.document_type = 'resume' AND fd.is_analyzed = TRUE;

-- ==================== 7. 대시보드 쿼리 ====================

-- 7.1 전체 통계
SELECT
  'Total Freelancers' as metric, COUNT(*) as value FROM freelancer
UNION ALL
SELECT 'Total Skills', COUNT(*) FROM skill
UNION ALL
SELECT 'Total Portfolio Items', COUNT(*) FROM portfolio_item
UNION ALL
SELECT 'Total Reviews', COUNT(*) FROM review
UNION ALL
SELECT 'Average Rating', ROUND(AVG(rating), 2) FROM review
UNION ALL
SELECT 'Total Evaluations', COUNT(*) FROM interview_evaluation
UNION ALL
SELECT 'Documents Uploaded', COUNT(*) FROM freelancer_document;

-- 7.2 프리랜서 시장 분석
SELECT
  'Available Freelancers' as category, COUNT(*) as count FROM freelancer_profile WHERE availability = 'available'
UNION ALL
SELECT 'Busy Freelancers', COUNT(*) FROM freelancer_profile WHERE availability = 'busy'
UNION ALL
SELECT 'Unavailable Freelancers', COUNT(*) FROM freelancer_profile WHERE availability = 'unavailable';

-- 7.3 경력별 프리랜서 분포
SELECT
  CASE
    WHEN experience < 2 THEN 'Junior (< 2 years)'
    WHEN experience < 5 THEN 'Mid-Level (2-5 years)'
    WHEN experience < 10 THEN 'Senior (5-10 years)'
    ELSE 'Expert (10+ years)'
  END as experience_level,
  COUNT(*) as freelancer_count,
  ROUND(AVG(hourly_rate), 0) as avg_hourly_rate
FROM freelancer_profile
GROUP BY experience_level
ORDER BY experience;

-- ==================== 8. 데이터 정합성 검사 ====================

-- 8.1 프로필이 없는 프리랜서
SELECT f.id, f.name, f.email
FROM freelancer f
LEFT JOIN freelancer_profile fp ON f.id = fp.freelancer_id
WHERE fp.id IS NULL;

-- 8.2 존재하지 않는 스킬 참조
SELECT fs.freelancer_id, fs.skill_id
FROM freelancer_skill fs
LEFT JOIN skill s ON fs.skill_id = s.id
WHERE s.id IS NULL;

-- 8.3 존재하지 않는 프리랜서 참조
SELECT fd.freelancer_id, fd.original_filename
FROM freelancer_document fd
LEFT JOIN freelancer f ON fd.freelancer_id = f.id
WHERE f.id IS NULL;

-- ==================== END OF QUERIES ====================
