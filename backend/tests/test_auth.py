import pyotp
from app.core.config import settings

def test_register_user_valid_otp(client):
    totp = pyotp.TOTP(settings.REGISTRATION_SECRET)
    valid_code = totp.now()

    response = client.post("/register", json={
        "username": "testuser",
        "password": "secure123",
        "otp_code": valid_code
    })

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data

def test_register_user_invalid_otp(client):
    response = client.post("/register", json={
        "username": "testinvalid",
        "password": "secure123",
        "otp_code": "000000"  # obviously invalid
    })

    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid or expired OTP code"
