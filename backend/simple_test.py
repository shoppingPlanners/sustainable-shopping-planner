#!/usr/bin/env python3
"""
Simple MongoDB connection test
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def test_mongodb():
    try:
        print("Testing MongoDB connection...")
        client = AsyncIOMotorClient('mongodb://localhost:27017')
        
        # Test connection
        await client.admin.command('ping')
        print("MongoDB connection successful!")
        
        # Test database access
        db = client['sustainable-shopping-planner']
        collections = await db.list_collection_names()
        print(f"Database collections: {collections}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"Connection failed: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_mongodb())
