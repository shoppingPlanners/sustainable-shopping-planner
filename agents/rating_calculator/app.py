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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=PORT, reload=True)


