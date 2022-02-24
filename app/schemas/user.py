from datetime import datetime as dt
from typing import Optional, List
from pydantic import BaseModel

from .profile import *
from ..utils.schemaHelper import Base, as_form

class UserBase(Base):
    email: Optional[str]
    user_type: Optional[str] = None
    user_profile_id: Optional[str] = None

    is_active: Optional[str] = None
    user_profile: Optional[Profile] = None


@as_form
class CreateUser(UserBase):
    password: str

class SurgeryBase(Base):
    room: Optional[str] = None
    patient_id: Optional[str] = None
    surgery_type_id: Optional[str] = None

    in_charge: Optional[str] = None

    start_time: Optional[dt] = None
    end_time: Optional[dt] = None
    status: Optional[str] = None
    is_active: Optional[str] = None


class User(CreateUser):
    id: str
    user_profile: Optional[Profile] = None
    handled_surgeries: Optional[SurgeryBase] = None
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