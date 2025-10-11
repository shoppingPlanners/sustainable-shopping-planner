import os
from typing import Optional

class Settings:
    def __init__(self):
        # Database
        self.mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
        self.database_name = os.getenv("DATABASE_NAME", "sustainable_shopping")
        
        # AI Configuration
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.ai_model = os.getenv("AI_MODEL", "gpt-3.5-turbo")
        
        # Redis for caching
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
        
        # Analytics
        self.analytics_batch_size = int(os.getenv("ANALYTICS_BATCH_SIZE", "100"))
        self.analytics_interval = int(os.getenv("ANALYTICS_INTERVAL", "3600"))  # 1 hour
        
        # Security
        self.secret_key = os.getenv("SECRET_KEY", "your-secret-key-here")

settings = Settings()

