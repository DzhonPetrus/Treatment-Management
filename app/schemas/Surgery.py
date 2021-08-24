from datetime import datetime as dt
from pydantic import BaseModel

class Base(BaseModel):
    class Config():
        orm_mode = True


class SurgeryBase(Base):
    start_time: dt
    end_time: dt

    status: str


class CreateSurgery(SurgeryBase):
    room_id: str
    patient_id: str
    surgery_type_id: str


class Surgery(SurgeryBase):
    room: str
    patient: str
    surgery_type: str
    created_at: dt
    updated_at: dt
