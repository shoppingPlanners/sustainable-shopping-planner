"""
AI Rating Calculator Agent for Sustainable Shopping Planner
Analyzes product reviews and computes AI ratings based on sentiment and sustainability factors.
"""

import json
import requests
import re
from typing import Dict, List, Any
from dataclasses import dataclass
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ProductData:
    """Product information structure"""
    id: str
    name: str
    brand: str
    category: str
    price: float
    description: str
    sustainability_features: List[str]

@dataclass
class ReviewData:
    """Review information structure"""
    id: str
    product_id: str
    user_id: str
    rating: int
    text: str
    date: str

@dataclass
class AIRating:
    """AI Rating result structure"""
    product_id: str
    overall_rating: float
    sentiment_score: float
    sustainability_score: float
    confidence: float
    breakdown: Dict[str, Any]
    timestamp: str

class SentimentAnalyzer:
    """Analyzes sentiment in review text"""
    
    def __init__(self):
        # Simple keyword-based sentiment analysis
        self.positive_words = [
            'excellent', 'amazing', 'great', 'wonderful', 'fantastic', 'love', 'perfect',
            'outstanding', 'superb', 'brilliant', 'exceptional', 'impressive', 'satisfied',
            'happy', 'pleased', 'recommend', 'quality', 'durable', 'comfortable'
        ]
        self.negative_words = [
            'terrible', 'awful', 'horrible', 'disappointed', 'hate', 'worst', 'bad',
            'poor', 'cheap', 'uncomfortable', 'broke', 'defective', 'waste', 'regret',
            'unhappy', 'frustrated', 'annoyed', 'disgusted', 'useless'
        ]
        self.sustainability_keywords = [
            'eco-friendly', 'sustainable', 'organic', 'recycled', 'biodegradable',
            'carbon-neutral', 'green', 'environmentally', 'ethical', 'fair-trade',
            'natural', 'renewable', 'compostable', 'zero-waste', 'conscious'
        ]
    
    def analyze_sentiment(self, text: str) -> float:
        """Analyze sentiment score from -1 (negative) to 1 (positive)"""
        text_lower = text.lower()
        
        positive_count = sum(1 for word in self.positive_words if word in text_lower)
        negative_count = sum(1 for word in self.negative_words if word in text_lower)
        
        total_words = len(text.split())
        if total_words == 0:
            return 0.0
        
        sentiment_score = (positive_count - negative_count) / total_words
        return max(-1.0, min(1.0, sentiment_score))
    
    def extract_sustainability_mentions(self, text: str) -> List[str]:
        """Extract sustainability-related mentions from text"""
        text_lower = text.lower()
        mentions = []
        
        for keyword in self.sustainability_keywords:
            if keyword in text_lower:
                mentions.append(keyword)
        
        return mentions

class SustainabilityAnalyzer:
    """Analyzes sustainability aspects of products and brands"""
    
    def __init__(self):
        self.sustainability_criteria = {
            'materials': ['organic', 'recycled', 'sustainable', 'natural', 'biodegradable'],
            'production': ['fair-trade', 'ethical', 'local', 'carbon-neutral'],
            'packaging': ['recyclable', 'minimal', 'biodegradable', 'reusable'],
            'brand_values': ['b-corp', 'certified', 'transparent', 'responsible']
        }
    
    def analyze_product_sustainability(self, product: ProductData) -> float:
        """Analyze product sustainability score (0-1)"""
        score = 0.0
        total_criteria = 0
        
        # Check materials
        materials_score = self._check_criteria(product.description, 
                                                   self.sustainability_criteria['materials'])
        score += materials_score
        total_criteria += 1
        
        # Check production practices
        production_score = self._check_criteria(product.description,
                                               self.sustainability_criteria['production'])
        score += production_score
        total_criteria += 1
        
        # Check sustainability features
        if product.sustainability_features:
            feature_score = len(product.sustainability_features) / 5.0  # Max 5 features
            score += min(1.0, feature_score)
        total_criteria += 1
        
        return score / total_criteria if total_criteria > 0 else 0.0
    
    def _check_criteria(self, text: str, criteria: List[str]) -> float:
        """Check how many criteria are met in text"""
        text_lower = text.lower()
        matches = sum(1 for criterion in criteria if criterion in text_lower)
        return min(1.0, matches / len(criteria))

class RatingCalculator:
    """Main rating calculator that combines sentiment and sustainability analysis"""
    
    def __init__(self):
        self.sentiment_analyzer = SentimentAnalyzer()
        self.sustainability_analyzer = SustainabilityAnalyzer()
    
    def calculate_rating(self, product: ProductData, reviews: List[ReviewData]) -> AIRating:
        """Calculate AI rating based on product data and reviews"""
        
        # Analyze sentiment from reviews
        sentiment_scores = []
        sustainability_mentions = []
        
        for review in reviews:
            sentiment = self.sentiment_analyzer.analyze_sentiment(review.text)
            sentiment_scores.append(sentiment)
            
            mentions = self.sentiment_analyzer.extract_sustainability_mentions(review.text)
            sustainability_mentions.extend(mentions)
        
        # Calculate average sentiment
        avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0.0
        
        # Analyze product sustainability
        sustainability_score = self.sustainability_analyzer.analyze_product_sustainability(product)
        
        # Calculate overall rating (weighted combination)
        # 60% sentiment, 40% sustainability
        overall_rating = (avg_sentiment * 0.6 + sustainability_score * 0.4)
        
        # Convert to 1-5 scale
        overall_rating = max(1.0, min(5.0, (overall_rating + 1) * 2.5))
        
        # Calculate confidence based on number of reviews and sustainability mentions
        confidence = min(1.0, len(reviews) / 10.0 + len(set(sustainability_mentions)) / 10.0)
        
        # Create breakdown
        breakdown = {
            'sentiment_analysis': {
                'average_sentiment': avg_sentiment,
                'total_reviews': len(reviews),
                'positive_reviews': len([s for s in sentiment_scores if s > 0.1]),
                'negative_reviews': len([s for s in sentiment_scores if s < -0.1])
            },
            'sustainability_analysis': {
                'product_sustainability': sustainability_score,
                'sustainability_mentions': list(set(sustainability_mentions)),
                'mention_count': len(sustainability_mentions)
            },
            'rating_weights': {
                'sentiment_weight': 0.6,
                'sustainability_weight': 0.4
            }
        }
        
        return AIRating(
            product_id=product.id,
            overall_rating=round(overall_rating, 1),
            sentiment_score=round(avg_sentiment, 2),
            sustainability_score=round(sustainability_score, 2),
            confidence=round(confidence, 2),
            breakdown=breakdown,
            timestamp=str(pd.Timestamp.now())
        )

class RatingAgent:
    """Main AI Agent for rating calculation"""
    
    def __init__(self, backend_url: str = "http://localhost:3000"):
        self.backend_url = backend_url
        self.calculator = RatingCalculator()
    
    def fetch_product_data(self, product_id: str) -> ProductData:
        """Fetch product data from backend"""
        try:
            response = requests.get(f"{self.backend_url}/api/products/{product_id}")
            response.raise_for_status()
            data = response.json()
            
            return ProductData(
                id=data['id'],
                name=data['name'],
                brand=data['brand'],
                category=data['category'],
                price=data['price'],
                description=data['description'],
                sustainability_features=data.get('sustainability_features', [])
            )
        except Exception as e:
            logger.error(f"Error fetching product data: {e}")
            raise
    
    def fetch_reviews(self, product_id: str) -> List[ReviewData]:
        """Fetch reviews for a product from backend"""
        try:
            response = requests.get(f"{self.backend_url}/api/products/{product_id}/reviews")
            response.raise_for_status()
            reviews_data = response.json()
            
            reviews = []
            for review_data in reviews_data:
                reviews.append(ReviewData(
                    id=review_data['id'],
                    product_id=review_data['product_id'],
                    user_id=review_data['user_id'],
                    rating=review_data['rating'],
                    text=review_data['text'],
                    date=review_data['date']
                ))
            
            return reviews
        except Exception as e:
            logger.error(f"Error fetching reviews: {e}")
            raise
    
    def calculate_product_rating(self, product_id: str) -> AIRating:
        """Main method to calculate AI rating for a product"""
        logger.info(f"Calculating AI rating for product {product_id}")
        
        # Fetch product and review data
        product = self.fetch_product_data(product_id)
        reviews = self.fetch_reviews(product_id)
        
        # Calculate rating
        rating = self.calculator.calculate_rating(product, reviews)
        
        logger.info(f"AI Rating calculated: {rating.overall_rating}/5.0")
        return rating
    
    def save_rating(self, rating: AIRating) -> bool:
        """Save calculated rating to backend"""
        try:
            response = requests.post(
                f"{self.backend_url}/api/ratings",
                json={
                    'product_id': rating.product_id,
                    'ai_rating': rating.overall_rating,
                    'sentiment_score': rating.sentiment_score,
                    'sustainability_score': rating.sustainability_score,
                    'confidence': rating.confidence,
                    'breakdown': rating.breakdown,
                    'timestamp': rating.timestamp
                }
            )
            response.raise_for_status()
            logger.info(f"Rating saved successfully for product {rating.product_id}")
            return True
        except Exception as e:
            logger.error(f"Error saving rating: {e}")
            return False

def main():
    """Main function to run the rating agent"""
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python app.py <product_id>")
        sys.exit(1)
    
    product_id = sys.argv[1]
    agent = RatingAgent()
    
    try:
        # Calculate rating
        rating = agent.calculate_product_rating(product_id)
        
        # Save rating
        success = agent.save_rating(rating)
        
        if success:
            print(f"✅ AI Rating calculated and saved: {rating.overall_rating}/5.0")
            print(f"📊 Sentiment Score: {rating.sentiment_score}")
            print(f"🌱 Sustainability Score: {rating.sustainability_score}")
            print(f"🎯 Confidence: {rating.confidence}")
        else:
            print("❌ Failed to save rating")
            
    except Exception as e:
        logger.error(f"Error in main: {e}")
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    import pandas as pd
    main()
