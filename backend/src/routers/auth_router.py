from fastapi import APIRouter, HTTPException
from services import auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
async def register(email: str, password: str, name: str):
    try:
        return await auth_service.register_user(email, password, name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(email: str, password: str):
    try:
        return await auth_service.login_user(email, password)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
