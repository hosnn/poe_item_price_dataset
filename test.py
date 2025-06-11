import json

for category in ["갑충석", "룬", "문신", "징조"]:
  try:
    with open(f"datas/split_detail/{category}.json", 'r', encoding='utf-8') as f:
      data = json.load(f)

    if "entries" in data:
      array = data["entries"]
      if isinstance(array, list):
        size = len(array)
        print(f"{category}의 개수: {size}")
  except Exception as e:
    print(f"처리 중 오류 발생: {e}")
