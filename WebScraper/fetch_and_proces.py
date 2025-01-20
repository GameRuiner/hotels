import sys
import json
from time import sleep

from crawler import scrape_ids
from fetch_hotels import fetch_hotels

locationId = sys.argv[1]
limit = int(sys.argv[2])

with open('fetched_cities.json') as f:
    fetched_cities = json.load(f)
    city = fetched_cities[locationId]
    print(city)
    print(f"Fetching hotels for {city['name']}, {city['country']}")
    offset_start = city["fetched"]

total_hotels = scrape_ids(locationId, fetch_total=True)
print(total_hotels, 'hotels')
offsets = [i for i in range(offset_start, total_hotels + 1, 30)]
for offset in offsets:
  if offset >= limit:
    break
  hotels = scrape_ids(locationId, offset = f'oa{offset}')
  fetch_hotels(hotels)
  sleep(1)