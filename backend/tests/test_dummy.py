# backend/tests/test_dummy.py

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "PulsePlan backend is running 🚀"}
