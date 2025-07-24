from pydantic import BaseModel
from typing import Optional

class TokenData(BaseModel):
    id: Optional[str] = None