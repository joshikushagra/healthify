import pytest
from fastapi.testclient import TestClient


def test_register_user(client, test_user_data):
    """Test user registration."""
    response = client.post("/auth/register", json=test_user_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["email"] == test_user_data["email"]
    assert data["first_name"] == test_user_data["first_name"]
    assert data["last_name"] == test_user_data["last_name"]
    assert data["role"] == test_user_data["role"]
    assert "id" in data


def test_register_duplicate_email(client, test_user_data):
    """Test registration with duplicate email."""
    # First registration
    client.post("/auth/register", json=test_user_data)
    
    # Second registration with same email
    response = client.post("/auth/register", json=test_user_data)
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]


def test_login_success(client, test_user_data):
    """Test successful login."""
    # Register user first
    client.post("/auth/register", json=test_user_data)
    
    # Login
    login_data = {
        "email": test_user_data["email"],
        "password": test_user_data["password"]
    }
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client, test_user_data):
    """Test login with invalid credentials."""
    # Register user first
    client.post("/auth/register", json=test_user_data)
    
    # Login with wrong password
    login_data = {
        "email": test_user_data["email"],
        "password": "wrongpassword"
    }
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]


def test_get_current_user(client, auth_headers):
    """Test getting current user profile."""
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200
    
    data = response.json()
    assert "email" in data
    assert "first_name" in data
    assert "last_name" in data


def test_get_current_user_unauthorized(client):
    """Test getting current user without authentication."""
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_refresh_token(client, test_user_tokens):
    """Test token refresh."""
    refresh_token = test_user_tokens["refresh_token"]
    
    response = client.post("/auth/refresh", json={"refresh_token": refresh_token})
    assert response.status_code == 200
    
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_logout(client, auth_headers):
    """Test logout."""
    response = client.post("/auth/logout", headers=auth_headers)
    assert response.status_code == 200
    assert "Successfully logged out" in response.json()["message"]
