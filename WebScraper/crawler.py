import requests
from time import sleep
from bs4 import BeautifulSoup
import re
import json
import sys

def fetch_hotels(locationId, offset='', fetch_total=False):
  print('Fetching', locationId, 'with offset', offset)
  headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'referer': 'https://www.tripadvisor.com/',
  }
  req = requests.get(
    f'https://www.tripadvisor.com/Hotels-g{locationId}-{offset}', headers=headers)
  content = req.text
  soup = BeautifulSoup(content, features="html.parser")
  with open('ids.txt', mode="at", encoding="utf8") as ids:
    for link in soup.select('[data-automation="hotel-card-title"] a'):
      ids.write(re.search('-d\d+\-', link['href']).group(0)[2:-1] + '\n')
  if fetch_total:
    soup = BeautifulSoup(content, features="html.parser")
    total_text = soup.select('.F1 .b')[0]
    total_str = re.search('\d+(,\d+)*', total_text.text).group(0)
    return int(total_str.replace(',', ''))


locationId = sys.argv[1]
limit = int(sys.argv[2])

with open('fetched_cities.json') as f:
    fetched_cities = json.load(f)
    city = fetched_cities[locationId]
    print(city)
    print(f"Fetching hotels for {city['name']}, {city['country']}")
    offset_start = city["fetched"]
     

total_hotels = fetch_hotels(locationId, fetch_total=True)
print(total_hotels, 'hotels')
offsets = [i for i in range(offset_start, total_hotels + 1, 30)]
for offset in offsets:
  if offset >= limit:
    break
  fetch_hotels(locationId, offset = f'oa{offset}')
  sleep(1)
