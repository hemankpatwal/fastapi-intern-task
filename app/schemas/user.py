from pydantic import BaseModel
from pydantic.networks import EmailStr
from typing import Optional

class User(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = None

class UserResponse(User):
    id: str
    name: str
    email: EmailStr

    class Config:
        # Allows Pydantic to work with MongoDB's ObjectId as a string
        orm_mode = True

    @classmethod
    def from_mongo(cls, mongo_obj):
        """Helper function to convert MongoDB document to Pydantic UserResponse."""
        # MongoDB stores _id as ObjectId, so we need to convert it to string
        mongo_obj["id"] = str(mongo_obj["_id"])
        del mongo_obj["_id"]  # Remove the original _id
        return cls(**mongo_obj)