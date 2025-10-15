"""
Agent 4: Suggestion Agent
Generates personalized sustainable product recommendations
Integrates data from the other 3 agents
"""

import logging
import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Suggestion Agent",
    description="Intelligent recommendation system for sustainable shopping",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
SUGGESTION_AGENT_PORT = int(os.getenv("SUGGESTION_AGENT_PORT", "5004"))
BRAND_COLLECTOR_URL = os.getenv("BRAND_COLLECTOR_URL", "http://localhost:5001")
RATING_CALCULATOR_URL = os.getenv("RATING_CALCULATOR_URL", "http://localhost:5002")
USER_BEHAVIOR_URL = os.getenv("USER_BEHAVIOR_URL", "http://localhost:5003")

# Pydantic Models
class ProductSuggestion(BaseModel):
    product_id: str
    product_name: str
    brand_name: str
    sustainability_score: float
    price: str
    recommendation_score: float
    reasons: List[str]
    category: str
    url: str

class FeedbackRequest(BaseModel):
    user_id: str
    product_id: str
    feedback_type: str  # 'viewed', 'clicked', 'purchased', 'dismissed', 'liked'

# In-memory cache
recommendations_cache = {}
http_client = None


class RecommendationEngine:
    """Generates personalized product recommendations"""
    
    def __init__(self):
        self.weights = {
            'sustainability_score': 0.35,
            'user_preference_match': 0.30,
            'price_fit': 0.15,
            'popularity': 0.10,
            'novelty': 0.10
        }
    
    async def generate_suggestions(
        self,
        user_id: str,
        limit: int = 10,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Generate personalized product suggestions"""
        
        try:
            logger.info(f"Generating suggestions for user {user_id} with filters: {filters}")
            
            # Step 1: Get user behavior data
            user_data = await self._get_user_data(user_id)
            
            # Step 2: Get product catalog with ratings
            products = await self._get_products_with_ratings()
            
            if not products:
                logger.warning("No products available for recommendations")
                return []
            
            logger.info(f"Retrieved {len(products)} products from catalog")
            
            # Apply filters first
            if filters:
                category_filter = filters.get('category')
                if category_filter and category_filter != 'all':
                    # Filter by category - use actual category field from database
                    filtered = []
                    for p in products:
                        product_category = p.get('category', '').lower()
                        product_name = p.get('product_name', '').lower()
                        category_lower = category_filter.lower()
                        
                        # Match category using database category field (more accurate)
                        category_match = False
                        
                        if (category_lower == 'dresses' and 'dress' in product_category) or \
                           (category_lower == 't-shirts' and 't-shirt' in product_category) or \
                           (category_lower == 'tops' and 'top' in product_category) or \
                           (category_lower == 'activewear' and 'activewear' in product_category) or \
                           (category_lower == 'bottoms' and ('bottom' in product_category or 'jean' in product_category)) or \
                           (category_lower == 'jackets' and ('jacket' in product_category or 'outerwear' in product_category)) or \
                           (category_lower == 'accessories' and 'accessor' in product_category) or \
                           (category_lower == 'footwear' and 'footwear' in product_category) or \
                           (category_lower == 'summer' and ('summer' in product_category or 'summer' in product_name)) or \
                           (category_lower in product_category or category_lower in product_name):
                            category_match = True
                        
                        if category_match:
                            filtered.append(p)
                    
                    products = filtered
                    logger.info(f"After category filter '{category_filter}': {len(products)} products")
            
            if not products:
                logger.warning(f"No products match filters: {filters}")
                return []
            
            # Step 3: Calculate recommendation scores
            scored_products = []
            
            for product in products:
                score = self._calculate_recommendation_score(user_data, product)
                
                # Lower threshold to 0.1 to allow more matches
                if score > 0.1:
                    suggestion = {
                        'product_id': product.get('id', product.get('product_url', '')),
                        'product_name': product.get('product_name', 'Unknown'),
                        'brand_name': product.get('brand_name', 'Unknown'),
                        'sustainability_score': product.get('sustainability_score', 50),
                        'price': product.get('price', 'N/A'),
                        'recommendation_score': round(score, 3),
                        'reasons': self._generate_reasons(user_data, product, score),
                        'category': product.get('category', 'General'),
                        'url': product.get('product_url', '#'),
                        'sustainability_focus': product.get('sustainability_focus', [])
                    }
                    scored_products.append(suggestion)
            
            logger.info(f"Products passing score threshold: {len(scored_products)}")
            
            # Step 4: Sort and diversify
            scored_products.sort(key=lambda x: x['recommendation_score'], reverse=True)
            diversified = self._diversify_recommendations(scored_products, limit)
            
            logger.info(f"Generated {len(diversified)} suggestions for user {user_id}")
            return diversified
            
        except Exception as e:
            logger.error(f"Error generating suggestions: {e}", exc_info=True)
            return await self._get_fallback_recommendations(limit)
    
    def _calculate_recommendation_score(
        self,
        user_data: Dict[str, Any],
        product: Dict[str, Any]
    ) -> float:
        """Calculate multi-factor recommendation score"""
        
        # 1. Sustainability score
        sustainability_score = product.get('sustainability_score', 50) / 100.0
        
        # 2. User preference match
        preference_match = self._calculate_preference_match(user_data, product)
        
        # 3. Price fit
        price_fit = self._calculate_price_fit(user_data, product)
        
        # 4. Popularity (mock - would be based on actual data)
        popularity = 0.5
        
        # 5. Novelty
        novelty = self._calculate_novelty(user_data, product)
        
        # Calculate weighted score
        total_score = (
            sustainability_score * self.weights['sustainability_score'] +
            preference_match * self.weights['user_preference_match'] +
            price_fit * self.weights['price_fit'] +
            popularity * self.weights['popularity'] +
            novelty * self.weights['novelty']
        )
        
        return total_score
    
    def _calculate_preference_match(
        self,
        user_data: Dict[str, Any],
        product: Dict[str, Any]
    ) -> float:
        """Calculate how well product matches user preferences"""
        
        score = 0.0
        
        # Category match
        preferred_categories = user_data.get('preferred_categories', [])
        if preferred_categories and product.get('category') in preferred_categories:
            score += 0.4
        
        # Brand match
        preferred_brands = user_data.get('preferred_brands', [])
        if preferred_brands and product.get('brand_name') in preferred_brands:
            score += 0.3
        
        # Sustainability interests match
        user_interests = user_data.get('sustainability_interests', [])
        product_focus = product.get('sustainability_focus', [])
        
        if user_interests and product_focus:
            overlap = len(set(user_interests) & set(product_focus))
            if overlap > 0:
                score += min(overlap / max(len(user_interests), 1), 1.0) * 0.3
        
        # Return 0.6 as baseline even with no matches (generous scoring)
        return max(score, 0.6)
    
    def _calculate_price_fit(
        self,
        user_data: Dict[str, Any],
        product: Dict[str, Any]
    ) -> float:
        """Calculate price fit"""
        
        avg_price = user_data.get('average_price_point', 50)
        
        # Extract numeric price
        try:
            price_str = product.get('price', '0')
            price = float(''.join(c for c in str(price_str) if c.isdigit() or c == '.'))
        except:
            return 0.5
        
        if price == 0:
            return 0.5
        
        # Calculate distance from average
        diff_ratio = abs(price - avg_price) / max(avg_price, 1)
        fit_score = max(0, 1 - diff_ratio)
        
        return fit_score
    
    def _calculate_novelty(
        self,
        user_data: Dict[str, Any],
        product: Dict[str, Any]
    ) -> float:
        """Calculate novelty score"""
        
        viewed_products = set(user_data.get('viewed_products', []))
        product_id = product.get('id', product.get('product_url', ''))
        
        # Already viewed = no novelty
        if product_id in viewed_products:
            return 0.0
        
        # Check if category is new
        viewed_categories = set(user_data.get('viewed_categories', []))
        product_category = product.get('category')
        
        if product_category not in viewed_categories:
            return 0.8
        
        return 0.5
    
    def _generate_reasons(
        self,
        user_data: Dict[str, Any],
        product: Dict[str, Any],
        score: float
    ) -> List[str]:
        """Generate human-readable recommendation reasons"""
        
        reasons = []
        
        # Sustainability
        sustainability_score = product.get('sustainability_score', 50)
        if sustainability_score >= 80:
            reasons.append(f"Excellent sustainability rating ({sustainability_score}/100)")
        elif sustainability_score >= 65:
            reasons.append(f"Good sustainability practices ({sustainability_score}/100)")
        
        # User preferences
        preferred_categories = user_data.get('preferred_categories', [])
        if product.get('category') in preferred_categories:
            reasons.append("Matches your favorite categories")
        
        # Sustainability focus
        product_focus = product.get('sustainability_focus', [])
        if product_focus:
            focus_str = ', '.join(product_focus[:3])
            reasons.append(f"Features: {focus_str}")
        
        # Certifications from rating
        if product.get('certifications'):
            reasons.append(f"Certified: {', '.join(product.get('certifications', [])[:2])}")
        
        return reasons[:4]
    
    def _diversify_recommendations(
        self,
        products: List[Dict[str, Any]],
        limit: int
    ) -> List[Dict[str, Any]]:
        """Diversify recommendations"""
        
        if len(products) <= limit:
            return products
        
        diversified = []
        brand_counts = defaultdict(int)
        category_counts = defaultdict(int)
        
        for product in products:
            brand = product.get('brand_name')
            category = product.get('category')
            
            # Limit per brand and category
            if (brand_counts[brand] < 3 and 
                category_counts[category] < 4 and 
                len(diversified) < limit):
                
                diversified.append(product)
                brand_counts[brand] += 1
                category_counts[category] += 1
        
        # Fill remaining slots
        for product in products:
            if product not in diversified and len(diversified) < limit:
                diversified.append(product)
        
        return diversified[:limit]
    
    async def _get_user_data(self, user_id: str) -> Dict[str, Any]:
        """Fetch user data from User Behavior Tracker"""
        
        try:
            response = await http_client.get(
                f"{USER_BEHAVIOR_URL}/behavior/recommendations/{user_id}",
                timeout=5.0
            )
            
            if response.status_code == 200:
                return response.json()
            
        except Exception as e:
            logger.warning(f"Could not fetch user data: {e}")
        
        return {
            'sustainability_score': 50,
            'preferred_categories': [],
            'preferred_brands': [],
            'sustainability_interests': [],
            'average_price_point': 50,
            'viewed_products': [],
            'viewed_categories': []
        }
    
    async def _get_products_with_ratings(self) -> List[Dict[str, Any]]:
        """Fetch products with their sustainability ratings"""
        
        products_with_ratings = []
        
        try:
            # Get brand data
            brands_response = await http_client.get(
                f"{BRAND_COLLECTOR_URL}/brands",
                timeout=10.0
            )
            
            if brands_response.status_code != 200:
                logger.warning("Could not fetch brands")
                return []
            
            brands_data = brands_response.json()
            brands = brands_data.get('brands', [])
            
            # Get ratings
            ratings_response = await http_client.get(
                f"{RATING_CALCULATOR_URL}/ratings",
                timeout=10.0
            )
            
            ratings = {}
            if ratings_response.status_code == 200:
                ratings_data = ratings_response.json()
                for rating in ratings_data.get('ratings', []):
                    ratings[rating['brand_name']] = rating
            
            # Combine products with ratings
            for brand in brands:
                brand_name = brand.get('brand_name', 'Unknown')
                brand_rating = ratings.get(brand_name, {})
                sustainability_score = brand_rating.get('overall_score', 50)
                certifications = brand.get('certifications', [])
                
                for product in brand.get('products', []):
                    product_with_rating = {
                        **product,
                        'brand_name': brand_name,
                        'sustainability_score': sustainability_score,
                        'certifications': certifications,
                        'id': product.get('product_url', '')
                    }
                    products_with_ratings.append(product_with_rating)
            
            logger.info(f"Fetched {len(products_with_ratings)} products with ratings")
            
        except Exception as e:
            logger.error(f"Error fetching products: {e}")
        
        return products_with_ratings
    
    async def _get_fallback_recommendations(self, limit: int) -> List[Dict[str, Any]]:
        """Return fallback recommendations when main algorithm fails"""
        
        try:
            products = await self._get_products_with_ratings()
            
            # Sort by sustainability score
            products.sort(key=lambda x: x.get('sustainability_score', 0), reverse=True)
            
            return [{
                'product_id': p.get('id', ''),
                'product_name': p.get('product_name', 'Unknown'),
                'brand_name': p.get('brand_name', 'Unknown'),
                'sustainability_score': p.get('sustainability_score', 50),
                'price': p.get('price', 'N/A'),
                'recommendation_score': p.get('sustainability_score', 50) / 100,
                'reasons': ['Highly sustainable product'],
                'category': p.get('category', 'General'),
                'url': p.get('product_url', '#')
            } for p in products[:limit]]
            
        except:
            return []


# Global instances
recommendation_engine = RecommendationEngine()


@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    global http_client
    
    logger.info("🚀 Starting Suggestion Agent...")
    
    http_client = httpx.AsyncClient(timeout=30.0)
    
    # Test connections to other agents
    await test_connections()
    
    logger.info("✅ Suggestion Agent started successfully!")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global http_client
    
    logger.info("Shutting down Suggestion Agent...")
    
    if http_client:
        await http_client.aclose()


async def test_connections():
    """Test connections to other agents"""
    
    agents = {
        "Brand Collector": BRAND_COLLECTOR_URL,
        "Rating Calculator": RATING_CALCULATOR_URL,
        "User Behavior Tracker": USER_BEHAVIOR_URL
    }
    
    for name, url in agents.items():
        try:
            response = await http_client.get(f"{url}/health", timeout=5.0)
            if response.status_code == 200:
                logger.info(f"✅ Connected to {name}")
            else:
                logger.warning(f"⚠️ {name} returned status {response.status_code}")
        except Exception as e:
            logger.warning(f"⚠️ Could not connect to {name}: {e}")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "agent": "Suggestion Agent",
        "version": "1.0.0",
        "status": "operational",
        "description": "Personalized sustainable product recommendations",
        "endpoints": {
            "suggestions": "GET /suggestions/{user_id}",
            "trending": "GET /trending",
            "feedback": "POST /feedback",
            "health": "GET /health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "connected_agents": {
            "brand_collector": BRAND_COLLECTOR_URL,
            "rating_calculator": RATING_CALCULATOR_URL,
            "user_behavior": USER_BEHAVIOR_URL
        }
    }


@app.get("/suggestions/{user_id}")
async def get_suggestions(
    user_id: str,
    limit: int = Query(10, ge=1, le=50),
    category: Optional[str] = None,
    min_sustainability_score: Optional[float] = Query(None, ge=0, le=100)
):
    """Get personalized product suggestions for a user"""
    
    try:
        logger.info(f"Generating suggestions for user {user_id}")
        
        # Build filters
        filters = {}
        if category:
            filters['category'] = category
        if min_sustainability_score:
            filters['min_sustainability_score'] = min_sustainability_score
        
        # Generate suggestions
        suggestions = await recommendation_engine.generate_suggestions(
            user_id=user_id,
            limit=limit,
            filters=filters
        )
        
        # Cache results
        cache_key = f"{user_id}_{limit}"
        recommendations_cache[cache_key] = {
            'suggestions': suggestions,
            'generated_at': datetime.utcnow(),
            'expires_at': datetime.utcnow() + timedelta(hours=1)
        }
        
        return {
            "status": "success",
            "user_id": user_id,
            "suggestions": suggestions,
            "count": len(suggestions),
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error generating suggestions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/trending")
async def get_trending_products(
    limit: int = Query(10, ge=1, le=50),
    min_sustainability_score: Optional[float] = Query(70, ge=0, le=100)
):
    """Get trending sustainable products"""
    
    try:
        # Get all products with ratings
        products = await recommendation_engine._get_products_with_ratings()
        
        # Filter by sustainability score
        if min_sustainability_score:
            products = [
                p for p in products
                if p.get('sustainability_score', 0) >= min_sustainability_score
            ]
        
        # Sort by sustainability score
        products.sort(key=lambda x: x.get('sustainability_score', 0), reverse=True)
        
        trending = [{
            'product_id': p.get('id', ''),
            'product_name': p.get('product_name', 'Unknown'),
            'brand_name': p.get('brand_name', 'Unknown'),
            'sustainability_score': p.get('sustainability_score', 50),
            'price': p.get('price', 'N/A'),
            'category': p.get('category', 'General'),
            'url': p.get('product_url', '#')
        } for p in products[:limit]]
        
        return {
            "status": "success",
            "trending_products": trending,
            "count": len(trending),
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting trending products: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/feedback")
async def submit_feedback(feedback: FeedbackRequest):
    """Submit feedback on a suggestion"""
    
    try:
        logger.info(f"Received feedback from user {feedback.user_id}")
        
        # Forward to User Behavior Tracker
        await http_client.post(
            f"{USER_BEHAVIOR_URL}/track",
            json={
                'user_id': feedback.user_id,
                'event_type': f'recommendation_{feedback.feedback_type}',
                'product_id': feedback.product_id,
                'timestamp': datetime.utcnow().timestamp()
            }
        )
        
        # Clear cache for this user
        cache_keys_to_remove = [k for k in recommendations_cache.keys() if k.startswith(feedback.user_id)]
        for key in cache_keys_to_remove:
            del recommendations_cache[key]
        
        return {
            "status": "success",
            "message": "Feedback recorded",
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error processing feedback: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats")
async def get_stats():
    """Get suggestion engine statistics"""
    
    return {
        "status": "success",
        "cached_recommendations": len(recommendations_cache),
        "recommendation_weights": recommendation_engine.weights,
        "timestamp": datetime.utcnow().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=SUGGESTION_AGENT_PORT)

