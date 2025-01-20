from pydantic import BaseModel
from pydantic.networks import EmailStr
from typing import Optional

class User(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = None

class UserResponse(User):
    id: str