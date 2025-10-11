import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import openai
from config import settings
from models import AIPrompt, UserInsight, BehaviorPattern

class AIService:
    def __init__(self):
        if settings.openai_api_key:
            openai.api_key = settings.openai_api_key
        self.client = openai.AsyncOpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None

    async def analyze_user_behavior(self, user_events: List[Dict], user_profile: Optional[Dict] = None) -> List[BehaviorPattern]:
        """Analyze user behavior patterns using AI"""
        if not self.client:
            return self._fallback_behavior_analysis(user_events, user_profile)

        try:
            prompt = self._build_behavior_analysis_prompt(user_events, user_profile)
            
            response = await self.client.chat.completions.create(
                model=settings.ai_model,
                messages=[
                    {"role": "system", "content": "You are an expert in user behavior analysis for sustainable shopping platforms. Analyze user behavior patterns and provide insights."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )

            result = json.loads(response.choices[0].message.content)
            return self._parse_behavior_patterns(result)
        except Exception as e:
            print(f"AI analysis failed: {e}")
            return self._fallback_behavior_analysis(user_events, user_profile)

    async def generate_insights(self, user_id: str, behavior_patterns: List[BehaviorPattern], 
                              recent_events: List[Dict]) -> List[UserInsight]:
        """Generate personalized insights for users"""
        if not self.client:
            return self._fallback_insights(user_id, behavior_patterns, recent_events)

        try:
            prompt = self._build_insights_prompt(user_id, behavior_patterns, recent_events)
            
            response = await self.client.chat.completions.create(
                model=settings.ai_model,
                messages=[
                    {"role": "system", "content": "You are a sustainable shopping advisor. Generate personalized, actionable insights to help users make better sustainable fashion choices."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.5
            )

            result = json.loads(response.choices[0].message.content)
            return self._parse_insights(result, user_id)
        except Exception as e:
            print(f"AI insights generation failed: {e}")
            return self._fallback_insights(user_id, behavior_patterns, recent_events)

    async def generate_analytics_summary(self, analytics_data: Dict) -> Dict[str, Any]:
        """Generate AI-powered analytics summary"""
        if not self.client:
            return self._fallback_analytics_summary(analytics_data)

        try:
            prompt = self._build_analytics_prompt(analytics_data)
            
            response = await self.client.chat.completions.create(
                model=settings.ai_model,
                messages=[
                    {"role": "system", "content": "You are a data analyst for a sustainable shopping platform. Analyze the data and provide actionable insights and recommendations."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.4
            )

            return json.loads(response.choices[0].message.content)
        except Exception as e:
            print(f"AI analytics summary failed: {e}")
            return self._fallback_analytics_summary(analytics_data)

    def _build_behavior_analysis_prompt(self, user_events: List[Dict], user_profile: Optional[Dict] = None) -> str:
        """Build prompt for behavior analysis"""
        events_summary = self._summarize_events(user_events)
        profile_info = f"User Profile: {json.dumps(user_profile, default=str)}" if user_profile else "No profile data"
        
        return f"""
        Analyze the following user behavior data and identify patterns:
        
        {profile_info}
        
        Recent Events Summary:
        {events_summary}
        
        Please identify:
        1. Shopping style patterns (budget-conscious, luxury-focused, sustainability-driven, etc.)
        2. Sustainability engagement level
        3. Price sensitivity patterns
        4. Brand preferences
        5. Category preferences
        6. Search behavior patterns
        
        Return a JSON response with patterns array, each containing:
        - pattern_type: string
        - confidence: float (0-1)
        - data: object with pattern details
        """

    def _build_insights_prompt(self, user_id: str, behavior_patterns: List[BehaviorPattern], 
                              recent_events: List[Dict]) -> str:
        """Build prompt for insights generation"""
        patterns_summary = "\n".join([
            f"- {p.pattern_type}: {p.confidence:.2f} confidence, {json.dumps(p.data)}"
            for p in behavior_patterns
        ])
        
        return f"""
        Based on the user's behavior patterns, generate personalized insights:
        
        User ID: {user_id}
        Behavior Patterns:
        {patterns_summary}
        
        Generate 3-5 actionable insights that help the user:
        1. Make more sustainable fashion choices
        2. Discover relevant brands and products
        3. Optimize their shopping experience
        4. Understand their impact
        
        Return JSON with insights array, each containing:
        - insight_type: string
        - title: string
        - description: string
        - priority: int (1-5)
        - actionable: boolean
        """

    def _build_analytics_prompt(self, analytics_data: Dict) -> str:
        """Build prompt for analytics summary"""
        return f"""
        Analyze this platform analytics data and provide insights:
        
        {json.dumps(analytics_data, default=str, indent=2)}
        
        Provide:
        1. Key trends and patterns
        2. User engagement insights
        3. Sustainability impact metrics
        4. Recommendations for platform improvement
        5. User behavior insights
        
        Return JSON with structured insights and recommendations.
        """

    def _summarize_events(self, events: List[Dict]) -> str:
        """Summarize events for AI analysis"""
        if not events:
            return "No events"
        
        event_types = {}
        pages = {}
        searches = []
        items = {}
        
        for event in events[-50:]:  # Last 50 events
            event_type = event.get('event_type', 'unknown')
            event_types[event_type] = event_types.get(event_type, 0) + 1
            
            if event.get('page'):
                pages[event['page']] = pages.get(event['page'], 0) + 1
            
            if event_type == 'search' and event.get('keywords'):
                searches.extend(event['keywords'])
            
            if event.get('item_id'):
                items[event['item_id']] = items.get(event['item_id'], 0) + 1
        
        return f"""
        Event Types: {event_types}
        Top Pages: {dict(sorted(pages.items(), key=lambda x: x[1], reverse=True)[:5])}
        Recent Searches: {searches[-10:]}
        Viewed Items: {dict(sorted(items.items(), key=lambda x: x[1], reverse=True)[:5])}
        """

    def _parse_behavior_patterns(self, ai_response: Dict) -> List[BehaviorPattern]:
        """Parse AI response into behavior patterns"""
        patterns = []
        for pattern_data in ai_response.get('patterns', []):
            patterns.append(BehaviorPattern(
                user_id="",  # Will be set by caller
                pattern_type=pattern_data.get('pattern_type', 'unknown'),
                confidence=pattern_data.get('confidence', 0.5),
                data=pattern_data.get('data', {}),
                created_at=datetime.now()
            ))
        return patterns

    def _parse_insights(self, ai_response: Dict, user_id: str) -> List[UserInsight]:
        """Parse AI response into user insights"""
        insights = []
        for insight_data in ai_response.get('insights', []):
            insights.append(UserInsight(
                user_id=user_id,
                insight_type=insight_data.get('insight_type', 'general'),
                title=insight_data.get('title', 'Insight'),
                description=insight_data.get('description', ''),
                priority=insight_data.get('priority', 3),
                actionable=insight_data.get('actionable', True),
                metadata=insight_data.get('metadata', {}),
                created_at=datetime.now()
            ))
        return insights

    def _fallback_behavior_analysis(self, user_events: List[Dict], user_profile: Optional[Dict] = None) -> List[BehaviorPattern]:
        """Fallback behavior analysis without AI"""
        patterns = []
        
        # Simple pattern detection
        if user_events:
            # Sustainability focus pattern
            sustainability_events = [e for e in user_events if 'sustainability' in str(e.get('tags', [])).lower()]
            if sustainability_events:
                patterns.append(BehaviorPattern(
                    user_id="",
                    pattern_type="sustainability_focus",
                    confidence=min(len(sustainability_events) / 10, 1.0),
                    data={"sustainability_events": len(sustainability_events)},
                    created_at=datetime.now()
                ))
            
            # Search behavior pattern
            search_events = [e for e in user_events if e.get('event_type') == 'search']
            if search_events:
                patterns.append(BehaviorPattern(
                    user_id="",
                    pattern_type="active_searcher",
                    confidence=min(len(search_events) / 5, 1.0),
                    data={"search_count": len(search_events)},
                    created_at=datetime.now()
                ))
        
        return patterns

    def _fallback_insights(self, user_id: str, behavior_patterns: List[BehaviorPattern], 
                          recent_events: List[Dict]) -> List[UserInsight]:
        """Fallback insights without AI"""
        insights = []
        
        # Basic insights based on patterns
        for pattern in behavior_patterns:
            if pattern.pattern_type == "sustainability_focus":
                insights.append(UserInsight(
                    user_id=user_id,
                    insight_type="recommendation",
                    title="Sustainability Champion",
                    description="You show strong interest in sustainable fashion. Consider exploring our premium sustainable brands section.",
                    priority=4,
                    actionable=True,
                    created_at=datetime.now()
                ))
            elif pattern.pattern_type == "active_searcher":
                insights.append(UserInsight(
                    user_id=user_id,
                    insight_type="suggestion",
                    title="Search Optimization",
                    description="You're an active searcher! Try using our advanced filters to find exactly what you're looking for.",
                    priority=3,
                    actionable=True,
                    created_at=datetime.now()
                ))
        
        return insights

    def _fallback_analytics_summary(self, analytics_data: Dict) -> Dict[str, Any]:
        """Fallback analytics summary without AI"""
        return {
            "user_behavior_insights": [
                "Users are actively engaging with the platform",
                "Search functionality is being utilized effectively",
                "Sustainability features are gaining traction"
            ],
            "recommendations": [
                "Consider adding more sustainable brand partnerships",
                "Optimize search results for better user experience",
                "Implement personalized recommendations based on user behavior"
            ],
            "sustainability_insights": {
                "engagement_level": "moderate",
                "trend": "increasing"
            }
        }

