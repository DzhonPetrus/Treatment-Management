from datetime import datetime as dt
from typing import Optional, List, Any
from pydantic import BaseModel
from ..utils.schemaHelper import Base, as_form


from .user import *
# from .treatment_service import *

class Treatment_typeBase(Base):
    treatment_type_name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    creator: Optional[UserBase] = None
    updator: Optional[UserBase] = None
    created_at: Optional[dt] = None
    updated_at: Optional[dt] = None

@as_form
class CreateTreatment_type(Treatment_typeBase):
    pass


class Treatment_type(Treatment_typeBase):
    id: str
    # treatment_service_name: Optional[List[TreatmentServiceNameBase]] = None
    treatment_service_name: Optional[List[Any]] = None


class OutTreatment_types(Base):
    data: List[Treatment_type]
    error: bool
    message: str

class OutTreatment_type(Base):
    data: Treatment_type
    error: bool
    message: str