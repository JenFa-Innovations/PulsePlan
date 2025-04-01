# backend/tests/test_dummy.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["message"] == "PulsePlan backend is running 🚀"
