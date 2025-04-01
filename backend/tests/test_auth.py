def test_register_user(client):
    response = client.post("/register", json={
        "username": "testuser",
        "password": "secure123"
    })

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data
