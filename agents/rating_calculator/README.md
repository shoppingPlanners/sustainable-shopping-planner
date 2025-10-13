# AI Rating Calculator Agent

This AI agent analyzes product reviews and calculates AI-powered sustainability ratings for the Sustainable Shopping Planner.

## 🌟 Features

- **Sentiment Analysis**: Analyzes customer review sentiment using keyword-based scoring
- **Sustainability Analysis**: Evaluates product sustainability based on materials, production, and features
- **AI Rating Calculation**: Combines sentiment and sustainability scores into an overall rating
- **Confidence Scoring**: Provides confidence levels based on review quantity and sustainability mentions
- **Detailed Breakdown**: Offers comprehensive analysis breakdown for transparency

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+ (for backend communication)
- Backend server running on port 3000

### Installation

1. **Install Python dependencies:**
   ```bash
   cd agents/rating_calculator
   python setup.py
   ```

2. **Start the backend server:**
   ```bash
   cd ../../backend
   npm install
   npm start
   ```

3. **Test the AI agent:**
   ```bash
   cd agents/rating_calculator
   python app.py 1
   ```

## 📊 How It Works

### 1. Review Submission Flow
```
User submits review → Backend stores review → Backend triggers AI agent
```

### 2. AI Analysis Process
```
AI Agent fetches product + reviews → Sentiment analysis → Sustainability analysis → Rating calculation
```

### 3. Rating Components

#### Sentiment Analysis
- Analyzes review text for positive/negative keywords
- Calculates sentiment score from -1 (negative) to +1 (positive)
- Considers review quantity and distribution

#### Sustainability Analysis
- Evaluates product description for sustainability features
- Checks for eco-friendly materials and practices
- Analyzes sustainability mentions in reviews

#### Overall Rating
- **Formula**: `(sentiment_score * 0.6) + (sustainability_score * 0.4)`
- **Scale**: 1.0 to 5.0 stars
- **Confidence**: Based on review count and sustainability mentions

## 🔧 API Integration

### Backend Endpoints Used
- `GET /api/products/{id}` - Fetch product data
- `GET /api/products/{id}/reviews` - Fetch product reviews
- `POST /api/ratings` - Save calculated rating

### Triggering AI Analysis
The AI agent is automatically triggered when:
- A new review is submitted
- Manual trigger via API call

## 📈 Rating Breakdown

### Sentiment Analysis
```python
# Positive keywords: excellent, amazing, great, love, perfect...
# Negative keywords: terrible, awful, disappointed, hate, worst...
sentiment_score = (positive_count - negative_count) / total_words
```

### Sustainability Analysis
```python
# Criteria categories:
# - Materials: organic, recycled, sustainable, natural
# - Production: fair-trade, ethical, local, carbon-neutral
# - Features: sustainability_features array
sustainability_score = sum(criteria_scores) / total_criteria
```

### Confidence Calculation
```python
confidence = min(1.0, (review_count / 10.0) + (sustainability_mentions / 10.0))
```

## 🎯 Example Output

```json
{
  "product_id": "1",
  "ai_rating": 4.6,
  "sentiment_score": 0.8,
  "sustainability_score": 0.9,
  "confidence": 0.85,
  "breakdown": {
    "sentiment_analysis": {
      "average_sentiment": 0.8,
      "total_reviews": 5,
      "positive_reviews": 4,
      "negative_reviews": 1
    },
    "sustainability_analysis": {
      "product_sustainability": 0.9,
      "sustainability_mentions": ["eco-friendly", "organic", "carbon-neutral"],
      "mention_count": 3
    }
  }
}
```

## 🛠️ Development

### Adding New Sustainability Keywords
Edit the `sustainability_keywords` list in `SentimentAnalyzer`:

```python
self.sustainability_keywords = [
    'eco-friendly', 'sustainable', 'organic', 'recycled',
    'biodegradable', 'carbon-neutral', 'green', 'environmentally',
    'ethical', 'fair-trade', 'natural', 'renewable',
    'compostable', 'zero-waste', 'conscious'
]
```

### Adjusting Rating Weights
Modify the weights in `RatingCalculator.calculate_rating()`:

```python
# Current: 60% sentiment, 40% sustainability
overall_rating = (avg_sentiment * 0.6 + sustainability_score * 0.4)
```

### Testing
```bash
# Test with specific product
python app.py 1

# Test with different products
python app.py 2
python app.py 3
```

## 🔍 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   pip install -r requirements.txt
   ```

2. **Backend Connection Failed**
   - Ensure backend server is running on port 3000
   - Check network connectivity

3. **Product Not Found**
   - Verify product ID exists in backend
   - Check backend API endpoints

### Debug Mode
Set logging level to DEBUG for detailed output:

```python
logging.basicConfig(level=logging.DEBUG)
```

## 📝 License

This project is part of the Sustainable Shopping Planner and follows the same MIT license.
