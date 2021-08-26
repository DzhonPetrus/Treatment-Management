from datetime import datetime as dt
from typing import Text, TextIO
from pydantic import BaseModel

class Base(BaseModel):
    class Config():
        orm_mode = True


class LabRequestBase(Base):

    status: str




class CreateLabRequest(LabRequestBase):
    pass


class LabRequest(LabRequestBase):
    created_at: dt
    updated_at: dt
