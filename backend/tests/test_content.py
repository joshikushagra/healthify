import pytest


def test_get_services(client):
    """Test getting all services."""
    response = client.get("/content/services")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)


def test_get_faqs(client):
    """Test getting all FAQs."""
    response = client.get("/content/faq")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)


def test_get_faqs_by_category(client):
    """Test getting FAQs by category."""
    response = client.get("/content/faq?category=general")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)


def test_health_check(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "version" in data


def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert "docs" in data
    assert "health" in data
