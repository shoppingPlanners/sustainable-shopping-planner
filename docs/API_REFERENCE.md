# API Reference

Complete API documentation for all 4 agents in the Sustainable Shopping Planner system.

## Table of Contents

1. [Agent 1: Brand Data Collector](#agent-1-brand-data-collector)
2. [Agent 2: Rating Calculator](#agent-2-rating-calculator)
3. [Agent 3: User Behavior Tracker](#agent-3-user-behavior-tracker)
4. [Agent 4: Suggestion Agent](#agent-4-suggestion-agent)

---

## Agent 1: Brand Data Collector

**Base URL**: `http://localhost:5001`

### GET /

Get agent information

**Response**:
```json
{
  "agent": "Brand Data Collector",
  "version": "1.0.0",
  "status": "operational",
  "brands_collected": 10
}
```

### GET /health

Health check endpoint

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "brands_in_database": 10
}
```

### POST /scrape

Scrape a brand website for products and sustainability data

**Request Body**:
```json
{
  "url": "https://example.com/products",
  "brand_name": "EcoBrand"  // optional
}
```

**Response**:
```json
{
  "status": "success",
  "data": {
    "brand_name": "EcoBrand",
    "url": "https://example.com/products",
    "products": [
      {
        "product_name": "Organic T-Shirt",
        "product_url": "https://example.com/product/1",
        "price": "$29.99",
        "category": "Clothing",
        "available_sizes": ["S", "M", "L"],
        "sustainability_focus": ["organic", "fair-trade"]
      }
    ],
    "sustainability_commitments": [
      "We use 100% organic materials",
      "Carbon neutral by 2030"
    ],
    "certifications": ["Fair Trade", "B-Corp"],
    "scraped_at": "2024-01-15T10:30:00Z",
    "product_count": 15
  },
  "cached": false
}
```

### GET /brands

Get all collected brand data

**Response**:
```json
{
  "status": "success",
  "count": 10,
  "brands": [...]
}
```

### GET /brands/{brand_id}

Get specific brand data

**Response**:
```json
{
  "status": "success",
  "data": {...}
}
```

### POST /scrape/batch

Scrape multiple brands at once

**Request Body**:
```json
["https://brand1.com", "https://brand2.com", "https://brand3.com"]
```

---

## Agent 2: Rating Calculator

**Base URL**: `http://localhost:5002`

### GET /

Get agent information

### GET /health

Health check endpoint

### POST /calculate

Calculate sustainability rating for a brand

**Request Body**:
```json
{
  "brand_name": "EcoBrand",
  "products": [...],
  "sustainability_commitments": [
    "We use 100% renewable energy",
    "Zero waste by 2025"
  ],
  "certifications": ["B-Corp", "Carbon Neutral"]
}
```

**Response**:
```json
{
  "status": "success",
  "rating": {
    "brand_name": "EcoBrand",
    "overall_score": 85.5,
    "environmental_score": 88.0,
    "social_score": 82.0,
    "economic_score": 86.5,
    "confidence_score": 0.85,
    "grade": "A",
    "breakdown": {
      "environmental": {
        "score": 88.0,
        "weight": 0.40,
        "factors": ["Carbon Neutral", "Renewable Energy", "Zero Waste"]
      },
      "social": {
        "score": 82.0,
        "weight": 0.35,
        "factors": ["Fair Trade", "Worker Rights"]
      },
      "economic": {
        "score": 86.5,
        "weight": 0.25,
        "factors": ["Durable", "Local Sourcing"]
      },
      "certifications": {
        "count": 2,
        "list": ["B-Corp", "Carbon Neutral"],
        "score_contribution": 29
      }
    },
    "calculated_at": "2024-01-15T10:35:00Z"
  }
}
```

### GET /ratings

Get all calculated ratings

**Response**:
```json
{
  "status": "success",
  "count": 10,
  "ratings": [...]
}
```

### GET /ratings/{brand_name}

Get rating for a specific brand

---

## Agent 3: User Behavior Tracker

**Base URL**: `http://localhost:5003`

### GET /

Get agent information

### GET /health

Health check endpoint

### POST /track

Track a user event

**Request Body**:
```json
{
  "user_id": "user123",
  "event_type": "view",  // 'view', 'search', 'click', 'purchase', 'add_to_cart', 'favorite'
  "product_id": "prod1",
  "brand_id": "brand1",
  "category": "clothing",
  "tags": ["organic", "sustainable"],
  "metadata": {
    "price": 29.99,
    "source": "recommendations"
  },
  "timestamp": 1705315800  // optional, auto-generated if not provided
}
```

**Response**:
```json
{
  "status": "success",
  "message": "Event tracked successfully"
}
```

### GET /behavior/patterns/{user_id}

Get behavior patterns for a user

**Query Parameters**:
- `days_back` (optional, default: 30) - Number of days to analyze

**Response**:
```json
{
  "status": "success",
  "user_id": "user123",
  "patterns": [
    {
      "pattern_type": "category_preference",
      "categories": ["clothing", "accessories", "footwear"],
      "confidence": 0.85,
      "created_at": "2024-01-15T10:40:00Z"
    },
    {
      "pattern_type": "sustainability_focus",
      "interests": ["organic", "fair-trade", "recycled"],
      "confidence": 0.75,
      "created_at": "2024-01-15T10:40:00Z"
    }
  ],
  "summary": "Analyzed 45 events, found 4 patterns"
}
```

### GET /behavior/sustainability-score/{user_id}

Get user's sustainability engagement score

**Query Parameters**:
- `days_back` (optional, default: 30)

**Response**:
```json
{
  "status": "success",
  "user_id": "user123",
  "sustainability_score": 78.5,
  "calculated_at": "2024-01-15T10:40:00Z"
}
```

### GET /behavior/insights/{user_id}

Get personalized insights for a user

**Query Parameters**:
- `days_back` (optional, default: 7)

**Response**:
```json
{
  "status": "success",
  "user_id": "user123",
  "insights": [
    {
      "user_id": "user123",
      "insight_type": "sustainability_champion",
      "title": "🌱 Sustainability Champion!",
      "description": "You're making great sustainable choices! Your sustainability score is 78/100.",
      "priority": 5,
      "actionable": false,
      "created_at": "2024-01-15T10:40:00Z",
      "metadata": {"score": 78.5}
    }
  ]
}
```

### GET /behavior/recommendations/{user_id}

Get user data formatted for recommendation engine

**Response**:
```json
{
  "status": "success",
  "user_id": "user123",
  "sustainability_score": 78.5,
  "preferred_categories": ["clothing", "accessories"],
  "preferred_brands": ["brand1", "brand2"],
  "sustainability_interests": ["organic", "fair-trade"],
  "average_price_point": 45.5,
  "price_std": 15.2,
  "viewed_products": ["prod1", "prod2", "prod3"],
  "viewed_categories": ["clothing", "accessories", "footwear"]
}
```

### GET /users

Get all tracked users

**Response**:
```json
{
  "status": "success",
  "count": 25,
  "users": [
    {
      "user_id": "user123",
      "event_count": 45,
      "sustainability_score": 78.5
    }
  ]
}
```

---

## Agent 4: Suggestion Agent

**Base URL**: `http://localhost:5004`

### GET /

Get agent information

### GET /health

Health check endpoint

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:45:00Z",
  "connected_agents": {
    "brand_collector": "http://localhost:5001",
    "rating_calculator": "http://localhost:5002",
    "user_behavior": "http://localhost:5003"
  }
}
```

### GET /suggestions/{user_id}

Get personalized product suggestions

**Query Parameters**:
- `limit` (optional, default: 10, max: 50) - Number of suggestions
- `category` (optional) - Filter by category
- `min_sustainability_score` (optional) - Minimum sustainability score (0-100)

**Response**:
```json
{
  "status": "success",
  "user_id": "user123",
  "suggestions": [
    {
      "product_id": "prod1",
      "product_name": "Organic Cotton T-Shirt",
      "brand_name": "EcoBrand",
      "sustainability_score": 85.5,
      "price": "$29.99",
      "recommendation_score": 0.892,
      "reasons": [
        "Excellent sustainability rating (86/100)",
        "Matches your favorite categories",
        "Features: organic, fair-trade",
        "Certified: B-Corp, Fair Trade"
      ],
      "category": "clothing",
      "url": "https://example.com/product/1"
    }
  ],
  "count": 10,
  "generated_at": "2024-01-15T10:45:00Z"
}
```

### GET /trending

Get trending sustainable products

**Query Parameters**:
- `limit` (optional, default: 10, max: 50)
- `min_sustainability_score` (optional, default: 70)

**Response**:
```json
{
  "status": "success",
  "trending_products": [...],
  "count": 10,
  "generated_at": "2024-01-15T10:45:00Z"
}
```

### POST /feedback

Submit feedback on a suggestion

**Request Body**:
```json
{
  "user_id": "user123",
  "product_id": "prod1",
  "feedback_type": "clicked"  // 'viewed', 'clicked', 'purchased', 'dismissed', 'liked'
}
```

**Response**:
```json
{
  "status": "success",
  "message": "Feedback recorded",
  "timestamp": "2024-01-15T10:45:00Z"
}
```

### GET /stats

Get suggestion engine statistics

**Response**:
```json
{
  "status": "success",
  "cached_recommendations": 15,
  "recommendation_weights": {
    "sustainability_score": 0.35,
    "user_preference_match": 0.30,
    "price_fit": 0.15,
    "popularity": 0.10,
    "novelty": 0.10
  },
  "timestamp": "2024-01-15T10:45:00Z"
}
```

---

## Error Responses

All agents follow the same error response format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

### Common HTTP Status Codes

- `200` - Success
- `400` - Bad Request (invalid input)
- `404` - Not Found (resource doesn't exist)
- `500` - Internal Server Error

---

## Interactive API Documentation

Each agent provides interactive API documentation via Swagger UI:

- Brand Data Collector: http://localhost:5001/docs
- Rating Calculator: http://localhost:5002/docs
- User Behavior Tracker: http://localhost:5003/docs
- Suggestion Agent: http://localhost:5004/docs

