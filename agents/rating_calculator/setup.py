#!/usr/bin/env python3
"""
Setup script for the AI Rating Calculator Agent
Installs required dependencies and sets up the environment
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required dependencies"""
    print("🔧 Installing Python requirements...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Python dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Python dependencies: {e}")
        return False
    
    return True

def test_installation():
    """Test if the installation works"""
    print("🧪 Testing installation...")
    
    try:
        # Test imports
        import requests
        import pandas as pd
        import numpy as np
        print("✅ All required packages imported successfully!")
        return True
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up AI Rating Calculator Agent...")
    print("=" * 50)
    
    # Change to the script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed!")
        sys.exit(1)
    
    # Test installation
    if not test_installation():
        print("❌ Setup verification failed!")
        sys.exit(1)
    
    print("=" * 50)
    print("✅ AI Rating Calculator Agent setup complete!")
    print("\n📋 Next steps:")
    print("1. Start the backend server: cd ../../backend && npm install && npm start")
    print("2. Test the AI agent: python app.py <product_id>")
    print("3. Start the frontend: cd ../../frontend && npm install && npm run dev")

if __name__ == "__main__":
    main()
