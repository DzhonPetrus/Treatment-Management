from datetime import datetime as dt
from pydantic import BaseModel

class Base(BaseModel):
    class Config():
        orm_mode = True


class LabTestBase(Base):
    name: str
    description: str
    price: float

    status: str


class CreateLabTest(LabTestBase):
    pass


class LabTest(LabTestBase):
    created_at: dt
    updated_at: dt
