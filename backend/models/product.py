"""
Product models for Sustainable Shopping Planner
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from database import Product

class ProductBase(BaseModel):
    """Base product model"""
    name: str = Field(..., description="Product name")
    brand: str = Field(..., description="Brand name")
    category: str = Field(..., description="Product category")
    price: float = Field(..., description="Product price")
    description: str = Field(..., description="Product description")
    sustainability_features: List[str] = Field(default=[], description="Sustainability features")
    image: str = Field(default="/placeholder.jpg", description="Product image URL")

class ProductCreate(ProductBase):
    """Product creation model"""
    pass

class ProductUpdate(BaseModel):
    """Product update model"""
    name: Optional[str] = None
    brand: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    sustainability_features: Optional[List[str]] = None
    image: Optional[str] = None

class ProductResponse(ProductBase):
    """Product response model"""
    id: str = Field(..., description="Product ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    class Config:
        from_attributes = True
    
    @classmethod
    def from_product(cls, product: Product) -> "ProductResponse":
        """Create response from Product document"""
        return cls(
            id=str(product.id),
            name=product.name,
            brand=product.brand,
            category=product.category,
            price=product.price,
            description=product.description,
            sustainability_features=product.sustainability_features,
            image=product.image,
            created_at=product.created_at,
            updated_at=product.updated_at
        )
