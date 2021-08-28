from datetime import datetime as dt
from pydantic import BaseModel

class Base(BaseModel):
    class Config():
        orm_mode = True


class TreatmentTypeBase(Base):
    name: str
    room: str
    description: str
    price: float

    


class CreateTreatmentType(TreatmentTypeBase):
    pass


class TreatmentType(TreatmentTypeBase):
    created_at: dt
    updated_at: dt
