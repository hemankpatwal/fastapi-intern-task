import pytest
import  sys
import os
from pathlib import Path
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient
from app.config.db import database, users_collection

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.main import app

TEST_DATABASE_NAME = "test_users_db"

@pytest.fixture(scope="session")
def test_client():
    client = TestClient(app)
    yield client

@pytest.fixture(scope="session", autouse=True)
async def setup_test_db():
    # Set up test database
    test_client = AsyncIOMotorClient("mongodb://localhost:27017")
    test_database = test_client[TEST_DATABASE_NAME]
    test_users_collection = test_database["users"]

    # Override the app's database connection
    database.client = test_client
    database._database = test_database
    users_collection._collection = test_users_collection

    # Clean up before and after each test
    yield
    await test_users_collection.delete_many({})
    test_client.drop_database(TEST_DATABASE_NAME)
