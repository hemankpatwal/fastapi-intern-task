from fastapi import APIRouter, HTTPException
from app.models import User
from app.config.db import user_collection
from bson import ObjectId

router = APIRouter()

@router.post("/create-user", response_model=User)
async def create_user(user: User):
    user_data = user.model_dump()
    result = user_collection.insert_one(user_data)
    return {**user_data, "id": str(result.inserted_id)}

@router.get("/get-user/{user_id}", response_model=User)
async def get_user(user_id: str):
    user = user_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return {**user, "id": str(user["_id"])}
    raise HTTPException(status_code=404, detail="User not found")

@router.get("/list-users", response_model=list[User])
async def list_users():
    users = [{**user, "id": str(user["_id"])} for user in user_collection.find()]
    return users

@router.put("/edit-user/{user_id}", response_model=User)
async def edit_user(user_id: str, user: User):
    updated_user = user.dict()
    result = user_collection.update_one({"_id": ObjectId(user_id)}, {"$set": updated_user})
    
    if result.modified_count == 1:
        updated_user["id"] = user_id
        return updated_user
    
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/delete-user/{user_id}")
async def delete_user(user_id: str):
    result = user_collection.delete_one({"_id": ObjectId(user_id)})
    
    if result.deleted_count == 1:
        return {"detail": "User deleted successfully"}
    
    raise HTTPException(status_code=404, detail="User not found")
