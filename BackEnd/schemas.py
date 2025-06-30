from pydantic import BaseModel
from typing import List, Optional

class User(BaseModel):
    email: str
    password: str


class Login(BaseModel):
    email: str
    password: str


class TokenData(BaseModel):
    email: Optional[str] = None
