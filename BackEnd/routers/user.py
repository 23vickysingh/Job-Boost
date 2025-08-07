from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random

import models, schemas
from database import get_db
from auth.hashing import Hash
from auth.tokens import create_access_token
from redis_client import redis_client
import os
import requests


def send_otp_email(to_email: str, otp: str) -> bool:
    """Send OTP via Brevo. Returns True on success."""
    api_key = os.getenv("BREVO_API_KEY")
    if not api_key:
        print(api_key)
        print("Brevo API key not configured")
        return False

    payload = {
        "sender": {"name": "JobBoost", "email": "no-reply@jobboost.com"},
        "to": [{"email": to_email}],
        "subject": "Your JobBoost OTP",
        "htmlContent": f"<p>Your verification code is <strong>{otp}</strong></p>",
    }
    headers = {"api-key": api_key, "Content-Type": "application/json"}
    try:
        response = requests.post(
            "https://api.brevo.com/v3/smtp/email", json=payload, headers=headers
        )
        response.raise_for_status()
        return True
    except requests.RequestException as e:
        print("Brevo send failed", e)
        return False


router = APIRouter(prefix="/user", tags=["User"])


@router.post("/register", response_model=schemas.UserResponse)
def register_user(request: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.user_id == request.user_id).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User ID already registered")

    hashed_password = Hash.bcrypt(request.password)
    new_user = models.User(user_id=request.user_id, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    profile = models.UserProfile(user_id=new_user.id)
    db.add(profile)
    db.commit()
    return new_user


@router.post("/request-registration")
def request_registration(request: schemas.RegistrationRequest, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.user_id == request.user_id).first():
        raise HTTPException(status_code=400, detail="User ID already registered")

    otp = f"{random.randint(100000, 999999)}"
    hashed = Hash.bcrypt(request.password)
    key = f"reg:{request.user_id}"
    redis_client.hset(key, mapping={"otp": otp, "password": hashed})
    redis_client.expire(key, timedelta(minutes=1))
    print("your otp for current session is " , otp)
    if not send_otp_email(request.user_id, otp):
        redis_client.delete(key)
        raise HTTPException(status_code=400, detail="Invalid email id")
    return {"message": "OTP sent"}


@router.post("/confirm-registration", response_model=schemas.UserResponse)
def confirm_registration(request: schemas.RegistrationVerify, db: Session = Depends(get_db)):
    key = f"reg:{request.user_id}"
    data = redis_client.hgetall(key)
    if not data or data.get("otp") != request.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if db.query(models.User).filter(models.User.user_id == request.user_id).first():
        redis_client.delete(key)
        raise HTTPException(status_code=400, detail="User ID already registered")

    new_user = models.User(user_id=request.user_id, password=data.get("password"))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    redis_client.delete(key)

    profile = models.UserProfile(user_id=new_user.id)
    db.add(profile)
    db.commit()
    return new_user


@router.post("/login")
def login_user(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == request.username).first()
    if not user or not Hash.verify(request.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/request-password-reset")
def request_password_reset(request: schemas.PasswordResetRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    otp = f"{random.randint(100000, 999999)}"
    key = f"reset:{user.id}"
    redis_client.setex(key, timedelta(minutes=10), otp)

    send_otp_email(request.user_id, otp)
    return {"message": "OTP sent"}


@router.post("/verify-otp")
def verify_otp(request: schemas.OTPVerify, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    key = f"reset:{user.id}"
    otp = redis_client.get(key)
    if not otp or otp != request.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    redis_client.setex(f"reset_verified:{user.id}", timedelta(minutes=10), "1")
    return {"message": "OTP verified"}


@router.post("/reset-password")
def reset_password(request: schemas.PasswordUpdate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    key = f"reset:{user.id}"
    otp = redis_client.get(key)
    verified = redis_client.get(f"reset_verified:{user.id}")
    if not otp or otp != request.otp or not verified:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    user.password = Hash.bcrypt(request.password)
    db.commit()
    redis_client.delete(key)
    redis_client.delete(f"reset_verified:{user.id}")
    return {"message": "Password updated"}
