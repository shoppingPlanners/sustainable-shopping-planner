"""
Configuration settings for Sustainable Shopping Planner Backend
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB Configuration
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "sustainable-shopping-planner")

# Server Configuration
PORT = int(os.getenv("PORT", 3000))
HOST = os.getenv("HOST", "0.0.0.0")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# AI Agent Configuration
AI_AGENT_PATH = os.getenv("AI_AGENT_PATH", "../agents/rating_calculator/app.py")

# CORS Configuration
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:3001").split(",")

# JWT Configuration (for future authentication)
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-here")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", 30))

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Database Configuration
DATABASE_CONFIG = {
    "url": MONGODB_URL,
    "name": DATABASE_NAME,
    "collections": {
        "products": "products",
        "reviews": "reviews", 
        "ai_ratings": "ai_ratings",
        "users": "users",
        "product_list": "product_list"  # Your existing collection
    }
}

# API Configuration
API_CONFIG = {
    "title": "Sustainable Shopping Planner API",
    "description": "Backend API for sustainable shopping with AI rating system and MongoDB",
    "version": "1.0.0",
    "docs_url": "/docs",
    "redoc_url": "/redoc"
}

# CORS Configuration
CORS_CONFIG = {
    "allow_origins": CORS_ORIGINS,
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"]
}
