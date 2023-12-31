from dotenv import load_dotenv
import os
import requests
import json

load_dotenv() 

with open('ids.txt', encoding="utf8") as f:
  f.readlines
  ids_set = set([int(line) for line in f.readlines() if line])

hotels_folder = './hotels/'

# empty jsons cleaner

# for file in os.listdir(hotels_folder):
#    hotel_json = json.load(open(hotels_folder+file, 'r', encoding="utf8"))
#    if 'message' in hotel_json:
#       print(file)

existing_ids = set([int(file.split('.')[0]) for file in os.listdir(hotels_folder)])

added_ids = set()
total = len(ids_set)
proceed = 0
for hotel_id in ids_set:
  if hotel_id not in existing_ids:
    url = f'https://api.content.tripadvisor.com/api/v1/location/{hotel_id}/details?key={os.environ["TRIPADVISOR_KEY"]}&language=en&currency=USD'
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers).text
    response_json = json.loads(response)
    if 'message' in response_json:
      print(response_json['message'])
    else:
      with open(f'{hotels_folder}{hotel_id}.json', 'wt', encoding="utf8") as f:
        f.write(response)
        added_ids.add(hotel_id)
        proceed += 1
        print(f'{proceed}/{total}')


with open('ids.txt',  'wt', encoding="utf8") as f:
  f.write('')
  for not_added_id in ids_set.difference(added_ids):
    f.write(not_added_id+'\n')