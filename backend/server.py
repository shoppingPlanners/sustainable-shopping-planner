"""
Main server file for Sustainable Shopping Planner Backend
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db, close_db
from config import API_CONFIG, CORS_CONFIG, PORT, HOST, DEBUG
from routes import productRoutes, reviewRoutes, ratingRoutes
from utils.database_utils import create_indexes
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(**API_CONFIG)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    **CORS_CONFIG
)

# Include routers
app.include_router(productRoutes.router)
app.include_router(reviewRoutes.router)
app.include_router(ratingRoutes.router)

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize database and setup on startup"""
    try:
        logger.info("🚀 Starting Sustainable Shopping Planner Backend...")
        
        # Initialize MongoDB connection
        await init_db()
        logger.info("✅ MongoDB connection established")
        
        # Create database indexes
        await create_indexes()
        logger.info("✅ Database indexes created")
        
        logger.info(f"🌱 Backend ready at http://{HOST}:{PORT}")
        logger.info(f"📚 API docs available at http://{HOST}:{PORT}/docs")
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    try:
        logger.info("🛑 Shutting down backend...")
        await close_db()
        logger.info("✅ Shutdown complete")
    except Exception as e:
        logger.error(f"❌ Shutdown error: {e}")

# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Sustainable Shopping Planner API",
        "version": API_CONFIG["version"],
        "status": "running",
        "docs": "/docs"
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "OK",
        "message": "API is running",
        "database": "connected"
    }

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "server:app",
        host=HOST,
        port=PORT,
        reload=DEBUG,
        log_level="info"
    )
