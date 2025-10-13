# System Workflow

This document explains how the 4 agents work together to provide personalized sustainable shopping recommendations.

## Overview

The Sustainable Shopping Planner consists of 4 specialized AI agents that work together:

```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                 │
│                  (Frontend Interface)                        │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   │ HTTP Requests
                   │
┌──────────────────▼──────────────────────────────────────────┐
│                                                              │
│              AGENT 4: Suggestion Agent                       │
│     (Generates Personalized Recommendations)                 │
│                                                              │
└─┬────────────────┬───────────────────┬──────────────────────┘
  │                │                   │
  │                │                   │
  │ Get            │ Get               │ Get
  │ Products       │ Ratings           │ User Data
  │                │                   │
  │                │                   │
┌─▼──────────┐  ┌─▼──────────┐  ┌────▼─────────┐
│            │  │            │  │              │
│  AGENT 1   │──│  AGENT 2   │  │   AGENT 3    │
│  Brand     │  │  Rating    │  │   User       │
│  Data      │  │  Calculator│  │   Behavior   │
│  Collector │  │            │  │   Tracker    │
│            │  │            │  │              │
└────────────┘  └────────────┘  └──────────────┘
     │                │                │
     │                │                │
     │ Scrapes        │ Calculates     │ Tracks
     │ Websites       │ Scores         │ Events
     │                │                │
     ▼                ▼                ▼
  [Brands]        [Ratings]        [Events]
```

## Workflow Steps

### 1. Data Collection (Agent 1: Brand Data Collector)

**Trigger**: Admin or scheduled job

**Process**:
1. Receives a URL to scrape (brand website)
2. Fetches the webpage content
3. Extracts:
   - Product information (name, price, URL, category)
   - Sustainability commitments
   - Certifications
   - Brand information
4. Stores the data
5. **Notifies Agent 2** with the collected data

**Example**:
```bash
POST /scrape
{
  "url": "https://sustainablebrand.com/products"
}
```

**Output**:
```json
{
  "brand_name": "EcoBrand",
  "products": [{"name": "Organic T-Shirt", ...}],
  "sustainability_commitments": ["Carbon neutral by 2030"],
  "certifications": ["B-Corp", "Fair Trade"]
}
```

---

### 2. Rating Calculation (Agent 2: Rating Calculator)

**Trigger**: Receives data from Agent 1

**Process**:
1. Receives brand data
2. Analyzes sustainability commitments using keyword matching
3. Assigns scores for certifications
4. Calculates:
   - Environmental score (40% weight)
   - Social score (35% weight)
   - Economic score (25% weight)
5. Computes overall sustainability rating (0-100)
6. Generates confidence score
7. Stores the rating

**Scoring Factors**:

**Environmental (40%)**:
- Carbon neutrality commitments (+10 points)
- Renewable energy use (+8 points)
- Zero waste initiatives (+8 points)
- Sustainable materials (+3 points per keyword)
- Environmental certifications (varies by cert)

**Social (35%)**:
- Fair trade practices (+8 points)
- Worker rights commitments (+8 points)
- Living wage policy (+10 points)
- Social certifications (B-Corp: +12 points)

**Economic (25%)**:
- Durability/quality focus (+8 points)
- Local sourcing (+7 points)
- Repair programs (+8 points)
- Fair pricing indicators (+5 points)

**Grade Scale**:
- A+ (90-100): Exceptional sustainability
- A (85-89): Excellent sustainability
- B (70-84): Good sustainability
- C (50-69): Moderate sustainability
- D (40-49): Below average
- F (0-39): Poor sustainability

---

### 3. User Behavior Tracking (Agent 3: User Behavior Tracker)

**Trigger**: User actions on the platform

**Process**:
1. Receives user events (view, search, click, purchase)
2. Stores events in database
3. Analyzes patterns:
   - Category preferences
   - Brand preferences
   - Sustainability interests
   - Price sensitivity
   - Shopping frequency
4. Calculates sustainability score (0-100)
5. Generates personalized insights

**Tracked Events**:
- `view` - User views a product
- `search` - User searches for products
- `click` - User clicks on a product
- `purchase` - User purchases a product
- `add_to_cart` - User adds product to cart
- `favorite` - User favorites a product

**Pattern Types**:
- `category_preference` - Preferred product categories
- `brand_preference` - Preferred brands
- `sustainability_focus` - Sustainability interests
- `price_sensitive` - Price sensitivity level
- `shopping_frequency` - How often user shops

**Sustainability Score Calculation**:
```python
sustainability_score = (sustainability_events / total_events) * 100

# With purchase weighting:
score = base_score * 0.7 + purchase_score * 0.3
```

---

### 4. Recommendation Generation (Agent 4: Suggestion Agent)

**Trigger**: User requests suggestions

**Process**:
1. Receives suggestion request with user_id
2. **Fetches user data from Agent 3**:
   - Sustainability score
   - Preferred categories
   - Preferred brands
   - Sustainability interests
   - Average price point
   - Viewed products/categories
3. **Fetches products from Agent 1**:
   - All available products
4. **Fetches ratings from Agent 2**:
   - Sustainability scores for brands
5. **Calculates recommendation score** for each product:
   ```
   recommendation_score = 
     sustainability_score     × 0.35 +
     user_preference_match    × 0.30 +
     price_fit               × 0.15 +
     popularity              × 0.10 +
     novelty                 × 0.10
   ```
6. Filters products (score > 0.3 threshold)
7. Sorts by recommendation score
8. **Diversifies results**:
   - Max 3 products per brand
   - Max 4 products per category
9. Returns top N suggestions with reasons

**Recommendation Score Components**:

1. **Sustainability Score (35%)**:
   ```
   sustainability_score / 100
   ```

2. **User Preference Match (30%)**:
   - Category match: +0.4
   - Brand match: +0.3
   - Sustainability interests match: up to +0.3

3. **Price Fit (15%)**:
   - How close to user's average price
   - Distance from average reduces score

4. **Popularity (10%)**:
   - Based on view/purchase counts
   - (Currently simplified)

5. **Novelty (10%)**:
   - Not yet viewed: +0.5
   - New category: +0.8
   - Already viewed: 0.0

**Reason Generation**:
The system generates human-readable explanations:
- "Excellent sustainability rating (86/100)"
- "Matches your favorite categories"
- "Features: organic, fair-trade"
- "Certified: B-Corp, Fair Trade"
- "Within your typical budget"
- "Popular among conscious shoppers"
- "Discover something new"

---

## Complete User Journey Example

### Step 1: User Discovers the Platform

```
User: "I want to shop sustainably"
```

### Step 2: User Browses Products

```bash
# User views a product
POST /track
{
  "user_id": "alice",
  "event_type": "view",
  "product_id": "organic-tshirt-1",
  "category": "clothing",
  "tags": ["organic", "fair-trade"]
}
```

### Step 3: User Searches for Specific Items

```bash
# User searches
POST /track
{
  "user_id": "alice",
  "event_type": "search",
  "keywords": ["organic", "cotton", "shirt"],
  "tags": ["organic", "sustainable"]
}
```

### Step 4: System Analyzes Behavior

Agent 3 detects patterns:
- Alice prefers organic products
- Alice is interested in clothing
- Alice values sustainability

### Step 5: User Requests Recommendations

```bash
GET /suggestions/alice?limit=5
```

Agent 4 process:
1. Fetches Alice's data: sustainability_score=75, prefers organic+fair-trade
2. Fetches all products with ratings
3. Calculates scores:
   - Product A (organic tshirt): 0.89 → Top match!
   - Product B (recycled jeans): 0.85 → Great match
   - Product C (regular dress): 0.42 → Lower match
4. Returns top 5 with explanations

### Step 6: User Receives Personalized Suggestions

```json
{
  "suggestions": [
    {
      "product_name": "Organic Cotton T-Shirt",
      "sustainability_score": 86,
      "recommendation_score": 0.89,
      "reasons": [
        "Matches your sustainability preferences",
        "Features: organic, fair-trade",
        "Excellent rating (86/100)"
      ]
    }
  ]
}
```

### Step 7: User Provides Feedback

```bash
# User clicks on suggestion
POST /feedback
{
  "user_id": "alice",
  "product_id": "organic-tshirt-1",
  "feedback_type": "clicked"
}
```

This feedback:
- Updates Alice's behavior profile
- Clears recommendation cache
- Influences future suggestions

---

## Data Flow

### Forward Flow (Data Collection → Recommendation)

```
1. Brand Website
        ↓
2. Agent 1 scrapes
        ↓
3. Brand Data stored
        ↓
4. Agent 2 receives notification
        ↓
5. Agent 2 calculates rating
        ↓
6. Rating stored
        ↓
7. User requests suggestions
        ↓
8. Agent 4 queries Agent 1 & 2
        ↓
9. Agent 4 queries Agent 3
        ↓
10. Agent 4 generates recommendations
```

### Feedback Loop (User Actions → Improved Recommendations)

```
1. User interacts with suggestions
        ↓
2. Agent 3 tracks events
        ↓
3. Agent 3 updates behavior patterns
        ↓
4. Agent 4 uses updated patterns
        ↓
5. Better personalized suggestions
```

---

## Performance Optimization

### Caching Strategy

1. **Agent 1**: Caches scraped data for 1 hour
2. **Agent 2**: Stores ratings persistently
3. **Agent 3**: Real-time event storage
4. **Agent 4**: Caches recommendations for 1 hour per user

### Async Communication

- Agent 1 → Agent 2: Background notification
- Agent 4 → Agents 1, 2, 3: Parallel requests
- All agents use async HTTP clients

### Database Strategy

- **Files** (development): JSON files for quick start
- **MongoDB** (production): User events and analytics
- **PostgreSQL** (production): Structured data (products, ratings)
- **Redis** (production): Caching and session storage

---

## Scalability Considerations

1. **Horizontal Scaling**: Each agent can run multiple instances
2. **Load Balancing**: Use nginx or traefik for agent load balancing
3. **Database Sharding**: Shard by user_id for behavior data
4. **Message Queue**: Use RabbitMQ/Kafka for agent communication in production
5. **CDN**: Cache static product images and data

---

## Monitoring & Health Checks

Each agent exposes:
- `/health` - Health status
- `/` - Agent information
- `/docs` - API documentation

Recommended monitoring:
- Response times
- Error rates
- Agent connectivity
- Cache hit rates
- Recommendation quality metrics

