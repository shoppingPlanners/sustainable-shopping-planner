#!/usr/bin/env python3
"""
Proper Agent Integration: Use Rating Calculator Agent to score all products

This demonstrates the correct multi-agent flow:
1. Brand Data Collector reads products from DB
2. Calls Rating Calculator Agent (Agent 2) via HTTP API
3. Rating Calculator calculates sustainability scores
4. Scores are saved back to database
"""

import requests
from pymongo import MongoClient
import time

# Agent URLs
RATING_CALCULATOR_URL = "http://localhost:5002"
DATABASE_URL = "mongodb://localhost:27017/sustainable-shopping-planner"

def test_rating_calculator():
    """Test if Rating Calculator is running"""
    try:
        response = requests.get(f"{RATING_CALCULATOR_URL}/health", timeout=3)
        if response.status_code == 200:
            print("✅ Rating Calculator Agent is running")
            return True
        else:
            print(f"⚠️  Rating Calculator returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Rating Calculator is not running: {e}")
        print("   Start it with: python run_all_script.py")
        return False

def calculate_product_score(product, brand_certs=[]):
    """Call Rating Calculator Agent to score a product"""
    try:
        # Extract numeric price from string like "$17"
        price_str = str(product.get("price", "0"))
        try:
            price = float(''.join(c for c in price_str if c.isdigit() or c == '.'))
        except:
            price = 0
        
        # Prepare product data for rating
        product_data = {
            "product_name": product.get("product_name", ""),
            "category": product.get("category", ""),
            "price": price,
            "description": product.get("description", ""),
            "sustainability_focus": product.get("sustainability_focus", []),
            "certifications": brand_certs  # Use brand certifications
        }
        
        # Call Rating Calculator Agent
        response = requests.post(
            f"{RATING_CALCULATOR_URL}/calculate_product_score",
            json=product_data,
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            return {
                "sustainability_score": result.get("sustainability_score", 50),
                "rating": result.get("rating", 3.5),
                "score_breakdown": result.get("score_breakdown", {})
            }
        else:
            print(f"   ⚠️  Rating calc returned {response.status_code}")
            return None
            
    except Exception as e:
        print(f"   ❌ Error calling Rating Calculator: {e}")
        return None

def score_all_products():
    """
    Main integration function:
    - Reads products from DB
    - Calls Rating Calculator Agent for each
    - Updates DB with scores
    """
    
    print("="*70)
    print("  🤖 AGENT INTEGRATION: Product Scoring")
    print("="*70)
    print("\nThis demonstrates proper multi-agent collaboration:")
    print("  Agent 1 (Brand Collector) → Agent 2 (Rating Calculator)")
    print()
    
    # Step 1: Check if Rating Calculator is running
    if not test_rating_calculator():
        return
    
    # Step 2: Connect to database
    print("\n📊 Connecting to database...")
    try:
        client = MongoClient(DATABASE_URL)
        db = client.get_default_database()
        db.command('ping')
        print("✅ Connected to MongoDB")
    except Exception as e:
        print(f"❌ Database error: {e}")
        return
    
    # Step 3: Get all brands and products
    brands = list(db.brands.find())
    total_products = sum(len(b.get('products', [])) for b in brands)
    
    print(f"✅ Found {len(brands)} brands with {total_products} products")
    print(f"\n🔄 Scoring products using Rating Calculator Agent...")
    print()
    
    # Step 4: Score each product using the agent
    scored_count = 0
    updated_brands = []
    
    for brand_idx, brand in enumerate(brands, 1):
        brand_domain = brand.get('brand_domain', 'Unknown')
        brand_certs = brand.get('certifications', [])
        products = brand.get('products', [])
        
        if not products:
            continue
        
        print(f"[{brand_idx}/{len(brands)}] {brand_domain} ({len(products)} products)")
        
        updated_products = []
        for product_idx, product in enumerate(products, 1):
            # Call Rating Calculator Agent
            score_result = calculate_product_score(product, brand_certs)
            
            if score_result:
                # Update product with scores from agent
                product['sustainability_score'] = score_result['sustainability_score']
                product['rating'] = score_result['rating']
                product['score_breakdown'] = score_result['score_breakdown']
                scored_count += 1
                
                # Show progress
                if product_idx <= 3:  # Show first 3 products per brand
                    print(f"  ✅ {product.get('product_name', 'N/A')[:40]:40} Score: {score_result['sustainability_score']:3}/100 | Rating: {score_result['rating']}")
            else:
                # Keep existing score or use default
                product['sustainability_score'] = product.get('sustainability_score', 50)
                product['rating'] = product.get('rating', 3.5)
            
            updated_products.append(product)
            
            # Small delay to avoid overwhelming the agent
            time.sleep(0.05)
        
        # Update brand in database
        db.brands.update_one(
            {'_id': brand['_id']},
            {'$set': {'products': updated_products}}
        )
        
        updated_brands.append(brand_domain)
    
    # Step 5: Summary
    print("\n" + "="*70)
    print("  📊 SCORING COMPLETE")
    print("="*70)
    print(f"\n✅ Scored {scored_count} products using Rating Calculator Agent")
    print(f"✅ Updated {len(updated_brands)} brands in database")
    print()
    
    # Show sample scored products
    print("📦 Sample Scored Products:")
    sample_products = []
    for brand in db.brands.find().limit(3):
        if brand.get('products'):
            sample_products.extend(brand['products'][:3])
    
    for i, product in enumerate(sample_products[:10], 1):
        name = product.get('product_name', 'N/A')[:45]
        score = product.get('sustainability_score', 0)
        rating = product.get('rating', 0)
        breakdown = product.get('score_breakdown', {})
        
        print(f"  {i:2}. {name:45} | Score: {score:3}/100 | Rating: {rating:.1f}")
        if breakdown and i <= 3:  # Show breakdown for first 3
            print(f"      Breakdown: Materials +{breakdown.get('materials', 0)}, "
                  f"Certs +{breakdown.get('certifications', 0)}, "
                  f"Focus +{breakdown.get('sustainability_focus', 0)}")
    
    print("\n🎉 Agent integration successful!")
    print("   The Rating Calculator Agent is now properly scoring products.")
    print()
    
    client.close()

if __name__ == "__main__":
    score_all_products()

