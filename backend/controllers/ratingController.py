"""
Rating Controller for Sustainable Shopping Planner
Handles AI rating-related operations
"""

from fastapi import HTTPException
from typing import List, Optional
from database import AIRating
from models.rating import AIRatingCreate, AIRatingResponse
import logging

logger = logging.getLogger(__name__)

class RatingController:
    """Rating controller class"""
    
    @staticmethod
    async def get_all_ratings(product_id: Optional[str] = None) -> List[AIRatingResponse]:
        """Get AI ratings with optional product filtering"""
        try:
            query = {}
            if product_id:
                query["product_id"] = product_id
            
            ratings = await AIRating.find(query).to_list()
            return [AIRatingResponse.from_rating(rating) for rating in ratings]
        except Exception as e:
            logger.error(f"Error fetching ratings: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch ratings")
    
    @staticmethod
    async def get_rating_by_id(rating_id: str) -> AIRatingResponse:
        """Get single rating by ID"""
        try:
            rating = await AIRating.get(rating_id)
            if not rating:
                raise HTTPException(status_code=404, detail="Rating not found")
            return AIRatingResponse.from_rating(rating)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error fetching rating {rating_id}: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch rating")
    
    @staticmethod
    async def get_product_rating(product_id: str) -> AIRatingResponse:
        """Get AI rating for specific product"""
        try:
            rating = await AIRating.find_one({"product_id": product_id})
            if not rating:
                raise HTTPException(status_code=404, detail="No AI rating found for this product")
            return AIRatingResponse.from_rating(rating)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error fetching product rating: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch product rating")
    
    @staticmethod
    async def create_rating(rating_data: AIRatingCreate) -> AIRatingResponse:
        """Save AI rating (called by AI agent)"""
        try:
            # Check if rating already exists for this product
            existing_rating = await AIRating.find_one({"product_id": rating_data.product_id})
            
            if existing_rating:
                # Update existing rating
                for field, value in rating_data.dict().items():
                    setattr(existing_rating, field, value)
                existing_rating.updated_at = datetime.utcnow()
                await existing_rating.save()
                rating_obj = existing_rating
            else:
                # Create new rating
                rating_obj = AIRating(**rating_data.dict())
                await rating_obj.insert()
            
            logger.info(f"💾 AI rating saved for product {rating_data.product_id}: {rating_data.ai_rating}/5.0")
            
            return AIRatingResponse.from_rating(rating_obj)
        except Exception as e:
            logger.error(f"Error saving rating: {e}")
            raise HTTPException(status_code=500, detail="Failed to save rating")
    
    @staticmethod
    async def update_rating(rating_id: str, rating_data: AIRatingCreate) -> AIRatingResponse:
        """Update existing rating"""
        try:
            rating = await AIRating.get(rating_id)
            if not rating:
                raise HTTPException(status_code=404, detail="Rating not found")
            
            for field, value in rating_data.dict().items():
                setattr(rating, field, value)
            rating.updated_at = datetime.utcnow()
            await rating.save()
            
            return AIRatingResponse.from_rating(rating)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating rating: {e}")
            raise HTTPException(status_code=500, detail="Failed to update rating")
    
    @staticmethod
    async def delete_rating(rating_id: str) -> dict:
        """Delete rating"""
        try:
            rating = await AIRating.get(rating_id)
            if not rating:
                raise HTTPException(status_code=404, detail="Rating not found")
            
            await rating.delete()
            return {"message": "Rating deleted successfully"}
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error deleting rating: {e}")
            raise HTTPException(status_code=500, detail="Failed to delete rating")
