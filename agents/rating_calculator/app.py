from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from pymongo import MongoClient

app = FastAPI(title="Rating Calculator", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
load_dotenv(os.path.join(ROOT_DIR, ".env"))
load_dotenv()

PORT = int(os.getenv("RATING_CALCULATOR_PORT", "5002"))


def get_mongo():
    url = os.getenv("DATABASE_URL", "mongodb://localhost:27017/sustainable-shopping-planner")
    client = MongoClient(url)
    db = client.get_default_database()
    return client, db


@app.get("/")
def root():
    return {"agent": "Rating Calculator", "status": "ok", "health": "/health"}


@app.get("/health")
def health():
    try:
        client, db = get_mongo()
        db.command("ping")
        client.close()
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "degraded", "error": str(e)}


@app.get("/ratings")
def ratings():
    # Read brands from Mongo and compute a simple rating per brand
    try:
        client, db = get_mongo()
        brands = list(db.brands.find({}, {"_id": 0}))
    except Exception as e:
        return {"ratings": [], "error": str(e)}
    finally:
        try:
            client.close()
        except Exception:
            pass

    ratings = []
    for b in brands:
        product_count = int(b.get("product_count", 0))
        certifications = b.get("certifications", [])
        # Simple heuristic: base on product count and certifications count
        score = min(100, 50 + min(product_count, 50) * 0.5 + len(certifications) * 10)
        ratings.append({
            "brand_name": b.get("brand_domain", "Unknown"),
            "overall_score": round(score, 2),
        })

    return {"ratings": ratings}


@app.post("/calculate_product_score")
def calculate_product_score(product: dict):
    """
    Calculate sustainability score for a single product.
    
    Expected input:
    {
        "product_name": "Organic Cotton T-Shirt",
        "category": "T-Shirts",
        "price": 35,
        "description": "Made from 100% organic cotton...",
        "sustainability_focus": ["organic", "fair trade"],
        "certifications": ["GOTS", "Fair Trade"]
    }
    
    Returns:
    {
        "sustainability_score": 85,
        "rating": 4.7,
        "score_breakdown": {...}
    }
    """
    try:
        # Initialize base score - varied by category
        product_name = product.get("product_name", "").lower()
        description = product.get("description", "").lower()
        category = product.get("category", "").lower()
        sustainability_focus = product.get("sustainability_focus", [])
        certifications = product.get("certifications", [])
        price = float(product.get("price", 0)) if product.get("price") else 0
        
        # Dynamic base score based on category (40-60)
        category_base_scores = {
            "dress": 52, "dresses": 52, "tops": 54, "shirts": 54, "t-shirt": 56,
            "jackets": 50, "outerwear": 50, "bottoms": 51, "jeans": 48,
            "activewear": 55, "shoes": 49, "footwear": 49, "accessories": 53,
            "bags": 51, "swimwear": 50
        }
        
        base_score = 50  # Default
        for cat_key, cat_score in category_base_scores.items():
            if cat_key in category or cat_key in product_name:
                base_score = cat_score
                break
        
        score = base_score
        score_breakdown = {
            "base": base_score,
            "materials": 0,
            "certifications": 0,
            "sustainability_focus": 0,
            "price_fairness": 0,
            "description_quality": 0,
            "product_quality": 0
        }
        
        # 1. Material Score (up to +30 points)
        premium_materials = ["organic", "recycled", "hemp", "tencel", "bamboo", "linen", "upcycled", "cotton"]
        material_bonus = sum(5 for m in premium_materials if m in product_name or m in description)
        material_bonus = min(30, material_bonus)
        score += material_bonus
        score_breakdown["materials"] = material_bonus
        
        # 2. Certifications (up to +20 points)
        cert_bonus = min(20, len(certifications) * 10)
        score += cert_bonus
        score_breakdown["certifications"] = cert_bonus
        
        # 3. Sustainability Focus (up to +15 points)
        focus_bonus = min(15, len(sustainability_focus) * 5)
        score += focus_bonus
        score_breakdown["sustainability_focus"] = focus_bonus
        
        # 4. Price Fairness (up to +10 points)
        # Fair pricing rewards reasonable prices
        if 20 <= price <= 100:
            price_bonus = 10
        elif 10 <= price < 20:
            price_bonus = 8
        elif 100 < price <= 150:
            price_bonus = 5
        elif 5 <= price < 10:
            price_bonus = 6
        else:
            price_bonus = 3
        score += price_bonus
        score_breakdown["price_fairness"] = price_bonus
        
        # 5. Description Quality (up to +5 points)
        sustainability_keywords = ["sustainable", "eco-friendly", "ethical", "fair", "responsible", "quality"]
        desc_bonus = min(5, sum(1 for kw in sustainability_keywords if kw in description))
        score += desc_bonus
        score_breakdown["description_quality"] = desc_bonus
        
        # 6. Product Quality Indicators (up to +10 points)
        quality_keywords = ["premium", "quality", "durable", "long-lasting", "handmade", "artisan", "classic"]
        quality_bonus = min(10, sum(2 for kw in quality_keywords if kw in product_name or kw in description))
        score += quality_bonus
        score_breakdown["product_quality"] = quality_bonus
        
        # Cap score at 100, minimum at 40
        final_score = min(100, max(40, score))
        
        # Generate rating based on score (more granular)
        if final_score >= 90:
            rating = 4.7 + (final_score - 90) * 0.03
        elif final_score >= 80:
            rating = 4.3 + (final_score - 80) * 0.04
        elif final_score >= 70:
            rating = 3.9 + (final_score - 70) * 0.04
        elif final_score >= 60:
            rating = 3.5 + (final_score - 60) * 0.04
        elif final_score >= 50:
            rating = 3.2 + (final_score - 50) * 0.03
        else:
            rating = 2.8 + (final_score - 40) * 0.04
        
        # Round to 1 decimal but keep variation
        rating = round(max(2.8, min(5.0, rating)), 1)
        
        return {
            "sustainability_score": int(final_score),
            "rating": rating,
            "score_breakdown": score_breakdown,
            "calculation_method": "enhanced_product_scoring_v1"
        }
        
    except Exception as e:
        return {"error": str(e), "sustainability_score": 50, "rating": 3.5}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=PORT, reload=True)


