import json

def process_json_for_regex(input_file, output_file):
    """
    JSON 파일에서 특정 필드를 제거하고 'regex: ""' 필드를 추가합니다.

    Args:
        input_file (str): 처리할 원본 JSON 파일 경로.
        output_file (str): 처리된 데이터가 저장될 새로운 JSON 파일 경로.
    """
    print(f"--- Processing '{input_file}' ---")
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

    except FileNotFoundError:
        print(f"Error: Input file not found: '{input_file}'")
        return
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from '{input_file}'. Check file validity.")
        return

    processed_data = []

    # 데이터가 리스트 형태인지 확인
    if not isinstance(data, list):
        print(f"Error: Expected a list of objects in '{input_file}', but got {type(data)}")
        return

    for item in data:
        new_item = {}
        # korType만 유지
        if 'korType' in item:
            new_item['korType'] = item['korType']
        
        # 'regex' 필드 추가
        new_item['regex'] = ''
        
        processed_data.append(new_item)

    # 새로운 JSON 파일로 저장
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(processed_data, f, indent=2, ensure_ascii=False)
        print(f"Successfully processed data and saved to '{output_file}'")
    except IOError:
        print(f"Error: Could not write to file '{output_file}'. Check permissions.")

def merge_and_fill_regex_same_key(empty_form_file, regex_source_file, output_file, match_key='korType'):
    """
    두 개의 JSON 파일을 동일한 키(match_key)를 기준으로 병합하고, 'regex' 필드를 채웁니다.
    매칭되는 항목이 없으면 'regex'를 공란으로 유지합니다.

    Args:
        empty_form_file (str): 'regex' 필드를 채울 대상이 되는 JSON 파일 경로 (empty_regex_form.json).
        regex_source_file (str): 'regex' 값을 가져올 JSON 파일 경로 (regex_form.json).
        output_file (str): 병합되고 채워진 데이터가 저장될 새로운 JSON 파일 경로.
        match_key (str): 두 파일에서 매칭 기준으로 사용할 키 (예: 'korType').
    """
    print(f"\n--- Merging '{empty_form_file}' and '{regex_source_file}' using key: '{match_key}' ---")
    try:
        with open(empty_form_file, 'r', encoding='utf-8') as f:
            empty_data = json.load(f)

        with open(regex_source_file, 'r', encoding='utf-8') as f:
            regex_data = json.load(f)

    except FileNotFoundError:
        print(f"Error: One or both files not found: '{empty_form_file}', '{regex_source_file}'")
        return
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from one of the files. Check file validity.")
        return

    merged_output = []

    # regex_data를 match_key를 키로 하는 딕셔너리로 변환하여 검색 속도 향상
    # (regex_form.json에 korType이 있다고 가정)
    regex_map = {item.get(match_key): item.get('regex', '') for item in regex_data if item.get(match_key) is not None}

    # empty_data의 각 항목을 순회하며 regex 값을 채움
    if not isinstance(empty_data, list):
        print(f"Error: Expected a list of objects in '{empty_form_file}', but got {type(empty_data)}")
        return

    for item in empty_data:
        current_item_match_value = item.get(match_key)
        
        # current_item_match_value가 regex_map에 있는지 확인
        if current_item_match_value and current_item_match_value in regex_map:
            item['regex'] = regex_map[current_item_match_value]
        else:
            # 일치하는 항목이 없으면 regex를 공란으로 유지 (이미 공란이더라도 명시적 처리)
            item['regex'] = '' 
        
        merged_output.append(item)

    # 새로운 JSON 파일로 저장
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(merged_output, f, indent=2, ensure_ascii=False)
        print(f"Successfully merged and filled regex to '{output_file}'")
    except IOError:
        print(f"Error: Could not write to file '{output_file}'. Check permissions.")

def merge_regex_to_scarabs(scarabs_file, regex_source_file, output_file, match_key='korType'):
    """
    merged_scarabs.json에 filled_regex_form.json의 'regex' 값을 'korType' 기준으로 합칩니다.
    매칭되는 항목이 없으면 'regex'를 공란으로 유지합니다.

    Args:
        scarabs_file (str): 'korType'과 'regex'를 추가할 대상이 되는 JSON 파일 경로 (merged_scarabs.json).
        regex_source_file (str): 'regex' 값을 가져올 JSON 파일 경로 (filled_regex_form.json).
        output_file (str): 병합되고 채워진 데이터가 저장될 새로운 JSON 파일 경로.
        match_key (str): 두 파일에서 매칭 기준으로 사용할 키 (기본값: 'korType').
    """
    print(f"\n--- Merging '{scarabs_file}' with regex from '{regex_source_file}' ---")
    try:
        with open(scarabs_file, 'r', encoding='utf-8') as f:
            scarabs_data = json.load(f)

        with open(regex_source_file, 'r', encoding='utf-8') as f:
            regex_data = json.load(f)

    except FileNotFoundError:
        print(f"Error: One or both files not found: '{scarabs_file}', '{regex_source_file}'")
        return
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from one of the files. Check file validity.")
        return

    # regex_data를 match_key를 키로 하는 딕셔너리로 변환하여 검색 속도 향상
    # filled_regex_form.json은 이미 'regex' 필드를 가지고 있다고 가정
    regex_map = {item.get(match_key): item.get('regex', '') for item in regex_data if item.get(match_key) is not None}

    # scarabs_data의 각 항목을 순회하며 regex 값을 채움
    if not isinstance(scarabs_data, list):
        print(f"Error: Expected a list of objects in '{scarabs_file}', but got {type(scarabs_data)}")
        return

    merged_scarabs_output = []
    for item in scarabs_data:
        current_kor_type = item.get(match_key)
        
        # korType이 regex_map에 있는지 확인
        if current_kor_type and current_kor_type in regex_map:
            item['regex'] = regex_map[current_kor_type]
        else:
            # 일치하는 항목이 없으면 'regex'를 공란으로 추가하거나 유지
            item['regex'] = '' 
        
        merged_scarabs_output.append(item)

    # 새로운 JSON 파일로 저장
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(merged_scarabs_output, f, indent=2, ensure_ascii=False)
        print(f"Successfully merged regex into scarabs data and saved to '{output_file}'")
    except IOError:
        print(f"Error: Could not write to file '{output_file}'. Check permissions.")

if __name__ == "__main__":
    input_json_file = 'result/merged_scarabs.json'
    output_json_file = 'regex/empty_regex_form.json'

    process_json_for_regex(input_json_file, output_json_file)

    empty_json_file = 'regex/empty_regex_form.json'
    regex_source_json_file = 'regex/regex_form.json'
    output_json_file = 'regex/filled_regex_form.json' 

    merge_and_fill_regex_same_key(empty_json_file, regex_source_json_file, output_json_file)