from datetime import datetime as dt
from pydantic import BaseModel
from typing import List

class Base(BaseModel):
    class Config():
        orm_mode = True


class ProfileBase(Base):
    start_time: dt
    end_time: dt

    status: str


class CreateProfile(Base):
    # department_id: str
    position: str
    first_name: str
    middle_name: str
    last_name: str
    suffix_name: str
    birth_date: str


class Profile(CreateProfile):
    # department: str
    created_at: dt
    updated_at: dt