"""
MongoDB models and configuration for Sustainable Shopping Planner
"""

from beanie import Document, Indexed
from pydantic import Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
import os

# MongoDB configuration
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "sustainable-shopping-planner")

# Global MongoDB client
client = None
database = None

async def init_db():
    """Initialize MongoDB connection"""
    global client, database
    client = AsyncIOMotorClient(MONGODB_URL)
    database = client[DATABASE_NAME]
    
    # Initialize Beanie with the database
    await init_beanie()
    
    print(f"✅ Connected to MongoDB: {DATABASE_NAME}")

async def init_beanie():
    """Initialize Beanie with document models"""
    from beanie import init_beanie
    await init_beanie(
        database=database,
        document_models=[Product, Review, AIRating, User]
    )

async def close_db():
    """Close MongoDB connection"""
    if client:
        client.close()

# MongoDB Document Models
class Product(Document):
    name: str = Field(..., description="Product name")
    brand: str = Field(..., description="Brand name")
    category: str = Field(..., description="Product category")
    price: float = Field(..., description="Product price")
    description: str = Field(..., description="Product description")
    sustainability_features: List[str] = Field(default=[], description="Sustainability features")
    image: str = Field(default="/placeholder.jpg", description="Product image URL")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "products"
        indexes = [
            "name",
            "brand", 
            "category",
            "price"
        ]

class Review(Document):
    product_id: Indexed(str, description="Product ID")
    user_id: Indexed(str, description="User ID")
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    text: str = Field(..., description="Review text")
    date: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "reviews"
        indexes = [
            "product_id",
            "user_id",
            "rating",
            "date"
        ]

class AIRating(Document):
    product_id: Indexed(str, description="Product ID")
    ai_rating: float = Field(..., ge=1.0, le=5.0, description="AI calculated rating")
    sentiment_score: float = Field(..., ge=-1.0, le=1.0, description="Sentiment score")
    sustainability_score: float = Field(..., ge=0.0, le=1.0, description="Sustainability score")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence level")
    breakdown: Dict[str, Any] = Field(..., description="Detailed breakdown")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "ai_ratings"
        indexes = [
            "product_id",
            "ai_rating",
            "timestamp"
        ]

class User(Document):
    email: Indexed(str, unique=True, description="User email")
    username: Indexed(str, unique=True, description="Username")
    hashed_password: str = Field(..., description="Hashed password")
    is_active: bool = Field(default=True, description="User active status")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "users"
        indexes = [
            "email",
            "username"
        ]

# Database utility functions
async def get_database():
    """Get database instance"""
    return database

async def get_collection(collection_name: str):
    """Get specific collection"""
    return database[collection_name]
