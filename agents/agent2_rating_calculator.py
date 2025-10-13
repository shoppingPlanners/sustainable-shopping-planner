"""
Agent 2: Rating Calculator
Calculates comprehensive sustainability scores for brands and products
"""

import logging
import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Rating Calculator Agent",
    description="Calculates sustainability ratings for brands and products",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
RATING_CALCULATOR_PORT = int(os.getenv("RATING_CALCULATOR_PORT", "5002"))
RATINGS_FILE = "ratings_data.json"

# Pydantic Models
class RatingRequest(BaseModel):
    brand_name: str
    products: List[Dict[str, Any]]
    sustainability_commitments: List[str]
    certifications: List[str]

class RatingResponse(BaseModel):
    brand_name: str
    overall_score: float
    environmental_score: float
    social_score: float
    economic_score: float
    confidence_score: float
    breakdown: Dict[str, Any]
    calculated_at: datetime

# In-memory storage
ratings_database = {}


class SustainabilityRatingEngine:
    """Calculates sustainability ratings based on multiple factors"""
    
    def __init__(self):
        # Scoring weights
        self.weights = {
            'environmental': 0.40,  # 40%
            'social': 0.35,         # 35%
            'economic': 0.25        # 25%
        }
        
        # Certification scores
        self.certification_scores = {
            'B-Corp': 15,
            'B Corporation': 15,
            'Fair Trade': 12,
            'Organic': 10,
            'GOTS': 12,
            'Cradle to Cradle': 13,
            'Bluesign': 11,
            'OEKO-TEX': 9,
            'FSC': 10,
            'Rainforest Alliance': 11,
            'Carbon Neutral': 14,
            'Climate Neutral': 14,
            'Leaping Bunny': 8,
            '1% for the Planet': 10
        }
        
        # Keywords for commitment analysis
        self.environmental_keywords = [
            'carbon neutral', 'renewable energy', 'zero waste', 'recycled',
            'sustainable materials', 'water conservation', 'biodegradable',
            'compostable', 'solar power', 'wind energy', 'emission reduction'
        ]
        
        self.social_keywords = [
            'fair trade', 'fair wages', 'worker rights', 'safe conditions',
            'community support', 'ethical sourcing', 'no child labor',
            'living wage', 'diversity', 'inclusion', 'gender equality'
        ]
        
        self.economic_keywords = [
            'transparent pricing', 'local sourcing', 'small business',
            'cooperative', 'profit sharing', 'fair prices', 'longevity',
            'durable', 'quality', 'warranty', 'repair program'
        ]
    
    def calculate_rating(self, brand_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate comprehensive sustainability rating"""
        
        logger.info(f"Calculating rating for {brand_data.get('brand_name')}")
        
        # Calculate individual component scores
        env_score = self._calculate_environmental_score(brand_data)
        social_score = self._calculate_social_score(brand_data)
        econ_score = self._calculate_economic_score(brand_data)
        
        # Calculate overall score
        overall_score = (
            env_score * self.weights['environmental'] +
            social_score * self.weights['social'] +
            econ_score * self.weights['economic']
        )
        
        # Calculate confidence score
        confidence = self._calculate_confidence(brand_data)
        
        # Detailed breakdown
        breakdown = {
            'environmental': {
                'score': env_score,
                'weight': self.weights['environmental'],
                'factors': self._get_environmental_factors(brand_data)
            },
            'social': {
                'score': social_score,
                'weight': self.weights['social'],
                'factors': self._get_social_factors(brand_data)
            },
            'economic': {
                'score': econ_score,
                'weight': self.weights['economic'],
                'factors': self._get_economic_factors(brand_data)
            },
            'certifications': self._analyze_certifications(brand_data.get('certifications', [])),
            'data_completeness': confidence
        }
        
        rating = {
            'brand_name': brand_data.get('brand_name', 'Unknown'),
            'overall_score': round(overall_score, 2),
            'environmental_score': round(env_score, 2),
            'social_score': round(social_score, 2),
            'economic_score': round(econ_score, 2),
            'confidence_score': round(confidence, 2),
            'breakdown': breakdown,
            'grade': self._score_to_grade(overall_score),
            'calculated_at': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Rating calculated: {overall_score:.2f}/100 (Grade: {rating['grade']})")
        
        return rating
    
    def _calculate_environmental_score(self, brand_data: Dict[str, Any]) -> float:
        """Calculate environmental sustainability score (0-100)"""
        
        score = 50.0  # Start at neutral
        
        commitments = brand_data.get('sustainability_commitments', [])
        certifications = brand_data.get('certifications', [])
        
        # Analyze commitments
        commitment_text = ' '.join(commitments).lower()
        
        for keyword in self.environmental_keywords:
            if keyword in commitment_text:
                score += 3
        
        # Check for certifications
        for cert in certifications:
            if cert in self.certification_scores:
                score += self.certification_scores[cert] * 0.5
        
        # Check for specific high-value commitments
        if 'carbon neutral' in commitment_text or 'net zero' in commitment_text:
            score += 10
        
        if 'renewable energy' in commitment_text:
            score += 8
        
        if 'zero waste' in commitment_text:
            score += 8
        
        # Check products for sustainable materials
        products = brand_data.get('products', [])
        sustainable_product_count = 0
        
        for product in products:
            sustainability_focus = product.get('sustainability_focus', [])
            if sustainability_focus:
                sustainable_product_count += 1
        
        if products:
            product_ratio = sustainable_product_count / len(products)
            score += product_ratio * 15
        
        return min(score, 100.0)
    
    def _calculate_social_score(self, brand_data: Dict[str, Any]) -> float:
        """Calculate social sustainability score (0-100)"""
        
        score = 50.0  # Start at neutral
        
        commitments = brand_data.get('sustainability_commitments', [])
        certifications = brand_data.get('certifications', [])
        
        commitment_text = ' '.join(commitments).lower()
        
        # Analyze social commitments
        for keyword in self.social_keywords:
            if keyword in commitment_text:
                score += 3
        
        # Social certifications
        social_certs = ['Fair Trade', 'B-Corp', 'B Corporation']
        for cert in certifications:
            if cert in social_certs:
                score += 12
        
        # Check for specific commitments
        if 'fair trade' in commitment_text:
            score += 8
        
        if any(term in commitment_text for term in ['living wage', 'fair wages']):
            score += 10
        
        if 'worker rights' in commitment_text or 'safe conditions' in commitment_text:
            score += 8
        
        return min(score, 100.0)
    
    def _calculate_economic_score(self, brand_data: Dict[str, Any]) -> float:
        """Calculate economic sustainability score (0-100)"""
        
        score = 50.0  # Start at neutral
        
        commitments = brand_data.get('sustainability_commitments', [])
        commitment_text = ' '.join(commitments).lower()
        
        # Analyze economic sustainability
        for keyword in self.economic_keywords:
            if keyword in commitment_text:
                score += 3
        
        # Check for durability/quality indicators
        if any(term in commitment_text for term in ['durable', 'quality', 'long-lasting']):
            score += 8
        
        if 'warranty' in commitment_text or 'repair' in commitment_text:
            score += 8
        
        if 'local' in commitment_text or 'locally sourced' in commitment_text:
            score += 7
        
        # Check product prices for fairness (if available)
        products = brand_data.get('products', [])
        if products:
            # Assume reasonable pricing if products exist
            score += 5
        
        return min(score, 100.0)
    
    def _calculate_confidence(self, brand_data: Dict[str, Any]) -> float:
        """Calculate confidence in the rating (0-1)"""
        
        confidence = 0.0
        
        # Data completeness factors
        if brand_data.get('sustainability_commitments'):
            confidence += 0.3
        
        if brand_data.get('certifications'):
            confidence += 0.3
        
        if brand_data.get('products'):
            confidence += 0.2
        
        # Specificity of commitments
        commitments = brand_data.get('sustainability_commitments', [])
        for commitment in commitments:
            # Check for numbers/percentages (indicates specificity)
            if re.search(r'\d+%', commitment) or re.search(r'\d{4}', commitment):
                confidence += 0.05
        
        if brand_data.get('url'):
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def _get_environmental_factors(self, brand_data: Dict[str, Any]) -> List[str]:
        """Get environmental factors found"""
        
        factors = []
        commitment_text = ' '.join(brand_data.get('sustainability_commitments', [])).lower()
        
        for keyword in self.environmental_keywords:
            if keyword in commitment_text:
                factors.append(keyword.replace('_', ' ').title())
        
        return factors[:10]
    
    def _get_social_factors(self, brand_data: Dict[str, Any]) -> List[str]:
        """Get social factors found"""
        
        factors = []
        commitment_text = ' '.join(brand_data.get('sustainability_commitments', [])).lower()
        
        for keyword in self.social_keywords:
            if keyword in commitment_text:
                factors.append(keyword.replace('_', ' ').title())
        
        return factors[:10]
    
    def _get_economic_factors(self, brand_data: Dict[str, Any]) -> List[str]:
        """Get economic factors found"""
        
        factors = []
        commitment_text = ' '.join(brand_data.get('sustainability_commitments', [])).lower()
        
        for keyword in self.economic_keywords:
            if keyword in commitment_text:
                factors.append(keyword.replace('_', ' ').title())
        
        return factors[:10]
    
    def _analyze_certifications(self, certifications: List[str]) -> Dict[str, Any]:
        """Analyze certifications"""
        
        return {
            'count': len(certifications),
            'list': certifications,
            'score_contribution': sum(
                self.certification_scores.get(cert, 0) for cert in certifications
            )
        }
    
    def _score_to_grade(self, score: float) -> str:
        """Convert numerical score to letter grade"""
        
        if score >= 90:
            return 'A+'
        elif score >= 85:
            return 'A'
        elif score >= 80:
            return 'A-'
        elif score >= 75:
            return 'B+'
        elif score >= 70:
            return 'B'
        elif score >= 65:
            return 'B-'
        elif score >= 60:
            return 'C+'
        elif score >= 55:
            return 'C'
        elif score >= 50:
            return 'C-'
        elif score >= 45:
            return 'D+'
        elif score >= 40:
            return 'D'
        else:
            return 'F'


# Global rating engine instance
rating_engine = SustainabilityRatingEngine()


@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    logger.info("🚀 Starting Rating Calculator Agent...")
    
    # Load existing ratings if available
    try:
        if os.path.exists(RATINGS_FILE):
            with open(RATINGS_FILE, 'r') as f:
                data = json.load(f)
                for item in data:
                    ratings_database[item['brand_name']] = item
            logger.info(f"Loaded {len(ratings_database)} ratings from cache")
    except Exception as e:
        logger.warning(f"Could not load cached ratings: {e}")
    
    logger.info("✅ Rating Calculator Agent started successfully!")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down Rating Calculator Agent...")
    
    # Save ratings
    try:
        with open(RATINGS_FILE, 'w') as f:
            json.dump(list(ratings_database.values()), f, indent=2)
        logger.info("Saved ratings to file")
    except Exception as e:
        logger.error(f"Could not save ratings: {e}")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "agent": "Rating Calculator",
        "version": "1.0.0",
        "status": "operational",
        "ratings_calculated": len(ratings_database),
        "endpoints": {
            "calculate": "POST /calculate",
            "ratings": "GET /ratings",
            "rating": "GET /ratings/{brand_name}",
            "health": "GET /health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "ratings_in_database": len(ratings_database)
    }


@app.post("/calculate")
async def calculate_rating(brand_data: Dict[str, Any]):
    """Calculate sustainability rating for a brand"""
    
    try:
        logger.info(f"Received rating request for: {brand_data.get('brand_name')}")
        
        # Calculate rating
        rating = rating_engine.calculate_rating(brand_data)
        
        # Store in database
        ratings_database[rating['brand_name']] = rating
        
        return {
            "status": "success",
            "rating": rating
        }
        
    except Exception as e:
        logger.error(f"Error calculating rating: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/ratings")
async def get_all_ratings():
    """Get all calculated ratings"""
    return {
        "status": "success",
        "count": len(ratings_database),
        "ratings": list(ratings_database.values())
    }


@app.get("/ratings/{brand_name}")
async def get_rating(brand_name: str):
    """Get rating for a specific brand"""
    
    # Try exact match
    if brand_name in ratings_database:
        return {
            "status": "success",
            "rating": ratings_database[brand_name]
        }
    
    # Try fuzzy match
    for name, rating in ratings_database.items():
        if brand_name.lower() in name.lower():
            return {
                "status": "success",
                "rating": rating
            }
    
    raise HTTPException(status_code=404, detail="Rating not found")


@app.post("/recalculate/{brand_name}")
async def recalculate_rating(brand_name: str):
    """Recalculate rating for a brand using latest data"""
    
    # This would fetch latest brand data and recalculate
    # For now, return existing rating
    
    if brand_name in ratings_database:
        return {
            "status": "success",
            "rating": ratings_database[brand_name]
        }
    
    raise HTTPException(status_code=404, detail="Brand not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=RATING_CALCULATOR_PORT)

