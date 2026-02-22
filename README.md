# CoffeeMap React Native

카공 최적화 카페 찾기 앱 - 네이버 블로그 분석 기반

## ✨ 주요 기능

- 📍 위치 기반 카페 검색 (카카오맵 API)
- 📊 블로그 분석 기반 종합 점수 (최대 5점)
- 🔌 작업 환경 분석 (콘센트, 소음, 공간감)
- 📝 네이버 블로그 리뷰 수집 및 분석
- 💾 로컬 캐시 (24시간)
- 🎯 정렬 기능 (평점, 거리)

## 📱 스크린샷

- 카페 리스트 (신호등 색상으로 평점 표시)
- 상세 정보 모달 (작업 적합도, 콘센트, 소음 등)
- 블로그 리뷰 링크

## 🛠 기술 스택

- React Native 0.73
- TypeScript
- React Navigation
- Axios
- AsyncStorage
- Geolocation Service

## 📦 설치 및 실행

### 1. 의존성 설치
```bash
npm install
```

### 2. 환경 설정

`src/services/api.ts` 파일에서 API 설정:

```typescript
const API_BASE_URL = 'YOUR_BACKEND_URL';
const KAKAO_API_KEY = 'YOUR_KAKAO_API_KEY';
```

### 3. Android 실행

```bash
npx react-native run-android
```

### 4. iOS 실행 (macOS만)

```bash
cd ios && pod install && cd ..
npx react-native run-ios
```

## 🏗 프로젝트 구조

```
src/
├── screens/
│   └── MapScreen.tsx          # 메인 화면 (검색, 리스트, 정렬)
├── components/
│   ├── CafeListItem.tsx       # 카페 리스트 아이템
│   ├── CafeDetailModal.tsx    # 상세 정보 모달
│   └── CafeInfo.tsx           # 카페 정보 표시
├── services/
│   └── api.ts                 # API 서비스 (카카오맵, 백엔드)
├── utils/
│   └── cache.ts               # AsyncStorage 캐시 관리
└── types/
    └── index.ts               # TypeScript 타입 정의
```

## 📊 점수 산정 방식

### 종합 점수 (최대 5점)

1. **작업 적합도** (최대 2.8점)
   - 블로그에서 "카공", "작업", "공부" 등 키워드 분석
   
2. **콘센트** (최대 0.4점)
   - 모든 좌석: 0.4점
   - 50% 정도: 0.28점
   - 벽면에만: 0.2점

3. **소음 레벨** (최대 0.3점)
   - 독서실 수준: 0.3점
   - 잔잔한 음악: 0.21점
   - 보통: 0.15점

4. **공간감** (최대 0.8점)
   - 매우 넓음: 0.8점
   - 넓은 편: 0.5점

5. **WiFi** (최대 0.4점)
6. **리뷰 개수** (최대 0.3점)

### 신호등 색상
- 🟢 초록: 3.7점 이상
- 🟡 노랑: 2.5~3.6점
- 🔴 빨강: 2.5점 미만
- ⚪ 회색: 분석 전

## 🔧 백엔드 연동

백엔드는 Python Flask 서버 사용:
- 위치: `/coffeemap/app_server.py`
- 포트: 5000
- API: `/api/blog-search`

## 📝 TODO

- [ ] 지도 뷰 추가 (WebView + 카카오맵)
- [ ] 즐겨찾기 기능
- [ ] 로그인/회원가입
- [ ] 푸시 알림
- [ ] 카페 리뷰 작성
- [ ] 필터링 기능 (WiFi, 콘센트 등)

## 🚀 배포

### Google Play Store
1. 서명 키 생성
2. `android/app/build.gradle` 설정
3. AAB 빌드: `cd android && ./gradlew bundleRelease`
4. Play Console 업로드

### App Store (iOS)
1. Xcode에서 Archive
2. App Store Connect 업로드
3. TestFlight 테스트
4. 심사 제출

## 📄 라이선스

MIT

## 👤 개발자

Lucy - [GitHub](https://github.com/LemonLucy/cafemap)
