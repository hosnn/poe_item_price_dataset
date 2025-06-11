import json
import os

# 파일 경로 설정
eng_file_path = "datas/eng/items.json"
kor_file_path = "datas/kor/items.json"
output_file_path = "datas/merged/items.json"

# JSON 데이터 읽기
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# 데이터 병합
def merge_json(eng_data, kor_data):
    merged_result = []

    for eng_item, kor_item in zip(eng_data['result'], kor_data['result']):
        if eng_item['id'] != kor_item['id']:
            raise ValueError(f"Mismatched IDs: {eng_item['id']} vs {kor_item['id']}")
        
        merged_entries = []
        for eng_entry, kor_entry in zip(eng_item['entries'], kor_item['entries']):
            # 기본 병합
            merged_entry = {
                "korType": kor_entry.get('type'),
                "engType": eng_entry.get('type')
            }

            # 조건부로 속성 추가
            if 'text' in eng_entry:
                merged_entry["engText"] = eng_entry['text']
            if 'text' in kor_entry:
                merged_entry["korText"] = kor_entry['text']
            if 'name' in eng_entry:
                merged_entry["engName"] = eng_entry['name']
            if 'name' in kor_entry:
                merged_entry["korName"] = kor_entry['name']

            # 중복 제거 처리 (공통 속성)
            common_keys = set(eng_entry.keys()).intersection(kor_entry.keys())
            for key in common_keys:
                if eng_entry[key] == kor_entry[key]:  # 값이 동일한 경우 한 번만 추가
                    merged_entry[key] = eng_entry[key]

            # 나머지 추가 속성 처리
            merged_entry.update({f"eng_{k}": v for k, v in eng_entry.items() if k not in ['type', 'text', 'name'] and k not in common_keys})
            merged_entry.update({f"kor_{k}": v for k, v in kor_entry.items() if k not in ['type', 'text', 'name'] and k not in common_keys})

            merged_entries.append(merged_entry)
        
        merged_result.append({
            "id": eng_item['id'],
            "labelKor": kor_item.get('label'),
            "labelEng": eng_item.get('label'),
            "entries": merged_entries
        })

    return {"result": merged_result}

# 메인 실행 로직
def items_merged():
    # JSON 파일 로드
    eng_data = load_json(eng_file_path)
    kor_data = load_json(kor_file_path)

    # 데이터 병합
    merged_data = merge_json(eng_data, kor_data)

    # 출력 디렉토리 생성
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    # 병합된 JSON 저장
    with open(output_file_path, 'w', encoding='utf-8') as file:
        # json.dump(merged_data, file, ensure_ascii=False, indent=4) # 가독성 들여쓰기
        json.dump(merged_data, file, ensure_ascii=False, separators=(',', ':')) # 들여쓰기 제거

    print(f"Merged JSON saved at {output_file_path}")
