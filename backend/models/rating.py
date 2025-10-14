"""
Rating models for Sustainable Shopping Planner
"""

from pydantic import BaseModel, Field
from typing import Dict, Any
from datetime import datetime
from database import AIRating

class AIRatingBase(BaseModel):
    """Base AI rating model"""
    product_id: str = Field(..., description="Product ID")
    ai_rating: float = Field(..., ge=1.0, le=5.0, description="AI calculated rating")
    sentiment_score: float = Field(..., ge=-1.0, le=1.0, description="Sentiment score")
    sustainability_score: float = Field(..., ge=0.0, le=1.0, description="Sustainability score")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence level")
    breakdown: Dict[str, Any] = Field(..., description="Detailed breakdown")

class AIRatingCreate(AIRatingBase):
    """AI rating creation model"""
    pass

class AIRatingUpdate(BaseModel):
    """AI rating update model"""
    ai_rating: Optional[float] = Field(None, ge=1.0, le=5.0)
    sentiment_score: Optional[float] = Field(None, ge=-1.0, le=1.0)
    sustainability_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    breakdown: Optional[Dict[str, Any]] = None

class AIRatingResponse(AIRatingBase):
    """AI rating response model"""
    id: str = Field(..., description="Rating ID")
    timestamp: datetime = Field(..., description="Rating timestamp")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        from_attributes = True
    
    @classmethod
    def from_rating(cls, rating: AIRating) -> "AIRatingResponse":
        """Create response from AIRating document"""
        return cls(
            id=str(rating.id),
            product_id=rating.product_id,
            ai_rating=rating.ai_rating,
            sentiment_score=rating.sentiment_score,
            sustainability_score=rating.sustainability_score,
            confidence=rating.confidence,
            breakdown=rating.breakdown,
            timestamp=rating.timestamp,
            created_at=rating.created_at,
            updated_at=rating.updated_at
        )
