from datetime import datetime as dt
from pydantic import BaseModel

class Base(BaseModel):
    class Config():
        orm_mode = True


class LabTestBase(Base):  
    status: str


class CreateLabTest(Base):
    name: str
    description: str
    price: float


class LabTest(Base):
    name: str
    description: str
    price: float
    created_at: dt
    updated_at: dt
