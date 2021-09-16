from datetime import date, datetime as dt
from pydantic import BaseModel
from typing import List, Optional

from ..utils.schemaHelper import Base, as_form

class ProfileBase(Base):
    # department_id: str
    department: str
    position: str
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    suffix_name: Optional[str] = None
    birth_date: Optional[date] = None
    picture: Optional[str] = None

    is_active: Optional[str] = None


@as_form
class CreateProfile(ProfileBase):
    pass



class Profile(ProfileBase):
    id: str
    created_at: Optional[dt] = None
    updated_at: Optional[dt] = None

class OutProfiles(Base):
    data: List[Profile]
    error: bool
    message: str

class OutProfile(Base):
    data: Profile
    error: bool
    message: str