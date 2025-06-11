import json
import os

# JSON 데이터 읽기
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# leagues 병합 함수
def merge_leagues(kor_data, eng_data):
    merged_result = []

    for kor_item, eng_item in zip(kor_data["result"], eng_data["result"]):
        if kor_item["id"] != eng_item["id"]:
            raise ValueError(f"Mismatched IDs: {kor_item['id']} vs {eng_item['id']}")

        merged_result.append({
            "id": kor_item["id"],
            "realm": kor_item["realm"],
            "korText": kor_item["text"],
            "engText": eng_item["text"]
        })

    return {"result": merged_result}

# 메인 실행
def leagues_merged():
    kor_file_path = "datas/kor/leagues.json"
    eng_file_path = "datas/eng/leagues.json"
    output_file_path = "datas/merged/leagues.json"

    kor_data = load_json(kor_file_path)
    eng_data = load_json(eng_file_path)

    merged_data = merge_leagues(kor_data, eng_data)

    # 출력 디렉토리 생성 및 저장
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    with open(output_file_path, "w", encoding="utf-8") as file:
        # json.dump(merged_data, file, ensure_ascii=False, indent=4) # 가독성 들여쓰기
        json.dump(merged_data, file, ensure_ascii=False, separators=(',', ':')) # 들여쓰기 제거


    print(f"Merged JSON saved to {output_file_path}")