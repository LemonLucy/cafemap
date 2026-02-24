import os
import json
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.getenv('DATABASE_URL')

def get_db_connection():
    """PostgreSQL 연결"""
    if not DATABASE_URL:
        return None
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

def init_cache_db():
    """캐시 테이블 생성"""
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS cafe_cache (
                    id SERIAL PRIMARY KEY,
                    cafe_name VARCHAR(255) NOT NULL,
                    cafe_address VARCHAR(500) NOT NULL,
                    region VARCHAR(100),
                    cache_version VARCHAR(20),
                    result JSONB NOT NULL,
                    hit_count INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(cafe_name, cafe_address, cache_version)
                )
            """)
            
            # 인덱스 생성
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_cafe_lookup 
                ON cafe_cache(cafe_name, cafe_address, cache_version)
            """)
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_region 
                ON cafe_cache(region)
            """)
            
            conn.commit()
            print("✅ Cache DB initialized")
    except Exception as e:
        print(f"❌ Cache DB init error: {e}")
    finally:
        conn.close()

def should_cache_to_postgres(cafe_address, total_score, hit_count=1):
    """Postgres 저장 여부 결정"""
    # 서울은 무조건 저장
    if '서울' in cafe_address:
        return True
    
    # 경기/인천 주요 도시
    major_cities = ['수원', '성남', '고양', '용인', '부천', '안산', '안양', '남양주', '화성', '평택', '인천']
    if any(city in cafe_address for city in major_cities):
        return True
    
    # 지방 도시는 조회 2회 이상 또는 고득점
    if hit_count >= 2 or total_score >= 3.0:
        return True
    
    return False

def get_region_from_address(address):
    """주소에서 지역 추출"""
    parts = address.split()
    if len(parts) > 0:
        # "서울특별시" → "서울", "경기도 수원시" → "수원"
        region = parts[0].replace('특별시', '').replace('광역시', '').replace('도', '')
        if len(parts) > 1 and '시' in parts[1]:
            region = parts[1].replace('시', '')
        return region
    return 'unknown'

def get_cached_result(cafe_name, cafe_address, cache_version):
    """캐시에서 결과 조회 (Postgres → 메모리 순)"""
    # 1차: 메모리 캐시
    from app_server import blog_cache
    cache_key = f"{cache_version}_{cafe_name}_{cafe_address}"
    if cache_key in blog_cache:
        return blog_cache[cache_key]
    
    # 2차: Postgres
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT result, hit_count FROM cafe_cache 
                WHERE cafe_name = %s AND cafe_address = %s AND cache_version = %s
            """, (cafe_name, cafe_address, cache_version))
            
            row = cur.fetchone()
            if row:
                # 조회수 증가
                cur.execute("""
                    UPDATE cafe_cache 
                    SET hit_count = hit_count + 1, updated_at = CURRENT_TIMESTAMP
                    WHERE cafe_name = %s AND cafe_address = %s AND cache_version = %s
                """, (cafe_name, cafe_address, cache_version))
                conn.commit()
                
                # 메모리 캐시에도 저장
                result = row['result']
                blog_cache[cache_key] = result
                return result
    except Exception as e:
        print(f"❌ Cache read error: {e}")
    finally:
        conn.close()
    
    return None

def save_cached_result(cafe_name, cafe_address, cache_version, result):
    """결과를 캐시에 저장"""
    from app_server import blog_cache, MAX_CACHE_SIZE
    
    # 메모리 캐시에 항상 저장
    cache_key = f"{cache_version}_{cafe_name}_{cafe_address}"
    if len(blog_cache) >= MAX_CACHE_SIZE:
        oldest_key = next(iter(blog_cache))
        del blog_cache[oldest_key]
    blog_cache[cache_key] = result
    
    # Postgres 저장 여부 결정
    region = get_region_from_address(cafe_address)
    total_score = result.get('totalScore', 0)
    
    if not should_cache_to_postgres(cafe_address, total_score):
        return  # 메모리만 저장
    
    # Postgres에 저장
    conn = get_db_connection()
    if not conn:
        return
    
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO cafe_cache (cafe_name, cafe_address, region, cache_version, result)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (cafe_name, cafe_address, cache_version) 
                DO UPDATE SET 
                    result = EXCLUDED.result,
                    hit_count = cafe_cache.hit_count + 1,
                    updated_at = CURRENT_TIMESTAMP
            """, (cafe_name, cafe_address, region, cache_version, json.dumps(result)))
            conn.commit()
            print(f"💾 Cached to Postgres: {cafe_name} ({region})")
    except Exception as e:
        print(f"❌ Cache save error: {e}")
    finally:
        conn.close()

def get_cache_stats():
    """캐시 통계"""
    conn = get_db_connection()
    if not conn:
        return {"error": "DB not connected"}
    
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    COUNT(*) as total_cafes,
                    SUM(hit_count) as total_hits,
                    COUNT(DISTINCT region) as regions,
                    pg_size_pretty(pg_total_relation_size('cafe_cache')) as db_size
                FROM cafe_cache
            """)
            stats = cur.fetchone()
            
            cur.execute("""
                SELECT region, COUNT(*) as count 
                FROM cafe_cache 
                GROUP BY region 
                ORDER BY count DESC 
                LIMIT 10
            """)
            top_regions = cur.fetchall()
            
            return {
                "stats": dict(stats),
                "top_regions": [dict(r) for r in top_regions]
            }
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()
