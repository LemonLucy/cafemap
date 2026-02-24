# 오라클 클라우드 배포 가이드

## 필요한 정보

배포 전에 준비해야 할 것들:

1. **네이버 API 키** (필수)
   - Client ID
   - Client Secret
   - 발급: https://developers.naver.com/apps/#/register

2. **PostgreSQL DB** (선택)
   - Railway DB 계속 사용 가능
   - 또는 오라클 Autonomous Database 사용
   - DATABASE_URL 형식: `postgresql://user:password@host:port/dbname`

3. **Railway 환경변수 확인**
   ```bash
   railway login
   railway variables
   ```

## 1. 인스턴스 생성
- **Shape**: VM.Standard.A1.Flex (ARM Ampere)
- **CPU**: 2 OCPU
- **RAM**: 12GB
- **OS**: Ubuntu 22.04 (Minimal)
- **Boot Volume**: 50GB

## 2. SSH 접속
```bash
ssh -i <your-private-key.pem> ubuntu@<your-instance-ip>
```

## 3. 배포 스크립트 실행
```bash
# 스크립트 다운로드
wget https://raw.githubusercontent.com/LemonLucy/cafemap/main/deploy_oracle.sh

# 실행 권한 부여
chmod +x deploy_oracle.sh

# 실행
./deploy_oracle.sh
```

## 4. 오라클 클라우드 방화벽 설정
인스턴스 대시보드에서:
1. **Virtual Cloud Networks** → 사용 중인 VCN 선택
2. **Security Lists** → Default Security List 선택
3. **Ingress Rules** 추가:
   - Source CIDR: `0.0.0.0/0`
   - Destination Port: `80`
   - Protocol: TCP

## 5. 서비스 관리 명령어
```bash
# 서비스 상태 확인
sudo systemctl status cafemap

# 서비스 재시작
sudo systemctl restart cafemap

# 로그 실시간 확인
sudo journalctl -u cafemap -f

# Nginx 재시작
sudo systemctl restart nginx
```

## 6. Vercel 프론트엔드 업데이트
프론트엔드 코드에서 API URL을 오라클 인스턴스 IP로 변경:
```javascript
const API_URL = 'http://<oracle-instance-ip>';
```

## 7. 환경변수 수정 (필요시)
```bash
sudo nano /opt/cafemap/.env
sudo systemctl restart cafemap
```

## 8. 자동 업데이트 스크립트
```bash
cd /opt/cafemap
git pull
sudo systemctl restart cafemap
```

## 주의사항
- 오라클 무료 티어는 CPU 사용률이 너무 낮으면 계정이 정지될 수 있으니 주기적으로 확인하세요
- 고정 IP를 할당받았다면 반드시 인스턴스에 연결해두세요 (미사용 시 과금)
- PostgreSQL DB가 필요하면 같은 인스턴스에 설치하거나 Autonomous Database 사용 가능
