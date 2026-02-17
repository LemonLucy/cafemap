from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import urllib.request
import urllib.parse
import re
import os
from database import init_db, save_cafes, get_cafes

# Load from environment variables or use placeholders
KAKAO_API_KEY = os.getenv("KAKAO_API_KEY", "YOUR_KAKAO_REST_API_KEY_HERE")
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID", "YOUR_NAVER_CLIENT_ID_HERE")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET", "YOUR_NAVER_CLIENT_SECRET_HERE")

def search_cafes(query, x, y, radius=1000):
    params = urllib.parse.urlencode({"query": query, "category_group_code": "CE7", "x": x, "y": y, "radius": radius})
    url = f"https://dapi.kakao.com/v2/local/search/keyword.json?{params}"
    req = urllib.request.Request(url, headers={"Authorization": f"KakaoAK {KAKAO_API_KEY}"})
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

def classify_category(keywords, combined_text):
    if re.search(r'노트북|작업|업무|스터디|공부|work', combined_text, re.IGNORECASE) or keywords["power_outlet"]:
        return "work"
    elif re.search(r'힐링|여유|편안|relax|쉬', combined_text, re.IGNORECASE):
        return "relax"
    elif re.search(r'자연|정원|테라스|야외|nature|green', combined_text, re.IGNORECASE):
        return "nature"
    elif keywords["vibe"]:
        return "unique"
    return "relax"

def fetch_and_store():
    cafes = search_cafes("카페", "127.027926", "37.497952")
    results = []
    
    for cafe in cafes:
        cafe_name = cafe.get("place_name")
        cafe_address = cafe.get("address_name", "")
        
        blogs = search_naver_blogs(cafe_name, cafe_address)
        combined_text = " ".join([post.get("description", "") for post in blogs])
        combined_text = re.sub(r'<[^>]+>', '', combined_text)
        keywords = extract_keywords(blogs)
        category = classify_category(keywords, combined_text)
        
        result = {
            "name": cafe_name,
            "address": cafe_address,
            "phone": cafe.get("phone", ""),
            "latitude": float(cafe.get("y")),
            "longitude": float(cafe.get("x")),
            "keywords": keywords,
            "blog_count": len(blogs),
            "category": category
        }
        results.append(result)
    
    save_cafes(results)
    return results

class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/cafes':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            data = get_cafes()
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
        elif self.path == '/api/refresh':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            try:
                data = fetch_and_store()
                self.wfile.write(json.dumps({"status": "success", "count": len(data)}, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))
        elif self.path == '/':
            self.path = '/index.html'
            return SimpleHTTPRequestHandler.do_GET(self)
        else:
            return SimpleHTTPRequestHandler.do_GET(self)
    
    def do_POST(self):
        if self.path == '/api/cafes':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            cafes = json.loads(post_data.decode('utf-8'))
            
            results = []
            for cafe in cafes:
                result = {
                    "name": cafe.get("name"),
                    "address": cafe.get("address"),
                    "phone": cafe.get("phone", ""),
                    "latitude": cafe.get("latitude"),
                    "longitude": cafe.get("longitude"),
                    "keywords": cafe.get("keywords", {}),
                    "blog_count": cafe.get("blog_count", 0),
                    "category": cafe.get("category", "relax")
                }
                results.append(result)
            
            save_cafes(results)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "success", "count": len(results)}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

init_db()
print('🚀 Venue app running at http://localhost:5000')
print('📊 Database: venue.db')
print('🔄 Refresh data: http://localhost:5000/api/refresh')
HTTPServer(('', 5000), Handler).serve_forever()
