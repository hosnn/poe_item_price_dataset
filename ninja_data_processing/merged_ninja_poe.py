import json
import os

def merge_single_pair(korean_data_file, english_data_file, output_file, kor_eng_key, eng_name_key, output_keys, league):
    """
    두 개의 JSON 파일을 특정 키를 기준으로 병합하여 새로운 JSON 파일을 생성합니다.

    Args:
        korean_data_file (str): 한국어 정보가 담긴 JSON 파일 경로.
        english_data_file (str): 영어 (poe.ninja) 정보가 담긴 JSON 파일 경로.
        output_file (str): 병합된 데이터가 저장될 새로운 JSON 파일 경로.
        kor_eng_key (str): 한국어 파일에서 영어 이름에 해당하는 키 (예: 'engType').
        eng_name_key (str): 영어 파일에서 아이템 이름에 해당하는 키 (예: 'name').
        output_keys (list): 최종 출력 파일에 포함될 키들의 리스트 (예: ['korType', 'engType', 'icon', 'chaosValue']).
    """
    print(f"\n--- Merging '{korean_data_file}' and '{english_data_file}' ---")
    try:
        with open(f"datas/split_detail/{korean_data_file}", 'r', encoding='utf-8') as f:
            kor_data = json.load(f)

        with open(f"datas/ninja/{league}/{english_data_file}", 'r', encoding='utf-8') as f:
            eng_data = json.load(f)

    except FileNotFoundError:
        print(f"Error: One or both files not found for this pair: '{korean_data_file}', '{english_data_file}'")
        return
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from one of the files in pair: '{korean_data_file}', '{english_data_file}'. Check file validity.")
        return

    merged_data = []

    # 영어 데이터를 빠르게 찾기 위해 딕셔너리로 변환
    # eng_data가 리스트 안에 'lines' 키를 가지고 있을 수 있으므로 확인
    eng_list = eng_data.get('lines', eng_data) # 'lines' 키가 없으면 eng_data 자체를 리스트로 간주
    if not isinstance(eng_list, list):
        print(f"Warning: '{english_data_file}' does not contain a 'lines' list or a direct list. Skipping this pair.")
        return

    eng_map = {item.get(eng_name_key): item for item in eng_list if item.get(eng_name_key) is not None}

    # 한국어 데이터가 'entries' 키를 가지고 있을 수 있으므로 확인
    kor_list = kor_data.get('entries', kor_data) # 'entries' 키가 없으면 kor_data 자체를 리스트로 간주
    if not isinstance(kor_list, list):
        print(f"Warning: '{korean_data_file}' does not contain an 'entries' list or a direct list. Skipping this pair.")
        return

    for kor_item in kor_list:
        kor_eng_value = kor_item.get(kor_eng_key)

        if kor_eng_value and kor_eng_value in eng_map:
            eng_item = eng_map[kor_eng_value]
            
            merged_entry = {}
            for key in output_keys:
                if key in kor_item: # 한국어 파일에 있는 키 우선
                    merged_entry[key] = kor_item.get(key)
                elif key in eng_item: # 영어 파일에 있는 키
                    merged_entry[key] = eng_item.get(key)
                else: # 양쪽에 없는 키는 None 또는 원하는 기본값으로 설정 가능
                    merged_entry[key] = None 
            
            # 여기서 korType, engType, icon, chaosValue 만을 명시적으로 포함
            # output_keys를 인자로 받아서 유연하게 처리
            final_entry = {
                'korType': merged_entry.get('korType'),
                'engType': merged_entry.get('engType'),
                'icon': merged_entry.get('icon'),
                'chaosValue': merged_entry.get('chaosValue')
            }
            merged_data.append(final_entry)

    # 결과 폴더 생성 (이미 존재하면 무시)
    os.makedirs("result", exist_ok=True)
    # 최종 출력 파일 경로 조합
    full_output_path = os.path.join("result", output_file)

    # 새로운 JSON 파일로 저장
    try:
        with open(f"{full_output_path}", 'w', encoding='utf-8') as f:
            json.dump(merged_data, f, indent=2, ensure_ascii=False)
        print(f"Successfully merged data into '{full_output_path}'")
    except IOError:
        print(f"Error: Could not write to file '{full_output_path}'. Check permissions.")