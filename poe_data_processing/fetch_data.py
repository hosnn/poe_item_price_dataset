import requests
import json
import os

# 데이터를 가져와 파일로 저장하는 함수
def fetch_and_save_data(domain, uri, save_folder):
  for domain_key, domain_url in domain.items():
    # 도메인별 하위 폴더 생성 (datas/kor, datas/eng)
    domain_folder = os.path.join(save_folder, domain_key)
    os.makedirs(domain_folder, exist_ok=True)

    for uri_key, uri_path in uri.items():
      try:
        # URL 구성
        full_url = f"{domain_url}{uri_path}"

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        # 데이터 요청
        response = requests.get(full_url, headers=headers)
        response.raise_for_status()  # HTTP 에러 확인
        
        # JSON 데이터 저장
        data = response.json()
        filename = f"{uri_key}.json"  # 파일명 생성
        file_path = os.path.join(domain_folder, filename)  # 저장 경로
        
        # 파일 저장
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        print(f"Data saved: {file_path}")
      except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data from {full_url}: {e}")


