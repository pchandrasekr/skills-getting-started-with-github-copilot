import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Arrange-Act-Assert: Get all activities

def test_get_activities():
    # Arrange: (nothing to set up, using in-memory data)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

# Arrange-Act-Assert: Register a participant (success)
def test_signup_success():
    # Arrange
    activity = "Chess Club"
    email = "testuser1@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]
    # Clean up
    client.delete(f"/activities/{activity}/signup", params={"email": email})

# Arrange-Act-Assert: Register a participant (duplicate)
def test_signup_duplicate():
    activity = "Chess Club"
    email = "testuser2@mergington.edu"
    # Arrange: sign up once
    client.post(f"/activities/{activity}/signup", params={"email": email})
    # Act: try to sign up again
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]
    # Clean up
    client.delete(f"/activities/{activity}/signup", params={"email": email})

# Arrange-Act-Assert: Unregister a participant (success)
def test_unregister_success():
    activity = "Chess Club"
    email = "testuser3@mergington.edu"
    # Arrange: sign up first
    client.post(f"/activities/{activity}/signup", params={"email": email})
    # Act
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert f"Removed {email}" in response.json()["message"]

# Arrange-Act-Assert: Unregister a participant (not found)
def test_unregister_not_found():
    activity = "Chess Club"
    email = "notfound@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
