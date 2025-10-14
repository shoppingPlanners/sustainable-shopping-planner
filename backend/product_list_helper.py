#!/usr/bin/env python3
"""
Product List Helper Script for Sustainable Shopping Planner
Helper functions to work with existing product_list collection
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import json

# Your MongoDB configuration
MONGODB_URL = "mongodb://localhost:27017"
DATABASE_NAME = "sustainable-shopping-planner"

async def connect_to_mongodb():
    """Connect to your MongoDB database"""
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    
    # Test connection
    await client.admin.command('ping')
    print(f"✅ Connected to MongoDB: {DATABASE_NAME}")
    return client, db

async def list_products(db, limit=10):
    """List products from product_list collection"""
    try:
        products = await db.product_list.find().limit(limit).to_list(limit)
        
        print(f"\n📋 Found {len(products)} products (showing first {limit}):")
        print("=" * 60)
        
        for i, product in enumerate(products, 1):
            print(f"\n{i}. Product ID: {product.get('_id')}")
            print(f"   Name: {product.get('name', product.get('title', 'N/A'))}")
            print(f"   Brand: {product.get('brand', product.get('manufacturer', 'N/A'))}")
            print(f"   Price: ${product.get('price', product.get('cost', 'N/A'))}")
            print(f"   Category: {product.get('category', product.get('type', 'N/A'))}")
            print(f"   Description: {product.get('description', product.get('details', 'N/A'))[:100]}...")
            
    except Exception as e:
        print(f"❌ Error listing products: {e}")

async def get_product_by_id(db, product_id):
    """Get specific product by ID"""
    try:
        from bson import ObjectId
        
        # Try to convert to ObjectId if it's a string
        try:
            product_id = ObjectId(product_id)
        except:
            pass  # Keep as string if conversion fails
        
        product = await db.product_list.find_one({"_id": product_id})
        
        if product:
            print(f"\n📦 Product Details:")
            print("=" * 40)
            for key, value in product.items():
                print(f"{key}: {value}")
        else:
            print(f"❌ Product with ID {product_id} not found")
            
    except Exception as e:
        print(f"❌ Error getting product: {e}")

async def search_products(db, search_term):
    """Search products by name or description"""
    try:
        # Create text index if it doesn't exist
        try:
            await db.product_list.create_index([("name", "text"), ("description", "text")])
        except:
            pass  # Index might already exist
        
        # Search for products
        query = {"$text": {"$search": search_term}}
        products = await db.product_list.find(query).limit(10).to_list(10)
        
        print(f"\n🔍 Search results for '{search_term}':")
        print("=" * 50)
        
        if products:
            for i, product in enumerate(products, 1):
                print(f"\n{i}. {product.get('name', product.get('title', 'N/A'))}")
                print(f"   Brand: {product.get('brand', product.get('manufacturer', 'N/A'))}")
                print(f"   Price: ${product.get('price', product.get('cost', 'N/A'))}")
        else:
            print("No products found matching your search.")
            
    except Exception as e:
        print(f"❌ Error searching products: {e}")

async def get_product_stats(db):
    """Get statistics about the product_list collection"""
    try:
        # Total count
        total_count = await db.product_list.count_documents({})
        
        # Count by category
        categories = await db.product_list.distinct("category")
        if not categories:
            categories = await db.product_list.distinct("type")
        
        # Count by brand
        brands = await db.product_list.distinct("brand")
        if not brands:
            brands = await db.product_list.distinct("manufacturer")
        
        # Price range
        price_stats = await db.product_list.aggregate([
            {
                "$group": {
                    "_id": None,
                    "min_price": {"$min": "$price"},
                    "max_price": {"$max": "$price"},
                    "avg_price": {"$avg": "$price"}
                }
            }
        ]).to_list(1)
        
        print(f"\n📊 Product List Statistics:")
        print("=" * 40)
        print(f"Total Products: {total_count}")
        print(f"Categories: {len(categories)} ({', '.join(categories[:5])}{'...' if len(categories) > 5 else ''})")
        print(f"Brands: {len(brands)} ({', '.join(brands[:5])}{'...' if len(brands) > 5 else ''})")
        
        if price_stats:
            stats = price_stats[0]
            print(f"Price Range: ${stats.get('min_price', 0):.2f} - ${stats.get('max_price', 0):.2f}")
            print(f"Average Price: ${stats.get('avg_price', 0):.2f}")
        
    except Exception as e:
        print(f"❌ Error getting stats: {e}")

async def export_products(db, filename="products_export.json"):
    """Export products to JSON file"""
    try:
        products = await db.product_list.find().to_list()
        
        # Convert ObjectId to string for JSON serialization
        for product in products:
            if '_id' in product:
                product['_id'] = str(product['_id'])
        
        with open(filename, 'w') as f:
            json.dump(products, f, indent=2, default=str)
        
        print(f"✅ Exported {len(products)} products to {filename}")
        
    except Exception as e:
        print(f"❌ Error exporting products: {e}")

async def main():
    """Main function with interactive menu"""
    try:
        client, db = await connect_to_mongodb()
        
        while True:
            print("\n" + "="*60)
            print("🌱 Sustainable Shopping Planner - Product List Helper")
            print("="*60)
            print("1. List products")
            print("2. Get product by ID")
            print("3. Search products")
            print("4. Get statistics")
            print("5. Export products to JSON")
            print("6. Exit")
            print("="*60)
            
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == "1":
                limit = input("How many products to show? (default 10): ").strip()
                limit = int(limit) if limit.isdigit() else 10
                await list_products(db, limit)
                
            elif choice == "2":
                product_id = input("Enter product ID: ").strip()
                await get_product_by_id(db, product_id)
                
            elif choice == "3":
                search_term = input("Enter search term: ").strip()
                await search_products(db, search_term)
                
            elif choice == "4":
                await get_product_stats(db)
                
            elif choice == "5":
                filename = input("Enter filename (default: products_export.json): ").strip()
                filename = filename if filename else "products_export.json"
                await export_products(db, filename)
                
            elif choice == "6":
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice. Please try again.")
                
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    asyncio.run(main())
