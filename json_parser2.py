import os
import json
import csv

hotels_folder = "./hotels/"

header = ['id', 'name', 'region', 'country', 'latitude', 'longitude',
          'ranking', 'ranking_out_of', 'rating', 'num_reviews', 'photo_count', 'amenities', 'brand', 'awards', 'price_level']
csv_file = "hotels2.csv"

with open(csv_file, "wt", newline='', encoding='utf-8') as f:
    csv_writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
    csv_writer.writerow(header)

    for filename in os.listdir(hotels_folder):
        if filename == '.gitkeep': continue
        hotel_json = json.load(open(hotels_folder+filename, 'r', encoding="utf8"))
        if not 'price_level' in hotel_json:
            continue
        regionList = [hotel for hotel in hotel_json['ancestors'] if hotel['level'] == 'Region']
        if len(regionList) == 0:
            regionList = [hotel for hotel in hotel_json['ancestors'] if hotel['level'] == 'Province']
        region = regionList[0]

        values = [
            int(hotel_json['location_id']),
            hotel_json['name'],
            region['name'],
            hotel_json['address_obj']['country'],
            float(hotel_json['latitude']),
            float(hotel_json['longitude']),
            int(hotel_json['ranking_data']['ranking']),
            int(hotel_json['ranking_data']['ranking_out_of']),
            float(hotel_json['rating']),
            int(hotel_json['num_reviews']),
            int(hotel_json['photo_count']),
            ",".join(hotel_json['amenities']),
            hotel_json['brand'] if 'brand' in hotel_json else None,
            ",".join([f"{award['display_name']} {award['year']}" for award in  hotel_json['awards']]),
            hotel_json['price_level']
        ]
        csv_writer.writerow(values)
