from fastapi import APIRouter, HTTPException
from services import auth_service
from models import UserRegister, UserLogin

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
async def register(user_data: UserRegister):
    try:
        return await auth_service.register_user(user_data.email, user_data.password, user_data.name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(user_data: UserLogin):
    try:
        return await auth_service.login_user(user_data.email, user_data.password)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
