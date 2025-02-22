import numpy as np
import pickle
import pymongo

from dotenv import load_dotenv
import os

load_dotenv()

import tensorflow_hub as hub


def load_model():
  module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
  model = hub.load(module_url)
  print ("module %s loaded" % module_url)
  return model

def get_hotel_location(hotel_doc):
  country = ''; region = ''; city = ''
  for ancestor in hotel_doc["ancestors"]:
    if ancestor["level"] in ["City", "Municipality", "Island"]:
      city = ancestor["name"]
    elif ancestor["level"] == "Island":
      region = ancestor["name"]
    elif ancestor["level"] == "Country":
      country = ancestor["name"]
  ancestorsArray = [ancestor for ancestor in [country, region, city] if ancestor]
  return " ".join(ancestorsArray)
  

def get_description():
  hotel_mapper = {}
  descriptions = []
  for hotel_doc in hotels_col.find({"description": {"$ne": None}}):
    hotel_mapper[len(descriptions)] = hotel_doc['location_id']
    location = get_hotel_location(hotel_doc)
    description = f"{location} {hotel_doc['description']}"
    descriptions.append(description)    
  return descriptions, hotel_mapper 

if __name__ == "__main__":
  client = pymongo.MongoClient(os.environ["MONGO_HOST"])
  db = client["hotels"]
  reviews_col = db["reviews"]
  hotels_col = db["hotels"]
  
  model = load_model()
  to_embed, mapper = get_description()
  embeddings_ = model(to_embed)
  embeddings_2D = np.reshape(embeddings_, (len(embeddings_), -1))
  
  np.save("API/embeddings.npy", embeddings_2D)
  with open("API/hotel_mapper.pkl", "wb") as f:
    pickle.dump(mapper, f)