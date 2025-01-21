from dotenv import load_dotenv
from tqdm import tqdm
import os
import requests
import json
import pymongo

load_dotenv()

client = pymongo.MongoClient(os.environ["MONGO_HOST"])
db = client["hotels"]
hotel_col = db['hotels']
photo_col = db["photos"]

existing_ids = set([str(i['_id'])
                   for i in photo_col.aggregate([{"$group": {"_id": "$location_id"}}])])
ids_set = set([i['location_id']
              for i in hotel_col.find({}, {'location_id': 1})])
added_ids = set()
total = len(ids_set)
for hotel_id in tqdm(ids_set, desc="Fetching hotel photos"):
  if hotel_id not in existing_ids:
    url = f'https://api.content.tripadvisor.com/api/v1/location/{hotel_id}/photos?key={os.environ["TRIPADVISOR_KEY"]}&language=en&source=Expert'
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers, timeout=500).text
    response_json = json.loads(response)
    if 'message' in response_json:
      print(response_json['message'])
      if 'message' == 'Limit Exceeded':
        break
    else:
      filter_criteria = {'location_id': hotel_id}
      photos = {'photos': response_json['data'], 'location_id': hotel_id}
      photo_col.update_one(filter_criteria, {'$set': photos}, upsert=True)
      added_ids.add(hotel_id)
