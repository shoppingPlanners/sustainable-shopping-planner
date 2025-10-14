"""
Rating routes for Sustainable Shopping Planner
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from controllers.ratingController import RatingController
from models.rating import AIRatingCreate, AIRatingResponse, AIRatingUpdate

router = APIRouter(prefix="/api/ratings", tags=["ratings"])

@router.get("/", response_model=List[AIRatingResponse])
async def get_ratings(
    product_id: Optional[str] = Query(None, description="Filter by product ID")
):
    """Get AI ratings with optional product filtering"""
    return await RatingController.get_all_ratings(product_id)

@router.get("/{rating_id}", response_model=AIRatingResponse)
async def get_rating(rating_id: str):
    """Get single rating by ID"""
    return await RatingController.get_rating_by_id(rating_id)

@router.get("/product/{product_id}", response_model=AIRatingResponse)
async def get_product_rating(product_id: str):
    """Get AI rating for specific product"""
    return await RatingController.get_product_rating(product_id)

@router.post("/", response_model=AIRatingResponse)
async def create_rating(rating: AIRatingCreate):
    """Save AI rating (called by AI agent)"""
    return await RatingController.create_rating(rating)

@router.put("/{rating_id}", response_model=AIRatingResponse)
async def update_rating(rating_id: str, rating: AIRatingUpdate):
    """Update existing rating"""
    return await RatingController.update_rating(rating_id, rating)

@router.delete("/{rating_id}")
async def delete_rating(rating_id: str):
    """Delete rating"""
    return await RatingController.delete_rating(rating_id)
