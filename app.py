from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from dotenv import load_dotenv
from pymongo import MongoClient
from os import environ

load_dotenv()
app = FastAPI()

client = MongoClient(environ["MONGO_HOST"])
db = client["hotels"]
reviews_col = db["reviews"]
hotels_col = db["hotels"]

class PromptRequest(BaseModel):
  prompt: str
  
class HotelRecommendation(BaseModel):
  locationId: str

class RecommendationResponse(BaseModel):
  recommendations: List[HotelRecommendation]

def get_recommendations(prompt: str) -> List[Dict]:
  # TODO: logic for fetching recommended hotels
  return [{"locationId": "10046238"}, {"locationId": "1006161"}, {"locationId": "10061941"}]

@app.post("/recommendations", response_model=RecommendationResponse)
async def recommend_hotels(request: PromptRequest):
  recommendations = get_recommendations(request.prompt)
  if not recommendations:
    raise HTTPException(status_code=404, detail="No recommendations found.")
  return {"recommendations": recommendations}

# uvicorn app:app --reload