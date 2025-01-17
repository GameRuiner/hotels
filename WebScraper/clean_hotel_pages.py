import re
import os

hotel_pages = os.listdir('./tmp/')

count = 0
# add loader
for page in hotel_pages:
  path = f"./tmp/{page}"
  with open(path, 'r', encoding="utf8") as hotel_page:
    match = re.search(r'captcha-delivery', hotel_page.read())
  if match:
    count += 1
    os.remove(path)
print (f"{count} was removed from {len(hotel_pages)}")
