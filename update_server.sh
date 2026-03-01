#!/bin/bash
# 오라클 서버에서 실행할 업데이트 스크립트

echo "🔄 Updating cafemap backend..."

# 프로젝트 디렉토리로 이동
cd /opt/cafemap || exit 1

# Git pull
echo "📥 Pulling latest changes..."
git pull origin main

# 가상환경 활성화
source venv/bin/activate

# DB 스키마 업데이트
echo "🗄️ Updating database schema..."
python3 update_db_schema.py

# 서비스 재시작
echo "🔄 Restarting service..."
sudo systemctl restart cafemap

# 상태 확인
echo "✅ Service status:"
sudo systemctl status cafemap --no-pager

echo "✅ Update complete!"
