from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from .. import models, schemas
from ..database import get_db
from ..auth.hashing import Hash
from ..auth.tokens import create_access_token

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


@router.post("/login")
def login_user(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user or not Hash.verify(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
