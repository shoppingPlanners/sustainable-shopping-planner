from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class EventType(str, Enum):
    PAGE_VIEW = "page_view"
    SEARCH = "search"
    VIEW_ITEM = "view_item"
    CLICK = "click"
    FILTER_SELECT = "filter_select"
    PURCHASE = "purchase"
    SESSION_START = "session_start"
    SESSION_END = "session_end"
    CONSENT_GIVEN = "consent_given"
    CONSENT_DECLINED = "consent_declined"

class TrackingEvent(BaseModel):
    event_type: EventType
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    item_id: Optional[str] = None
    brand_id: Optional[str] = None
    page: Optional[str] = None
    keywords: Optional[List[str]] = None
    element: Optional[str] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None
    timestamp: Optional[float] = None

class UserProfile(BaseModel):
    user_id: str
    age: Optional[int] = Field(None, ge=0, le=120)
    gender: Optional[str] = None
    location: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = None
    sustainability_score: Optional[float] = Field(None, ge=0, le=100)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class BehaviorPattern(BaseModel):
    user_id: str
    pattern_type: str  # e.g., "shopping_style", "sustainability_focus", "price_sensitivity"
    confidence: float = Field(ge=0, le=1)
    data: Dict[str, Any]
    created_at: datetime

class UserInsight(BaseModel):
    user_id: str
    insight_type: str  # e.g., "recommendation", "warning", "suggestion"
    title: str
    description: str
    priority: int = Field(ge=1, le=5)  # 1=low, 5=high
    actionable: bool = True
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime

class AnalyticsSummary(BaseModel):
    created_at: float
    window_start: float
    total_events: int
    unique_users: int
    unique_sessions: int
    by_type: Dict[str, int]
    top_pages: List[Dict[str, Union[str, int]]]
    top_searches: List[Dict[str, Union[str, int]]]
    top_items: List[Dict[str, Union[str, int]]]
    sustainability_insights: Dict[str, Any]
    user_behavior_insights: List[str]
    recommendations: List[str]

class AIPrompt(BaseModel):
    prompt: str
    context: Dict[str, Any]
    model: str = "gpt-3.5-turbo"
    max_tokens: int = 500
    temperature: float = 0.7

