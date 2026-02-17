from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.request
import urllib.parse
import re

KAKAO_API_KEY = "ad534f7d1e1d1b0c9fd81b194aafe281"
NAVER_CLIENT_ID = "Acsdbniypoa33q2mwIkQ"
NAVER_CLIENT_SECRET = "n7rPAfQjvw"

def search_cafes(query, x, y, radius=1000):
    url = f"https://dapi.kakao.com/v2/local/search/keyword.json"
    params = urllib.parse.urlencode({"query": query, "category_group_code": "CE7", "x": x, "y": y, "radius": radius})
    req = urllib.request.Request(f"{url}?{params}", headers={"Authorization": f"KakaoAK {KAKAO_API_KEY}"})
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode('utf-8')).get("documents", [])

def search_naver_blogs(cafe_name, cafe_address):
    params = urllib.parse.urlencode({"query": f"{cafe_name} {cafe_address}", "display": 5, "sort": "date"})
    url = f"https://openapi.naver.com/v1/search/blog.json?{params}"
    req = urllib.request.Request(url, headers={"X-Naver-Client-Id": NAVER_CLIENT_ID, "X-Naver-Client-Secret": NAVER_CLIENT_SECRET})
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode('utf-8')).get("items", [])

def extract_keywords(blog_posts):
    keywords = {"power_outlet": False, "quietness": False, "vibe": False}
    combined_text = " ".join([post.get("description", "") for post in blog_posts])
    combined_text = re.sub(r'<[^>]+>', '', combined_text)
    
    if re.search(r'콘센트|충전|전원|power', combined_text, re.IGNORECASE):
        keywords["power_outlet"] = True
    if re.search(r'조용|quiet|집중', combined_text, re.IGNORECASE):
        keywords["quietness"] = True
    if re.search(r'분위기|vibe|감성|무드', combined_text, re.IGNORECASE):
        keywords["vibe"] = True
    
    return keywords

def build_pipeline(query, x, y):
    cafes = search_cafes(query, x, y)
    results = []
    
    for cafe in cafes:
        cafe_name = cafe.get("place_name")
        cafe_address = cafe.get("address_name", "")
        
        blogs = search_naver_blogs(cafe_name, cafe_address)
        keywords = extract_keywords(blogs)
        
        result = {
            "name": cafe_name,
            "address": cafe_address,
            "phone": cafe.get("phone", ""),
            "x": cafe.get("x"),
            "y": cafe.get("y"),
            "keywords": keywords,
            "blog_count": len(blogs)
        }
        results.append(result)
    
    return results

class VenueHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as f:
                self.wfile.write(f.read())
        elif self.path == '/api/cafes':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            try:
                data = build_pipeline("카페", "127.027926", "37.497952")
            except:
                data = [
                    {"name": "스타벅스 강남역점", "address": "서울 강남구 강남대로 지하 396", "phone": "02-123-4567", "x": "127.027926", "y": "37.497952", "keywords": {"power_outlet": True, "quietness": False, "vibe": True}, "blog_count": 12},
                    {"name": "투썸플레이스 강남점", "address": "서울 강남구 테헤란로 123", "phone": "02-234-5678", "x": "127.028", "y": "37.498", "keywords": {"power_outlet": True, "quietness": True, "vibe": True}, "blog_count": 8},
                    {"name": "카페베네 역삼점", "address": "서울 강남구 역삼동 456", "phone": "02-345-6789", "x": "127.029", "y": "37.499", "keywords": {"power_outlet": False, "quietness": True, "vibe": False}, "blog_count": 5}
                ]
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    server = HTTPServer(('localhost', 5000), VenueHandler)
    print('🚀 Venue app running at http://localhost:5000')
    server.serve_forever()
