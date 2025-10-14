#!/usr/bin/env python3
"""
Dependency installation script with troubleshooting
"""

import subprocess
import sys
import os
import platform

def check_python_version():
    """Check Python version compatibility"""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        return False
    
    print("✅ Python version is compatible")
    return True

def upgrade_pip():
    """Upgrade pip to latest version"""
    print("🔧 Upgrading pip...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "--upgrade", "pip"
        ])
        print("✅ Pip upgraded successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Failed to upgrade pip: {e}")
        return False

def install_packages_individually():
    """Install packages one by one to identify problematic ones"""
    packages = [
        "fastapi",
        "uvicorn[standard]",
        "pydantic",
        "python-multipart",
        "requests",
        "python-dotenv",
        "motor",
        "pymongo",
        "beanie"
    ]
    
    failed_packages = []
    
    for package in packages:
        print(f"📦 Installing {package}...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", package
            ])
            print(f"✅ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")
            failed_packages.append(package)
    
    return failed_packages

def install_minimal_requirements():
    """Install minimal working requirements"""
    minimal_packages = [
        "fastapi",
        "uvicorn",
        "pydantic",
        "motor",
        "python-dotenv"
    ]
    
    print("🔧 Installing minimal requirements...")
    for package in minimal_packages:
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", package
            ])
            print(f"✅ {package} installed")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")

def check_system_info():
    """Check system information"""
    print("🖥️  System Information:")
    print(f"   Platform: {platform.platform()}")
    print(f"   Architecture: {platform.architecture()}")
    print(f"   Python executable: {sys.executable}")
    print(f"   Pip location: {subprocess.check_output([sys.executable, '-m', 'pip', '--version']).decode()}")

def main():
    """Main installation function"""
    print("🌱 Sustainable Shopping Planner - Dependency Installation")
    print("=" * 60)
    
    # Check system info
    check_system_info()
    print()
    
    # Check Python version
    if not check_python_version():
        return False
    
    print()
    
    # Upgrade pip
    upgrade_pip()
    print()
    
    # Try installing from requirements.txt first
    print("📦 Attempting to install from requirements.txt...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ All dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install from requirements.txt")
        print("🔧 Trying individual package installation...")
        print()
        
        # Try installing packages individually
        failed_packages = install_packages_individually()
        
        if failed_packages:
            print(f"\n⚠️  Failed packages: {failed_packages}")
            print("🔧 Trying minimal installation...")
            install_minimal_requirements()
            
            print("\n📋 Manual installation steps:")
            for package in failed_packages:
                print(f"   pip install {package}")
        else:
            print("✅ All packages installed successfully!")
            return True
    
    return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n🎉 Installation completed successfully!")
        print("🚀 You can now run: python server.py")
    else:
        print("\n❌ Installation had issues. Please try manual installation:")
        print("   pip install fastapi uvicorn pydantic motor python-dotenv")
        print("   pip install beanie pymongo requests python-multipart")
