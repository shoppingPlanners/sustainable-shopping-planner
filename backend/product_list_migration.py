#!/usr/bin/env python3
"""
Product List Migration Script for Sustainable Shopping Planner
Migrates existing product_list collection to the new schema
"""

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from database import Product, Review, AIRating
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Your MongoDB configuration
MONGODB_URL = "mongodb://localhost:27017"
DATABASE_NAME = "sustainable-shopping-planner"

async def connect_to_mongodb():
    """Connect to your existing MongoDB database"""
    try:
        client = AsyncIOMotorClient(MONGODB_URL)
        db = client[DATABASE_NAME]
        
        # Test connection
        await client.admin.command('ping')
        logger.info(f"✅ Connected to MongoDB: {DATABASE_NAME}")
        return client, db
    except Exception as e:
        logger.error(f"❌ Failed to connect to MongoDB: {e}")
        raise

async def analyze_existing_data(db):
    """Analyze existing product_list collection"""
    try:
        # Check if product_list collection exists
        collections = await db.list_collection_names()
        logger.info(f"📋 Available collections: {collections}")
        
        if "product_list" in collections:
            # Get sample documents
            sample_docs = await db.product_list.find().limit(3).to_list(3)
            logger.info(f"📊 Sample documents from product_list:")
            for i, doc in enumerate(sample_docs):
                logger.info(f"  Document {i+1}: {list(doc.keys())}")
                logger.info(f"    Sample: {doc}")
            
            # Get total count
            count = await db.product_list.count_documents({})
            logger.info(f"📈 Total documents in product_list: {count}")
            
            return sample_docs
        else:
            logger.warning("⚠️  product_list collection not found")
            return []
            
    except Exception as e:
        logger.error(f"❌ Error analyzing existing data: {e}")
        return []

async def migrate_product_list(db):
    """Migrate product_list to new products collection"""
    try:
        logger.info("🔄 Starting product_list migration...")
        
        # Get all documents from product_list
        product_docs = await db.product_list.find().to_list()
        
        if not product_docs:
            logger.warning("⚠️  No documents found in product_list")
            return
        
        migrated_count = 0
        
        for doc in product_docs:
            try:
                # Map existing fields to new schema
                product_data = {
                    "name": doc.get("name", doc.get("title", "Unknown Product")),
                    "brand": doc.get("brand", doc.get("manufacturer", "Unknown Brand")),
                    "category": doc.get("category", doc.get("type", "clothing")),
                    "price": float(doc.get("price", doc.get("cost", 0))),
                    "description": doc.get("description", doc.get("details", "")),
                    "sustainability_features": doc.get("sustainability_features", doc.get("eco_features", [])),
                    "image": doc.get("image", doc.get("image_url", "/placeholder.jpg")),
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
                
                # Create new product document
                new_product = Product(**product_data)
                await new_product.insert()
                
                migrated_count += 1
                logger.info(f"✅ Migrated product: {product_data['name']}")
                
            except Exception as e:
                logger.error(f"❌ Error migrating product {doc.get('_id', 'unknown')}: {e}")
                continue
        
        logger.info(f"🎉 Migration completed! Migrated {migrated_count} products")
        
    except Exception as e:
        logger.error(f"❌ Error during migration: {e}")

async def create_sample_reviews(db):
    """Create sample reviews for migrated products"""
    try:
        logger.info("📝 Creating sample reviews...")
        
        # Get migrated products
        products = await Product.find_all().to_list()
        
        if not products:
            logger.warning("⚠️  No products found to create reviews for")
            return
        
        # Create sample reviews
        sample_reviews = [
            {
                "product_id": str(products[0].id),
                "user_id": "user1",
                "rating": 5,
                "text": "Amazing sustainable product! Love the eco-friendly materials and the brand's commitment to sustainability.",
                "date": datetime.utcnow()
            },
            {
                "product_id": str(products[0].id),
                "user_id": "user2", 
                "rating": 4,
                "text": "Great quality and fit. The sustainable approach is definitely a plus. Would recommend!",
                "date": datetime.utcnow()
            }
        ]
        
        for review_data in sample_reviews:
            review = Review(**review_data)
            await review.insert()
            logger.info(f"✅ Created review for product {review_data['product_id']}")
        
        logger.info("🎉 Sample reviews created successfully!")
        
    except Exception as e:
        logger.error(f"❌ Error creating sample reviews: {e}")

async def setup_database_indexes(db):
    """Setup indexes for optimal performance"""
    try:
        logger.info("🔍 Setting up database indexes...")
        
        # Products indexes
        await db.products.create_index("name")
        await db.products.create_index("brand")
        await db.products.create_index("category")
        await db.products.create_index("price")
        
        # Reviews indexes
        await db.reviews.create_index("product_id")
        await db.reviews.create_index("user_id")
        await db.reviews.create_index("rating")
        await db.reviews.create_index("date")
        await db.reviews.create_index([("product_id", 1), ("rating", 1)])
        
        # AI Ratings indexes
        await db.ai_ratings.create_index("product_id")
        await db.ai_ratings.create_index("ai_rating")
        await db.ai_ratings.create_index("timestamp")
        
        logger.info("✅ Database indexes created successfully!")
        
    except Exception as e:
        logger.error(f"❌ Error setting up indexes: {e}")

async def main():
    """Main migration function"""
    logger.info("🌱 Sustainable Shopping Planner - Product List Migration")
    logger.info("=" * 70)
    
    try:
        # Connect to MongoDB
        client, db = await connect_to_mongodb()
        
        # Analyze existing data
        sample_docs = await analyze_existing_data(db)
        
        if sample_docs:
            # Ask user if they want to proceed with migration
            print("\n" + "="*50)
            print("📊 FOUND EXISTING PRODUCT_LIST COLLECTION")
            print("="*50)
            print(f"Database: {DATABASE_NAME}")
            print(f"Collection: product_list")
            print(f"Sample document structure:")
            for key, value in sample_docs[0].items():
                print(f"  {key}: {type(value).__name__}")
            print("\n" + "="*50)
            
            response = input("Do you want to migrate product_list to the new schema? (y/n): ")
            
            if response.lower() == 'y':
                # Initialize Beanie
                from beanie import init_beanie
                await init_beanie(
                    database=db,
                    document_models=[Product, Review, AIRating]
                )
                
                # Migrate data
                await migrate_product_list(db)
                
                # Create sample reviews
                await create_sample_reviews(db)
                
                # Setup indexes
                await setup_database_indexes(db)
                
                logger.info("🎉 Migration completed successfully!")
            else:
                logger.info("❌ Migration cancelled by user")
        else:
            logger.info("📝 No existing product_list found. You can add products manually or through the API.")
        
        # Show final status
        collections = await db.list_collection_names()
        logger.info(f"📋 Final collections: {collections}")
        
    except Exception as e:
        logger.error(f"❌ Migration failed: {e}")
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    asyncio.run(main())
