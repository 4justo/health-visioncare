import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import SessionLocal

client = TestClient(app)

def test_create_patient():
    # First, login to get token
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "testpassword123"}
    )
    token = login_response.json()["access_token"]
    
    # Create patient
    response = client.post(
        "/api/v1/patients/",
        json={
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1990-01-01",
            "gender": "male",
            "email": "john.doe@example.com",
            "phone": "1234567890",
            "clinic_name": "Vision Clinic"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"
    assert data["patient_id"].startswith("PAT-")

def test_get_patients():
    # Login
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "testpassword123"}
    )
    token = login_response.json()["access_token"]
    
    # Get patients
    response = client.get(
        "/api/v1/patients/",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "pages" in data

def test_search_patients():
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "testpassword123"}
    )
    token = login_response.json()["access_token"]
    
    # Search patients
    response = client.get(
        "/api/v1/patients/?search=John&gender=male",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data["items"], list)
