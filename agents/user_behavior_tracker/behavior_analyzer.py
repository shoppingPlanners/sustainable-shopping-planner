import asyncio
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import motor.motor_asyncio
from models import BehaviorPattern, UserInsight, TrackingEvent, EventType
from ai_service import AIService
from config import settings

class BehaviorAnalyzer:
    def __init__(self, db: motor.motor_asyncio.AsyncIOMotorDatabase):
        self.db = db
        self.events_col = db["events"]
        self.profiles_col = db["profiles"]
        self.patterns_col = db["behavior_patterns"]
        self.insights_col = db["user_insights"]
        self.ai_service = AIService()

    async def analyze_user_behavior(self, user_id: str, days_back: int = 30) -> List[BehaviorPattern]:
        """Analyze user behavior and return patterns"""
        # Get user events from the last N days
        since = datetime.now() - timedelta(days=days_back)
        events = await self._get_user_events(user_id, since)
        
        if not events:
            return []

        # Get user profile
        user_profile = await self._get_user_profile(user_id)
        
        # Use AI to analyze behavior
        patterns = await self.ai_service.analyze_user_behavior(events, user_profile)
        
        # Set user_id for all patterns
        for pattern in patterns:
            pattern.user_id = user_id
        
        # Store patterns in database
        await self._store_patterns(patterns)
        
        return patterns

    async def generate_user_insights(self, user_id: str, days_back: int = 7) -> List[UserInsight]:
        """Generate personalized insights for a user"""
        # Get recent behavior patterns
        patterns = await self._get_recent_patterns(user_id, days_back)
        
        # Get recent events
        since = datetime.now() - timedelta(days=days_back)
        recent_events = await self._get_user_events(user_id, since)
        
        # Generate insights using AI
        insights = await self.ai_service.generate_insights(user_id, patterns, recent_events)
        
        # Store insights in database
        await self._store_insights(insights)
        
        return insights

    async def calculate_sustainability_score(self, user_id: str, days_back: int = 30) -> float:
        """Calculate user's sustainability engagement score"""
        since = datetime.now() - timedelta(days=days_back)
        events = await self._get_user_events(user_id, since)
        
        if not events:
            return 0.0
        
        sustainability_events = 0
        total_events = len(events)
        
        for event in events:
            # Check for sustainability-related actions
            if self._is_sustainability_event(event):
                sustainability_events += 1
        
        # Calculate score (0-100)
        score = (sustainability_events / total_events) * 100 if total_events > 0 else 0
        
        # Update user profile with sustainability score
        await self.profiles_col.update_one(
            {"_id": user_id},
            {"$set": {"sustainability_score": score, "updated_at": datetime.now()}},
            upsert=True
        )
        
        return score

    async def detect_behavior_anomalies(self, user_id: str) -> List[Dict[str, Any]]:
        """Detect unusual behavior patterns"""
        # Get user's historical patterns
        patterns = await self._get_recent_patterns(user_id, 90)  # 3 months
        
        if len(patterns) < 5:  # Need enough data
            return []
        
        anomalies = []
        
        # Check for sudden changes in behavior
        recent_patterns = [p for p in patterns if p.created_at > datetime.now() - timedelta(days=7)]
        historical_patterns = [p for p in patterns if p.created_at <= datetime.now() - timedelta(days=7)]
        
        if recent_patterns and historical_patterns:
            # Compare pattern types
            recent_types = set(p.pattern_type for p in recent_patterns)
            historical_types = set(p.pattern_type for p in historical_patterns)
            
            new_patterns = recent_types - historical_types
            if new_patterns:
                anomalies.append({
                    "type": "new_behavior_pattern",
                    "description": f"New behavior patterns detected: {', '.join(new_patterns)}",
                    "severity": "low",
                    "timestamp": datetime.now()
                })
        
        return anomalies

    async def get_user_recommendations(self, user_id: str) -> List[Dict[str, Any]]:
        """Get personalized recommendations based on behavior analysis"""
        patterns = await self._get_recent_patterns(user_id, 30)
        insights = await self._get_recent_insights(user_id, 7)
        
        recommendations = []
        
        # Generate recommendations based on patterns
        for pattern in patterns:
            if pattern.pattern_type == "sustainability_focus" and pattern.confidence > 0.7:
                recommendations.append({
                    "type": "brand_recommendation",
                    "title": "Premium Sustainable Brands",
                    "description": "Based on your sustainability focus, try these premium sustainable brands",
                    "priority": "high",
                    "action": "explore_brands",
                    "metadata": {"brands": ["Patagonia", "Reformation", "Eileen Fisher"]}
                })
            
            elif pattern.pattern_type == "price_sensitive" and pattern.confidence > 0.6:
                recommendations.append({
                    "type": "price_alert",
                    "title": "Budget-Friendly Options",
                    "description": "We found some great sustainable options within your budget range",
                    "priority": "medium",
                    "action": "view_deals",
                    "metadata": {"price_range": "under_100"}
                })
        
        # Add insights-based recommendations
        for insight in insights:
            if insight.actionable and insight.priority >= 4:
                recommendations.append({
                    "type": "insight_recommendation",
                    "title": insight.title,
                    "description": insight.description,
                    "priority": "high" if insight.priority >= 4 else "medium",
                    "action": "follow_insight",
                    "metadata": insight.metadata
                })
        
        return recommendations

    async def _get_user_events(self, user_id: str, since: datetime) -> List[Dict]:
        """Get user events since a specific date"""
        cursor = self.events_col.find({
            "user_id": user_id,
            "timestamp": {"$gte": since.timestamp()}
        }).sort("timestamp", -1)
        
        events = []
        async for event in cursor:
            events.append(event)
        
        return events

    async def _get_user_profile(self, user_id: str) -> Optional[Dict]:
        """Get user profile data"""
        return await self.profiles_col.find_one({"_id": user_id})

    async def _get_recent_patterns(self, user_id: str, days_back: int) -> List[BehaviorPattern]:
        """Get recent behavior patterns for a user"""
        since = datetime.now() - timedelta(days=days_back)
        cursor = self.patterns_col.find({
            "user_id": user_id,
            "created_at": {"$gte": since}
        }).sort("created_at", -1)
        
        patterns = []
        async for pattern_doc in cursor:
            patterns.append(BehaviorPattern(**pattern_doc))
        
        return patterns

    async def _get_recent_insights(self, user_id: str, days_back: int) -> List[UserInsight]:
        """Get recent insights for a user"""
        since = datetime.now() - timedelta(days=days_back)
        cursor = self.insights_col.find({
            "user_id": user_id,
            "created_at": {"$gte": since}
        }).sort("created_at", -1)
        
        insights = []
        async for insight_doc in cursor:
            insights.append(UserInsight(**insight_doc))
        
        return insights

    async def _store_patterns(self, patterns: List[BehaviorPattern]):
        """Store behavior patterns in database"""
        if not patterns:
            return
        
        pattern_docs = []
        for pattern in patterns:
            pattern_doc = pattern.dict()
            pattern_doc["_id"] = f"{pattern.user_id}_{pattern.pattern_type}_{int(pattern.created_at.timestamp())}"
            pattern_docs.append(pattern_doc)
        
        if pattern_docs:
            await self.patterns_col.insert_many(pattern_docs, ordered=False)

    async def _store_insights(self, insights: List[UserInsight]):
        """Store user insights in database"""
        if not insights:
            return
        
        insight_docs = []
        for insight in insights:
            insight_doc = insight.dict()
            insight_doc["_id"] = f"{insight.user_id}_{insight.insight_type}_{int(insight.created_at.timestamp())}"
            insight_docs.append(insight_doc)
        
        if insight_docs:
            await self.insights_col.insert_many(insight_docs, ordered=False)

    def _is_sustainability_event(self, event: Dict) -> bool:
        """Check if an event is sustainability-related"""
        # Check tags for sustainability keywords
        tags = event.get('tags', [])
        sustainability_keywords = [
            'organic', 'sustainable', 'eco-friendly', 'recycled', 'fair trade',
            'carbon neutral', 'biodegradable', 'ethical', 'green'
        ]
        
        for tag in tags:
            if any(keyword in tag.lower() for keyword in sustainability_keywords):
                return True
        
        # Check for sustainability-related searches
        if event.get('event_type') == 'search':
            keywords = event.get('keywords', [])
            for keyword in keywords:
                if any(sus_keyword in keyword.lower() for sus_keyword in sustainability_keywords):
                    return True
        
        return False





