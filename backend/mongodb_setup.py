#!/usr/bin/env python3
"""
MongoDB setup script for Sustainable Shopping Planner
Creates database, collections, and indexes
"""

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from database import MONGODB_URL, DATABASE_NAME

async def setup_mongodb():
    """Setup MongoDB database and collections"""
    print("🔧 Setting up MongoDB for Sustainable Shopping Planner...")
    
    try:
        # Connect to MongoDB
        client = AsyncIOMotorClient(MONGODB_URL)
        db = client[DATABASE_NAME]
        
        print(f"✅ Connected to MongoDB: {DATABASE_NAME}")
        
        # Create collections with validation
        collections = {
            "products": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["name", "brand", "category", "price", "description"],
                        "properties": {
                            "name": {"bsonType": "string"},
                            "brand": {"bsonType": "string"},
                            "category": {"bsonType": "string"},
                            "price": {"bsonType": "double"},
                            "description": {"bsonType": "string"},
                            "sustainability_features": {"bsonType": "array"},
                            "image": {"bsonType": "string"},
                            "created_at": {"bsonType": "date"},
                            "updated_at": {"bsonType": "date"}
                        }
                    }
                }
            },
            "reviews": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["product_id", "user_id", "rating", "text"],
                        "properties": {
                            "product_id": {"bsonType": "string"},
                            "user_id": {"bsonType": "string"},
                            "rating": {"bsonType": "int", "minimum": 1, "maximum": 5},
                            "text": {"bsonType": "string"},
                            "date": {"bsonType": "date"},
                            "created_at": {"bsonType": "date"}
                        }
                    }
                }
            },
            "ai_ratings": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["product_id", "ai_rating", "sentiment_score", "sustainability_score", "confidence", "breakdown"],
                        "properties": {
                            "product_id": {"bsonType": "string"},
                            "ai_rating": {"bsonType": "double", "minimum": 1.0, "maximum": 5.0},
                            "sentiment_score": {"bsonType": "double", "minimum": -1.0, "maximum": 1.0},
                            "sustainability_score": {"bsonType": "double", "minimum": 0.0, "maximum": 1.0},
                            "confidence": {"bsonType": "double", "minimum": 0.0, "maximum": 1.0},
                            "breakdown": {"bsonType": "object"},
                            "timestamp": {"bsonType": "date"},
                            "created_at": {"bsonType": "date"},
                            "updated_at": {"bsonType": "date"}
                        }
                    }
                }
            },
            "users": {
                "validator": {
                    "$jsonSchema": {
                        "bsonType": "object",
                        "required": ["email", "username", "hashed_password"],
                        "properties": {
                            "email": {"bsonType": "string"},
                            "username": {"bsonType": "string"},
                            "hashed_password": {"bsonType": "string"},
                            "is_active": {"bsonType": "bool"},
                            "created_at": {"bsonType": "date"},
                            "updated_at": {"bsonType": "date"}
                        }
                    }
                }
            }
        }
        
        # Create collections
        for collection_name, config in collections.items():
            try:
                await db.create_collection(collection_name, validator=config["validator"])
                print(f"✅ Created collection: {collection_name}")
            except Exception as e:
                if "already exists" in str(e):
                    print(f"📊 Collection already exists: {collection_name}")
                else:
                    print(f"⚠️  Warning creating {collection_name}: {e}")
        
        # Create indexes
        indexes = {
            "products": [
                ("name", 1),
                ("brand", 1),
                ("category", 1),
                ("price", 1)
            ],
            "reviews": [
                ("product_id", 1),
                ("user_id", 1),
                ("rating", 1),
                ("date", -1),
                [("product_id", 1), ("rating", 1)]
            ],
            "ai_ratings": [
                ("product_id", 1),
                ("ai_rating", 1),
                ("timestamp", -1)
            ],
            "users": [
                ("email", 1),
                ("username", 1)
            ]
        }
        
        for collection_name, collection_indexes in indexes.items():
            collection = db[collection_name]
            for index_spec in collection_indexes:
                try:
                    await collection.create_index(index_spec)
                    print(f"✅ Created index on {collection_name}: {index_spec}")
                except Exception as e:
                    if "already exists" in str(e):
                        print(f"📊 Index already exists on {collection_name}: {index_spec}")
                    else:
                        print(f"⚠️  Warning creating index on {collection_name}: {e}")
        
        print("\n🎉 MongoDB setup completed successfully!")
        print(f"📊 Database: {DATABASE_NAME}")
        print("📋 Collections: products, reviews, ai_ratings, users")
        print("🔍 Indexes: Created for optimal query performance")
        
    except Exception as e:
        print(f"❌ Error setting up MongoDB: {e}")
        raise
    finally:
        if 'client' in locals():
            client.close()

async def test_connection():
    """Test MongoDB connection"""
    try:
        client = AsyncIOMotorClient(MONGODB_URL)
        db = client[DATABASE_NAME]
        
        # Test connection
        await client.admin.command('ping')
        print("✅ MongoDB connection test successful")
        
        # List collections
        collections = await db.list_collection_names()
        print(f"📋 Available collections: {collections}")
        
        return True
    except Exception as e:
        print(f"❌ MongoDB connection test failed: {e}")
        return False
    finally:
        if 'client' in locals():
            client.close()

def main():
    """Main setup function"""
    print("🌱 Sustainable Shopping Planner - MongoDB Setup")
    print("=" * 60)
    
    # Run setup
    asyncio.run(setup_mongodb())
    
    # Test connection
    print("\n🧪 Testing connection...")
    asyncio.run(test_connection())

if __name__ == "__main__":
    main()
