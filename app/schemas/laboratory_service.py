from datetime import datetime as dt
from typing import Optional, List
from pydantic import BaseModel
from ..utils.schemaHelper import Base, as_form


from .user import *
from .laboratory_type import *

class Laboratory_serviceBase(Base):
    lab_test_types_id: Optional[str] = None
    lab_service_name: Optional[str] = None
    description: Optional[str] = None
    unit_price: Optional[float] = None
    is_active: Optional[str] = None

    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    creator: Optional[UserBase] = None
    updator: Optional[UserBase] = None
    created_at: Optional[dt] = None
    updated_at: Optional[dt] = None
    laboratory_type_info: Optional[Laboratory_typeBase] = None

@as_form
class CreateLaboratory_service(Laboratory_serviceBase):
    pass


class Laboratory_service(Laboratory_serviceBase):
    id: str


class OutLaboratory_services(Base):
    data: List[Laboratory_service]
    error: bool
    message: str

class OutLaboratory_service(Base):
    data: Laboratory_service
    error: bool
    message: str
