from datetime import datetime as dt
from typing import Optional, List
from pydantic import BaseModel


from ..utils.schemaHelper import Base, as_form
from .lab_request import *
from .user import *

class LabResultBase(Base):
    lab_request_id : Optional[str] = None
    specimen : Optional[str] = None
    result : Optional[str] = None
    reference : Optional[str] = None
    unit : Optional[str] = None
    detailed_result : Optional[str] = None

    lab_result_no : Optional[str] = None
    comments : Optional[str] = None

    ordered : Optional[str] = None
    dt_requested: Optional[dt] = None
    dt_received: Optional[dt] = None
    dt_reported: Optional[dt] = None

    status: Optional[str] = None
    is_active: Optional[str] = None

    creator: Optional[UserBase] = None
    updator: Optional[UserBase] = None
    created_at: Optional[dt] = None
    updated_at: Optional[dt] = None

@as_form
class CreateLabResult(LabResultBase):
    pass


class LabResult(LabResultBase):
    id: str
    lab_request: Optional[LabRequest] = None

class OutLabResults(Base):
    data: List[LabResult]
    error: bool
    message: str

class OutLabResult(Base):
    data: LabResult
    error: bool
    message: str
