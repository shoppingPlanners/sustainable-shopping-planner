from fastapi import APIRouter, HTTPException
from services import auth_service
from models import UserRegister, UserLogin

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
async def register(payload: UserRegister):
    try:
        return await auth_service.register_user(payload.email, payload.password, payload.name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login(payload: UserLogin):
    try:
        return await auth_service.login_user(payload.email, payload.password)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
