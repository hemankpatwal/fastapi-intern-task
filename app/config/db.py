from pymongo import MongoClient
import os

# Load environment variables from .env file (if using python-dotenv)
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")

client = MongoClient(MONGODB_URI)
db = client["user_database"]
user_collection = db["users"]
