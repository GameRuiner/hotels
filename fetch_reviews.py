from dotenv import load_dotenv
import os
import requests
import json
import pymongo

load_dotenv() 

reviews_folder = './reviews/'
hotels_folder = './hotels/'

existing_ids = set([int(file.split('.')[0]) for file in os.listdir(reviews_folder) if file != '.gitkeep'])
ids_set = set([int(file.split('.')[0]) for file in os.listdir(hotels_folder) if file != '.gitkeep'])

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
      client = pymongo.MongoClient(os.environ["MONGO_HOST"])
      db = client["hotels"]
      col = db["reviews"]
      filter_criteria = {'id': response_json['id']}
      col.update_one(filter_criteria, {'$set': response_json}, upsert=True)
      added_ids.add(hotel_id)
      proceed += 1
      print(f'{proceed}/{total}')
