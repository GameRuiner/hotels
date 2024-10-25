import requests
from time import sleep
import pymongo
from dotenv import load_dotenv
import os
import re

load_dotenv()

client = pymongo.MongoClient(os.environ["MONGO_HOST"])
db = client["hotels"]
hotel_col = db['hotels']

# TODO: intersect with existing pages?
hotels = list(hotel_col.find({'hotel_class': {'$exists': False}}, {'web_url': 1, 'location_id': 1}))

def fetch_hotel_pages(hotels):
  headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'referer': 'https://www.tripadvisor.com/',
  }
  for hotel in hotels:
    req = requests.get(hotel['web_url'], headers=headers)
    content = req.text
    match = re.search(r'captcha-delivery', content)
    if match:
      print(f"Request to {hotel['location_id']} was blocked")
      break
    with open(f"./tmp/{hotel['location_id']}.html", 'w+', encoding="utf8") as hotel_page:
      hotel_page.write(content)
    sleep(1)

print(f"Fetching {len(hotels)} hotels")
fetch_hotel_pages(hotels)