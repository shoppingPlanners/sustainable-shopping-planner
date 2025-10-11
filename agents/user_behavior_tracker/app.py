import os, time
from typing import Any, Literal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import motor.motor_asyncio
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client["sustainable_shopping"]
events_col = db["events"]
profiles_col = db["profiles"]
summaries_col = db["usage_summaries"]

app = FastAPI(title="User Behavior Tracker Agent")


class TrackDoc(BaseModel):
    event_type: str
    user_id: str | None = None
    session_id: str | None = None
    item_id: str | None = None
    brand_id: str | None = None
    metadata: dict | None = None
    timestamp: float | None = None


class BioDoc(BaseModel):
    user_id: str
    age: int | None = None
    gender: str | None = None
    location: str | None = None
    preferences: dict[str, Any] | None = None


@app.on_event("startup")
async def on_startup():
    await events_col.create_index([("timestamp", -1)])
    await summaries_col.create_index([("created_at", -1)])


@app.post("/track")
async def track(doc: TrackDoc):
    payload = doc.dict()
    payload["timestamp"] = payload.get("timestamp") or time.time()
    await events_col.insert_one(payload)
    return {"status": "ok"}


@app.post("/bio")
async def bio(doc: BioDoc):
    update = {k: v for k, v in doc.dict().items() if k != "user_id" and v is not None}
    if update:
        await profiles_col.update_one({"_id": doc.user_id}, {"$set": update}, upsert=True)
    return {"status": "ok"}


@app.post("/summarize")
async def summarize():
    # simple rolling summary for last 24h
    now = time.time()
    since = now - 86400
    total = await events_col.count_documents({"timestamp": {"$gte": since}})
    by_type = {}
    async for row in events_col.aggregate([
        {"$match": {"timestamp": {"$gte": since}}},
        {"$group": {"_id": "$event_type", "count": {"$sum": 1}}},
    ]):
        by_type[row["_id"]] = row["count"]

    summary = {
        "created_at": now,
        "window_start": since,
        "total_events": total,
        "by_type": by_type,
        "notes": _generate_notes(by_type),
    }
    await summaries_col.insert_one(summary)
    return {"status": "ok", "summary": summary}


def _generate_notes(by_type: dict[str, int]) -> list[str]:
    notes: list[str] = []
    if by_type.get("search", 0) > by_type.get("page_view", 0) * 0.5:
        notes.append("High search engagement observed; consider surfacing search tips.")
    if by_type.get("filter_select", 0) > 20:
        notes.append("Users are actively using filters; ensure filter UX remains fast.")
    if by_type.get("view_item", 0) == 0:
        notes.append("No item views recorded; verify instrumentation on product cards.")
    return notes


@app.get("/summaries/latest")
async def latest_summary():
    doc = await summaries_col.find_one(sort=[("created_at", -1)])
    if not doc:
        raise HTTPException(status_code=404, detail="No summaries yet")
    # convert ObjectId if present
    doc["_id"] = str(doc.get("_id"))
    return doc




