#!/usr/bin/env python3
"""세션 테이블 추가 스크립트"""
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

def update_schema():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    # 세션 테이블 생성
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            token VARCHAR(255) PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            email VARCHAR(255) NOT NULL,
            nickname VARCHAR(50) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP DEFAULT (CURRENT_TIMESTAMP + INTERVAL '30 days')
        );
    """)
    
    # 인덱스 생성
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);
        CREATE INDEX IF NOT EXISTS idx_sessions_expires ON sessions(expires_at);
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    print('✅ Sessions table created successfully')

if __name__ == '__main__':
    update_schema()
