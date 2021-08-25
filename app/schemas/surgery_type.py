from datetime import datetime as dt
from pydantic import BaseModel

class Base(BaseModel):
    class Config():
        orm_mode = True


class SurgeryTypeBase(Base):
    name: str
    description: str
    price: float

    status: str


class CreateSurgeryType(SurgeryTypeBase):
    pass


class SurgeryType(SurgeryTypeBase):
    created_at: dt
    updated_at: dt
