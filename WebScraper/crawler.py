import requests
from bs4 import BeautifulSoup
import re

def scrape_ids(locationId, offset='', fetch_total=False):
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
  if fetch_total:
    soup = BeautifulSoup(content, features="html.parser")
    total_text = soup.select('[data-test-target="hotels-main-list"] b, [data-test-target="hotels-main-list"] .b')[0]
    total_str = re.search('\d+(,\d+)*', total_text.text).group(0)
    return int(total_str.replace(',', ''))
  else:
    ids_set = set()
    for link in soup.select('[data-automation="hotel-card-title"] a'):
      ids_set.add(int(re.search('-d\d+\-', link['href']).group(0)[2:-1]))
    return ids_set
