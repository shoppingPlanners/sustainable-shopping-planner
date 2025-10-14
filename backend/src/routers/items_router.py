from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from typing import List, Optional
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/api/items", tags=["items"])

# Direct MongoDB connection
mongo_client = MongoClient(os.getenv("DATABASE_URL", "mongodb://localhost:27017/sustainable-shopping-planner"))
mongo_db = mongo_client.get_default_database()

class ItemResponse(BaseModel):
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

@router.get("/", response_model=List[ItemResponse])
async def get_items(
    category: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
):
    """
    Get items from the database with optional filtering by category.
    """
    try:
        # Build filter conditions
        filter_conditions = {}
        if category and category != "all":
            filter_conditions["category"] = category
        
        # Fetch items from MongoDB using direct connection
        items_cursor = mongo_db.item.find(filter_conditions).skip(offset).limit(limit)
        items = list(items_cursor)
        
        # Convert to response format
        result = []
        for item in items:
            # Convert ObjectId to string for JSON serialization
            item_id = str(item["_id"])
            del item["_id"]
            item["id"] = item_id
            
            result.append(ItemResponse(**item))
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch items: {str(e)}")

@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: str):
    """
    Get a specific item by ID.
    """
    try:
        from bson import ObjectId
        item = mongo_db.item.find_one({"_id": ObjectId(item_id)})
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        
        # Convert ObjectId to string for JSON serialization
        item_id_str = str(item["_id"])
        del item["_id"]
        item["id"] = item_id_str
        
        return ItemResponse(**item)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch item: {str(e)}")
