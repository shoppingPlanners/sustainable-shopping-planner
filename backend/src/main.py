from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth_router, items_router, preferences_router
from database import db

app = FastAPI(title="Python Prisma Auth API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

app.include_router(auth_router.router)
app.include_router(items_router.router)
app.include_router(preferences_router.router)

# Simple health check endpoint for smoke testing
@app.get("/health")
async def health():
    return {"status": "ok"}
