"""
Review Controller for Sustainable Shopping Planner
Handles review-related operations
"""

from fastapi import HTTPException, BackgroundTasks
from typing import List, Optional
from database import Review
from models.review import ReviewCreate, ReviewResponse
from utils.ai_trigger import trigger_ai_rating_calculation
import logging

logger = logging.getLogger(__name__)

class ReviewController:
    """Review controller class"""
    
    @staticmethod
    async def get_all_reviews(product_id: Optional[str] = None, user_id: Optional[str] = None) -> List[ReviewResponse]:
        """Get reviews with optional filtering"""
        try:
            query = {}
            if product_id:
                query["product_id"] = product_id
            if user_id:
                query["user_id"] = user_id
            
            reviews = await Review.find(query).to_list()
            return [ReviewResponse.from_review(review) for review in reviews]
        except Exception as e:
            logger.error(f"Error fetching reviews: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch reviews")
    
    @staticmethod
    async def get_review_by_id(review_id: str) -> ReviewResponse:
        """Get single review by ID"""
        try:
            review = await Review.get(review_id)
            if not review:
                raise HTTPException(status_code=404, detail="Review not found")
            return ReviewResponse.from_review(review)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error fetching review {review_id}: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch review")
    
    @staticmethod
    async def create_review(review_data: ReviewCreate, background_tasks: BackgroundTasks) -> ReviewResponse:
        """Create new review and trigger AI rating calculation"""
        try:
            # Validate rating
            if review_data.rating < 1 or review_data.rating > 5:
                raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
            
            new_review = Review(**review_data.dict())
            await new_review.insert()
            
            # Trigger AI rating calculation in background
            background_tasks.add_task(trigger_ai_rating_calculation, review_data.product_id)
            
            logger.info(f"📝 Review created for product {review_data.product_id}, AI calculation triggered")
            
            return ReviewResponse.from_review(new_review)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error creating review: {e}")
            raise HTTPException(status_code=500, detail="Failed to create review")
    
    @staticmethod
    async def get_product_reviews(product_id: str) -> List[ReviewResponse]:
        """Get reviews for specific product"""
        try:
            reviews = await Review.find({"product_id": product_id}).to_list()
            return [ReviewResponse.from_review(review) for review in reviews]
        except Exception as e:
            logger.error(f"Error fetching product reviews: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch product reviews")
    
    @staticmethod
    async def update_review(review_id: str, review_data: ReviewCreate) -> ReviewResponse:
        """Update existing review"""
        try:
            review = await Review.get(review_id)
            if not review:
                raise HTTPException(status_code=404, detail="Review not found")
            
            for field, value in review_data.dict().items():
                setattr(review, field, value)
            
            await review.save()
            return ReviewResponse.from_review(review)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating review: {e}")
            raise HTTPException(status_code=500, detail="Failed to update review")
    
    @staticmethod
    async def delete_review(review_id: str) -> dict:
        """Delete review"""
        try:
            review = await Review.get(review_id)
            if not review:
                raise HTTPException(status_code=404, detail="Review not found")
            
            await review.delete()
            return {"message": "Review deleted successfully"}
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error deleting review: {e}")
            raise HTTPException(status_code=500, detail="Failed to delete review")
