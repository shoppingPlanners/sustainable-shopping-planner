"""
Agent 3: User Behavior Tracker
Tracks and analyzes user behavior to understand preferences and patterns
"""

import logging
import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="User Behavior Tracker Agent",
    description="Tracks and analyzes user behavior patterns",
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
USER_BEHAVIOR_PORT = int(os.getenv("USER_BEHAVIOR_PORT", "5003"))
EVENTS_FILE = "user_events.json"
PROFILES_FILE = "user_profiles.json"

# Pydantic Models
class TrackingEvent(BaseModel):
    user_id: str
    event_type: str  # 'view', 'search', 'click', 'purchase', 'add_to_cart', 'favorite'
    product_id: Optional[str] = None
    brand_id: Optional[str] = None
    category: Optional[str] = None
    tags: List[str] = []
    metadata: Optional[Dict[str, Any]] = None
    timestamp: Optional[float] = None

class UserProfile(BaseModel):
    user_id: str
    preferences: Dict[str, Any] = {}
    sustainability_score: float = 50.0
    price_range: Dict[str, float] = {}
    favorite_brands: List[str] = []
    favorite_categories: List[str] = []

# In-memory storage
user_events = defaultdict(list)
user_profiles = {}


class BehaviorAnalyzer:
    """Analyzes user behavior to extract patterns and preferences"""
    
    def __init__(self):
        self.sustainability_keywords = [
            'organic', 'sustainable', 'eco-friendly', 'recycled', 'fair trade',
            'carbon neutral', 'biodegradable', 'ethical', 'green', 'vegan'
        ]
    
    def analyze_user_patterns(
        self,
        user_id: str,
        days_back: int = 30
    ) -> Dict[str, Any]:
        """Analyze user behavior patterns"""
        
        events = self._get_user_events(user_id, days_back)
        
        if not events:
            return {
                'patterns': [],
                'summary': 'Insufficient data'
            }
        
        patterns = []
        
        # Category preferences
        category_counts = defaultdict(int)
        for event in events:
            if event.get('category'):
                category_counts[event['category']] += 1
        
        if category_counts:
            top_categories = sorted(
                category_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
            
            patterns.append({
                'pattern_type': 'category_preference',
                'categories': [cat for cat, _ in top_categories],
                'confidence': min(len(events) / 20, 1.0),
                'created_at': datetime.utcnow().isoformat()
            })
        
        # Brand preferences
        brand_counts = defaultdict(int)
        for event in events:
            if event.get('brand_id'):
                brand_counts[event['brand_id']] += 1
        
        if brand_counts:
            top_brands = sorted(
                brand_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
            
            patterns.append({
                'pattern_type': 'brand_preference',
                'brands': [brand for brand, _ in top_brands],
                'confidence': min(len(events) / 15, 1.0),
                'created_at': datetime.utcnow().isoformat()
            })
        
        # Sustainability focus
        sustainability_events = 0
        for event in events:
            tags = event.get('tags', [])
            if any(keyword in ' '.join(tags).lower() for keyword in self.sustainability_keywords):
                sustainability_events += 1
        
        if sustainability_events > 0:
            sustainability_ratio = sustainability_events / len(events)
            patterns.append({
                'pattern_type': 'sustainability_focus',
                'interests': self._extract_sustainability_interests(events),
                'confidence': sustainability_ratio,
                'created_at': datetime.utcnow().isoformat()
            })
        
        # Price sensitivity
        price_pattern = self._analyze_price_sensitivity(events)
        if price_pattern:
            patterns.append(price_pattern)
        
        # Shopping frequency
        time_span = (
            max(e.get('timestamp', 0) for e in events) -
            min(e.get('timestamp', 0) for e in events)
        )
        
        if time_span > 0:
            days = time_span / 86400  # Convert to days
            frequency = len(events) / days
            
            patterns.append({
                'pattern_type': 'shopping_frequency',
                'events_per_day': frequency,
                'total_events': len(events),
                'confidence': 0.8,
                'created_at': datetime.utcnow().isoformat()
            })
        
        return {
            'patterns': patterns,
            'summary': f'Analyzed {len(events)} events, found {len(patterns)} patterns'
        }
    
    def calculate_sustainability_score(
        self,
        user_id: str,
        days_back: int = 30
    ) -> float:
        """Calculate user's sustainability engagement score (0-100)"""
        
        events = self._get_user_events(user_id, days_back)
        
        if not events:
            return 50.0  # Neutral score
        
        sustainability_events = 0
        total_events = len(events)
        
        for event in events:
            tags = event.get('tags', [])
            if any(keyword in ' '.join(tags).lower() for keyword in self.sustainability_keywords):
                sustainability_events += 1
        
        # Calculate score (0-100)
        score = (sustainability_events / total_events) * 100 if total_events > 0 else 50.0
        
        # Boost for purchases vs just views
        purchase_events = [e for e in events if e.get('event_type') == 'purchase']
        if purchase_events:
            sustainable_purchases = sum(
                1 for e in purchase_events
                if any(keyword in ' '.join(e.get('tags', [])).lower() 
                       for keyword in self.sustainability_keywords)
            )
            purchase_ratio = sustainable_purchases / len(purchase_events)
            score = score * 0.7 + purchase_ratio * 100 * 0.3
        
        return round(score, 2)
    
    def generate_insights(
        self,
        user_id: str,
        days_back: int = 7
    ) -> List[Dict[str, Any]]:
        """Generate personalized insights for user"""
        
        insights = []
        events = self._get_user_events(user_id, days_back)
        
        if not events:
            return insights
        
        # Sustainability insight
        sustainability_score = self.calculate_sustainability_score(user_id, days_back)
        
        if sustainability_score >= 70:
            insights.append({
                'user_id': user_id,
                'insight_type': 'sustainability_champion',
                'title': '🌱 Sustainability Champion!',
                'description': f"You're making great sustainable choices! Your sustainability score is {sustainability_score:.0f}/100.",
                'priority': 5,
                'actionable': False,
                'created_at': datetime.utcnow().isoformat(),
                'metadata': {'score': sustainability_score}
            })
        elif sustainability_score < 40:
            insights.append({
                'user_id': user_id,
                'insight_type': 'sustainability_opportunity',
                'title': '🌍 Discover Sustainable Options',
                'description': "We have many eco-friendly alternatives that match your style!",
                'priority': 4,
                'actionable': True,
                'created_at': datetime.utcnow().isoformat(),
                'metadata': {'score': sustainability_score}
            })
        
        # Category exploration insight
        patterns = self.analyze_user_patterns(user_id, days_back)
        categories = set()
        
        for pattern in patterns.get('patterns', []):
            if pattern['pattern_type'] == 'category_preference':
                categories.update(pattern['categories'])
        
        if len(categories) < 2:
            insights.append({
                'user_id': user_id,
                'insight_type': 'explore_categories',
                'title': '🔍 Explore New Categories',
                'description': "Discover more sustainable products across different categories!",
                'priority': 3,
                'actionable': True,
                'created_at': datetime.utcnow().isoformat(),
                'metadata': {'current_categories': list(categories)}
            })
        
        return insights
    
    def get_recommendations_input(self, user_id: str) -> Dict[str, Any]:
        """Get user data formatted for recommendation engine"""
        
        patterns = self.analyze_user_patterns(user_id, 30)
        sustainability_score = self.calculate_sustainability_score(user_id, 30)
        
        # Extract preferences
        preferred_categories = []
        preferred_brands = []
        sustainability_interests = []
        
        for pattern in patterns.get('patterns', []):
            if pattern['pattern_type'] == 'category_preference':
                preferred_categories = pattern['categories']
            elif pattern['pattern_type'] == 'brand_preference':
                preferred_brands = pattern['brands']
            elif pattern['pattern_type'] == 'sustainability_focus':
                sustainability_interests = pattern.get('interests', [])
        
        # Calculate average price point
        events = self._get_user_events(user_id, 30)
        prices = []
        
        for event in events:
            metadata = event.get('metadata', {})
            if metadata.get('price'):
                prices.append(float(metadata['price']))
        
        avg_price = sum(prices) / len(prices) if prices else 50
        price_std = (sum((p - avg_price) ** 2 for p in prices) / len(prices)) ** 0.5 if len(prices) > 1 else 30
        
        return {
            'user_id': user_id,
            'sustainability_score': sustainability_score,
            'preferred_categories': preferred_categories,
            'preferred_brands': preferred_brands,
            'sustainability_interests': sustainability_interests,
            'average_price_point': avg_price,
            'price_std': price_std,
            'viewed_products': [e['product_id'] for e in events if e.get('product_id')],
            'viewed_categories': list(set(e['category'] for e in events if e.get('category')))
        }
    
    def _get_user_events(self, user_id: str, days_back: int) -> List[Dict[str, Any]]:
        """Get user events for the last N days"""
        
        if user_id not in user_events:
            return []
        
        cutoff_time = datetime.utcnow() - timedelta(days=days_back)
        cutoff_timestamp = cutoff_time.timestamp()
        
        return [
            e for e in user_events[user_id]
            if e.get('timestamp', 0) >= cutoff_timestamp
        ]
    
    def _extract_sustainability_interests(self, events: List[Dict[str, Any]]) -> List[str]:
        """Extract specific sustainability interests from events"""
        
        interests = set()
        
        for event in events:
            tags = event.get('tags', [])
            for tag in tags:
                tag_lower = tag.lower()
                for keyword in self.sustainability_keywords:
                    if keyword in tag_lower:
                        interests.add(keyword)
        
        return list(interests)
    
    def _analyze_price_sensitivity(self, events: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Analyze price sensitivity from events"""
        
        prices = []
        
        for event in events:
            metadata = event.get('metadata', {})
            if metadata.get('price'):
                try:
                    prices.append(float(metadata['price']))
                except (ValueError, TypeError):
                    pass
        
        if len(prices) < 3:
            return None
        
        avg_price = sum(prices) / len(prices)
        max_price = max(prices)
        
        # Determine sensitivity
        if avg_price < 50:
            sensitivity = 'high'
            confidence = 0.8
        elif avg_price > 150:
            sensitivity = 'low'
            confidence = 0.8
        else:
            sensitivity = 'medium'
            confidence = 0.6
        
        return {
            'pattern_type': 'price_sensitive',
            'sensitivity': sensitivity,
            'average_price': avg_price,
            'max_price': max_price,
            'confidence': confidence,
            'created_at': datetime.utcnow().isoformat()
        }


# Global analyzer instance
analyzer = BehaviorAnalyzer()


@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    logger.info("🚀 Starting User Behavior Tracker Agent...")
    
    # Load existing data if available
    try:
        if os.path.exists(EVENTS_FILE):
            with open(EVENTS_FILE, 'r') as f:
                data = json.load(f)
                for user_id, events in data.items():
                    user_events[user_id] = events
            logger.info(f"Loaded events for {len(user_events)} users")
    except Exception as e:
        logger.warning(f"Could not load cached events: {e}")
    
    try:
        if os.path.exists(PROFILES_FILE):
            with open(PROFILES_FILE, 'r') as f:
                user_profiles.update(json.load(f))
            logger.info(f"Loaded {len(user_profiles)} user profiles")
    except Exception as e:
        logger.warning(f"Could not load cached profiles: {e}")
    
    logger.info("✅ User Behavior Tracker Agent started successfully!")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down User Behavior Tracker Agent...")
    
    # Save events
    try:
        with open(EVENTS_FILE, 'w') as f:
            json.dump(dict(user_events), f, indent=2)
        logger.info("Saved user events")
    except Exception as e:
        logger.error(f"Could not save events: {e}")
    
    # Save profiles
    try:
        with open(PROFILES_FILE, 'w') as f:
            json.dump(user_profiles, f, indent=2)
        logger.info("Saved user profiles")
    except Exception as e:
        logger.error(f"Could not save profiles: {e}")


@app.get("/")
async def root():
    """Root endpoint"""
    total_events = sum(len(events) for events in user_events.values())
    
    return {
        "agent": "User Behavior Tracker",
        "version": "1.0.0",
        "status": "operational",
        "users_tracked": len(user_events),
        "total_events": total_events,
        "endpoints": {
            "track": "POST /track",
            "patterns": "GET /behavior/patterns/{user_id}",
            "score": "GET /behavior/sustainability-score/{user_id}",
            "insights": "GET /behavior/insights/{user_id}",
            "recommendations": "GET /behavior/recommendations/{user_id}",
            "health": "GET /health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    total_events = sum(len(events) for events in user_events.values())
    
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "users_tracked": len(user_events),
        "total_events": total_events
    }


@app.post("/track")
async def track_event(event: TrackingEvent):
    """Track a user event"""
    
    try:
        # Set timestamp if not provided
        if not event.timestamp:
            event.timestamp = datetime.utcnow().timestamp()
        
        # Store event
        event_dict = event.dict()
        user_events[event.user_id].append(event_dict)
        
        logger.info(f"Tracked event: {event.event_type} for user {event.user_id}")
        
        return {
            "status": "success",
            "message": "Event tracked successfully"
        }
        
    except Exception as e:
        logger.error(f"Error tracking event: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/behavior/patterns/{user_id}")
async def get_user_patterns(user_id: str, days_back: int = 30):
    """Get behavior patterns for a user"""
    
    try:
        patterns = analyzer.analyze_user_patterns(user_id, days_back)
        
        return {
            "status": "success",
            "user_id": user_id,
            **patterns
        }
        
    except Exception as e:
        logger.error(f"Error analyzing patterns: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/behavior/sustainability-score/{user_id}")
async def get_sustainability_score(user_id: str, days_back: int = 30):
    """Get user's sustainability score"""
    
    try:
        score = analyzer.calculate_sustainability_score(user_id, days_back)
        
        return {
            "status": "success",
            "user_id": user_id,
            "sustainability_score": score,
            "calculated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error calculating score: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/behavior/insights/{user_id}")
async def get_user_insights(user_id: str, days_back: int = 7):
    """Get personalized insights for a user"""
    
    try:
        insights = analyzer.generate_insights(user_id, days_back)
        
        return {
            "status": "success",
            "user_id": user_id,
            "insights": insights
        }
        
    except Exception as e:
        logger.error(f"Error generating insights: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/behavior/recommendations/{user_id}")
async def get_recommendations_input(user_id: str):
    """Get user data formatted for recommendation engine"""
    
    try:
        data = analyzer.get_recommendations_input(user_id)
        
        return {
            "status": "success",
            **data
        }
        
    except Exception as e:
        logger.error(f"Error getting recommendation data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/users")
async def get_all_users():
    """Get all tracked users"""
    
    users = []
    
    for user_id in user_events.keys():
        score = analyzer.calculate_sustainability_score(user_id, 30)
        event_count = len(user_events[user_id])
        
        users.append({
            'user_id': user_id,
            'event_count': event_count,
            'sustainability_score': score
        })
    
    return {
        "status": "success",
        "count": len(users),
        "users": users
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=USER_BEHAVIOR_PORT)

