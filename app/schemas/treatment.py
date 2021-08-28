from datetime import datetime as dt
from typing import Optional
from pydantic import BaseModel

class Base(BaseModel):
    class Config():
        orm_mode = True


class TreatmentBase(Base):
    start_time: dt
    end_time: dt

    status: str


class CreateTreatment(TreatmentBase):
    room_id: str
    patient_id: str
    treatment_type_id: str


class Treatment(TreatmentBase):
    patient: str
    description: str
    status: Optional[str]
    treatment_type: str
    created_at: Optional[dt]
    updated_at: Optional[dt]
