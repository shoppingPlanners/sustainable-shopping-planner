#!/usr/bin/env python3
"""
Startup script for the new structured Sustainable Shopping Planner Backend
"""

import subprocess
import sys
import os
import time

def install_requirements():
    """Install Python requirements with troubleshooting"""
    print("🔧 Installing Python requirements...")
    
    # First try minimal requirements
    try:
        print("📦 Trying minimal requirements first...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements-minimal.txt"])
        print("✅ Minimal requirements installed successfully!")
        
        # Then try full requirements
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements-full.txt"])
            print("✅ All dependencies installed successfully!")
            return True
        except subprocess.CalledProcessError:
            print("⚠️  Some optional packages failed, but core functionality should work")
            return True
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install even minimal requirements: {e}")
        print("🔧 Trying troubleshooting script...")
        
        # Try the troubleshooting script
        try:
            subprocess.check_call([sys.executable, "install_dependencies.py"])
            return True
        except subprocess.CalledProcessError:
            print("❌ Troubleshooting script also failed")
            print("📋 Please try manual installation:")
            print("   pip install fastapi uvicorn pydantic motor python-dotenv")
            return False

def create_env_file():
    """Create .env file from template if it doesn't exist"""
    if not os.path.exists(".env"):
        if os.path.exists("env_template.txt"):
            print("📝 Creating .env file from template...")
            with open("env_template.txt", "r") as template:
                content = template.read()
            with open(".env", "w") as env_file:
                env_file.write(content)
            print("✅ .env file created successfully!")
        else:
            print("⚠️  No .env template found. Please create .env file manually.")
    else:
        print("📊 .env file already exists")

def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting Sustainable Shopping Planner Backend...")
    print("=" * 60)
    
    try:
        # Start the server with uvicorn
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "server:app", 
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
    print("🌱 Sustainable Shopping Planner - Structured Backend")
    print("=" * 60)
    
    # Create .env file
    create_env_file()
    
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
    
    print("\n📁 Project Structure:")
    print("   • Controllers: Business logic")
    print("   • Models: Data validation")
    print("   • Routes: API endpoints")
    print("   • Utils: Helper functions")
    print("   • Config: Configuration management")
    
    print("\n" + "=" * 60)
    
    # Start the server
    start_server()

if __name__ == "__main__":
    main()
