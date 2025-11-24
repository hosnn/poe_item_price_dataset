from ninja_data_processing.fetch_data import fetch_and_save_data
from ninja_data_processing.merged_ninja_poe import merge_single_pair
from make_regex_form import merge_regex_to_scarabs

def main():
  DOMAIN = {
    'currency': 'https://poe.ninja/api/data/currencyoverview',
    'item': 'https://poe.ninja/api/data/itemoverview',
  }

  LEAGUES = {
    # 'standard': 'Standard',
    'Keepers' : 'Keepers',
  }

  CATEGORIES = {
    'scarab': 'Scarab',
    'tattoo': 'Tattoo',
    'omen': 'Omen',
    'rune': 'Runegraft',
    'oil': 'Oil',
  }

  save_folder = "datas/ninja"  # 저장 폴더 이름
  fetch_and_save_data(DOMAIN['item'], LEAGUES, CATEGORIES, save_folder)

  # 병합할 파일 쌍 정의
    # 각 딕셔너리는 하나의 병합 작업을 나타냅니다.
    # 'kor_data_file': 한국어 파일 경로
    # 'eng_data_file': 영어 파일 경로 (poe.ninja)
    # 'output_file': 병합된 결과가 저장될 파일 경로
    # 'kor_eng_key': 한국어 파일에서 매칭 기준으로 사용할 영어 이름 키 (ex: 'engType')
    # 'eng_name_key': 영어 파일에서 매칭 기준으로 사용할 이름 키 (ex: 'name')
    # 'output_keys': 최종 출력에 포함시킬 키들의 리스트
    
  merge_configurations = [
      {
          'kor_data_file': '갑충석.json',
          'eng_data_file': 'scarab.json',
          'output_file': 'merged_scarabs.json',
          'kor_eng_key': 'engType',
          'eng_name_key': 'name',
          'output_keys': ['korType', 'engType', 'icon', 'chaosValue']
      },
      {
          'kor_data_file': '룬.json',
          'eng_data_file': 'rune.json',
          'output_file': 'merged_rune.json',
          'kor_eng_key': 'engType', 
          'eng_name_key': 'name',
          'output_keys': ['korType', 'engType', 'icon', 'chaosValue']
      },
      {
          'kor_data_file': '문신.json',
          'eng_data_file': 'tattoo.json',
          'output_file': 'merged_tattoo.json',
          'kor_eng_key': 'engType', 
          'eng_name_key': 'name',
          'output_keys': ['korType', 'engType', 'icon', 'chaosValue']
      },
      {
          'kor_data_file': '성유.json',
          'eng_data_file': 'oil.json',
          'output_file': 'merged_oil.json',
          'kor_eng_key': 'engType', 
          'eng_name_key': 'name',
          'output_keys': ['korType', 'engType', 'icon', 'chaosValue']
      },
  ]

  league = 'Keepers'

  # 각 설정을 반복하며 병합 함수 호출
  for config in merge_configurations:
      merge_single_pair(
          config['kor_data_file'],
          config['eng_data_file'],
          config['output_file'],
          config['kor_eng_key'],
          config['eng_name_key'],
          config['output_keys'],
          league
      )

  scarabs_file = 'result/merged_scarabs.json'
  regex_source_file = 'regex/filled_regex_form.json'

  # 'korType'을 기준으로 두 파일을 합침
  merge_regex_to_scarabs(scarabs_file, regex_source_file, scarabs_file, match_key='korType')

if __name__ == "__main__":
    main()