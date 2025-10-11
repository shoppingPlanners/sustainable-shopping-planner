import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorDatabase
from models import AnalyticsSummary, TrackingEvent, EventType
from ai_service import AIService
from config import settings

class AnalyticsService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.events_col = db["events"]
        self.profiles_col = db["profiles"]
        self.summaries_col = db["usage_summaries"]
        self.ai_service = AIService()

    async def generate_summary(self, hours_back: int = 24) -> AnalyticsSummary:
        """Generate comprehensive analytics summary"""
        now = datetime.now()
        since = now - timedelta(hours=hours_back)
        
        # Get basic metrics
        total_events = await self.events_col.count_documents({"timestamp": {"$gte": since.timestamp()}})
        unique_users = len(await self.events_col.distinct("user_id", {"timestamp": {"$gte": since.timestamp()}}))
        unique_sessions = len(await self.events_col.distinct("session_id", {"timestamp": {"$gte": since.timestamp()}}))
        
        # Get events by type
        by_type = {}
        async for row in self.events_col.aggregate([
            {"$match": {"timestamp": {"$gte": since.timestamp()}}},
            {"$group": {"_id": "$event_type", "count": {"$sum": 1}}},
        ]):
            by_type[row["_id"]] = row["count"]
        
        # Get top pages
        top_pages = await self._get_top_pages(since)
        
        # Get top searches
        top_searches = await self._get_top_searches(since)
        
        # Get top items
        top_items = await self._get_top_items(since)
        
        # Get sustainability insights
        sustainability_insights = await self._get_sustainability_insights(since)
        
        # Generate AI-powered insights
        analytics_data = {
            "total_events": total_events,
            "unique_users": unique_users,
            "by_type": by_type,
            "top_pages": top_pages,
            "top_searches": top_searches,
            "top_items": top_items,
            "sustainability_insights": sustainability_insights
        }
        
        ai_insights = await self.ai_service.generate_analytics_summary(analytics_data)
        
        summary = AnalyticsSummary(
            created_at=now.timestamp(),
            window_start=since.timestamp(),
            total_events=total_events,
            unique_users=unique_users,
            unique_sessions=unique_sessions,
            by_type=by_type,
            top_pages=top_pages,
            top_searches=top_searches,
            top_items=top_items,
            sustainability_insights=sustainability_insights,
            user_behavior_insights=ai_insights.get("user_behavior_insights", []),
            recommendations=ai_insights.get("recommendations", [])
        )
        
        # Store summary
        await self.summaries_col.insert_one(summary.dict())
        
        return summary

    async def get_user_analytics(self, user_id: str, days_back: int = 30) -> Dict[str, Any]:
        """Get detailed analytics for a specific user"""
        since = datetime.now() - timedelta(days=days_back)
        
        # Get user events
        events = []
        async for event in self.events_col.find({
            "user_id": user_id,
            "timestamp": {"$gte": since.timestamp()}
        }).sort("timestamp", -1):
            events.append(event)
        
        if not events:
            return {"error": "No data found for user"}
        
        # Calculate metrics
        total_events = len(events)
        event_types = {}
        pages_visited = {}
        searches_made = []
        items_viewed = {}
        sustainability_score = 0
        
        for event in events:
            event_type = event.get('event_type', 'unknown')
            event_types[event_type] = event_types.get(event_type, 0) + 1
            
            if event.get('page'):
                pages_visited[event['page']] = pages_visited.get(event['page'], 0) + 1
            
            if event_type == 'search' and event.get('keywords'):
                searches_made.extend(event['keywords'])
            
            if event.get('item_id'):
                items_viewed[event['item_id']] = items_viewed.get(event['item_id'], 0) + 1
            
            # Calculate sustainability engagement
            if self._is_sustainability_event(event):
                sustainability_score += 1
        
        sustainability_score = (sustainability_score / total_events) * 100 if total_events > 0 else 0
        
        return {
            "user_id": user_id,
            "period_days": days_back,
            "total_events": total_events,
            "event_types": event_types,
            "top_pages": dict(sorted(pages_visited.items(), key=lambda x: x[1], reverse=True)[:10]),
            "recent_searches": searches_made[-20:],
            "top_items": dict(sorted(items_viewed.items(), key=lambda x: x[1], reverse=True)[:10]),
            "sustainability_score": sustainability_score,
            "engagement_level": self._calculate_engagement_level(total_events, days_back),
            "last_activity": events[0].get('timestamp') if events else None
        }

    async def get_platform_metrics(self, days_back: int = 7) -> Dict[str, Any]:
        """Get platform-wide metrics"""
        since = datetime.now() - timedelta(days=days_back)
        
        # Daily active users
        daily_users = []
        for i in range(days_back):
            day_start = since + timedelta(days=i)
            day_end = day_start + timedelta(days=1)
            
            count = len(await self.events_col.distinct("user_id", {
                "timestamp": {"$gte": day_start.timestamp(), "$lt": day_end.timestamp()}
            }))
            daily_users.append({
                "date": day_start.strftime("%Y-%m-%d"),
                "users": count
            })
        
        # Event trends
        event_trends = {}
        for event_type in EventType:
            trend = []
            for i in range(days_back):
                day_start = since + timedelta(days=i)
                day_end = day_start + timedelta(days=1)
                
                count = await self.events_col.count_documents({
                    "event_type": event_type.value,
                    "timestamp": {"$gte": day_start.timestamp(), "$lt": day_end.timestamp()}
                })
                trend.append({
                    "date": day_start.strftime("%Y-%m-%d"),
                    "count": count
                })
            event_trends[event_type.value] = trend
        
        # Sustainability engagement
        sustainability_events = await self.events_col.count_documents({
            "timestamp": {"$gte": since.timestamp()},
            "tags": {"$regex": "sustainable|organic|eco|recycled", "$options": "i"}
        })
        
        total_events = await self.events_col.count_documents({"timestamp": {"$gte": since.timestamp()}})
        sustainability_rate = (sustainability_events / total_events * 100) if total_events > 0 else 0
        
        return {
            "period_days": days_back,
            "daily_active_users": daily_users,
            "event_trends": event_trends,
            "sustainability_engagement_rate": sustainability_rate,
            "total_events": total_events,
            "unique_users": len(await self.events_col.distinct("user_id", {"timestamp": {"$gte": since.timestamp()}}))
        }

    async def _get_top_pages(self, since: datetime) -> List[Dict[str, Any]]:
        """Get top pages by view count"""
        pipeline = [
            {"$match": {"event_type": "page_view", "timestamp": {"$gte": since.timestamp()}}},
            {"$group": {"_id": "$page", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]
        
        pages = []
        async for row in self.events_col.aggregate(pipeline):
            pages.append({"page": row["_id"], "views": row["count"]})
        
        return pages

    async def _get_top_searches(self, since: datetime) -> List[Dict[str, Any]]:
        """Get top search terms"""
        pipeline = [
            {"$match": {"event_type": "search", "timestamp": {"$gte": since.timestamp()}}},
            {"$unwind": "$keywords"},
            {"$group": {"_id": "$keywords", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]
        
        searches = []
        async for row in self.events_col.aggregate(pipeline):
            searches.append({"keyword": row["_id"], "searches": row["count"]})
        
        return searches

    async def _get_top_items(self, since: datetime) -> List[Dict[str, Any]]:
        """Get top viewed items"""
        pipeline = [
            {"$match": {"event_type": "view_item", "timestamp": {"$gte": since.timestamp()}}},
            {"$group": {"_id": "$item_id", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]
        
        items = []
        async for row in self.events_col.aggregate(pipeline):
            items.append({"item_id": row["_id"], "views": row["count"]})
        
        return items

    async def _get_sustainability_insights(self, since: datetime) -> Dict[str, Any]:
        """Get sustainability-related insights"""
        # Count sustainability-related events
        sustainability_events = await self.events_col.count_documents({
            "timestamp": {"$gte": since.timestamp()},
            "$or": [
                {"tags": {"$regex": "sustainable|organic|eco|recycled", "$options": "i"}},
                {"keywords": {"$regex": "sustainable|organic|eco|recycled", "$options": "i"}}
            ]
        })
        
        total_events = await self.events_col.count_documents({"timestamp": {"$gte": since.timestamp()}})
        
        # Get top sustainable brands
        sustainable_brands = []
        async for row in self.events_col.aggregate([
            {"$match": {
                "timestamp": {"$gte": since.timestamp()},
                "tags": {"$regex": "sustainable|organic|eco|recycled", "$options": "i"}
            }},
            {"$group": {"_id": "$brand_id", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 5}
        ]):
            sustainable_brands.append({"brand_id": row["_id"], "engagement": row["count"]})
        
        return {
            "sustainability_events": sustainability_events,
            "total_events": total_events,
            "sustainability_rate": (sustainability_events / total_events * 100) if total_events > 0 else 0,
            "top_sustainable_brands": sustainable_brands
        }

    def _is_sustainability_event(self, event: Dict) -> bool:
        """Check if an event is sustainability-related"""
        tags = event.get('tags', [])
        keywords = event.get('keywords', [])
        
        sustainability_keywords = [
            'sustainable', 'organic', 'eco', 'recycled', 'fair trade',
            'carbon neutral', 'biodegradable', 'ethical', 'green'
        ]
        
        for tag in tags:
            if any(keyword in tag.lower() for keyword in sustainability_keywords):
                return True
        
        for keyword in keywords:
            if any(sus_keyword in keyword.lower() for sus_keyword in sustainability_keywords):
                return True
        
        return False

    def _calculate_engagement_level(self, total_events: int, days: int) -> str:
        """Calculate user engagement level"""
        events_per_day = total_events / days if days > 0 else 0
        
        if events_per_day >= 10:
            return "high"
        elif events_per_day >= 5:
            return "medium"
        elif events_per_day >= 1:
            return "low"
        else:
            return "minimal"


