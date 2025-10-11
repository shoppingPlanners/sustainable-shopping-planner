from database import db

async def get_user_by_email(email: str):
    return await db.user.find_unique(where={"email": email})

async def create_user(email: str, password: str, name: str):
    return await db.user.create(
        data={"email": email, "password": password, "name": name}
    )
