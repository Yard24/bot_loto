from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/users/", json={"email": "test@test.com", "password": "password123"})
    assert response.status_code == 200
    assert response.json()["message"] == "User created successfully"

def test_duplicate_email():
    client.post("/users/", json={"email": "test@test.com", "password": "password123"})
    response = client.post("/users/", json={"email": "test@test.com", "password": "password123"})
    assert response.status_code == 400
