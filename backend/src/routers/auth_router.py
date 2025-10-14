from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services import auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])

class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/register")
async def register(request: RegisterRequest):
    try:
        return await auth_service.register_user(request.email, request.password, request.name)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(request: LoginRequest):
    try:
        return await auth_service.login_user(request.email, request.password)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
