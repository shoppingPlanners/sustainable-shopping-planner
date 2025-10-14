# User Behavior Tracker AI Agent

An advanced AI-powered user behavior tracking and analytics system for sustainable shopping platforms. This agent provides comprehensive user behavior analysis, personalized insights, and actionable recommendations using machine learning and AI technologies.

## Features

### 🧠 AI-Powered Analysis
- **Behavior Pattern Recognition**: Automatically detects user shopping patterns, preferences, and engagement levels
- **Sustainability Scoring**: Calculates user sustainability engagement scores based on behavior
- **Personalized Insights**: Generates actionable recommendations using OpenAI GPT models
- **Anomaly Detection**: Identifies unusual behavior patterns for security and optimization

### 📊 Advanced Analytics
- **Real-time Event Tracking**: Comprehensive event tracking with session management
- **User Journey Analysis**: Deep insights into user behavior across the platform
- **Platform Metrics**: Platform-wide analytics with trends and insights
- **Sustainability Impact**: Track and measure sustainability engagement across users

### 🔒 Privacy & Compliance
- **Consent Management**: GDPR-compliant consent tracking and management
- **Data Anonymization**: Secure handling of user data with privacy controls
- **Configurable Retention**: Flexible data retention policies

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │  Behavior        │    │   MongoDB       │
│   Tracking      │───▶│  Tracker Agent   │───▶│   Database      │
│   Library       │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │   AI Service     │
                       │   (OpenAI GPT)   │
                       └──────────────────┘
```

## Quick Start

### Prerequisites
- Python 3.8+
- MongoDB 4.4+
- OpenAI API Key (optional, fallback mode available)

### Installation

1. **Clone and navigate to the agent directory:**
```bash
cd agents/user_behavior_tracker
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Start MongoDB:**
```bash
# Using Docker
docker run -d -p 27017:27017 --name mongodb mongo:latest

# Or start your local MongoDB instance
```

5. **Run the agent:**
```bash
python run.py
```

The agent will start on `http://localhost:8001` by default.

## Configuration

### Environment Variables

Create a `.env` file in the agent directory:

```env
# Database
MONGO_URI=mongodb://localhost:27017
DATABASE_NAME=sustainable_shopping

# AI Configuration (Optional)
OPENAI_API_KEY=your_openai_api_key_here
AI_MODEL=gpt-3.5-turbo

# Server Configuration
HOST=0.0.0.0
PORT=8001
RELOAD=true

# Redis (Optional, for caching)
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key-here
```

### Frontend Integration

The agent works seamlessly with the frontend tracking library. Update your frontend configuration:

```typescript
// frontend/lib/config.ts
export const TRACKER_URL = "http://localhost:8001";
```

## API Endpoints

### Core Tracking
- `POST /track` - Track user events
- `POST /bio` - Update user profile
- `GET /health` - Health check

### Analytics
- `POST /summarize` - Generate analytics summary
- `GET /summaries/latest` - Get latest summary
- `GET /analytics/user/{user_id}` - User-specific analytics
- `GET /analytics/platform` - Platform-wide metrics

### Behavior Analysis
- `GET /behavior/patterns/{user_id}` - Get user behavior patterns
- `GET /behavior/insights/{user_id}` - Get personalized insights
- `GET /behavior/sustainability-score/{user_id}` - Calculate sustainability score
- `GET /behavior/recommendations/{user_id}` - Get recommendations
- `GET /behavior/anomalies/{user_id}` - Detect behavior anomalies

## Usage Examples

### Tracking Events

```python
import requests

# Track a page view
requests.post("http://localhost:8001/track", json={
    "event_type": "page_view",
    "user_id": "user123",
    "session_id": "session456",
    "page": "/suggestions",
    "timestamp": 1640995200.0
})

# Track a search
requests.post("http://localhost:8001/track", json={
    "event_type": "search",
    "user_id": "user123",
    "keywords": ["sustainable", "organic", "cotton"],
    "timestamp": 1640995200.0
})
```

### Getting User Insights

```python
# Get behavior patterns
response = requests.get("http://localhost:8001/behavior/patterns/user123")
patterns = response.json()["patterns"]

# Get personalized insights
response = requests.get("http://localhost:8001/behavior/insights/user123")
insights = response.json()["insights"]

# Get sustainability score
response = requests.get("http://localhost:8001/behavior/sustainability-score/user123")
score = response.json()["sustainability_score"]
```

### Analytics Summary

```python
# Generate platform analytics
response = requests.post("http://localhost:8001/summarize", json={"hours_back": 24})
summary = response.json()["summary"]

print(f"Total events: {summary['total_events']}")
print(f"Unique users: {summary['unique_users']}")
print(f"Top pages: {summary['top_pages']}")
```

## Data Models

### TrackingEvent
```python
{
    "event_type": "page_view|search|view_item|click|filter_select|purchase",
    "user_id": "string",
    "session_id": "string",
    "item_id": "string",
    "brand_id": "string",
    "page": "string",
    "keywords": ["string"],
    "element": "string",
    "tags": ["string"],
    "metadata": {},
    "timestamp": 1640995200.0
}
```

### UserProfile
```python
{
    "user_id": "string",
    "age": 25,
    "gender": "string",
    "location": "string",
    "preferences": {},
    "sustainability_score": 85.5,
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
}
```

### BehaviorPattern
```python
{
    "user_id": "string",
    "pattern_type": "sustainability_focus|price_sensitive|active_searcher",
    "confidence": 0.85,
    "data": {},
    "created_at": "2023-01-01T00:00:00Z"
}
```

## AI Features

### Behavior Analysis
The AI service analyzes user behavior patterns including:
- **Shopping Style**: Budget-conscious, luxury-focused, sustainability-driven
- **Engagement Level**: High, medium, low, minimal
- **Sustainability Focus**: Based on interaction with sustainable products
- **Search Behavior**: Active searcher patterns
- **Price Sensitivity**: Based on price range interactions

### Personalized Insights
Generates actionable insights such as:
- Brand recommendations based on preferences
- Sustainability tips and suggestions
- Price optimization recommendations
- Product discovery suggestions

### Analytics Intelligence
Provides platform-level insights:
- User engagement trends
- Sustainability impact metrics
- Feature usage analytics
- Optimization recommendations

## Monitoring & Health Checks

### Health Endpoint
```bash
curl http://localhost:8001/health
```

Response:
```json
{
    "status": "healthy",
    "timestamp": 1640995200.0,
    "version": "2.0.0",
    "services": {
        "database": "connected",
        "ai_service": "available"
    }
}
```

### Logging
The agent provides comprehensive logging for:
- Event tracking
- AI analysis results
- Error handling
- Performance metrics

## Development

### Running in Development Mode
```bash
python run.py
# or
uvicorn app:app --reload --host 0.0.0.0 --port 8001
```

### Testing
```bash
# Test health endpoint
curl http://localhost:8001/health

# Test event tracking
curl -X POST http://localhost:8001/track \
  -H "Content-Type: application/json" \
  -d '{"event_type": "page_view", "user_id": "test_user", "page": "/test"}'
```

## Production Deployment

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8001

CMD ["python", "run.py"]
```

### Environment Setup
- Use production MongoDB instance
- Set up Redis for caching
- Configure OpenAI API key
- Set appropriate CORS origins
- Use production-grade secret keys

## Troubleshooting

### Common Issues

1. **MongoDB Connection Failed**
   - Check MongoDB is running
   - Verify MONGO_URI in .env
   - Check network connectivity

2. **AI Service Not Working**
   - Verify OPENAI_API_KEY is set
   - Check API key validity
   - System will fall back to rule-based analysis

3. **Frontend Tracking Issues**
   - Verify TRACKER_URL in frontend config
   - Check CORS settings
   - Ensure consent is properly managed

### Performance Optimization

1. **Database Indexes**: Automatically created on startup
2. **Background Processing**: Heavy analysis runs in background
3. **Caching**: Redis integration for frequently accessed data
4. **Batch Processing**: Efficient handling of multiple events

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is part of the Sustainable Shopping Planner platform.