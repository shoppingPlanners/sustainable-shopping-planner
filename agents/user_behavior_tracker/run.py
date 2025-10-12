#!/usr/bin/env python3
"""
User Behavior Tracker AI Agent - Main Entry Point
"""

import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Configuration
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8001"))
    reload = os.getenv("RELOAD", "true").lower() == "true"
    
    print(f"Starting User Behavior Tracker AI Agent on {host}:{port}")
    print(f"Reload mode: {reload}")
    
    # Start the server
    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )