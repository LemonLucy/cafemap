import requests
import json
import re

# API credentials
KAKAO_API_KEY = "ad534f7d1e1d1b0c9fd81b194aafe281"
NAVER_CLIENT_ID = "Acsdbniypoa33q2mwIkQ"
NAVER_CLIENT_SECRET = "n7rPAfQjvw"

def search_cafes(query, x, y, radius=1000):
    """Search cafes using Kakao Local API"""
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": f"KakaoAK {KAKAO_API_KEY}"}
    params = {"query": query, "category_group_code": "CE7", "x": x, "y": y, "radius": radius}
    
    response = requests.get(url, headers=headers, params=params)
    return response.json().get("documents", [])

def search_naver_blogs(cafe_name, cafe_address):
    """Search Naver blogs for a specific cafe"""
    url = "https://openapi.naver.com/v1/search/blog.json"
    headers = {"X-Naver-Client-Id": NAVER_CLIENT_ID, "X-Naver-Client-Secret": NAVER_CLIENT_SECRET}
    params = {"query": f"{cafe_name} {cafe_address}", "display": 5, "sort": "date"}
    
    response = requests.get(url, headers=headers, params=params)
    return response.json().get("items", [])

def extract_keywords(blog_posts):
    """Extract keywords from blog snippets"""
    keywords = {"power_outlet": False, "quietness": False, "vibe": False}
    combined_text = " ".join([post.get("description", "") for post in blog_posts])
    
    # Remove HTML tags
    combined_text = re.sub(r'<[^>]+>', '', combined_text)
    
    if re.search(r'콘센트|충전|전원|power', combined_text, re.IGNORECASE):
        keywords["power_outlet"] = True
    if re.search(r'조용|quiet|집중', combined_text, re.IGNORECASE):
        keywords["quietness"] = True
    if re.search(r'분위기|vibe|감성|무드', combined_text, re.IGNORECASE):
        keywords["vibe"] = True
    
    return keywords

def build_pipeline(query, x, y):
    """Main pipeline to fetch and merge cafe data"""
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

if __name__ == "__main__":
    # Example: Search cafes near Gangnam Station
    data = build_pipeline("카페", "127.027926", "37.497952")
    print(json.dumps(data, ensure_ascii=False, indent=2))
