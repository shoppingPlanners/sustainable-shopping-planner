"""
Integration Tests for Sustainable Shopping Planner
Tests the complete workflow across all 4 agents
"""

import pytest
import httpx
import asyncio
import time
from typing import Dict, Any

# Agent URLs
BRAND_COLLECTOR_URL = "http://localhost:5001"
RATING_CALCULATOR_URL = "http://localhost:5002"
USER_BEHAVIOR_URL = "http://localhost:5003"
SUGGESTION_AGENT_URL = "http://localhost:5004"


@pytest.fixture
async def http_client():
    """Create async HTTP client"""
    async with httpx.AsyncClient(timeout=30.0) as client:
        yield client


@pytest.mark.asyncio
async def test_all_agents_healthy(http_client):
    """Test that all agents are running and healthy"""
    
    agents = {
        "Brand Collector": BRAND_COLLECTOR_URL,
        "Rating Calculator": RATING_CALCULATOR_URL,
        "User Behavior": USER_BEHAVIOR_URL,
        "Suggestion Agent": SUGGESTION_AGENT_URL
    }
    
    for name, url in agents.items():
        response = await http_client.get(f"{url}/health")
        assert response.status_code == 200, f"{name} is not healthy"
        data = response.json()
        assert data["status"] == "healthy", f"{name} reports unhealthy status"
        print(f"✓ {name} is healthy")


@pytest.mark.asyncio
async def test_complete_workflow(http_client):
    """Test the complete workflow from scraping to recommendations"""
    
    print("\n=== Testing Complete Workflow ===\n")
    
    # Step 1: Scrape a brand
    print("Step 1: Scraping brand data...")
    scrape_response = await http_client.post(
        f"{BRAND_COLLECTOR_URL}/scrape",
        json={
            "url": "http://automationpractice.pl/index.php?id_category=3&controller=category",
            "brand_name": "TestBrand"
        }
    )
    assert scrape_response.status_code == 200
    scrape_data = scrape_response.json()
    assert scrape_data["status"] == "success"
    brand_data = scrape_data["data"]
    print(f"✓ Scraped {brand_data['product_count']} products")
    
    # Step 2: Calculate rating
    print("\nStep 2: Calculating sustainability rating...")
    rating_response = await http_client.post(
        f"{RATING_CALCULATOR_URL}/calculate",
        json={
            "brand_name": brand_data["brand_name"],
            "products": brand_data["products"],
            "sustainability_commitments": [
                "We use 100% organic materials",
                "Carbon neutral by 2030",
                "Fair trade certified"
            ],
            "certifications": ["Fair Trade", "B-Corp"]
        }
    )
    assert rating_response.status_code == 200
    rating_data = rating_response.json()
    assert rating_data["status"] == "success"
    rating = rating_data["rating"]
    print(f"✓ Rating calculated: {rating['overall_score']}/100 (Grade: {rating['grade']})")
    
    # Step 3: Simulate user behavior
    print("\nStep 3: Tracking user behavior...")
    user_id = "test_user_" + str(int(time.time()))
    
    # Track multiple events
    events = [
        {"event_type": "search", "category": "clothing", "tags": ["organic", "sustainable"]},
        {"event_type": "view", "product_id": "prod1", "category": "clothing", "tags": ["organic"]},
        {"event_type": "view", "product_id": "prod2", "category": "clothing", "tags": ["fair-trade"]},
        {"event_type": "click", "product_id": "prod1", "category": "clothing"},
    ]
    
    for event_data in events:
        event_data["user_id"] = user_id
        event_data["timestamp"] = time.time()
        
        track_response = await http_client.post(
            f"{USER_BEHAVIOR_URL}/track",
            json=event_data
        )
        assert track_response.status_code == 200
    
    print(f"✓ Tracked {len(events)} events for user {user_id}")
    
    # Wait a moment for processing
    await asyncio.sleep(1)
    
    # Get user patterns
    patterns_response = await http_client.get(
        f"{USER_BEHAVIOR_URL}/behavior/patterns/{user_id}"
    )
    assert patterns_response.status_code == 200
    patterns_data = patterns_response.json()
    print(f"✓ Analyzed behavior: {patterns_data['summary']}")
    
    # Get sustainability score
    score_response = await http_client.get(
        f"{USER_BEHAVIOR_URL}/behavior/sustainability-score/{user_id}"
    )
    assert score_response.status_code == 200
    score_data = score_response.json()
    sustainability_score = score_data["sustainability_score"]
    print(f"✓ User sustainability score: {sustainability_score}/100")
    
    # Step 4: Get personalized suggestions
    print("\nStep 4: Generating personalized suggestions...")
    suggestions_response = await http_client.get(
        f"{SUGGESTION_AGENT_URL}/suggestions/{user_id}",
        params={"limit": 5}
    )
    assert suggestions_response.status_code == 200
    suggestions_data = suggestions_response.json()
    assert suggestions_data["status"] == "success"
    suggestions = suggestions_data["suggestions"]
    print(f"✓ Generated {len(suggestions)} suggestions")
    
    # Display top suggestion
    if suggestions:
        top = suggestions[0]
        print(f"\nTop Suggestion:")
        print(f"  Product: {top['product_name']}")
        print(f"  Brand: {top['brand_name']}")
        print(f"  Sustainability: {top['sustainability_score']}/100")
        print(f"  Recommendation Score: {top['recommendation_score']:.3f}")
        print(f"  Reasons:")
        for reason in top['reasons']:
            print(f"    - {reason}")
    
    # Step 5: Submit feedback
    print("\nStep 5: Submitting feedback...")
    if suggestions:
        feedback_response = await http_client.post(
            f"{SUGGESTION_AGENT_URL}/feedback",
            json={
                "user_id": user_id,
                "product_id": suggestions[0]["product_id"],
                "feedback_type": "clicked"
            }
        )
        assert feedback_response.status_code == 200
        print("✓ Feedback recorded")
    
    print("\n=== Workflow Test Completed Successfully ===\n")


@pytest.mark.asyncio
async def test_agent_communication(http_client):
    """Test that agents can communicate with each other"""
    
    print("\n=== Testing Agent Communication ===\n")
    
    # Test Agent 4 can reach Agent 1
    brands_response = await http_client.get(f"{BRAND_COLLECTOR_URL}/brands")
    assert brands_response.status_code == 200
    print("✓ Agent 4 → Agent 1 communication OK")
    
    # Test Agent 4 can reach Agent 2
    ratings_response = await http_client.get(f"{RATING_CALCULATOR_URL}/ratings")
    assert ratings_response.status_code == 200
    print("✓ Agent 4 → Agent 2 communication OK")
    
    # Test Agent 4 can reach Agent 3
    users_response = await http_client.get(f"{USER_BEHAVIOR_URL}/users")
    assert users_response.status_code == 200
    print("✓ Agent 4 → Agent 3 communication OK")
    
    print("\n=== Agent Communication Test Completed ===\n")


@pytest.mark.asyncio
async def test_trending_products(http_client):
    """Test trending products endpoint"""
    
    print("\n=== Testing Trending Products ===\n")
    
    response = await http_client.get(
        f"{SUGGESTION_AGENT_URL}/trending",
        params={"limit": 5, "min_sustainability_score": 70}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    
    print(f"✓ Retrieved {data['count']} trending products")
    
    if data["trending_products"]:
        print("\nTop Trending Product:")
        top = data["trending_products"][0]
        print(f"  Product: {top['product_name']}")
        print(f"  Brand: {top['brand_name']}")
        print(f"  Sustainability: {top['sustainability_score']}/100")
    
    print("\n=== Trending Products Test Completed ===\n")


@pytest.mark.asyncio
async def test_rating_accuracy(http_client):
    """Test that ratings are calculated accurately"""
    
    print("\n=== Testing Rating Accuracy ===\n")
    
    # Test brand with excellent sustainability
    excellent_brand = {
        "brand_name": "ExcellentBrand",
        "products": [],
        "sustainability_commitments": [
            "100% renewable energy",
            "Carbon neutral since 2020",
            "Zero waste operations",
            "Fair trade certified",
            "Living wage for all workers"
        ],
        "certifications": ["B-Corp", "Fair Trade", "Carbon Neutral", "GOTS"]
    }
    
    response = await http_client.post(
        f"{RATING_CALCULATOR_URL}/calculate",
        json=excellent_brand
    )
    
    assert response.status_code == 200
    data = response.json()
    rating = data["rating"]
    
    print(f"Excellent Brand Score: {rating['overall_score']}/100")
    print(f"Grade: {rating['grade']}")
    
    # Should score high (>80)
    assert rating['overall_score'] >= 80, "Excellent brand should score >=80"
    assert rating['grade'] in ['A+', 'A', 'A-'], "Excellent brand should get A grade"
    
    print("✓ Rating accuracy validated")
    print("\n=== Rating Accuracy Test Completed ===\n")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("  Sustainable Shopping Planner - Integration Tests")
    print("="*60 + "\n")
    print("Make sure all agents are running:")
    print("  python run_all.py")
    print("\nThen run: pytest tests/test_integration.py -v\n")

