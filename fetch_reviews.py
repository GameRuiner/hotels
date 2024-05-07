from dotenv import load_dotenv
import os
import requests
import json
import pymongo

load_dotenv() 

client = pymongo.MongoClient(os.environ["MONGO_HOST"])
db = client["hotels"]
hotel_col = db['hotels']
col = db["reviews"]

existing_ids = set([str(i['_id']) for i in col.aggregate([{"$group": {"_id": "$location_id"}}])])
ids_set = set([i['location_id'] for i in hotel_col.find({}, {'location_id': 1})])

added_ids = set()
total = len(ids_set)
proceed = 0
for hotel_id in ids_set:
  if hotel_id not in existing_ids:
    url = f'https://api.content.tripadvisor.com/api/v1/location/{hotel_id}/reviews?key={os.environ["TRIPADVISOR_KEY"]}&language=en'
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers).text
    response_json = json.loads(response)
    if 'message' in response_json:
      print(response_json['message'])
    else:
      for review in response_json['data']:
        filter_criteria = {'id': review['id']}
        col.update_one(filter_criteria, {'$set': review}, upsert=True)
      added_ids.add(hotel_id)
      proceed += 1
      print(f'{proceed}/{total}')
