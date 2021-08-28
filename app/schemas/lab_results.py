from datetime import datetime as dt
from typing import Optional
from pydantic import BaseModel

class Base(BaseModel):
    class Config():
        orm_mode = True


class LabResultsBase(Base):
    specimen : str
    result : str
    reference : str
    unit : str
    detailed_result : str
    status: Optional[str]




class CreateLabResults(LabResultsBase):
    pass


class LabResults(Base):
    specimen : str
    result : str
    reference : str
    unit : str
    detailed_result : str
    status: Optional[str]
    created_at: Optional[dt]
    updated_at: Optional[dt]
