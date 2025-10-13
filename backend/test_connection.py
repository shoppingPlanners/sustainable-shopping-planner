#!/usr/bin/env python3
"""
Test connection to your existing MongoDB database
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

# Your MongoDB configuration
MONGODB_URL = "mongodb://localhost:27017"
DATABASE_NAME = "sustainable-shopping-planner"

async def test_connection():
    """Test connection to your MongoDB database"""
    try:
        print("🔌 Testing MongoDB connection...")
        print(f"URL: {MONGODB_URL}")
        print(f"Database: {DATABASE_NAME}")
        
        # Connect to MongoDB
        client = AsyncIOMotorClient(MONGODB_URL)
        db = client[DATABASE_NAME]
        
        # Test connection
        await client.admin.command('ping')
        print("✅ MongoDB connection successful!")
        
        # List collections
        collections = await db.list_collection_names()
        print(f"\n📋 Available collections: {collections}")
        
        # Check if product_list exists
        if "product_list" in collections:
            print("\n🎉 Found your existing product_list collection!")
            
            # Get sample data
            sample_docs = await db.product_list.find().limit(3).to_list(3)
            print(f"\n📊 Sample documents ({len(sample_docs)}):")
            
            for i, doc in enumerate(sample_docs, 1):
                print(f"\n{i}. Document structure:")
                for key, value in doc.items():
                    if key == '_id':
                        print(f"   {key}: {type(value).__name__} (ObjectId)")
                    else:
                        print(f"   {key}: {type(value).__name__} = {str(value)[:50]}{'...' if len(str(value)) > 50 else ''}")
            
            # Get total count
            total_count = await db.product_list.count_documents({})
            print(f"\n📈 Total documents in product_list: {total_count}")
            
            # Show field mapping suggestions
            print(f"\n🔄 Field mapping suggestions:")
            if sample_docs:
                sample = sample_docs[0]
                print(f"   name/title → name")
                print(f"   brand/manufacturer → brand")
                print(f"   price/cost → price")
                print(f"   category/type → category")
                print(f"   description/details → description")
                print(f"   image/image_url → image")
        else:
            print("\n⚠️  product_list collection not found")
            print("   This might be a new database or the collection has a different name.")
        
        # Check if new collections exist
        new_collections = ["products", "reviews", "ai_ratings", "users"]
        existing_new = [col for col in new_collections if col in collections]
        
        if existing_new:
            print(f"\n📊 New collections found: {existing_new}")
        else:
            print(f"\n📝 No new collections found. You can create them by running the migration script.")
        
        print(f"\n🚀 Next steps:")
        print(f"   1. Run: python product_list_helper.py (to explore your data)")
        print(f"   2. Run: python product_list_migration.py (to migrate data)")
        print(f"   3. Run: python start.py (to start the backend)")
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print(f"\n🔧 Troubleshooting:")
        print(f"   1. Make sure MongoDB is running")
        print(f"   2. Check the connection string: {MONGODB_URL}")
        print(f"   3. Verify database name: {DATABASE_NAME}")
        print(f"   4. Check if MongoDB is accessible on port 27017")

if __name__ == "__main__":
    asyncio.run(test_connection())
