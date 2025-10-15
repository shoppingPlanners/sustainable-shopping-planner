from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from typing import List, Optional
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter(prefix="/api/items", tags=["items"])

# Direct MongoDB connection
mongo_client = MongoClient(os.getenv("DATABASE_URL", "mongodb://localhost:27017/sustainable-shopping-planner"))
mongo_db = mongo_client.get_default_database()

class ItemResponse(BaseModel):
    id: str
    name: str
    brand: str
    rating: float
    sustainabilityScore: int
    price: str
    image: str
    buyUrl: str
    features: List[str]
    category: str

@router.get("/", response_model=List[ItemResponse])
async def get_items(
    category: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
):
    """
    Get items by flattening products within brands, with optional category filter.
    """
    try:
        # Fetch brands from MongoDB (filtering occurs after flattening products)
        brands_cursor = mongo_db.brands.find({})

        flattened: List[ItemResponse] = []
        for brand_doc in brands_cursor:
            brand_id_str = str(brand_doc.get("_id"))
            brand_domain = brand_doc.get("brand_domain", "")
            products = brand_doc.get("products", []) or []

            for index, product in enumerate(products):
                product_category = product.get("category", "N/A") or "N/A"

                # Apply category filter if provided
                if category and category != "all":
                    if (product_category or "").lower() != category.lower():
                        continue

                # Get price and convert to string
                price_value = product.get("price", 0)
                if isinstance(price_value, (int, float)):
                    price_str = f"${price_value:.2f}"
                else:
                    # Extract numeric value if it's already a string like "$48.00"
                    price_str = str(price_value)
                
                item_response = ItemResponse(
                    id=f"{brand_id_str}:{index}",
                    name=product.get("product_name", ""),
                    brand=brand_domain,
                    rating=product.get("rating", 3.5),  # Use rating from Rating Calculator Agent
                    sustainabilityScore=product.get("sustainability_score", 50),  # Use score from Rating Calculator Agent
                    price=price_str,
                    image=product.get("image", ""),
                    buyUrl=product.get("product_url", ""),
                    features=product.get("available_sizes", []) or [],
                    category=product_category,
                )
                flattened.append(item_response)

        # Apply pagination after flattening
        paginated = flattened[offset: offset + limit]
        return paginated
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch items: {str(e)}")

@router.get("/{item_id}", response_model=ItemResponse)
async def get_item(item_id: str):
    """
    Get a specific product using a composite id: "brandObjectId:index".
    """
    try:
        # Expect composite id like "<brandId>:<productIndex>"
        if ":" not in item_id:
            raise HTTPException(status_code=400, detail="Invalid item id format. Expected 'brandId:index'.")

        brand_id_str, index_str = item_id.split(":", 1)
        try:
            index = int(index_str)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid product index in item id.")

        from bson import ObjectId
        brand_doc = mongo_db.brands.find_one({"_id": ObjectId(brand_id_str)})
        if not brand_doc:
            raise HTTPException(status_code=404, detail="Brand not found")

        products = brand_doc.get("products", []) or []
        if index < 0 or index >= len(products):
            raise HTTPException(status_code=404, detail="Product not found for given index")

        product = products[index]
        product_category = product.get("category", "N/A") or "N/A"

        # Get price and convert to string
        price_value = product.get("price", 0)
        if isinstance(price_value, (int, float)):
            price_str = f"${price_value:.2f}"
        else:
            price_str = str(price_value)

        item_response = ItemResponse(
            id=f"{brand_id_str}:{index}",
            name=product.get("product_name", ""),
            brand=brand_doc.get("brand_domain", ""),
            rating=product.get("rating", 3.5),  # Use rating from Rating Calculator Agent
            sustainabilityScore=product.get("sustainability_score", 50),  # Use score from Rating Calculator Agent
            price=price_str,
            image=product.get("image", ""),
            buyUrl=product.get("product_url", ""),
            features=product.get("available_sizes", []) or [],
            category=product_category,
        )
        return item_response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch item: {str(e)}")
