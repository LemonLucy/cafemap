import psycopg2
from psycopg2.extras import RealDictCursor
import bcrypt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)

# 세션 관리
def create_session(token, user_id, email, nickname):
    conn = get_db()
    cur = conn.cursor()
    expires_at = datetime.now() + timedelta(days=30)
    cur.execute(
        "INSERT INTO sessions (token, user_id, email, nickname, expires_at) VALUES (%s, %s, %s, %s, %s)",
        (token, user_id, email, nickname, expires_at)
    )
    conn.commit()
    cur.close()
    conn.close()

def get_session(token):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM sessions WHERE token = %s AND expires_at > NOW()",
        (token,)
    )
    session = cur.fetchone()
    cur.close()
    conn.close()
    return dict(session) if session else None

def delete_session(token):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM sessions WHERE token = %s", (token,))
    conn.commit()
    cur.close()
    conn.close()

def cleanup_expired_sessions():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM sessions WHERE expires_at < NOW()")
    conn.commit()
    cur.close()
    conn.close()

# 사용자 관리
def create_user(email, password, nickname):
    conn = get_db()
    cur = conn.cursor()
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    cur.execute("INSERT INTO users (email, password_hash, nickname) VALUES (%s, %s, %s) RETURNING id", 
                (email, password_hash, nickname))
    user_id = cur.fetchone()['id']
    conn.commit()
    cur.close()
    conn.close()
    return user_id

def verify_user(email, password):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if user and bcrypt.checkpw(password.encode(), user['password_hash'].encode()):
        return dict(user)
    return None

# 리뷰 관리
def add_review(user_id, cafe_id, rating, content):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO reviews (user_id, cafe_id, rating, content) VALUES (%s, %s, %s, %s) RETURNING id",
                (user_id, cafe_id, rating, content))
    review_id = cur.fetchone()['id']
    conn.commit()
    cur.close()
    conn.close()
    return review_id

def update_review(review_id, user_id, rating, content):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE reviews SET rating = %s, content = %s WHERE id = %s AND user_id = %s",
        (rating, content, review_id, user_id)
    )
    updated = cur.rowcount > 0
    conn.commit()
    cur.close()
    conn.close()
    return updated

def delete_review(review_id, user_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM reviews WHERE id = %s AND user_id = %s", (review_id, user_id))
    deleted = cur.rowcount > 0
    conn.commit()
    cur.close()
    conn.close()
    return deleted

def get_cafe_reviews(cafe_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT r.*, u.nickname FROM reviews r 
        JOIN users u ON r.user_id = u.id 
        WHERE r.cafe_id = %s ORDER BY r.created_at DESC
    """, (cafe_id,))
    reviews = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(r) for r in reviews]

def get_user_reviews(user_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM reviews WHERE user_id = %s ORDER BY created_at DESC", (user_id,))
    reviews = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(r) for r in reviews]

# 좋아요 관리
def toggle_like(user_id, cafe_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id FROM likes WHERE user_id = %s AND cafe_id = %s", (user_id, cafe_id))
    existing = cur.fetchone()
    
    if existing:
        cur.execute("DELETE FROM likes WHERE user_id = %s AND cafe_id = %s", (user_id, cafe_id))
        liked = False
    else:
        cur.execute("INSERT INTO likes (user_id, cafe_id) VALUES (%s, %s)", (user_id, cafe_id))
        liked = True
    
    conn.commit()
    cur.close()
    conn.close()
    return liked

def get_user_likes(user_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT cafe_id FROM likes WHERE user_id = %s", (user_id,))
    likes = cur.fetchall()
    cur.close()
    conn.close()
    return [l['cafe_id'] for l in likes]

def get_cafe_like_count(cafe_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) as count FROM likes WHERE cafe_id = %s", (cafe_id,))
    count = cur.fetchone()['count']
    cur.close()
    conn.close()
    return count
