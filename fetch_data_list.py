from poe_data_processing.fetch_data import fetch_and_save_data
from poe_data_processing.items_merged import items_merged
from poe_data_processing.leagues_merged import leagues_merged
from poe_data_processing.splite_category import split_json_by_id, extract_and_save_currency_types

DOMAIN = {
  'eng': 'https://www.pathofexile.com',
  'kor': 'https://poe.game.daum.net'
}

URI = {
  "leagues": "/api/trade/data/leagues",
  "items": "/api/trade/data/items",
  # "stats": "/api/trade/data/stats",
  # "static": "/api/trade/data/static",
  # "filters": "/api/trade/data/filters"
}

save_folder = "datas"
fetch_and_save_data(DOMAIN, URI, save_folder)
leagues_merged()
items_merged()

split_json_by_id()

input_filepath = "datas/split/currency.json"
output_dir = "datas/split_detail"
target_types = ["징조", "문신", "룬", "성유"]
extract_and_save_currency_types(input_filepath, output_dir, target_types)

input_filepath = "datas/split/map.json"
target_types = ["갑충석", "올플레임"]
extract_and_save_currency_types(input_filepath, output_dir, target_types)