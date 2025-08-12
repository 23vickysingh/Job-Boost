from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import random

import models, schemas
from database import get_db
from auth.hashing import Hash
from auth.tokens import create_access_token
from services.otp_service import OTPService
from services.email_service import EmailService
import os

router = APIRouter(prefix="/user", tags=["User"])
otp_service = OTPService()
email_service = EmailService()


@router.post("/request-registration")
def request_registration(request: schemas.RegistrationRequest, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.user_id == request.user_id).first():
        raise HTTPException(status_code=400, detail="User ID already registered")

    otp = otp_service.generate_otp()
    
    # Store registration data with OTP
    registration_data = {
        "password": Hash.bcrypt(request.password)
    }
    
    otp_service.store_otp(request.user_id, otp, "registration", ttl_minutes=10, 
                         additional_data=registration_data)
    
    print("your otp for current session is", otp)
    if not email_service.send_otp(request.user_id, otp):
        otp_service.delete_otp(request.user_id, "registration")
        raise HTTPException(status_code=400, detail="Invalid email id")
    return {"message": "OTP sent"}


@router.post("/confirm-registration", response_model=schemas.UserResponse)
def confirm_registration(request: schemas.RegistrationVerify, db: Session = Depends(get_db)):
    # Verify OTP and get stored data
    stored_data = otp_service.verify_otp(request.user_id, request.otp, "registration")
    if not stored_data:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    if db.query(models.User).filter(models.User.user_id == request.user_id).first():
        raise HTTPException(status_code=400, detail="User ID already registered")

    # Get password from stored data
    password = stored_data.get("password")
    if not password:
        raise HTTPException(status_code=400, detail="Registration data not found")

    new_user = models.User(user_id=request.user_id, password=password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

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

    otp = otp_service.generate_otp()
    otp_service.store_otp(request.user_id, otp, "password_reset", ttl_minutes=10)
    print("your otp to reset password is ", otp)
    # email_service.send_otp(request.user_id, otp)
    return {"message": "OTP sent"}


@router.post("/verify-otp")
def verify_otp(request: schemas.RegistrationVerify, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check if OTP is valid without consuming it
    if not otp_service.is_otp_valid(request.user_id, request.otp, "password_reset"):
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    return {"message": "OTP verified"}


@router.post("/reset-password")
def reset_password(request: schemas.PasswordUpdate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify and consume OTP
    stored_data = otp_service.verify_otp(request.user_id, request.otp, "password_reset")
    if not stored_data:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    user.password = Hash.bcrypt(request.password)
    db.commit()
    
    return {"message": "Password updated"}
