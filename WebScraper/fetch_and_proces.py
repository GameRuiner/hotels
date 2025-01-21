import sys
import json

from crawler import scrape_ids
from fetch_hotels import fetch_hotels
from fetch_hotel_pages import fetch_hotel_pages

locationId = sys.argv[1]
limit = int(sys.argv[2])

with open('fetched_cities.json') as f:
    fetched_cities = json.load(f)
    city = fetched_cities[locationId]
    print(f"Fetching hotels for {city['name']}, {city['country']}")
    offset_start = city["fetched"]

total_hotels = scrape_ids(locationId, fetch_total=True)
print('Total hotels', total_hotels)
offsets = [i for i in range(offset_start, total_hotels + 1, 30)]
for offset in offsets:
  if offset >= limit:
    break
  hotels = scrape_ids(locationId, offset = f'oa{offset}')
  fetched_hotels = fetch_hotels(hotels)
  fetch_hotel_pages(fetched_hotels)

fetched_cities[locationId]['fetched'] = limit
with open('fetched_cities.json', "w") as f:
  json.dump(fetched_cities, f)