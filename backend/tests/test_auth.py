import time
import pyotp
import pytest
from app.core.config import settings
from app.main import redis_client


@pytest.fixture
def valid_otp():
    """Generate a valid OTP based on the shared secret."""
    return pyotp.TOTP(settings.REGISTRATION_SECRET).now()


def register_user(client, username: str, otp_code: str, password: str = "secure123"):
    return client.post("/register", json={
        "username": username,
        "password": password,
        "otp_code": otp_code
    })


def login_user(client, username: str, password: str):
    return client.post("/login", json={
        "username": username,
        "password": password
    })


def test_register_user_with_valid_otp(client, valid_otp):
    response = register_user(client, "testuser", valid_otp)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data


def test_register_user_with_invalid_otp(client):
    response = register_user(client, "invaliduser", "000000")
    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid or expired OTP code"


def test_login_with_valid_credentials(client, valid_otp):
    register_user(client, "loginuser", valid_otp)
    res = login_user(client, "loginuser", "secure123")
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_with_wrong_password(client, valid_otp):
    register_user(client, "wrongpwuser", valid_otp)
    res = login_user(client, "wrongpwuser", "wrongpassword")
    assert res.status_code == 401


def test_login_with_invalid_user(client):
    res = login_user(client, "nonexistent", "nopassword")
    assert res.status_code == 401


def test_login_lockout_after_failed_attempts(client, valid_otp):
    register_user(client, "lockuser", valid_otp)

    # 3x wrong password
    for _ in range(3):
        res = login_user(client, "lockuser", "wrongpass")
        assert res.status_code == 401

    # Should be locked now
    res = login_user(client, "lockuser", "secure123")
    assert res.status_code == 403
    assert "Too many failed attempts" in res.json()["detail"]


def test_login_unlock_after_wait(client, valid_otp):
    register_user(client, "unlockuser", valid_otp)

    # Trigger lockout
    for _ in range(3):
        login_user(client, "unlockuser", "wrongpass")

    time.sleep(31)  # wait for lockout to expire

    res = login_user(client, "unlockuser", "secure123")
    assert res.status_code == 200
    assert "access_token" in res.json()

def test_blacklist_login(client, valid_otp):
    # First, register the user
    response = register_user(client, "blacklistuser", valid_otp)
    assert response.status_code == 201
    
    # Simulate a failed login attempt
    res = login_user(client, "blacklistuser", "wrongpassword")
    assert res.status_code == 401

    # Now, the user should be locked out after the failed attempts
    for _ in range(2):  # Make 2 more failed login attempts to trigger lockout
        res = login_user(client, "blacklistuser", "wrongpassword")
        assert res.status_code == 401
    
    # The account should be locked now, so it should be added to blacklist
    res = login_user(client, "blacklistuser", "wrongpassword")
    assert res.status_code == 403
    assert "Too many failed attempts" in res.text  # Assert the correct error message

    # Manually add the user to the blacklist in Redis
    redis_client.setex(f"blacklist:blacklistuser", 3600, "blocked")  # Blacklist for 1 hour

    # Attempt login again - it should be blocked as the user is blacklisted
    res = login_user(client, "blacklistuser", "secure123")
    assert res.status_code == 403
    assert "User is blacklisted" in res.text  # Assert the correct blacklist message