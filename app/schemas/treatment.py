from datetime import datetime as dt
from typing import Optional
from pydantic import BaseModel

class Base(BaseModel):
    class Config():
        orm_mode = True


class TreatmentBase(Base):
    description: str
    status: Optional[str]

    created_at: Optional[dt]
    updated_at: Optional[dt]


class CreateTreatment(TreatmentBase):
    pass
    # room_id: str
    # patient_id: str
    # treatment_type_id: str


class Treatment(TreatmentBase):
    # patient: str
    # treatment_type: str
    pass
