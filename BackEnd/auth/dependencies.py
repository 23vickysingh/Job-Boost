from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session  

import models, database
from auth.tokens import verify_access_token

# OAuth2PasswordBearer expects the full login URL relative to the API root.
# Our login route lives under the /user prefix, so we specify that here to
# ensure FastAPI generates the correct OpenAPI docs and token retrieval works.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user_id = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise credentials_exception
    return user
