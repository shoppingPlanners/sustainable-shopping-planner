"""
Review routes for Sustainable Shopping Planner
"""

from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from typing import List, Optional
from controllers.reviewController import ReviewController
from models.review import ReviewCreate, ReviewResponse, ReviewUpdate

router = APIRouter(prefix="/api/reviews", tags=["reviews"])

@router.get("/", response_model=List[ReviewResponse])
async def get_reviews(
    product_id: Optional[str] = Query(None, description="Filter by product ID"),
    user_id: Optional[str] = Query(None, description="Filter by user ID")
):
    """Get reviews with optional filtering"""
    return await ReviewController.get_all_reviews(product_id, user_id)

@router.get("/{review_id}", response_model=ReviewResponse)
async def get_review(review_id: str):
    """Get single review by ID"""
    return await ReviewController.get_review_by_id(review_id)

@router.post("/", response_model=ReviewResponse)
async def create_review(review: ReviewCreate, background_tasks: BackgroundTasks):
    """Create new review and trigger AI rating calculation"""
    return await ReviewController.create_review(review, background_tasks)

@router.get("/product/{product_id}", response_model=List[ReviewResponse])
async def get_product_reviews(product_id: str):
    """Get reviews for specific product"""
    return await ReviewController.get_product_reviews(product_id)

@router.put("/{review_id}", response_model=ReviewResponse)
async def update_review(review_id: str, review: ReviewUpdate):
    """Update existing review"""
    return await ReviewController.update_review(review_id, review)

@router.delete("/{review_id}")
async def delete_review(review_id: str):
    """Delete review"""
    return await ReviewController.delete_review(review_id)
