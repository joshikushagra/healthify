import pytest
from unittest.mock import patch, AsyncMock


def test_create_chat_session(client, auth_headers):
    """Test creating a chat session."""
    response = client.post("/chat/session", headers=auth_headers)
    assert response.status_code == 201
    
    data = response.json()
    assert "session_id" in data
    assert data["is_active"] is True


def test_get_chat_sessions(client, auth_headers):
    """Test getting user's chat sessions."""
    # Create a session first
    client.post("/chat/session", headers=auth_headers)
    
    response = client.get("/chat/sessions", headers=auth_headers)
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


@patch('app.services.ai_service.ai_service.analyze_symptoms')
def test_analyze_symptoms(mock_analyze_symptoms, client, auth_headers):
    """Test symptom analysis."""
    # Mock AI service response
    mock_response = {
        "conditions": [
            {
                "name": "Common Cold",
                "probability": 0.7,
                "description": "Viral infection of the upper respiratory tract",
                "severity": "mild"
            }
        ],
        "triage_advice": {
            "urgency": "low",
            "recommendation": "Rest and stay hydrated",
            "timeframe": "within 24 hours"
        },
        "disclaimer": "This is not a substitute for professional medical advice.",
        "confidence_score": 0.7,
        "follow_up_recommendations": ["Monitor symptoms", "Consult doctor if symptoms worsen"]
    }
    mock_analyze_symptoms.return_value = mock_response
    
    symptom_data = {
        "symptoms": ["cough", "runny nose", "sore throat"],
        "age": 30,
        "gender": "male"
    }
    
    response = client.post("/chat/symptom", json=symptom_data, headers=auth_headers)
    assert response.status_code == 200
    
    data = response.json()
    assert "conditions" in data
    assert "triage_advice" in data
    assert "disclaimer" in data


def test_analyze_symptoms_unauthorized(client):
    """Test symptom analysis without authentication."""
    symptom_data = {
        "symptoms": ["cough", "runny nose"],
        "age": 30
    }
    
    response = client.post("/chat/symptom", json=symptom_data)
    assert response.status_code == 401


def test_send_message(client, auth_headers):
    """Test sending a message in a chat session."""
    # Create a session first
    session_response = client.post("/chat/session", headers=auth_headers)
    session_id = session_response.json()["session_id"]
    
    message_data = {
        "content": "Hello, I have a headache",
        "message_type": "user"
    }
    
    response = client.post(
        f"/chat/sessions/{session_id}/messages",
        json=message_data,
        headers=auth_headers
    )
    assert response.status_code == 200
    
    data = response.json()
    assert data["content"] == message_data["content"]
    assert data["message_type"] == "user"


def test_end_chat_session(client, auth_headers):
    """Test ending a chat session."""
    # Create a session first
    session_response = client.post("/chat/session", headers=auth_headers)
    session_id = session_response.json()["session_id"]
    
    response = client.delete(f"/chat/sessions/{session_id}", headers=auth_headers)
    assert response.status_code == 200
    assert "Chat session ended successfully" in response.json()["message"]
