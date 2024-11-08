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


def get_description():
  hotel_mapper = {}
  descriptions = []
  for hotel_doc in hotels_col.find({"description": {"$ne": None}}):
    hotel_mapper[len(descriptions)] = hotel_doc['location_id']
    descriptions.append(hotel_doc['description'])
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
  
  np.save("embeddings.npy", embeddings_2D)
  with open("hotel_mapper.pkl", "wb") as f:
    pickle.dump(mapper, f)