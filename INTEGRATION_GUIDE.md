# Integration Guide

This guide explains how all 4 agents work together as an integrated system and how to use them effectively.

## System Architecture

The Sustainable Shopping Planner consists of 4 autonomous agents that communicate via REST APIs:

### Agent 1: Brand Data Collector (Port 5001)
- **Role**: Data acquisition
- **Responsibilities**:
  - Scrapes brand websites
  - Extracts product information
  - Identifies sustainability commitments
  - Detects certifications
- **Outputs to**: Agent 2 (Rating Calculator)

### Agent 2: Rating Calculator (Port 5002)
- **Role**: Sustainability assessment
- **Responsibilities**:
  - Calculates environmental scores
  - Calculates social scores
  - Calculates economic scores
  - Assigns overall rating (0-100)
  - Generates grade (A+ to F)
- **Inputs from**: Agent 1 (Brand Data Collector)
- **Outputs to**: Agent 4 (Suggestion Agent)

### Agent 3: User Behavior Tracker (Port 5003)
- **Role**: User analytics
- **Responsibilities**:
  - Tracks user events
  - Identifies behavior patterns
  - Calculates sustainability engagement
  - Generates insights
- **Outputs to**: Agent 4 (Suggestion Agent)

### Agent 4: Suggestion Agent (Port 5004)
- **Role**: Recommendation engine
- **Responsibilities**:
  - Generates personalized suggestions
  - Ranks products by relevance
  - Provides explanation for recommendations
  - Handles feedback
- **Inputs from**: Agents 1, 2, and 3
- **Outputs to**: Frontend/Users

## Communication Flow

### Data Collection Flow
```
Admin → Agent 1 (scrape) → Brand Data → Agent 2 (calculate) → Rating
```

### Recommendation Flow
```
User → Agent 4 (request) →
    ↓
    ├→ Agent 1 (get products)
    ├→ Agent 2 (get ratings)
    └→ Agent 3 (get user data)
    ↓
Agent 4 (generate) → Suggestions → User
```

### Feedback Loop
```
User → Agent 4 (feedback) → Agent 3 (track) → Updated Patterns
```

## Integration Patterns

### Pattern 1: Async Background Processing

Agent 1 notifies Agent 2 in the background:

```python
# In Agent 1 (Brand Data Collector)
async def scrape_brand(url: str):
    brand_data = await scraper.scrape(url)
    
    # Store locally
    store_brand_data(brand_data)
    
    # Notify Agent 2 in background
    background_tasks.add_task(notify_rating_calculator, brand_data)
    
    return brand_data

async def notify_rating_calculator(brand_data):
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{RATING_CALCULATOR_URL}/calculate",
            json=brand_data
        )
```

### Pattern 2: Parallel Data Fetching

Agent 4 fetches data in parallel:

```python
# In Agent 4 (Suggestion Agent)
async def generate_suggestions(user_id):
    # Fetch from all agents in parallel
    user_data_task = fetch_user_data(user_id)
    products_task = fetch_products()
    ratings_task = fetch_ratings()
    
    user_data, products, ratings = await asyncio.gather(
        user_data_task,
        products_task,
        ratings_task
    )
    
    # Generate recommendations
    return calculate_recommendations(user_data, products, ratings)
```

### Pattern 3: Caching for Performance

```python
# In Agent 4 (Suggestion Agent)
cache = {}

async def get_suggestions(user_id):
    cache_key = f"suggestions_{user_id}"
    
    # Check cache
    if cache_key in cache:
        cached_data, timestamp = cache[cache_key]
        if (datetime.now() - timestamp).seconds < 3600:  # 1 hour
            return cached_data
    
    # Generate fresh suggestions
    suggestions = await generate_suggestions(user_id)
    
    # Cache results
    cache[cache_key] = (suggestions, datetime.now())
    
    return suggestions
```

## Frontend Integration

### Basic Integration

```javascript
// React/Next.js example

// 1. Track user behavior
const trackEvent = async (event) => {
  await fetch('http://localhost:5003/track', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_id: userId,
      event_type: event.type,
      product_id: event.productId,
      category: event.category,
      tags: event.tags
    })
  });
};

// 2. Get personalized suggestions
const getSuggestions = async (userId) => {
  const response = await fetch(
    `http://localhost:5004/suggestions/${userId}?limit=10`
  );
  const data = await response.json();
  return data.suggestions;
};

// 3. Display suggestions
function SuggestionsPage({ userId }) {
  const [suggestions, setSuggestions] = useState([]);
  
  useEffect(() => {
    getSuggestions(userId).then(setSuggestions);
  }, [userId]);
  
  const handleProductClick = (product) => {
    // Track click
    trackEvent({
      type: 'click',
      productId: product.product_id,
      category: product.category,
      tags: ['sustainable']
    });
    
    // Submit feedback
    fetch('http://localhost:5004/feedback', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: userId,
        product_id: product.product_id,
        feedback_type: 'clicked'
      })
    });
    
    // Navigate to product
    router.push(`/products/${product.product_id}`);
  };
  
  return (
    <div>
      <h1>Sustainable Recommendations for You</h1>
      {suggestions.map(product => (
        <ProductCard
          key={product.product_id}
          product={product}
          onClick={() => handleProductClick(product)}
        />
      ))}
    </div>
  );
}
```

### Advanced: Real-time Recommendations

```javascript
// Stream recommendations as user browses
function useRealtimeRecommendations(userId) {
  const [recommendations, setRecommendations] = useState([]);
  
  useEffect(() => {
    const updateRecommendations = async () => {
      const suggestions = await getSuggestions(userId);
      setRecommendations(suggestions);
    };
    
    // Update every 5 minutes
    const interval = setInterval(updateRecommendations, 300000);
    
    // Initial load
    updateRecommendations();
    
    return () => clearInterval(interval);
  }, [userId]);
  
  return recommendations;
}
```

## Mobile App Integration

### Flutter Example

```dart
class SuggestionService {
  static const baseUrl = 'http://localhost:5004';
  
  Future<List<Product>> getSuggestions(String userId, {int limit = 10}) async {
    final response = await http.get(
      Uri.parse('$baseUrl/suggestions/$userId?limit=$limit'),
    );
    
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return (data['suggestions'] as List)
          .map((json) => Product.fromJson(json))
          .toList();
    }
    
    throw Exception('Failed to load suggestions');
  }
  
  Future<void> trackEvent(TrackingEvent event) async {
    await http.post(
      Uri.parse('http://localhost:5003/track'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode(event.toJson()),
    );
  }
}
```

## Backend API Integration

### Unified API Gateway (Optional)

You can create a unified API gateway that wraps all agents:

```python
from fastapi import FastAPI
import httpx

app = FastAPI()

class UnifiedAPI:
    def __init__(self):
        self.client = httpx.AsyncClient()
        self.agents = {
            'brand_collector': 'http://localhost:5001',
            'rating_calculator': 'http://localhost:5002',
            'user_behavior': 'http://localhost:5003',
            'suggestion': 'http://localhost:5004'
        }
    
    async def get_suggestions(self, user_id: str):
        response = await self.client.get(
            f"{self.agents['suggestion']}/suggestions/{user_id}"
        )
        return response.json()
    
    async def track_event(self, event_data: dict):
        response = await self.client.post(
            f"{self.agents['user_behavior']}/track",
            json=event_data
        )
        return response.json()
    
    async def get_brand_info(self, brand_name: str):
        # Get brand data
        brand_response = await self.client.get(
            f"{self.agents['brand_collector']}/brands/{brand_name}"
        )
        brand_data = brand_response.json()
        
        # Get rating
        rating_response = await self.client.get(
            f"{self.agents['rating_calculator']}/ratings/{brand_name}"
        )
        rating_data = rating_response.json()
        
        # Combine
        return {
            **brand_data,
            'rating': rating_data
        }

api = UnifiedAPI()

@app.get("/api/suggestions/{user_id}")
async def get_suggestions(user_id: str):
    return await api.get_suggestions(user_id)

@app.post("/api/track")
async def track_event(event: dict):
    return await api.track_event(event)

@app.get("/api/brands/{brand_name}")
async def get_brand(brand_name: str):
    return await api.get_brand_info(brand_name)
```

## Error Handling

### Graceful Degradation

```python
async def get_suggestions_with_fallback(user_id: str):
    try:
        # Try to get user data
        user_data = await fetch_user_data(user_id)
    except:
        # Fallback to default user profile
        user_data = get_default_user_profile()
    
    try:
        # Try to get products with ratings
        products = await fetch_products_with_ratings()
    except:
        # Fallback to cached products
        products = get_cached_products()
    
    # Generate suggestions even with partial data
    return generate_suggestions(user_data, products)
```

### Retry Logic

```python
async def fetch_with_retry(url: str, max_retries: int = 3):
    for attempt in range(max_retries):
        try:
            response = await http_client.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
```

## Monitoring & Observability

### Health Check Aggregation

```python
@app.get("/health/all")
async def check_all_agents():
    agents = {
        'brand_collector': 'http://localhost:5001',
        'rating_calculator': 'http://localhost:5002',
        'user_behavior': 'http://localhost:5003',
        'suggestion': 'http://localhost:5004'
    }
    
    results = {}
    
    for name, url in agents.items():
        try:
            response = await http_client.get(f"{url}/health", timeout=5.0)
            results[name] = {
                'status': 'healthy' if response.status_code == 200 else 'unhealthy',
                'response_time': response.elapsed.total_seconds()
            }
        except Exception as e:
            results[name] = {
                'status': 'down',
                'error': str(e)
            }
    
    overall_healthy = all(r['status'] == 'healthy' for r in results.values())
    
    return {
        'overall_status': 'healthy' if overall_healthy else 'degraded',
        'agents': results
    }
```

## Best Practices

1. **Always track user events** for better recommendations
2. **Cache aggressively** but invalidate on feedback
3. **Handle failures gracefully** with fallbacks
4. **Monitor agent health** continuously
5. **Use async operations** for better performance
6. **Implement retry logic** for inter-agent communication
7. **Version your APIs** for backward compatibility
8. **Log all inter-agent communication** for debugging
9. **Rate limit** API calls to prevent abuse
10. **Secure** agent-to-agent communication in production

## Deployment Considerations

### Production Setup

1. **Use a message queue** (RabbitMQ/Kafka) for async communication
2. **Deploy behind a load balancer** (nginx/traefik)
3. **Use service discovery** (Consul/etcd) for agent URLs
4. **Implement circuit breakers** (e.g., using resilience4j)
5. **Add API authentication** (JWT tokens)
6. **Enable HTTPS** for all communication
7. **Set up monitoring** (Prometheus + Grafana)
8. **Configure logging** (ELK stack or similar)

### Kubernetes Deployment

```yaml
# Example deployment for Agent 1
apiVersion: apps/v1
kind: Deployment
metadata:
  name: brand-collector
spec:
  replicas: 3
  selector:
    matchLabels:
      app: brand-collector
  template:
    metadata:
      labels:
        app: brand-collector
    spec:
      containers:
      - name: brand-collector
        image: sustainable-shopping/brand-collector:latest
        ports:
        - containerPort: 5001
        env:
        - name: RATING_CALCULATOR_URL
          value: "http://rating-calculator-service:5002"
        resources:
          limits:
            cpu: "500m"
            memory: "512Mi"
---
apiVersion: v1
kind: Service
metadata:
  name: brand-collector-service
spec:
  selector:
    app: brand-collector
  ports:
  - port: 5001
    targetPort: 5001
```

## Troubleshooting

### Common Issues

1. **Agent can't reach another agent**
   - Check URLs in `.env`
   - Verify all agents are running
   - Check firewall rules

2. **Slow recommendations**
   - Enable caching
   - Use parallel requests
   - Optimize database queries

3. **Inaccurate recommendations**
   - Ensure sufficient user behavior data
   - Verify ratings are calculated correctly
   - Adjust recommendation weights

4. **Memory issues**
   - Clear old cache entries
   - Limit event history retention
   - Use database pagination

## Support

For integration help:
- See `docs/API_REFERENCE.md` for detailed API documentation
- Check `docs/WORKFLOW.md` for system architecture
- Review `QUICKSTART.md` for setup instructions

