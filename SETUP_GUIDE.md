# 🌱 Sustainable Shopping Planner - Complete Setup Guide

This guide will help you set up the complete Sustainable Shopping Planner with Python backend and AI rating system.

## 📋 System Overview

The system consists of four main components:
1. **Python Backend** (FastAPI) - API server with AI integration
2. **MongoDB Database** - NoSQL database for products, reviews, and ratings
3. **AI Agent** (Python) - Rating calculator with sentiment & sustainability analysis  
4. **Frontend** (Next.js) - User interface for shopping and reviews

## 🚀 Quick Start (All-in-One)

### Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB 4.4+
- Git

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd sustainable-shopping-planner
```

### 2. Start MongoDB
```bash
# Start MongoDB service
mongod

# Or using Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

### 3. Setup MongoDB Database
```bash
cd backend
python mongodb_setup.py
```
This will:
- Create database and collections
- Set up indexes for optimal performance
- Configure data validation

### 4. Start Backend (Python)
```bash
cd backend
python start.py
```
This will:
- Install Python dependencies
- Connect to MongoDB
- Start FastAPI server on port 3000
- Enable AI agent integration

### 5. Start Frontend (Next.js)
```bash
# In a new terminal
cd frontend
npm install
npm run dev
```
Frontend will be available at http://localhost:3001

### 6. Test the System
1. Visit http://localhost:3001
2. Navigate to a product page
3. Submit a review
4. Watch the AI rating update automatically!

## 🔧 Detailed Setup

### MongoDB Setup

#### 1. Install MongoDB
```bash
# Ubuntu/Debian
sudo apt-get install mongodb

# macOS
brew install mongodb-community

# Windows
# Download from https://www.mongodb.com/try/download/community
```

#### 2. Start MongoDB
```bash
# Start MongoDB service
sudo systemctl start mongod

# Or manually
mongod --dbpath /data/db
```

#### 3. Setup Database
```bash
cd backend
python mongodb_setup.py
```

#### 4. Verify MongoDB
```bash
# Connect to MongoDB shell
mongo

# Check database
use sustainable_shopping
show collections
```

### Backend Setup (Python)

#### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

#### 2. Start the Server
```bash
python main.py
# OR
python start.py  # Includes dependency installation
```

#### 3. Verify Backend
- API: http://localhost:3000
- Docs: http://localhost:3000/docs
- Health: http://localhost:3000/api/health

### AI Agent Setup

#### 1. Install AI Dependencies
```bash
cd agents/rating_calculator
python setup.py
```

#### 2. Test AI Agent
```bash
python app.py 1  # Test with product ID 1
```

### Frontend Setup (Next.js)

#### 1. Install Dependencies
```bash
cd frontend
npm install
```

#### 2. Start Development Server
```bash
npm run dev
```

#### 3. Access Frontend
- Main App: http://localhost:3001
- Product Pages: http://localhost:3001/products/1

## 🧪 Testing the Complete Flow

### 1. Test API Endpoints
```bash
# Get all products
curl http://localhost:3000/api/products

# Get specific product
curl http://localhost:3000/api/products/1

# Submit a review (triggers AI calculation)
curl -X POST http://localhost:3000/api/reviews \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": "1",
    "user_id": "test-user",
    "rating": 5,
    "text": "Amazing sustainable product! Love the eco-friendly materials."
  }'

# Check AI rating
curl http://localhost:3000/api/ratings/product/1
```

### 2. Test Frontend Integration
1. Open http://localhost:3001
2. Navigate to a product page
3. Submit a review with sustainability keywords
4. Watch the AI rating update in real-time

### 3. Test AI Agent Manually
```bash
cd agents/rating_calculator
python app.py 1
```

## 📊 System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Python        │    │   AI Agent      │
│   (Next.js)     │◄──►│   Backend       │◄──►│   (Python)      │
│   Port 3001     │    │   (FastAPI)     │    │   Rating Calc   │
│                 │    │   Port 3000     │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User          │    │   Database      │    │   AI Analysis   │
│   Interface     │    │   (SQLite/      │    │   (Sentiment +   │
│                 │    │   PostgreSQL)   │    │   Sustainability)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🔄 Complete User Flow

### 1. User Submits Review
```
User → Frontend → Python Backend → Database
```

### 2. AI Rating Calculation
```
Backend → AI Agent → Sentiment Analysis → Sustainability Analysis → Rating Calculation
```

### 3. Rating Display
```
AI Agent → Backend → Database → Frontend → User
```

## 🛠️ Development Commands

### Backend Development
```bash
# Start with auto-reload
python -m uvicorn main:app --reload --port 3000

# Start with debug logging
python -m uvicorn main:app --reload --log-level debug

# Run tests
python -m pytest  # (if you add tests)
```

### AI Agent Development
```bash
# Test specific product
python app.py 1

# Debug mode
python -c "import logging; logging.basicConfig(level=logging.DEBUG); exec(open('app.py').read())"
```

### Frontend Development
```bash
# Start development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

## 🔍 Monitoring & Debugging

### Backend Logs
The Python backend provides comprehensive logging:
- API requests/responses
- AI agent execution
- Database operations
- Error tracking

### AI Agent Logs
- Sentiment analysis results
- Sustainability scoring
- Rating calculations
- API communication

### Frontend Logs
- User interactions
- API calls
- Component rendering
- Error boundaries

## 🚀 Production Deployment

### Backend (Python)
```bash
# Using Gunicorn
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:3000

# Using Docker
docker build -t sustainable-backend .
docker run -p 3000:3000 sustainable-backend
```

### Frontend (Next.js)
```bash
# Build for production
npm run build

# Start production server
npm start

# Or using PM2
npm install -g pm2
pm2 start npm --name "sustainable-frontend" -- start
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Port Conflicts
```bash
# Check what's using port 3000
lsof -i :3000

# Kill process
kill -9 <PID>
```

#### 2. Python Dependencies
```bash
# Reinstall requirements
cd backend
pip install -r requirements.txt --force-reinstall
```

#### 3. AI Agent Not Working
```bash
# Check AI agent setup
cd agents/rating_calculator
python setup.py

# Test manually
python app.py 1
```

#### 4. Frontend Build Issues
```bash
# Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Debug Mode
```bash
# Backend debug
python -m uvicorn main:app --reload --log-level debug

# AI agent debug
cd agents/rating_calculator
python -c "import logging; logging.basicConfig(level=logging.DEBUG); exec(open('app.py').read())"
```

## 📈 Performance Optimization

### Backend
- Use PostgreSQL for production
- Implement caching with Redis
- Add database connection pooling
- Use async/await for I/O operations

### AI Agent
- Cache analysis results
- Batch process multiple products
- Optimize keyword matching
- Use more sophisticated NLP models

### Frontend
- Implement code splitting
- Add image optimization
- Use CDN for static assets
- Implement service workers

## 🎯 Next Steps

1. **Database Integration**: Replace mock data with real database
2. **Authentication**: Add user authentication and authorization
3. **Advanced AI**: Implement more sophisticated NLP models
4. **Real-time Updates**: Add WebSocket support for live updates
5. **Mobile App**: Create React Native mobile application
6. **Analytics**: Add user behavior tracking and analytics

## 📞 Support

If you encounter any issues:
1. Check the logs for error messages
2. Verify all services are running
3. Test individual components
4. Check the troubleshooting section
5. Create an issue in the repository

---

**Happy Sustainable Shopping! 🌱**
