from dotenv import load_dotenv
import os
import requests
import json
import pymongo

load_dotenv() 

client = pymongo.MongoClient(os.environ["MONGO_HOST"])
db = client["hotels"]
col = db["hotels"]

def fetch_hotels(ids_set):
  existing_ids = set([i['location_id'] for i in col.find({}, {'location_id': 1})])
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
        added_ids.add(hotel_id)
        filter_criteria = {'location_id': response_json['location_id']}
        col.update_one(filter_criteria, {'$set': response_json}, upsert=True)
        proceed += 1
        # TODO update with tqdm
        print(f'{proceed}/{total}')
  not_added_ids = ids_set.difference(added_ids)
  if len(not_added_ids) > 0:
    print('Not added', not_added_ids)