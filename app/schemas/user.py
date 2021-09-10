from datetime import datetime as dt
from typing import Optional, List
from pydantic import BaseModel

from .profile import *
from ..utils.schemaHelper import Base, as_form

class UserBase(Base):
    email: str
    user_type: str
    user_profile_id: Optional[str] = None

    status: Optional[str] = None
    is_active: Optional[str] = None


@as_form
class CreateUser(UserBase):
    password: str


class User(CreateUser):
    id: str
    user_profile: Optional[Profile] = None
    created_at: Optional[dt] = None
    updated_at: Optional[dt] = None


class OutUsers(Base):
    data: List[User]
    error: bool
    message: str

class OutUser(Base):
    data: User
    error: bool
    message: str