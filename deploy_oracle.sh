#!/bin/bash
# 오라클 클라우드 Ubuntu 서버 배포 스크립트

echo "=== 카공맵 백엔드 오라클 클라우드 배포 ==="

# 1. 시스템 업데이트
sudo apt update && sudo apt upgrade -y

# 2. Python 3.12 설치
sudo apt install -y python3.12 python3.12-venv python3-pip

# 3. Nginx 설치
sudo apt install -y nginx

# 4. 방화벽 설정 (오라클 클라우드)
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
sudo netfilter-persistent save

# 5. 프로젝트 디렉토리 생성
sudo mkdir -p /opt/cafemap
sudo chown $USER:$USER /opt/cafemap
cd /opt/cafemap

# 6. Git 클론
git clone https://github.com/LemonLucy/cafemap.git .

# 7. 가상환경 생성 및 패키지 설치
python3.12 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

# 8. 환경변수 설정 (수동으로 입력 필요)
echo ""
echo "=== 환경변수 설정 ==="
read -p "NAVER_CLIENT_ID 입력: " NAVER_ID
read -p "NAVER_CLIENT_SECRET 입력: " NAVER_SECRET
read -p "DATABASE_URL 입력 (선택, PostgreSQL 사용시): " DB_URL

cat > .env << EOF
NAVER_CLIENT_ID=${NAVER_ID}
NAVER_CLIENT_SECRET=${NAVER_SECRET}
PORT=8000
${DB_URL:+DATABASE_URL=${DB_URL}}
EOF

# 9. systemd 서비스 파일 생성
sudo tee /etc/systemd/system/cafemap.service > /dev/null << 'EOF'
[Unit]
Description=Cafemap Backend Server
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/opt/cafemap
Environment="PATH=/opt/cafemap/venv/bin"
EnvironmentFile=/opt/cafemap/.env
ExecStart=/opt/cafemap/venv/bin/python3 app_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 10. Nginx 설정
sudo tee /etc/nginx/sites-available/cafemap > /dev/null << 'EOF'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_cache_bypass $http_upgrade;
        
        # CORS 헤더
        add_header 'Access-Control-Allow-Origin' '*' always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS' always;
        add_header 'Access-Control-Allow-Headers' 'Content-Type' always;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/cafemap /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# 11. 서비스 시작
sudo systemctl daemon-reload
sudo systemctl enable cafemap
sudo systemctl start cafemap
sudo systemctl restart nginx

echo ""
echo "=== 배포 완료! ==="
echo "서비스 상태 확인: sudo systemctl status cafemap"
echo "로그 확인: sudo journalctl -u cafemap -f"
echo "Nginx 상태: sudo systemctl status nginx"
echo ""
echo "외부 IP 확인 후 Vercel 프론트엔드의 API URL을 업데이트하세요!"
