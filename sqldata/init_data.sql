-- ==================== 초기 데이터 삽입 ====================
-- SuperManager 시스템용 마스터 데이터 및 샘플 데이터

USE supermanager;

-- ==================== 1. Skill Master Data ====================

INSERT INTO skill (id, name, category) VALUES
-- Frontend Skills
('skill-001', 'React', 'frontend'),
('skill-002', 'Vue', 'frontend'),
('skill-003', 'Angular', 'frontend'),
('skill-004', 'TypeScript', 'frontend'),
('skill-005', 'JavaScript', 'frontend'),
('skill-006', 'HTML5', 'frontend'),
('skill-007', 'CSS3', 'frontend'),
('skill-008', 'Tailwind CSS', 'frontend'),
('skill-009', 'Bootstrap', 'frontend'),
('skill-010', 'Figma', 'design'),

-- Backend Skills
('skill-011', 'Python', 'backend'),
('skill-012', 'Node.js', 'backend'),
('skill-013', 'Java', 'backend'),
('skill-014', 'Spring', 'backend'),
('skill-015', 'Django', 'backend'),
('skill-016', 'Flask', 'backend'),
('skill-017', 'C#', 'backend'),
('skill-018', 'Go', 'backend'),
('skill-019', 'Rust', 'backend'),
('skill-020', 'PHP', 'backend'),

-- Database Skills
('skill-021', 'MySQL', 'database'),
('skill-022', 'PostgreSQL', 'database'),
('skill-023', 'MongoDB', 'database'),
('skill-024', 'Redis', 'database'),
('skill-025', 'Elasticsearch', 'database'),
('skill-026', 'Firebase', 'database'),

-- DevOps Skills
('skill-027', 'Docker', 'devops'),
('skill-028', 'Kubernetes', 'devops'),
('skill-029', 'AWS', 'devops'),
('skill-030', 'Azure', 'devops'),
('skill-031', 'GCP', 'devops'),
('skill-032', 'Jenkins', 'devops'),
('skill-033', 'GitLab CI', 'devops'),
('skill-034', 'Terraform', 'devops'),

-- UI/UX Design
('skill-035', 'UI Design', 'design'),
('skill-036', 'UX Design', 'design'),
('skill-037', 'Photoshop', 'design'),
('skill-038', 'Illustrator', 'design'),

-- Other Skills
('skill-039', 'Git', 'tools'),
('skill-040', 'REST API', 'tools'),
('skill-041', 'GraphQL', 'tools');

-- ==================== 2. Interview Category Master Data ====================

INSERT INTO interview_category (id, name, description, weight, max_score, `order`) VALUES
('cat-001', '기술 역량 & 문제해결', '최근 프로젝트에서 가장 어려웠던 기술 문제와 해결 과정', 20, 5.0, 1),
('cat-002', '포트폴리오/기여 검증', '포트폴리오에서 직접 구현한 부분과 기여도 검증', 20, 5.0, 2),
('cat-003', '커뮤니케이션 & 일정관리', '불명확한 요구사항 명확화와 일정 공유 능력', 20, 5.0, 3),
('cat-004', '계약/업무 방식 & 품질보증', '범위/마일스톤/소유권/보안/하자보수 합의 능력', 20, 5.0, 4);

-- ==================== 3. Interview Questions ====================

INSERT INTO interview_question (id, category_id, question_text, `order`) VALUES
('q-001', 'cat-001', '최근 프로젝트에서 가장 어려웠던 기술 문제와 해결 과정은?', 1),
('q-002', 'cat-002', '이 포트폴리오에서 직접 구현한 부분과 기여도(%)는?', 1),
('q-003', 'cat-003', '불명확한 요구를 어떻게 명확화하나요? 지연 시 어떻게 공유하나요?', 1),
('q-004', 'cat-004', '범위/마일스톤/소유권/보안/하자보수는 어떻게 합의하나요?', 1);

-- ==================== 4. Interview Checkpoints ====================

INSERT INTO interview_checkpoint (id, category_id, checkpoint_text, `order`) VALUES
-- 기술역량 체크포인트
('cp-001', 'cat-001', '사용 스택의 선택 이유와 대안 설명', 1),
('cp-002', 'cat-001', '설계·테스트·배포 흐름 이해', 2),
('cp-003', 'cat-001', '성능/보안/확장성 고려', 3),

-- 포트폴리오 체크포인트
('cp-004', 'cat-002', '코드/리포지터리/커밋 증빙', 1),
('cp-005', 'cat-002', '데모 또는 산출물 제공', 2),
('cp-006', 'cat-002', '재사용 가능한 구조/문서화', 3),

-- 커뮤니케이션 체크포인트
('cp-007', 'cat-003', '요구사항 정리 습관(메모/PRD)', 1),
('cp-008', 'cat-003', '리스크 조기 공유 주기 합의', 2),
('cp-009', 'cat-003', '이슈트래커/문서 도구 활용', 3),

-- 계약/업무 방식 체크포인트
('cp-010', 'cat-004', '명확한 SOW(범위·산출물)', 1),
('cp-011', 'cat-004', '마일스톤-지불 연동', 2),
('cp-012', 'cat-004', '테스트/리뷰/문서 기준', 3),
('cp-013', 'cat-004', 'IP/보안·SLA 합의', 4);

-- ==================== 5. Interview Red Flags ====================

INSERT INTO interview_red_flag (id, category_id, flag_text, severity, `order`) VALUES
-- 기술역량 레드플래그
('rf-001', 'cat-001', '추상적 답변만 함', 'high', 1),
('rf-002', 'cat-001', '테스트/모듈화 부재', 'high', 2),
('rf-003', 'cat-001', '도구/버전 이해 부족', 'medium', 3),

-- 포트폴리오 레드플래그
('rf-004', 'cat-002', '기여 범위 모호', 'critical', 1),
('rf-005', 'cat-002', 'NDA만으로 모든 증빙 거부', 'critical', 2),
('rf-006', 'cat-002', '데모 미제공', 'high', 3),

-- 커뮤니케이션 레드플래그
('rf-007', 'cat-003', '과도한 낙관 일정', 'high', 1),
('rf-008', 'cat-003', '피드백 방어적', 'medium', 2),
('rf-009', 'cat-003', '기록/회의록 회피', 'medium', 3),

-- 계약/업무 방식 레드플래그
('rf-010', 'cat-004', '선지급 과다 요구', 'high', 1),
('rf-011', 'cat-004', '소스코드 전달/소유권 거부', 'critical', 2),
('rf-012', 'cat-004', '유지보수 불가', 'critical', 3),
('rf-013', 'cat-004', 'SLA 부재', 'high', 4);

-- ==================== 6. 샘플 프리랜서 데이터 ====================

INSERT INTO freelancer (id, name, email, phone) VALUES
('freelancer-001', '김준호', 'junho.kim@example.com', '010-1234-5678'),
('freelancer-002', '이수영', 'suyoung.lee@example.com', '010-2345-6789'),
('freelancer-003', '박민준', 'minjun.park@example.com', '010-3456-7890'),
('freelancer-004', '최지은', 'jieun.choi@example.com', '010-4567-8901');

-- ==================== 7. 샘플 프리랜서 프로필 ====================

INSERT INTO freelancer_profile (id, freelancer_id, experience, hourly_rate, bio, availability) VALUES
('prof-001', 'freelancer-001', 5, 50000, '경력 5년의 React 개발자입니다. UI/UX에 관심이 많습니다.', 'available'),
('prof-002', 'freelancer-002', 7, 60000, '풀스택 개발자로 백엔드와 프론트엔드 모두 경험이 있습니다.', 'available'),
('prof-003', 'freelancer-003', 3, 35000, '신입 개발자지만 열정적으로 배우고 있습니다.', 'busy'),
('prof-004', 'freelancer-004', 6, 55000, '데이터베이스 설계 및 최적화 전문가입니다.', 'available');

-- ==================== 8. 샘플 프리랜서 스킬 ====================

INSERT INTO freelancer_skill (freelancer_id, skill_id, proficiency_level) VALUES
-- 김준호: React 개발자
('freelancer-001', 'skill-001', 'advanced'),  -- React
('freelancer-001', 'skill-004', 'advanced'),  -- TypeScript
('freelancer-001', 'skill-012', 'intermediate'),  -- Node.js
('freelancer-001', 'skill-005', 'advanced'),  -- JavaScript
('freelancer-001', 'skill-039', 'advanced'),  -- Git

-- 이수영: 풀스택 개발자
('freelancer-002', 'skill-001', 'advanced'),  -- React
('freelancer-002', 'skill-011', 'advanced'),  -- Python
('freelancer-002', 'skill-015', 'intermediate'),  -- Django
('freelancer-002', 'skill-021', 'advanced'),  -- MySQL
('freelancer-002', 'skill-027', 'intermediate'),  -- Docker

-- 박민준: 신입 개발자
('freelancer-003', 'skill-001', 'beginner'),  -- React
('freelancer-003', 'skill-005', 'beginner'),  -- JavaScript
('freelancer-003', 'skill-007', 'intermediate'),  -- CSS3
('freelancer-003', 'skill-039', 'beginner'),  -- Git

-- 최지은: 데이터베이스 전문가
('freelancer-004', 'skill-021', 'expert'),  -- MySQL
('freelancer-004', 'skill-022', 'expert'),  -- PostgreSQL
('freelancer-004', 'skill-023', 'advanced'),  -- MongoDB
('freelancer-004', 'skill-024', 'advanced'),  -- Redis
('freelancer-004', 'skill-025', 'intermediate');  -- Elasticsearch

-- ==================== 9. 샘플 포트폴리오 ====================

INSERT INTO portfolio_item (id, freelancer_id, title, description, url, role, company, duration_months, technologies) VALUES
('port-001', 'freelancer-001', '전자상거래 플랫폼', 'React와 Node.js로 구축한 풀스택 전자상거래 플랫폼', 'https://example-ecommerce.com', '프론트엔드 리드', '테크스타트업', 12, '["React", "Node.js", "MongoDB", "Stripe"]'),
('port-002', 'freelancer-002', 'SaaS 플랫폼', 'Django와 React로 구축한 SaaS 플랫폼', 'https://example-saas.com', '풀스택 개발자', '엔터프라이즈 소프트웨어', 18, '["Django", "React", "PostgreSQL", "Docker"]'),
('port-003', 'freelancer-003', '개인 포트폴리오 사이트', 'React로 구축한 반응형 포트폴리오 웹사이트', 'https://example-portfolio.com', '개발자', '개인 프로젝트', 3, '["React", "Tailwind CSS", "JavaScript"]'),
('port-004', 'freelancer-004', '대규모 데이터베이스 최적화', '100만 사용자 규모 서비스의 데이터베이스 최적화', 'https://example-case-study.com', '데이터베이스 아키텍트', '대형 기술 회사', 12, '["PostgreSQL", "Redis", "Elasticsearch"]');

-- ==================== 10. 샘플 리뷰 ====================

INSERT INTO review (id, freelancer_id, rating, comment, project_name, reviewer_name) VALUES
('rev-001', 'freelancer-001', 4.8, '우수한 기술력과 의사소통 능력', '전자상거래 프로젝트', '클라이언트_1'),
('rev-002', 'freelancer-001', 4.5, '일정 관리가 탁월함', '모바일 앱 프로젝트', '클라이언트_2'),
('rev-003', 'freelancer-002', 4.7, '데이터베이스 설계가 뛰어남', 'SaaS 플랫폼', '클라이언트_3'),
('rev-004', 'freelancer-002', 4.6, '성능 최적화를 잘함', '추가 프로젝트', '클라이언트_4'),
('rev-005', 'freelancer-004', 4.9, '데이터베이스 최적화 전문가', '대규모 최적화', '클라이언트_5'),
('rev-006', 'freelancer-004', 4.8, '성능 향상 눈에 띔', '추가 프로젝트', '클라이언트_6');

-- ==================== 데이터 확인 ====================

SELECT '=== Freelancer Summary ===' as info;
SELECT COUNT(*) as total_freelancers FROM freelancer;
SELECT COUNT(*) as total_skills FROM skill;
SELECT COUNT(*) as total_portfolio_items FROM portfolio_item;
SELECT COUNT(*) as total_reviews FROM review;

SELECT '=== Interview Category Summary ===' as info;
SELECT COUNT(*) as total_categories FROM interview_category;
SELECT COUNT(*) as total_questions FROM interview_question;
SELECT COUNT(*) as total_checkpoints FROM interview_checkpoint;
SELECT COUNT(*) as total_red_flags FROM interview_red_flag;

-- ==================== END OF INIT DATA ====================
