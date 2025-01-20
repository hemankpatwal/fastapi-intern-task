from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config
from bson import ObjectId

# MongoDB configuration
MONGO_URI = config("MONGO_URI", default="mongodb://localhost:27017")
DATABASE_NAME = "users_db"

client = AsyncIOMotorClient(MONGO_URI)
database = client["users_db"]
users_collection = database["users"]

# To convert ObjectId to string when returning from MongoDB
def str_to_object_id(id: str) -> ObjectId:
    return ObjectId(id)  # Convert string to ObjectId