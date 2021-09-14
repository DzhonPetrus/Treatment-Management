from typing import List, Optional
from pydantic import BaseModel

from ..utils.schemaHelper import Base, as_form



class Login(Base):
    email: str
    password: str



class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    email: Optional[str] = None
    user_type: Optional[str] = None