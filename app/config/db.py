from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config

# MongoDB configuration
MONGO_URI = config("MONGO_URI", default="mongodb://localhost:27017")
DATABASE_NAME = "users_db"

client = AsyncIOMotorClient(MONGO_URI)
database = client["users_db"]
users_collection = database["users"]