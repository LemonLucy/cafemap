# CoffeeMap React Native

카공 최적화 카페 찾기 앱

## 개발 환경 설정

### 필수 요구사항
- Node.js 18+
- React Native CLI
- Android Studio (Android)
- Xcode (iOS, macOS만)

### 설치

```bash
npm install
```

### 실행

**Android:**
```bash
npx react-native run-android
```

**iOS:**
```bash
cd ios && pod install && cd ..
npx react-native run-ios
```

## 프로젝트 구조

```
src/
├── screens/       # 화면 컴포넌트
├── components/    # 재사용 가능한 컴포넌트
├── services/      # API 서비스
├── types/         # TypeScript 타입 정의
└── utils/         # 유틸리티 함수
```

## 백엔드 연동

`src/services/api.ts`에서 `API_BASE_URL`을 실제 서버 URL로 변경하세요.

```typescript
const API_BASE_URL = 'https://your-server.com';
```

## TODO

- [ ] 카카오맵 SDK 연동
- [ ] 위치 기반 카페 검색
- [ ] 카페 리스트 UI
- [ ] 상세 정보 모달
- [ ] 캐시 관리
- [ ] 로그인/회원가입
- [ ] 즐겨찾기 기능

## 기존 웹 버전

웹 버전은 `/coffeemap` 디렉토리에 있습니다.
