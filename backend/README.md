# 🌱 Sustainable Shopping Planner - Python Backend

FastAPI-based backend with MongoDB integration and AI rating system for sustainable shopping recommendations.

## 📁 Project Structure

```
backend/
├── __init__.py                 # Package initialization
├── server.py                   # Main server file
├── config.py                   # Configuration settings
├── database.py                 # MongoDB models and connection
├── requirements.txt            # Python dependencies
├── package.json               # Project metadata (Node.js style)
├── README.md                  # This file
│
├── controllers/               # Business logic controllers
│   ├── __init__.py
│   ├── productController.py   # Product operations
│   ├── reviewController.py    # Review operations
│   └── ratingController.py    # AI rating operations
│
├── models/                   # Pydantic models
│   ├── __init__.py
│   ├── product.py           # Product models
│   ├── review.py            # Review models
│   └── rating.py            # AI rating models
│
├── routes/                  # API route handlers
│   ├── __init__.py
│   ├── productRoutes.py     # Product endpoints
│   ├── reviewRoutes.py      # Review endpoints
│   └── ratingRoutes.py      # Rating endpoints
│
├── utils/                  # Utility functions
│   ├── __init__.py
│   ├── ai_trigger.py        # AI agent integration
│   └── database_utils.py   # Database utilities
│
└── scripts/               # Helper scripts
    ├── test_connection.py
    ├── product_list_helper.py
    └── product_list_migration.py
```

## 🚀 Quick Start

### 1. Environment Setup

Create a `.env` file in the backend directory:

```bash
# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=sustainable-shopping-planner

# Server Configuration
PORT=3000
HOST=0.0.0.0
DEBUG=True

# AI Agent Configuration
AI_AGENT_PATH=../agents/rating_calculator/app.py

# CORS Configuration
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the Server

```bash
# Development mode
python server.py

# Or using uvicorn directly
uvicorn server:app --reload --host 0.0.0.0 --port 3000
```

### 4. Access the API

- **API**: http://localhost:3000
- **Interactive Docs**: http://localhost:3000/docs
- **Health Check**: http://localhost:3000/api/health

## 📊 API Endpoints

### Products
- `GET /api/products` - Get all products
- `GET /api/products/{id}` - Get single product
- `POST /api/products` - Create new product
- `PUT /api/products/{id}` - Update product
- `DELETE /api/products/{id}` - Delete product
- `GET /api/products/search/?q=query` - Search products

### Reviews
- `GET /api/reviews` - Get all reviews
- `GET /api/reviews/{id}` - Get single review
- `POST /api/reviews` - Create new review (triggers AI calculation)
- `PUT /api/reviews/{id}` - Update review
- `DELETE /api/reviews/{id}` - Delete review
- `GET /api/reviews/product/{id}` - Get product reviews

### AI Ratings
- `GET /api/ratings` - Get all AI ratings
- `GET /api/ratings/{id}` - Get single rating
- `GET /api/ratings/product/{id}` - Get product rating
- `POST /api/ratings` - Save AI rating (called by AI agent)
- `PUT /api/ratings/{id}` - Update rating
- `DELETE /api/ratings/{id}` - Delete rating

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MONGODB_URL` | `mongodb://localhost:27017` | MongoDB connection string |
| `DATABASE_NAME` | `sustainable-shopping-planner` | Database name |
| `PORT` | `3000` | Server port |
| `HOST` | `0.0.0.0` | Server host |
| `DEBUG` | `True` | Debug mode |
| `CORS_ORIGINS` | `http://localhost:3000,http://localhost:3001` | CORS origins |

### Database Configuration

The system uses MongoDB with the following collections:
- **products** - Product catalog
- **reviews** - Customer reviews
- **ai_ratings** - AI-calculated ratings
- **users** - User accounts
- **product_list** - Your existing collection

## 🛠️ Development

### Project Structure Benefits

1. **Separation of Concerns** - Controllers, models, routes, and utils are separated
2. **Modularity** - Each component can be developed and tested independently
3. **Scalability** - Easy to add new features and endpoints
4. **Maintainability** - Clear structure makes code easier to maintain
5. **Reusability** - Components can be reused across different parts of the application

### Adding New Features

1. **Create Model** - Add Pydantic models in `models/`
2. **Create Controller** - Add business logic in `controllers/`
3. **Create Routes** - Add API endpoints in `routes/`
4. **Update Database** - Add MongoDB models in `database.py`
5. **Test** - Test the new functionality

### Code Organization

- **Controllers** - Handle business logic and database operations
- **Models** - Define data structures and validation
- **Routes** - Define API endpoints and request/response handling
- **Utils** - Provide utility functions and helpers
- **Config** - Centralize configuration management

## 🧪 Testing

### Test Connection

```bash
python test_connection.py
```

### Test with Existing Data

```bash
python product_list_helper.py
```

### Migrate Existing Data

```bash
python product_list_migration.py
```

## 📈 Performance

### Database Indexes

The system automatically creates indexes for:
- Product search (name, description)
- Review filtering (product_id, user_id, rating)
- AI rating queries (product_id, ai_rating, timestamp)

### Caching

- MongoDB connection pooling
- Async operations for better performance
- Optimized queries with proper indexing

## 🔒 Security

### Input Validation

- Pydantic models provide automatic validation
- Type checking and range validation
- SQL injection prevention through MongoDB

### CORS Configuration

- Configurable CORS origins
- Secure by default
- Production-ready settings

## 🚀 Production Deployment

### Using Docker

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 3000

CMD ["python", "server.py"]
```

### Using Gunicorn

```bash
pip install gunicorn
gunicorn server:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:3000
```

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MongoDB Documentation](https://docs.mongodb.com/)
- [Beanie ODM](https://beanie-odm.dev/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)

---

**Happy Sustainable Shopping! 🌱**