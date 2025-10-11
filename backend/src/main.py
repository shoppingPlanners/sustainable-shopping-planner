from fastapi import FastAPI
from routers import auth_router, items_router
from database import db

app = FastAPI(title="Sustainable Shopping Planner API")

@app.on_event("startup")
async def startup():
    await db.connect()

@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()

app.include_router(auth_router.router)
app.include_router(items_router.router)
