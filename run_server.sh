#!/bin/bash

# SuperManager 백엔드 서버 실행 스크립트

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║     🚀 SuperManager 백엔드 서버 시작                    ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 현재 디렉토리 확인
if [ ! -f "app.py" ]; then
    echo -e "${RED}❌ 오류: 백엔드 디렉토리에서 실행해주세요${NC}"
    echo "   cd /Users/doseunghyeon/developerApp/python/www.supermanger.com"
    exit 1
fi

# Python 확인
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python3이 설치되어 있지 않습니다${NC}"
    exit 1
fi

echo -e "${BLUE}📋 시스템 정보:${NC}"
echo "   Python: $(python3 --version)"
echo ""

# 1. 의존성 확인
echo -e "${YELLOW}1️⃣  의존성 확인 중...${NC}"
python3 -m pip list | grep -q Flask
if [ $? -eq 0 ]; then
    echo -e "   ${GREEN}✅ Flask 설치됨${NC}"
else
    echo -e "   ${YELLOW}⚠️  Flask가 없습니다. 설치 중...${NC}"
    pip install -r requirements.txt
fi
echo ""

# 2. 데이터베이스 초기화
echo -e "${YELLOW}2️⃣  데이터베이스 초기화 중...${NC}"
python3 setup.py
if [ $? -eq 0 ]; then
    echo -e "   ${GREEN}✅ 초기화 완료${NC}"
else
    echo -e "   ${RED}❌ 초기화 실패${NC}"
    exit 1
fi
echo ""

# 3. Flask 서버 시작
echo -e "${YELLOW}3️⃣  Flask 서버 시작 중...${NC}"
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✨ 서버가 시작되었습니다!${NC}"
echo ""
echo -e "   ${BLUE}🌐 API 주소: http://192.168.0.109:8000/api${NC}"
echo -e "   ${BLUE}📊 DB 주소: 192.168.0.109:3306${NC}"
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

python3 app.py
