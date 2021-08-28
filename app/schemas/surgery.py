from datetime import datetime as dt
from typing import Optional
from pydantic import BaseModel

class Base(BaseModel):
    class Config():
        orm_mode = True


class SurgeryBase(Base):
    created_at: Optional[dt]
    updated_at: Optional[dt]

    status: Optional[str]


class CreateSurgery(SurgeryBase):
    room_id: str
    patient_id: str
    surgery_type_id: str


class Surgery(SurgeryBase):
    room: str
    patient: str
    surgery_type: str
