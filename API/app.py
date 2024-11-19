import numpy as np
import pickle
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from dotenv import load_dotenv
from pymongo import MongoClient
from os import environ
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()

import tensorflow_hub as hub

app = FastAPI()

client = MongoClient(environ["MONGO_HOST"])
db = client["hotels"]
reviews_col = db["reviews"]
hotels_col = db["hotels"]

embeddings_2D = np.load("embeddings.npy")
with open("hotel_mapper.pkl", "rb") as f:
    hotel_mapper = pickle.load(f)
    
module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
model = hub.load(module_url)
print("Model loaded successfully")

class PromptRequest(BaseModel):
  prompt: str
  
class HotelRecommendation(BaseModel):
  locationId: str

class RecommendationResponse(BaseModel):
  recommendations: List[HotelRecommendation]

def get_recommendations(prompt: str) -> List[Dict]:
  prompt_embedded = model([prompt])
  target_tensor_2D = np.reshape(prompt_embedded, (1, -1))
  similarities = cosine_similarity(target_tensor_2D, embeddings_2D)
  top_indices = np.argsort(similarities[0])[::-1][:3]
  return [{"locationId": hotel_mapper[index]} for index in top_indices]

@app.post("/recommendations", response_model=RecommendationResponse)
async def recommend_hotels(request: PromptRequest):
  recommendations = get_recommendations(request.prompt)
  if not recommendations:
    raise HTTPException(status_code=404, detail="No recommendations found.")
  return {"recommendations": recommendations}

# uvicorn app:app --reload