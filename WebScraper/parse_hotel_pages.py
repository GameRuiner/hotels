import re
import pymongo
from dotenv import load_dotenv
import os
from tqdm import tqdm

load_dotenv()

client = pymongo.MongoClient(os.environ["MONGO_HOST"])
db = client["hotels"]
hotel_col = db['hotels']
hotel_additional_col = db['hotels_additional_info']
fetched_hotel_pages = set([f.split('.')[0] for f in os.listdir('./tmp/')])
hotels_without_class = set([i['location_id'] for i in hotel_col.aggregate([
    {
        '$lookup': {
            'from': 'hotels_additional_info',
            'localField': 'location_id',
            'foreignField': 'location_id',
            'as': 'additional_info'
        }
    },
    {
        '$match': {
            'additional_info.hotel_class': {'$exists': False} 
        }
    },
    {
        '$project': {
            'location_id': 1
        }
    }
])])


ids = fetched_hotel_pages.intersection(hotels_without_class)

succeeded_update = []
document_not_found = []
not_found_class = []

for location_id in tqdm(ids, desc="Parsing hotel pages") :
  with open(f"./tmp/{location_id}.html", 'r', encoding="utf8") as hotel_page:
    match = re.search(r'(\d\.\d) of 5 stars', hotel_page.read())
    if match:
      hotel_class = float(match.group(1))
      result = hotel_additional_col.update_one(
        {'location_id': location_id}, 
        {'$set': {'hotel_class': hotel_class}}, 
        upsert=True
      )
      if result.raw_result['ok']:
        succeeded_update.append(location_id)
      else:
        document_not_found.append(location_id)
    else:
      not_found_class.append(location_id)

