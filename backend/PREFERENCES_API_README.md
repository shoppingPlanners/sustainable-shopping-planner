# Preferences & Recommendations API

This document explains the new preferences and recommendations functionality that connects the frontend home page with the backend.

## New API Endpoints

### 1. Save User Preferences
```
POST /api/preferences/save
```

**Request Body:**
```json
{
  "category": "tops",
  "budget": "50-100", 
  "style": "casual",
  "sustainability_priorities": "organic materials",
  "size": "M"
}
```

**Response:**
```json
{
  "success": true,
  "preferences_id": "68ea4801e0c2056078a77ebb",
  "message": "Preferences saved successfully"
}
```

### 2. Get Personalized Recommendations
```
GET /api/preferences/recommendations?category=tops&budget=50-100&style=casual
```

**Query Parameters:**
- `category` (optional): tops, bottoms, dresses, outerwear, activewear
- `budget` (optional): under-50, 50-100, 100-200, 200-plus
- `style` (optional): casual, professional, trendy, minimalist, bohemian
- `sustainability_priorities` (optional): text describing priorities
- `size` (optional): size preference
- `limit` (optional): number of recommendations (default: 10)

**Response:**
```json
[
  {
    "id": "68ea3da3def3a44b1d099322",
    "name": "Sustainable Product 12",
    "brand": "People Tree",
    "rating": 4.1,
    "sustainabilityScore": 92,
    "price": "$54",
    "image": "/sustainable-product-12.jpg",
    "buyUrl": "https://example12.com",
    "features": ["Inclusive Sizing", "Low Water Usage", "Upcycled Fabric"],
    "category": "tops",
    "match_score": 75.0,
    "reason": "Matches your preferred category; Fits your budget; Exceptional sustainability rating"
  }
]
```

### 3. Get Recent Preferences
```
GET /api/preferences/recent
```

Returns the most recently saved user preferences.

## Frontend Integration

The home page (`/frontend/app/page.tsx`) now includes:

1. **Interactive Form**: Users can select preferences for category, budget, style, sustainability priorities, and size
2. **Real-time State Management**: Form data is managed with React state
3. **API Integration**: Form submission saves preferences and fetches personalized recommendations
4. **Recommendations Display**: Shows personalized product recommendations with match scores and reasons
5. **Loading States**: Proper loading indicators and error handling
6. **Analytics Tracking**: Form submissions are tracked for analytics

## Recommendation Algorithm

The recommendation system scores items based on:

- **Category Match** (30 points): Exact category match
- **Budget Match** (25 points): Price within selected budget range
- **Sustainability Match** (20 points): Features match user priorities
- **High Sustainability Score** (15 points): Items with 90%+ sustainability rating
- **User Rating** (10 points): Items with high user ratings

Items are ranked by total score and returned with match percentages and explanations.

## Database Collections

- `item`: Contains all product data (existing)
- `user_preferences`: Stores user preference submissions with timestamps

## Testing

1. **Start the backend**:
   ```bash
   cd backend
   python -m uvicorn src.main:app --reload --port 8000
   ```

2. **Start the frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

3. **Visit** `http://localhost:3000` and fill out the preferences form

4. **Test API directly**:
   ```bash
   # Save preferences
   curl -X POST "http://localhost:8000/api/preferences/save" \
     -H "Content-Type: application/json" \
     -d '{"category": "tops", "budget": "50-100"}'
   
   # Get recommendations
   curl "http://localhost:8000/api/preferences/recommendations?category=tops&budget=50-100"
   ```

## Features

- ✅ **Personalized Recommendations**: AI-powered matching based on user preferences
- ✅ **Match Scoring**: Items scored and ranked by relevance
- ✅ **Reason Explanations**: Clear explanations for why items are recommended
- ✅ **Real-time Form**: Interactive form with state management
- ✅ **Error Handling**: Proper error states and user feedback
- ✅ **Analytics Integration**: Form submissions tracked for insights
- ✅ **Responsive Design**: Works on all device sizes
