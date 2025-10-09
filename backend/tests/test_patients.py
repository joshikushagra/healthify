import pytest


def test_create_patient_profile(client, auth_headers):
    """Test creating a patient profile."""
    patient_data = {
        "blood_type": "O+",
        "height": 175,
        "weight": 70,
        "emergency_contact_name": "John Doe",
        "emergency_contact_phone": "+1234567890"
    }
    
    response = client.post("/patients/", json=patient_data, headers=auth_headers)
    assert response.status_code == 201
    
    data = response.json()
    assert data["blood_type"] == patient_data["blood_type"]
    assert data["height"] == patient_data["height"]
    assert data["weight"] == patient_data["weight"]


def test_get_my_patient_profile(client, auth_headers):
    """Test getting current user's patient profile."""
    # Create profile first
    patient_data = {
        "blood_type": "O+",
        "height": 175,
        "weight": 70
    }
    client.post("/patients/", json=patient_data, headers=auth_headers)
    
    response = client.get("/patients/me", headers=auth_headers)
    assert response.status_code == 200
    
    data = response.json()
    assert "blood_type" in data
    assert "height" in data
    assert "weight" in data


def test_add_medical_history(client, auth_headers):
    """Test adding medical history."""
    # Create patient profile first
    patient_data = {"blood_type": "O+"}
    client.post("/patients/", json=patient_data, headers=auth_headers)
    
    history_data = {
        "condition": "Diabetes",
        "status": "active",
        "notes": "Type 2 diabetes, well controlled"
    }
    
    response = client.post(
        "/patients/me/medical-history",
        json=history_data,
        headers=auth_headers
    )
    assert response.status_code == 201
    
    data = response.json()
    assert data["condition"] == history_data["condition"]
    assert data["status"] == history_data["status"]


def test_add_allergy(client, auth_headers):
    """Test adding an allergy."""
    # Create patient profile first
    patient_data = {"blood_type": "O+"}
    client.post("/patients/", json=patient_data, headers=auth_headers)
    
    allergy_data = {
        "allergen": "Penicillin",
        "severity": "severe",
        "reaction": "Anaphylaxis"
    }
    
    response = client.post(
        "/patients/me/allergies",
        json=allergy_data,
        headers=auth_headers
    )
    assert response.status_code == 201
    
    data = response.json()
    assert data["allergen"] == allergy_data["allergen"]
    assert data["severity"] == allergy_data["severity"]


def test_add_medication(client, auth_headers):
    """Test adding a medication."""
    # Create patient profile first
    patient_data = {"blood_type": "O+"}
    client.post("/patients/", json=patient_data, headers=auth_headers)
    
    medication_data = {
        "name": "Metformin",
        "dosage": "500mg",
        "frequency": "Twice daily",
        "is_active": True
    }
    
    response = client.post(
        "/patients/me/medications",
        json=medication_data,
        headers=auth_headers
    )
    assert response.status_code == 201
    
    data = response.json()
    assert data["name"] == medication_data["name"]
    assert data["dosage"] == medication_data["dosage"]


def test_get_medical_history(client, auth_headers):
    """Test getting medical history."""
    # Create patient profile first
    patient_data = {"blood_type": "O+"}
    client.post("/patients/", json=patient_data, headers=auth_headers)
    
    response = client.get("/patients/me/medical-history", headers=auth_headers)
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)


def test_get_allergies(client, auth_headers):
    """Test getting allergies."""
    # Create patient profile first
    patient_data = {"blood_type": "O+"}
    client.post("/patients/", json=patient_data, headers=auth_headers)
    
    response = client.get("/patients/me/allergies", headers=auth_headers)
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)


def test_get_medications(client, auth_headers):
    """Test getting medications."""
    # Create patient profile first
    patient_data = {"blood_type": "O+"}
    client.post("/patients/", json=patient_data, headers=auth_headers)
    
    response = client.get("/patients/me/medications", headers=auth_headers)
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
