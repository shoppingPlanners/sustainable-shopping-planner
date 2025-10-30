from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from functools import lru_cache
import hashlib
import json
from datetime import datetime, timedelta
import httpx
import asyncio

load_dotenv()

router = APIRouter(prefix="/api/preferences", tags=["preferences"])

# Direct MongoDB connection
mongo_client = MongoClient(os.getenv("DATABASE_URL", "mongodb://localhost:27017/sustainable-shopping-planner"))
mongo_db = mongo_client.get_default_database()

# Agent URLs
SUGGESTION_AGENT_URL = os.getenv("SUGGESTION_AGENT_URL", "http://localhost:5004")
USER_BEHAVIOR_URL = os.getenv("USER_BEHAVIOR_URL", "http://localhost:5003")

# Simple in-memory cache with expiration
recommendation_cache: Dict[str, Dict[str, Any]] = {}
CACHE_EXPIRY_MINUTES = 15

def get_cache_key(params: Dict[str, Any]) -> str:
    """Generate a unique cache key from parameters."""
    sorted_params = json.dumps(params, sort_keys=True)
    return hashlib.md5(sorted_params.encode()).hexdigest()

def get_from_cache(cache_key: str) -> Optional[List[Dict[str, Any]]]:
    """Get data from cache if it exists and hasn't expired."""
    if cache_key in recommendation_cache:
        cached_data = recommendation_cache[cache_key]
        if datetime.now() < cached_data["expiry"]:
            print(f"Cache hit for key: {cache_key}")
            return cached_data["data"]
        else:
            # Remove expired cache
            del recommendation_cache[cache_key]
    return None

def set_in_cache(cache_key: str, data: List[Dict[str, Any]]):
    """Store data in cache with expiration."""
    recommendation_cache[cache_key] = {
        "data": data,
        "expiry": datetime.now() + timedelta(minutes=CACHE_EXPIRY_MINUTES)
    }
    print(f"Cache set for key: {cache_key}")

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
    sustainability_focus: Optional[List[str]] = []
    is_bestseller: Optional[bool] = False
    description: Optional[str] = ""

@router.post("/save")
async def save_preferences(preferences: UserPreferences):
    """
    Save user preferences to the database and track with User Behavior Agent.
    """
    try:
        # Store preferences in MongoDB
        preferences_data = preferences.dict()
        preferences_data["timestamp"] = {"$date": {"$numberLong": str(int(__import__("time").time() * 1000))}}
        
        result = mongo_db.user_preferences.insert_one(preferences_data)
        
        # Track preferences update with User Behavior Agent (Agent 3)
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                await client.post(
                    f"{USER_BEHAVIOR_URL}/track",
                    json={
                        "user_id": str(result.inserted_id),
                        "session_id": f"pref_{result.inserted_id}",
                        "event_type": "preferences_updated",
                        "timestamp": __import__("time").time(),
                        "metadata": preferences_data
                    }
                )
        except Exception as e:
            # Don't fail if behavior tracking fails
            print(f"Warning: Failed to track preferences with Agent 3: {e}")
        
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
    limit: int = 10,
    user_id: Optional[str] = None
):
    """
    Get personalized recommendations using the 4-agent system.
    
    Flow: Backend → Suggestion Agent (4) → [Brand Collector (1), Rating Calculator (2), User Behavior (3)]
    """
    try:
        # Try agent-based approach first (streamlined multi-agent flow)
        try:
            return await get_recommendations_from_agents(
                user_id=user_id or "guest_user",
                category=category,
                budget=budget,
                style=style,
                sustainability_priorities=sustainability_priorities,
                size=size,
                limit=limit
            )
        except Exception as agent_error:
            print(f"Agent-based recommendations failed: {agent_error}")
            print("Falling back to direct database query...")
            # Fallback to direct database query if agents fail
            return await get_recommendations_from_database(
                category=category,
                budget=budget,
                style=style,
                sustainability_priorities=sustainability_priorities,
                size=size,
                limit=limit
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get recommendations: {str(e)}")


async def get_recommendations_from_agents(
    user_id: str,
    category: Optional[str] = None,
    budget: Optional[str] = None,
    style: Optional[str] = None,
    sustainability_priorities: Optional[str] = None,
    size: Optional[str] = None,
    limit: int = 10
) -> List[RecommendationResponse]:
    """
    Get recommendations using the 4-agent system (STREAMLINED FLOW).
    
    This function orchestrates:
    1. Suggestion Agent (Agent 4) - coordinates everything
    2. Brand Data Collector (Agent 1) - called by Agent 4
    3. Rating Calculator (Agent 2) - called by Agent 4
    4. User Behavior Tracker (Agent 3) - called by Agent 4
    """
    
    print(f"🤖 Using Agent-Based Flow for user: {user_id}")
    
    # Step 1: Update user preferences in behavior tracker if provided
    if any([category, budget, style, sustainability_priorities, size]):
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                await client.post(
                    f"{USER_BEHAVIOR_URL}/track",
                    json={
                        "user_id": user_id,
                        "session_id": f"session_{user_id}",
                        "event_type": "search_preferences",
                        "timestamp": __import__("time").time(),
                        "metadata": {
                            "category": category,
                            "budget": budget,
                            "style": style,
                            "sustainability_priorities": sustainability_priorities,
                            "size": size
                        }
                    }
                )
                print("  ✅ Tracked preferences with Agent 3")
        except Exception as e:
            print(f"  ⚠️ Failed to track preferences: {e}")
    
    # Step 2: Call Suggestion Agent (which will call Agents 1, 2, 3)
    async with httpx.AsyncClient(timeout=15.0) as client:
        params = {"limit": limit}
        if category and category != "all":
            params["category"] = category
        
        print(f"  🎯 Calling Suggestion Agent (Agent 4)...")
        response = await client.get(
            f"{SUGGESTION_AGENT_URL}/suggestions/{user_id}",
            params=params
        )
        
        if response.status_code != 200:
            raise Exception(f"Suggestion Agent returned {response.status_code}: {response.text}")
        
        data = response.json()
        suggestions = data.get("suggestions", [])
        print(f"  ✅ Received {len(suggestions)} suggestions from Agent 4")
    
    # Step 3: Convert agent response to our format and apply additional filters
    recommendations = []
    for suggestion in suggestions:
        # Apply budget filter
        if budget and budget != "all":
            price_str = suggestion.get("price", "0")
            try:
                price = float(price_str.replace("$", "").replace("£", "").replace(",", ""))
                
                skip = False
                if budget == "under-20" and price >= 20:
                    skip = True
                elif budget == "20-30" and not (20 <= price <= 30):
                    skip = True
                elif budget == "30-50" and not (30 < price <= 50):
                    skip = True
                elif budget == "50-plus" and price <= 50:
                    skip = True
                
                if skip:
                    continue
            except:
                pass
        
        # Apply sustainability priority filter
        if sustainability_priorities:
            sustainability_focus = suggestion.get("sustainability_focus", [])
            if sustainability_focus:
                priorities_lower = sustainability_priorities.lower()
                focus_str = " ".join(sustainability_focus).lower()
                if not any(keyword in focus_str for keyword in priorities_lower.split()):
                    # Don't skip, but lower the score
                    pass
        
        # Convert to our response format
        rec = RecommendationResponse(
            id=suggestion.get("product_id", ""),
            name=suggestion.get("product_name", ""),
            brand=suggestion.get("brand_name", ""),
            rating=4.5,  # Default rating
            sustainabilityScore=int(suggestion.get("sustainability_score", 70)),
            price=suggestion.get("price", "N/A"),
            image="/placeholder.jpg",  # Would need to be in suggestion response
            buyUrl=suggestion.get("url", "#"),
            features=suggestion.get("reasons", []),
            category=suggestion.get("category", ""),
            match_score=suggestion.get("recommendation_score", 0.0) * 100,
            reason="; ".join(suggestion.get("reasons", [])[:3]),
            sustainability_focus=[],
            is_bestseller=False,
            description=""
        )
        recommendations.append(rec)
    
    print(f"  ✅ Returning {len(recommendations)} filtered recommendations")
    return recommendations[:limit]


async def get_recommendations_from_database(
    category: Optional[str] = None,
    budget: Optional[str] = None,
    style: Optional[str] = None,
    sustainability_priorities: Optional[str] = None,
    size: Optional[str] = None,
    limit: int = 10
) -> List[RecommendationResponse]:
    """
    Fallback: Get recommendations directly from database (original implementation).
    """
    print("🗄️  Using Direct Database Fallback")
    
    # Generate cache key from parameters
    cache_params = {
        "category": category,
        "budget": budget,
        "style": style,
        "sustainability_priorities": sustainability_priorities,
        "size": size,
        "limit": limit
    }
    cache_key = get_cache_key(cache_params)
    
    # Try to get from cache
    cached_result = get_from_cache(cache_key)
    if cached_result is not None:
        return cached_result
    
    # Build filter conditions based on preferences
    filter_conditions = {}
    
    if category and category != "all":
        filter_conditions["category"] = category
    
    # Get all items by flattening products from brands collection
    brands_cursor = mongo_db.brands.find({})
    items = []
    
    for brand_doc in brands_cursor:
        brand_id_str = str(brand_doc.get("_id"))
        brand_domain = brand_doc.get("brand_domain", "")
        products = brand_doc.get("products", []) or []
        
        for index, product in enumerate(products):
            product_category = product.get("category", "") or ""
            product_name = product.get("product_name", "").lower()
            
            # Apply category filter - use actual category field from database
            if category and category != "all":
                category_lower = category.lower()
                product_category_lower = product_category.lower()
                
                # Map frontend categories to database categories
                category_match = False
                
                if category_lower == "dresses" and "dress" in product_category_lower:
                    category_match = True
                elif category_lower == "t-shirts" and "t-shirt" in product_category_lower:
                    category_match = True
                elif category_lower == "tops" and "top" in product_category_lower:
                    category_match = True
                elif category_lower == "summer" and ("summer" in product_category_lower or "summer" in product_name):
                    category_match = True
                elif category_lower == "activewear" and "activewear" in product_category_lower:
                    category_match = True
                elif category_lower == "bottoms" and ("bottom" in product_category_lower or "jean" in product_category_lower):
                    category_match = True
                elif category_lower == "jackets" and ("jacket" in product_category_lower or "outerwear" in product_category_lower):
                    category_match = True
                elif category_lower == "accessories" and "accessor" in product_category_lower:
                    category_match = True
                elif category_lower == "footwear" and "footwear" in product_category_lower:
                    category_match = True
                # Fallback: try matching in category or product name
                elif category_lower in product_category_lower or category_lower in product_name:
                    category_match = True
                
                if not category_match:
                    continue
            
            sustainability_list = product.get("sustainability_focus", []) or []
            # Use the actual sustainability_score from the database (calculated by scraper)
            sustainability_score = product.get("sustainability_score", product.get("sustainabilityScore", 70))
            
            # Get price and convert to string if needed
            price_value = product.get("price", 0)
            price_str = f"${price_value}" if isinstance(price_value, (int, float)) else str(price_value)
            
            item = {
                "_id": f"{brand_id_str}:{index}",
                "name": product.get("product_name", product.get("name", "")),
                "brand": brand_domain,
                "rating": product.get("rating", 0.0),
                "sustainabilityScore": sustainability_score,  # Use actual score from database
                "price": price_str,
                "image": product.get("image", product.get("image_url", "")),
                "buyUrl": product.get("product_url", ""),
                "features": product.get("available_sizes", product.get("sizes", [])) or [],
                "category": product_category,
                "sustainability_focus": sustainability_list,
                "is_bestseller": product.get("is_bestseller", False),
                "description": product.get("description", ""),
            }
            items.append(item)
    
    if not items:
        return []
    
    # Score and rank items based on preferences (improved algorithm)
    scored_items = []
    for item in items:
        score = 0.0
        reasons = []
        
        # Category match (high weight)
        if category and item.get("category") == category:
            score += 35
            reasons.append(f"Perfect {category} match")
        
        # Budget match (high weight with gradual scoring)
        if budget:
            price_value = item.get("price", 0)
            # Handle both string and float prices
            if isinstance(price_value, str):
                price_str = price_value.replace("$", "").replace("£", "").replace(",", "")
                price = float(price_str) if price_str else 0.0
            else:
                price = float(price_value) if price_value else 0.0
            try:
                if budget == "under-20":
                    if price < 20:
                        score += 30
                        reasons.append(f"Great value at ${price:.0f}")
                    elif price < 25:
                        score += 15
                elif budget == "20-30":
                    if 20 <= price <= 30:
                        score += 30
                        reasons.append(f"Perfect budget fit at ${price:.0f}")
                    elif 18 <= price < 20 or 30 < price <= 35:
                        score += 20
                elif budget == "30-50":
                    if 30 < price <= 50:
                        score += 30
                        reasons.append(f"Quality choice at ${price:.0f}")
                    elif 25 <= price <= 30 or 50 < price <= 60:
                        score += 20
                elif budget == "50-plus":
                    if price > 50:
                        score += 30
                        reasons.append(f"Premium option at ${price:.0f}")
                    elif price > 45:
                        score += 20
            except ValueError:
                pass
        
        # Sustainability priorities match (improved matching)
        sustainability_focus = item.get("sustainability_focus", [])
        if sustainability_priorities and sustainability_focus:
            priorities_lower = sustainability_priorities.lower()
            sustainability_keywords = {
                "organic": ["organic"],
                "recycled": ["recycled", "upcycled"],
                "fair trade": ["fair trade", "ethical"],
                "carbon": ["carbon neutral", "carbon"],
                "eco": ["eco", "sustainable"],
                "vegan": ["vegan", "cruelty-free"],
                "natural": ["natural", "biodegradable"]
            }
            
            matches = 0
            for keyword, variations in sustainability_keywords.items():
                if any(var in priorities_lower for var in variations):
                    if any(var in " ".join(sustainability_focus).lower() for var in variations):
                        matches += 1
            
            if matches > 0:
                score += min(25, matches * 8)
                reasons.append(f"Matches {matches} sustainability priorit{'y' if matches == 1 else 'ies'}")
        
        # Sustainability score bonus (graduated) - use actual score from database
        sustainability_score = item.get("sustainabilityScore", 0)
        if sustainability_score >= 90:
            score += 20
            reasons.append(f"Exceptional sustainability ({sustainability_score}/100)")
        elif sustainability_score >= 80:
            score += 15
            reasons.append(f"Highly sustainable ({sustainability_score}/100)")
        elif sustainability_score >= 70:
            score += 12
            reasons.append(f"Very sustainable ({sustainability_score}/100)")
        elif sustainability_score >= 60:
            score += 8
            reasons.append(f"Good sustainability ({sustainability_score}/100)")
        elif sustainability_score >= 50:
            score += 5
            reasons.append(f"Sustainable practices ({sustainability_score}/100)")
        
        # Rating bonus (graduated)
        rating = item.get("rating", 0)
        if rating >= 4.8:
            score += 12
            reasons.append(f"⭐ {rating}/5 customer rating")
        elif rating >= 4.5:
            score += 8
            reasons.append(f"Highly rated ({rating}/5)")
        elif rating >= 4.0:
            score += 5
            reasons.append("Well-rated product")
        
        # Bestseller bonus
        if item.get("is_bestseller", False):
            score += 8
            reasons.append("Popular choice")
        
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
        recommendation = RecommendationResponse(
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
            reason=scored_item["reason"],
            sustainability_focus=item.get("sustainability_focus", []),
            is_bestseller=item.get("is_bestseller", False),
            description=item.get("description", "")
        )
        result.append(recommendation)
    
    # Store in cache before returning
    set_in_cache(cache_key, result)
    
    return result

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


@router.get("/analysis")
async def get_preferences_analysis():
    """
    Get overall analysis of user_preferences across all submissions.
    Returns totals and most frequent values per field.
    """
    try:
        coll = mongo_db.user_preferences

        total = coll.count_documents({})
        last_doc = coll.find().sort("timestamp", -1).limit(1)
        last_pref = next(last_doc, None)
        if last_pref and "_id" in last_pref:
            del last_pref["_id"]

        def top_value_for(field: str) -> Optional[Dict[str, Any]]:
            pipeline = [
                {"$match": {field: {"$exists": True, "$ne": None, "$ne": ""}}},
                {"$group": {"_id": f"${field}", "count": {"$sum": 1}}},
                {"$sort": {"count": -1}},
                {"$limit": 1},
            ]
            result = list(coll.aggregate(pipeline))
            if result:
                return {"value": result[0]["_id"], "count": result[0]["count"]}
            return None

        analysis = {
            "total_submissions": total,
            "top_category": top_value_for("category"),
            "top_budget": top_value_for("budget"),
            "top_style": top_value_for("style"),
            "top_sustainability_priorities": top_value_for("sustainability_priorities"),
            "top_size": top_value_for("size"),
            "last_preference": last_pref or {},
        }

        return {"success": True, "analysis": analysis}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze preferences: {str(e)}")
