from dotenv import load_dotenv
import os
import requests
import json
import pymongo
from tqdm import tqdm

load_dotenv()

client = pymongo.MongoClient(os.environ["MONGO_HOST"])
db = client["hotels"]
col = db["hotels"]


def fetch_hotels(ids_set):
  existing_ids = set([i['location_id']
                     for i in col.find({}, {'location_id': 1})])
  added_ids = set()
  fetched_hotels = []

  for hotel_id in tqdm(ids_set, desc="Fetching hotel documents"):
    if hotel_id not in existing_ids:
      url = f'https://api.content.tripadvisor.com/api/v1/location/{hotel_id}/details?key={os.environ["TRIPADVISOR_KEY"]}&language=en&currency=USD'
      headers = {"accept": "application/json"}
      response = requests.get(url, headers=headers).text
      response_json = json.loads(response)
      if 'message' in response_json:
        print(response_json['message'])
        return False
      else:
        added_ids.add(hotel_id)
        filter_criteria = {'location_id': response_json['location_id']}
        col.update_one(filter_criteria, {'$set': response_json}, upsert=True)
        fetched_hotels.append(
          {'location_id': response_json['location_id'], 'web_url': response_json['web_url']})
  not_added_ids = ids_set.difference(added_ids)
  if len(not_added_ids) > 0:
    print('Not added', not_added_ids)
  return fetched_hotels
