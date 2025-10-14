# 🔧 Troubleshooting Guide

## Common Installation Issues

### 1. Metadata Generation Failed

**Error:** `error: metadata-generation-failed`

**Solutions:**

#### Option A: Use the troubleshooting script
```bash
python install_dependencies.py
```

#### Option B: Install minimal requirements first
```bash
pip install -r requirements-minimal.txt
```

#### Option C: Install packages individually
```bash
pip install fastapi
pip install uvicorn
pip install pydantic
pip install motor
pip install python-dotenv
```

### 2. Python Version Issues

**Check your Python version:**
```bash
python --version
```

**Required:** Python 3.8+ (you have Python 3.13 which should work)

### 3. Pip Issues

**Upgrade pip:**
```bash
python -m pip install --upgrade pip
```

**Clear pip cache:**
```bash
pip cache purge
```

### 4. Windows-Specific Issues

**Use Windows Store Python:**
```bash
# If using Windows Store Python, try:
python -m pip install --user fastapi uvicorn pydantic motor python-dotenv
```

**Alternative installation:**
```bash
# Try with --no-cache-dir
pip install --no-cache-dir fastapi uvicorn pydantic motor python-dotenv
```

### 5. Virtual Environment Issues

**Create a new virtual environment:**
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements-minimal.txt
```

## Step-by-Step Installation

### Method 1: Troubleshooting Script
```bash
cd backend
python install_dependencies.py
```

### Method 2: Manual Installation
```bash
cd backend

# Step 1: Install minimal requirements
pip install -r requirements-minimal.txt

# Step 2: Test basic functionality
python -c "import fastapi; print('FastAPI works!')"

# Step 3: Install full requirements
pip install -r requirements-full.txt
```

### Method 3: Individual Package Installation
```bash
cd backend

# Install core packages
pip install fastapi
pip install uvicorn
pip install pydantic
pip install motor
pip install python-dotenv

# Test installation
python -c "import fastapi, uvicorn, pydantic, motor; print('Core packages work!')"

# Install additional packages
pip install beanie
pip install pymongo
pip install requests
pip install python-multipart
```

## Testing Installation

### Test Core Functionality
```bash
python -c "
import fastapi
import uvicorn
import pydantic
import motor
print('✅ Core packages imported successfully!')
"
```

### Test Database Connection
```bash
python test_connection.py
```

### Test Server
```bash
python server.py
```

## Alternative Solutions

### 1. Use Conda Instead of Pip
```bash
# Install conda first, then:
conda install fastapi uvicorn pydantic
pip install motor python-dotenv beanie
```

### 2. Use Docker
```bash
# Create Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "server.py"]
```

### 3. Use Poetry
```bash
# Install poetry first, then:
poetry init
poetry add fastapi uvicorn pydantic motor python-dotenv beanie
```

## Getting Help

If you're still having issues:

1. **Check Python version:** `python --version`
2. **Check pip version:** `pip --version`
3. **Try virtual environment:** `python -m venv venv`
4. **Use minimal requirements:** `pip install -r requirements-minimal.txt`
5. **Run troubleshooting script:** `python install_dependencies.py`

## Success Indicators

You'll know the installation worked when:
- ✅ No error messages during installation
- ✅ `python -c "import fastapi"` works
- ✅ `python test_connection.py` connects to MongoDB
- ✅ `python server.py` starts the server
- ✅ You can access http://localhost:3000/docs
