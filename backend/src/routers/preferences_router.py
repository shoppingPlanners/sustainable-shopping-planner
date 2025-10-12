from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from typing import List, Optional
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/api/preferences", tags=["preferences"])

# Direct MongoDB connection
mongo_client = MongoClient(os.getenv("DATABASE_URL", "mongodb://localhost:27017/sustainable-shopping-planner"))
mongo_db = mongo_client.get_default_database()

class UserPreferences(BaseModel):
    category: Optional[str] = None
    budget: Optional[str] = None
    style: Optional[str] = None
    sustainability_priorities: Optional[str] = None
    size: Optional[str] = None

class RecommendationResponse(BaseModel):
    id: str
    name: str
    brand: str
    rating: float
    sustainabilityScore: int
    price: str
    image: str
    buyUrl: str
    features: List[str]
    category: str
    match_score: float
    reason: str

@router.post("/save")
async def save_preferences(preferences: UserPreferences):
    """
    Save user preferences to the database.
    """
    try:
        # Store preferences in MongoDB
        preferences_data = preferences.dict()
        preferences_data["timestamp"] = {"$date": {"$numberLong": str(int(__import__("time").time() * 1000))}}
        
        result = mongo_db.user_preferences.insert_one(preferences_data)
        
        return {
            "success": True,
            "preferences_id": str(result.inserted_id),
            "message": "Preferences saved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save preferences: {str(e)}")

@router.get("/recommendations", response_model=List[RecommendationResponse])
async def get_recommendations(
    category: Optional[str] = None,
    budget: Optional[str] = None,
    style: Optional[str] = None,
    sustainability_priorities: Optional[str] = None,
    size: Optional[str] = None,
    limit: int = 10
):
    """
    Get personalized recommendations based on user preferences.
    """
    try:
        # Build filter conditions based on preferences
        filter_conditions = {}
        
        if category and category != "all":
            filter_conditions["category"] = category
        
        # Get all items matching basic filters
        items_cursor = mongo_db.item.find(filter_conditions).limit(50)  # Get more items for scoring
        items = list(items_cursor)
        
        if not items:
            return []
        
        # Score and rank items based on preferences
        scored_items = []
        for item in items:
            score = 0.0
            reasons = []
            
            # Category match (high weight)
            if category and item.get("category") == category:
                score += 30
                reasons.append("Matches your preferred category")
            
            # Budget match
            if budget:
                price_str = item.get("price", "$0").replace("$", "").replace(",", "")
                try:
                    price = float(price_str)
                    if budget == "under-50" and price < 50:
                        score += 25
                        reasons.append("Fits your budget")
                    elif budget == "50-100" and 50 <= price <= 100:
                        score += 25
                        reasons.append("Fits your budget")
                    elif budget == "100-200" and 100 < price <= 200:
                        score += 25
                        reasons.append("Fits your budget")
                    elif budget == "200-plus" and price > 200:
                        score += 25
                        reasons.append("Fits your budget")
                except ValueError:
                    pass
            
            # Sustainability priorities match
            if sustainability_priorities:
                priorities_lower = sustainability_priorities.lower()
                item_features = [f.lower() for f in item.get("features", [])]
                
                if any(priority in item_features for priority in ["organic", "recycled", "fair trade", "carbon neutral"]):
                    score += 20
                    reasons.append("Matches your sustainability priorities")
            
            # High sustainability score bonus
            sustainability_score = item.get("sustainabilityScore", 0)
            if sustainability_score >= 90:
                score += 15
                reasons.append("Exceptional sustainability rating")
            elif sustainability_score >= 80:
                score += 10
                reasons.append("High sustainability rating")
            
            # High rating bonus
            rating = item.get("rating", 0)
            if rating >= 4.5:
                score += 10
                reasons.append("Highly rated by users")
            elif rating >= 4.0:
                score += 5
                reasons.append("Well-rated product")
            
            # Convert ObjectId to string for JSON serialization
            item_id = str(item["_id"])
            del item["_id"]
            item["id"] = item_id
            
            scored_items.append({
                "item": item,
                "score": score,
                "reason": "; ".join(reasons) if reasons else "Good match for your preferences"
            })
        
        # Sort by score and take top items
        scored_items.sort(key=lambda x: x["score"], reverse=True)
        top_items = scored_items[:limit]
        
        # Convert to response format
        result = []
        for scored_item in top_items:
            item = scored_item["item"]
            result.append(RecommendationResponse(
                id=item["id"],
                name=item["name"],
                brand=item["brand"],
                rating=item["rating"],
                sustainabilityScore=item["sustainabilityScore"],
                price=item["price"],
                image=item["image"],
                buyUrl=item["buyUrl"],
                features=item["features"],
                category=item["category"],
                match_score=round(scored_item["score"], 1),
                reason=scored_item["reason"]
            ))
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get recommendations: {str(e)}")

@router.get("/recent")
async def get_recent_preferences():
    """
    Get the most recent user preferences.
    """
    try:
        recent_prefs = mongo_db.user_preferences.find().sort("timestamp", -1).limit(1)
        prefs = list(recent_prefs)
        
        if prefs:
            pref = prefs[0]
            del pref["_id"]
            return pref
        else:
            return {}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get recent preferences: {str(e)}")
