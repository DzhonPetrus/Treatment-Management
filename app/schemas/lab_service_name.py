from datetime import datetime as dt
from typing import Optional, List
from pydantic import BaseModel
from ..utils.schemaHelper import Base, as_form


from .user import *
from .lab_test_type import *

class LabServiceNameBase(Base):
    lab_test_types_id: Optional[str] = None
    lab_service_name: Optional[str] = None
    description: Optional[str] = None
    unit_price: Optional[float] = None
    status: Optional[str] = None

    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    creator: Optional[UserBase] = None
    updator: Optional[UserBase] = None
    created_at: Optional[dt] = None
    updated_at: Optional[dt] = None
    lab_test_type_info: Optional[Laboratory_typeBase] = None

@as_form
class CreateLabServiceName(LabServiceNameBase):
    pass


class LabServiceName(LabServiceNameBase):
    id: str


class OutLabServiceNames(Base):
    data: List[LabServiceName]
    error: bool
    message: str

class OutLabServiceName(Base):
    data: LabServiceName
    error: bool
    message: str
