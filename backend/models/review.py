"""
Review models for Sustainable Shopping Planner
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from database import Review

class ReviewBase(BaseModel):
    """Base review model"""
    product_id: str = Field(..., description="Product ID")
    user_id: str = Field(..., description="User ID")
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    text: str = Field(..., description="Review text")

class ReviewCreate(ReviewBase):
    """Review creation model"""
    pass

class ReviewUpdate(BaseModel):
    """Review update model"""
    rating: Optional[int] = Field(None, ge=1, le=5)
    text: Optional[str] = None

class ReviewResponse(ReviewBase):
    """Review response model"""
    id: str = Field(..., description="Review ID")
    date: datetime = Field(..., description="Review date")
    created_at: datetime = Field(..., description="Creation timestamp")
    
    class Config:
        from_attributes = True
    
    @classmethod
    def from_review(cls, review: Review) -> "ReviewResponse":
        """Create response from Review document"""
        return cls(
            id=str(review.id),
            product_id=review.product_id,
            user_id=review.user_id,
            rating=review.rating,
            text=review.text,
            date=review.date,
            created_at=review.created_at
        )
