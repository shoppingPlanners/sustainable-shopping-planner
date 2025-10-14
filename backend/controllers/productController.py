"""
Product Controller for Sustainable Shopping Planner
Handles product-related operations
"""

from fastapi import HTTPException
from typing import List, Optional
from database import Product
from models.product import ProductCreate, ProductResponse
import logging

logger = logging.getLogger(__name__)

class ProductController:
    """Product controller class"""
    
    @staticmethod
    async def get_all_products() -> List[ProductResponse]:
        """Get all products"""
        try:
            products = await Product.find_all().to_list()
            return [ProductResponse.from_product(product) for product in products]
        except Exception as e:
            logger.error(f"Error fetching products: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch products")
    
    @staticmethod
    async def get_product_by_id(product_id: str) -> ProductResponse:
        """Get single product by ID"""
        try:
            product = await Product.get(product_id)
            if not product:
                raise HTTPException(status_code=404, detail="Product not found")
            return ProductResponse.from_product(product)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error fetching product {product_id}: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch product")
    
    @staticmethod
    async def create_product(product_data: ProductCreate) -> ProductResponse:
        """Create new product"""
        try:
            new_product = Product(**product_data.dict())
            await new_product.insert()
            return ProductResponse.from_product(new_product)
        except Exception as e:
            logger.error(f"Error creating product: {e}")
            raise HTTPException(status_code=500, detail="Failed to create product")
    
    @staticmethod
    async def update_product(product_id: str, product_data: ProductCreate) -> ProductResponse:
        """Update existing product"""
        try:
            product = await Product.get(product_id)
            if not product:
                raise HTTPException(status_code=404, detail="Product not found")
            
            for field, value in product_data.dict().items():
                setattr(product, field, value)
            
            await product.save()
            return ProductResponse.from_product(product)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating product: {e}")
            raise HTTPException(status_code=500, detail="Failed to update product")
    
    @staticmethod
    async def delete_product(product_id: str) -> dict:
        """Delete product"""
        try:
            product = await Product.get(product_id)
            if not product:
                raise HTTPException(status_code=404, detail="Product not found")
            
            await product.delete()
            return {"message": "Product deleted successfully"}
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error deleting product: {e}")
            raise HTTPException(status_code=500, detail="Failed to delete product")
    
    @staticmethod
    async def search_products(query: str, limit: int = 10) -> List[ProductResponse]:
        """Search products by name or description"""
        try:
            # Create text index if it doesn't exist
            from database import database
            try:
                await database.products.create_index([("name", "text"), ("description", "text")])
            except:
                pass  # Index might already exist
            
            # Search products
            products = await Product.find({"$text": {"$search": query}}).limit(limit).to_list(limit)
            return [ProductResponse.from_product(product) for product in products]
        except Exception as e:
            logger.error(f"Error searching products: {e}")
            raise HTTPException(status_code=500, detail="Failed to search products")
