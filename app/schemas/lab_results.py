from datetime import datetime as dt
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
    status: str




class CreateLabResults(LabResultsBase):
    pass


class LabResults(Base):
    specimen : str
    result : str
    reference : str
    unit : str
    detailed_result : str
    status: str
    created_at: dt
    updated_at: dt
