from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from services import auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/register")
async def register(payload: RegisterRequest):
    try:
        return await auth_service.register_user(payload.email, payload.password, payload.name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(payload: LoginRequest):
    try:
        return await auth_service.login_user(payload.email, payload.password)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
