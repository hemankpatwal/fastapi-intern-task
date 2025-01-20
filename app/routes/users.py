from fastapi import APIRouter, HTTPException
from app.config.db import users_collection
from app.schemas.user import User, UserResponse
from app.utils.helpers import user_helper
from bson import ObjectId
from typing import List

router = APIRouter()

@router.post("/users", response_model=UserResponse)
async def create_user(user: User):
    if await users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="User with this email already exists.")
    new_user = await users_collection.insert_one(user.dict())
    created_user = await users_collection.find_one({"_id": new_user.inserted_id})
    return user_helper(created_user)

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user_helper(user)

@router.get("/users", response_model=List[UserResponse])
async def list_users():
    users = await users_collection.find().to_list(100)
    return [user_helper(user) for user in users]

@router.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: str):
    result = await users_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found.")