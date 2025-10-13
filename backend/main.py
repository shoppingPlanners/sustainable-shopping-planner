"""
Sustainable Shopping Planner - Python Backend
FastAPI-based backend with AI rating integration and MongoDB
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import asyncio
import subprocess
import json
from datetime import datetime
import logging
from database import init_db, close_db, Product, Review, AIRating, User
from bson import ObjectId

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Sustainable Shopping Planner API",
    description="Backend API for sustainable shopping with AI rating system and MongoDB",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize MongoDB connection on startup"""
    await init_db()
    await seed_initial_data()

@app.on_event("shutdown")
async def shutdown_event():
    """Close MongoDB connection on shutdown"""
    await close_db()

# Seed initial data
async def seed_initial_data():
    """Seed database with initial data if empty"""
    try:
        # Check if products exist in the new products collection
        existing_products = await Product.find_all().to_list()
        
        # Check if product_list collection exists (your existing data)
        from database import database
        product_list_exists = "product_list" in await database.list_collection_names()
        
        if not existing_products and product_list_exists:
            logger.info("🔄 Found existing product_list collection. You can migrate it using:")
            logger.info("   python product_list_migration.py")
            logger.info("   or use the helper script: python product_list_helper.py")
        elif not existing_products:
            logger.info("🌱 Seeding initial data...")
            
            # Create initial products
            initial_products = [
                Product(
                    name="Organic Cotton T-Shirt",
                    brand="EcoWear",
                    category="clothing",
                    price=29.99,
                    description="100% organic cotton t-shirt made from sustainable farming practices. Fair-trade certified and carbon-neutral shipping.",
                    sustainability_features=["organic-cotton", "fair-trade", "carbon-neutral"],
                    image="/organic-cotton-t-shirt-sustainable-fashion.png"
                ),
                Product(
                    name="Recycled Denim Jeans",
                    brand="GreenDenim",
                    category="clothing",
                    price=89.99,
                    description="Jeans made from 80% recycled denim with minimal water usage. Ethically produced with biodegradable packaging.",
                    sustainability_features=["recycled-materials", "water-efficient", "biodegradable-packaging"],
                    image="/recycled-denim-jeans-sustainable-fashion.png"
                ),
                Product(
                    name="Hemp Hoodie",
                    brand="NaturalWear",
                    category="clothing",
                    price=79.99,
                    description="Comfortable hoodie made from hemp fiber. Naturally antimicrobial and requires minimal pesticides to grow.",
                    sustainability_features=["hemp-fiber", "natural", "low-pesticide"],
                    image="/hemp-hoodie-sustainable-fashion.jpg"
                )
            ]
            
            for product in initial_products:
                await product.insert()
            
            # Create initial reviews
            initial_reviews = [
                Review(
                    product_id=str(initial_products[0].id),
                    user_id="user1",
                    rating=5,
                    text="Amazing quality! The organic cotton is so soft and comfortable. Love that it's eco-friendly and the brand is transparent about their practices.",
                    date=datetime.utcnow()
                ),
                Review(
                    product_id=str(initial_products[0].id),
                    user_id="user2",
                    rating=4,
                    text="Great shirt, fits well. The sustainable materials are a plus. Shipping was carbon-neutral which I appreciate.",
                    date=datetime.utcnow()
                ),
                Review(
                    product_id=str(initial_products[1].id),
                    user_id="user3",
                    rating=5,
                    text="Excellent jeans! The recycled denim feels just like new denim. Love the sustainable approach and the fit is perfect.",
                    date=datetime.utcnow()
                )
            ]
            
            for review in initial_reviews:
                await review.insert()
            
            logger.info("✅ Initial data seeded successfully")
        else:
            logger.info("📊 Database already contains data, skipping seed")
            
    except Exception as e:
        logger.error(f"❌ Error seeding initial data: {e}")

# Pydantic models
class Product(BaseModel):
    id: str
    name: str
    brand: str
    category: str
    price: float
    description: str
    sustainability_features: List[str] = []
    image: str = "/placeholder.jpg"

class ProductCreate(BaseModel):
    name: str
    brand: str
    category: str
    price: float
    description: str
    sustainability_features: List[str] = []
    image: str = "/placeholder.jpg"

class Review(BaseModel):
    id: str
    product_id: str
    user_id: str
    rating: int
    text: str
    date: str

class ReviewCreate(BaseModel):
    product_id: str
    user_id: str
    rating: int
    text: str

class AIRating(BaseModel):
    id: str
    product_id: str
    ai_rating: float
    sentiment_score: float
    sustainability_score: float
    confidence: float
    breakdown: dict
    timestamp: str

class AIRatingCreate(BaseModel):
    product_id: str
    ai_rating: float
    sentiment_score: float
    sustainability_score: float
    confidence: float
    breakdown: dict
    timestamp: str

# MongoDB operations will replace the mock database

# Helper functions
def convert_objectid_to_str(obj):
    """Convert ObjectId to string for JSON serialization"""
    if hasattr(obj, 'id'):
        obj.id = str(obj.id)
    return obj

async def trigger_ai_rating_calculation(product_id: str):
    """Trigger AI rating calculation in background"""
    try:
        logger.info(f"🤖 Triggering AI rating calculation for product {product_id}")
        
        # Run the AI agent
        process = await asyncio.create_subprocess_exec(
            "python", "app.py", product_id,
            cwd="../agents/rating_calculator",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        stdout, stderr = await process.communicate()
        
        if process.returncode == 0:
            logger.info(f"✅ AI rating calculation completed for product {product_id}")
            logger.info(f"AI Output: {stdout.decode()}")
        else:
            logger.error(f"❌ AI rating calculation failed: {stderr.decode()}")
            
    except Exception as e:
        logger.error(f"❌ Failed to trigger AI rating calculation: {e}")

# API Routes

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Sustainable Shopping Planner API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "OK", "message": "API is running"}

# Product endpoints
@app.get("/api/products", response_model=List[Product])
async def get_products():
    """Get all products"""
    try:
        products = await Product.find_all().to_list()
        return [convert_objectid_to_str(product) for product in products]
    except Exception as e:
        logger.error(f"Error fetching products: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch products")

@app.get("/api/products/{product_id}", response_model=Product)
async def get_product(product_id: str):
    """Get single product by ID"""
    try:
        product = await Product.get(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return convert_objectid_to_str(product)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching product {product_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch product")

@app.post("/api/products", response_model=Product)
async def create_product(product: ProductCreate):
    """Create new product"""
    try:
        new_product = Product(**product.dict())
        await new_product.insert()
        return convert_objectid_to_str(new_product)
    except Exception as e:
        logger.error(f"Error creating product: {e}")
        raise HTTPException(status_code=500, detail="Failed to create product")

# Review endpoints
@app.get("/api/reviews", response_model=List[Review])
async def get_reviews(product_id: Optional[str] = None, user_id: Optional[str] = None):
    """Get reviews with optional filtering"""
    try:
        query = {}
        if product_id:
            query["product_id"] = product_id
        if user_id:
            query["user_id"] = user_id
        
        reviews = await Review.find(query).to_list()
        return [convert_objectid_to_str(review) for review in reviews]
    except Exception as e:
        logger.error(f"Error fetching reviews: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch reviews")

@app.get("/api/reviews/{review_id}", response_model=Review)
async def get_review(review_id: str):
    """Get single review by ID"""
    try:
        review = await Review.get(review_id)
        if not review:
            raise HTTPException(status_code=404, detail="Review not found")
        return convert_objectid_to_str(review)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching review {review_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch review")

@app.post("/api/reviews", response_model=Review)
async def create_review(review: ReviewCreate, background_tasks: BackgroundTasks):
    """Create new review and trigger AI rating calculation"""
    try:
        # Validate rating
        if review.rating < 1 or review.rating > 5:
            raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
        
        new_review = Review(**review.dict())
        await new_review.insert()
        
        # Trigger AI rating calculation in background
        background_tasks.add_task(trigger_ai_rating_calculation, review.product_id)
        
        logger.info(f"📝 Review created for product {review.product_id}, AI calculation triggered")
        
        return convert_objectid_to_str(new_review)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating review: {e}")
        raise HTTPException(status_code=500, detail="Failed to create review")

@app.get("/api/products/{product_id}/reviews", response_model=List[Review])
async def get_product_reviews(product_id: str):
    """Get reviews for specific product"""
    try:
        reviews = await Review.find({"product_id": product_id}).to_list()
        return [convert_objectid_to_str(review) for review in reviews]
    except Exception as e:
        logger.error(f"Error fetching product reviews: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch product reviews")

# Rating endpoints
@app.get("/api/ratings", response_model=List[AIRating])
async def get_ratings(product_id: Optional[str] = None):
    """Get AI ratings with optional product filtering"""
    try:
        query = {}
        if product_id:
            query["product_id"] = product_id
        
        ratings = await AIRating.find(query).to_list()
        return [convert_objectid_to_str(rating) for rating in ratings]
    except Exception as e:
        logger.error(f"Error fetching ratings: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch ratings")

@app.get("/api/ratings/{rating_id}", response_model=AIRating)
async def get_rating(rating_id: str):
    """Get single rating by ID"""
    try:
        rating = await AIRating.get(rating_id)
        if not rating:
            raise HTTPException(status_code=404, detail="Rating not found")
        return convert_objectid_to_str(rating)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching rating {rating_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch rating")

@app.get("/api/ratings/product/{product_id}", response_model=AIRating)
async def get_product_rating(product_id: str):
    """Get AI rating for specific product"""
    try:
        rating = await AIRating.find_one({"product_id": product_id})
        if not rating:
            raise HTTPException(status_code=404, detail="No AI rating found for this product")
        return convert_objectid_to_str(rating)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching product rating: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch product rating")

@app.post("/api/ratings", response_model=AIRating)
async def create_rating(rating: AIRatingCreate):
    """Save AI rating (called by AI agent)"""
    try:
        # Check if rating already exists for this product
        existing_rating = await AIRating.find_one({"product_id": rating.product_id})
        
        if existing_rating:
            # Update existing rating
            for field, value in rating.dict().items():
                setattr(existing_rating, field, value)
            existing_rating.updated_at = datetime.utcnow()
            await existing_rating.save()
            rating_obj = existing_rating
        else:
            # Create new rating
            rating_obj = AIRating(**rating.dict())
            await rating_obj.insert()
        
        logger.info(f"💾 AI rating saved for product {rating.product_id}: {rating.ai_rating}/5.0")
        
        return convert_objectid_to_str(rating_obj)
    except Exception as e:
        logger.error(f"Error saving rating: {e}")
        raise HTTPException(status_code=500, detail="Failed to save rating")

@app.put("/api/ratings/{rating_id}", response_model=AIRating)
async def update_rating(rating_id: str, rating_update: AIRatingCreate):
    """Update existing rating"""
    try:
        rating = await AIRating.get(rating_id)
        if not rating:
            raise HTTPException(status_code=404, detail="Rating not found")
        
        for field, value in rating_update.dict().items():
            setattr(rating, field, value)
        rating.updated_at = datetime.utcnow()
        await rating.save()
        
        return convert_objectid_to_str(rating)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating rating: {e}")
        raise HTTPException(status_code=500, detail="Failed to update rating")

@app.delete("/api/ratings/{rating_id}")
async def delete_rating(rating_id: str):
    """Delete rating"""
    try:
        rating = await AIRating.get(rating_id)
        if not rating:
            raise HTTPException(status_code=404, detail="Rating not found")
        
        await rating.delete()
        return {"message": "Rating deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting rating: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete rating")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=3000,
        reload=True,
        log_level="info"
    )
