from datetime import datetime as dt
from typing import Optional, List
from pydantic import BaseModel

from ..utils.schemaHelper import Base, as_form

class LabResultBase(Base):
    specimen : Optional[str] = None
    result : Optional[str] = None
    reference : Optional[str] = None
    unit : Optional[str] = None
    detailed_result : Optional[str] = None

    status: Optional[str] = None
    is_active: Optional[str] = None


@as_form
class CreateLabResult(LabResultBase):
    pass


class LabResult(LabResultBase):
    id: str
    created_at: Optional[dt] = None
    updated_at: Optional[dt] = None

class OutLabResults(Base):
    data: List[LabResult]
    error: bool
    message: str

class OutLabResult(Base):
    data: LabResult
    error: bool
    message: str