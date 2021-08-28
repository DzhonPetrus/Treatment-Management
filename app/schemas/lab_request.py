from datetime import datetime as dt
from typing import Optional, Text, TextIO
from pydantic import BaseModel

class Base(BaseModel):
    class Config():
        orm_mode = True


class LabRequestBase(Base):
    lab_tests_id : str
    lab_requests_id : str

    status: str




class CreateLabRequest(LabRequestBase):
    pass


class LabRequest(Base):
    lab_tests : str
    lab_requests : str    
    created_at: Optional[dt]
    updated_at: Optional[dt]