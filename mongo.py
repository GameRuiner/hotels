import pymongo
import os
import json
from dotenv import load_dotenv

load_dotenv() 

client = pymongo.MongoClient(os.environ["MONGO_HOST"])


def copy_hotels():
  db = client["hotels"]
  col = db["hotels"]
  hotels_folder = "./hotels/"

  for filename in os.listdir(hotels_folder):
    if filename == '.gitkeep': continue
    hotel_json = json.load(open(hotels_folder+filename, 'r', encoding="utf8"))
    filter_criteria = {'location_id': hotel_json['location_id']}
    col.update_one(filter_criteria, {'$set': hotel_json}, upsert=True)


def copy_reviews():
  db = client["hotels"]
  col = db["reviews"]
  folder = "./reviews/"

  for filename in os.listdir(folder):
    if filename == '.gitkeep': continue
    reviews_json = json.load(open(folder+filename, 'r', encoding="utf8"))
    if 'data' not in reviews_json:
      continue 
    for review in reviews_json['data']:
      filter_criteria = {'id': review['id']}
      col.update_one(filter_criteria, {'$set': review}, upsert=True)

copy_reviews()

