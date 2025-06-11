import json
import os

def split_json_by_id():
  input_filepath = "datas/merged/items.json"
  output_dir = "datas/split"
  
  # 출력 디렉토리가 없으면 생성
  if not os.path.exists(output_dir):
    os.makedirs(output_dir)

  try:
    with open(input_filepath, 'r', encoding='utf-8') as f:
      data = json.load(f)

    # 'result' 키가 존재하는지 확인
    if "result" not in data or not isinstance(data["result"], list):
      print(f"오류: '{input_filepath}' 파일에 'result' 키가 없거나 리스트 형태가 아닙니다.")
      return

    for item in data["result"]:
      if "id" in item:
        item_id = item["id"]
        output_filename = f"{item_id}.json"
        output_filepath = os.path.join(output_dir, output_filename)

        with open(output_filepath, 'w', encoding='utf-8') as outfile:
          json.dump(item, outfile, indent=2, ensure_ascii=False) # JSON 파일 들여쓰기는 여전히 2칸
        print(f"ID '{item_id}' 데이터가 '{output_filepath}' 에 저장되었습니다.")
      else:
        print(f"경고: 'id' 키가 없는 항목이 발견되어 건너뜁니다: {item}")

  except FileNotFoundError:
    print(f"오류: '{input_filepath}' 파일을 찾을 수 없습니다.")
  except json.JSONDecodeError:
    print(f"오류: '{input_filepath}' 파일이 유효한 JSON 형식이 아닙니다.")
  except Exception as e:
    print(f"처리 중 오류 발생: {e}")


def extract_and_save_currency_types(input_filepath, output_dir, target_types):

  if not os.path.exists(output_dir):
    os.makedirs(output_dir)

  extracted_data = {key: [] for key in target_types} # 각 타입별로 데이터를 저장할 딕셔너리

  try:
    with open(input_filepath, 'r', encoding='utf-8') as f:
      data = json.load(f)

    if "entries" not in data or not isinstance(data["entries"], list):
      print(f"오류: '{input_filepath}' 파일에 'entries' 키가 없거나 리스트 형태가 아닙니다.")
      return

    for entry in data["entries"]:
      kor_type = entry.get("korType", "") # 'korType'이 없을 경우 빈 문자열 반환
      for target_type in target_types:
        if target_type in kor_type:
          extracted_data[target_type].append(entry)
          break # 해당 항목은 하나의 target_type에만 포함시키고 다음 항목으로 넘어감

    for target_type, items in extracted_data.items():
      if items: # 해당 타입에 추출된 항목이 있을 경우에만 파일로 저장
        output_filename = f"{target_type}.json"
        output_filepath = os.path.join(output_dir, output_filename)

        # 원본 currency.json의 구조를 유지하면서 entries만 필터링하여 저장
        output_json_data = {
          "id": f"{target_type}",
          "entries": items
        }

        with open(output_filepath, 'w', encoding='utf-8') as outfile:
          json.dump(output_json_data, outfile, indent=2, ensure_ascii=False)
        print(f"'{target_type}' 관련 데이터가 '{output_filepath}' 에 저장되었습니다.")
      else:
        print(f"'{target_type}' 에 해당하는 항목이 '{input_filepath}' 에서 발견되지 않았습니다.")

  except FileNotFoundError:
    print(f"오류: '{input_filepath}' 파일을 찾을 수 없습니다.")
  except json.JSONDecodeError:
    print(f"오류: '{input_filepath}' 파일이 유효한 JSON 형식이 아닙니다.")
  except Exception as e:
    print(f"처리 중 오류 발생: {e}")