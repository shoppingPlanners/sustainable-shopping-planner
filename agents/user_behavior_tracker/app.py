import os
import time
import asyncio
from typing import Any, List, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Try to import motor, fallback to basic functionality if not available
try:
    import motor.motor_asyncio
    MOTOR_AVAILABLE = True
except ImportError:
    MOTOR_AVAILABLE = False
    print("Motor not available, using fallback mode")

from config import settings
from models import TrackingEvent, UserProfile, AnalyticsSummary

# Initialize database if motor is available
if MOTOR_AVAILABLE:
    try:
        client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_uri)
        db = client[settings.database_name]
        
        # Initialize services
        from behavior_analyzer import BehaviorAnalyzer
        from analytics_service import AnalyticsService
        behavior_analyzer = BehaviorAnalyzer(db)
        analytics_service = AnalyticsService(db)
    except Exception as e:
        print(f"Database initialization failed: {e}")
        MOTOR_AVAILABLE = False
        db = None
        behavior_analyzer = None
        analytics_service = None
else:
    db = None
    behavior_analyzer = None
    analytics_service = None

app = FastAPI(
    title="User Behavior Tracker AI Agent",
    description="Advanced AI-powered user behavior tracking and analytics for sustainable shopping",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    """Initialize database indexes and start background tasks"""
    if MOTOR_AVAILABLE and db is not None:
        try:
            # Create indexes for better performance
            await db.events.create_index([("timestamp", -1)])
            await db.events.create_index([("user_id", 1), ("timestamp", -1)])
            await db.events.create_index([("session_id", 1)])
            await db.events.create_index([("event_type", 1)])
            
            await db.profiles.create_index([("user_id", 1)])
            await db.usage_summaries.create_index([("created_at", -1)])
            await db.behavior_patterns.create_index([("user_id", 1), ("created_at", -1)])
            await db.user_insights.create_index([("user_id", 1), ("created_at", -1)])
            
            print("User Behavior Tracker AI Agent started successfully!")
        except Exception as e:
            print(f"Database setup failed: {e}")
    else:
        print("User Behavior Tracker AI Agent started in fallback mode!")

@app.on_event("shutdown")
async def shutdown():
    """Cleanup on shutdown"""
    if MOTOR_AVAILABLE and 'client' in globals():
        client.close()

# Core Tracking Endpoints
@app.post("/track")
async def track_event(event: TrackingEvent, background_tasks: BackgroundTasks):
    """Track user events with AI-powered analysis"""
    try:
        # Set timestamp if not provided
        if not event.timestamp:
            event.timestamp = time.time()
        
        if MOTOR_AVAILABLE and db is not None:
            # Store event in database
            event_dict = event.dict()
            await db.events.insert_one(event_dict)
            
            # Trigger background analysis for registered users
            if event.user_id and behavior_analyzer:
                background_tasks.add_task(analyze_user_behavior_background, event.user_id)
        else:
            # Fallback mode - just log the event
            print(f"Event tracked (fallback): {event.event_type} for user {event.user_id}")
        
        return {"status": "success", "message": "Event tracked successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to track event: {str(e)}")

@app.post("/bio")
async def update_profile(profile: UserProfile):
    """Update user profile information"""
    try:
        profile_dict = profile.dict()
        profile_dict["updated_at"] = time.time()
        
        await db.profiles.update_one(
            {"_id": profile.user_id},
            {"$set": profile_dict},
            upsert=True
        )
        
        return {"status": "success", "message": "Profile updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update profile: {str(e)}")

# Analytics Endpoints
@app.post("/summarize")
async def generate_summary(hours_back: int = 24):
    """Generate comprehensive analytics summary with AI insights"""
    try:
        summary = await analytics_service.generate_summary(hours_back)
        return {"status": "success", "summary": summary.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate summary: {str(e)}")

@app.get("/summaries/latest")
async def get_latest_summary():
    """Get the most recent analytics summary"""
    try:
        doc = await db.usage_summaries.find_one(sort=[("created_at", -1)])
        if not doc:
            raise HTTPException(status_code=404, detail="No summaries available")
        
        # Convert ObjectId to string
        doc["_id"] = str(doc.get("_id"))
        return doc
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get latest summary: {str(e)}")

@app.get("/analytics/user/{user_id}")
async def get_user_analytics(user_id: str, days_back: int = 30):
    """Get detailed analytics for a specific user"""
    try:
        analytics = await analytics_service.get_user_analytics(user_id, days_back)
        return {"status": "success", "analytics": analytics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user analytics: {str(e)}")

@app.get("/analytics/platform")
async def get_platform_metrics(days_back: int = 7):
    """Get platform-wide metrics and trends"""
    try:
        metrics = await analytics_service.get_platform_metrics(days_back)
        return {"status": "success", "metrics": metrics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get platform metrics: {str(e)}")

# Behavior Analysis Endpoints
@app.get("/behavior/patterns/{user_id}")
async def get_user_patterns(user_id: str, days_back: int = 30):
    """Get behavior patterns for a user"""
    try:
        patterns = await behavior_analyzer.analyze_user_behavior(user_id, days_back)
        return {"status": "success", "patterns": [p.dict() for p in patterns]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze behavior: {str(e)}")

@app.get("/behavior/insights/{user_id}")
async def get_user_insights(user_id: str, days_back: int = 7):
    """Get personalized insights for a user"""
    try:
        insights = await behavior_analyzer.generate_user_insights(user_id, days_back)
        return {"status": "success", "insights": [i.dict() for i in insights]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate insights: {str(e)}")

@app.get("/behavior/sustainability-score/{user_id}")
async def get_sustainability_score(user_id: str, days_back: int = 30):
    """Get user's sustainability engagement score"""
    try:
        score = await behavior_analyzer.calculate_sustainability_score(user_id, days_back)
        return {"status": "success", "sustainability_score": score}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to calculate sustainability score: {str(e)}")

@app.get("/behavior/recommendations/{user_id}")
async def get_user_recommendations(user_id: str):
    """Get personalized recommendations for a user"""
    try:
        recommendations = await behavior_analyzer.get_user_recommendations(user_id)
        return {"status": "success", "recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get recommendations: {str(e)}")

@app.get("/behavior/anomalies/{user_id}")
async def get_behavior_anomalies(user_id: str):
    """Detect unusual behavior patterns for a user"""
    try:
        anomalies = await behavior_analyzer.detect_behavior_anomalies(user_id)
        return {"status": "success", "anomalies": anomalies}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to detect anomalies: {str(e)}")

# Health and Status Endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        status = {
            "status": "healthy",
            "timestamp": time.time(),
            "version": "2.0.0",
            "services": {
                "database": "connected" if MOTOR_AVAILABLE and db is not None else "fallback_mode",
                "ai_service": "available" if behavior_analyzer and behavior_analyzer.ai_service.client else "fallback_mode"
            }
        }
        
        if MOTOR_AVAILABLE and db is not None:
            # Test database connection
            await db.command("ping")
        else:
            status["services"]["database"] = "fallback_mode"
            
        return status
    except Exception as e:
        return {
            "status": "degraded",
            "timestamp": time.time(),
            "version": "2.0.0",
            "error": str(e),
            "services": {
                "database": "fallback_mode",
                "ai_service": "fallback_mode"
            }
        }

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "User Behavior Tracker AI Agent",
        "version": "2.0.0",
        "description": "Advanced AI-powered user behavior tracking and analytics",
        "endpoints": {
            "tracking": "/track, /bio",
            "analytics": "/summarize, /analytics/*",
            "behavior": "/behavior/*",
            "health": "/health"
        }
    }

# Background Tasks
async def analyze_user_behavior_background(user_id: str):
    """Background task to analyze user behavior"""
    try:
        await behavior_analyzer.analyze_user_behavior(user_id, days_back=7)
        await behavior_analyzer.generate_user_insights(user_id, days_back=3)
    except Exception as e:
        print(f"Background analysis failed for user {user_id}: {e}")




