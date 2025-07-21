from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta
import random

from .. import models, schemas
from ..database import get_db
from ..auth.hashing import Hash
from ..auth.tokens import create_access_token

def send_otp_email(to_email: str, otp: str):
    """Placeholder email sender"""
    print(f"Sending OTP {otp} to {to_email}")

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

@router.post("/register", response_model=schemas.UserOut)
def register_user(request: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    existing_user = db.query(models.User).filter(models.User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = Hash.bcrypt(request.password)
    new_user = models.User(email=request.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/request-registration")
def request_registration(request: schemas.RegistrationRequest, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == request.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    otp = f"{random.randint(100000, 999999)}"
    hashed = Hash.bcrypt(request.password)
    expires = datetime.utcnow() + timedelta(minutes=1)

    db.query(models.RegistrationOTP).filter(models.RegistrationOTP.email == request.email).delete()
    reg = models.RegistrationOTP(email=request.email, hashed_password=hashed, otp=otp, expires_at=expires)
    db.add(reg)
    db.commit()

    send_otp_email(request.email, otp)
    return {"message": "OTP sent"}


@router.post("/confirm-registration", response_model=schemas.UserOut)
def confirm_registration(request: schemas.RegistrationVerify, db: Session = Depends(get_db)):
    record = (
        db.query(models.RegistrationOTP)
        .filter(
            models.RegistrationOTP.email == request.email,
            models.RegistrationOTP.otp == request.otp,
            models.RegistrationOTP.expires_at > datetime.utcnow(),
        )
        .first()
    )
    if not record:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if db.query(models.User).filter(models.User.email == request.email).first():
        db.delete(record)
        db.commit()
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = models.User(email=record.email, hashed_password=record.hashed_password)
    db.add(new_user)
    db.delete(record)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
def login_user(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user or not Hash.verify(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/request-password-reset")
def request_password_reset(request: schemas.PasswordResetRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    otp = f"{random.randint(100000, 999999)}"
    expires = datetime.utcnow() + timedelta(minutes=10)
    reset = models.PasswordReset(user_id=user.id, otp=otp, expires_at=expires)
    db.add(reset)
    db.commit()

    send_otp_email(user.email, otp)
    return {"message": "OTP sent"}


@router.post("/verify-otp")
def verify_otp(request: schemas.OTPVerify, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    reset = (
        db.query(models.PasswordReset)
        .filter(models.PasswordReset.user_id == user.id, models.PasswordReset.otp == request.otp, models.PasswordReset.expires_at > datetime.utcnow())
        .order_by(models.PasswordReset.id.desc())
        .first()
    )
    if not reset:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    reset.is_verified = True
    db.commit()
    return {"message": "OTP verified"}


@router.post("/reset-password")
def reset_password(request: schemas.PasswordUpdate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    reset = (
        db.query(models.PasswordReset)
        .filter(
            models.PasswordReset.user_id == user.id,
            models.PasswordReset.otp == request.otp,
            models.PasswordReset.expires_at > datetime.utcnow(),
            models.PasswordReset.is_verified == True,
        )
        .order_by(models.PasswordReset.id.desc())
        .first()
    )
    if not reset:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    user.hashed_password = Hash.bcrypt(request.password)
    db.commit()
    return {"message": "Password updated"}
