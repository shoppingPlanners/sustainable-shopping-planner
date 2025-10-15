#!/usr/bin/env python3
"""
Demonstration script to show the 4-agent integration flow
Run after starting all services with: python run_all_script.py

This script demonstrates:
- Agent 1: Brand Data Collector (Port 5001)
- Agent 2: Rating Calculator (Port 5002)
- Agent 3: User Behavior Tracker (Port 5003)
- Agent 4: Suggestion Agent (Port 5004) - Orchestrator
"""

import requests
import json
import time
from typing import Dict, Any, List

# Agent URLs
AGENTS = {
    "brand_collector": "http://localhost:5001",
    "rating_calculator": "http://localhost:5002",
    "user_behavior": "http://localhost:5003",
    "suggestion_agent": "http://localhost:5004",
    "backend": "http://localhost:8000"
}

def print_section(title: str):
    """Print a formatted section header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")

def check_agent_health():
    """Step 1: Check all agents are running"""
    print_section("STEP 1: Health Check - All Agents")
    
    all_healthy = True
    for name, url in AGENTS.items():
        try:
            response = requests.get(f"{url}/health", timeout=3)
            status = "✅ HEALTHY" if response.status_code == 200 else "⚠️  DEGRADED"
            print(f"{name:20} {url:30} {status}")
            if response.status_code == 200:
                data = response.json()
                print(f"                     Response: {json.dumps(data)[:100]}...")
        except requests.exceptions.RequestException as e:
            print(f"{name:20} {url:30} ❌ OFFLINE - {str(e)[:50]}")
            all_healthy = False
    
    time.sleep(1)
    return all_healthy

def demonstrate_brand_collector():
    """Step 2: Get products from Brand Data Collector (Agent 1)"""
    print_section("STEP 2: Brand Data Collector (Agent 1)")
    
    try:
        print("🔍 Fetching brands from Agent 1...")
        response = requests.get(f"{AGENTS['brand_collector']}/brands?limit=3")
        
        if response.status_code == 200:
            data = response.json()
            brands = data.get('brands', [])
            
            print(f"✅ Retrieved {len(brands)} brands")
            
            for i, brand in enumerate(brands[:2], 1):
                print(f"\n  Brand {i}:")
                print(f"    Name: {brand.get('brand_domain', 'N/A')}")
                print(f"    Products: {brand.get('product_count', 0)}")
                print(f"    Certifications: {', '.join(brand.get('certifications', [])[:3])}")
                
                products = brand.get('products', [])[:2]
                for j, product in enumerate(products, 1):
                    print(f"      Product {j}: {product.get('product_name', 'N/A')} - ${product.get('price', 'N/A')}")
            
            return brands
        else:
            print(f"❌ Failed to fetch brands: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def demonstrate_rating_calculator():
    """Step 3: Get sustainability ratings from Rating Calculator (Agent 2)"""
    print_section("STEP 3: Rating Calculator (Agent 2)")
    
    try:
        print("📊 Calculating sustainability ratings...")
        response = requests.get(f"{AGENTS['rating_calculator']}/ratings")
        
        if response.status_code == 200:
            data = response.json()
            ratings = data.get('ratings', [])
            
            print(f"✅ Calculated ratings for {len(ratings)} brands")
            
            # Show top 5 rated brands
            sorted_ratings = sorted(ratings, key=lambda x: x.get('overall_score', 0), reverse=True)
            print("\n  Top 5 Sustainable Brands:")
            for i, rating in enumerate(sorted_ratings[:5], 1):
                print(f"    {i}. {rating.get('brand_name', 'N/A'):30} Score: {rating.get('overall_score', 0):.1f}/100")
            
            return ratings
        else:
            print(f"❌ Failed to get ratings: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def demonstrate_user_behavior():
    """Step 4: Track and analyze user behavior (Agent 3)"""
    print_section("STEP 4: User Behavior Tracker (Agent 3)")
    
    test_user_id = "demo_user_123"
    
    try:
        # Track a sample event
        print(f"📝 Tracking user event for: {test_user_id}")
        
        event_data = {
            "user_id": test_user_id,
            "session_id": "demo_session",
            "event_type": "product_view",
            "product_id": "sustainable_tshirt_001",
            "timestamp": time.time(),
            "metadata": {
                "category": "t-shirts",
                "sustainability_score": 85
            }
        }
        
        track_response = requests.post(
            f"{AGENTS['user_behavior']}/track",
            json=event_data,
            timeout=5
        )
        
        if track_response.status_code == 200:
            print("✅ Event tracked successfully")
            print(f"   Event: {event_data['event_type']}")
            print(f"   Product: {event_data['product_id']}")
        
        # Get user recommendations data
        print(f"\n🔍 Fetching user behavior data...")
        behavior_response = requests.get(
            f"{AGENTS['user_behavior']}/behavior/recommendations/{test_user_id}",
            timeout=5
        )
        
        if behavior_response.status_code == 200:
            behavior_data = behavior_response.json()
            print("✅ User behavior analysis retrieved")
            print(f"   Sustainability Score: {behavior_data.get('sustainability_score', 'N/A')}")
            print(f"   Preferred Categories: {behavior_data.get('preferred_categories', [])}")
            print(f"   Average Price Point: ${behavior_data.get('average_price_point', 'N/A')}")
            return behavior_data
        else:
            print(f"⚠️  Behavior data not available (status {behavior_response.status_code})")
            return {}
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return {}

def demonstrate_suggestion_agent():
    """Step 5: Generate personalized suggestions using Suggestion Agent (Agent 4)"""
    print_section("STEP 5: Suggestion Agent (Agent 4) - ORCHESTRATOR")
    
    test_user_id = "demo_user_123"
    
    try:
        print(f"🎯 Generating personalized suggestions for: {test_user_id}")
        print("   (This agent calls Agents 1, 2, and 3 internally)")
        print()
        
        response = requests.get(
            f"{AGENTS['suggestion_agent']}/suggestions/{test_user_id}?limit=5",
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            suggestions = data.get('suggestions', [])
            
            print(f"✅ Generated {len(suggestions)} personalized suggestions\n")
            
            for i, suggestion in enumerate(suggestions, 1):
                print(f"  Suggestion {i}:")
                print(f"    Product: {suggestion.get('product_name', 'N/A')}")
                print(f"    Brand: {suggestion.get('brand_name', 'N/A')}")
                print(f"    Category: {suggestion.get('category', 'N/A')}")
                print(f"    Sustainability Score: {suggestion.get('sustainability_score', 0)}/100")
                print(f"    Recommendation Score: {suggestion.get('recommendation_score', 0):.3f}")
                print(f"    Price: {suggestion.get('price', 'N/A')}")
                print(f"    Reasons: {', '.join(suggestion.get('reasons', [])[:2])}")
                print()
            
            return suggestions
        else:
            print(f"❌ Failed to generate suggestions: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return []
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def demonstrate_trending_products():
    """Bonus: Get trending sustainable products"""
    print_section("BONUS: Trending Sustainable Products")
    
    try:
        print("🔥 Fetching trending products (min 70% sustainability)...")
        
        response = requests.get(
            f"{AGENTS['suggestion_agent']}/trending?limit=5&min_sustainability_score=70",
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            trending = data.get('trending_products', [])
            
            print(f"✅ Found {len(trending)} trending products\n")
            
            for i, product in enumerate(trending, 1):
                print(f"  {i}. {product.get('product_name', 'N/A')}")
                print(f"     Brand: {product.get('brand_name', 'N/A')}")
                print(f"     Sustainability: {product.get('sustainability_score', 0)}/100")
                print(f"     Price: {product.get('price', 'N/A')}")
                print()
            
            return trending
        else:
            print(f"❌ Failed to get trending: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def demonstrate_backend_integration():
    """Step 6: Demonstrate backend integration with agents"""
    print_section("STEP 6: Backend Integration - Complete Flow")
    
    try:
        print("🔄 Testing Backend → Agent 4 → [Agents 1,2,3] flow...")
        print()
        
        # Test preferences save
        preferences = {
            "category": "t-shirts",
            "budget": "30-50",
            "style": "casual",
            "sustainability_priorities": "organic, fair trade",
            "size": "M"
        }
        
        print(f"📝 Saving preferences: {preferences}")
        save_response = requests.post(
            f"{AGENTS['backend']}/api/preferences/save",
            json=preferences,
            timeout=5
        )
        
        if save_response.status_code == 200:
            print("✅ Preferences saved successfully")
            
            # Get recommendations (this should now use the agent flow)
            print("\n🎯 Getting recommendations through backend...")
            params = {
                "category": "t-shirts",
                "budget": "30-50",
                "sustainability_priorities": "organic",
                "limit": 5,
                "user_id": "demo_user_123"
            }
            
            rec_response = requests.get(
                f"{AGENTS['backend']}/api/preferences/recommendations",
                params=params,
                timeout=15
            )
            
            if rec_response.status_code == 200:
                recommendations = rec_response.json()
                print(f"✅ Received {len(recommendations)} recommendations from backend")
                print("\n  Top 3 Recommendations:")
                for i, rec in enumerate(recommendations[:3], 1):
                    print(f"    {i}. {rec.get('name', 'N/A')}")
                    print(f"       Brand: {rec.get('brand', 'N/A')}")
                    print(f"       Sustainability: {rec.get('sustainabilityScore', 0)}/100")
                    print(f"       Match Score: {rec.get('match_score', 0):.1f}")
                    print(f"       Reason: {rec.get('reason', 'N/A')[:60]}...")
                    print()
            else:
                print(f"⚠️  Failed to get recommendations: {rec_response.status_code}")
        else:
            print(f"⚠️  Failed to save preferences: {save_response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main demonstration flow"""
    print("\n" + "="*70)
    print("  🌱 SUSTAINABLE SHOPPING PLANNER - AGENT INTEGRATION DEMO")
    print("="*70)
    print("\n  This demonstrates how 4 AI agents work together to provide")
    print("  personalized sustainable shopping recommendations.\n")
    print("  Make sure you've started all services with:")
    print("  $ python run_all_script.py")
    print()
    
    input("Press Enter to start the demonstration...")
    
    # Run each step
    if not check_agent_health():
        print("\n⚠️  WARNING: Some agents are offline. Results may be limited.")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Exiting...")
            return
    
    demonstrate_brand_collector()
    time.sleep(1)
    
    demonstrate_rating_calculator()
    time.sleep(1)
    
    demonstrate_user_behavior()
    time.sleep(1)
    
    demonstrate_suggestion_agent()
    time.sleep(1)
    
    demonstrate_trending_products()
    time.sleep(1)
    
    demonstrate_backend_integration()
    
    # Final summary
    print_section("DEMONSTRATION COMPLETE")
    print("✅ You've seen all 4 agents working together!")
    print()
    print("Flow Summary:")
    print("  1. Agent 1 (Brand Collector) - Provides product data")
    print("  2. Agent 2 (Rating Calculator) - Calculates sustainability scores")
    print("  3. Agent 3 (User Behavior) - Tracks and analyzes user preferences")
    print("  4. Agent 4 (Suggestion) - Orchestrates all agents for recommendations")
    print()
    print("Integration:")
    print("  Frontend → Backend → Agent 4 → [Agents 1, 2, 3] → Results")
    print()
    print("="*70)
    print()

if __name__ == "__main__":
    main()

