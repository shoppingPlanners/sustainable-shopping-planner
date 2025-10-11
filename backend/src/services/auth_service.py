from repositeries import user_repository
from core.security import hash_password, verify_password, create_access_token

async def register_user(email: str, password: str, name: str):
    existing = await user_repository.get_user_by_email(email)
    if existing:
        raise Exception("User already exists")

    hashed = hash_password(password)
    user = await user_repository.create_user(email, hashed, name)
    return {"message": "User created successfully", "user": user}

async def login_user(email: str, password: str):
    user = await user_repository.get_user_by_email(email)
    if not user:
        raise Exception("Invalid email or password")

    if not verify_password(password, user.password):
        raise Exception("Invalid email or password")

    token = create_access_token({"sub": user.email, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}
