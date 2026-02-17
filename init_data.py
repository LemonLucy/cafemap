from database import init_db, save_cafes

# Sample data to populate database
sample_cafes = [
    {"name": "스타벅스 강남역점", "address": "서울 강남구 강남대로 지하 396", "phone": "02-123-4567", "x": "127.027926", "y": "37.497952", "keywords": {"power_outlet": True, "quietness": False, "vibe": True}, "blog_count": 12},
    {"name": "투썸플레이스 강남점", "address": "서울 강남구 테헤란로 123", "phone": "02-234-5678", "x": "127.028", "y": "37.498", "keywords": {"power_outlet": True, "quietness": True, "vibe": True}, "blog_count": 8},
    {"name": "카페베네 역삼점", "address": "서울 강남구 역삼동 456", "phone": "02-345-6789", "x": "127.029", "y": "37.499", "keywords": {"power_outlet": False, "quietness": True, "vibe": False}, "blog_count": 5},
    {"name": "블루보틀 삼성점", "address": "서울 강남구 삼성동 789", "phone": "02-456-7890", "x": "127.030", "y": "37.500", "keywords": {"power_outlet": True, "quietness": True, "vibe": True}, "blog_count": 15}
]

init_db()
save_cafes(sample_cafes)
print(f'✅ Initialized database with {len(sample_cafes)} sample cafes')
print('📝 Once Kakao API is working, visit: http://localhost:5000/api/refresh')
