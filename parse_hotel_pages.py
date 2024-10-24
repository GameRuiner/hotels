import re
import pymongo
from dotenv import load_dotenv
import os

load_dotenv()

client = pymongo.MongoClient(os.environ["MONGO_HOST"])
db = client["hotels"]
hotel_col = db['hotels']
fetched_hotel_pages = set([f.split('.')[0] for f in os.listdir('./tmp/')])
hotels_without_class = set([i['location_id'] for i in hotel_col.find({'hotel_class': {'$exists': False}}, {'location_id': 1})])

for location_id in fetched_hotel_pages.intersection(hotels_without_class):
  with open(f"./tmp/{location_id}.html", 'r', encoding="utf8") as hotel_page:
    match = re.search(r'(\d\.\d) of 5 stars', hotel_page.read())
    if match:
      hotel_class = float(match.group(1))
      result = hotel_col.update_one(
        {'location_id': location_id},
        {'$set': {'hotel_class': hotel_class}} 
      )
      if result.matched_count > 0:
        print(f"Successfully updated hotel_class {hotel_class} for location_id: {location_id}")
      else:
        print(f"No document found with location_id: {location_id}")
    else:
      print(f'Did not find class for {location_id}')

