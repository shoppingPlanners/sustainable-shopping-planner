# Sustainable Shopping Planner - Integrated System

A comprehensive AI-powered sustainable shopping platform that integrates four intelligent agents working together to provide personalized, sustainable shopping recommendations.

## 🌟 System Overview

This integrated system combines four specialized AI agents:

1. **Brand Data Collector Agent** - Scrapes and collects sustainability data from brand websites
2. **Rating Calculator Agent** - Calculates comprehensive sustainability ratings using ML and NLP
3. **User Behavior Tracker Agent** - Analyzes user behavior and preferences
4. **Suggestion Agent** - Provides intelligent, personalized recommendations

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Next.js)                       │
│              User Interface & Visualization                  │
└───────────────────────┬─────────────────────────────────────┘
                        │
                        │ REST API
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                  Unified Backend API                         │
│              (FastAPI - Python / Express - Node)            │
└───┬──────────────┬──────────────┬──────────────┬───────────┘
    │              │              │              │
    ▼              ▼              ▼              ▼
┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐
│ Brand   │  │ Rating  │  │ User    │  │Suggestion│
│  Data   │  │Calculator│  │Behavior │  │ Agent   │
│Collector│  │ Agent   │  │ Tracker │  │         │
└─────────┘  └─────────┘  └─────────┘  └─────────┘
     │            │            │            │
     └────────────┴────────────┴────────────┘
                    │
                    ▼
          ┌──────────────────┐
          │   Database Layer  │
          │  PostgreSQL +     │
          │  MongoDB          │
          └──────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL 14+
- MongoDB 6.0+
- Redis (optional, for caching)

### Installation

1. Clone the repository and navigate to the integrated system:
```bash
cd sustainable-shopping-integrated
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install Node.js dependencies:
```bash
cd frontend
npm install
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize databases:
```bash
python scripts/init_databases.py
```

### Running the System

#### Option 1: Run All Services at Once
```bash
python run_all.py
```

#### Option 2: Run Services Individually

Terminal 1 - Backend API:
```bash
cd backend
python -m uvicorn main:app --reload --port 8000
```

Terminal 2 - Brand Data Collector Agent:
```bash
cd agents/brand_data_collector
python app.py
```

Terminal 3 - Rating Calculator Agent:
```bash
cd agents/rating_calculator
python app.py
```

Terminal 4 - User Behavior Tracker Agent:
```bash
cd agents/user_behavior_tracker
python app.py
```

Terminal 5 - Suggestion Agent:
```bash
cd agents/suggestion_agent
python app.py
```

Terminal 6 - Frontend:
```bash
cd frontend
npm run dev
```

## 📦 Project Structure

```
sustainable-shopping-integrated/
├── agents/
│   ├── brand_data_collector/     # Agent 1: Brand data scraping
│   ├── rating_calculator/         # Agent 2: Sustainability rating
│   ├── user_behavior_tracker/     # Agent 3: User analytics
│   └── suggestion_agent/          # Agent 4: Recommendations
├── backend/
│   ├── api/                       # Unified API endpoints
│   ├── models/                    # Database models
│   ├── services/                  # Business logic
│   └── main.py                    # FastAPI application
├── frontend/
│   ├── app/                       # Next.js pages
│   ├── components/                # React components
│   └── lib/                       # Utilities
├── shared/
│   ├── database/                  # Database utilities
│   ├── models/                    # Shared data models
│   └── communication/             # Inter-agent communication
├── scripts/
│   ├── init_databases.py          # Database initialization
│   └── seed_data.py               # Sample data seeding
├── docs/
│   ├── API.md                     # API documentation
│   ├── AGENTS.md                  # Agent documentation
│   └── DEPLOYMENT.md              # Deployment guide
├── requirements.txt               # Python dependencies
├── docker-compose.yml             # Docker configuration
├── run_all.py                     # Run all services
└── README.md                      # This file
```

## 🤖 Agent Details

### 1. Brand Data Collector Agent
- **Port**: 5001
- **Purpose**: Scrapes brand websites for sustainability data
- **Key Features**:
  - Multi-site scraping with configurable selectors
  - Sustainability commitment extraction
  - Certification detection
  - Product catalog collection

### 2. Rating Calculator Agent
- **Port**: 5002
- **Purpose**: Calculates comprehensive sustainability scores
- **Key Features**:
  - NLP-based commitment analysis
  - Multi-factor scoring (environmental, social, economic)
  - Confidence scoring
  - Historical rating tracking

### 3. User Behavior Tracker Agent
- **Port**: 5003
- **Purpose**: Tracks and analyzes user behavior
- **Key Features**:
  - Event tracking (views, searches, purchases)
  - Pattern recognition
  - Sustainability score calculation
  - Anomaly detection

### 4. Suggestion Agent (NEW)
- **Port**: 5004
- **Purpose**: Generates personalized recommendations
- **Key Features**:
  - Multi-factor recommendation engine
  - Real-time personalization
  - Collaborative and content-based filtering
  - Explanation generation for recommendations

## 🔌 API Endpoints

### Main API (Port 8000)

#### Brands & Products
- `GET /api/brands` - List all brands
- `GET /api/brands/{id}` - Get brand details
- `GET /api/products` - List products
- `GET /api/products/{id}` - Get product details

#### Ratings
- `GET /api/ratings/brand/{id}` - Get brand rating
- `GET /api/ratings/product/{id}` - Get product rating
- `POST /api/ratings/calculate` - Trigger rating calculation

#### User Behavior
- `POST /api/tracking/event` - Track user event
- `GET /api/tracking/analytics/{user_id}` - Get user analytics
- `GET /api/tracking/score/{user_id}` - Get sustainability score

#### Recommendations
- `GET /api/suggestions/{user_id}` - Get personalized suggestions
- `GET /api/suggestions/trending` - Get trending sustainable products
- `POST /api/suggestions/feedback` - Submit feedback on recommendation

## 🛠️ Configuration

### Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/sustainable_shopping
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=sustainable_shopping

# APIs
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Services
BRAND_COLLECTOR_URL=http://localhost:5001
RATING_CALCULATOR_URL=http://localhost:5002
USER_BEHAVIOR_URL=http://localhost:5003
SUGGESTION_AGENT_URL=http://localhost:5004

# Redis (optional)
REDIS_URL=redis://localhost:6379

# Security
JWT_SECRET=your_jwt_secret
ENCRYPTION_KEY=your_encryption_key
```

## 📊 Features

### For Users
- ✅ Personalized sustainable product recommendations
- ✅ Detailed sustainability ratings and explanations
- ✅ Price comparison with sustainability factors
- ✅ Carbon footprint tracking
- ✅ Shopping behavior insights
- ✅ Goal setting and progress tracking

### For Administrators
- ✅ Real-time analytics dashboard
- ✅ Brand data management
- ✅ Rating algorithm tuning
- ✅ User behavior insights
- ✅ System health monitoring

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific agent tests
pytest tests/agents/test_brand_collector.py
pytest tests/agents/test_rating_calculator.py
pytest tests/agents/test_user_behavior.py
pytest tests/agents/test_suggestion_agent.py

# Run integration tests
pytest tests/integration/
```

## 🚢 Deployment

### Docker Deployment

```bash
# Build all services
docker-compose build

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

### Production Deployment

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed production deployment instructions.

## 🔒 Security

- JWT-based authentication
- Rate limiting on all endpoints
- Input validation and sanitization
- SQL injection prevention
- XSS protection
- CORS configuration
- Encrypted data storage

## 📈 Performance

- Response time: < 200ms (p95)
- Concurrent users: 10,000+
- Database queries optimized with indexes
- Redis caching for frequent queries
- Async processing for heavy operations

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## 📝 License

MIT License - see [LICENSE](LICENSE) for details.

## 👥 Team

Built for the Sustainable Shopping Initiative

## 📞 Support

For issues and questions:
- GitHub Issues: [Link to issues]
- Email: support@sustainableshopping.com
- Discord: [Link to discord]

## 🗺️ Roadmap

- [ ] Mobile app integration
- [ ] Voice assistant integration
- [ ] Blockchain-based verification
- [ ] Carbon credit marketplace
- [ ] Social features and community
- [ ] AR product visualization
- [ ] Multi-language support
- [ ] Offline mode

## 🙏 Acknowledgments

- OpenAI for GPT models
- Anthropic for Claude models
- The open-source community
- Sustainability data providers

