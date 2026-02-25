#!/usr/bin/env python3
"""
오라클 DB에 카페 데이터 프리로드 (이미지 URL 포함)
"""
import os
import sys
import time
from app_server import search_naver_blog, get_blog_image_url
from cache_db import init_cache_db, save_cached_result

# 환경변수 설정
os.environ['DATABASE_URL'] = 'postgresql://cafemap:CafeMap2026!@#@localhost:5432/cafemap'
os.environ['NAVER_CLIENT_ID'] = 'tr30Ch1tbJBqwNlv9svx'
os.environ['NAVER_CLIENT_SECRET'] = 'fsrn1wXmk3'

CACHE_VERSION = "v18"

# 주요 브랜드 카페
BRANDS = [
    "스타벅스", "투썸플레이스", "이디야", "커피빈", "할리스",
    "탐앤탐스", "파스쿠찌", "엔제리너스", "빽다방", "메가커피",
    "컴포즈커피", "폴바셋", "카페베네", "더벤티", "커피베이"
]

# 서울 주요 지역
SEOUL_AREAS = [
    "강남", "서초", "송파", "강동", "광진", "성동", "중구", "종로",
    "용산", "마포", "서대문", "은평", "노원", "도봉", "강북", "성북",
    "동대문", "중랑", "영등포", "동작", "관악", "구로", "금천", "양천", "강서"
]

# 경기 주요 도시
GYEONGGI_CITIES = [
    "수원", "성남", "고양", "용인", "부천", "안산", "안양",
    "남양주", "화성", "평택", "의정부", "시흥", "파주", "김포"
]

def preload_cafe(query, region):
    """카페 데이터 프리로드"""
    print(f"\n🔍 검색: {query} {region}")
    
    try:
        # analyze_blog_content 함수 사용 (전체 분석 결과 반환)
        from app_server import analyze_blog_content
        
        result = analyze_blog_content(query, region)
        if not result or result.get('totalScore', 0) == 0:
            print(f"  ❌ 검색 실패 또는 결과 없음")
            return False
        
        cafe_name = result.get('cafeName', query)
        cafe_address = result.get('address', region)
        
        # 이미지 URL 추출
        image_url = None
        blogs = result.get('blogs', [])
        if blogs:
            first_blog = blogs[0]
            blog_link = first_blog.get('url')  # 'url' 키 사용
            if blog_link:
                print(f"  📷 이미지 추출 중... ({blog_link[:50]}...)")
                image_url = get_blog_image_url(blog_link)
                if image_url:
                    print(f"  ✅ 이미지: {image_url[:60]}...")
                else:
                    print(f"  ⚠️  이미지 추출 실패")
        
        # DB에 저장
        save_cached_result(cafe_name, cafe_address, CACHE_VERSION, result, image_url)
        print(f"  💾 저장 완료: {cafe_name} ({cafe_address})")
        
        time.sleep(0.5)  # API rate limit
        return True
        
    except Exception as e:
        print(f"  ❌ 오류: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("🚀 오라클 DB 카페 데이터 프리로드 시작")
    print("=" * 60)
    
    # DB 초기화
    init_cache_db()
    
    total = 0
    success = 0
    
    # 1. 서울 브랜드 카페
    print("\n📍 서울 브랜드 카페 프리로드")
    for brand in BRANDS:
        for area in SEOUL_AREAS[:10]:  # 주요 10개 지역만
            if preload_cafe(brand, f"서울 {area}"):
                success += 1
            total += 1
    
    # 2. 경기 브랜드 카페
    print("\n📍 경기 브랜드 카페 프리로드")
    for brand in BRANDS[:5]:  # 주요 5개 브랜드만
        for city in GYEONGGI_CITIES[:5]:  # 주요 5개 도시만
            if preload_cafe(brand, f"경기 {city}"):
                success += 1
            total += 1
    
    print("\n" + "=" * 60)
    print(f"✅ 프리로드 완료: {success}/{total} 성공")
    print("=" * 60)

if __name__ == "__main__":
    main()
