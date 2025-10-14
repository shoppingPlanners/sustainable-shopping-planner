"""
Product routes for Sustainable Shopping Planner
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from controllers.productController import ProductController
from models.product import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter(prefix="/api/products", tags=["products"])

@router.get("/", response_model=List[ProductResponse])
async def get_products():
    """Get all products"""
    return await ProductController.get_all_products()

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str):
    """Get single product by ID"""
    return await ProductController.get_product_by_id(product_id)

@router.post("/", response_model=ProductResponse)
async def create_product(product: ProductCreate):
    """Create new product"""
    return await ProductController.create_product(product)

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: str, product: ProductUpdate):
    """Update existing product"""
    return await ProductController.update_product(product_id, product)

@router.delete("/{product_id}")
async def delete_product(product_id: str):
    """Delete product"""
    return await ProductController.delete_product(product_id)

@router.get("/search/", response_model=List[ProductResponse])
async def search_products(
    q: str = Query(..., description="Search query"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of results")
):
    """Search products by name or description"""
    return await ProductController.search_products(q, limit)
