from database import db
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# Create a direct MongoDB connection
mongo_client = MongoClient(os.getenv("DATABASE_URL", "mongodb://localhost:27017/sustainable-shopping-planner"))
mongo_db = mongo_client.get_default_database()

async def get_user_by_email(email: str):
    # Use raw MongoDB operation
    user = mongo_db.users.find_one({"email": email})
    if user:
        # Convert ObjectId to string for JSON serialization
        user["id"] = str(user["_id"])
        del user["_id"]
    return user

async def create_user(email: str, password: str, name: str):
    # Use raw MongoDB operation
    user_data = {
        "email": email,
        "password": password,
        "name": name,
        "role": "user"
    }
    result = mongo_db.users.insert_one(user_data)
    
    # Return the created user
    created_user = mongo_db.users.find_one({"_id": result.inserted_id})
    if created_user:
        created_user["id"] = str(created_user["_id"])
        del created_user["_id"]
    return created_user
