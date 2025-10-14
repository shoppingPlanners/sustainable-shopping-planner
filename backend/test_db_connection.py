#!/usr/bin/env python3
"""
Test script to check database connection and data structure.
"""

import asyncio
import os
from database import db
from dotenv import load_dotenv

load_dotenv()

async def test_database():
    """Test database connection and check items."""
    try:
        print("Connecting to database...")
        await db.connect()
        print("✅ Connected to database successfully")
        
        # Check if we can find any items
        print("\nChecking items in database...")
        items = await db.item.find_many()
        print(f"Found {len(items)} items in database")
        
        if items:
            print("\nFirst item structure:")
            first_item = items[0]
            print(f"ID: {first_item.id}")
            print(f"Name: {first_item.name}")
            print(f"Brand: {first_item.brand}")
            print(f"Category: {first_item.category}")
            print(f"Features: {first_item.features}")
        else:
            print("❌ No items found in database")
            
            # Let's check what collections exist
            print("\nChecking database structure...")
            # This is a bit tricky with Prisma, let's try to create a test item
            print("Attempting to create a test item...")
            test_item = await db.item.create(data={
                "itemId": 999,
                "name": "Test Item",
                "brand": "Test Brand",
                "rating": 4.5,
                "sustainabilityScore": 85,
                "price": "$50",
                "image": "/test.jpg",
                "buyUrl": "https://test.com",
                "features": ["Test Feature"],
                "category": "test"
            })
            print(f"✅ Test item created: {test_item.id}")
            
            # Clean up test item
            await db.item.delete(where={"id": test_item.id})
            print("✅ Test item cleaned up")
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()
    finally:
        await db.disconnect()
        print("\nDisconnected from database")

if __name__ == "__main__":
    asyncio.run(test_database())
