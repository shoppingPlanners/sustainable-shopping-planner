#!/usr/bin/env python3
"""
Startup script for the Sustainable Shopping Planner Python Backend
"""

import subprocess
import sys
import os
import time

def install_requirements():
    """Install Python requirements"""
    print("🔧 Installing Python requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Python dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Python dependencies: {e}")
        return False

def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting Sustainable Shopping Planner Backend...")
    print("=" * 60)
    
    try:
        # Start the server with uvicorn
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "3000", 
            "--reload",
            "--log-level", "info"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")

def main():
    """Main startup function"""
    print("🌱 Sustainable Shopping Planner - Python Backend")
    print("=" * 60)
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed!")
        sys.exit(1)
    
    print("\n📋 Backend API will be available at:")
    print("   • Main API: http://localhost:3000")
    print("   • API Docs: http://localhost:3000/docs")
    print("   • Health Check: http://localhost:3000/api/health")
    print("\n🤖 AI Agent integration ready!")
    print("   • AI Agent: agents/rating_calculator/app.py")
    print("   • Auto-triggered on review submission")
    
    print("\n" + "=" * 60)
    
    # Start the server
    start_server()

if __name__ == "__main__":
    main()
