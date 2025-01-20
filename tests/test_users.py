import pytest
from bson import ObjectId

@pytest.fixture
def new_user():
    return {
        "name": "Test User",
        "email": "testuser@example.com",
        "age": 30
    }

@pytest.fixture
def invalid_user():
    return {
        "name": "Invalid User",
        "email": "invalid-email",  # Invalid email
        "age": 25
    }

def test_create_user(test_client, new_user):
    response = test_client.post("/api/users", json=new_user)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == new_user["name"]
    assert data["email"] == new_user["email"]
    assert data["age"] == new_user["age"]
    assert "id" in data

def test_create_user_with_existing_email(test_client, new_user):
    # Create the user once
    test_client.post("/api/users", json=new_user)

    # Attempt to create the user again
    response = test_client.post("/api/users", json=new_user)
    assert response.status_code == 400
    assert response.json()["detail"] == "User with this email already exists."

def test_create_user_with_invalid_data(test_client, invalid_user):
    response = test_client.post("/api/users", json=invalid_user)
    assert response.status_code == 422  # Unprocessable Entity

def test_get_user(test_client, new_user):
    # Create a user
    create_response = test_client.post("/api/users", json=new_user)
    user_id = create_response.json()["id"]

    # Get the user
    response = test_client.get(f"/api/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["name"] == new_user["name"]

def test_get_user_not_found(test_client):
    response = test_client.get(f"/api/users/{ObjectId()}")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found."

def test_list_users(test_client, new_user):
    # Create a user
    test_client.post("/api/users", json=new_user)

    # List users
    response = test_client.get("/api/users")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_delete_user(test_client, new_user):
    # Create a user
    create_response = test_client.post("/api/users", json=new_user)
    user_id = create_response.json()["id"]

    # Delete the user
    delete_response = test_client.delete(f"/api/users/{user_id}")
    assert delete_response.status_code == 204

    # Verify user is deleted
    get_response = test_client.get(f"/api/users/{user_id}")
    assert get_response.status_code == 404

def test_delete_user_not_found(test_client):
    response = test_client.delete(f"/api/users/{ObjectId()}")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found."
