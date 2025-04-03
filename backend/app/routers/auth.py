# backend/app/routers/auth.py

from fastapi import Request
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.main import limiter
from app.models import User
from app.schemas import UserCreate, UserResponse, LoginRequest, Token
from app.security import hash_password, create_access_token, verify_password
from app.core.config import settings
from app.core.redis import add_to_blacklist, is_blacklisted
import pyotp
from datetime import datetime, timedelta

LOCK_THRESHOLDS = [3, 5, 7]
LOCK_TIMES = [30, 60, 300]  # seconds

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("3/minute")
def register(request: Request, user: UserCreate, db: Session = Depends(get_db)):
    totp = pyotp.TOTP(settings.REGISTRATION_SECRET)
    if not totp.verify(user.otp_code):
        raise HTTPException(status_code=403, detail="Invalid or expired OTP code")

    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_pw = hash_password(user.password)
    db_user = User(username=user.username, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
def login(request: Request, login_data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == login_data.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Check if the user is blacklisted
    if is_blacklisted(login_data.username):
        raise HTTPException(status_code=403, detail="User is blacklisted")

    # check lockout
    if user.lock_until and user.lock_until > datetime.utcnow():
        remaining = int((user.lock_until - datetime.utcnow()).total_seconds())
        raise HTTPException(
            status_code=403,
            detail=f"Too many failed attempts. Try again in {remaining} seconds."
        )

    # wrong password
    if not verify_password(login_data.password, user.hashed_password):
        user.failed_attempts += 1

        if user.failed_attempts in LOCK_THRESHOLDS:
            i = LOCK_THRESHOLDS.index(user.failed_attempts)
            duration = LOCK_TIMES[i]
            user.lock_until = datetime.utcnow() + timedelta(seconds=duration)

        db.commit()
        if user.failed_attempts >= LOCK_THRESHOLDS[-1]:  # max threshold reached
            add_to_blacklist(login_data.username, 3600)  # Blacklist the user for 1 hour

        raise HTTPException(status_code=401, detail="Invalid credentials")

    # right password → reset counters
    user.failed_attempts = 0
    user.lock_until = None
    db.commit()

    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}