import json
import os

UNIQUE_TYPES = ['accessory', 'armour', 'weapon', 'flask', 'jewel', 'map']


def _load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def _save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _build_unique_eng_to_kor():
    # datas/split/*.json 의 entries 에는 유니크 아이템의 engName/korName 이 들어있다.
    eng_to_kor = {}
    for name in UNIQUE_TYPES:
        path = f'datas/split/{name}.json'
        if not os.path.exists(path):
            continue
        for entry in _load_json(path).get('entries', []):
            eng, kor = entry.get('engName'), entry.get('korName')
            if eng and kor and eng not in eng_to_kor:
                eng_to_kor[eng] = kor
    return eng_to_kor


def merge_unique(league, output_file='result/merged_unique.json'):
    """poe.ninja 고유 아이템 시세 + 한글 이름. 같은 이름 여러 행(변형)은 매물이 가장 많은 행 하나만 사용."""
    eng_to_kor = _build_unique_eng_to_kor()
    best = {}

    for type_name in UNIQUE_TYPES:
        path = f'datas/ninja/{league}/unique_{type_name}.json'
        if not os.path.exists(path):
            print(f"[merge_unique] 파일 없음, 건너뜀: {path}")
            continue
        for line in _load_json(path).get('lines', []):
            name = line.get('name')
            # Foulborn 은 일반 버전과 이름이 겹치면서 가격이 전혀 다르므로 제외
            if not name or name.startswith('Foulborn '):
                continue
            current = best.get(name)
            if current is None or (line.get('listingCount') or 0) > (current.get('listingCount') or 0):
                best[name] = line

    result = []
    unmapped = 0
    for eng_name, line in best.items():
        kor_name = eng_to_kor.get(eng_name)
        if not kor_name:
            unmapped += 1
            continue
        result.append({
            'korName': kor_name,
            'engName': eng_name,
            'baseType': line.get('baseType'),
            'icon': line.get('icon'),
            'chaosValue': line.get('chaosValue') or 0,
            'listingCount': line.get('listingCount') or 0,
        })

    result.sort(key=lambda x: x['chaosValue'], reverse=True)
    _save_json(output_file, result)
    print(f"[merge_unique] {len(result)}개 저장 (한글 이름 매핑 실패 {unmapped}개 제외) -> {output_file}")


def merge_card(league, output_file='result/merged_card.json'):
    """poe.ninja 점술 카드 시세 + 한글 이름."""
    ninja_path = f'datas/ninja/{league}/card.json'
    kor_path = 'datas/split/card.json'
    if not os.path.exists(ninja_path) or not os.path.exists(kor_path):
        print(f"[merge_card] 필요한 파일 없음, 건너뜀: {ninja_path}, {kor_path}")
        return

    eng_to_kor = {
        e.get('engType'): e.get('korType')
        for e in _load_json(kor_path).get('entries', [])
        if e.get('engType') and e.get('korType')
    }

    result = []
    unmapped = 0
    for line in _load_json(ninja_path).get('lines', []):
        eng_name = line.get('name')
        kor_name = eng_to_kor.get(eng_name)
        if not eng_name or not kor_name:
            unmapped += 1
            continue
        result.append({
            'korType': kor_name,
            'engType': eng_name,
            'icon': line.get('icon'),
            'chaosValue': line.get('chaosValue') or 0,
            'volume': line.get('volume') or 0,
        })

    result.sort(key=lambda x: x['chaosValue'], reverse=True)
    _save_json(output_file, result)
    print(f"[merge_card] {len(result)}개 저장 (한글 이름 매핑 실패 {unmapped}개 제외) -> {output_file}")
