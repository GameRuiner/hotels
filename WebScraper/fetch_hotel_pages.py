import requests
from time import sleep
import pymongo
from dotenv import load_dotenv
import os
import re

load_dotenv()

# TODO: merge into singleton
client = pymongo.MongoClient(os.environ["MONGO_HOST"])
db = client["hotels"]
hotel_col = db['hotels']

tmp_folder = 'tmp'

def fetch_hotel_pages(hotels):
  print(f"Fetching {len(hotels)} hotels")
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

if __name__ == '__main__':
  fetched_ids = set(
    os.path.splitext(filename)[0]
    for filename in os.listdir(tmp_folder)
    if filename.endswith('.html')
  )

  hotels = list(hotel_col.aggregate([
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
              'additional_info.hotel_class': {'$exists': False},
              'location_id': {'$nin': list(fetched_ids)}
          }
      },
      {
          '$project': {
              'web_url': 1,
              'location_id': 1
          }
      }
  ]))
  fetch_hotel_pages(hotels)