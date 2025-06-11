import requests
import json
import os

# 데이터를 가져와 파일로 저장하는 함수
def fetch_and_save_data(domain, leagues, categories, save_folder):
  for leagues_key, leagues_url in leagues.items():

    leagues_folder = os.path.join(save_folder, leagues_key)
    os.makedirs(leagues_folder, exist_ok=True)

    for categories_key, categories_path in categories.items():
      try:
        # URL 구성
        full_url = f"{domain}?league={leagues_url}&type={categories_path}"

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        # 데이터 요청
        response = requests.get(full_url, headers=headers)
        response.raise_for_status()  # HTTP 에러 확인
        
        # JSON 데이터 저장
        data = response.json()
        
        # 필요한 필드만 추출
        filtered_data = {
            "lines": [
                {
                    'id': item.get('id'),
                    'name': item.get('name'),
                    'icon': item.get('icon'),
                    'chaosValue': item.get('chaosValue')
                }
                for item in data.get('lines', [])
            ]
        }
        
        filename = f"{categories_key}.json"  # 파일명 생성
        file_path = os.path.join(leagues_folder, filename)  # 저장 경로
        
        # 파일 저장
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(filtered_data, f, ensure_ascii=False, indent=4)
        
        print(f"Data saved: {file_path}")
      except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data from {full_url}: {e}")


