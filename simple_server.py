from http.server import HTTPServer, SimpleHTTPRequestHandler
import json

demo_data = [
    {"name": "스타벅스 강남역점", "address": "서울 강남구 강남대로 지하 396", "phone": "02-123-4567", "x": "127.027926", "y": "37.497952", "keywords": {"power_outlet": True, "quietness": False, "vibe": True}, "blog_count": 12},
    {"name": "투썸플레이스 강남점", "address": "서울 강남구 테헤란로 123", "phone": "02-234-5678", "x": "127.028", "y": "37.498", "keywords": {"power_outlet": True, "quietness": True, "vibe": True}, "blog_count": 8},
    {"name": "카페베네 역삼점", "address": "서울 강남구 역삼동 456", "phone": "02-345-6789", "x": "127.029", "y": "37.499", "keywords": {"power_outlet": False, "quietness": True, "vibe": False}, "blog_count": 5},
    {"name": "블루보틀 삼성점", "address": "서울 강남구 삼성동 789", "phone": "02-456-7890", "x": "127.030", "y": "37.500", "keywords": {"power_outlet": True, "quietness": True, "vibe": True}, "blog_count": 15}
]

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/cafes':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(demo_data, ensure_ascii=False).encode('utf-8'))
        elif self.path == '/':
            self.path = '/index.html'
            return SimpleHTTPRequestHandler.do_GET(self)
        else:
            return SimpleHTTPRequestHandler.do_GET(self)

print('🚀 Venue app running at http://localhost:5000')
print('📝 Note: Using demo data. Enable Kakao Local API to see real cafes.')
HTTPServer(('', 5000), Handler).serve_forever()
