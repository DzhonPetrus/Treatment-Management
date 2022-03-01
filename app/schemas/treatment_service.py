from datetime import datetime as dt
from typing import Optional, List
from pydantic import BaseModel
from ..utils.schemaHelper import Base, as_form


from .user import *
from .treatment_type import *

class Treatment_serviceBase(Base):
    treatment_types_id: Optional[str] = None
    treatment_service_name: Optional[str] = None
    description: Optional[str] = None
    unit_price: Optional[float] = None
    is_active: Optional[str] = None

    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    creator: Optional[UserBase] = None
    updator: Optional[UserBase] = None
    created_at: Optional[dt] = None
    updated_at: Optional[dt] = None
    treatment_type_info: Optional[Treatment_typeBase] = None

@as_form
class CreateTreatment_service(Treatment_serviceBase):
    pass


class Treatment_service(Treatment_serviceBase):
    id: str


class OutTreatment_services(Base):
    data: List[Treatment_service]
    error: bool
    message: str

class OutTreatment_service(Base):
    data: Treatment_service
    error: bool
    message: str
