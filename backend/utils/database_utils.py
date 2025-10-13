"""
Database utility functions
"""

from database import database
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

async def get_database_stats() -> Dict[str, Any]:
    """Get database statistics"""
    try:
        stats = {
            "collections": {},
            "total_documents": 0
        }
        
        # Get collection names
        collections = await database.list_collection_names()
        
        for collection_name in collections:
            collection = database[collection_name]
            count = await collection.count_documents({})
            stats["collections"][collection_name] = count
            stats["total_documents"] += count
        
        return stats
    except Exception as e:
        logger.error(f"Error getting database stats: {e}")
        return {"error": str(e)}

async def create_indexes():
    """Create database indexes for optimal performance"""
    try:
        # Products indexes
        await database.products.create_index("name")
        await database.products.create_index("brand")
        await database.products.create_index("category")
        await database.products.create_index("price")
        await database.products.create_index([("name", "text"), ("description", "text")])
        
        # Reviews indexes
        await database.reviews.create_index("product_id")
        await database.reviews.create_index("user_id")
        await database.reviews.create_index("rating")
        await database.reviews.create_index("date")
        await database.reviews.create_index([("product_id", 1), ("rating", 1)])
        
        # AI Ratings indexes
        await database.ai_ratings.create_index("product_id")
        await database.ai_ratings.create_index("ai_rating")
        await database.ai_ratings.create_index("timestamp")
        
        logger.info("✅ Database indexes created successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating indexes: {e}")
        return False

async def cleanup_old_data(days: int = 30):
    """Clean up old data (optional maintenance function)"""
    try:
        from datetime import datetime, timedelta
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Clean up old reviews (example)
        result = await database.reviews.delete_many({
            "created_at": {"$lt": cutoff_date}
        })
        
        logger.info(f"Cleaned up {result.deleted_count} old reviews")
        return result.deleted_count
    except Exception as e:
        logger.error(f"Error cleaning up old data: {e}")
        return 0
