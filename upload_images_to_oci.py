#!/usr/bin/env python3
"""
네이버 블로그 이미지를 오라클 Object Storage에 업로드
"""
import os
import requests
from bs4 import BeautifulSoup
import hashlib
import oci

# OCI 설정
config = oci.config.from_file("~/.oci/config", "DEFAULT")
object_storage = oci.object_storage.ObjectStorageClient(config)
namespace = "ax91qzradksx"
bucket_name = "cafemap-images"

def download_and_upload_blog_images(blog_url, cafe_name, max_images=5):
    """블로그에서 이미지 다운로드 후 Object Storage에 업로드"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'Referer': 'https://blog.naver.com/'
        }
        
        # 모바일 URL을 PC URL로 변환
        if 'm.blog.naver.com' in blog_url:
            blog_url = blog_url.replace('m.blog.naver.com', 'blog.naver.com')
        
        response = requests.get(blog_url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # iframe 태그에서 실제 주소(src)를 가져옴
        main_frame = soup.find('iframe', id='mainFrame')
        if not main_frame:
            return []
        
        actual_url = "https://blog.naver.com" + main_frame['src']
        
        # 실제 본문 페이지 접속
        res = requests.get(actual_url, headers=headers, timeout=5)
        content_soup = BeautifulSoup(res.text, 'html.parser')
        
        # 이미지 태그 찾기
        img_tags = content_soup.select('img[src*="postfiles.pstatic.net"]')
        
        uploaded_urls = []
        
        for i, img in enumerate(img_tags[:max_images]):
            img_url = img.get('data-lazy-src') or img.get('src')
            if not img_url:
                continue
            
            # URL 정리
            img_url = img_url.split('?')[0]
            
            # 이미지 다운로드
            img_response = requests.get(img_url, headers=headers, timeout=10)
            if img_response.status_code != 200:
                continue
            
            # 파일명 생성 (해시 기반)
            url_hash = hashlib.md5(img_url.encode()).hexdigest()
            ext = os.path.splitext(img_url)[1] or '.jpg'
            object_name = f"cafes/{cafe_name.replace(' ', '_')}/{url_hash}{ext}"
            
            # Object Storage에 업로드
            object_storage.put_object(
                namespace,
                bucket_name,
                object_name,
                img_response.content
            )
            
            # Public URL 생성
            public_url = f"https://objectstorage.ap-chuncheon-1.oraclecloud.com/n/{namespace}/b/{bucket_name}/o/{object_name}"
            uploaded_urls.append(public_url)
            
            print(f"  ✅ 업로드: {object_name}")
        
        return uploaded_urls
        
    except Exception as e:
        print(f"  ❌ 오류: {e}")
        return []

if __name__ == "__main__":
    # 테스트: 스태그커피 안양
    test_url = "https://blog.naver.com/2_sen_/224064644984"
    print("테스트: 스태그커피 안양")
    print(f"블로그: {test_url}")
    print("")
    
    urls = download_and_upload_blog_images(test_url, "스태그커피_안양", max_images=5)
    
    print(f"\n업로드된 이미지 {len(urls)}개:")
    for url in urls:
        print(f"  {url}")
